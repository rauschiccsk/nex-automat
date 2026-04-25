/**
 * Runtime config loader — fetches public UI settings from backend on boot.
 *
 * Cache is in-memory (per page-load). Initial values match compile-time
 * defaults so getConfigNumber/String() work immediately, before loadConfig()
 * resolves. After loadConfig() succeeds, cache is replaced with server values.
 *
 * Reload requires page refresh (Ctrl+R) to pick up new values — admin who
 * changes a setting in Settings UI must instruct users to reload.
 */

import { SEARCH_DEBOUNCE_MS } from './constants'

interface ConfigCache {
  'ui.search_debounce_ms': number
  'ui.toast_default_duration_ms': number
}

// Compile-time defaults — match nex_config / database seed values.
const DEFAULTS: ConfigCache = {
  'ui.search_debounce_ms': SEARCH_DEBOUNCE_MS,
  'ui.toast_default_duration_ms': 4000
}

let cache: ConfigCache = { ...DEFAULTS }
let loaded = false

/**
 * Fetch public settings and update in-memory cache. Idempotent — safe to
 * call multiple times. On failure, keeps existing cache (compile-time defaults
 * on first failure, last successful values on subsequent failures).
 */
export async function loadConfig(): Promise<void> {
  try {
    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:9110'
    const res = await fetch(`${apiBase}/api/system/settings/public`)
    if (!res.ok) return
    const data = (await res.json()) as Record<string, unknown>
    cache = {
      'ui.search_debounce_ms':
        typeof data['ui.search_debounce_ms'] === 'number'
          ? (data['ui.search_debounce_ms'] as number)
          : DEFAULTS['ui.search_debounce_ms'],
      'ui.toast_default_duration_ms':
        typeof data['ui.toast_default_duration_ms'] === 'number'
          ? (data['ui.toast_default_duration_ms'] as number)
          : DEFAULTS['ui.toast_default_duration_ms']
    }
    loaded = true
  } catch {
    // Network error — keep current cache (defaults on first call).
  }
}

export function getConfigNumber(key: keyof ConfigCache): number {
  return cache[key]
}

export function isConfigLoaded(): boolean {
  return loaded
}
