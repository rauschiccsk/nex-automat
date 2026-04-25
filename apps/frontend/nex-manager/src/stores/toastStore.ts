import { create } from 'zustand'
import { getConfigNumber } from '@renderer/lib/config'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
  id: string
  message: string
  type: ToastType
  duration?: number
}

interface ToastState {
  toasts: Toast[]
  addToast: (message: string, type?: ToastType, duration?: number) => void
  removeToast: (id: string) => void
  clearAll: () => void
}

let nextId = 0

export const useToastStore = create<ToastState>((set) => ({
  toasts: [],

  addToast: (message, type = 'info', duration?: number): void => {
    const effectiveDuration =
      duration === undefined ? getConfigNumber('ui.toast_default_duration_ms') : duration
    const id = String(++nextId)
    set((state) => ({
      toasts: [...state.toasts, { id, message, type, duration: effectiveDuration }]
    }))
    if (effectiveDuration > 0) {
      setTimeout(() => {
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id)
        }))
      }, effectiveDuration)
    }
  },

  removeToast: (id): void => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id)
    }))
  },

  clearAll: (): void => {
    set({ toasts: [] })
  }
}))
