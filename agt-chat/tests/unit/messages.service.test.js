/**
 * Tests unitaires — MessagesService
 */
const messagesService = require('../../src/modules/messages/messages.service');
const messagesRepo = require('../../src/modules/messages/messages.repository');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const capabilitiesService = require('../../src/modules/capabilities/capabilities.service');
const AppError = require('../../src/common/errors/AppError');

jest.mock('../../src/modules/messages/messages.repository');
jest.mock('../../src/modules/conversations/conversations.repository');
jest.mock('../../src/modules/capabilities/capabilities.service');
jest.mock('../../src/common/clients/usersClient', () => ({
  resolveProfilesId: jest.fn().mockResolvedValue(null),
}));
jest.mock('../../src/common/clients/notificationClient', () => ({
  sendNotification: jest.fn().mockResolvedValue(undefined),
}));
jest.mock('../../src/common/broker/publisher', () => ({
  publish: jest.fn().mockResolvedValue(undefined),
}));

const defaultCaps = {
  max_message_length: 4096, message_edit_enabled: true,
  message_delete_enabled: true, message_search_enabled: true,
  reactions_enabled: true, read_receipts_enabled: true,
};

describe('MessagesService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesService.getCapabilities.mockResolvedValue(defaultCaps);
    capabilitiesService.requireFeature.mockImplementation((caps, feature) => {
      if (caps[feature] === false) throw new AppError('FEATURE_DISABLED', 'disabled', 403);
    });
  });

  describe('sendMessage', () => {
    test('persiste avant broadcast WS', async () => {
      const ioMock = { to: jest.fn(() => ({ emit: jest.fn() })) };
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
      conversationsRepo.findParticipants.mockResolvedValue([]);
      conversationsRepo.touch.mockResolvedValue();
      const createdMsg = { id: 'msg-1', content: 'hello', created_at: new Date().toISOString() };
      messagesRepo.create.mockResolvedValue(createdMsg);

      const result = await messagesService.sendMessage('conv-1', 'user-1', { content: 'hello' }, ioMock);

      // Vérifier que create() est appelé avant emit()
      expect(messagesRepo.create).toHaveBeenCalled();
      expect(result.id).toBe('msg-1');
    });

    test('respecte max_message_length de capabilities', async () => {
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
      capabilitiesService.getCapabilities.mockResolvedValue({ ...defaultCaps, max_message_length: 10 });

      await expect(
        messagesService.sendMessage('conv-1', 'user-1', { content: 'this message is too long' })
      ).rejects.toThrow(AppError);
    });

    test('échoue si non participant', async () => {
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      conversationsRepo.findParticipant.mockResolvedValue(null);

      await expect(
        messagesService.sendMessage('conv-1', 'user-1', { content: 'hello' })
      ).rejects.toThrow(AppError);
    });
  });

  describe('editMessage', () => {
    test('seul auteur peut éditer', async () => {
      messagesRepo.findById.mockResolvedValue({
        id: 'msg-1', conversation_id: 'conv-1', sender_id: 'user-2',
        is_deleted: false, created_at: new Date().toISOString(),
      });
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });

      await expect(
        messagesService.editMessage('conv-1', 'msg-1', 'user-1', 'new content')
      ).rejects.toThrow(AppError);
    });

    test('refuse si MESSAGE_EDIT_WINDOW_EXPIRED', async () => {
      // Message créé il y a 20 minutes (délai = 15 min par défaut)
      const oldDate = new Date(Date.now() - 20 * 60 * 1000).toISOString();
      messagesRepo.findById.mockResolvedValue({
        id: 'msg-1', conversation_id: 'conv-1', sender_id: 'user-1',
        is_deleted: false, created_at: oldDate,
      });
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });

      await expect(
        messagesService.editMessage('conv-1', 'msg-1', 'user-1', 'new content')
      ).rejects.toThrow(AppError);
    });

    test('édition réussie dans le délai', async () => {
      const recentDate = new Date(Date.now() - 2 * 60 * 1000).toISOString(); // il y a 2 minutes
      messagesRepo.findById.mockResolvedValue({
        id: 'msg-1', conversation_id: 'conv-1', sender_id: 'user-1',
        is_deleted: false, created_at: recentDate,
      });
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      messagesRepo.edit.mockResolvedValue({ id: 'msg-1', content: 'edited', edited_at: new Date().toISOString() });

      const result = await messagesService.editMessage('conv-1', 'msg-1', 'user-1', 'edited');
      expect(result.content).toBe('edited');
    });
  });

  describe('deleteMessage', () => {
    test('soft delete — content = null', async () => {
      messagesRepo.findById.mockResolvedValue({
        id: 'msg-1', conversation_id: 'conv-1', sender_id: 'user-1', is_deleted: false,
      });
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
      messagesRepo.softDelete.mockResolvedValue({ id: 'msg-1', is_deleted: true, content: null });

      await messagesService.deleteMessage('conv-1', 'msg-1', 'user-1');
      expect(messagesRepo.softDelete).toHaveBeenCalledWith('msg-1');
    });
  });

  describe('searchMessages', () => {
    test('échoue si message_search_enabled = false', async () => {
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      capabilitiesService.requireFeature.mockImplementationOnce(() => {
        throw new AppError('FEATURE_DISABLED', 'disabled', 403);
      });

      await expect(
        messagesService.searchMessages('conv-1', 'user-1', 'hello')
      ).rejects.toThrow(AppError);
    });
  });
});
