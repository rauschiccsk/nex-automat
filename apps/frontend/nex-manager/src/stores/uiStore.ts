import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UiState {
  sidebarOpen: boolean
  sidebarWidth: number
  infoPanelOpen: boolean
  theme: 'light' | 'dark' | 'system'
  loading: boolean
  expandedCategories: string[]

  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setSidebarWidth: (width: number) => void
  toggleInfoPanel: () => void
  setInfoPanelOpen: (open: boolean) => void
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  setLoading: (loading: boolean) => void
  toggleCategory: (category: string) => void
}

export const useUiStore = create<UiState>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      sidebarWidth: 220,
      infoPanelOpen: false,
      theme: 'system',
      loading: false,
      expandedCategories: ['catalogs'],

      toggleSidebar: (): void => {
        set((state) => ({ sidebarOpen: !state.sidebarOpen }))
      },

      setSidebarOpen: (open): void => {
        set({ sidebarOpen: open })
      },

      setSidebarWidth: (width): void => {
        set({ sidebarWidth: width })
      },

      toggleInfoPanel: (): void => {
        set((state) => ({ infoPanelOpen: !state.infoPanelOpen }))
      },

      setInfoPanelOpen: (open): void => {
        set({ infoPanelOpen: open })
      },

      setTheme: (theme): void => {
        set({ theme })
      },

      setLoading: (loading): void => {
        set({ loading })
      },

      toggleCategory: (category): void => {
        set((state) => {
          const current = state.expandedCategories
          const isExpanded = current.includes(category)
          return {
            expandedCategories: isExpanded
              ? current.filter((c) => c !== category)
              : [...current, category]
          }
        })
      }
    }),
    {
      name: 'nex-ui-store',
      partialize: (state) => ({
        sidebarOpen: state.sidebarOpen,
        sidebarWidth: state.sidebarWidth,
        infoPanelOpen: state.infoPanelOpen,
        theme: state.theme,
        expandedCategories: state.expandedCategories
      })
    }
  )
)
