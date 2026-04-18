import { HaversineProvider } from '../../src/infrastructure/providers/eta/haversine.provider';

/**
 * Tests unitaires du provider Haversine.
 * Validé contre des distances réelles connues.
 */
describe('HaversineProvider', () => {
  let provider: HaversineProvider;

  beforeEach(() => {
    provider = new HaversineProvider();
  });

  describe('getDistance()', () => {
    it('calcule la distance Yaoundé → Douala (~240 km)', async () => {
      // Yaoundé : 3.848°N 11.502°E | Douala : 4.050°N 9.767°E
      const result = await provider.getDistance(3.848, 11.502, 4.050, 9.767);
      // Distance réelle ≈ 195–200 km (vol d'oiseau)
      expect(result.distance_m).toBeGreaterThan(180_000);
      expect(result.distance_m).toBeLessThan(220_000);
    });

    it('retourne 0 pour deux points identiques', async () => {
      const result = await provider.getDistance(3.848, 11.502, 3.848, 11.502);
      expect(result.distance_m).toBe(0);
    });

    it('calcule une courte distance (< 1 km)', async () => {
      // ~111m pour 0.001° de latitude
      const result = await provider.getDistance(3.848, 11.502, 3.849, 11.502);
      expect(result.distance_m).toBeGreaterThan(80);
      expect(result.distance_m).toBeLessThan(150);
    });

    it('retourne une durée estimée positive', async () => {
      const result = await provider.getDistance(3.848, 11.502, 4.050, 9.767);
      expect(result.duration_s).toBeGreaterThan(0);
    });
  });

  describe('getETA()', () => {
    it('retourne un eta_datetime dans le futur', async () => {
      const before = new Date();
      const result = await provider.getETA(3.848, 11.502, 4.050, 9.767);
      const etaDate = new Date(result.eta_datetime);
      expect(etaDate.getTime()).toBeGreaterThan(before.getTime());
    });

    it('retourne eta_seconds > 0 pour deux points différents', async () => {
      const result = await provider.getETA(3.848, 11.502, 4.050, 9.767);
      expect(result.eta_seconds).toBeGreaterThan(0);
    });
  });
});
