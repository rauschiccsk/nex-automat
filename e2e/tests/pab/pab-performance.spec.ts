import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('PAB Performance', () => {
  test('PERF-1: Načítanie zoznamu partnerov < 5000ms', async ({
    authenticatedPage: page,
  }) => {
    const startTime = Date.now()

    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Wait for actual data to appear (status bar with record count)
    await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z \\d+ záznamov/')
      .waitFor({ timeout: 15_000 })

    const loadTime = Date.now() - startTime

    // Threshold: 5s for self-hosted runner (includes navigation + API + render)
    expect(loadTime).toBeLessThan(5000)
    console.log(`PAB list load time: ${loadTime}ms`)
  })

  test('PERF-2: Načítanie detailu partnera < 3000ms', async ({
    authenticatedPage: page,
  }) => {
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Search for known partner
    await page.locator(sel.partnerSearch).fill('HOFFER')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )
    await page.locator(sel.partnerGrid).locator('text=HOFFER').first().waitFor({ timeout: 10_000 })

    // Measure detail load
    const startTime = Date.now()
    await page.locator(sel.partnerGrid).locator('text=HOFFER').first().dblclick()
    await page.locator(sel.partnerDetail).waitFor({ timeout: 10_000 })

    // Wait for form fields to render
    await page.locator(sel.partnerName).waitFor({ timeout: 10_000 })

    const loadTime = Date.now() - startTime

    // Threshold: 3s for detail view (includes API + render)
    expect(loadTime).toBeLessThan(3000)
    console.log(`PAB detail load time: ${loadTime}ms`)
  })

  test('PERF-3: Search response < 3000ms (vrátane debounce)', async ({
    authenticatedPage: page,
  }) => {
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Wait for initial data load
    await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z \\d+ záznamov/')
      .waitFor({ timeout: 15_000 })

    // Measure search
    const startTime = Date.now()
    await page.locator(sel.partnerSearch).fill('HOFFER')

    // Wait for search results (HOFFER row visible)
    await expect(
      page.locator(sel.partnerGrid).locator('text=HOFFER')
    ).toBeVisible({ timeout: 10_000 })

    const searchTime = Date.now() - startTime

    // Threshold: 3s including debounce delay + API + render
    expect(searchTime).toBeLessThan(3000)
    console.log(`PAB search response time: ${searchTime}ms`)
  })

  test('PERF-4: Grid scroll — žiadny JS error, riadky renderované', async ({
    authenticatedPage: page,
  }) => {
    // Collect JS errors
    const jsErrors: string[] = []
    page.on('pageerror', (error) => {
      jsErrors.push(error.message)
    })

    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Wait for data
    await page
      .locator(sel.partnerGrid)
      .locator('text=/\\d+ z \\d+ záznamov/')
      .waitFor({ timeout: 15_000 })

    // Click first row to focus grid
    const firstRow = page.locator(sel.partnerGrid).locator('tbody tr').first()
    await firstRow.click()

    // Scroll down using keyboard (small delay for render between key presses)
    for (let i = 0; i < 20; i++) {
      await page.keyboard.press('ArrowDown')
    }

    // Press End to jump to last row
    await page.keyboard.press('End')
    // Wait for rows to be rendered after scroll
    await expect(page.locator(sel.partnerGrid).locator('tbody tr').first()).toBeVisible()

    // Rows should still be rendered
    const visibleRows = page.locator(sel.partnerGrid).locator('tbody tr')
    const rowCount = await visibleRows.count()
    expect(rowCount).toBeGreaterThan(0)

    // Press Home to go back
    await page.keyboard.press('Home')
    await expect(page.locator(sel.partnerGrid).locator('tbody tr').first()).toBeVisible()

    // No JS errors during scrolling
    expect(jsErrors).toHaveLength(0)
  })
})
