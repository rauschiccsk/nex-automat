import { useState, useCallback, type ReactElement, type FormEvent } from 'react'
import { Eye, EyeOff, LogIn, Moon, Sun, User, Lock, Loader2, AlertCircle } from 'lucide-react'
import { useAuthStore, type ApiError } from '@renderer/stores/authStore'
import { useModuleStore } from '@renderer/stores/moduleStore'
import { useUiStore } from '@renderer/stores/uiStore'
import { cn } from '@renderer/lib/utils'

export default function LoginScreen(): ReactElement {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { login } = useAuthStore()
  const { loadModules } = useModuleStore()
  const { theme, setTheme } = useUiStore()
  const isDark = theme === 'dark'

  const isValid = username.trim().length > 0 && password.trim().length > 0

  const handleToggleTheme = useCallback((): void => {
    setTheme(isDark ? 'light' : 'dark')
  }, [isDark, setTheme])

  const handleSubmit = useCallback(
    (e: FormEvent): void => {
      e.preventDefault()
      if (!isValid || loading) return

      setError(null)
      setLoading(true)

      console.debug('[AUTH] LoginScreen: submitting login…')
      login(username.trim(), password)
        .then(() => {
          console.debug('[AUTH] LoginScreen: login OK, loading modules…')
          return loadModules()
        })
        .then(() => {
          console.debug('[AUTH] LoginScreen: modules loaded OK')
        })
        .catch((err: ApiError) => {
          console.warn('[AUTH] LoginScreen: login/loadModules failed:', err)
          if (err.status === 401) {
            setError('Nesprávne prihlasovacie údaje')
          } else if (err.status === 0 || !err.status) {
            setError('Server nie je dostupný. Skúste to neskôr.')
          } else {
            setError(err.message || 'Prihlásenie zlyhalo')
          }
        })
        .finally(() => setLoading(false))
    },
    [username, password, isValid, loading, login, loadModules]
  )

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 relative">
      {/* Theme toggle - top right */}
      <button
        onClick={handleToggleTheme}
        className="absolute top-4 right-4 p-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-white/50 dark:hover:bg-gray-700/50 transition-colors"
        aria-label="Prepnúť tému"
      >
        {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      </button>

      {/* Login box */}
      <div className="w-full max-w-md mx-auto px-4">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 p-8">
          {/* Logo */}
          <div className="flex flex-col items-center mb-8">
            <div className="bg-blue-600 text-white w-14 h-14 rounded-full flex items-center justify-center font-bold text-2xl mb-3 shadow-lg shadow-blue-600/30">
              N
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">NEX Automat</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Prihlásenie do systému
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username */}
            <div>
              <label
                htmlFor="login-username"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
              >
                Používateľské meno
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  id="login-username"
                  type="text"
                  value={username}
                  onChange={(e) => { setUsername(e.target.value); setError(null) }}
                  disabled={loading}
                  placeholder="Zadajte meno"
                  autoComplete="username"
                  className={cn(
                    'w-full pl-10 pr-4 py-2.5 rounded-lg border text-sm transition-colors outline-none',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'border-gray-300 dark:border-gray-600',
                    'placeholder-gray-400 dark:placeholder-gray-500',
                    'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                    'disabled:opacity-50 disabled:cursor-not-allowed'
                  )}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="login-password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
              >
                Heslo
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  id="login-password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setError(null) }}
                  disabled={loading}
                  placeholder="Zadajte heslo"
                  autoComplete="current-password"
                  className={cn(
                    'w-full pl-10 pr-10 py-2.5 rounded-lg border text-sm transition-colors outline-none',
                    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
                    'border-gray-300 dark:border-gray-600',
                    'placeholder-gray-400 dark:placeholder-gray-500',
                    'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
                    'disabled:opacity-50 disabled:cursor-not-allowed'
                  )}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  aria-label={showPassword ? 'Skryť heslo' : 'Zobraziť heslo'}
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Error message */}
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                <AlertCircle className="h-4 w-4 text-red-500 shrink-0" />
                <span className="text-sm text-red-700 dark:text-red-400">{error}</span>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={!isValid || loading}
              className={cn(
                'w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700',
                'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600'
              )}
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <LogIn className="h-4 w-4" />
              )}
              {loading ? 'Prihlasovanie...' : 'Prihlásiť sa'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
