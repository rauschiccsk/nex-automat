import { test as base, expect, type Page } from '@playwright/test'

/**
 * Auth fixture: logs in via UI and provides an authenticated page.
 *
 * E2E_USER_PASSWORD env variable must be set (never hardcoded).
 * Default username: admin (override with E2E_USERNAME).
 */

const USERNAME = process.env.E2E_USERNAME || 'admin'
const PASSWORD = process.env.E2E_USER_PASSWORD || ''

export interface AuthFixtures {
  authenticatedPage: Page
}

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Navigate to app
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Fill login form
    await page.locator('[data-testid="username"]').fill(USERNAME)
    await page.locator('[data-testid="password"]').fill(PASSWORD)
    await page.locator('[data-testid="login-button"]').click()

    // Wait for authenticated shell
    await expect(page.locator('[data-testid="sidebar"]')).toBeVisible({
      timeout: 15_000,
    })

    await use(page)
  },
})

export { expect }
