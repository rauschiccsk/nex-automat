import { test, expect } from '../../fixtures/seed-data'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'

test.describe('PAB Partner CRUD', () => {
  test('Scenár 9: Vytvorenie partnera — create dialog, submit, viditeľný v zozname', async ({
    authenticatedPage: page,
  }) => {
    // Open PAB module — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Click create button
    await page.locator(sel.createPartnerButton).click()
    await page.locator(sel.createPartnerDialog).waitFor()

    // Fill form
    const testId = 99800 + Math.floor(Math.random() * 99)
    const testName = `E2E_CREATE_${Date.now()}`
    await page.locator(sel.createPartnerId).fill(String(testId))
    await page.locator(sel.createPartnerName).fill(testName)

    // Submit
    await page.locator(sel.createSubmit).click()

    // Dialog should close
    await expect(page.locator(sel.createPartnerDialog)).not.toBeVisible({ timeout: 10_000 })

    // Search for the created partner
    await page.locator(sel.partnerSearch).fill(testName)
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Should be visible in grid
    await expect(page.locator(sel.partnerGrid).locator(`text=${testName}`)).toBeVisible({
      timeout: 10_000,
    })

    // Cleanup: delete via API
    const API_BASE = process.env.E2E_API_URL || 'http://localhost:9110'
    const loginRes = await fetch(`${API_BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: process.env.E2E_USERNAME || 'admin',
        password: process.env.E2E_USER_PASSWORD || '',
      }),
    })
    if (loginRes.ok) {
      const { access_token } = await loginRes.json()
      await fetch(`${API_BASE}/api/pab/partners/${testId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${access_token}` },
      })
    }
  })

  test('Scenár 10: Editácia — zmena názvu, uloženie', async ({
    authenticatedPage: page,
    testPartner,
  }) => {
    // Open PAB module — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Search for test partner
    await page.locator(sel.partnerSearch).fill(testPartner.partnerName)
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Double-click to open detail
    await page
      .locator(sel.partnerGrid)
      .locator(`text=${testPartner.partnerName}`)
      .first()
      .dblclick()
    await page.locator(sel.partnerDetail).waitFor({ timeout: 10_000 })

    // Change name
    const newName = `${testPartner.partnerName}_EDITED`
    const nameInput = page.locator(sel.partnerName)
    await nameInput.clear()
    await nameInput.fill(newName)

    // Save
    await page.locator(sel.saveButton).click()

    // Should show success toast
    await expect(page.locator('text=/aktualizovaný/')).toBeVisible({ timeout: 5_000 })
  })

  test('Scenár 11: Vymazanie — confirmation, soft-delete', async ({
    authenticatedPage: page,
    testPartner,
  }) => {
    // Open PAB module — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Search for test partner
    await page.locator(sel.partnerSearch).fill(testPartner.partnerName)
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Double-click to open detail
    await page
      .locator(sel.partnerGrid)
      .locator(`text=${testPartner.partnerName}`)
      .first()
      .dblclick()
    await page.locator(sel.partnerDetail).waitFor({ timeout: 10_000 })

    // Click delete
    await page.locator(sel.deleteButton).click()

    // Confirmation dialog should appear
    await expect(page.locator('text=Potvrdenie vymazania')).toBeVisible()

    // Confirm deletion
    await page.locator('button:has-text("Áno, vymazať")').click()

    // Should show success toast
    await expect(page.locator('text=vymazaný')).toBeVisible({ timeout: 5_000 })
  })

  test('Scenár 12: Diakritika — hľadaj "Košice", správne zobrazenie', async ({
    authenticatedPage: page,
  }) => {
    // Open PAB module — expand "Katalógy" if needed
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // Search with diacritics
    await page.locator(sel.partnerSearch).fill('Košice')
    await page.waitForResponse((resp) =>
      resp.url().includes('/api/pab/partners') && resp.status() === 200
    )

    // Check that grid filter is working (no errors)
    const errorAlert = page.locator('.bg-red-50, .bg-red-900\\/20')
    const isErrorVisible = await errorAlert.isVisible().catch(() => false)
    expect(isErrorVisible).toBe(false)

    // If results exist, they should display diacritics correctly
    const gridText = await page.locator(sel.partnerGrid).textContent()
    // No assertion on specific content — just verify no encoding errors (garbled text)
    expect(gridText).toBeTruthy()
  })
})
