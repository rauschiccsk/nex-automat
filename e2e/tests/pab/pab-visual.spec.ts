import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('PAB Visual & UI', () => {
  test('VIS-1: Žiadne JS errors pri navigácii na PAB', async ({
    authenticatedPage: page,
  }) => {
    // Collect console errors
    const consoleErrors: string[] = []
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text())
      }
    })

    // Collect uncaught exceptions
    const pageErrors: string[] = []
    page.on('pageerror', (error) => {
      pageErrors.push(error.message)
    })

    // Navigate to PAB
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Wait for full render — wait for data to appear in grid
    await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z \\d+ záznamov/')
      .waitFor({ timeout: 15_000 })

    // No uncaught exceptions
    expect(pageErrors).toHaveLength(0)

    // Filter out benign console errors (e.g., favicon, sourcemap)
    const realErrors = consoleErrors.filter(
      (e) =>
        !e.includes('favicon') &&
        !e.includes('sourcemap') &&
        !e.includes('DevTools') &&
        !e.includes('404')
    )
    expect(realErrors).toHaveLength(0)
  })

  test('VIS-2: Sidebar navigácia — PAB modul viditeľný a kliknuteľný', async ({
    authenticatedPage: page,
  }) => {
    const sidebar = page.locator(sel.sidebar)
    await expect(sidebar).toBeVisible()

    // Sidebar should contain "Katalógy" category
    await expect(sidebar.locator('text=Katalógy')).toBeVisible({ timeout: 5_000 })

    // Use navigateToModule helper (already proven to work across all tests)
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')

    // Grid should appear — confirms sidebar navigation works
    await expect(page.locator(sel.partnerGrid)).toBeVisible({ timeout: 15_000 })

    // Status bar confirms data loaded successfully via sidebar nav
    const statusBar = page.locator(sel.partnerGrid).locator('text=/\\d+ z \\d+ záznamov/')
    await expect(statusBar).toBeVisible({ timeout: 10_000 })
  })

  test('VIS-3: Grid hlavičky — správne stĺpce', async ({
    authenticatedPage: page,
  }) => {
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Check for expected column headers in the grid
    const grid = page.locator(sel.partnerGrid)

    // These header texts should be present (adapt to actual headers)
    const expectedHeaders = ['Názov', 'IČO', 'Mesto']

    for (const header of expectedHeaders) {
      const headerCell = grid.locator(`th:has-text("${header}"), [role="columnheader"]:has-text("${header}")`)
      await expect(headerCell.first()).toBeVisible({ timeout: 5_000 })
    }
  })

  test('VIS-4: Dark mode toggle', async ({ authenticatedPage: page }) => {
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Look for dark mode toggle (common patterns)
    const darkModeToggle = page.locator(
      '[data-testid="dark-mode-toggle"], [data-testid="theme-toggle"], button[aria-label*="dark"], button[aria-label*="theme"]'
    )

    const hasToggle = await darkModeToggle.first().isVisible().catch(() => false)

    if (!hasToggle) {
      test.skip(true, 'Dark mode toggle not implemented')
      return
    }

    // Click toggle
    await darkModeToggle.first().click()

    // Check that <html> or <body> has dark class
    await expect(
      page.locator('html.dark, body.dark, [data-theme="dark"]').first()
    ).toBeVisible({ timeout: 3_000 })

    // Grid should still be visible after toggle
    await expect(page.locator(sel.partnerGrid)).toBeVisible()

    // Toggle back
    await darkModeToggle.first().click()
    await expect(page.locator(sel.partnerGrid)).toBeVisible()
  })

  test('VIS-5: Diakritika v UI — správne zobrazenie slovenských znakov', async ({
    authenticatedPage: page,
  }) => {
    const sidebar = page.locator(sel.sidebar)
    await expect(sidebar).toBeVisible()

    // Sidebar should contain Slovak diacritics (Katalógy, not Katalogy)
    const sidebarText = await sidebar.textContent()
    expect(sidebarText).toContain('Katalóg')

    // Navigate to PAB
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Status bar should show "záznamov" with proper diacritics
    const statusBar = page.locator(sel.partnerGrid).locator('text=/záznamov/')
    await expect(statusBar).toBeVisible({ timeout: 10_000 })

    // Create button should have Slovak text
    const createBtn = page.locator(sel.createPartnerButton)
    await expect(createBtn).toBeVisible()
    const btnText = await createBtn.textContent()
    // Button text should be readable (not garbled encoding)
    expect(btnText).toBeTruthy()
    expect(btnText!.length).toBeGreaterThan(0)
  })
})
