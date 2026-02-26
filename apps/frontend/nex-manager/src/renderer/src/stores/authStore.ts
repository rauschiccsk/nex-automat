import { create } from 'zustand'
import { api, type ApiError } from '@renderer/lib/api'

export interface AuthUser {
  id: number
  name: string
  username: string
  email?: string
  role?: string
  fullName?: string
  groups?: string[]
}

export type { ApiError }

interface AuthState {
  user: AuthUser | null
  token: string | null
  authenticated: boolean
  permissions: Record<string, string[]>

  login: (username: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: AuthUser) => void
  checkPermission: (moduleCode: string, permission: string) => boolean
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  authenticated: false,
  permissions: {},

  login: async (username: string, password: string): Promise<void> => {
    console.debug('[AUTH] authStore.login() called for:', username)
    // Call real API
    const loginRes = await api.login(username, password)
    console.debug('[AUTH] authStore: login API OK, fetching /me…')

    // Fetch user profile (nested: me.user.*, me.permissions[])
    const me = await api.getMe()
    const u = me.user

    const user: AuthUser = {
      id: u.user_id,
      name: u.full_name || u.login_name || 'Používateľ',
      username: u.login_name,
      email: u.email,
      fullName: u.full_name,
      groups: u.groups ?? []
    }

    // Transform permissions array to Record<module_code, string[]>
    const permissions: Record<string, string[]> = {}
    for (const p of me.permissions ?? []) {
      const perms: string[] = []
      if (p.can_view) perms.push('view')
      if (p.can_create) perms.push('create')
      if (p.can_edit) perms.push('edit')
      if (p.can_delete) perms.push('delete')
      if (p.can_print) perms.push('print')
      if (p.can_export) perms.push('export')
      if (p.can_admin) perms.push('admin')
      permissions[p.module_code] = perms
    }

    console.debug('[AUTH] authStore: /me OK, setting authenticated=true, user:', user.username)
    set({
      user,
      token: loginRes.access_token,
      authenticated: true,
      permissions
    })
  },

  logout: (): void => {
    console.debug('[AUTH] authStore.logout() called — stack:', new Error().stack?.split('\n').slice(1, 4).join(' ← '))
    api.clearTokens()
    set({
      user: null,
      token: null,
      authenticated: false,
      permissions: {}
    })
  },

  setUser: (user): void => {
    set({ user })
  },

  checkPermission: (moduleCode: string, permission: string): boolean => {
    const perms = get().permissions[moduleCode]
    if (!perms) return false
    return perms.includes(permission)
  }
}))
