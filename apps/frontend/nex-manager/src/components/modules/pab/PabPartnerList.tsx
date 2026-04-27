import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Building2, Loader2, AlertCircle, RotateCcw } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { usePartnerCatalogStore } from '@renderer/stores/partnerCatalogStore'
import { BaseAgGrid } from '@renderer/components/grids'
import { pabGridConfig } from './pabGridConfig'
import type { PartnerCatalog, PartnerCatalogListResponse } from '@renderer/types/pab'
import PabCreateDialog from './PabCreateDialog'

// Sanity guard against runaway DB sizes; matches backend cap.
const MAX_FETCH = 1_000_000

export default function PabPartnerList(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const { openDetail } = usePartnerCatalogStore()

  const canCreate = checkPermission('PAB', 'create')

  // Data state — load full catalog ONCE, AG Grid handles filter/sort
  // client-side via row-model virtualization. Tested up to 250k rows.
  const [allPartners, setAllPartners] = useState<PartnerCatalog[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Create dialog
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  // Fetch ALL partners (single network call, no filters/search server-side).
  // Re-fetch only on explicit refresh or after a CRUD op.
  const fetchPartners = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res: PartnerCatalogListResponse = await api.getPabPartners({
        limit: MAX_FETCH,
        offset: 0,
        sort_by: 'partner_name',
        sort_order: 'asc'
      })
      setAllPartners(res.items)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať partnerov'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [addToast])

  useEffect(() => {
    void fetchPartners()
  }, [fetchPartners])

  const handleRowDoubleClick = useCallback(
    (partner: PartnerCatalog & { id: number }): void => {
      openDetail(partner.partner_id)
    },
    [openDetail]
  )

  const handleCreated = useCallback((): void => {
    setCreateDialogOpen(false)
    void fetchPartners()
  }, [fetchPartners])

  // Map data for AG Grid (requires `id` field)
  const gridData = allPartners.map((p) => ({ ...p, id: p.partner_id }))

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Building2 className="h-6 w-6" />
          Katalóg partnerov
        </h1>
        <div className="flex items-center gap-3">
          {/* Refresh button */}
          <button
            onClick={() => void fetchPartners()}
            disabled={loading}
            title="Obnoviť dáta"
            className={cn(
              'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
              'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          >
            <RotateCcw className={cn('h-4 w-4', loading && 'animate-spin')} />
            Obnoviť
          </button>

          {/* Create button */}
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

      {/* Total count — full count, no narrowing, AG Grid handles per-column filter */}
      {!loading && !error && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0">
          Celkom: {allPartners.length} partnerov
          <span className="ml-2 italic">
            (filter v hlavičke každého stĺpca — okamžité vyhľadávanie)
          </span>
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void fetchPartners()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Skúsiť znova
          </button>
        </div>
      )}

      {/* Loading state */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-16 gap-2">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <span className="text-gray-500 dark:text-gray-400">
            Načítavam partnerov...
          </span>
          <span className="text-xs text-gray-400 dark:text-gray-500">
            Pri veľkých katalógoch (250k+ záznamov) trvá načítanie ~5-15 sekúnd
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
