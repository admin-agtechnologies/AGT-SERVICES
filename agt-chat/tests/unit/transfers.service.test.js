/**
 * Tests unitaires — TransfersService
 */
const transfersService = require('../../src/modules/transfers/transfers.service');
const transfersRepo = require('../../src/modules/transfers/transfers.repository');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const capabilitiesService = require('../../src/modules/capabilities/capabilities.service');
const { checkPermission } = require('../../src/common/clients/usersClient');
const AppError = require('../../src/common/errors/AppError');

jest.mock('../../src/modules/transfers/transfers.repository');
jest.mock('../../src/modules/conversations/conversations.repository');
jest.mock('../../src/modules/capabilities/capabilities.service');
jest.mock('../../src/common/clients/usersClient', () => ({
  checkPermission: jest.fn(),
  resolveProfilesId: jest.fn().mockResolvedValue(null),
}));
jest.mock('../../src/common/clients/notificationClient', () => ({
  sendNotification: jest.fn().mockResolvedValue(undefined),
}));
jest.mock('../../src/common/broker/publisher', () => ({
  publish: jest.fn().mockResolvedValue(undefined),
}));

describe('TransfersService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesService.getCapabilities.mockResolvedValue({ transfer_enabled: true });
    capabilitiesService.requireFeature.mockImplementation((caps, feature) => {
      if (caps[feature] === false) throw new AppError('FEATURE_DISABLED', 'disabled', 403);
    });
  });

  describe('createTransfer', () => {
    test('crée un transfert avec conversation de type transfer', async () => {
      conversationsRepo.createWithParticipants.mockResolvedValue({ id: 'conv-t', type: 'transfer' });
      transfersRepo.create.mockResolvedValue({ id: 'transfer-1', status: 'pending' });
      conversationsRepo.findParticipants.mockResolvedValue([]);

      const result = await transfersService.createTransfer({
        user_id: 'user-1', platform_id: 'plat-1', bot_history: [], context: {},
      });

      expect(conversationsRepo.createWithParticipants).toHaveBeenCalledWith(
        expect.objectContaining({ type: 'transfer' }),
        ['user-1']
      );
      expect(transfersRepo.create).toHaveBeenCalled();
      expect(result.transfer.id).toBe('transfer-1');
    });

    test('échoue si transfer_enabled = false', async () => {
      capabilitiesService.requireFeature.mockImplementationOnce(() => {
        throw new AppError('FEATURE_DISABLED', 'disabled', 403);
      });

      await expect(
        transfersService.createTransfer({ user_id: 'u', platform_id: 'plat-1' })
      ).rejects.toThrow(AppError);
    });
  });

  describe('takeTransfer', () => {
    test('verrou optimiste : 409 si déjà pris', async () => {
      checkPermission.mockResolvedValue(true);
      // takeOptimistic retourne null si déjà pris
      transfersRepo.takeOptimistic.mockResolvedValue(null);

      await expect(
        transfersService.takeTransfer('transfer-1', 'operator-1', 'plat-1')
      ).rejects.toThrow(AppError);

      await expect(
        transfersService.takeTransfer('transfer-1', 'operator-1', 'plat-1')
      ).rejects.toMatchObject({ httpStatus: 409, code: 'TRANSFER_ALREADY_TAKEN' });
    });

    test('refuse si pas la permission chat:transfer:take', async () => {
      checkPermission.mockResolvedValue(false);

      await expect(
        transfersService.takeTransfer('transfer-1', 'operator-1', 'plat-1')
      ).rejects.toMatchObject({ httpStatus: 403 });
    });

    test('prise en charge réussie', async () => {
      checkPermission.mockResolvedValue(true);
      const taken = { id: 'transfer-1', status: 'taken', operator_id: 'operator-1', conversation_id: 'conv-t' };
      transfersRepo.takeOptimistic.mockResolvedValue(taken);
      conversationsRepo.addParticipant.mockResolvedValue({});

      const result = await transfersService.takeTransfer('transfer-1', 'operator-1', 'plat-1');
      expect(result.status).toBe('taken');
    });
  });

  describe('closeTransfer', () => {
    test('clôture avec statut final correct', async () => {
      const closed = { id: 'transfer-1', status: 'closed', closed_at: new Date().toISOString() };
      transfersRepo.close.mockResolvedValue(closed);

      const result = await transfersService.closeTransfer('transfer-1', 'operator-1');
      expect(result.status).toBe('closed');
    });

    test('échoue si opérateur incorrect', async () => {
      transfersRepo.close.mockResolvedValue(null); // UPDATE WHERE operator_id = ... ne matche pas

      await expect(
        transfersService.closeTransfer('transfer-1', 'wrong-operator')
      ).rejects.toThrow(AppError);
    });
  });

  describe('getPendingTransfers', () => {
    test('retourne uniquement les transferts status=pending', async () => {
      const pending = [{ id: 't1', status: 'pending' }, { id: 't2', status: 'pending' }];
      transfersRepo.findPending.mockResolvedValue(pending);

      const result = await transfersService.getPendingTransfers();
      expect(result).toHaveLength(2);
      result.forEach((t) => expect(t.status).toBe('pending'));
    });
  });
});
