import { useMemo, type ReactElement } from 'react'
import { X, Info } from 'lucide-react'
import { useUiStore } from '@renderer/stores/uiStore'
import { useTabStore } from '@renderer/stores/tabStore'
import { useModuleStore, type NexModule } from '@renderer/stores/moduleStore'
import { cn } from '@renderer/lib/utils'

interface DetailRow {
  label: string
  value: string
}

function getModuleCategory(mod: NexModule): string {
  const dotIdx = mod.id.indexOf('.')
  if (dotIdx > 0) return mod.id.substring(0, dotIdx)
  return 'base'
}

function formatDate(): string {
  return new Date().toLocaleDateString('sk-SK', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

export default function InfoPanel(): ReactElement {
  const { infoPanelOpen, setInfoPanelOpen } = useUiStore()
  const { tabs, activeTabId } = useTabStore()
  const { modules } = useModuleStore()

  const activeTab = useMemo(() => {
    if (!activeTabId) return null
    return tabs.find((t) => t.id === activeTabId) ?? null
  }, [tabs, activeTabId])

  const activeModule = useMemo((): NexModule | null => {
    if (!activeTab) return null
    return modules.find((m) => m.id === activeTab.id) ?? null
  }, [activeTab, modules])

  const details = useMemo((): DetailRow[] => {
    if (!activeModule) return []
    return [
      { label: 'ID', value: activeModule.id },
      { label: 'Názov', value: activeModule.name },
      { label: 'Kategória', value: getModuleCategory(activeModule) },
      { label: 'Stav', value: activeModule.enabled ? 'Aktívny' : 'Neaktívny' },
      { label: 'Verzia', value: '1.0.0' },
      { label: 'Posledná zmena', value: formatDate() }
    ]
  }, [activeModule])

  const handleClose = (): void => {
    setInfoPanelOpen(false)
  }

  return (
    <>
      {/* Overlay / backdrop */}
      <div
        onClick={handleClose}
        className={cn(
          'fixed inset-0 z-40 bg-black/30 transition-opacity duration-300',
          infoPanelOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        )}
      />

      {/* Panel */}
      <div
        className={cn(
          'fixed top-0 right-0 h-full w-[350px] z-50 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 shadow-xl transition-transform duration-300 ease-in-out flex flex-col',
          infoPanelOpen ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <Info className="h-5 w-5 text-blue-500" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Detail</h2>
          </div>
          <button
            onClick={handleClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Zavrieť panel"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeModule ? (
            <div className="space-y-4">
              {/* Module header */}
              <div className="flex items-center gap-3 pb-4 border-b border-gray-200 dark:border-gray-700">
                <div className="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center text-2xl">
                  {activeModule.icon ?? '📦'}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {activeModule.name}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{activeModule.id}</p>
                </div>
              </div>

              {/* Detail rows */}
              <div className="space-y-3">
                {details.map((row) => (
                  <div key={row.label} className="flex justify-between items-center">
                    <span className="text-sm text-gray-500 dark:text-gray-400">{row.label}</span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {row.value}
                    </span>
                  </div>
                ))}
              </div>

              {/* Status badge */}
              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2">
                  <div
                    className={cn(
                      'w-2 h-2 rounded-full',
                      activeModule.enabled ? 'bg-green-500' : 'bg-gray-400'
                    )}
                  />
                  <span className="text-sm text-gray-600 dark:text-gray-300">
                    {activeModule.enabled ? 'Modul je aktívny' : 'Modul je neaktívny'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <Info className="h-12 w-12 text-gray-300 dark:text-gray-600 mb-3" />
              <p className="text-gray-500 dark:text-gray-400 text-sm">Žiadny aktívny modul</p>
              <p className="text-gray-400 dark:text-gray-500 text-xs mt-1">
                Otvorte modul pre zobrazenie detailov
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
