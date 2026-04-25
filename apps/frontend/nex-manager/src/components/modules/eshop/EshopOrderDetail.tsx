import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { ArrowLeft, Loader2, AlertCircle, ExternalLink, Clock } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import { useEshopStore } from '@renderer/stores/eshopStore'
import { useAuthStore } from '@renderer/stores/authStore'
import type { EshopOrderDetail as EshopOrderDetailType } from '@renderer/types/eshop'
import { StatusBadge } from './EshopOrderList'

const ORDER_STATUSES = ['new', 'paid', 'processing', 'shipped', 'delivered', 'cancelled', 'returned']

export default function EshopOrderDetail(): ReactElement {
  const { addToast } = useToastStore()
  const { selectedOrderId, closeOrderDetail } = useEshopStore()
  const { checkPermission } = useAuthStore()
  const canEdit = checkPermission('ESHOP', 'edit')

  const [order, setOrder] = useState<EshopOrderDetailType | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Status change
  const [newStatus, setNewStatus] = useState('')
  const [statusNote, setStatusNote] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [updating, setUpdating] = useState(false)

  const fetchOrder = useCallback(async (): Promise<void> => {
    if (selectedOrderId === null) return
    setLoading(true)
    setError(null)
    try {
      const o = await api.getEshopOrderDetail(selectedOrderId)
      setOrder(o)
      setNewStatus(o.status)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať objednávku'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [selectedOrderId, addToast])

  useEffect(() => {
    void fetchOrder()
  }, [fetchOrder])

  const handleStatusChange = useCallback(async (): Promise<void> => {
    if (!order || !newStatus || newStatus === order.status) return
    setUpdating(true)
    try {
      await api.updateEshopOrder(order.order_id, {
        status: newStatus,
        note: statusNote || undefined
      })
      addToast('Stav objednávky bol zmenený', 'success')
      setConfirmOpen(false)
      setStatusNote('')
      void fetchOrder()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Chyba pri zmene stavu', 'error')
    } finally {
      setUpdating(false)
    }
  }, [order, newStatus, statusNote, addToast, fetchOrder])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-3 text-gray-500 dark:text-gray-400">Načítavam...</span>
      </div>
    )
  }

  if (error || !order) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-4">
        <AlertCircle className="h-8 w-8 text-red-500" />
        <p className="text-sm text-red-700 dark:text-red-400">{error || 'Objednávka nenájdená'}</p>
        <button
          onClick={closeOrderDetail}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          Späť na zoznam
        </button>
      </div>
    )
  }

  const subtotal = order.items.reduce((sum, item) => sum + item.unit_price_vat * item.quantity, 0)

  return (
    <div data-testid="order-detail" className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center gap-3 shrink-0">
        <button
          data-testid="back-button"
          onClick={closeOrderDetail}
          className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          title="Späť na zoznam"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div className="flex-1">
          <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-3">
            Objednávka: {order.order_number}
            <StatusBadge status={order.status} type="order" />
            <StatusBadge status={order.payment_status} type="payment" />
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            ID: {order.order_id} | Vytvorená: {new Date(order.created_at).toLocaleString('sk-SK')}
          </p>
        </div>
      </div>

      {/* Customer info */}
      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
        <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Zákazník</h2>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500 dark:text-gray-400">Meno: </span>
            <span data-testid="customer-name" className="text-gray-900 dark:text-white">{order.customer_name}</span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Email: </span>
            <span data-testid="customer-email" className="text-gray-900 dark:text-white">{order.customer_email}</span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Telefón: </span>
            <span className="text-gray-900 dark:text-white">{order.customer_phone || '—'}</span>
          </div>
        </div>
      </div>

      {/* Addresses */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Fakturačná adresa</h2>
          <div data-testid="billing-address" className="text-sm text-gray-900 dark:text-white space-y-0.5">
            <div>{order.billing_name}{order.billing_name2 ? ` ${order.billing_name2}` : ''}</div>
            <div>{order.billing_street}</div>
            <div>{order.billing_zip} {order.billing_city}</div>
            <div>{order.billing_country}</div>
            {order.ico && <div>IČO: {order.ico}</div>}
            {order.dic && <div>DIČ: {order.dic}</div>}
          </div>
        </div>
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Dodacia adresa</h2>
          <div data-testid="shipping-address" className="text-sm text-gray-900 dark:text-white space-y-0.5">
            {order.shipping_name ? (
              <>
                <div>{order.shipping_name}{order.shipping_name2 ? ` ${order.shipping_name2}` : ''}</div>
                <div>{order.shipping_street}</div>
                <div>{order.shipping_zip} {order.shipping_city}</div>
                <div>{order.shipping_country}</div>
              </>
            ) : (
              <div className="text-gray-400 dark:text-gray-500">Rovnaká ako fakturačná</div>
            )}
          </div>
        </div>
      </div>

      {/* Order items table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 p-4 pb-2">Položky</h2>
        <table data-testid="order-items-table" className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700 text-left">
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium">SKU</th>
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium">Názov</th>
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium text-right">Množstvo</th>
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium text-right">Cena s DPH</th>
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium text-right">DPH %</th>
              <th className="px-4 py-2 text-gray-500 dark:text-gray-400 font-medium text-right">Spolu</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item, idx) => (
              <tr key={idx} className="border-b border-gray-100 dark:border-gray-700/50">
                <td className="px-4 py-2 text-gray-900 dark:text-white font-mono text-xs">{item.sku}</td>
                <td className="px-4 py-2 text-gray-900 dark:text-white">{item.name}</td>
                <td className="px-4 py-2 text-gray-900 dark:text-white text-right">{item.quantity}</td>
                <td className="px-4 py-2 text-gray-900 dark:text-white text-right">{item.unit_price_vat.toFixed(2)}</td>
                <td className="px-4 py-2 text-gray-900 dark:text-white text-right">{item.vat_rate}%</td>
                <td className="px-4 py-2 text-gray-900 dark:text-white text-right font-medium">
                  {(item.unit_price_vat * item.quantity).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t-2 border-gray-300 dark:border-gray-600">
              <td colSpan={5} className="px-4 py-2 text-right font-semibold text-gray-700 dark:text-gray-300">
                Medzisúčet:
              </td>
              <td className="px-4 py-2 text-right font-semibold text-gray-900 dark:text-white">
                {subtotal.toFixed(2)}
              </td>
            </tr>
            <tr>
              <td colSpan={5} className="px-4 py-2 text-right font-bold text-gray-900 dark:text-white">
                Celkom s DPH:
              </td>
              <td data-testid="order-total" className="px-4 py-2 text-right font-bold text-gray-900 dark:text-white">
                {order.total_amount_vat.toFixed(2)} {order.currency}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Tracking info */}
      {(order.tracking_number || order.tracking_link) && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Sledovanie zásielky</h2>
          <div className="text-sm space-y-1">
            {order.tracking_number && (
              <div>
                <span className="text-gray-500 dark:text-gray-400">Číslo zásielky: </span>
                <span className="text-gray-900 dark:text-white font-mono">{order.tracking_number}</span>
              </div>
            )}
            {order.tracking_link && (
              <div>
                <span className="text-gray-500 dark:text-gray-400">Odkaz: </span>
                <a
                  href={order.tracking_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 dark:text-blue-400 hover:underline inline-flex items-center gap-1"
                >
                  Sledovať zásielku <ExternalLink className="h-3 w-3" />
                </a>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Note */}
      {order.note && (
        <div className="bg-yellow-50 dark:bg-yellow-900/10 rounded-lg p-4 border border-yellow-200 dark:border-yellow-800">
          <h2 className="text-sm font-semibold text-yellow-700 dark:text-yellow-400 mb-1">Poznámka</h2>
          <p className="text-sm text-yellow-800 dark:text-yellow-300">{order.note}</p>
        </div>
      )}

      {/* Status change */}
      {canEdit && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Zmena stavu</h2>
          <div className="flex items-end gap-3">
            <div className="flex-1">
              <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Nový stav</label>
              <select
                data-testid="status-select"
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className={cn(
                  'w-full px-3 py-2 rounded-lg border text-sm outline-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'border-gray-300 dark:border-gray-600 focus:border-blue-500'
                )}
              >
                {ORDER_STATUSES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Poznámka (voliteľná)</label>
              <input
                type="text"
                value={statusNote}
                onChange={(e) => setStatusNote(e.target.value)}
                placeholder="Poznámka k zmene..."
                className={cn(
                  'w-full px-3 py-2 rounded-lg border text-sm outline-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  'border-gray-300 dark:border-gray-600 focus:border-blue-500'
                )}
              />
            </div>
            <button
              data-testid="change-status-button"
              disabled={!newStatus || newStatus === order.status || updating}
              onClick={() => setConfirmOpen(true)}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed'
              )}
            >
              Zmeniť stav
            </button>
          </div>
        </div>
      )}

      {/* Confirmation dialog */}
      {confirmOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 w-96 shadow-xl">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Potvrdiť zmenu stavu
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Zmeniť stav z <strong>{order.status}</strong> na <strong>{newStatus}</strong>?
            </p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setConfirmOpen(false)}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                Zrušiť
              </button>
              <button
                data-testid="confirm-status-change"
                onClick={() => void handleStatusChange()}
                disabled={updating}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {updating ? 'Mením...' : 'Potvrdiť'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Status history timeline */}
      {order.status_history.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
            <Clock className="h-4 w-4" />
            História stavov
          </h2>
          <div data-testid="status-history" className="space-y-3">
            {order.status_history.map((entry, idx) => (
              <div key={idx} className="flex items-start gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 shrink-0" />
                <div className="flex-1">
                  <div className="text-gray-900 dark:text-white">
                    {entry.old_status ? `${entry.old_status} → ${entry.new_status}` : entry.new_status}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {new Date(entry.created_at).toLocaleString('sk-SK')}
                    {entry.changed_by && ` • ${entry.changed_by}`}
                    {entry.note && ` • ${entry.note}`}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
