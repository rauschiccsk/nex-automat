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

export interface MeUser {
  user_id: number
  login_name: string
  full_name: string
  email: string
  is_active: boolean
  last_login_at: string | null
  groups: string[]
}

export interface MePermission {
  module_code: string
  module_name: string
  can_view: boolean
  can_create: boolean
  can_edit: boolean
  can_delete: boolean
  can_print: boolean
  can_export: boolean
  can_admin: boolean
}

export interface MeResponse {
  user: MeUser
  permissions: MePermission[]
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

export interface ModulesByCategoryResponse {
  categories: ModuleCategory[]
  total: number
}

export interface SystemCategory {
  key: string
  name: string
  order: number
}

export interface SystemModule {
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

export interface SystemModulesResponse {
  version: string
  categories: SystemCategory[]
  modules: SystemModule[]
  total: number
}

export interface ApiError {
  status: number
  message: string
  detail?: string
}

export interface MessageResponse {
  message: string
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

  async changeSelfPassword(currentPassword: string, newPassword: string): Promise<MessageResponse> {
    return this.request<MessageResponse>('/api/auth/change-password', {
      method: 'PUT',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    })
  }

  // ── Module endpoints ──

  async getModulesByCategory(): Promise<ModuleCategory[]> {
    const data = await this.request<ModulesByCategoryResponse>('/api/modules/by-category')
    return data.categories
  }

  // ── System endpoints (YAML registry — no auth required) ──

  async getSystemModules(status?: 'active' | 'planned'): Promise<SystemModulesResponse> {
    const query = new URLSearchParams()
    if (status) query.set('status', status)
    const qs = query.toString()
    return this.request<SystemModulesResponse>(
      `/api/system/modules${qs ? '?' + qs : ''}`,
      {},
      true // skipAuth — public endpoint
    )
  }

  // ── User endpoints ──

  async getUsers(params?: {
    group_id?: number
    is_active?: boolean
    search?: string
  }): Promise<import('@renderer/types/users').UserListResponse> {
    const query = new URLSearchParams()
    if (params?.group_id != null) query.set('group_id', String(params.group_id))
    if (params?.is_active != null) query.set('is_active', String(params.is_active))
    if (params?.search) query.set('search', params.search)
    const qs = query.toString()
    return this.request(`/api/users${qs ? '?' + qs : ''}`)
  }

  async getUser(id: number): Promise<import('@renderer/types/users').User> {
    return this.request(`/api/users/${id}`)
  }

  async createUser(
    data: import('@renderer/types/users').CreateUserPayload
  ): Promise<import('@renderer/types/users').User> {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updateUser(
    id: number,
    data: import('@renderer/types/users').UpdateUserPayload
  ): Promise<import('@renderer/types/users').User> {
    return this.request(`/api/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async changeUserPassword(id: number, newPassword: string): Promise<MessageResponse> {
    return this.request(`/api/users/${id}/password`, {
      method: 'PUT',
      body: JSON.stringify({ new_password: newPassword })
    })
  }

  // ── Partner endpoints ──

  async getPartners(
    params?: import('@renderer/types/partner').PartnerListParams
  ): Promise<import('@renderer/types/partner').PartnerListResponse> {
    const query = new URLSearchParams()
    if (params?.partner_type) query.set('partner_type', params.partner_type)
    if (params?.is_active != null) query.set('is_active', String(params.is_active))
    if (params?.search) query.set('search', params.search)
    if (params?.page != null) query.set('page', String(params.page))
    if (params?.page_size != null) query.set('page_size', String(params.page_size))
    if (params?.sort_by) query.set('sort_by', params.sort_by)
    if (params?.sort_order) query.set('sort_order', params.sort_order)
    const qs = query.toString()
    return this.request(`/api/partners${qs ? '?' + qs : ''}`)
  }

  async getPartner(id: string): Promise<import('@renderer/types/partner').Partner> {
    return this.request(`/api/partners/${id}`)
  }

  async createPartner(
    data: import('@renderer/types/partner').PartnerCreate
  ): Promise<import('@renderer/types/partner').Partner> {
    return this.request('/api/partners', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePartner(
    id: string,
    data: import('@renderer/types/partner').PartnerUpdate
  ): Promise<import('@renderer/types/partner').Partner> {
    return this.request(`/api/partners/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  // ── PAB (Partner Catalog) endpoints ──

  async getPabPartners(
    params?: import('@renderer/types/pab').PartnerListParams
  ): Promise<import('@renderer/types/pab').PartnerCatalogListResponse> {
    const query = new URLSearchParams()
    if (params?.search) query.set('search', params.search)
    if (params?.partner_class) query.set('partner_class', params.partner_class)
    if (params?.is_active != null) query.set('is_active', String(params.is_active))
    if (params?.is_supplier != null) query.set('is_supplier', String(params.is_supplier))
    if (params?.is_customer != null) query.set('is_customer', String(params.is_customer))
    if (params?.limit != null) query.set('limit', String(params.limit))
    if (params?.offset != null) query.set('offset', String(params.offset))
    if (params?.sort_by) query.set('sort_by', params.sort_by)
    if (params?.sort_order) query.set('sort_order', params.sort_order)
    const qs = query.toString()
    return this.request(`/api/pab/partners${qs ? '?' + qs : ''}`)
  }

  async getPabPartner(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerCatalog> {
    return this.request(`/api/pab/partners/${partnerId}`)
  }

  async createPabPartner(
    data: import('@renderer/types/pab').PartnerCatalogCreate
  ): Promise<import('@renderer/types/pab').PartnerCatalog> {
    return this.request('/api/pab/partners', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePabPartner(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerCatalogUpdate
  ): Promise<import('@renderer/types/pab').PartnerCatalog> {
    return this.request(`/api/pab/partners/${partnerId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deletePabPartner(partnerId: number): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}`, { method: 'DELETE' })
  }

  // Extensions (1:1)
  async getPabExtensions(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerExtensions> {
    return this.request(`/api/pab/partners/${partnerId}/extensions`)
  }

  async upsertPabExtensions(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerExtensionsUpsert
  ): Promise<import('@renderer/types/pab').PartnerExtensions> {
    return this.request(`/api/pab/partners/${partnerId}/extensions`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  // Addresses
  async getPabAddresses(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerAddress[]> {
    return this.request(`/api/pab/partners/${partnerId}/addresses`)
  }

  async createPabAddress(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerAddressCreate
  ): Promise<import('@renderer/types/pab').PartnerAddress> {
    return this.request(`/api/pab/partners/${partnerId}/addresses`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePabAddress(
    partnerId: number,
    addressType: string,
    data: import('@renderer/types/pab').PartnerAddressUpdate
  ): Promise<import('@renderer/types/pab').PartnerAddress> {
    return this.request(`/api/pab/partners/${partnerId}/addresses/${addressType}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deletePabAddress(partnerId: number, addressType: string): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}/addresses/${addressType}`, {
      method: 'DELETE'
    })
  }

  // Contacts
  async getPabContacts(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerContact[]> {
    return this.request(`/api/pab/partners/${partnerId}/contacts`)
  }

  async createPabContact(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerContactCreate
  ): Promise<import('@renderer/types/pab').PartnerContact> {
    return this.request(`/api/pab/partners/${partnerId}/contacts`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePabContact(
    partnerId: number,
    contactId: number,
    data: import('@renderer/types/pab').PartnerContactUpdate
  ): Promise<import('@renderer/types/pab').PartnerContact> {
    return this.request(`/api/pab/partners/${partnerId}/contacts/${contactId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deletePabContact(partnerId: number, contactId: number): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}/contacts/${contactId}`, {
      method: 'DELETE'
    })
  }

  // Bank Accounts
  async getPabBankAccounts(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerBankAccount[]> {
    return this.request(`/api/pab/partners/${partnerId}/bank-accounts`)
  }

  async createPabBankAccount(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerBankAccountCreate
  ): Promise<import('@renderer/types/pab').PartnerBankAccount> {
    return this.request(`/api/pab/partners/${partnerId}/bank-accounts`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePabBankAccount(
    partnerId: number,
    accountId: number,
    data: import('@renderer/types/pab').PartnerBankAccountUpdate
  ): Promise<import('@renderer/types/pab').PartnerBankAccount> {
    return this.request(`/api/pab/partners/${partnerId}/bank-accounts/${accountId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deletePabBankAccount(partnerId: number, accountId: number): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}/bank-accounts/${accountId}`, {
      method: 'DELETE'
    })
  }

  // Categories
  async getPabCategories(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerCategoryMapping[]> {
    return this.request(`/api/pab/partners/${partnerId}/categories`)
  }

  async assignPabCategory(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerCategoryAssign
  ): Promise<import('@renderer/types/pab').PartnerCategoryMapping> {
    return this.request(`/api/pab/partners/${partnerId}/categories`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async unassignPabCategory(partnerId: number, categoryId: number): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}/categories/${categoryId}`, {
      method: 'DELETE'
    })
  }

  // Texts
  async getPabTexts(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerText[]> {
    return this.request(`/api/pab/partners/${partnerId}/texts`)
  }

  async upsertPabTexts(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerTextUpsert
  ): Promise<import('@renderer/types/pab').PartnerText> {
    return this.request(`/api/pab/partners/${partnerId}/texts`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  // Facilities
  async getPabFacilities(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerFacility[]> {
    return this.request(`/api/pab/partners/${partnerId}/facilities`)
  }

  async createPabFacility(
    partnerId: number,
    data: import('@renderer/types/pab').PartnerFacilityCreate
  ): Promise<import('@renderer/types/pab').PartnerFacility> {
    return this.request(`/api/pab/partners/${partnerId}/facilities`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updatePabFacility(
    partnerId: number,
    facilityId: number,
    data: import('@renderer/types/pab').PartnerFacilityUpdate
  ): Promise<import('@renderer/types/pab').PartnerFacility> {
    return this.request(`/api/pab/partners/${partnerId}/facilities/${facilityId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async deletePabFacility(partnerId: number, facilityId: number): Promise<MessageResponse> {
    return this.request(`/api/pab/partners/${partnerId}/facilities/${facilityId}`, {
      method: 'DELETE'
    })
  }

  // History
  async getPabHistory(
    partnerId: number
  ): Promise<import('@renderer/types/pab').PartnerHistory[]> {
    return this.request(`/api/pab/partners/${partnerId}/history`)
  }

  async getPabHistoryVersion(
    partnerId: number,
    modifyId: number
  ): Promise<import('@renderer/types/pab').PartnerHistory> {
    return this.request(`/api/pab/partners/${partnerId}/history/${modifyId}`)
  }

  // ── Migration endpoints ──

  async getMigrationCategories(): Promise<
    import('@renderer/types/migration').CategoriesListResponse
  > {
    return this.request('/api/migration/categories')
  }

  async getMigrationCategory(
    code: string
  ): Promise<import('@renderer/types/migration').MigrationCategory> {
    return this.request(`/api/migration/categories/${code}`)
  }

  async getMigrationBatches(
    code: string
  ): Promise<import('@renderer/types/migration').BatchListResponse> {
    return this.request(`/api/migration/categories/${code}/batches`)
  }

  async runMigration(
    data: import('@renderer/types/migration').MigrationRunRequest
  ): Promise<import('@renderer/types/migration').MigrationRunResponse> {
    return this.request('/api/migration/run', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async getMigrationStats(): Promise<import('@renderer/types/migration').MigrationStats> {
    return this.request('/api/migration/stats')
  }

  async getMigrationMappings(
    category: string,
    page = 1,
    pageSize = 50,
    search?: string
  ): Promise<import('@renderer/types/migration').IdMappingListResponse> {
    const query = new URLSearchParams()
    query.set('page', String(page))
    query.set('page_size', String(pageSize))
    if (search) query.set('search', search)
    return this.request(`/api/migration/mappings/${category}?${query.toString()}`)
  }

  async resetMigrationCategory(code: string): Promise<MessageResponse> {
    return this.request(`/api/migration/categories/${code}/reset`, {
      method: 'POST'
    })
  }

  // ── ESHOP Admin endpoints ──

  async getEshopOrders(params?: {
    page?: number
    page_size?: number
    status?: string
    tenant_id?: number
  }): Promise<import('@renderer/types/eshop').EshopOrderListResponse> {
    const query = new URLSearchParams()
    if (params?.page != null) query.set('page', String(params.page))
    if (params?.page_size != null) query.set('page_size', String(params.page_size))
    if (params?.status) query.set('status', params.status)
    if (params?.tenant_id != null) query.set('tenant_id', String(params.tenant_id))
    const qs = query.toString()
    return this.request(`/api/eshop/admin/orders${qs ? '?' + qs : ''}`)
  }

  async getEshopOrderDetail(
    orderId: number
  ): Promise<import('@renderer/types/eshop').EshopOrderDetail> {
    return this.request(`/api/eshop/admin/orders/${orderId}`)
  }

  async updateEshopOrder(
    orderId: number,
    data: import('@renderer/types/eshop').EshopOrderUpdateRequest
  ): Promise<MessageResponse> {
    return this.request(`/api/eshop/admin/orders/${orderId}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    })
  }

  async getEshopProducts(params?: {
    page?: number
    page_size?: number
    tenant_id?: number
    include_inactive?: boolean
  }): Promise<import('@renderer/types/eshop').EshopProductListResponse> {
    const query = new URLSearchParams()
    if (params?.page != null) query.set('page', String(params.page))
    if (params?.page_size != null) query.set('page_size', String(params.page_size))
    if (params?.tenant_id != null) query.set('tenant_id', String(params.tenant_id))
    if (params?.include_inactive != null) query.set('include_inactive', String(params.include_inactive))
    const qs = query.toString()
    return this.request(`/api/eshop/admin/products${qs ? '?' + qs : ''}`)
  }

  async getEshopProduct(
    productId: number
  ): Promise<import('@renderer/types/eshop').EshopProduct> {
    // Single product fetched via products list endpoint with matching ID
    const res = await this.request<import('@renderer/types/eshop').EshopProductListResponse>(
      `/api/eshop/admin/products?page=1&page_size=1000&include_inactive=true`
    )
    const product = res.products.find((p) => p.product_id === productId)
    if (!product) {
      throw { status: 404, message: `Produkt ${productId} nebol nájdený` } as import('./api').ApiError
    }
    return product
  }

  async createEshopProduct(
    data: import('@renderer/types/eshop').EshopProductCreateRequest,
    tenantId = 1
  ): Promise<import('@renderer/types/eshop').EshopProduct> {
    return this.request(`/api/eshop/admin/products?tenant_id=${tenantId}`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async updateEshopProduct(
    productId: number,
    data: import('@renderer/types/eshop').EshopProductUpdateRequest
  ): Promise<import('@renderer/types/eshop').EshopProduct> {
    return this.request(`/api/eshop/admin/products/${productId}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    })
  }

  async deleteEshopProduct(productId: number): Promise<void> {
    await this.request(`/api/eshop/admin/products/${productId}`, {
      method: 'DELETE'
    })
  }

  async getEshopTenants(): Promise<import('@renderer/types/eshop').EshopTenantListResponse> {
    return this.request('/api/eshop/admin/tenants')
  }
}

// Singleton export
export const api = new ApiClient()
