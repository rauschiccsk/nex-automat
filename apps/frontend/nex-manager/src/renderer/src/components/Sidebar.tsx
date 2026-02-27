import { useState, useCallback, useRef, useEffect, type ReactElement } from 'react'
import {
  Star,
  Clock,
  ChevronRight,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react'
import { useUiStore } from '@renderer/stores/uiStore'
import { useModuleStore, type NexModule } from '@renderer/stores/moduleStore'
import { useTabStore } from '@renderer/stores/tabStore'
import { cn } from '@renderer/lib/utils'
import { APP_VERSION } from '@renderer/version'

const MIN_WIDTH = 48
const MAX_WIDTH = 300
const DEFAULT_WIDTH = 220

const CATEGORY_GROUPS: { key: string; label: string }[] = [
  { key: 'base', label: 'Základné' },
  { key: 'stock', label: 'Sklad' },
  { key: 'sales', label: 'Predaj' },
  { key: 'purchase', label: 'Nákup' },
  { key: 'accounting', label: 'Účtovníctvo' },
  { key: 'pos', label: 'Pokladňa' },
  { key: 'system', label: 'Systém' }
]

function getModuleCategory(mod: NexModule): string {
  return mod.category ?? 'base'
}

export default function Sidebar(): ReactElement {
  const { sidebarOpen, toggleSidebar } = useUiStore()
  const { modules } = useModuleStore()
  const { addTab } = useTabStore()

  const [sidebarWidth, setSidebarWidth] = useState(DEFAULT_WIDTH)
  const [isResizing, setIsResizing] = useState(false)
  const sidebarRef = useRef<HTMLDivElement>(null)

  // Local mock state for favorites and recent (moduleStore lacks these)
  const [favoriteIds] = useState<string[]>(() =>
    modules.filter((_, i) => i < 3).map((m) => m.id)
  )
  const [recentIds] = useState<string[]>(() =>
    modules.slice(0, 10).map((m) => m.id)
  )

  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    () => new Set(['base'])
  )

  const collapsed = !sidebarOpen
  const currentWidth = collapsed ? MIN_WIDTH : sidebarWidth

  // Resize handlers
  const handleMouseDown = useCallback(
    (e: React.MouseEvent): void => {
      if (collapsed) return
      e.preventDefault()
      setIsResizing(true)
    },
    [collapsed]
  )

  useEffect(() => {
    if (!isResizing) return

    const handleMouseMove = (e: MouseEvent): void => {
      const newWidth = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH + 1, e.clientX))
      setSidebarWidth(newWidth)
    }

    const handleMouseUp = (): void => {
      setIsResizing(false)
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isResizing])

  const handleOpenTab = useCallback(
    (mod: NexModule): void => {
      addTab({ id: mod.id, label: mod.name, icon: mod.icon, closable: true })
    },
    [addTab]
  )

  const toggleCategory = useCallback((key: string): void => {
    setExpandedCategories((prev) => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }, [])

  const favorites = modules.filter((m) => favoriteIds.includes(m.id))
  const recent = modules.filter((m) => recentIds.includes(m.id)).slice(0, 10)

  const renderModuleItem = (mod: NexModule): ReactElement => (
    <button
      key={mod.id}
      onClick={() => handleOpenTab(mod)}
      className={cn(
        'flex items-center gap-2 w-full rounded-md text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors',
        collapsed ? 'justify-center p-2' : 'px-2 py-1.5'
      )}
      title={collapsed ? mod.name : undefined}
    >
      <span className="text-base shrink-0">{mod.icon ?? '📦'}</span>
      {!collapsed && <span className="truncate">{mod.name}</span>}
    </button>
  )

  return (
    <div
      ref={sidebarRef}
      className="bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 h-full flex flex-col relative select-none"
      style={{ width: currentWidth, minWidth: currentWidth }}
    >
      {/* Collapse/expand toggle */}
      <div className={cn('flex items-center p-2', collapsed ? 'justify-center' : 'justify-end')}>
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          title={collapsed ? 'Rozbaliť' : 'Zbaliť'}
        >
          {collapsed ? (
            <PanelLeftOpen className="h-4 w-4" />
          ) : (
            <PanelLeftClose className="h-4 w-4" />
          )}
        </button>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto px-2 space-y-4">
        {/* Favorites */}
        <section>
          {!collapsed && (
            <h3 className="flex items-center gap-1.5 text-xs font-semibold uppercase text-gray-400 dark:text-gray-500 mb-1 px-1">
              <Star className="h-3.5 w-3.5" />
              Obľúbené
            </h3>
          )}
          {collapsed && (
            <div className="flex justify-center mb-1">
              <Star className="h-4 w-4 text-gray-400" />
            </div>
          )}
          <div className="space-y-0.5">
            {favorites.map(renderModuleItem)}
          </div>
        </section>

        {/* Recent */}
        <section>
          {!collapsed && (
            <h3 className="flex items-center gap-1.5 text-xs font-semibold uppercase text-gray-400 dark:text-gray-500 mb-1 px-1">
              <Clock className="h-3.5 w-3.5" />
              Nedávne
            </h3>
          )}
          {collapsed && (
            <div className="flex justify-center mb-1">
              <Clock className="h-4 w-4 text-gray-400" />
            </div>
          )}
          <div className="space-y-0.5">
            {recent.map(renderModuleItem)}
          </div>
        </section>

        {/* Categories */}
        {!collapsed && (
          <section>
            <h3 className="text-xs font-semibold uppercase text-gray-400 dark:text-gray-500 mb-1 px-1">
              Kategórie
            </h3>
            {CATEGORY_GROUPS.map((group) => {
              const groupModules = modules.filter(
                (m) => getModuleCategory(m) === group.key
              )
              if (groupModules.length === 0) return null
              const isExpanded = expandedCategories.has(group.key)
              return (
                <div key={group.key} className="mb-1">
                  <button
                    onClick={() => toggleCategory(group.key)}
                    className="flex items-center gap-1 w-full px-1 py-1 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 transition-colors"
                  >
                    <ChevronRight
                      className={cn(
                        'h-4 w-4 transition-transform',
                        isExpanded && 'rotate-90'
                      )}
                    />
                    <span>{group.label}</span>
                  </button>
                  {isExpanded && (
                    <div className="ml-3 space-y-0.5">
                      {groupModules.map(renderModuleItem)}
                    </div>
                  )}
                </div>
              )
            })}
          </section>
        )}
      </div>

      {/* Version footer */}
      <div
        className={cn(
          'mt-auto border-t border-gray-200 dark:border-gray-700 p-2 text-xs text-gray-400 dark:text-gray-500',
          collapsed ? 'text-center' : ''
        )}
      >
        {collapsed ? 'v' : `v${APP_VERSION}`}
      </div>

      {/* Resize handle */}
      {!collapsed && (
        <div
          onMouseDown={handleMouseDown}
          className={cn(
            'absolute right-0 top-0 w-1 h-full cursor-col-resize hover:bg-blue-400/50 transition-colors',
            isResizing && 'bg-blue-500/50'
          )}
        />
      )}
    </div>
  )
}
