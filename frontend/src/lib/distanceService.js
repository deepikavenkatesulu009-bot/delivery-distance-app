// src/lib/distanceService.js

// Convert kilometers -> miles
export function kmToMiles(km) {
    if (km == null || isNaN(Number(km))) return null;
    return Number(km) * 0.62137119223733;
  }
  
  // Convert miles -> kilometers
  export function milesToKm(mi) {
    if (mi == null || isNaN(Number(mi))) return null;
    return Number(mi) * 1.609344;
  }
  
  /**
   * Normalize an API result to ensure both units exist.
   * Accepts different shapes:
   * - { distance: number, unit: 'km'|'mi'|'both' }
   * - or { distance_km: number, distance_mi: number }
   *
   * Returns: { distance_km: number, distance_mi: number }
   */
  export function normalizeDistance(apiResult = {}) {
    // if both provided already
    if (apiResult.distance_km != null && apiResult.distance_mi != null) {
      return {
        distance_km: Number(apiResult.distance_km),
        distance_mi: Number(apiResult.distance_mi)
      };
    }
  
    // if distance + unit provided
    if (apiResult.distance != null && apiResult.unit) {
      const d = Number(apiResult.distance);
      const unit = apiResult.unit.toLowerCase();
      if (unit === 'km' || unit === 'k' || unit === 'kilometers' || unit === 'kilometres') {
        return {
          distance_km: d,
          distance_mi: kmToMiles(d)
        };
      } else if (unit === 'mi' || unit === 'miles') {
        return {
          distance_km: milesToKm(d),
          distance_mi: d
        };
      }
    }
  
    // fallback: attempt to read distance_km or distance_mi keys
    if (apiResult.distance_km != null) {
      return {
        distance_km: Number(apiResult.distance_km),
        distance_mi: kmToMiles(Number(apiResult.distance_km))
      };
    }
    if (apiResult.distance_mi != null) {
      return {
        distance_km: milesToKm(Number(apiResult.distance_mi)),
        distance_mi: Number(apiResult.distance_mi)
      };
    }
  
    // nothing usable
    return { distance_km: null, distance_mi: null };
  }
  