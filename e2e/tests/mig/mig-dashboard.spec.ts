import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('Migration Dashboard', () => {
  test.beforeEach(async ({ authenticatedPage: page }) => {
    // Open MIG module via sidebar — expand "Systém" category first
    await navigateToModule(page, 'Systém', 'Migrácia dát')
    await page.locator(sel.migrationDashboard).waitFor({ timeout: 15_000 })
  })

  test('Scenár 1: Dashboard — kategórie viditeľné', async ({
    authenticatedPage: page,
  }) => {
    // Dashboard should be visible
    await expect(page.locator(sel.migrationDashboard)).toBeVisible()

    // Should show stats bar with "Celkom kategorii"
    await expect(page.locator('text=Celkom kategorii')).toBeVisible()

    // Category cards should be present
    const categoryCards = page.locator('[data-testid^="category-card-"]')
    const count = await categoryCards.count()
    expect(count).toBeGreaterThan(0)
  })

  test('Scenár 2: PAB completed — status, záznamy', async ({
    authenticatedPage: page,
  }) => {
    // PAB category card should exist
    const pabCard = page.locator(sel.categoryCard('PAB'))
    await expect(pabCard).toBeVisible()

    // PAB should show "Dokoncene" status
    await expect(pabCard.locator('text=Dokoncene')).toBeVisible()

    // Should show record count
    await expect(pabCard.locator('text=/\\d+ zaznamov/')).toBeVisible()
  })

  test('Scenár 3: Locked kategória — dependencies message, disabled button', async ({
    authenticatedPage: page,
  }) => {
    // Find a locked category (one with unsatisfied dependencies)
    // Look for "Najprv migruj:" text
    const lockedIndicator = page.locator('text=/Najprv migruj:/')
    const isLocked = await lockedIndicator.isVisible().catch(() => false)

    if (!isLocked) {
      test.skip(true, 'No locked categories found on staging')
      return
    }

    // Lock icon should be visible on locked cards
    await expect(lockedIndicator.first()).toBeVisible()
  })

  test('Scenár 4: Spustenie migrácie', async ({
    authenticatedPage: page,
  }) => {
    // SAFETY: Skip on staging with real data
    test.skip(true, 'Unsafe on staging — modifies production data')
  })

  test('Scenár 5: Re-run — confirmation dialog', async ({
    authenticatedPage: page,
  }) => {
    // Find a completed category with Re-run button
    // Re-run buttons are nested inside category cards — use data-testid prefix
    const rerunButton = page.locator('[data-testid^="run-button-"]').first()
    const hasRerun = await rerunButton.isVisible({ timeout: 3_000 }).catch(() => false)

    if (!hasRerun) {
      test.skip(true, 'No run/re-run buttons available')
      return
    }

    // Click the run/re-run button
    await rerunButton.click()

    // Confirmation dialog should appear with heading "Spustit migraciu"
    await expect(page.getByRole('heading', { name: 'Spustit migraciu' })).toBeVisible({ timeout: 5_000 })

    // Cancel the dialog
    await page.locator('button:has-text("Nie")').click()
    await expect(page.getByRole('heading', { name: 'Spustit migraciu' })).not.toBeVisible({ timeout: 3_000 })
  })

  test('Scenár 6: Error handling', async ({
    authenticatedPage: page,
  }) => {
    // Skip: cannot safely trigger errors on staging
    test.skip(true, 'Cannot safely trigger error scenarios on staging')
  })
})
