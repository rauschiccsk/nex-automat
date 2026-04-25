import { useState, useEffect, useCallback, type ReactElement, type FormEvent } from 'react'
import { X, Loader2, Eye, EyeOff } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import type { User, UserGroup } from '@renderer/types/users'

interface UserFormDialogProps {
  user: User | null // null = create mode
  onClose: (saved: boolean) => void
}

export default function UserFormDialog({ user, onClose }: UserFormDialogProps): ReactElement {
  const { addToast } = useToastStore()
  const isEdit = user != null

  // ── Form state ──
  const [username, setUsername] = useState(user?.login_name ?? '')
  const [fullName, setFullName] = useState(user?.full_name ?? '')
  const [email, setEmail] = useState(user?.email ?? '')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isActive, setIsActive] = useState(user?.is_active ?? true)
  const [selectedGroupIds, setSelectedGroupIds] = useState<number[]>(
    user?.groups.map((g) => g.group_id) ?? []
  )

  // ── Available groups ──
  const [allGroups, setAllGroups] = useState<UserGroup[]>([])

  // ── UI state ──
  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  // Load available groups from existing users data (lightweight approach)
  useEffect(() => {
    api
      .getUsers()
      .then((res) => {
        const map = new Map<number, UserGroup>()
        for (const u of res.users) {
          for (const g of u.groups) {
            if (!map.has(g.group_id)) map.set(g.group_id, g)
          }
        }
        setAllGroups(
          Array.from(map.values()).sort((a, b) => a.group_name.localeCompare(b.group_name))
        )
      })
      .catch(() => {
        // Groups will be empty — not critical
      })
  }, [])

  // ── Validation ──
  const validate = useCallback((): boolean => {
    const errs: Record<string, string> = {}

    if (!isEdit && !username.trim()) errs.username = 'Povinné pole'
    if (!fullName.trim()) errs.fullName = 'Povinné pole'
    if (!isEdit && !email.trim()) errs.email = 'Povinné pole'
    if (email.trim() && (!email.includes('@') || !email.includes('.'))) {
      errs.email = 'Neplatný formát e-mailu'
    }
    if (!isEdit && !password) errs.password = 'Povinné pole'
    if (!isEdit && password && password.length < 6) {
      errs.password = 'Minimálne 6 znakov'
    }

    setErrors(errs)
    return Object.keys(errs).length === 0
  }, [isEdit, username, fullName, email, password])

  // ── Submit ──
  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return

      setSaving(true)
      try {
        if (isEdit && user) {
          await api.updateUser(user.user_id, {
            full_name: fullName.trim(),
            email: email.trim() || undefined,
            is_active: isActive,
            group_ids: selectedGroupIds.length > 0 ? selectedGroupIds : undefined
          })
          addToast('Používateľ bol aktualizovaný', 'success')
        } else {
          await api.createUser({
            username: username.trim(),
            full_name: fullName.trim(),
            email: email.trim(),
            password,
            is_active: isActive,
            group_ids: selectedGroupIds.length > 0 ? selectedGroupIds : undefined
          })
          addToast('Používateľ bol vytvorený', 'success')
        }
        onClose(true)
      } catch (err) {
        const e = err as ApiError
        if (e.status === 409) {
          addToast('Používateľské meno už existuje', 'error')
          setErrors((prev) => ({ ...prev, username: 'Už existuje' }))
        } else {
          addToast(e.message || 'Uloženie zlyhalo', 'error')
        }
      } finally {
        setSaving(false)
      }
    },
    [
      validate,
      isEdit,
      user,
      username,
      fullName,
      email,
      password,
      isActive,
      selectedGroupIds,
      onClose,
      addToast
    ]
  )

  const handleGroupToggle = useCallback((groupId: number): void => {
    setSelectedGroupIds((prev) =>
      prev.includes(groupId) ? prev.filter((id) => id !== groupId) : [...prev, groupId]
    )
  }, [])

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-40 bg-black/40" onClick={() => onClose(false)} />

      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {isEdit ? 'Upraviť používateľa' : 'Nový používateľ'}
            </h2>
            <button
              onClick={() => onClose(false)}
              className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={(e) => void handleSubmit(e)} className="px-6 py-4 space-y-4">
            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Používateľské meno
              </label>
              {isEdit ? (
                <div className="px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-sm text-gray-500 dark:text-gray-400">
                  {user?.login_name}
                </div>
              ) : (
                <>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => {
                      setUsername(e.target.value)
                      setErrors((prev) => ({ ...prev, username: '' }))
                    }}
                    disabled={saving}
                    className={cn(
                      'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
                      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                      errors.username
                        ? 'border-red-500 focus:ring-red-500/20'
                        : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                      'disabled:opacity-50'
                    )}
                  />
                  {errors.username && (
                    <p className="mt-1 text-xs text-red-500">{errors.username}</p>
                  )}
                </>
              )}
            </div>

            {/* Full name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Celé meno
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => {
                  setFullName(e.target.value)
                  setErrors((prev) => ({ ...prev, fullName: '' }))
                }}
                disabled={saving}
                className={cn(
                  'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  errors.fullName
                    ? 'border-red-500 focus:ring-red-500/20'
                    : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                  'disabled:opacity-50'
                )}
              />
              {errors.fullName && <p className="mt-1 text-xs text-red-500">{errors.fullName}</p>}
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                E-mail
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value)
                  setErrors((prev) => ({ ...prev, email: '' }))
                }}
                disabled={saving}
                className={cn(
                  'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
                  'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                  errors.email
                    ? 'border-red-500 focus:ring-red-500/20'
                    : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                  'disabled:opacity-50'
                )}
              />
              {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email}</p>}
            </div>

            {/* Password (create mode only) */}
            {!isEdit && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Heslo
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value)
                      setErrors((prev) => ({ ...prev, password: '' }))
                    }}
                    disabled={saving}
                    className={cn(
                      'w-full px-3 pr-10 py-2 rounded-lg border text-sm transition-colors outline-none',
                      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                      errors.password
                        ? 'border-red-500 focus:ring-red-500/20'
                        : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                      'disabled:opacity-50'
                    )}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((p) => !p)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="mt-1 text-xs text-red-500">{errors.password}</p>
                )}
              </div>
            )}

            {/* Active checkbox */}
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
                disabled={saving}
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">Aktívny</span>
            </label>

            {/* Groups */}
            {allGroups.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Skupiny
                </label>
                <div className="flex flex-wrap gap-2">
                  {allGroups.map((g) => (
                    <button
                      key={g.group_id}
                      type="button"
                      onClick={() => handleGroupToggle(g.group_id)}
                      disabled={saving}
                      className={cn(
                        'px-3 py-1.5 rounded-lg border text-sm transition-colors',
                        selectedGroupIds.includes(g.group_id)
                          ? 'bg-blue-100 border-blue-300 text-blue-700 dark:bg-blue-900/30 dark:border-blue-600 dark:text-blue-400'
                          : 'bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600',
                        'disabled:opacity-50'
                      )}
                    >
                      {g.group_name}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </form>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            <button
              type="button"
              onClick={() => onClose(false)}
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
              form=""
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
              {isEdit ? 'Uložiť' : 'Vytvoriť'}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
