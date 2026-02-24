import { useState, useCallback, type ReactElement } from 'react'
import { Bell, Moon, Sun, LogOut, ChevronDown, PanelRightOpen } from 'lucide-react'
import { useUiStore } from '@renderer/stores/uiStore'
import { useAuthStore } from '@renderer/stores/authStore'

function getInitials(username: string): string {
  return username
    .split(/[\s._-]+/)
    .map((part) => part.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
}

export default function Header(): ReactElement {
  const { theme, setTheme, toggleInfoPanel } = useUiStore()
  const { user, logout } = useAuthStore()
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)

  const isDark = theme === 'dark'

  const handleToggleTheme = useCallback((): void => {
    setTheme(isDark ? 'light' : 'dark')
  }, [isDark, setTheme])

  const handleLogout = useCallback((): void => {
    logout()
    setIsUserMenuOpen(false)
  }, [logout])

  const initials = user ? getInitials(user.username) : '??'
  const displayName = user?.username ?? 'Neprihlásený'

  return (
    <header className="h-14 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-4 shrink-0">
      {/* Logo */}
      <div className="flex items-center gap-2">
        <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
          N
        </div>
        <span className="font-semibold text-lg text-gray-900 dark:text-white hidden sm:block">
          NEX Automat
        </span>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-3">
        {/* Notification bell */}
        <button
          className="relative p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Notifikácie"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs w-4 h-4 rounded-full flex items-center justify-center font-medium">
            3
          </span>
        </button>

        {/* Info panel toggle */}
        <button
          onClick={toggleInfoPanel}
          className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Panel s detailmi"
        >
          <PanelRightOpen className="h-5 w-5" />
        </button>

        {/* Dark mode toggle */}
        <button
          onClick={handleToggleTheme}
          className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Prepnúť tému"
        >
          {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>

        {/* User menu */}
        <div className="relative">
          <button
            onClick={() => setIsUserMenuOpen((prev) => !prev)}
            className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <div className="bg-blue-500 text-white w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium">
              {initials}
            </div>
            <span className="text-sm text-gray-700 dark:text-gray-300 hidden sm:block">
              {displayName}
            </span>
            <ChevronDown className="h-4 w-4 text-gray-400" />
          </button>

          {isUserMenuOpen && (
            <>
              {/* Overlay to close menu */}
              <div
                className="fixed inset-0 z-40"
                onClick={() => setIsUserMenuOpen(false)}
              />
              {/* Dropdown */}
              <div className="absolute right-0 top-full mt-1 z-50 w-48 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-lg py-1">
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 w-full px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  Odhlásiť sa
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
