/**
 * Centralized API client with JWT auth, auto-refresh, and error handling.
 */

let API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9110'

/**
 * Initializes API_BASE_URL from Electron runtime config (resources/config.json).
 * Must be called before any API requests. Falls back to VITE_API_URL or localhost.
 */
export async function initApiConfig(): Promise<void> {
  try {
    if (window.api?.config?.getConfig) {
      const cfg = await window.api.config.getConfig()
      if (cfg?.apiUrl) {
        API_BASE_URL = cfg.apiUrl
      }
    }
  } catch {
    // Fallback — keep existing value (VITE_API_URL or localhost)
  }
}

// ─── Response types ───────────────────────────────────────────────

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface MeResponse {
  user_id: string
  username: string
  email: string
  full_name: string
  groups: string[]
  permissions: Record<string, string[]>
}

export interface ApiModule {
  module_code: string
  module_name: string
  category: string
  icon: string
  module_type: string
  is_mock: boolean
  sort_order: number
}

export interface ModuleCategory {
  category: string
  modules: ApiModule[]
}

export interface ApiError {
  status: number
  message: string
  detail?: string
}

// ─── Client ───────────────────────────────────────────────────────

class ApiClient {
  private accessToken: string | null = null
  private refreshToken: string | null = null
  private refreshPromise: Promise<void> | null = null

  // ── Token management ──

  setTokens(access: string, refresh: string): void {
    this.accessToken = access
    this.refreshToken = refresh
  }

  clearTokens(): void {
    this.accessToken = null
    this.refreshToken = null
    this.refreshPromise = null
  }

  getAccessToken(): string | null {
    return this.accessToken
  }

  // ── Core fetch ──

  private async request<T>(
    path: string,
    options: RequestInit = {},
    skipAuth = false
  ): Promise<T> {
    const url = `${API_BASE_URL}${path}`
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>)
    }

    if (!skipAuth && this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }

    const response = await fetch(url, {
      ...options,
      headers
    })

    // Token expired — try refresh once
    if (response.status === 401 && !skipAuth && this.refreshToken) {
      await this.doRefresh()
      // Retry with new token
      headers['Authorization'] = `Bearer ${this.accessToken}`
      const retry = await fetch(url, { ...options, headers })
      if (!retry.ok) {
        throw await this.buildError(retry)
      }
      return retry.json() as Promise<T>
    }

    if (!response.ok) {
      throw await this.buildError(response)
    }

    return response.json() as Promise<T>
  }

  private async doRefresh(): Promise<void> {
    // Deduplicate concurrent refresh calls
    if (this.refreshPromise) {
      return this.refreshPromise
    }

    this.refreshPromise = (async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: this.refreshToken })
        })

        if (!res.ok) {
          this.clearTokens()
          throw await this.buildError(res)
        }

        const data = (await res.json()) as LoginResponse
        this.accessToken = data.access_token
        this.refreshToken = data.refresh_token
      } finally {
        this.refreshPromise = null
      }
    })()

    return this.refreshPromise
  }

  private async buildError(response: Response): Promise<ApiError> {
    let message = `HTTP ${response.status}`
    let detail: string | undefined
    try {
      const body = await response.json()
      message = body.message || body.detail || message
      detail = body.detail
    } catch {
      // ignore parse errors
    }
    return { status: response.status, message, detail }
  }

  // ── Auth endpoints ──

  async login(username: string, password: string): Promise<LoginResponse> {
    const data = await this.request<LoginResponse>(
      '/api/auth/login',
      {
        method: 'POST',
        body: JSON.stringify({ username, password })
      },
      true // skipAuth — no token yet
    )
    this.setTokens(data.access_token, data.refresh_token)
    return data
  }

  async getMe(): Promise<MeResponse> {
    return this.request<MeResponse>('/api/auth/me')
  }

  // ── Module endpoints ──

  async getModulesByCategory(): Promise<ModuleCategory[]> {
    return this.request<ModuleCategory[]>('/api/modules/by-category')
  }
}

// Singleton export
export const api = new ApiClient()
