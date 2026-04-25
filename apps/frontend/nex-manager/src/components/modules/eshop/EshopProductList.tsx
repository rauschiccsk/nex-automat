import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Package, Plus, Loader2, AlertCircle, RotateCcw, Trash2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { useEshopStore } from '@renderer/stores/eshopStore'
import { BaseGrid } from '@renderer/components/grids'
import { eshopProductGridConfig } from './eshopGridConfigs'
import type { EshopProduct, EshopProductListResponse } from '@renderer/types/eshop'

export default function EshopProductList(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const {
    productActiveFilter,
    setProductActiveFilter,
    productsPage,
    setProductsPage,
    openProductEdit
  } = useEshopStore()

  const canCreate = checkPermission('ESHOP', 'create')
  const canDelete = checkPermission('ESHOP', 'delete')

  const [products, setProducts] = useState<EshopProduct[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Delete confirmation
  const [deleteTarget, setDeleteTarget] = useState<EshopProduct | null>(null)

  const fetchProducts = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res: EshopProductListResponse = await api.getEshopProducts({
        page: productsPage,
        page_size: 20,
        include_inactive: productActiveFilter === null ? true : productActiveFilter === false
      })
      let filtered = res.products
      if (productActiveFilter !== null) {
        filtered = filtered.filter((p) => p.is_active === productActiveFilter)
      }
      setProducts(filtered)
      setTotal(res.total)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať produkty'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [productActiveFilter, productsPage, addToast])

  useEffect(() => {
    void fetchProducts()
  }, [fetchProducts])

  const handleRowDoubleClick = useCallback(
    (product: EshopProduct & { id: number }): void => {
      openProductEdit(product.product_id)
    },
    [openProductEdit]
  )

  const handleDelete = useCallback(async (): Promise<void> => {
    if (!deleteTarget) return
    try {
      await api.deleteEshopProduct(deleteTarget.product_id)
      addToast(`Produkt ${deleteTarget.sku} bol deaktivovaný`, 'success')
      setDeleteTarget(null)
      void fetchProducts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Chyba pri mazaní produktu', 'error')
    }
  }, [deleteTarget, addToast, fetchProducts])

  const gridData = products.map((p) => ({ ...p, id: p.product_id }))
  const pageCount = Math.max(1, Math.ceil(total / 20))

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Package className="h-6 w-6" />
          Produkty
        </h1>
        <div className="flex items-center gap-3">
          {/* Active filter */}
          <select
            data-testid="product-active-filter"
            value={productActiveFilter === null ? '' : String(productActiveFilter)}
            onChange={(e) => {
              const v = e.target.value
              setProductActiveFilter(v === '' ? null : v === 'true')
            }}
            className={cn(
              'px-3 py-2 rounded-lg border text-sm outline-none transition-colors',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600 focus:border-blue-500'
            )}
          >
            <option value="">Všetky</option>
            <option value="true">Aktívne</option>
            <option value="false">Neaktívne</option>
          </select>

          {/* Create button */}
          {canCreate && (
            <button
              data-testid="new-product-button"
              onClick={() => openProductEdit(null)}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700'
              )}
            >
              <Plus className="h-4 w-4" />
              Nový produkt
            </button>
          )}
        </div>
      </div>

      {/* Total */}
      {!loading && !error && (
        <div className="text-xs text-gray-500 dark:text-gray-400 shrink-0">
          Celkom: {total} produktov
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void fetchProducts()}
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
          <div data-testid="product-grid">
            <BaseGrid
              data={gridData}
              config={eshopProductGridConfig}
              onRowDoubleClick={handleRowDoubleClick}
              className="flex-1 min-h-0"
            />
          </div>

          {/* Delete button row (shown when we have products and can delete) */}
          {canDelete && products.length > 0 && (
            <div className="text-xs text-gray-400 dark:text-gray-500 shrink-0">
              Dvojklik na riadok = upraviť produkt
            </div>
          )}

          {/* Pagination */}
          {pageCount > 1 && (
            <div className="flex items-center justify-center gap-2 py-2 shrink-0">
              <button
                disabled={productsPage <= 1}
                onClick={() => setProductsPage(productsPage - 1)}
                className="px-3 py-1.5 rounded text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Predošlá
              </button>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Strana {productsPage} z {pageCount}
              </span>
              <button
                disabled={productsPage >= pageCount}
                onClick={() => setProductsPage(productsPage + 1)}
                className="px-3 py-1.5 rounded text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Ďalšia
              </button>
            </div>
          )}
        </>
      ) : null}

      {/* Delete confirmation dialog */}
      {deleteTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 w-96 shadow-xl">
            <div className="flex items-center gap-3 mb-4">
              <Trash2 className="h-5 w-5 text-red-500" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Deaktivovať produkt?
              </h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Produkt <strong>{deleteTarget.name}</strong> (SKU: {deleteTarget.sku}) bude deaktivovaný.
            </p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setDeleteTarget(null)}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Zrušiť
              </button>
              <button
                data-testid="confirm-delete"
                onClick={() => void handleDelete()}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-red-600 text-white hover:bg-red-700 transition-colors"
              >
                Deaktivovať
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
