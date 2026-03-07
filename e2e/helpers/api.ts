import { Page, APIRequestContext } from '@playwright/test'

const API_BASE = process.env.E2E_API_URL || 'http://localhost:9110'
const USERNAME = process.env.E2E_USERNAME || 'admin'
const PASSWORD = process.env.E2E_USER_PASSWORD || 'admin'

/** Authenticate and return a Bearer token */
export async function getAuthToken(request: APIRequestContext): Promise<string> {
  const res = await request.post(`${API_BASE}/api/auth/login`, {
    data: { username: USERNAME, password: PASSWORD },
  })
  if (!res.ok()) {
    throw new Error(`Login failed: ${res.status()} ${await res.text()}`)
  }
  const data = await res.json()
  return data.access_token
}

/** Authenticated GET — returns parsed JSON */
export async function apiGet(request: APIRequestContext, path: string) {
  const token = await getAuthToken(request)
  const response = await request.get(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!response.ok()) {
    throw new Error(`API GET ${path} failed: ${response.status()}`)
  }
  return response.json()
}

/** Authenticated POST — returns { status, data } */
export async function apiPost(request: APIRequestContext, path: string, body: unknown) {
  const token = await getAuthToken(request)
  const response = await request.post(`${API_BASE}${path}`, {
    data: body,
    headers: { Authorization: `Bearer ${token}` },
  })
  return { status: response.status(), data: await response.json() }
}

/** Authenticated DELETE — returns { status } */
export async function apiDelete(request: APIRequestContext, path: string) {
  const token = await getAuthToken(request)
  const response = await request.delete(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return { status: response.status() }
}

/** Get total partner count from API */
export async function getPartnerCount(request: APIRequestContext): Promise<number> {
  const data = await apiGet(request, '/api/pab/partners?limit=1')
  return data.total
}

/** Search partners — returns { items, total, limit, offset } */
export async function searchPartners(request: APIRequestContext, query: string) {
  return apiGet(request, `/api/pab/partners?search=${encodeURIComponent(query)}`)
}

/** Get partner detail by ID */
export async function getPartnerDetail(request: APIRequestContext, partnerId: number) {
  return apiGet(request, `/api/pab/partners/${partnerId}`)
}

/** Get partner history */
export async function getPartnerHistory(request: APIRequestContext, partnerId: number) {
  return apiGet(request, `/api/pab/partners/${partnerId}/history`)
}

/** Get partner addresses */
export async function getPartnerAddresses(request: APIRequestContext, partnerId: number) {
  return apiGet(request, `/api/pab/partners/${partnerId}/addresses`)
}

export { API_BASE }
