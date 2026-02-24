import { type ReactElement, useMemo } from 'react'
import { X } from 'lucide-react'
import { useTabStore } from '@renderer/stores/tabStore'
import { cn } from '@renderer/lib/utils'

export default function TabBar(): ReactElement {
  const { tabs, activeTabId, setActiveTab, removeTab } = useTabStore()

  // Build display labels with multi-instance suffix
  const tabLabels = useMemo(() => {
    // Count occurrences of each label
    const labelCounts = new Map<string, number>()
    for (const tab of tabs) {
      labelCounts.set(tab.label, (labelCounts.get(tab.label) ?? 0) + 1)
    }

    // Assign suffix indices for duplicated labels
    const labelIndices = new Map<string, number>()
    return tabs.map((tab) => {
      const count = labelCounts.get(tab.label) ?? 1
      if (count > 1) {
        const idx = (labelIndices.get(tab.label) ?? 0) + 1
        labelIndices.set(tab.label, idx)
        return { ...tab, displayLabel: `${tab.label}-${idx}` }
      }
      return { ...tab, displayLabel: tab.label }
    })
  }, [tabs])

  return (
    <div className="h-10 bg-gray-100 dark:bg-gray-800 flex items-center overflow-x-auto border-b border-gray-200 dark:border-gray-700 shrink-0">
      {tabLabels.map((tab) => {
        const isActive = tab.id === activeTabId
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={cn(
              'flex items-center gap-1.5 px-3 h-full cursor-pointer border-r border-gray-200 dark:border-gray-700 text-sm whitespace-nowrap transition-colors',
              isActive
                ? 'bg-white dark:bg-gray-700 font-medium text-gray-900 dark:text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
            )}
          >
            <span>{tab.displayLabel}</span>
            {tab.closable !== false && (
              <span
                role="button"
                tabIndex={0}
                onClick={(e) => {
                  e.stopPropagation()
                  removeTab(tab.id)
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.stopPropagation()
                    removeTab(tab.id)
                  }
                }}
                className="rounded p-0.5 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                <X className="h-3.5 w-3.5" />
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
