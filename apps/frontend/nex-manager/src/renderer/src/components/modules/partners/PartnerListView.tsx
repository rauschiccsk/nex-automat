import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Building2, Loader2, AlertCircle, RotateCcw } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { BaseGrid } from '@renderer/components/grids'
import { partnersGridConfig } from './partnersGridConfig'
import type { Partner } from '@renderer/types/partner'
import PartnerFormDialog from './PartnerFormDialog'

export default function PartnerListView(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()

  const canCreate = checkPermission('PAB', 'create')
  const canEdit = checkPermission('PAB', 'edit')

  // ── Data state ──
  const [partners, setPartners] = useState<Partner[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // ── Dialog state ──
  const [formDialogOpen, setFormDialogOpen] = useState(false)
  const [editingPartner, setEditingPartner] = useState<Partner | null>(null)

  // ── Fetch all partners (client-side) ──
  const fetchPartners = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.getPartners({ page: 1, page_size: 10000 })
      setPartners(res.items)
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

  // ── Dialog handlers ──
  const handleCreate = useCallback((): void => {
    setEditingPartner(null)
    setFormDialogOpen(true)
  }, [])

  const handleRowDoubleClick = useCallback(
    (partner: Partner): void => {
      if (!canEdit) return
      setEditingPartner(partner)
      setFormDialogOpen(true)
    },
    [canEdit]
  )

  const handleFormClose = useCallback((): void => {
    setFormDialogOpen(false)
    setEditingPartner(null)
  }, [])

  const handleFormSaved = useCallback((): void => {
    setFormDialogOpen(false)
    setEditingPartner(null)
    void fetchPartners()
  }, [fetchPartners])

  return (
    <div className="flex flex-col h-full gap-3">
      {/* ── Toolbar ── */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Building2 className="h-6 w-6" />
          Katalóg partnerov
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

      {/* ── Error state ── */}
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

      {/* ── Loading state ── */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : (
        /* ── BaseGrid ── */
        <BaseGrid
          data={partners}
          config={partnersGridConfig}
          onRowDoubleClick={handleRowDoubleClick}
          className="flex-1 min-h-0"
        />
      )}

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
