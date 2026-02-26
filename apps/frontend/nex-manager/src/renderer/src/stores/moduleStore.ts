import { create } from 'zustand'
import { api } from '@renderer/lib/api'

export interface NexModule {
  id: string
  name: string
  icon?: string
  enabled: boolean
  order?: number
  // New fields from API
  category?: string
  type?: string
  isMock?: boolean
}

interface ModuleState {
  modules: NexModule[]
  activeModuleId: string | null
  loading: boolean

  setModules: (modules: NexModule[]) => void
  setActiveModule: (id: string | null) => void
  toggleModule: (id: string) => void
  getModule: (id: string) => NexModule | undefined
  loadModules: () => Promise<void>
}

export const useModuleStore = create<ModuleState>((set, get) => ({
  modules: [],
  activeModuleId: null,
  loading: false,

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
  },

  loadModules: async (): Promise<void> => {
    set({ loading: true })
    try {
      const categories = await api.getModulesByCategory()

      const modules: NexModule[] = categories.flatMap((cat) =>
        cat.modules.map((m) => ({
          id: m.module_code,
          name: m.module_name,
          icon: m.icon || undefined,
          enabled: true,
          order: m.sort_order,
          category: cat.category,
          type: m.module_type,
          isMock: m.is_mock
        }))
      )

      // Sort by order
      modules.sort((a, b) => (a.order ?? 999) - (b.order ?? 999))

      set({ modules, loading: false })
    } catch (err) {
      set({ loading: false })
      throw err
    }
  }
}))
