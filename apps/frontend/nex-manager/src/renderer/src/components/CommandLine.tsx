import { useState, useEffect, useRef, useCallback, useMemo, type ReactElement } from 'react'
import { Terminal, Search } from 'lucide-react'
import { useTabStore } from '@renderer/stores/tabStore'
import { useModuleStore, type NexModule } from '@renderer/stores/moduleStore'
import { useToastStore } from '@renderer/stores/toastStore'
import { useUiStore } from '@renderer/stores/uiStore'
import { cn } from '@renderer/lib/utils'

const HELP_TEXT = [
  '/open [modul] alebo /o [modul] — otvoriť modul',
  '/close alebo /c — zatvoriť aktívny tab',
  '/theme dark | light — prepnúť tému',
  '/help alebo /h — zobraziť nápovedu'
].join('\n')

export default function CommandLine(): ReactElement {
  const [active, setActive] = useState(false)
  const [input, setInput] = useState('')
  const [selectedIndex, setSelectedIndex] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)

  const { modules } = useModuleStore()
  const { addTab, removeTab, activeTabId } = useTabStore()
  const { addToast } = useToastStore()
  const { setTheme } = useUiStore()

  // Filter modules for autocomplete
  const filtered = useMemo((): NexModule[] => {
    const trimmed = input.trim().toLowerCase()
    // Extract search term after /open or /o prefix
    let search = trimmed
    if (trimmed.startsWith('/open ') || trimmed.startsWith('/o ')) {
      search = trimmed.startsWith('/open ') ? trimmed.slice(6) : trimmed.slice(3)
    } else if (trimmed.startsWith('/') || trimmed === '') {
      return []
    }
    if (!search) return []

    return modules
      .filter(
        (m) =>
          m.id.toLowerCase().includes(search) || m.name.toLowerCase().includes(search)
      )
      .slice(0, 8)
  }, [input, modules])

  // Reset selection when filtered list changes
  useEffect(() => {
    setSelectedIndex(0)
  }, [filtered.length])

  // Global "/" listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent): void => {
      if (active) return
      const tag = (e.target as HTMLElement)?.tagName
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return
      if ((e.target as HTMLElement)?.isContentEditable) return
      if (e.key === '/') {
        e.preventDefault()
        setActive(true)
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [active])

  // Focus input when activated
  useEffect(() => {
    if (active) {
      inputRef.current?.focus()
    } else {
      setInput('')
      setSelectedIndex(0)
    }
  }, [active])

  const openModule = useCallback(
    (mod: NexModule): void => {
      addTab({ id: mod.id, label: mod.name, icon: mod.icon, closable: true })
      setActive(false)
    },
    [addTab]
  )

  const executeCommand = useCallback((): void => {
    const trimmed = input.trim()
    if (!trimmed) return

    // /help
    if (trimmed === '/help' || trimmed === '/h') {
      addToast(HELP_TEXT, 'info', 8000)
      setActive(false)
      return
    }

    // /close
    if (trimmed === '/close' || trimmed === '/c') {
      if (activeTabId) {
        removeTab(activeTabId)
      } else {
        addToast('Žiadny aktívny tab na zatvorenie', 'warning')
      }
      setActive(false)
      return
    }

    // /theme
    if (trimmed.startsWith('/theme ')) {
      const themeVal = trimmed.slice(7).trim()
      if (themeVal === 'dark' || themeVal === 'light') {
        setTheme(themeVal)
        addToast(`Téma nastavená na ${themeVal}`, 'success', 2000)
      } else {
        addToast('Použitie: /theme dark | light', 'error')
      }
      setActive(false)
      return
    }

    // /open or /o
    if (trimmed.startsWith('/open ') || trimmed.startsWith('/o ')) {
      const search = (trimmed.startsWith('/open ') ? trimmed.slice(6) : trimmed.slice(3)).trim().toLowerCase()
      if (!search) {
        addToast('Zadajte názov alebo ID modulu', 'warning')
        return
      }
      const found = modules.find(
        (m) => m.id.toLowerCase() === search || m.name.toLowerCase() === search
      )
      if (found) {
        openModule(found)
      } else if (filtered.length > 0) {
        openModule(filtered[0])
      } else {
        addToast(`Modul "${search}" sa nenašiel`, 'error')
      }
      setActive(false)
      return
    }

    addToast(`Nerozpoznaný príkaz: ${trimmed}`, 'error')
    setActive(false)
  }, [input, modules, filtered, activeTabId, addTab, removeTab, addToast, setTheme, openModule])

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent): void => {
      if (e.key === 'Escape') {
        e.preventDefault()
        setActive(false)
        return
      }
      if (e.key === 'Enter') {
        e.preventDefault()
        if (filtered.length > 0) {
          openModule(filtered[selectedIndex])
        } else {
          executeCommand()
        }
        return
      }
      if (e.key === 'ArrowDown') {
        e.preventDefault()
        setSelectedIndex((prev) => (prev + 1) % Math.max(filtered.length, 1))
        return
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault()
        setSelectedIndex((prev) => (prev - 1 + Math.max(filtered.length, 1)) % Math.max(filtered.length, 1))
      }
    },
    [filtered, selectedIndex, openModule, executeCommand]
  )

  // Inactive bar
  if (!active) {
    return (
      <div
        onClick={() => setActive(true)}
        className="h-8 bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-center px-3 gap-2 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors shrink-0 select-none"
      >
        <Terminal className="h-3.5 w-3.5 text-gray-400 dark:text-gray-500" />
        <span className="text-xs text-gray-400 dark:text-gray-500">
          / pre vyhľadávanie
        </span>
      </div>
    )
  }

  // Active bar with dropdown
  return (
    <div className="relative shrink-0">
      {/* Autocomplete dropdown (rendered above input) */}
      {filtered.length > 0 && (
        <div className="absolute bottom-full left-0 right-0 z-50 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-t-lg shadow-lg max-h-72 overflow-y-auto">
          {filtered.map((mod, idx) => (
            <button
              key={mod.id}
              onClick={() => openModule(mod)}
              className={cn(
                'flex items-center gap-2 w-full px-3 py-2 text-sm transition-colors',
                idx === selectedIndex
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              )}
            >
              <span className="text-base shrink-0">{mod.icon ?? '📦'}</span>
              <span className="font-medium">{mod.name}</span>
              <span className="text-xs text-gray-400 dark:text-gray-500 ml-auto">
                {mod.id}
              </span>
            </button>
          ))}
        </div>
      )}

      {/* Input bar */}
      <div className="h-10 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-center px-3 gap-2">
        <Search className="h-4 w-4 text-gray-400 dark:text-gray-500 shrink-0" />
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Zadajte príkaz (/help pre nápovedu)..."
          className="flex-1 bg-transparent text-sm text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 outline-none"
        />
        <button
          onClick={() => setActive(false)}
          className="text-xs text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
        >
          ESC
        </button>
      </div>
    </div>
  )
}
