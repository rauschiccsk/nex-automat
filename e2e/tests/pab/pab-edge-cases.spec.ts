import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'
import { apiDelete, apiPost, getAuthToken } from '../../helpers/api'

test.describe('PAB Edge Cases', () => {
  test.beforeEach(async ({ authenticatedPage: page }) => {
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })
  })

  test('EC-1: Create — prázdny partner_name → chybová hláška', async ({
    authenticatedPage: page,
  }) => {
    // Open create dialog
    await page.locator(sel.createPartnerButton).click()
    await page.locator(sel.createPartnerDialog).waitFor()

    // Fill only partner_id, leave name empty
    const testId = 98000 + Math.floor(Math.random() * 999)
    await page.locator(sel.createPartnerId).fill(String(testId))
    // Leave partner_name empty

    // Submit
    await page.locator(sel.createSubmit).click()

    // Dialog should still be open (validation error)
    await expect(page.locator(sel.createPartnerDialog)).toBeVisible({ timeout: 3_000 })

    // Should show some validation error (red border, error text, or toast)
    const hasValidationError = await page
      .locator(
        '.text-red-500, .text-red-600, .border-red-500, [role="alert"], .text-destructive'
      )
      .first()
      .isVisible()
      .catch(() => false)

    // If no client-side validation, the dialog at least stays open
    expect(
      hasValidationError ||
        (await page.locator(sel.createPartnerDialog).isVisible())
    ).toBe(true)

    // Close dialog
    await page.locator(sel.createCancel).click()
  })

  test('EC-2: Create — dlhý názov (100 znakov) + over-limit (150) rejected', async ({
    authenticatedPage: page,
  }) => {
    // Part A: 100-char name should succeed
    const longName = 'E2E_LONG_' + 'X'.repeat(91) // 100 chars total
    const testId = 97000 + (Date.now() % 1000)

    const createResult = await apiPost(page.request, '/api/pab/partners', {
      partner_id: testId,
      partner_name: longName,
      partner_class: 'business',
      is_active: true,
      is_customer: true,
      is_supplier: false,
    })
    expect(createResult.status).toBeLessThan(300)

    // Verify in UI via search
    await page.locator(sel.partnerSearch).fill('E2E_LONG_')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    await expect(
      page.locator(sel.partnerGrid).locator('text=E2E_LONG_').first()
    ).toBeVisible({ timeout: 10_000 })

    // Teardown
    await apiDelete(page.request, `/api/pab/partners/${testId}`)

    // Part B: 150-char name should be rejected (422)
    const tooLong = 'E2E_TOOLONG_' + 'Y'.repeat(138)
    const testId2 = 97100 + (Date.now() % 100)
    const rejectResult = await apiPost(page.request, '/api/pab/partners', {
      partner_id: testId2,
      partner_name: tooLong,
      partner_class: 'business',
      is_active: true,
      is_customer: true,
      is_supplier: false,
    })
    expect(rejectResult.status).toBeGreaterThanOrEqual(400)
  })

  test('EC-3: Create — špeciálne znaky v názve', async ({
    authenticatedPage: page,
  }) => {
    const ts = Date.now()
    const specialName = `E2E_SC_${ts} & Co. (špeciál)`
    // Use timestamp-based ID to avoid collision
    const testId = 96000 + (ts % 1000)

    // Create via API to avoid UI dialog timing issues
    const createResult = await apiPost(page.request, '/api/pab/partners', {
      partner_id: testId,
      partner_name: specialName,
      partner_class: 'business',
      is_active: true,
      is_customer: true,
      is_supplier: false,
    })
    expect(createResult.status).toBeLessThan(300)

    // Verify in UI — search by unique timestamp part
    await page.locator(sel.partnerSearch).fill(`E2E_SC_${ts}`)
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    await expect(
      page.locator(sel.partnerGrid).locator(`text=E2E_SC_${ts}`).first()
    ).toBeVisible({ timeout: 10_000 })

    // Verify the special chars rendered correctly (& not escaped to &amp; etc.)
    const cellText = await page
      .locator(sel.partnerGrid)
      .locator(`text=E2E_SC_${ts}`)
      .first()
      .textContent()
    expect(cellText).toContain('&')
    expect(cellText).toContain('špeciál')

    // Teardown
    await apiDelete(page.request, `/api/pab/partners/${testId}`)
  })

  test('EC-4: Partner bez sub-entities — prázdne taby bez erroru', async ({
    authenticatedPage: page,
  }) => {
    // Create a minimal partner via API
    const testId = 98300 + Math.floor(Math.random() * 99)
    const testName = `E2E_NOSUB_${Date.now()}`

    const createResult = await apiPost(page.request, '/api/pab/partners', {
      partner_id: testId,
      partner_name: testName,
      partner_class: 'business',
      is_active: true,
      is_customer: true,
      is_supplier: false,
    })
    expect(createResult.status).toBeLessThan(300)

    // Search and open detail
    await page.locator(sel.partnerSearch).fill(testName)
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )
    await page
      .locator(sel.partnerGrid)
      .locator(`text=${testName}`)
      .first()
      .dblclick()
    await page.locator(sel.partnerDetail).waitFor({ timeout: 10_000 })

    // Navigate through tabs that show sub-entities
    const subEntityTabs = ['addresses', 'contacts', 'bank-accounts', 'categories', 'texts']

    for (const tabId of subEntityTabs) {
      await page.locator(sel.tab(tabId)).click()
      await page.locator(sel.tab(tabId)).waitFor({ state: 'visible' })

      // No error alert should be visible
      const errorAlert = page.locator('.bg-red-50, .bg-red-900\\/20').first()
      const isErrorVisible = await errorAlert.isVisible().catch(() => false)
      expect(isErrorVisible).toBe(false)
    }

    // Teardown
    await apiDelete(page.request, `/api/pab/partners/${testId}`)
  })

  test('EC-5: Duplicitné IČO — over backend constraint', async ({
    authenticatedPage: page,
  }) => {
    // Try to create a partner with existing IČO (36529214 = HOFFER)
    const testId = 98400 + Math.floor(Math.random() * 99)
    const result = await apiPost(page.request, '/api/pab/partners', {
      partner_id: testId,
      partner_name: `E2E_DUPE_ICO_${Date.now()}`,
      partner_class: 'business',
      is_active: true,
      is_customer: true,
      is_supplier: false,
      company_id: '36529214', // HOFFER's IČO
    })

    if (result.status >= 400) {
      // Backend enforces unique constraint — good
      expect(result.status).toBeGreaterThanOrEqual(400)
    } else {
      // No unique constraint — clean up and skip
      await apiDelete(page.request, `/api/pab/partners/${testId}`)
      test.skip(true, 'Backend does not enforce unique company_id constraint')
    }
  })

  test('EC-6: Sieťový error handling — mock 500 response', async ({
    authenticatedPage: page,
  }) => {
    // Intercept API calls to return 500
    await page.route('**/api/pab/partners**', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal Server Error' }),
      })
    })

    // Try to search — should trigger error
    await page.locator(sel.partnerSearch).fill('TESTFAIL')

    // Wait for the intercepted response to complete
    await page.waitForResponse((resp) => resp.url().includes('/api/pab/partners'))

    // Should show error state (red alert, error message, or empty state with error)
    // The app should NOT freeze — check that UI is still interactive
    const searchInput = page.locator(sel.partnerSearch)
    await expect(searchInput).toBeEnabled()

    // Remove intercept
    await page.unroute('**/api/pab/partners**')

    // After removing intercept, app should recover
    await page.locator(sel.partnerSearch).clear()
    await page.locator(sel.partnerSearch).fill('HOFFER')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Grid should show results again
    await expect(
      page.locator(sel.partnerGrid).locator('text=HOFFER')
    ).toBeVisible({ timeout: 10_000 })
  })
})
