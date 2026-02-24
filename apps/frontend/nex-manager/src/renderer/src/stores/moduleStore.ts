import { create } from 'zustand'

export interface NexModule {
  id: string
  name: string
  icon?: string
  enabled: boolean
  order?: number
}

interface ModuleState {
  modules: NexModule[]
  activeModuleId: string | null
  setModules: (modules: NexModule[]) => void
  setActiveModule: (id: string | null) => void
  toggleModule: (id: string) => void
  getModule: (id: string) => NexModule | undefined
}

export const useModuleStore = create<ModuleState>((set, get) => ({
  modules: [],
  activeModuleId: null,

  setModules: (modules): void => {
    set({ modules })
  },

  setActiveModule: (id): void => {
    set({ activeModuleId: id })
  },

  toggleModule: (id): void => {
    set((state) => ({
      modules: state.modules.map((m) => (m.id === id ? { ...m, enabled: !m.enabled } : m))
    }))
  },

  getModule: (id): NexModule | undefined => {
    return get().modules.find((m) => m.id === id)
  }
}))
