import { test as authTest, expect } from './auth'
import type { Page } from '@playwright/test'

const API_BASE = process.env.E2E_API_URL || 'http://localhost:9110'

interface TestPartnerFixture {
  partnerId: number
  partnerName: string
  cleanup: () => Promise<void>
}

export interface SeedFixtures {
  testPartner: TestPartnerFixture
}

async function getAuthToken(): Promise<string> {
  const username = process.env.E2E_USERNAME || 'admin'
  const password = process.env.E2E_USER_PASSWORD || ''
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) throw new Error(`Login failed: ${res.status}`)
  const data = await res.json()
  return data.access_token
}

export const test = authTest.extend<SeedFixtures>({
  testPartner: async ({}, use) => {
    const token = await getAuthToken()
    const partnerId = 99900 + Math.floor(Math.random() * 99)
    const partnerName = `E2E_TEST_${Date.now()}`

    // Create test partner via API
    const createRes = await fetch(`${API_BASE}/api/pab/partners`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        partner_id: partnerId,
        partner_name: partnerName,
        partner_class: 'business',
        is_active: true,
        is_customer: true,
        is_supplier: false,
      }),
    })

    if (!createRes.ok) {
      const err = await createRes.text()
      throw new Error(`Failed to create test partner: ${createRes.status} ${err}`)
    }

    const cleanup = async (): Promise<void> => {
      try {
        const freshToken = await getAuthToken()
        await fetch(`${API_BASE}/api/pab/partners/${partnerId}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${freshToken}` },
        })
      } catch {
        // Ignore cleanup errors
      }
    }

    await use({ partnerId, partnerName, cleanup })

    // Teardown: always clean up
    await cleanup()
  },
})

export { expect }
