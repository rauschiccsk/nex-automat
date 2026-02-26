import { create } from 'zustand'
import { api, type ApiError } from '@renderer/lib/api'

export interface AuthUser {
  id: string
  username: string
  email?: string
  role?: string
  // New fields from /api/auth/me
  userId?: string
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
    // Call real API
    const loginRes = await api.login(username, password)

    // Fetch user profile
    const me = await api.getMe()

    const user: AuthUser = {
      id: me.user_id,
      username: me.username,
      email: me.email,
      fullName: me.full_name,
      userId: me.user_id,
      groups: me.groups
    }

    set({
      user,
      token: loginRes.access_token,
      authenticated: true,
      permissions: me.permissions
    })
  },

  logout: (): void => {
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
