// MigrationDashboard — main view for MIG module
import { useState, useEffect, useCallback, useMemo, type ReactElement } from 'react'
import {
  Database,
  Loader2,
  AlertCircle,
  RotateCcw,
  CheckCircle2,
  XCircle,
  Clock,
  Lock,
  BarChart3
} from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import CategoryDetail from './CategoryDetail'
import type {
  MigrationCategory,
  MigrationStats,
  CategoriesListResponse
} from '@renderer/types/migration'

// === StatsBar ===

function StatsBar({ stats }: { stats: MigrationStats | null }): ReactElement {
  if (!stats) return <div />

  const items = [
    {
      label: 'Celkom kategorii',
      value: stats.total_categories,
      icon: BarChart3,
      color: 'text-gray-700 dark:text-gray-300'
    },
    {
      label: 'Dokoncene',
      value: stats.completed_categories,
      icon: CheckCircle2,
      color: 'text-green-600 dark:text-green-400'
    },
    {
      label: 'Cakajuce',
      value: stats.pending_categories,
      icon: Clock,
      color: 'text-amber-600 dark:text-amber-400'
    },
    {
      label: 'Neuspesne',
      value: stats.failed_categories,
      icon: XCircle,
      color: 'text-red-600 dark:text-red-400'
    }
  ]

  return (
    <div className="grid grid-cols-4 gap-3">
      {items.map((item) => {
        const Icon = item.icon
        return (
          <div
            key={item.label}
            className="flex items-center gap-3 p-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
          >
            <Icon className={cn('h-5 w-5 shrink-0', item.color)} />
            <div>
              <div className={cn('text-xl font-bold', item.color)}>{item.value}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">{item.label}</div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// === CategoryCard ===

const STATUS_BORDER: Record<string, string> = {
  completed: 'border-green-300 dark:border-green-700',
  failed: 'border-red-300 dark:border-red-700',
  running: 'border-blue-300 dark:border-blue-700',
  pending: 'border-gray-200 dark:border-gray-700'
}

const STATUS_BADGE_CLASS: Record<string, string> = {
  completed: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  failed: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  running: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  pending: 'bg-gray-100 text-gray-600 dark:bg-gray-700/50 dark:text-gray-400'
}

const STATUS_LABELS: Record<string, string> = {
  completed: 'Dokoncene',
  failed: 'Chyba',
  running: 'Prebieha',
  pending: 'Caka'
}

interface CategoryCardProps {
  category: MigrationCategory
  isSelected: boolean
  onClick: () => void
}

function CategoryCard({ category, isSelected, onClick }: CategoryCardProps): ReactElement {
  return (
    <button
      onClick={onClick}
      className={cn(
        'w-full text-left p-3 rounded-lg border-2 transition-all hover:shadow-md',
        STATUS_BORDER[category.status] ?? STATUS_BORDER.pending,
        isSelected && 'ring-2 ring-blue-500 ring-offset-1 dark:ring-offset-gray-900',
        !category.can_run && category.status === 'pending' && 'opacity-70'
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-2">
          <span className="font-mono text-sm font-bold text-gray-900 dark:text-white">
            {category.code}
          </span>
          {!category.can_run && category.status === 'pending' && (
            <Lock className="h-3.5 w-3.5 text-gray-400 dark:text-gray-500" />
          )}
        </div>
        <div className="flex items-center gap-1">
          {category.status === 'completed' && (
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          )}
          {category.status === 'failed' && <XCircle className="h-4 w-4 text-red-500" />}
          <span
            className={cn(
              'text-xs font-medium px-1.5 py-0.5 rounded-full',
              STATUS_BADGE_CLASS[category.status] ?? STATUS_BADGE_CLASS.pending
            )}
          >
            {STATUS_LABELS[category.status] ?? category.status}
          </span>
        </div>
      </div>

      {/* Name & description */}
      <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        {category.name}
      </div>
      <div className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mb-2">
        {category.description}
      </div>

      {/* Tables */}
      <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400 mb-2">
        <span className="font-mono">{category.source_tables.join(', ')}</span>
        <span className="mx-1">&#8594;</span>
        <span className="font-mono">{category.target_tables.join(', ')}</span>
      </div>

      {/* Dependencies */}
      {category.dependency_codes.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {category.dependencies.map((dep) => (
            <span
              key={dep.code}
              className={cn(
                'inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium',
                dep.is_satisfied
                  ? 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400'
                  : 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400'
              )}
            >
              {dep.code}
            </span>
          ))}
        </div>
      )}

      {/* Record count */}
      {category.record_count > 0 && (
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
          {category.record_count.toLocaleString('sk-SK')} zaznamov
        </div>
      )}
    </button>
  )
}

// === DependencyLevel ===

interface DependencyLevelProps {
  level: number
  categories: MigrationCategory[]
  selectedCode: string | null
  onSelect: (code: string) => void
}

function DependencyLevel({
  level,
  categories,
  selectedCode,
  onSelect
}: DependencyLevelProps): ReactElement | null {
  if (categories.length === 0) return null
  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase mb-2">
        Uroven {level}
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {categories.map((cat) => (
          <CategoryCard
            key={cat.code}
            category={cat}
            isSelected={selectedCode === cat.code}
            onClick={() => onSelect(cat.code)}
          />
        ))}
      </div>
    </div>
  )
}

// === MigrationDashboard (main) ===

export default function MigrationDashboard(): ReactElement {
  const { addToast } = useToastStore()

  const [categories, setCategories] = useState<MigrationCategory[]>([])
  const [stats, setStats] = useState<MigrationStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedCode, setSelectedCode] = useState<string | null>(null)

  // === Fetch data ===
  const fetchData = useCallback(async (): Promise<void> => {
    setLoading(true)
    setError(null)
    try {
      const [catRes, statsRes] = await Promise.all([
        api.getMigrationCategories(),
        api.getMigrationStats()
      ])
      setCategories((catRes as CategoriesListResponse).categories)
      setStats(statsRes)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa nacitat migracne data'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [addToast])

  useEffect(() => {
    void fetchData()
  }, [fetchData])

  // Group categories by level
  const levels = useMemo(() => {
    const map = new Map<number, MigrationCategory[]>()
    for (const cat of categories) {
      const arr = map.get(cat.level) ?? []
      arr.push(cat)
      map.set(cat.level, arr)
    }
    return Array.from(map.entries()).sort(([a], [b]) => a - b)
  }, [categories])

  const selectedCategory = useMemo(
    () => categories.find((c) => c.code === selectedCode) ?? null,
    [categories, selectedCode]
  )

  const handleSelect = useCallback(
    (code: string): void => {
      setSelectedCode((prev) => (prev === code ? null : code))
    },
    []
  )

  return (
    <div className="flex flex-col h-full gap-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between shrink-0">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Database className="h-6 w-6" />
          Migracia dat
        </h1>
        <button
          onClick={() => void fetchData()}
          disabled={loading}
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
        >
          <RotateCcw className={cn('h-4 w-4', loading && 'animate-spin')} />
          Obnovit
        </button>
      </div>

      {/* Error */}
      {error && !loading && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 shrink-0">
          <AlertCircle className="h-5 w-5 text-red-500 shrink-0" />
          <span className="text-sm text-red-700 dark:text-red-400 flex-1">{error}</span>
          <button
            onClick={() => void fetchData()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Skusit znova
          </button>
        </div>
      )}

      {/* Loading */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : (
        <div className="flex-1 overflow-auto space-y-6">
          {/* Stats */}
          <StatsBar stats={stats} />

          {/* Levels */}
          {levels.map(([level, cats]) => (
            <DependencyLevel
              key={level}
              level={level}
              categories={cats}
              selectedCode={selectedCode}
              onSelect={handleSelect}
            />
          ))}

          {/* Detail panel */}
          {selectedCategory && (
            <CategoryDetail
              category={selectedCategory}
              onClose={() => setSelectedCode(null)}
              onRefresh={() => void fetchData()}
            />
          )}
        </div>
      )}
    </div>
  )
}
