// src/lib/calculatorStore.js
import { writable, get } from 'svelte/store';
import { normalizeDistance } from '$lib/distanceService.js'; // ensure path is correct

export const source = writable('');
export const destination = writable('');
export const unit = writable('both'); // 'km' | 'mi' | 'both'

export const apiResult = writable(null);
export const resultBoth = writable(null); // { distance_km, distance_mi }
export const error = writable('');
export const loading = writable(false);

/**
 * Safely get a trimmed string from a store value.
 * Returns '' if the value is null/undefined/not-a-string.
 */
function getTrimmed(store) {
  const v = get(store);
  if (v == null) return '';
  if (typeof v === 'string') return v.trim();
  try {
    return String(v).trim();
  } catch {
    return '';
  }
}

/**
 * Calculate distance using backend. If user selected 'both', send 'km' to backend
 * (server expects 'km' or 'mi') and compute the other unit locally.
 */
export async function calculate() {
  const s = getTrimmed(source);
  const d = getTrimmed(destination);
  const u = get(unit);

  if (!s || !d) {
    error.set('Please enter both source and destination addresses.');
    return;
  }

  error.set('');
  loading.set(true);
  apiResult.set(null);
  resultBoth.set(null);

  try {
    const backendUnit = u === 'both' ? 'km' : u;

    const res = await fetch('/api/distance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: s, destination: d, unit: backendUnit })
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || 'Failed to get distance.');
    }

    const data = await res.json();
    apiResult.set(data);

    // Normalize to ensure both km and mi are present
    const normalized = normalizeDistance(data);
    resultBoth.set(normalized);

    // Optional: persist to /api/history (uncomment if backend supports)
    /*
    try {
      await fetch('/api/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source_text: s,
          dest_text: d,
          distance_km: normalized.distance_km,
          distance_mi: normalized.distance_mi
        })
      });
    } catch (err) {
      console.warn('Failed to write history:', err);
    }
    */

  } catch (err) {
    error.set(err?.message || String(err));
  } finally {
    loading.set(false);
  }
}
