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

let loadingSince: number | null = null
const STALE_LOCK_MS = 15_000

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
    if (get().loading) {
      const elapsed = loadingSince ? Date.now() - loadingSince : 0
      if (elapsed < STALE_LOCK_MS) {
        console.debug('[MODULES] loadModules(): already loading (' + elapsed + 'ms), skipping')
        return
      }
      console.warn('[MODULES] loadModules(): stale lock detected (' + elapsed + 'ms), resetting')
    }
    console.log('[MODULES] loadModules() called')
    loadingSince = Date.now()
    set({ loading: true })
    try {
      const categories = await api.getModulesByCategory()
      console.log('[MODULES] API response categories:', categories.length,
        'first:', JSON.stringify(categories[0]?.category ?? null))

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

      console.log('[MODULES] Stored modules count:', modules.length)
      console.log('[MODULES] Categories:', [...new Set(modules.map((m) => m.category))])
      loadingSince = null
      set({ modules, loading: false })
    } catch (err) {
      console.warn('[MODULES] loadModules() failed:', err)
      loadingSince = null
      set({ loading: false })
      throw err
    }
  }
}))
