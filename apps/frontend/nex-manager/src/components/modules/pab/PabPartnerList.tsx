import { useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Building2, Loader2, AlertCircle, RotateCcw, CheckCircle2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { useAuthStore } from '@renderer/stores/authStore'
import { usePartnerCatalogStore } from '@renderer/stores/partnerCatalogStore'
import { usePabCatalogStore, type PabRow } from '@renderer/stores/pabCatalogStore'
import { BaseAgGrid } from '@renderer/components/grids'
import { pabGridConfig } from './pabGridConfig'
import { useState } from 'react'
import PabCreateDialog from './PabCreateDialog'

export default function PabPartnerList(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { openDetail } = usePartnerCatalogStore()

  // Genesis Pattern: parsed catalog held in RAM (Zustand store) across module
  // navigations. First visit in session: store hydrates from IDB. Subsequent
  // visits: instant — no parse, no IDB read, no AG Grid re-init from scratch.
  const partners = usePabCatalogStore((s) => s.partners)
  const syncStatus = usePabCatalogStore((s) => s.syncStatus)
  const error = usePabCatalogStore((s) => s.error)
  const lastSyncedAt = usePabCatalogStore((s) => s.lastSyncedAt)
  const ensureLoaded = usePabCatalogStore((s) => s.ensureLoaded)
  const syncFromServer = usePabCatalogStore((s) => s.syncFromServer)

  const canCreate = checkPermission('PAB', 'create')

  // Create dialog
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  // Filtered count — updated by AG Grid via onDisplayedCountChange
  // (read of internal row-model count, ~1ms).
  const [displayedCount, setDisplayedCount] = useState<number | null>(null)

  useEffect(() => {
    void ensureLoaded()
  }, [ensureLoaded])

  const handleRowDoubleClick = useCallback(
    (row: PabRow): void => {
      openDetail(row.partner_id)
    },
    [openDetail]
  )

  const handleCreated = useCallback((): void => {
    setCreateDialogOpen(false)
    void syncFromServer()
  }, [syncFromServer])

  // First-paint loading state — only when store is empty AND fetching
  const isInitialLoad = partners.length === 0 && syncStatus === 'fetching'

  // Build status badge
  let statusLabel = ''
  let statusColor = 'text-gray-400 dark:text-gray-500'
  let StatusIcon = CheckCircle2
  if (syncStatus === 'cache-hit') {
    statusLabel = 'Z cache'
    statusColor = 'text-blue-500 dark:text-blue-400'
  } else if (syncStatus === 'fetching' && partners.length > 0) {
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
            onClick={() => void syncFromServer()}
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
      {!isInitialLoad && !error && partners.length > 0 && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0 flex items-center gap-3">
          <span>
            Celkom: {partners.length} partnerov
            {displayedCount !== null && displayedCount !== partners.length && (
              <span className="text-blue-600 dark:text-blue-400">
                {' '}· zobrazené: {displayedCount}
              </span>
            )}
          </span>
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

      {/* Error state — only when no data to show */}
      {error && partners.length === 0 && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void syncFromServer()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Skúsiť znova
          </button>
        </div>
      )}

      {/* Loading state — first sync, no data yet */}
      {isInitialLoad ? (
        <div className="flex flex-col items-center justify-center py-16 gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <span className="text-gray-500 dark:text-gray-400">
            Načítavam partnerov…
          </span>
          <span className="text-xs text-gray-400 dark:text-gray-500">
            Prvotná synchronizácia veľkého katalógu môže trvať niekoľko sekúnd
          </span>
        </div>
      ) : partners.length > 0 ? (
        <div data-testid="partner-grid" className="flex-1 min-h-0">
          <BaseAgGrid
            data={partners}
            config={pabGridConfig}
            onRowDoubleClick={handleRowDoubleClick}
            onDisplayedCountChange={setDisplayedCount}
          />
        </div>
      ) : null}

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
