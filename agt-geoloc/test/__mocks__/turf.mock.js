/**
 * Mock @turf/turf pour les tests Jest.
 * Les calculs réels sont testés via les tests d'intégration avec turf compilé.
 */
const point = (coords) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: coords } });
const polygon = (coords) => ({ type: 'Feature', geometry: { type: 'Polygon', coordinates: coords } });

const distance = (from, to, options) => {
  // Implémentation simplifiée Haversine pour les tests
  const R = options?.units === 'meters' ? 6371000 : 6371;
  const [lng1, lat1] = from.geometry.coordinates;
  const [lng2, lat2] = to.geometry.coordinates;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLng/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
};

const booleanPointInPolygon = (pt, poly) => {
  // Ray casting simplifié pour les tests rectangulaires
  const [x, y] = pt.geometry.coordinates;
  const ring = poly.geometry.coordinates[0];
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i];
    const [xj, yj] = ring[j];
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {
      inside = !inside;
    }
  }
  return inside;
};

module.exports = { point, polygon, distance, booleanPointInPolygon };
