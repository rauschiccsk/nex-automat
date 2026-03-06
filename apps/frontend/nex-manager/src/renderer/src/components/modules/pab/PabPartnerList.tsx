import { useState, useEffect, useCallback, useRef, type ReactElement } from 'react'
import { Plus, Building2, Loader2, AlertCircle, RotateCcw, Search } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { usePartnerCatalogStore } from '@renderer/stores/partnerCatalogStore'
import { BaseGrid } from '@renderer/components/grids'
import { pabGridConfig } from './pabGridConfig'
import type { PartnerCatalog, PartnerCatalogListResponse } from '@renderer/types/pab'
import PabCreateDialog from './PabCreateDialog'

export default function PabPartnerList(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const {
    searchQuery,
    setSearchQuery,
    filterPartnerClass,
    setFilterPartnerClass,
    filterIsActive,
    setFilterIsActive,
    openDetail
  } = usePartnerCatalogStore()

  const canCreate = checkPermission('PAB', 'create')

  // Data state
  const [partners, setPartners] = useState<PartnerCatalog[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Create dialog
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

  // Debounce search
  const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [debouncedSearch, setDebouncedSearch] = useState(searchQuery)

  useEffect(() => {
    if (searchTimer.current) clearTimeout(searchTimer.current)
    searchTimer.current = setTimeout(() => {
      setDebouncedSearch(searchQuery)
    }, 300)
    return () => {
      if (searchTimer.current) clearTimeout(searchTimer.current)
    }
  }, [searchQuery])

  // Fetch partners
  const fetchPartners = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res: PartnerCatalogListResponse = await api.getPabPartners({
        search: debouncedSearch || undefined,
        partner_class: filterPartnerClass,
        is_active: filterIsActive ?? undefined,
        limit: 10000,
        offset: 0,
        sort_by: 'partner_name',
        sort_order: 'asc'
      })
      setPartners(res.items)
      setTotal(res.total)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať partnerov'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [debouncedSearch, filterPartnerClass, filterIsActive, addToast])

  useEffect(() => {
    void fetchPartners()
  }, [fetchPartners])

  const handleRowDoubleClick = useCallback(
    (partner: PartnerCatalog): void => {
      openDetail(partner.partner_id)
    },
    [openDetail]
  )

  const handleCreated = useCallback((): void => {
    setCreateDialogOpen(false)
    void fetchPartners()
  }, [fetchPartners])

  // Map data for BaseGrid (requires `id` field)
  const gridData = partners.map((p) => ({ ...p, id: p.partner_id }))

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Building2 className="h-6 w-6" />
          Katalóg partnerov
        </h1>
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Hľadať partnera..."
              className={cn(
                'pl-9 pr-3 py-2 rounded-lg border text-sm w-64 outline-none transition-colors',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
              )}
            />
          </div>

          {/* Partner class filter */}
          <select
            value={filterPartnerClass}
            onChange={(e) => setFilterPartnerClass(e.target.value as 'business' | 'retail' | 'guest')}
            className={cn(
              'px-3 py-2 rounded-lg border text-sm outline-none transition-colors',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600 focus:border-blue-500'
            )}
          >
            <option value="business">Obchodní partneri</option>
            <option value="retail">Retail zákazníci</option>
            <option value="guest">Guest zákazníci</option>
          </select>

          {/* Active filter */}
          <select
            value={filterIsActive === null ? '' : String(filterIsActive)}
            onChange={(e) => {
              const v = e.target.value
              setFilterIsActive(v === '' ? null : v === 'true')
            }}
            className={cn(
              'px-3 py-2 rounded-lg border text-sm outline-none transition-colors',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600 focus:border-blue-500'
            )}
          >
            <option value="">Všetci</option>
            <option value="true">Aktívni</option>
            <option value="false">Neaktívni</option>
          </select>

          {/* Create button */}
          {canCreate && (
            <button
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

      {/* Total count */}
      {!loading && !error && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0">
          Celkom: {total} partnerov
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
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <span className="ml-3 text-gray-500 dark:text-gray-400">Načítavam...</span>
        </div>
      ) : (
        <BaseGrid
          data={gridData}
          config={pabGridConfig}
          onRowDoubleClick={handleRowDoubleClick}
          className="flex-1 min-h-0"
        />
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
