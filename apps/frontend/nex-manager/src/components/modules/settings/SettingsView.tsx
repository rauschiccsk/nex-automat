import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Settings as SettingsIcon, Loader2, Save, RefreshCw } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError, type Setting } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'

const CATEGORY_LABELS: Record<string, string> = {
  auth: 'Autentifikácia',
  business: 'Biznis pravidlá',
  ui: 'UI / UX',
  integration: 'Integrácie',
  payment: 'Platby',
  general: 'Všeobecné'
}

function valueToInputString(v: unknown): string {
  if (v === null || v === undefined) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'number' || typeof v === 'boolean') return String(v)
  return JSON.stringify(v)
}

function parseInputString(s: string, original: unknown): unknown {
  // Preserve type from original value: string stays string, number/bool/array re-parse from JSON.
  if (typeof original === 'string') return s
  if (typeof original === 'number') {
    const n = Number(s)
    return Number.isNaN(n) ? original : n
  }
  if (typeof original === 'boolean') return s === 'true' || s === '1'
  // Object / array — try JSON parse, fallback to original on error.
  try {
    return JSON.parse(s)
  } catch {
    return original
  }
}

export default function SettingsView(): ReactElement {
  const { addToast } = useToastStore()

  const [settings, setSettings] = useState<Setting[]>([])
  const [loading, setLoading] = useState(true)
  const [drafts, setDrafts] = useState<Record<string, string>>({})
  const [saving, setSaving] = useState<string | null>(null)

  const fetchSettings = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const res = await api.listSettings()
      setSettings(res.settings)
      // Initialize drafts from current values
      const d: Record<string, string> = {}
      for (const s of res.settings) {
        d[s.setting_key] = valueToInputString(s.value)
      }
      setDrafts(d)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Načítanie nastavení zlyhalo', 'error')
    } finally {
      setLoading(false)
    }
  }, [addToast])

  useEffect(() => {
    void fetchSettings()
  }, [fetchSettings])

  const handleSave = useCallback(
    async (s: Setting): Promise<void> => {
      const draftStr = drafts[s.setting_key] ?? ''
      const newValue = parseInputString(draftStr, s.value)
      setSaving(s.setting_key)
      try {
        const updated = await api.updateSetting(s.setting_key, newValue)
        addToast(`${s.setting_key}: uložené`, 'success')
        // Update local state
        setSettings((prev) => prev.map((x) => (x.setting_key === s.setting_key ? updated : x)))
        setDrafts((prev) => ({ ...prev, [s.setting_key]: valueToInputString(updated.value) }))
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || `Uloženie ${s.setting_key} zlyhalo`, 'error')
      } finally {
        setSaving(null)
      }
    },
    [drafts, addToast]
  )

  // Group by category
  const grouped = settings.reduce<Record<string, Setting[]>>((acc, s) => {
    if (!acc[s.category]) acc[s.category] = []
    acc[s.category].push(s)
    return acc
  }, {})

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <SettingsIcon className="h-6 w-6" />
          Nastavenia
        </h1>
        <button
          onClick={() => void fetchSettings()}
          disabled={loading}
          className={cn(
            'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
            'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600',
            'disabled:opacity-50'
          )}
        >
          <RefreshCw className={cn('h-4 w-4', loading && 'animate-spin')} />
          Obnoviť
        </button>
      </div>

      {loading ? (
        <div className="p-8 flex items-center justify-center text-gray-500">
          <Loader2 className="h-6 w-6 animate-spin" />
        </div>
      ) : settings.length === 0 ? (
        <div className="p-8 text-center text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          Žiadne nastavenia
        </div>
      ) : (
        Object.entries(grouped).map(([category, items]) => (
          <div
            key={category}
            className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden"
          >
            <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
              <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wide">
                {CATEGORY_LABELS[category] || category}
              </h2>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {items.map((s) => {
                const draft = drafts[s.setting_key] ?? ''
                const original = valueToInputString(s.value)
                const dirty = draft !== original
                return (
                  <div
                    key={s.setting_key}
                    className="p-4 flex flex-col gap-2 md:flex-row md:items-start md:gap-4"
                  >
                    <div className="md:w-1/3">
                      <div className="font-mono text-sm text-gray-900 dark:text-white">
                        {s.setting_key}
                      </div>
                      {s.description && (
                        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {s.description}
                        </div>
                      )}
                      {s.updated_by && (
                        <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                          Naposledy: {s.updated_by}
                        </div>
                      )}
                    </div>
                    <div className="flex-1 flex items-center gap-2">
                      <input
                        type="text"
                        value={draft}
                        onChange={(e) =>
                          setDrafts((prev) => ({ ...prev, [s.setting_key]: e.target.value }))
                        }
                        className={cn(
                          'flex-1 px-3 py-2 rounded-lg border text-sm font-mono outline-none transition-colors',
                          'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                          dirty
                            ? 'border-amber-400 focus:ring-2 focus:ring-amber-500/20'
                            : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
                        )}
                        disabled={saving === s.setting_key}
                      />
                      <button
                        onClick={() => void handleSave(s)}
                        disabled={!dirty || saving === s.setting_key}
                        className={cn(
                          'flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                          dirty
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed',
                          'disabled:opacity-50 disabled:cursor-not-allowed'
                        )}
                      >
                        {saving === s.setting_key ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Save className="h-4 w-4" />
                        )}
                        Uložiť
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        ))
      )}

      <div className="text-xs text-gray-500 dark:text-gray-400 mt-2 px-1">
        Citlivé secrets (JWT_SECRET_KEY, POSTGRES_PASSWORD, SMTP_PASSWORD) a kritické parametre
        (bcrypt rounds, JWT algoritmus) sú spravované v{' '}
        <code className="font-mono bg-gray-100 dark:bg-gray-700 px-1 rounded">.env</code> súbore a
        nie sú dostupné v UI.
      </div>
    </div>
  )
}
