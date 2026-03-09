import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Building2, Loader2, AlertCircle, RotateCcw } from 'lucide-react'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import type { EshopTenant } from '@renderer/types/eshop'

export default function EshopTenantList(): ReactElement {
  const { addToast } = useToastStore()

  const [tenants, setTenants] = useState<EshopTenant[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchTenants = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.getEshopTenants()
      setTenants(res.tenants)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať tenantov'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [addToast])

  useEffect(() => {
    void fetchTenants()
  }, [fetchTenants])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-3 text-gray-500 dark:text-gray-400">Načítavam...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-4">
        <AlertCircle className="h-8 w-8 text-red-500" />
        <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
        <button
          onClick={() => void fetchTenants()}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          Skúsiť znova
        </button>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-3">
      <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
        <Building2 className="h-6 w-6" />
        Tenanty
      </h1>

      <div className="text-xs text-gray-500 dark:text-gray-400">
        Celkom: {tenants.length} tenantov (iba na čítanie)
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
        <table data-testid="tenant-table" className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
              <th className="px-4 py-2.5 text-left text-gray-500 dark:text-gray-400 font-medium">Spoločnosť</th>
              <th className="px-4 py-2.5 text-left text-gray-500 dark:text-gray-400 font-medium">Doména</th>
              <th className="px-4 py-2.5 text-left text-gray-500 dark:text-gray-400 font-medium">Značka</th>
              <th className="px-4 py-2.5 text-left text-gray-500 dark:text-gray-400 font-medium">Mena</th>
              <th className="px-4 py-2.5 text-center text-gray-500 dark:text-gray-400 font-medium">Aktívny</th>
            </tr>
          </thead>
          <tbody>
            {tenants.map((t) => (
              <tr
                key={t.tenant_id}
                className="border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/30"
              >
                <td className="px-4 py-2.5 text-gray-900 dark:text-white font-medium">{t.company_name}</td>
                <td className="px-4 py-2.5 text-gray-700 dark:text-gray-300">{t.domain}</td>
                <td className="px-4 py-2.5 text-gray-700 dark:text-gray-300">{t.brand_name}</td>
                <td className="px-4 py-2.5 text-gray-700 dark:text-gray-300">{t.currency}</td>
                <td className="px-4 py-2.5 text-center">
                  {t.is_active ? (
                    <span className="text-green-600 dark:text-green-400">✓</span>
                  ) : (
                    <span className="text-red-500">✗</span>
                  )}
                </td>
              </tr>
            ))}
            {tenants.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-400 dark:text-gray-500">
                  Žiadni tenanty
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
