import { create } from 'zustand'

export interface AuthUser {
  id: string
  username: string
  email?: string
  role?: string
}

interface AuthState {
  user: AuthUser | null
  token: string | null
  authenticated: boolean
  login: (user: AuthUser, token: string) => void
  logout: () => void
  setUser: (user: AuthUser) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  authenticated: false,

  login: (user, token): void => {
    set({ user, token, authenticated: true })
  },

  logout: (): void => {
    set({ user: null, token: null, authenticated: false })
  },

  setUser: (user): void => {
    set({ user })
  }
}))
