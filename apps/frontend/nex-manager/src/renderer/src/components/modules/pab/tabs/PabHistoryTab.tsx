import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Loader2, Clock, Eye, X } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerHistory } from '@renderer/types/pab'

interface PabHistoryTabProps {
  partnerId: number
}

function formatDateTime(iso: string | null): string {
  if (!iso) return '—'
  try {
    return new Date(iso).toLocaleString('sk-SK', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    })
  } catch {
    return iso
  }
}

export default function PabHistoryTab({ partnerId }: PabHistoryTabProps): ReactElement {
  const { addToast } = useToastStore()

  const [history, setHistory] = useState<PartnerHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedVersion, setSelectedVersion] = useState<PartnerHistory | null>(null)
  const [loadingVersion, setLoadingVersion] = useState(false)

  const loadHistory = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabHistory(partnerId)
      setHistory(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať históriu', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => { void loadHistory() }, [loadHistory])

  const handleViewVersion = useCallback(async (modifyId: number): Promise<void> => {
    setLoadingVersion(true)
    try {
      const version = await api.getPabHistoryVersion(partnerId, modifyId)
      setSelectedVersion(version)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať verziu', 'error')
    } finally {
      setLoadingVersion(false)
    }
  }, [partnerId, addToast])

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  if (history.length === 0) {
    return <p className="text-sm text-gray-500 dark:text-gray-400 py-4">Žiadna história zmien</p>
  }

  const labelCls = 'text-xs font-medium text-gray-500 dark:text-gray-400'
  const valueCls = 'text-sm text-gray-900 dark:text-white'

  return (
    <div className="space-y-4 max-w-5xl">
      {/* Version detail overlay */}
      {selectedVersion && (
        <div className="p-4 rounded-lg border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
              Detail verzie #{selectedVersion.modify_id}
              {selectedVersion.valid_to === null && (
                <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                  Aktuálna
                </span>
              )}
            </h4>
            <button onClick={() => setSelectedVersion(null)} className="p-1 rounded text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700">
              <X className="h-4 w-4" />
            </button>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div><span className={labelCls}>Kód</span><p className={valueCls}>{selectedVersion.partner_code}</p></div>
            <div><span className={labelCls}>Názov</span><p className={valueCls}>{selectedVersion.partner_name}</p></div>
            <div><span className={labelCls}>Reg. názov</span><p className={valueCls}>{selectedVersion.reg_name ?? '—'}</p></div>
            <div><span className={labelCls}>Trieda</span><p className={valueCls}>{selectedVersion.partner_class}</p></div>
            <div><span className={labelCls}>IČO</span><p className={valueCls}>{selectedVersion.company_id ?? '—'}</p></div>
            <div><span className={labelCls}>DIČ</span><p className={valueCls}>{selectedVersion.tax_id ?? '—'}</p></div>
            <div><span className={labelCls}>IČ DPH</span><p className={valueCls}>{selectedVersion.vat_id ?? '—'}</p></div>
            <div><span className={labelCls}>Platca DPH</span><p className={valueCls}>{selectedVersion.is_vat_payer ? 'Áno' : 'Nie'}</p></div>
            <div><span className={labelCls}>Dodávateľ</span><p className={valueCls}>{selectedVersion.is_supplier ? 'Áno' : 'Nie'}</p></div>
            <div><span className={labelCls}>Odberateľ</span><p className={valueCls}>{selectedVersion.is_customer ? 'Áno' : 'Nie'}</p></div>
            <div><span className={labelCls}>Ulica</span><p className={valueCls}>{selectedVersion.street ?? '—'}</p></div>
            <div><span className={labelCls}>Mesto</span><p className={valueCls}>{selectedVersion.city ?? '—'}</p></div>
            <div><span className={labelCls}>PSČ</span><p className={valueCls}>{selectedVersion.zip_code ?? '—'}</p></div>
            <div><span className={labelCls}>Krajina</span><p className={valueCls}>{selectedVersion.country_code ?? '—'}</p></div>
            <div><span className={labelCls}>Platná od</span><p className={valueCls}>{formatDateTime(selectedVersion.valid_from)}</p></div>
            <div><span className={labelCls}>Platná do</span><p className={valueCls}>{selectedVersion.valid_to ? formatDateTime(selectedVersion.valid_to) : '—'}</p></div>
            <div><span className={labelCls}>Zmenil</span><p className={valueCls}>{selectedVersion.changed_by ?? '—'}</p></div>
          </div>
        </div>
      )}

      {/* Timeline */}
      <div className="relative">
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />

        {[...history].reverse().map((h) => {
          const isCurrent = h.valid_to === null
          return (
            <div key={h.history_id} className="relative pl-10 pb-4">
              {/* Timeline dot */}
              <div className={cn(
                'absolute left-2.5 w-3 h-3 rounded-full border-2',
                isCurrent
                  ? 'bg-green-500 border-green-500'
                  : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600'
              )} style={{ top: '6px' }} />

              <div className={cn(
                'p-3 rounded-lg border transition-colors',
                isCurrent
                  ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10'
                  : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50',
                selectedVersion?.modify_id === h.modify_id && 'ring-2 ring-blue-500'
              )}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Clock className="h-3.5 w-3.5 text-gray-400" />
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      Verzia {h.modify_id}
                    </span>
                    {isCurrent && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                        Aktuálna
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => void handleViewVersion(h.modify_id)}
                    disabled={loadingVersion}
                    className="flex items-center gap-1 px-2 py-1 rounded text-xs text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                    title="Zobraziť detail"
                  >
                    {loadingVersion && selectedVersion?.modify_id === h.modify_id
                      ? <Loader2 className="h-3 w-3 animate-spin" />
                      : <Eye className="h-3 w-3" />
                    }
                    Detail
                  </button>
                </div>
                <div className="mt-1 text-xs text-gray-500 dark:text-gray-400 flex gap-4">
                  <span>Od: {formatDateTime(h.valid_from)}</span>
                  <span>Do: {h.valid_to ? formatDateTime(h.valid_to) : '—'}</span>
                  {h.changed_by && <span>Zmenil: {h.changed_by}</span>}
                </div>
                <div className="mt-1 text-xs text-gray-600 dark:text-gray-400">
                  {h.partner_name}
                  {h.company_id && ` | IČO: ${h.company_id}`}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
