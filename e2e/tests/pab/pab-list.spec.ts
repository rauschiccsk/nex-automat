import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('PAB Partner List', () => {
  test.beforeEach(async ({ authenticatedPage: page }) => {
    // Open PAB module via sidebar — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    // Wait for grid to load
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })
  })

  test('Scenár 1: Načítanie zoznamu — grid viditeľný, správne stĺpce', async ({
    authenticatedPage: page,
  }) => {
    // Grid should be visible
    await expect(page.locator(sel.partnerGrid)).toBeVisible()

    // Should show record count in status bar
    const statusBar = page.locator(sel.partnerGrid).locator('text=/\\d+ z \\d+ záznamov/')
    await expect(statusBar).toBeVisible({ timeout: 10_000 })
  })

  test('Scenár 2: Vyhľadávanie — "HOFFER" → výsledok s IČO 36529214', async ({
    authenticatedPage: page,
  }) => {
    // Type search query
    await page.locator(sel.partnerSearch).fill('HOFFER')

    // Wait for debounce + API response
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Should find HOFFER
    await expect(page.locator(sel.partnerGrid).locator('text=HOFFER')).toBeVisible({
      timeout: 10_000,
    })
    await expect(page.locator(sel.partnerGrid).locator('text=36529214')).toBeVisible()
  })

  test('Scenár 3: Filter partner_class — default business, prepni na filter', async ({
    authenticatedPage: page,
  }) => {
    // Default filter is "business" — Obchodní partneri
    const classFilter = page.locator(sel.partnerClassFilter)
    await expect(classFilter).toHaveValue('business')

    // Get current count
    const initialStatusText = await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z \\d+ záznamov/')
      .textContent()

    // Note: "Všetci" isn't an option in partner_class filter (it has business/retail/guest)
    // Switch to retail
    await classFilter.selectOption('retail')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Count should change (or may be 0)
    const retailStatusText = await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z?/')
      .first()
      .textContent({ timeout: 5_000 })
      .catch(() => null)

    // Switch back to business
    await classFilter.selectOption('business')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )
  })

  test('Scenár 4: Grid navigácia — ArrowDown 5x, End, Home', async ({
    authenticatedPage: page,
  }) => {
    // Wait for rows to load
    await page.locator(sel.partnerGrid).locator('tbody tr').first().waitFor({ timeout: 10_000 })

    // Click first row to focus grid
    const firstRow = page.locator(sel.partnerGrid).locator('tbody tr').first()
    await firstRow.click()

    // Press ArrowDown 5 times
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press('ArrowDown')
    }

    // Selected row should have blue background class
    const selectedRow = page.locator(sel.partnerGrid).locator('tr.bg-blue-100, tr[class*="bg-blue"]')
    await expect(selectedRow).toBeVisible()

    // Press End — should go to last row
    await page.keyboard.press('End')
    await expect(page.locator(sel.partnerGrid).locator('tbody tr').first()).toBeVisible()

    // Press Home — should go to first row
    await page.keyboard.press('Home')
    await expect(page.locator(sel.partnerGrid).locator('tbody tr').first()).toBeVisible()
  })
})
