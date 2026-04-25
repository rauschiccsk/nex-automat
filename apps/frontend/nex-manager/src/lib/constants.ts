/**
 * Shared frontend constants — values used across multiple modules.
 *
 * These start as named constants (Phase 2.1 deduplication). In Phase 2.3
 * (backfill), runtime-tunable values may be replaced with reads from the
 * Settings API (`/api/system/settings`); compile-time defaults stay here as
 * fallbacks when settings are unavailable (boot, offline).
 */

/** Debounce delay (ms) for search inputs across modules. */
export const SEARCH_DEBOUNCE_MS = 300
