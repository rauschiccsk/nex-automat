// CategoryDetail — detail panel with tabs (Info, Batches, Mappings, Run)
import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { X, Info, List, Link2, Play, Loader2, AlertCircle, RotateCcw } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import { useAuthStore } from '@renderer/stores/authStore'
import { BaseGrid } from '@renderer/components/grids'
import { migrationBatchesGridConfig, migrationMappingsGridConfig } from './migrationGridConfigs'
import RunWizard from './RunWizard'
import type {
  MigrationCategory,
  MigrationBatch,
  MigrationIdMapping,
  BatchListResponse,
  IdMappingListResponse
} from '@renderer/types/migration'

interface CategoryDetailProps {
  category: MigrationCategory
  onClose: () => void
  onRefresh: () => void
}

type TabId = 'info' | 'batches' | 'mappings' | 'run'

const TABS: { id: TabId; label: string; icon: typeof Info }[] = [
  { id: 'info', label: 'Info', icon: Info },
  { id: 'batches', label: 'Batche', icon: List },
  { id: 'mappings', label: 'ID Mapovania', icon: Link2 },
  { id: 'run', label: 'Spustit', icon: Play }
]

export default function CategoryDetail({
  category,
  onClose,
  onRefresh
}: CategoryDetailProps): ReactElement {
  const [activeTab, setActiveTab] = useState<TabId>('info')
  const { addToast } = useToastStore()
  const { checkPermission } = useAuthStore()

  const canRun = checkPermission('MIG', 'create')
  const canReset = checkPermission('MIG', 'delete')

  // === Batches state ===
  const [batches, setBatches] = useState<MigrationBatch[]>([])
  const [batchesLoading, setBatchesLoading] = useState(false)
  const [batchesError, setBatchesError] = useState<string | null>(null)

  // === Mappings state (server-side pagination) ===
  const [mappings, setMappings] = useState<MigrationIdMapping[]>([])
  const [mappingsTotal, setMappingsTotal] = useState(0)
  const [mappingsPage, setMappingsPage] = useState(1)
  const [mappingsPageSize, setMappingsPageSize] = useState(50)
  const [mappingsLoading, setMappingsLoading] = useState(false)
  const [mappingsError, setMappingsError] = useState<string | null>(null)

  // === Fetch batches ===
  const fetchBatches = useCallback(async (): Promise<void> => {
    setBatchesLoading(true)
    setBatchesError(null)
    try {
      const res: BatchListResponse = await api.getMigrationBatches(category.code)
      setBatches(res.batches)
    } catch (err) {
      const e = err as ApiError
      setBatchesError(e.message || 'Chyba pri nacitani batchov')
    } finally {
      setBatchesLoading(false)
    }
  }, [category.code])

  // === Fetch mappings ===
  const fetchMappings = useCallback(async (): Promise<void> => {
    setMappingsLoading(true)
    setMappingsError(null)
    try {
      const res: IdMappingListResponse = await api.getMigrationMappings(
        category.code,
        mappingsPage,
        mappingsPageSize
      )
      // Add synthetic id for BaseGrid compatibility
      const items = res.items.map((item, idx) => ({
        ...item,
        id: `${item.source_table}:${item.source_key}:${idx}`
      }))
      setMappings(items)
      setMappingsTotal(res.total)
    } catch (err) {
      const e = err as ApiError
      setMappingsError(e.message || 'Chyba pri nacitani mapovani')
    } finally {
      setMappingsLoading(false)
    }
  }, [category.code, mappingsPage, mappingsPageSize])

  // Load data on tab change
  useEffect(() => {
    if (activeTab === 'batches') void fetchBatches()
    if (activeTab === 'mappings') void fetchMappings()
  }, [activeTab, fetchBatches, fetchMappings])

  // === Reset handler ===
  const handleReset = useCallback(async (): Promise<void> => {
    if (!confirm(`Naozaj chcete resetovat kategoriu ${category.code} na "pending"?`)) return
    try {
      await api.resetMigrationCategory(category.code)
      addToast(`Kategoria ${category.code} bola resetovana`, 'success')
      onRefresh()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Chyba pri resete', 'error')
    }
  }, [category.code, addToast, onRefresh])

  const renderInfo = (): ReactElement => (
    <div className="space-y-4 p-4">
      <dl className="space-y-3">
        <div>
          <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">Popis</dt>
          <dd className="text-sm text-gray-900 dark:text-white mt-1">{category.description}</dd>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
              Zdrojove tabulky
            </dt>
            <dd className="mt-1 flex flex-wrap gap-1">
              {category.source_tables.map((t) => (
                <span
                  key={t}
                  className="font-mono text-xs px-1.5 py-0.5 bg-blue-50 dark:bg-blue-900/20 rounded text-blue-700 dark:text-blue-400"
                >
                  {t}
                </span>
              ))}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
              Cielove tabulky
            </dt>
            <dd className="mt-1 flex flex-wrap gap-1">
              {category.target_tables.map((t) => (
                <span
                  key={t}
                  className="font-mono text-xs px-1.5 py-0.5 bg-green-50 dark:bg-green-900/20 rounded text-green-700 dark:text-green-400"
                >
                  {t}
                </span>
              ))}
            </dd>
          </div>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
            Zavislosti
          </dt>
          <dd className="mt-1 flex flex-wrap gap-1">
            {category.dependency_codes.length === 0 ? (
              <span className="text-sm text-gray-400 dark:text-gray-500">Ziadne</span>
            ) : (
              category.dependencies.map((dep) => (
                <span
                  key={dep.code}
                  className={cn(
                    'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium',
                    dep.is_satisfied
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                      : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                  )}
                >
                  {dep.code}
                </span>
              ))
            )}
          </dd>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
              Zaznamy
            </dt>
            <dd className="text-lg font-semibold text-gray-900 dark:text-white">
              {category.record_count.toLocaleString('sk-SK')}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
              Posledna migracia
            </dt>
            <dd className="text-sm text-gray-900 dark:text-white">
              {category.last_migrated_at
                ? new Date(category.last_migrated_at).toLocaleString('sk-SK')
                : '-'}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400">
              Uroven
            </dt>
            <dd className="text-lg font-semibold text-gray-900 dark:text-white">{category.level}</dd>
          </div>
        </div>
      </dl>

      {canReset && category.status !== 'pending' && (
        <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={() => { void handleReset() }}
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/10 transition-colors"
          >
            <RotateCcw className="h-4 w-4" />
            Resetovat na pending
          </button>
        </div>
      )}
    </div>
  )

  const renderBatches = (): ReactElement => (
    <div className="flex flex-col h-full p-2">
      {batchesLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-blue-500" />
        </div>
      ) : batchesError ? (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-sm text-red-700 dark:text-red-400">
          <AlertCircle className="h-4 w-4 shrink-0" />
          {batchesError}
        </div>
      ) : (
        <BaseGrid
          data={batches}
          config={migrationBatchesGridConfig}
          className="flex-1 min-h-0"
        />
      )}
    </div>
  )

  const renderMappings = (): ReactElement => (
    <div className="flex flex-col h-full p-2">
      {mappingsLoading && mappings.length === 0 ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-blue-500" />
        </div>
      ) : mappingsError ? (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-sm text-red-700 dark:text-red-400">
          <AlertCircle className="h-4 w-4 shrink-0" />
          {mappingsError}
        </div>
      ) : (
        <BaseGrid
          data={mappings}
          config={migrationMappingsGridConfig}
          className="flex-1 min-h-0"
          serverSide
          totalRows={mappingsTotal}
          currentPage={mappingsPage}
          pageSize={mappingsPageSize}
          onPageChange={(page) => setMappingsPage(page)}
          onPageSizeChange={(size) => {
            setMappingsPageSize(size)
            setMappingsPage(1)
          }}
        />
      )}
    </div>
  )

  const renderRun = (): ReactElement => (
    <div className="p-4">
      {canRun ? (
        <RunWizard
          category={category}
          onClose={onClose}
          onCompleted={onRefresh}
        />
      ) : (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/10 border border-amber-200 dark:border-amber-800">
          <AlertCircle className="h-5 w-5 text-amber-500 shrink-0" />
          <span className="text-sm text-amber-700 dark:text-amber-400">
            Nemate opravnenie spustit migraciu.
          </span>
        </div>
      )}
    </div>
  )

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900 shadow-lg overflow-hidden flex flex-col max-h-[600px]">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shrink-0">
        <div className="flex items-center gap-3">
          <span className="font-mono text-base font-bold text-gray-900 dark:text-white">
            {category.code}
          </span>
          <span className="text-sm text-gray-600 dark:text-gray-400">{category.name}</span>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 shrink-0">
        {TABS.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={cn(
                'flex items-center gap-1.5 px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px',
                activeTab === tab.id
                  ? 'border-blue-600 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              )}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto min-h-0">
        {activeTab === 'info' && renderInfo()}
        {activeTab === 'batches' && renderBatches()}
        {activeTab === 'mappings' && renderMappings()}
        {activeTab === 'run' && renderRun()}
      </div>
    </div>
  )
}
