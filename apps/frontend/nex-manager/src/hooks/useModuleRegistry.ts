/**
 * Hook for fetching YAML-based module registry from /api/system/modules.
 *
 * This provides the category definitions and full module list from the
 * YAML registry (single source of truth). It complements the existing
 * moduleStore which loads modules from the database (with RBAC filtering).
 *
 * Usage:
 *   const { categories, registryModules, loading } = useModuleRegistry()
 */

import { useEffect, useRef, useState } from 'react'
import { api } from '@renderer/lib/api'

export interface RegistryCategory {
  key: string
  name: string
  order: number
}

export interface RegistryModule {
  key: string
  name: string
  category: string
  icon: string
  order: number
  status: 'active' | 'planned'
  backend_router: string
  frontend_module: string
  roles: string[]
}

export interface ModuleRegistryResponse {
  version: string
  categories: RegistryCategory[]
  modules: RegistryModule[]
  total: number
}

// Module-level cache so we don't refetch on every component mount
let _cache: ModuleRegistryResponse | null = null
let _cachePromise: Promise<ModuleRegistryResponse> | null = null

async function fetchRegistry(): Promise<ModuleRegistryResponse> {
  if (_cache) return _cache
  if (_cachePromise) return _cachePromise

  _cachePromise = api
    .getSystemModules()
    .then((data) => {
      _cache = data
      _cachePromise = null
      return data
    })
    .catch((err) => {
      _cachePromise = null
      throw err
    })

  return _cachePromise
}

export function useModuleRegistry(): {
  categories: RegistryCategory[]
  registryModules: RegistryModule[]
  activeModules: RegistryModule[]
  loading: boolean
  error: string | null
} {
  const [data, setData] = useState<ModuleRegistryResponse | null>(_cache)
  const [loading, setLoading] = useState(!_cache)
  const [error, setError] = useState<string | null>(null)
  const fetched = useRef(false)

  useEffect(() => {
    if (fetched.current || _cache) {
      if (_cache && !data) setData(_cache)
      return
    }
    fetched.current = true

    fetchRegistry()
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.warn('[REGISTRY] Failed to fetch module registry:', err)
        setError(err?.message || 'Failed to load registry')
        setLoading(false)
      })
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const categories = data?.categories ?? []
  const registryModules = data?.modules ?? []
  const activeModules = registryModules.filter((m) => m.status === 'active')

  return { categories, registryModules, activeModules, loading, error }
}
