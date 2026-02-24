import { create } from 'zustand'

interface UiState {
  sidebarOpen: boolean
  infoPanelOpen: boolean
  theme: 'light' | 'dark' | 'system'
  loading: boolean
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  toggleInfoPanel: () => void
  setInfoPanelOpen: (open: boolean) => void
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  setLoading: (loading: boolean) => void
}

export const useUiStore = create<UiState>((set) => ({
  sidebarOpen: true,
  infoPanelOpen: false,
  theme: 'system',
  loading: false,

  toggleSidebar: (): void => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }))
  },

  setSidebarOpen: (open): void => {
    set({ sidebarOpen: open })
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
  }
}))
