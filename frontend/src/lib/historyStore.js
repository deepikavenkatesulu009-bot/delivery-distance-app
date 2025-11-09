// src/lib/historyStore.js
import { writable } from 'svelte/store';
import { normalizeDistance } from '$lib/distanceService.js'; // adjust if your path differs

export const history = writable([]);
export const loading = writable(false);
export const error = writable('');

/** safe number -> returns number or null */
function safeNum(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

/**
 * Load history from backend, normalize each item to ensure both km & mi exist.
 * Sets history, loading and error stores.
 */
export async function loadHistory() {
  loading.set(true);
  error.set('');
  history.set([]);

  try {
    const res = await fetch('/api/history');

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || 'Failed to load history.');
    }

    const data = await res.json().catch(() => []);

    if (!Array.isArray(data)) {
      throw new Error('Unexpected history format.');
    }

    const normalized = data.map((item) => {
      const norm = normalizeDistance(item || {});
      return {
        source_text: item?.source_text ?? item?.source ?? '[Unknown source]',
        dest_text: item?.dest_text ?? item?.destination ?? '[Unknown destination]',
        distance_km: safeNum(norm.distance_km),
        distance_mi: safeNum(norm.distance_mi),
        created_at: item?.created_at ?? item?.createdAt ?? null,
        __raw: item
      };
    });

    history.set(normalized);
  } catch (err) {
    error.set(err?.message ?? String(err));
  } finally {
    loading.set(false);
  }
}
