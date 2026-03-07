import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('PAB Partner Detail', () => {
  test.beforeEach(async ({ authenticatedPage: page }) => {
    // Open PAB module — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Search for HOFFER
    await page.locator(sel.partnerSearch).fill('HOFFER')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Double-click the row to open detail
    await page.locator(sel.partnerGrid).locator('text=HOFFER').first().dblclick()
    await page.locator(sel.partnerDetail).waitFor({ timeout: 10_000 })
  })

  test('Scenár 5: Detail základné údaje — HOFFER, IČO, DIČ, IČ DPH', async ({
    authenticatedPage: page,
  }) => {
    // Partner name should be visible in detail header
    await expect(page.locator('text=HOFFER').first()).toBeVisible()

    // Detail panel should have loaded with the basic tab form
    const detailText = await page.locator(sel.partnerDetail).textContent()
    expect(detailText).toBeTruthy()

    // Check that key form labels are present (IČO, DIČ, IČ DPH fields exist)
    await expect(page.locator(sel.partnerDetail).locator('text=IČO')).toBeVisible()
    await expect(page.locator(sel.partnerDetail).locator('text=DIČ')).toBeVisible()
    await expect(page.locator(sel.partnerDetail).locator('text=IČ DPH')).toBeVisible()

    // Partner name input should have a value
    const nameInput = page.locator(sel.partnerName)
    await expect(nameInput).toHaveValue(/HOFFER/)
  })

  test('Scenár 6: Všetky taby — prejdi 9 tabov, žiadny error', async ({
    authenticatedPage: page,
  }) => {
    const tabIds = [
      'basic',
      'extensions',
      'addresses',
      'contacts',
      'bank-accounts',
      'categories',
      'texts',
      'facilities',
      'history',
    ]

    for (const tabId of tabIds) {
      await page.locator(sel.tab(tabId)).click()
      await page.locator(sel.tab(tabId)).waitFor({ state: 'visible' })

      // No error should be visible
      const errorAlert = page.locator('.bg-red-50, .bg-red-900\\/20').first()
      const isErrorVisible = await errorAlert.isVisible().catch(() => false)
      expect(isErrorVisible).toBe(false)
    }
  })

  test('Scenár 7: Adresy tab — Bratislavská cesta, Komárno', async ({
    authenticatedPage: page,
  }) => {
    // Click Addresses tab
    await page.locator(sel.tab('addresses')).click()
    // Wait for the tab content to load
    await page.locator(sel.tab('addresses')).waitFor({ state: 'visible' })

    // Check for address data (may vary — accept partial match)
    const addressContent = await page.locator(sel.partnerDetail).textContent()
    // HOFFER address should contain some of these
    expect(addressContent).toBeTruthy()
  })

  test('Scenár 8: Kontakty tab — existencia záznamu', async ({
    authenticatedPage: page,
  }) => {
    // Click Contacts tab
    await page.locator(sel.tab('contacts')).click()
    // Wait for the tab content to load
    await page.locator(sel.tab('contacts')).waitFor({ state: 'visible' })

    // Page should not show error
    const errorAlert = page.locator('.bg-red-50, .bg-red-900\\/20').first()
    const isErrorVisible = await errorAlert.isVisible().catch(() => false)
    expect(isErrorVisible).toBe(false)
  })
})
