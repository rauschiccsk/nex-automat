/**
 * In-memory Zustand store for the parsed PAB partner catalog.
 *
 * Genesis Performance Pattern (Phase J.5.b) — keeps the parsed array of
 * 250k+ partner records in RAM across module navigations within one
 * browser session. Eliminates the JSON.parse(80MB) + AG Grid re-init
 * cost on every component mount.
 *
 * Cache hierarchy (in latency order):
 *   1. RAM (this store, parsed array)         <50ms read
 *   2. IndexedDB (lib/catalogCache, blob)     ~1-2s read+parse
 *   3. Server (/api/pab/partners full)        ~5s end-to-end
 *
 * On first PAB open in a session: load from IDB → parse → store. Subsequent
 * opens read directly from `partners` (already parsed, ready for AG Grid).
 *
 * Also runs a background ETag check (rate-limited to one per
 * ETAG_CHECK_INTERVAL_MS to avoid spamming the server when the user clicks
 * back and forth between modules) and triggers a re-sync if stale.
 *
 * On logout call clear() to wipe RAM (IDB also wiped via clearAllCaches in
 * authStore).
 */

import { create } from 'zustand'
import { api, type ApiError } from '@renderer/lib/api'
import {
  getCachedItems,
  setCachedItems,
  getCachedMeta,
  upsertCachedItem,
  removeCachedItem,
} from '@renderer/lib/catalogCache'
import type { PartnerCatalog } from '@renderer/types/pab'

const MAX_FETCH = 1_000_000
const CATALOG = 'pab' as const
const ETAG_CHECK_INTERVAL_MS = 30_000

/** AG Grid wants `id`; we duplicate partner_id into id at load time. */
export type PabRow = PartnerCatalog & { id: number }

export type SyncStatus =
  | 'idle' // never loaded
  | 'cache-hit' // RAM or IDB hit, no fresh check yet
  | 'fetching' // network sync in progress
  | 'fresh' // ETag verified equal OR fresh data loaded
  | 'error' // last sync attempt failed

interface PabCatalogState {
  partners: PabRow[]
  etag: string | null
  lastSyncedAt: number | null
  lastEtagCheckAt: number | null
  syncStatus: SyncStatus
  error: string | null

  /**
   * Idempotent entry point: ensure store has data, kicking off sync as
   * needed. Called by PabPartnerList on mount. Behavior:
   *   - RAM hit (loaded recently) → no-op
   *   - RAM hit (stale ETag check)→ background ETag re-check
   *   - RAM miss, IDB hit         → render IDB data + background ETag check
   *   - RAM miss, IDB miss        → full network sync
   */
  ensureLoaded: () => Promise<void>

  /** Force a fresh full sync from the server, regardless of ETag. */
  syncFromServer: () => Promise<void>

  /** Patch one partner in RAM + IDB after CRUD update/create. */
  upsertPartner: (partner: PartnerCatalog) => Promise<void>

  /** Remove one partner from RAM + IDB after delete. */
  removePartner: (partnerId: number) => Promise<void>

  /** Wipe RAM (used on logout). IDB is wiped separately by authStore. */
  clear: () => void
}

export const usePabCatalogStore = create<PabCatalogState>((set, get) => ({
  partners: [],
  etag: null,
  lastSyncedAt: null,
  lastEtagCheckAt: null,
  syncStatus: 'idle',
  error: null,

  ensureLoaded: async () => {
    const state = get()

    // Skip-fast: RAM hit + recent ETag check
    if (
      state.partners.length > 0 &&
      state.lastEtagCheckAt &&
      Date.now() - state.lastEtagCheckAt < ETAG_CHECK_INTERVAL_MS
    ) {
      return
    }

    // RAM miss → try IDB hydration first (instant render path)
    if (state.partners.length === 0) {
      try {
        const cached = await getCachedItems<PabRow>(CATALOG)
        const meta = await getCachedMeta(CATALOG)
        if (cached) {
          set({
            partners: cached,
            etag: meta?.etag ?? null,
            lastSyncedAt: meta?.fetchedAt ?? null,
            syncStatus: 'cache-hit',
          })
        }
      } catch (e) {
        // Corrupted DB or quota — fall through to network
        console.warn('PAB IDB cache read failed', e)
      }
    }

    // Background ETag check (cheap, ~50ms)
    let serverEtag: string
    try {
      const etagRes = await api.getPabEtag()
      serverEtag = etagRes.etag
      set({ lastEtagCheckAt: Date.now() })
    } catch (e) {
      const err = e as ApiError
      // ETag failed: keep showing whatever we have; only surface error if no data
      if (get().partners.length === 0) {
        set({ error: err.message || 'Nepodarilo sa načítať partnerov', syncStatus: 'error' })
      } else {
        set({ syncStatus: 'error' })
      }
      return
    }

    // ETag matches → cache is fresh, nothing more to do
    if (serverEtag === get().etag && get().partners.length > 0) {
      set({ syncStatus: 'fresh' })
      return
    }

    // Stale or empty → full sync
    await get().syncFromServer()
  },

  syncFromServer: async () => {
    if (get().syncStatus === 'fetching') return // dedupe concurrent calls
    const hadData = get().partners.length > 0
    set({ syncStatus: 'fetching', error: null })
    try {
      const etagRes = await api.getPabEtag()
      const res = await api.getPabPartners({
        limit: MAX_FETCH,
        offset: 0,
        sort_by: 'partner_name',
        sort_order: 'asc',
      })
      const items: PabRow[] = res.items.map((p) => ({ ...p, id: p.partner_id }))
      set({
        partners: items,
        etag: etagRes.etag,
        lastSyncedAt: Date.now(),
        lastEtagCheckAt: Date.now(),
        syncStatus: 'fresh',
      })
      // IDB write is async, fire-and-forget — don't block UI on cache persistence.
      // If it fails, ETag check next time will trigger re-sync.
      void setCachedItems(CATALOG, items, etagRes.etag).catch((e) => {
        console.warn('PAB IDB cache write failed', e)
      })
      // Notify of background change (avoid toast on first-ever sync to prevent
      // surprise on cold load — only meaningful when refreshing existing data)
      if (hadData) {
        // import lazy to avoid circular dep
        const { useToastStore } = await import('@renderer/stores/toastStore')
        useToastStore
          .getState()
          .addToast(`Katalóg partnerov bol aktualizovaný (${items.length} záznamov)`, 'info')
      }
    } catch (e) {
      const err = e as ApiError
      set({ error: err.message || 'Sync zlyhal', syncStatus: 'error' })
    }
  },

  upsertPartner: async (partner) => {
    const row: PabRow = { ...partner, id: partner.partner_id }
    const list = get().partners
    const idx = list.findIndex((x) => x.partner_id === partner.partner_id)
    const next = idx >= 0 ? [...list.slice(0, idx), row, ...list.slice(idx + 1)] : [...list, row]
    set({ partners: next })
    // Mirror to IDB (fire-and-forget — ETag mismatch will trigger re-sync if write fails)
    void upsertCachedItem(CATALOG, row).catch((e) => {
      console.warn('PAB IDB upsert failed', e)
    })
  },

  removePartner: async (partnerId) => {
    set({ partners: get().partners.filter((x) => x.partner_id !== partnerId) })
    void removeCachedItem(CATALOG, partnerId).catch((e) => {
      console.warn('PAB IDB remove failed', e)
    })
  },

  clear: () => {
    set({
      partners: [],
      etag: null,
      lastSyncedAt: null,
      lastEtagCheckAt: null,
      syncStatus: 'idle',
      error: null,
    })
  },
}))
