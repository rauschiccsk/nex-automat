/**
 * Playwright Global Teardown
 *
 * Runs after ALL test suites complete (even on failure).
 * Cleans up E2E test partners that may have been left behind
 * by crashed tests or soft-delete-only cleanup.
 *
 * Strategy: API-based soft delete (sets is_active=false).
 * This ensures E2E records don't pollute production data counts.
 * Works in both local and CI environments without DB access.
 */

const API_BASE = process.env.E2E_API_URL || 'http://localhost:9110'
const USERNAME = process.env.E2E_USERNAME || 'admin'
const PASSWORD = process.env.E2E_USER_PASSWORD || ''

async function getAuthToken(): Promise<string> {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
  })
  if (!res.ok) throw new Error(`Login failed: ${res.status}`)
  const data = await res.json()
  return data.access_token
}

async function globalTeardown() {
  try {
    const token = await getAuthToken()
    const headers = { Authorization: `Bearer ${token}` }

    // Fetch all partners with E2E_ prefix (active ones that were missed by per-test cleanup)
    const listRes = await fetch(
      `${API_BASE}/api/pab/partners?search=E2E_&is_active=true&limit=500`,
      { headers }
    )
    if (!listRes.ok) {
      console.error(`[Global Teardown] Failed to list partners: ${listRes.status}`)
      return
    }

    const data = await listRes.json()
    const partners = (data.items || []).filter(
      (p: { partner_name: string }) => p.partner_name?.startsWith('E2E_')
    )

    if (partners.length === 0) {
      console.log('[Global Teardown] No active E2E test partners to clean up')
      return
    }

    // Soft-delete each E2E partner
    let cleaned = 0
    for (const partner of partners) {
      try {
        const delRes = await fetch(
          `${API_BASE}/api/pab/partners/${partner.partner_id}`,
          { method: 'DELETE', headers }
        )
        if (delRes.ok) cleaned++
      } catch {
        // Ignore individual delete errors
      }
    }

    console.log(
      `[Global Teardown] Cleaned up ${cleaned}/${partners.length} E2E test partners`
    )
  } catch (error) {
    console.error('[Global Teardown] Failed to clean E2E data:', error)
    // Never fail the teardown — it must not block CI
  }
}

export default globalTeardown
