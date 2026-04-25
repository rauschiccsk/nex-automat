import { useState, useEffect, useCallback, useRef, type ReactElement } from 'react'
import { ShoppingCart, Loader2, AlertCircle, RotateCcw, Search } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import { useEshopStore } from '@renderer/stores/eshopStore'
import { BaseGrid } from '@renderer/components/grids'
import { eshopOrderGridConfig } from './eshopGridConfigs'
import type { EshopOrder, EshopOrderListResponse } from '@renderer/types/eshop'

/** Order status badge colors. */
const ORDER_STATUS_COLORS: Record<string, string> = {
  new: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
  paid: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  processing: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  shipped: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
  delivered: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
  cancelled: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  returned: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
}

/** Payment status badge colors. */
const PAYMENT_STATUS_COLORS: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
  paid: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  failed: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  authorized: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
}

const ORDER_STATUS_OPTIONS = [
  { value: '', label: 'Všetky stavy' },
  { value: 'new', label: 'Nová' },
  { value: 'paid', label: 'Zaplatená' },
  { value: 'processing', label: 'Spracováva sa' },
  { value: 'shipped', label: 'Odoslaná' },
  { value: 'delivered', label: 'Doručená' },
  { value: 'cancelled', label: 'Zrušená' },
  { value: 'returned', label: 'Vrátená' }
]

export function StatusBadge({ status, type }: { status: string; type: 'order' | 'payment' }): ReactElement {
  const colors = type === 'order' ? ORDER_STATUS_COLORS : PAYMENT_STATUS_COLORS
  const colorClass = colors[status] || 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  return (
    <span data-testid={`${type}-status-badge`} className={cn('px-2 py-0.5 rounded-full text-xs font-medium', colorClass)}>
      {status}
    </span>
  )
}

export default function EshopOrderList(): ReactElement {
  const { addToast } = useToastStore()
  const {
    orderStatusFilter,
    setOrderStatusFilter,
    orderSearch,
    setOrderSearch,
    ordersPage,
    setOrdersPage,
    openOrderDetail
  } = useEshopStore()

  const [orders, setOrders] = useState<EshopOrder[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Debounce search
  const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [debouncedSearch, setDebouncedSearch] = useState(orderSearch)

  useEffect(() => {
    if (searchTimer.current) clearTimeout(searchTimer.current)
    searchTimer.current = setTimeout(() => {
      setDebouncedSearch(orderSearch)
    }, 300)
    return () => {
      if (searchTimer.current) clearTimeout(searchTimer.current)
    }
  }, [orderSearch])

  const fetchOrders = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res: EshopOrderListResponse = await api.getEshopOrders({
        page: ordersPage,
        page_size: 20,
        status: orderStatusFilter || undefined
      })
      // Client-side search filter
      let filtered = res.orders
      if (debouncedSearch) {
        const q = debouncedSearch.toLowerCase()
        filtered = filtered.filter(
          (o) =>
            o.order_number.toLowerCase().includes(q) ||
            o.customer_name.toLowerCase().includes(q)
        )
      }
      setOrders(filtered)
      setTotal(res.total)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať objednávky'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [debouncedSearch, orderStatusFilter, ordersPage, addToast])

  useEffect(() => {
    void fetchOrders()
  }, [fetchOrders])

  const handleRowDoubleClick = useCallback(
    (order: EshopOrder & { id: number }): void => {
      openOrderDetail(order.order_id)
    },
    [openOrderDetail]
  )

  const gridData = orders.map((o) => ({ ...o, id: o.order_id }))

  const pageCount = Math.max(1, Math.ceil(total / 20))

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <ShoppingCart className="h-6 w-6" />
          Objednávky
        </h1>
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              data-testid="order-search"
              value={orderSearch}
              onChange={(e) => setOrderSearch(e.target.value)}
              placeholder="Hľadať objednávku..."
              className={cn(
                'pl-9 pr-3 py-2 rounded-lg border text-sm w-64 outline-none transition-colors',
                'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
              )}
            />
          </div>

          {/* Status filter */}
          <select
            data-testid="order-status-filter"
            value={orderStatusFilter || ''}
            onChange={(e) => setOrderStatusFilter(e.target.value || null)}
            className={cn(
              'px-3 py-2 rounded-lg border text-sm outline-none transition-colors',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600 focus:border-blue-500'
            )}
          >
            {ORDER_STATUS_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Total count */}
      {!loading && !error && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0">
          Celkom: {total} objednávok
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void fetchOrders()}
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
      ) : !error ? (
        <>
          <div data-testid="order-grid">
            <BaseGrid
              data={gridData}
              config={eshopOrderGridConfig}
              onRowDoubleClick={handleRowDoubleClick}
              className="flex-1 min-h-0"
            />
          </div>

          {/* Pagination */}
          {pageCount > 1 && (
            <div className="flex items-center justify-center gap-2 py-2 shrink-0">
              <button
                disabled={ordersPage <= 1}
                onClick={() => setOrdersPage(ordersPage - 1)}
                className="px-3 py-1.5 rounded text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Predošlá
              </button>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Strana {ordersPage} z {pageCount}
              </span>
              <button
                disabled={ordersPage >= pageCount}
                onClick={() => setOrdersPage(ordersPage + 1)}
                className="px-3 py-1.5 rounded text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Ďalšia
              </button>
            </div>
          )}
        </>
      ) : null}
    </div>
  )
}
