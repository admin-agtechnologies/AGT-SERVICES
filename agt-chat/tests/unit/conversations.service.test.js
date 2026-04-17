/**
 * Tests unitaires — ConversationsService
 */
const conversationsService = require('../../src/modules/conversations/conversations.service');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const capabilitiesService = require('../../src/modules/capabilities/capabilities.service');
const AppError = require('../../src/common/errors/AppError');

jest.mock('../../src/modules/conversations/conversations.repository');
jest.mock('../../src/modules/capabilities/capabilities.service');

const defaultCaps = {
  direct_enabled: true, channels_enabled: true, max_channel_members: 500,
  transfer_enabled: false, reactions_enabled: true, typing_enabled: true,
  presence_enabled: true, read_receipts_enabled: true, message_edit_enabled: true,
  message_delete_enabled: true, message_search_enabled: true, max_message_length: 4096,
};

describe('ConversationsService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesService.getCapabilities.mockResolvedValue(defaultCaps);
    capabilitiesService.requireFeature.mockImplementation((caps, feature) => {
      if (caps[feature] === false) throw new AppError('FEATURE_DISABLED', 'disabled', 403);
    });
  });

  describe('createConversation - direct', () => {
    test('crée une conv directe et ajoute les deux participants', async () => {
      conversationsRepo.findDirectBetween.mockResolvedValue(null);
      conversationsRepo.createWithParticipants.mockResolvedValue({ id: 'conv-1', type: 'direct' });

      const result = await conversationsService.createConversation(
        { type: 'direct', platform_id: 'plat-1', participant_ids: ['user-2'] },
        'user-1'
      );

      expect(conversationsRepo.createWithParticipants).toHaveBeenCalledWith(
        expect.objectContaining({ type: 'direct', created_by: 'user-1' }),
        ['user-1', 'user-2']
      );
      expect(result.type).toBe('direct');
    });

    test('retourne la conv existante si déjà existante (anti-doublon)', async () => {
      const existing = { id: 'existing-conv', type: 'direct' };
      conversationsRepo.findDirectBetween.mockResolvedValue(existing);

      const result = await conversationsService.createConversation(
        { type: 'direct', platform_id: 'plat-1', participant_ids: ['user-2'] },
        'user-1'
      );

      expect(conversationsRepo.createWithParticipants).not.toHaveBeenCalled();
      expect(result).toEqual(existing);
    });

    test('échoue si direct_enabled = false', async () => {
      capabilitiesService.requireFeature.mockImplementationOnce(() => {
        throw new AppError('FEATURE_DISABLED', 'disabled', 403);
      });

      await expect(
        conversationsService.createConversation(
          { type: 'direct', platform_id: 'plat-1', participant_ids: ['user-2'] },
          'user-1'
        )
      ).rejects.toThrow(AppError);
    });
  });

  describe('createConversation - channel', () => {
    test('crée un canal avec nom obligatoire', async () => {
      conversationsRepo.createWithParticipants.mockResolvedValue({ id: 'chan-1', type: 'channel' });

      await conversationsService.createConversation(
        { type: 'channel', platform_id: 'plat-1', name: 'general' },
        'user-1'
      );

      expect(conversationsRepo.createWithParticipants).toHaveBeenCalled();
    });

    test('échoue sans nom pour un canal', async () => {
      await expect(
        conversationsService.createConversation(
          { type: 'channel', platform_id: 'plat-1' },
          'user-1'
        )
      ).rejects.toThrow(AppError);
    });

    test('refuse si max_channel_members atteint', async () => {
      const capsLimited = { ...defaultCaps, max_channel_members: 2 };
      capabilitiesService.getCapabilities.mockResolvedValue(capsLimited);

      await expect(
        conversationsService.createConversation(
          { type: 'channel', platform_id: 'plat-1', name: 'chan', participant_ids: ['u2', 'u3'] },
          'user-1'
        )
      ).rejects.toThrow(AppError);
    });
  });

  describe('deleteConversation', () => {
    test('soft delete par owner', async () => {
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', type: 'channel' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'owner' });
      conversationsRepo.softDelete.mockResolvedValue({});

      await conversationsService.deleteConversation('conv-1', 'user-1');
      expect(conversationsRepo.softDelete).toHaveBeenCalledWith('conv-1');
    });

    test('seul admin peut supprimer', async () => {
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', type: 'channel' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });

      await expect(
        conversationsService.deleteConversation('conv-1', 'user-1')
      ).rejects.toThrow(AppError);
    });
  });

  describe('addParticipant', () => {
    test('refuse si max_channel_members atteint', async () => {
      conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'plat-1' });
      conversationsRepo.findParticipant.mockResolvedValue({ role: 'owner' });
      conversationsRepo.countParticipants.mockResolvedValue(500);
      capabilitiesService.getCapabilities.mockResolvedValue({ ...defaultCaps, max_channel_members: 500 });

      await expect(
        conversationsService.addParticipant('conv-1', 'user-1', 'user-new')
      ).rejects.toThrow(AppError);
    });
  });
});
