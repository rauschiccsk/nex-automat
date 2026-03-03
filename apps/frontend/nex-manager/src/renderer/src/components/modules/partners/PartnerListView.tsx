import { useState, useEffect, useCallback, type ReactElement } from 'react'
import {
  Search,
  Plus,
  Pencil,
  Loader2,
  Building2,
  ChevronUp,
  ChevronDown,
  ChevronsLeft,
  ChevronLeft,
  ChevronRight,
  ChevronsRight,
  AlertCircle,
  RotateCcw,
  X
} from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type {
  Partner,
  PartnerType,
  SortField,
  SortOrder,
  PartnerListResponse
} from '@renderer/types/partner'
import PartnerFormDialog from './PartnerFormDialog'

type ActiveFilter = 'all' | 'active' | 'inactive'
type TypeFilter = 'all' | PartnerType

const TYPE_BADGE: Record<PartnerType, { label: string; cls: string }> = {
  customer: {
    label: 'Odberateľ',
    cls: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
  },
  supplier: {
    label: 'Dodávateľ',
    cls: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
  },
  both: {
    label: 'Oba',
    cls: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
  }
}

const PAGE_SIZES = [25, 50, 100, 200]

export default function PartnerListView(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()

  const canCreate = checkPermission('PAB', 'create')
  const canEdit = checkPermission('PAB', 'edit')

  // ── Data state ──
  const [data, setData] = useState<PartnerListResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // ── Filter / search state ──
  const [searchTerm, setSearchTerm] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [activeFilter, setActiveFilter] = useState<ActiveFilter>('all')
  const [typeFilter, setTypeFilter] = useState<TypeFilter>('all')

  // ── Pagination state ──
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(50)

  // ── Sort state ──
  const [sortBy, setSortBy] = useState<SortField>('code')
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc')

  // ── Dialog state ──
  const [formDialogOpen, setFormDialogOpen] = useState(false)
  const [editingPartner, setEditingPartner] = useState<Partner | null>(null)

  // ── Debounced search ──
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm)
      setPage(1) // reset to page 1 on search change
    }, 300)
    return (): void => clearTimeout(timer)
  }, [searchTerm])

  // Reset to page 1 on filter change
  useEffect(() => {
    setPage(1)
  }, [activeFilter, typeFilter, pageSize])

  // ── Fetch partners ──
  const fetchPartners = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.getPartners({
        search: debouncedSearch || undefined,
        partner_type: typeFilter !== 'all' ? typeFilter : undefined,
        is_active:
          activeFilter === 'active' ? true : activeFilter === 'inactive' ? false : undefined,
        page,
        page_size: pageSize,
        sort_by: sortBy,
        sort_order: sortOrder
      })
      setData(res)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať partnerov'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [debouncedSearch, activeFilter, typeFilter, page, pageSize, sortBy, sortOrder, addToast])

  useEffect(() => {
    void fetchPartners()
  }, [fetchPartners])

  // ── Sort handler ──
  const handleSort = useCallback(
    (field: SortField): void => {
      if (sortBy === field) {
        setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'))
      } else {
        setSortBy(field)
        setSortOrder('asc')
      }
    },
    [sortBy]
  )

  // ── Dialog handlers ──
  const handleCreate = useCallback((): void => {
    setEditingPartner(null)
    setFormDialogOpen(true)
  }, [])

  const handleEdit = useCallback((partner: Partner): void => {
    setEditingPartner(partner)
    setFormDialogOpen(true)
  }, [])

  const handleFormClose = useCallback((): void => {
    setFormDialogOpen(false)
    setEditingPartner(null)
  }, [])

  const handleFormSaved = useCallback((): void => {
    setFormDialogOpen(false)
    setEditingPartner(null)
    void fetchPartners()
  }, [fetchPartners])

  // ── Derived values ──
  const partners = data?.items ?? []
  const total = data?.total ?? 0
  const totalPages = data?.total_pages ?? 1
  const startItem = total > 0 ? (page - 1) * pageSize + 1 : 0
  const endItem = Math.min(page * pageSize, total)

  // ── Active filter chips ──
  const activeChips: { label: string; onRemove: () => void }[] = []
  if (typeFilter !== 'all') {
    activeChips.push({
      label: TYPE_BADGE[typeFilter].label,
      onRemove: () => setTypeFilter('all')
    })
  }
  if (activeFilter !== 'all') {
    activeChips.push({
      label: activeFilter === 'active' ? 'Aktívny' : 'Neaktívny',
      onRemove: () => setActiveFilter('all')
    })
  }

  // ── Sort icon helper ──
  const SortIcon = ({ field }: { field: SortField }): ReactElement | null => {
    if (sortBy !== field) return null
    return sortOrder === 'asc' ? (
      <ChevronUp className="h-3.5 w-3.5 inline ml-1" />
    ) : (
      <ChevronDown className="h-3.5 w-3.5 inline ml-1" />
    )
  }

  const sortableThClass =
    'cursor-pointer select-none hover:text-gray-900 dark:hover:text-white transition-colors'

  return (
    <div className="flex flex-col gap-4">
      {/* ── Header row ── */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Building2 className="h-6 w-6" />
          Partneri
        </h1>
        {canCreate && (
          <button
            onClick={handleCreate}
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

      {/* ── Filter row ── */}
      <div className="flex flex-wrap items-center gap-3">
        {/* Search */}
        <div className="relative flex-1 min-w-[200px] max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Hľadať kód, názov, IČO, mesto, email..."
            className={cn(
              'w-full pl-10 pr-4 py-2 rounded-lg border text-sm transition-colors outline-none',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600',
              'placeholder-gray-400 dark:placeholder-gray-500',
              'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
            )}
          />
        </div>

        {/* Type filter */}
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value as TypeFilter)}
          className={cn(
            'px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
            'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
            'border-gray-300 dark:border-gray-600',
            'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
          )}
        >
          <option value="all">Všetci</option>
          <option value="customer">Odberatelia</option>
          <option value="supplier">Dodávatelia</option>
          <option value="both">Oba</option>
        </select>

        {/* Active/Inactive toggle */}
        <div className="flex rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden text-sm">
          {(['all', 'active', 'inactive'] as ActiveFilter[]).map((f) => (
            <button
              key={f}
              onClick={() => setActiveFilter(f)}
              className={cn(
                'px-3 py-2 transition-colors',
                activeFilter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600'
              )}
            >
              {f === 'all' ? 'Všetci' : f === 'active' ? 'Aktívni' : 'Neaktívni'}
            </button>
          ))}
        </div>

        {/* Active filter chips */}
        {activeChips.length > 0 && (
          <div className="flex items-center gap-2">
            {activeChips.map((chip) => (
              <span
                key={chip.label}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
              >
                {chip.label}
                <button
                  onClick={chip.onRemove}
                  className="hover:bg-blue-200 dark:hover:bg-blue-800 rounded-full p-0.5 transition-colors"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* ── Error state ── */}
      {error && !loading && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
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

      {/* ── Table ── */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : partners.length === 0 && !error ? (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <Building2 className="h-12 w-12 text-gray-300 dark:text-gray-600 mb-3" />
          <p className="text-gray-500 dark:text-gray-400">Žiadni partneri</p>
        </div>
      ) : partners.length > 0 ? (
        <>
          <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                  <th
                    className={cn(
                      'px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[100px]',
                      sortableThClass
                    )}
                    onClick={() => handleSort('code')}
                  >
                    Kód
                    <SortIcon field="code" />
                  </th>
                  <th
                    className={cn(
                      'px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400',
                      sortableThClass
                    )}
                    onClick={() => handleSort('name')}
                  >
                    Názov
                    <SortIcon field="name" />
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[120px] hidden lg:table-cell">
                    IČO
                  </th>
                  <th
                    className={cn(
                      'px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[150px] hidden md:table-cell',
                      sortableThClass
                    )}
                    onClick={() => handleSort('city')}
                  >
                    Mesto
                    <SortIcon field="city" />
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[100px]">
                    Typ
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[80px]">
                    Aktívny
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[130px] hidden xl:table-cell">
                    Telefón
                  </th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400 w-[180px] hidden xl:table-cell">
                    Email
                  </th>
                  {canEdit && (
                    <th className="px-4 py-3 text-right font-medium text-gray-600 dark:text-gray-400 w-[80px]">
                      Akcie
                    </th>
                  )}
                </tr>
              </thead>
              <tbody>
                {partners.map((partner) => {
                  const typeBadge = TYPE_BADGE[partner.partner_type] ?? TYPE_BADGE.customer
                  return (
                    <tr
                      key={partner.id}
                      className="border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                    >
                      <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                        {partner.code}
                      </td>
                      <td className="px-4 py-3 text-gray-700 dark:text-gray-300">
                        {partner.name}
                      </td>
                      <td className="px-4 py-3 text-gray-500 dark:text-gray-400 hidden lg:table-cell">
                        {partner.company_id || '—'}
                      </td>
                      <td className="px-4 py-3 text-gray-500 dark:text-gray-400 hidden md:table-cell">
                        {partner.city || '—'}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={cn(
                            'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                            typeBadge.cls
                          )}
                        >
                          {typeBadge.label}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={cn(
                            'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                            partner.is_active
                              ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                              : 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400'
                          )}
                        >
                          {partner.is_active ? 'Aktívny' : 'Neaktívny'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-500 dark:text-gray-400 hidden xl:table-cell">
                        {partner.phone || '—'}
                      </td>
                      <td className="px-4 py-3 text-gray-500 dark:text-gray-400 hidden xl:table-cell">
                        {partner.email || '—'}
                      </td>
                      {canEdit && (
                        <td className="px-4 py-3">
                          <div className="flex items-center justify-end">
                            <button
                              onClick={() => handleEdit(partner)}
                              className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                              title="Upraviť"
                            >
                              <Pencil className="h-4 w-4" />
                            </button>
                          </div>
                        </td>
                      )}
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* ── Pagination bar ── */}
          <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <span>
                Zobrazených {startItem}–{endItem} z {total}
              </span>
              <select
                value={pageSize}
                onChange={(e) => setPageSize(Number(e.target.value))}
                className={cn(
                  'px-2 py-1 rounded border text-sm outline-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'border-gray-300 dark:border-gray-600',
                  'focus:border-blue-500 focus:ring-1 focus:ring-blue-500/20'
                )}
              >
                {PAGE_SIZES.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-1">
              <button
                onClick={() => setPage(1)}
                disabled={page <= 1}
                className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Prvá"
              >
                <ChevronsLeft className="h-4 w-4" />
              </button>
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Predchádzajúca"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <span className="px-3 py-1 text-sm font-medium">
                Strana {page} z {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Nasledujúca"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
              <button
                onClick={() => setPage(totalPages)}
                disabled={page >= totalPages}
                className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Posledná"
              >
                <ChevronsRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </>
      ) : null}

      {/* ── Dialog ── */}
      {formDialogOpen && (
        <PartnerFormDialog
          open={formDialogOpen}
          onClose={handleFormClose}
          onSaved={handleFormSaved}
          partner={editingPartner}
        />
      )}
    </div>
  )
}
