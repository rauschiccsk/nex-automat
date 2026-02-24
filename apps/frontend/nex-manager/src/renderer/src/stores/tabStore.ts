import { create } from 'zustand'
import { useToastStore } from '@renderer/stores/toastStore'

export interface Tab {
  id: string
  label: string
  icon?: string
  closable?: boolean
}

interface TabState {
  tabs: Tab[]
  activeTabId: string | null
  addTab: (tab: Tab) => void
  removeTab: (id: string) => void
  setActiveTab: (id: string) => void
  clearTabs: () => void
}

export const useTabStore = create<TabState>((set, get) => ({
  tabs: [],
  activeTabId: null,

  addTab: (tab): void => {
    const existing = get().tabs.find((t) => t.id === tab.id)
    if (existing) {
      set({ activeTabId: tab.id })
      return
    }
    set((state) => ({
      tabs: [...state.tabs, tab],
      activeTabId: tab.id
    }))
  },

  removeTab: (id): void => {
    const state = get()
    const idx = state.tabs.findIndex((t) => t.id === id)
    if (idx === -1) return

    const newTabs = state.tabs.filter((t) => t.id !== id)
    let newActive = state.activeTabId

    if (state.activeTabId === id) {
      if (newTabs.length > 0) {
        const newIdx = Math.min(idx, newTabs.length - 1)
        newActive = newTabs[newIdx].id
      } else {
        newActive = null
      }
    }

    set({ tabs: newTabs, activeTabId: newActive })
    useToastStore.getState().addToast(`Tab zatvorený`, 'info', 2000)
  },

  setActiveTab: (id): void => {
    set({ activeTabId: id })
  },

  clearTabs: (): void => {
    set({ tabs: [], activeTabId: null })
  }
}))
