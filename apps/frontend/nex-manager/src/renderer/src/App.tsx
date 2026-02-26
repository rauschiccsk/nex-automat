import { useEffect, useMemo, type ReactElement } from 'react'
import { LayoutDashboard } from 'lucide-react'

import Header from '@renderer/components/Header'
import Sidebar from '@renderer/components/Sidebar'
import TabBar from '@renderer/components/TabBar'
import Breadcrumbs, { type BreadcrumbItem } from '@renderer/components/Breadcrumbs'
import MockModule from '@renderer/components/MockModule'
import CommandLine from '@renderer/components/CommandLine'
import InfoPanel from '@renderer/components/InfoPanel'
import LoginScreen from '@renderer/components/LoginScreen'
import Toast from '@renderer/components/Toast'

import { useAuthStore } from '@renderer/stores/authStore'
import { useUiStore } from '@renderer/stores/uiStore'
import { useTabStore } from '@renderer/stores/tabStore'
import { useModuleStore } from '@renderer/stores/moduleStore'

function App(): ReactElement {
  const { authenticated, logout } = useAuthStore()
  const { theme } = useUiStore()
  const { activeTabId, tabs } = useTabStore()
  const { modules, loadModules } = useModuleStore()

  // Dark mode: sync document.documentElement class
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [theme])

  // After login: ensure modules are loaded (fallback if LoginScreen didn't load them)
  useEffect(() => {
    if (authenticated && modules.length === 0) {
      loadModules().catch(() => logout())
    }
  }, [authenticated]) // eslint-disable-line react-hooks/exhaustive-deps

  // Find active tab and its module for breadcrumbs
  const activeTab = useMemo(() => {
    if (!activeTabId) return null
    return tabs.find((t) => t.id === activeTabId) ?? null
  }, [tabs, activeTabId])

  const activeModule = useMemo(() => {
    if (!activeTab) return null
    return modules.find((m) => m.id === activeTab.id) ?? null
  }, [activeTab, modules])

  const breadcrumbItems = useMemo((): BreadcrumbItem[] => {
    const items: BreadcrumbItem[] = [{ label: 'NEX Automat' }]
    if (activeModule) {
      // Derive category from module id prefix
      const dotIdx = activeModule.id.indexOf('.')
      if (dotIdx > 0) {
        items.push({ label: activeModule.id.substring(0, dotIdx) })
      }
      items.push({ label: activeModule.name })
    }
    return items
  }, [activeModule])

  // Unauthenticated: login screen
  if (!authenticated) {
    return (
      <>
        <LoginScreen />
        <Toast />
      </>
    )
  }

  // Authenticated: main shell
  return (
    <div className="h-screen flex flex-col bg-white dark:bg-gray-900">
      {/* Header */}
      <Header />

      {/* Middle section: Sidebar + Main + InfoPanel */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar: left panel */}
        <Sidebar />

        {/* Main content area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* TabBar */}
          <TabBar />

          {/* Breadcrumbs */}
          <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700 shrink-0">
            <Breadcrumbs items={breadcrumbItems} />
          </div>

          {/* Content */}
          <div className="flex-1 overflow-auto p-4">
            {activeTab ? (
              <MockModule
                title={activeTab.label}
                description={`Modul ${activeTab.id} \u2014 obsah bude implementovan\u00fd`}
                icon={<LayoutDashboard className="h-8 w-8" />}
              />
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <LayoutDashboard className="h-16 w-16 text-gray-300 dark:text-gray-600 mb-4" />
                <h2 className="text-xl font-semibold text-gray-600 dark:text-gray-400 mb-2">
                  Vyberte modul z bo&#269;n&#233;ho panela
                </h2>
                <p className="text-sm text-gray-400 dark:text-gray-500">
                  Alebo pou&#382;ite kl&#225;ves{' '}
                  <kbd className="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs font-mono">
                    /
                  </kbd>{' '}
                  pre vyh&#318;ad&#225;vanie
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* CommandLine: bottom */}
      <CommandLine />

      {/* InfoPanel: always rendered, positioned fixed/slide-in based on internal state */}
      <InfoPanel />

      {/* Toast: always rendered, fixed position, z-50 */}
      <Toast />
    </div>
  )
}

export default App
