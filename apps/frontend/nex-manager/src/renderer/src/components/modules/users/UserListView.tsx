import { useState, useEffect, useCallback, useMemo, type ReactElement } from 'react'
import {
  Search,
  Plus,
  Pencil,
  KeyRound,
  Loader2,
  Users,
  ToggleLeft,
  ToggleRight
} from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { User, UserGroup } from '@renderer/types/users'
import UserFormDialog from './UserFormDialog'
import ChangePasswordDialog from './ChangePasswordDialog'

type ActiveFilter = 'all' | 'active' | 'inactive'

export default function UserListView(): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()

  const canCreate = checkPermission('USR', 'create')
  const canEdit = checkPermission('USR', 'edit')

  // ── Data state ──
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [activeFilter, setActiveFilter] = useState<ActiveFilter>('all')
  const [groupFilter, setGroupFilter] = useState<number | null>(null)

  // ── Dialog state ──
  const [formDialogOpen, setFormDialogOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [passwordDialogOpen, setPasswordDialogOpen] = useState(false)
  const [passwordUser, setPasswordUser] = useState<{ id: number; username: string } | null>(null)

  // ── Debounced search ──
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 300)
    return (): void => clearTimeout(timer)
  }, [searchTerm])

  // ── Extract unique groups from users ──
  const allGroups = useMemo((): UserGroup[] => {
    const map = new Map<number, UserGroup>()
    for (const u of users) {
      for (const g of u.groups) {
        if (!map.has(g.group_id)) map.set(g.group_id, g)
      }
    }
    return Array.from(map.values()).sort((a, b) => a.group_name.localeCompare(b.group_name))
  }, [users])

  // ── Fetch users ──
  const fetchUsers = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const params: { search?: string; is_active?: boolean; group_id?: number } = {}
      if (debouncedSearch) params.search = debouncedSearch
      if (activeFilter === 'active') params.is_active = true
      if (activeFilter === 'inactive') params.is_active = false
      if (groupFilter != null) params.group_id = groupFilter
      const res = await api.getUsers(params)
      setUsers(res.users)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať používateľov', 'error')
    } finally {
      setLoading(false)
    }
  }, [debouncedSearch, activeFilter, groupFilter, addToast])

  useEffect(() => {
    void fetchUsers()
  }, [fetchUsers])

  // ── Handlers ──
  const handleCreate = useCallback((): void => {
    setEditingUser(null)
    setFormDialogOpen(true)
  }, [])

  const handleEdit = useCallback((user: User): void => {
    setEditingUser(user)
    setFormDialogOpen(true)
  }, [])

  const handleChangePassword = useCallback((user: User): void => {
    setPasswordUser({ id: user.user_id, username: user.login_name })
    setPasswordDialogOpen(true)
  }, [])

  const handleToggleActive = useCallback(
    async (user: User): Promise<void> => {
      try {
        await api.updateUser(user.user_id, { is_active: !user.is_active })
        addToast(
          user.is_active
            ? `Používateľ ${user.login_name} bol deaktivovaný`
            : `Používateľ ${user.login_name} bol aktivovaný`,
          'success'
        )
        void fetchUsers()
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || 'Zmena stavu zlyhala', 'error')
      }
    },
    [addToast, fetchUsers]
  )

  const handleFormClose = useCallback(
    (saved: boolean): void => {
      setFormDialogOpen(false)
      setEditingUser(null)
      if (saved) void fetchUsers()
    },
    [fetchUsers]
  )

  const handlePasswordClose = useCallback((): void => {
    setPasswordDialogOpen(false)
    setPasswordUser(null)
  }, [])

  // ── Format helpers ──
  const formatDate = (iso: string | null): string => {
    if (!iso) return 'Nikdy'
    try {
      return new Intl.DateTimeFormat('sk-SK', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(iso))
    } catch {
      return iso
    }
  }

  return (
    <div className="flex flex-col gap-4">
      {/* ── Header row ── */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Users className="h-6 w-6" />
          Používatelia
        </h1>
        {canCreate && (
          <button
            onClick={handleCreate}
            className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              'bg-blue-600 text-white hover:bg-blue-700'
            )}
          >
            <Plus className="h-4 w-4" />
            Nový používateľ
          </button>
        )}
      </div>

      {/* ── Filter row ── */}
      <div className="flex flex-wrap items-center gap-3">
        {/* Search */}
        <div className="relative flex-1 min-w-[200px] max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Hľadať meno, login, email…"
            className={cn(
              'w-full pl-10 pr-4 py-2 rounded-lg border text-sm transition-colors outline-none',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'border-gray-300 dark:border-gray-600',
              'placeholder-gray-400 dark:placeholder-gray-500',
              'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
            )}
          />
        </div>

        {/* Group filter */}
        <select
          value={groupFilter ?? ''}
          onChange={(e) => setGroupFilter(e.target.value ? Number(e.target.value) : null)}
          className={cn(
            'px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
            'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
            'border-gray-300 dark:border-gray-600',
            'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
          )}
        >
          <option value="">Všetky skupiny</option>
          {allGroups.map((g) => (
            <option key={g.group_id} value={g.group_id}>
              {g.group_name}
            </option>
          ))}
        </select>

        {/* Active/Inactive toggle */}
        <div className="flex rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden text-sm">
          {(['all', 'active', 'inactive'] as ActiveFilter[]).map((f) => (
            <button
              key={f}
              onClick={() => setActiveFilter(f)}
              className={cn(
                'px-3 py-2 transition-colors',
                activeFilter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600'
              )}
            >
              {f === 'all' ? 'Všetci' : f === 'active' ? 'Aktívni' : 'Neaktívni'}
            </button>
          ))}
        </div>
      </div>

      {/* ── Table ── */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : users.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <Users className="h-12 w-12 text-gray-300 dark:text-gray-600 mb-3" />
          <p className="text-gray-500 dark:text-gray-400">Žiadni používatelia</p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Username
                </th>
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Meno
                </th>
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Email
                </th>
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Skupiny
                </th>
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Aktívny
                </th>
                <th className="px-4 py-3 text-left font-medium text-gray-600 dark:text-gray-400">
                  Posledné prihlásenie
                </th>
                {canEdit && (
                  <th className="px-4 py-3 text-right font-medium text-gray-600 dark:text-gray-400">
                    Akcie
                  </th>
                )}
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr
                  key={user.user_id}
                  className="border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                    {user.login_name}
                  </td>
                  <td className="px-4 py-3 text-gray-700 dark:text-gray-300">{user.full_name}</td>
                  <td className="px-4 py-3 text-gray-500 dark:text-gray-400">
                    {user.email || '—'}
                  </td>
                  <td className="px-4 py-3 text-gray-500 dark:text-gray-400">
                    {user.groups.length > 0
                      ? user.groups.map((g) => g.group_name).join(', ')
                      : '—'}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={cn(
                        'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                        user.is_active
                          ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                          : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                      )}
                    >
                      {user.is_active ? 'Aktívny' : 'Neaktívny'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 dark:text-gray-400">
                    {formatDate(user.last_login_at)}
                  </td>
                  {canEdit && (
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-end gap-1">
                        <button
                          onClick={() => handleEdit(user)}
                          className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                          title="Upraviť"
                        >
                          <Pencil className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleChangePassword(user)}
                          className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                          title="Zmeniť heslo"
                        >
                          <KeyRound className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => void handleToggleActive(user)}
                          className={cn(
                            'p-1.5 rounded-lg transition-colors',
                            user.is_active
                              ? 'text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20'
                              : 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20'
                          )}
                          title={user.is_active ? 'Deaktivovať' : 'Aktivovať'}
                        >
                          {user.is_active ? (
                            <ToggleRight className="h-4 w-4" />
                          ) : (
                            <ToggleLeft className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Dialogs ── */}
      {formDialogOpen && (
        <UserFormDialog user={editingUser} onClose={handleFormClose} />
      )}

      {passwordDialogOpen && passwordUser && (
        <ChangePasswordDialog
          userId={passwordUser.id}
          username={passwordUser.username}
          onClose={handlePasswordClose}
        />
      )}
    </div>
  )
}
