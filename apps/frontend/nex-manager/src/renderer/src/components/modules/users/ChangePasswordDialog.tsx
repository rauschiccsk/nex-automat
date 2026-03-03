import { useState, useCallback, type ReactElement, type FormEvent } from 'react'
import { X, Loader2, Eye, EyeOff } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'

interface AdminModeProps {
  userId: number
  username: string
  onClose: () => void
}

interface SelfModeProps {
  userId?: undefined
  username?: undefined
  onClose: () => void
}

type ChangePasswordDialogProps = AdminModeProps | SelfModeProps

export default function ChangePasswordDialog(props: ChangePasswordDialogProps): ReactElement {
  const { onClose } = props
  const isAdminMode = props.userId != null
  const { addToast } = useToastStore()

  // ── Form state ──
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showCurrent, setShowCurrent] = useState(false)
  const [showNew, setShowNew] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  // ── UI state ──
  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const title = isAdminMode ? `Zmena hesla \u2014 ${props.username}` : 'Zmena vlastného hesla'

  // ── Validation ──
  const validate = useCallback((): boolean => {
    const errs: Record<string, string> = {}

    if (!isAdminMode && !currentPassword) errs.currentPassword = 'Povinné pole'
    if (!newPassword) errs.newPassword = 'Povinné pole'
    else if (newPassword.length < 6) errs.newPassword = 'Minimálne 6 znakov'
    if (!confirmPassword) errs.confirmPassword = 'Povinné pole'
    else if (newPassword !== confirmPassword) errs.confirmPassword = 'Heslá sa nezhodujú'

    setErrors(errs)
    return Object.keys(errs).length === 0
  }, [isAdminMode, currentPassword, newPassword, confirmPassword])

  // ── Submit ──
  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return

      setSaving(true)
      try {
        if (isAdminMode) {
          await api.changeUserPassword(props.userId, newPassword)
        } else {
          await api.changeSelfPassword(currentPassword, newPassword)
        }
        addToast('Heslo bolo zmenené', 'success')
        onClose()
      } catch (err) {
        const apiErr = err as ApiError
        if (!isAdminMode && apiErr.status === 401) {
          setErrors((prev) => ({ ...prev, currentPassword: 'Nesprávne aktuálne heslo' }))
          addToast('Nesprávne aktuálne heslo', 'error')
        } else {
          addToast(apiErr.message || 'Zmena hesla zlyhala', 'error')
        }
      } finally {
        setSaving(false)
      }
    },
    [validate, isAdminMode, props, newPassword, currentPassword, onClose, addToast]
  )

  const inputClasses = (fieldError?: string): string =>
    cn(
      'w-full px-3 pr-10 py-2 rounded-lg border text-sm transition-colors outline-none',
      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
      fieldError
        ? 'border-red-500 focus:ring-red-500/20'
        : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
      'disabled:opacity-50'
    )

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-40 bg-black/40" onClick={onClose} />

      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl w-full max-w-md">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">{title}</h2>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={(e) => void handleSubmit(e)} className="px-6 py-4 space-y-4">
            {/* Current password (self mode only) */}
            {!isAdminMode && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Aktuálne heslo
                </label>
                <div className="relative">
                  <input
                    type={showCurrent ? 'text' : 'password'}
                    value={currentPassword}
                    onChange={(e) => {
                      setCurrentPassword(e.target.value)
                      setErrors((prev) => ({ ...prev, currentPassword: '' }))
                    }}
                    disabled={saving}
                    autoComplete="current-password"
                    className={inputClasses(errors.currentPassword)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrent((p) => !p)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    tabIndex={-1}
                  >
                    {showCurrent ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
                {errors.currentPassword && (
                  <p className="mt-1 text-xs text-red-500">{errors.currentPassword}</p>
                )}
              </div>
            )}

            {/* New password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Nové heslo
              </label>
              <div className="relative">
                <input
                  type={showNew ? 'text' : 'password'}
                  value={newPassword}
                  onChange={(e) => {
                    setNewPassword(e.target.value)
                    setErrors((prev) => ({ ...prev, newPassword: '' }))
                  }}
                  disabled={saving}
                  autoComplete="new-password"
                  className={inputClasses(errors.newPassword)}
                />
                <button
                  type="button"
                  onClick={() => setShowNew((p) => !p)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  tabIndex={-1}
                >
                  {showNew ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.newPassword && (
                <p className="mt-1 text-xs text-red-500">{errors.newPassword}</p>
              )}
            </div>

            {/* Confirm password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Potvrdiť nové heslo
              </label>
              <div className="relative">
                <input
                  type={showConfirm ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value)
                    setErrors((prev) => ({ ...prev, confirmPassword: '' }))
                  }}
                  disabled={saving}
                  autoComplete="new-password"
                  className={inputClasses(errors.confirmPassword)}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirm((p) => !p)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  tabIndex={-1}
                >
                  {showConfirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-xs text-red-500">{errors.confirmPassword}</p>
              )}
            </div>
          </form>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            <button
              type="button"
              onClick={onClose}
              disabled={saving}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300',
                'hover:bg-gray-50 dark:hover:bg-gray-700',
                'disabled:opacity-50'
              )}
            >
              Zrušiť
            </button>
            <button
              type="submit"
              onClick={(e) => {
                e.preventDefault()
                void handleSubmit(e as unknown as FormEvent)
              }}
              disabled={saving}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700',
                'disabled:opacity-50 disabled:cursor-not-allowed'
              )}
            >
              {saving && <Loader2 className="h-4 w-4 animate-spin" />}
              Zmeniť heslo
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
