import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Loader2, Trash2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerCategoryMapping, CategoryType } from '@renderer/types/pab'

const CATEGORY_TYPE_LABELS: Record<string, string> = {
  supplier: 'Dodávateľ',
  customer: 'Odberateľ'
}

interface PabCategoriesTabProps {
  partnerId: number
}

export default function PabCategoriesTab({ partnerId }: PabCategoriesTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [categories, setCategories] = useState<PartnerCategoryMapping[]>([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [saving, setSaving] = useState(false)
  const [newCategoryId, setNewCategoryId] = useState('')
  const [newCategoryType, setNewCategoryType] = useState<CategoryType>('customer')

  const loadCategories = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabCategories(partnerId)
      setCategories(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať skupiny', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => { void loadCategories() }, [loadCategories])

  const handleAssign = useCallback(async (): Promise<void> => {
    const catId = parseInt(newCategoryId, 10)
    if (isNaN(catId) || catId <= 0) {
      addToast('Zadajte platné ID kategórie', 'error')
      return
    }
    setSaving(true)
    try {
      await api.assignPabCategory(partnerId, {
        category_id: catId,
        category_type: newCategoryType
      })
      addToast('Skupina bola priradená', 'success')
      setAdding(false)
      setNewCategoryId('')
      void loadCategories()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Priradenie zlyhalo', 'error')
    } finally {
      setSaving(false)
    }
  }, [partnerId, newCategoryId, newCategoryType, addToast, loadCategories])

  const handleUnassign = useCallback(async (categoryId: number): Promise<void> => {
    if (!confirm('Naozaj chcete odstrániť túto skupinu?')) return
    try {
      await api.unassignPabCategory(partnerId, categoryId)
      addToast('Skupina bola odstránená', 'success')
      void loadCategories()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Odstránenie zlyhalo', 'error')
    }
  }, [partnerId, addToast, loadCategories])

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50'

  return (
    <div className="space-y-4 max-w-3xl">
      {categories.length === 0 && !adding && (
        <p className="text-sm text-gray-500 dark:text-gray-400">Žiadne priradené skupiny</p>
      )}

      {/* Category list */}
      <div className="space-y-2">
        {categories.map((cat) => (
          <div key={cat.id} className="flex items-center justify-between p-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                Kategória #{cat.category_id}
              </span>
              <span className={cn(
                'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                cat.category_type === 'supplier'
                  ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                  : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
              )}>
                {CATEGORY_TYPE_LABELS[cat.category_type] ?? cat.category_type}
              </span>
            </div>
            {canDelete && (
              <button onClick={() => void handleUnassign(cat.category_id)} className="p-1.5 rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" title="Odstrániť">
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Add form */}
      {adding && (
        <div className="p-4 border rounded-lg border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 space-y-3">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Pridať skupinu</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">ID kategórie</label>
              <input type="number" value={newCategoryId} onChange={(e) => setNewCategoryId(e.target.value)} disabled={saving} className={inputCls} min={1} placeholder="Zadajte ID" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Typ</label>
              <select value={newCategoryType} onChange={(e) => setNewCategoryType(e.target.value as CategoryType)} disabled={saving} className={inputCls}>
                <option value="customer">Odberateľ</option>
                <option value="supplier">Dodávateľ</option>
              </select>
            </div>
            <div className="flex items-end gap-2">
              <button type="button" onClick={() => setAdding(false)} disabled={saving} className="px-3 py-2 rounded-lg text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
                Zrušiť
              </button>
              <button type="button" onClick={() => void handleAssign()} disabled={saving} className={cn('flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50')}>
                {saving && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
                Priradiť
              </button>
            </div>
          </div>
        </div>
      )}

      {canEdit && !adding && (
        <button onClick={() => setAdding(true)} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border border-dashed border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
          <Plus className="h-3.5 w-3.5" /> Pridať skupinu
        </button>
      )}
    </div>
  )
}
