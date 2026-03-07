import type { Page } from '@playwright/test'

/**
 * Expands a sidebar category if it is collapsed, then clicks the module button.
 *
 * The sidebar has collapsible categories (Systém, Katalógy, Sklad, etc.).
 * Each category is a `<button>` containing the category name and a chevron icon.
 * When collapsed, the child module buttons are hidden.
 *
 * This helper:
 * 1. Waits for sidebar to be visible
 * 2. Tries to click the module button (first in favorites/recent, then in categories)
 * 3. If not visible, expands the parent category and clicks the module button
 */
export async function navigateToModule(
  page: Page,
  categoryName: string,
  moduleName: string,
): Promise<void> {
  const sidebar = page.locator('[data-testid="sidebar"]')
  await sidebar.waitFor({ timeout: 10_000 })

  // Small settle delay — sidebar may be animating after previous navigation
  await page.waitForTimeout(300)

  // Look for module button anywhere in sidebar (favorites, recent, or categories)
  const moduleButton = sidebar.locator(`button:has-text("${moduleName}")`)

  // Check if the module button is already visible (in favorites/recent or expanded category)
  const isVisible = await moduleButton.first().isVisible().catch(() => false)

  if (!isVisible) {
    // Expand the parent category by clicking its button
    // Use exact category button — it's the one that contains ONLY the category name + chevron
    const categoryButton = sidebar.locator(`button:has-text("${categoryName}")`).first()
    await categoryButton.click()
    // Wait for the module button to become visible after expansion
    await moduleButton.first().waitFor({ state: 'visible', timeout: 5_000 })
  }

  // Click the first matching module button
  await moduleButton.first().click()

  // Small settle delay after module opens
  await page.waitForTimeout(300)
}
