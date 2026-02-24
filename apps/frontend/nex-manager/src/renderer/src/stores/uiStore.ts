import { create } from 'zustand'

interface UiState {
  sidebarOpen: boolean
  theme: 'light' | 'dark' | 'system'
  loading: boolean
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  setLoading: (loading: boolean) => void
}

export const useUiStore = create<UiState>((set) => ({
  sidebarOpen: true,
  theme: 'system',
  loading: false,

  toggleSidebar: (): void => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }))
  },

  setSidebarOpen: (open): void => {
    set({ sidebarOpen: open })
  },

  setTheme: (theme): void => {
    set({ theme })
  },

  setLoading: (loading): void => {
    set({ loading })
  }
}))
