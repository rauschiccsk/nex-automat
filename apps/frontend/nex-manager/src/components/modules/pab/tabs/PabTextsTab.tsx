import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Loader2, Save } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerText, TextType } from '@renderer/types/pab'

const TEXT_TYPE_LABELS: Record<string, string> = {
  owner_name: 'Meno vlastníka',
  description: 'Popis',
  notice: 'Poznámka'
}

const ALL_TEXT_TYPES: TextType[] = ['owner_name', 'description', 'notice']

interface PabTextsTabProps {
  partnerId: number
}

export default function PabTextsTab({ partnerId }: PabTextsTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')

  const [texts, setTexts] = useState<PartnerText[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState<string | null>(null)

  // Form state per text type
  const [formValues, setFormValues] = useState<Record<string, string>>({
    owner_name: '',
    description: '',
    notice: ''
  })

  const loadTexts = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabTexts(partnerId)
      setTexts(data)
      const newValues: Record<string, string> = { owner_name: '', description: '', notice: '' }
      for (const t of data) {
        if (t.text_type in newValues) {
          newValues[t.text_type] = t.text_content ?? ''
        }
      }
      setFormValues(newValues)
    } catch {
      // Texts may not exist yet
      setTexts([])
    } finally {
      setLoading(false)
    }
  }, [partnerId])

  useEffect(() => { void loadTexts() }, [loadTexts])

  const handleSave = useCallback(async (textType: TextType): Promise<void> => {
    setSaving(textType)
    try {
      await api.upsertPabTexts(partnerId, {
        text_type: textType,
        line_number: 1,
        language: 'sk',
        text_content: formValues[textType]?.trim() || null
      })
      addToast(`${TEXT_TYPE_LABELS[textType]} bol uložený`, 'success')
      void loadTexts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Uloženie zlyhalo', 'error')
    } finally {
      setSaving(null)
    }
  }, [partnerId, formValues, addToast, loadTexts])

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50 resize-y min-h-[60px]'
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  // Check if value changed from stored
  const existingTextsMap = new Map(texts.map((t) => [t.text_type, t.text_content ?? '']))

  return (
    <div className="space-y-6 max-w-3xl">
      {ALL_TEXT_TYPES.map((textType) => {
        const storedValue = existingTextsMap.get(textType) ?? ''
        const currentValue = formValues[textType] ?? ''
        const isDirty = currentValue !== storedValue
        const isSaving = saving === textType

        return (
          <div key={textType} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <div className="flex items-center justify-between mb-2">
              <label className={labelCls}>{TEXT_TYPE_LABELS[textType]}</label>
              {canEdit && isDirty && (
                <button
                  type="button"
                  onClick={() => void handleSave(textType)}
                  disabled={isSaving}
                  className={cn('flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50')}
                >
                  {isSaving ? <Loader2 className="h-3 w-3 animate-spin" /> : <Save className="h-3 w-3" />}
                  Uložiť
                </button>
              )}
            </div>
            <textarea
              value={currentValue}
              onChange={(e) => setFormValues((prev) => ({ ...prev, [textType]: e.target.value }))}
              disabled={!canEdit || isSaving}
              className={inputCls}
              rows={3}
              placeholder={`Zadajte ${TEXT_TYPE_LABELS[textType].toLowerCase()}...`}
            />
          </div>
        )
      })}
    </div>
  )
}
