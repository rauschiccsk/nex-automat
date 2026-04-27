import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Building2, Loader2, AlertCircle, RotateCcw, CheckCircle2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { usePartnerCatalogStore } from '@renderer/stores/partnerCatalogStore'
import { BaseAgGrid } from '@renderer/components/grids'
import {
  getCachedItems,
  setCachedItems,
  getCachedEtag,
  getCachedMeta,
} from '@renderer/lib/catalogCache'
import { pabGridConfig } from './pabGridConfig'
import type { PartnerCatalog, PartnerCatalogListResponse } from '@renderer/types/pab'
import PabCreateDialog from './PabCreateDialog'

const MAX_FETCH = 1_000_000
const CATALOG = 'pab' as const

type SyncStatus = 'idle' | 'cache-hit' | 'fetching' | 'fresh' | 'error'

export default function PabPartnerList(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const { openDetail } = usePartnerCatalogStore()

  const canCreate = checkPermission('PAB', 'create')

  // Genesis Pattern: load from IndexedDB cache first (instant), then check
  // server ETag in background. If stale, re-fetch and apply update.
  const [partners, setPartners] = useState<PartnerCatalog[]>([])
  const [loading, setLoading] = useState(true)  // first paint only
  const [syncStatus, setSyncStatus] = useState<SyncStatus>('idle')
  const [error, setError] = useState<string | null>(null)
  const [lastSyncedAt, setLastSyncedAt] = useState<number | null>(null)

  // Create dialog
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  // Hydrate from cache on mount, then check freshness
  useEffect(() => {
    let cancelled = false

    const init = async (): Promise<void> => {
      // 1. Try IndexedDB cache first — instant if hit
      try {
        const cached = await getCachedItems<PartnerCatalog>(CATALOG)
        if (cached && !cancelled) {
          setPartners(cached)
          setLoading(false)
          setSyncStatus('cache-hit')
          const meta = await getCachedMeta(CATALOG)
          if (meta) setLastSyncedAt(meta.fetchedAt)
        }
      } catch (e) {
        // Cache read failed (corrupted DB?) — fall through to network fetch
        console.warn('PAB cache read failed, falling back to network', e)
      }

      // 2. Check freshness via lightweight ETag endpoint
      let serverEtag: string
      try {
        const res = await api.getPabEtag()
        serverEtag = res.etag
      } catch (e) {
        // ETag failed — if we have cache, keep showing it; if not, surface error
        if (cancelled) return
        const err = e as ApiError
        if (partners.length === 0) {
          setError(err.message || 'Nepodarilo sa načítať partnerov')
          setLoading(false)
        }
        setSyncStatus('error')
        return
      }

      // 3. Compare with cached ETag — skip re-fetch if matching
      const cachedEtag = await getCachedEtag(CATALOG)
      if (cachedEtag === serverEtag && partners.length > 0) {
        setSyncStatus('fresh')
        return
      }

      // 4. Stale (or missing) — fetch full catalog and update cache
      if (cancelled) return
      setSyncStatus('fetching')
      try {
        const res: PartnerCatalogListResponse = await api.getPabPartners({
          limit: MAX_FETCH,
          offset: 0,
          sort_by: 'partner_name',
          sort_order: 'asc',
        })
        if (cancelled) return
        // Items must have an `id` field for IndexedDB keyPath; PAB uses
        // partner_id as id.
        const items = res.items.map((p) => ({ ...p, id: p.partner_id }))
        setPartners(items)
        setLoading(false)
        setLastSyncedAt(Date.now())
        await setCachedItems(CATALOG, items, serverEtag)
        if (cachedEtag) {
          // We updated existing cache silently — toast user that something changed
          addToast(`Katalóg partnerov bol aktualizovaný (${items.length} záznamov)`, 'info')
        }
        setSyncStatus('fresh')
      } catch (e) {
        if (cancelled) return
        const err = e as ApiError
        setError(err.message || 'Sync zlyhal')
        setSyncStatus('error')
        // Keep cache-hit data on screen if we had it; just flag error
        if (partners.length === 0) setLoading(false)
      }
    }

    void init()
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Manual force-refresh — bypasses ETag, always re-fetches
  const forceRefresh = useCallback(async (): Promise<void> => {
    setSyncStatus('fetching')
    try {
      const etagRes = await api.getPabEtag()
      const res: PartnerCatalogListResponse = await api.getPabPartners({
        limit: MAX_FETCH,
        offset: 0,
        sort_by: 'partner_name',
        sort_order: 'asc',
      })
      const items = res.items.map((p) => ({ ...p, id: p.partner_id }))
      setPartners(items)
      setLastSyncedAt(Date.now())
      await setCachedItems(CATALOG, items, etagRes.etag)
      setSyncStatus('fresh')
      addToast('Katalóg partnerov obnovený', 'success')
    } catch (e) {
      const err = e as ApiError
      setError(err.message || 'Refresh zlyhal')
      setSyncStatus('error')
    }
  }, [addToast])

  const handleRowDoubleClick = useCallback(
    (partner: PartnerCatalog & { id: number }): void => {
      openDetail(partner.partner_id)
    },
    [openDetail]
  )

  const handleCreated = useCallback((): void => {
    setCreateDialogOpen(false)
    void forceRefresh()
  }, [forceRefresh])

  // Map data for AG Grid (requires `id` field — already added during cache write)
  const gridData = partners as Array<PartnerCatalog & { id: number }>

  // Build status indicator label + color
  let statusLabel = ''
  let statusColor = 'text-gray-400 dark:text-gray-500'
  let StatusIcon = CheckCircle2
  if (syncStatus === 'cache-hit') {
    statusLabel = 'Z cache'
    statusColor = 'text-blue-500 dark:text-blue-400'
  } else if (syncStatus === 'fetching') {
    statusLabel = 'Synchronizujem…'
    statusColor = 'text-blue-500 dark:text-blue-400'
    StatusIcon = Loader2
  } else if (syncStatus === 'fresh') {
    statusLabel = 'Aktuálne'
    statusColor = 'text-green-600 dark:text-green-400'
  } else if (syncStatus === 'error') {
    statusLabel = 'Sync chyba'
    statusColor = 'text-red-500 dark:text-red-400'
    StatusIcon = AlertCircle
  }

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Building2 className="h-6 w-6" />
          Katalóg partnerov
        </h1>
        <div className="flex items-center gap-3">
          <button
            onClick={() => void forceRefresh()}
            disabled={syncStatus === 'fetching'}
            title="Vynútiť obnovenie zo servera"
            className={cn(
              'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
              'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          >
            <RotateCcw
              className={cn('h-4 w-4', syncStatus === 'fetching' && 'animate-spin')}
            />
            Obnoviť
          </button>

          {canCreate && (
            <button
              data-testid="create-partner-button"
              onClick={() => setCreateDialogOpen(true)}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700'
              )}
            >
              <Plus className="h-4 w-4" />
              Nový partner
            </button>
          )}
        </div>
      </div>

      {/* Count + sync status */}
      {!loading && !error && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0 flex items-center gap-3">
          <span>Celkom: {partners.length} partnerov</span>
          {statusLabel && (
            <span className={cn('flex items-center gap-1.5', statusColor)}>
              <StatusIcon
                className={cn('h-3.5 w-3.5', syncStatus === 'fetching' && 'animate-spin')}
              />
              {statusLabel}
              {lastSyncedAt && syncStatus !== 'fetching' && (
                <span className="text-gray-400 dark:text-gray-500">
                  (sync {formatRelativeTime(lastSyncedAt)})
                </span>
              )}
            </span>
          )}
        </div>
      )}

      {/* Error state — shown only if we have NO data to display */}
      {error && partners.length === 0 && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void forceRefresh()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Skúsiť znova
          </button>
        </div>
      )}

      {/* Loading state — only when we have no cache to show */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-16 gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <span className="text-gray-500 dark:text-gray-400">
            Načítavam partnerov…
          </span>
          <span className="text-xs text-gray-400 dark:text-gray-500">
            Prvotná synchronizácia veľkého katalógu môže trvať 10–20 sekúnd
          </span>
        </div>
      ) : (
        <div data-testid="partner-grid" className="flex-1 min-h-0">
          <BaseAgGrid
            data={gridData}
            config={pabGridConfig}
            onRowDoubleClick={handleRowDoubleClick}
          />
        </div>
      )}

      {/* Create Dialog */}
      {createDialogOpen && (
        <PabCreateDialog
          open={createDialogOpen}
          onClose={() => setCreateDialogOpen(false)}
          onCreated={handleCreated}
        />
      )}
    </div>
  )
}

function formatRelativeTime(epochMs: number): string {
  const ageSec = Math.floor((Date.now() - epochMs) / 1000)
  if (ageSec < 60) return 'pred chvíľou'
  if (ageSec < 3600) return `pred ${Math.floor(ageSec / 60)} min`
  if (ageSec < 86400) return `pred ${Math.floor(ageSec / 3600)} h`
  return `pred ${Math.floor(ageSec / 86400)} d`
}
