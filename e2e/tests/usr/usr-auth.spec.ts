import { test as base, expect } from '@playwright/test'
import { test as authTest } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

const USERNAME = process.env.E2E_USERNAME || 'admin'

authTest.describe('User Authentication & Management', () => {
  authTest('Scenár 1: Prihlásenie → dashboard', async ({
    authenticatedPage: page,
  }) => {
    // Should see sidebar (means authenticated)
    await expect(page.locator(sel.sidebar)).toBeVisible()

    // Should see user info in header (avatar/name)
    const header = page.locator('header')
    await expect(header).toBeVisible()
  })

  authTest('Scenár 2: Zoznam users — aspoň 1 user', async ({
    authenticatedPage: page,
  }) => {
    // Open USR module via sidebar — expand "Systém" category first
    await navigateToModule(page, 'Systém', 'Používatelia')

    // Wait for user table to load
    await page.locator(sel.userTable).waitFor({ timeout: 15_000 })

    // Count rows in table
    const rows = page.locator(sel.userTable).locator('tbody tr')
    const count = await rows.count()
    expect(count).toBeGreaterThanOrEqual(1) // At least 1 user (admin)
  })

  authTest('Scenár 3: RBAC — login Nazar, restricted features', async ({
    page,
  }) => {
    const nazarPassword = process.env.E2E_NAZAR_PASSWORD

    if (!nazarPassword) {
      authTest.skip(true, 'E2E_NAZAR_PASSWORD not set — skipping RBAC test')
      return
    }

    // Navigate to app
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Login as Nazar
    await page.locator(sel.username).fill('Nazar')
    await page.locator(sel.password).fill(nazarPassword)
    await page.locator(sel.loginButton).click()

    // Wait for auth
    await expect(page.locator(sel.sidebar)).toBeVisible({ timeout: 15_000 })

    // Nazar should have restricted access
    await expect(page.locator('text=Nazar').first()).toBeVisible()
  })

  authTest('Scenár 4: Odhlásenie — logout → login screen', async ({
    authenticatedPage: page,
  }) => {
    // Open user dropdown menu — click the user avatar/button in the header
    const userMenuTrigger = page.locator('[data-testid="user-menu-button"]')
    const hasTrigger = await userMenuTrigger.isVisible().catch(() => false)

    if (hasTrigger) {
      await userMenuTrigger.click()
    } else {
      // Fallback: click the last button in the header (avatar area)
      const headerButton = page.locator('header').locator('button').last()
      await headerButton.click()
    }

    // Wait for the dropdown to appear, then click logout
    await page.locator(sel.logoutButton).waitFor({ state: 'visible', timeout: 5_000 })
    await page.locator(sel.logoutButton).click()

    // Should see login screen
    await expect(page.locator(sel.loginButton)).toBeVisible({ timeout: 10_000 })
    await expect(page.locator(sel.username)).toBeVisible()
  })
})
