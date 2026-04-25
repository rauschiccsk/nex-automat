/**
 * Types for migration module (MIG).
 * Matches API schemas from nex-manager-api/migration/schemas.py
 *
 * Field names are EXACTLY as returned by backend (snake_case).
 */

// === Status types ===

export type MigrationStatus = 'pending' | 'completed' | 'failed' | 'running'

// === Category schemas ===

export interface DependencyInfo {
  code: string
  name: string
  status: string // pending, completed, failed
  is_satisfied: boolean
}

export interface MigrationCategory {
  code: string
  name: string
  description: string
  source_tables: string[]
  target_tables: string[]
  dependency_codes: string[]
  dependencies: DependencyInfo[]
  level: number // dependency level (0, 1, 2, 3)

  // Status from DB
  status: MigrationStatus
  record_count: number
  first_migrated_at: string | null
  last_migrated_at: string | null
  last_batch_id: number | null

  // Computed
  can_run: boolean
  blocked_by: string[]
}

export interface CategoriesListResponse {
  categories: MigrationCategory[]
  total: number
  completed: number
  pending: number
  failed: number
}

// === Batch schemas ===

export interface MigrationBatch {
  id: number
  category: string
  status: string
  source_count: number
  target_count: number
  error_count: number
  skipped_count: number
  started_at: string
  completed_at: string | null
  error_log: string | null
  metadata: Record<string, unknown> | null
  duration_seconds: number | null
}

export interface BatchListResponse {
  batches: MigrationBatch[]
  total: number
}

// === Migration run schemas ===

export interface MigrationRunRequest {
  category: string
  dry_run: boolean
}

export interface MigrationRunResponse {
  batch_id: number | null
  category: string
  status: string
  source_count: number
  target_count: number
  error_count: number
  errors: Record<string, unknown>[]
  warnings: Record<string, unknown>[]
  duration_seconds: number
  message: string
}

// === ID Mapping schemas ===

export interface MigrationIdMapping {
  id: string // synthetic: source_table:source_key (for BaseGrid)
  source_table: string
  source_key: string
  target_table: string
  target_id: string
  migrated_at: string
}

export interface IdMappingListResponse {
  items: MigrationIdMapping[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// === Stats schemas ===

export interface MigrationStats {
  total_categories: number
  completed_categories: number
  pending_categories: number
  failed_categories: number
  total_records_migrated: number
  total_batches: number
  last_migration_at: string | null
}
