import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Activity, LogOut, Loader2, RefreshCw } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError, type Session } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'

type Filter = 'active' | 'all' | 'mine'

const ACTIVE_THRESHOLD_MS = 30 * 60 * 1000 // 30 min
const REFRESH_INTERVAL_MS = 30 * 1000

function formatRelative(isoTs: string): string {
  const seconds = Math.floor((Date.now() - new Date(isoTs).getTime()) / 1000)
  if (seconds < 60) return 'pred chvíľou'
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `pred ${minutes} min`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `pred ${hours} h`
  const days = Math.floor(hours / 24)
  return `pred ${days} d`
}

function parseUserAgent(ua: string | null): string {
  if (!ua) return '—'
  const browser =
    ua.match(/Edg\/[\d.]+/)?.[0] ||
    ua.match(/Chrome\/[\d.]+/)?.[0] ||
    ua.match(/Firefox\/[\d.]+/)?.[0] ||
    ua.match(/Safari\/[\d.]+/)?.[0] ||
    'Unknown'
  const os = ua.includes('Windows')
    ? 'Windows'
    : ua.includes('Macintosh') || ua.includes('Mac OS X')
      ? 'macOS'
      : ua.includes('Linux')
        ? 'Linux'
        : ua.includes('Android')
          ? 'Android'
          : ua.includes('iPhone') || ua.includes('iPad')
            ? 'iOS'
            : 'Unknown'
  return `${browser.split('/')[0]} · ${os}`
}

export default function SessionsView(): ReactElement {
  const { user: currentUser, checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const isAdmin = checkPermission('USR', 'admin')

  const [sessions, setSessions] = useState<Session[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<Filter>('active')
  const [terminating, setTerminating] = useState<number | null>(null)

  const fetchSessions = useCallback(async (): Promise<void> => {
    try {
      const res = isAdmin ? await api.listSessions() : await api.listMySessions()
      setSessions(res.sessions)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať sessions', 'error')
    } finally {
      setLoading(false)
    }
  }, [addToast, isAdmin])

  useEffect(() => {
    void fetchSessions()
    const interval = setInterval(() => void fetchSessions(), REFRESH_INTERVAL_MS)
    return (): void => clearInterval(interval)
  }, [fetchSessions])

  const handleTerminate = useCallback(
    async (session: Session): Promise<void> => {
      const isMyCurrent = session.is_self
      const confirmMsg = isMyCurrent
        ? 'Naozaj sa chcete odhlásiť z tejto session?'
        : `Ukončiť session používateľa ${session.login_name}?`
      if (!window.confirm(confirmMsg)) return

      setTerminating(session.session_id)
      try {
        await api.terminateSession(session.session_id)
        addToast('Session bola ukončená', 'success')
        if (isMyCurrent) {
          // Self-terminated current session — clear local state and reload to re-login.
          await api.logout()
          window.location.reload()
        } else {
          await fetchSessions()
        }
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || 'Ukončenie session zlyhalo', 'error')
      } finally {
        setTerminating(null)
      }
    },
    [addToast, fetchSessions]
  )

  // Filter logic
  const filtered = sessions.filter((s) => {
    if (filter === 'mine') return s.user_id === (currentUser?.id ?? -1)
    if (filter === 'active') {
      return Date.now() - new Date(s.last_seen_at).getTime() <= ACTIVE_THRESHOLD_MS
    }
    return true
  })

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Activity className="h-6 w-6" />
          Aktívne sessions
        </h1>
        <button
          onClick={() => void fetchSessions()}
          disabled={loading}
          className={cn(
            'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
            'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600',
            'disabled:opacity-50'
          )}
          title="Obnoviť"
        >
          <RefreshCw className={cn('h-4 w-4', loading && 'animate-spin')} />
          Obnoviť
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden text-sm w-fit">
        {(
          [
            { key: 'active' as Filter, label: 'Aktívne (30 min)' },
            { key: 'all' as Filter, label: 'Všetky' },
            { key: 'mine' as Filter, label: 'Moje' }
          ] as const
        ).map((f) => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            className={cn(
              'px-3 py-2 transition-colors',
              filter === f.key
                ? 'bg-blue-600 text-white'
                : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600'
            )}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        {loading ? (
          <div className="p-8 flex items-center justify-center text-gray-500">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-8 text-center text-gray-500 dark:text-gray-400">
            Žiadne sessions
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-900/50 text-left">
              <tr>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300">Používateľ</th>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300">IP</th>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300">Zariadenie</th>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300">Prihlásený</th>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300">Posledná aktivita</th>
                <th className="px-4 py-3 font-medium text-gray-700 dark:text-gray-300 text-right">Akcia</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filtered.map((s) => (
                <tr
                  key={s.session_id}
                  className={cn(
                    'transition-colors',
                    s.is_self
                      ? 'bg-blue-50 dark:bg-blue-900/10'
                      : 'hover:bg-gray-50 dark:hover:bg-gray-900/30'
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="text-gray-900 dark:text-white font-medium">{s.login_name}</div>
                    {s.full_name && (
                      <div className="text-xs text-gray-500 dark:text-gray-400">{s.full_name}</div>
                    )}
                    {s.is_self && (
                      <span className="inline-block mt-1 text-xs px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
                        moja session
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-gray-700 dark:text-gray-300 font-mono text-xs">
                    {s.ip_address || '—'}
                  </td>
                  <td className="px-4 py-3 text-gray-700 dark:text-gray-300 text-xs">
                    {parseUserAgent(s.user_agent)}
                  </td>
                  <td className="px-4 py-3 text-gray-700 dark:text-gray-300 text-xs">
                    {formatRelative(s.created_at)}
                  </td>
                  <td className="px-4 py-3 text-gray-700 dark:text-gray-300 text-xs">
                    {formatRelative(s.last_seen_at)}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => void handleTerminate(s)}
                      disabled={terminating === s.session_id}
                      className={cn(
                        'p-1.5 rounded-lg transition-colors',
                        'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20',
                        'disabled:opacity-50 disabled:cursor-not-allowed'
                      )}
                      title="Ukončiť session"
                    >
                      {terminating === s.session_id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <LogOut className="h-4 w-4" />
                      )}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
