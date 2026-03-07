import { test, expect } from '../../fixtures/auth'
import { sel } from '../../helpers/selectors'
import { navigateToModule } from '../../helpers/sidebar'
import {
  apiGet,
  getPartnerCount,
  searchPartners,
  getPartnerDetail,
  getPartnerHistory,
  getPartnerAddresses,
} from '../../helpers/api'

test.describe('PAB Data Integrity', () => {
  test('DI-1: Celkový počet partnerov ≥ 150', async ({
    authenticatedPage: page,
  }) => {
    // Verify count via API (no is_active filter — matches UI default behavior)
    const total = await getPartnerCount(page.request)
    expect(total).toBeGreaterThanOrEqual(150)

    // Navigate to PAB list
    await navigateToModule(page, 'Katalógy', 'Katalóg partnerov')
    await page.locator(sel.partnerGrid).waitFor({ timeout: 15_000 })

    // UI should show record count in status bar
    const statusBar = page.locator(sel.partnerGrid).locator('text=/\\d+ z \\d+ záznamov/')
    await expect(statusBar).toBeVisible({ timeout: 10_000 })

    // Extract the total from status bar and compare with API
    const statusText = await statusBar.textContent()
    const match = statusText?.match(/(\d+) z (\d+) záznamov/)
    expect(match).toBeTruthy()
    const uiTotal = parseInt(match![2], 10)
    expect(uiTotal).toBe(total)
  })

  test('DI-2: Konkrétny partner — HOFFER s.r.o., IČO 36529214', async ({
    authenticatedPage: page,
  }) => {
    // Verify via API
    const result = await searchPartners(page.request, 'HOFFER')
    expect(result.total).toBe(1)

    const hoffer = result.items[0]
    expect(hoffer.partner_name).toBe('HOFFER s.r.o.')
    expect(hoffer.company_id).toBe('36529214')
    expect(hoffer.tax_id).toBe('2020158965')
    expect(hoffer.vat_id).toBe('SK2020158965')
    expect(hoffer.is_vat_payer).toBe(true)
    expect(hoffer.street).toBe('Bratislavská cesta 1798')
    expect(hoffer.city).toBe('Komárno')
    expect(hoffer.country_code).toBe('SK')
    expect(hoffer.partner_id).toBe(2337)
  })

  test('DI-3: Konkrétny partner — ICC s.r.o., IČO 31427332', async ({
    authenticatedPage: page,
  }) => {
    // Continental not in DB — use ICC s.r.o. (partner_id=1) instead
    const icc = await getPartnerDetail(page.request, 1)
    expect(icc.partner_name).toBe('ICC s.r.o.')
    expect(icc.company_id).toBe('31427332')
    expect(icc.city).toBe('Komárno')
    expect(icc.country_code).toBe('SK')
    expect(icc.partner_class).toBe('business')
  })

  test('DI-4: Krajinné kódy — 2-písmenkový ISO format', async ({
    authenticatedPage: page,
  }) => {
    const data = await apiGet(page.request, '/api/pab/partners?is_active=true&limit=200')
    const items = data.items as Array<{ country_code: string | null }>

    expect(items.length).toBeGreaterThan(0)

    // All country_code values must be 2-char ISO codes
    const countryCodes = items
      .map((p) => p.country_code)
      .filter((c): c is string => c !== null && c !== undefined)

    for (const code of countryCodes) {
      expect(code.length).toBe(2)
      expect(code).toMatch(/^[A-Z]{2}$/)
    }

    // Verify known codes exist
    const uniqueCodes = new Set(countryCodes)
    expect(uniqueCodes.has('SK')).toBe(true)

    // No legacy "KN" code
    expect(uniqueCodes.has('KN')).toBe(false)
  })

  test('DI-5: partner_id nie je sekvenčný (migračné IDs)', async ({
    authenticatedPage: page,
  }) => {
    const data = await apiGet(page.request, '/api/pab/partners?is_active=true&limit=200')
    const ids: number[] = data.items.map((p: { partner_id: number }) => p.partner_id)

    expect(ids.length).toBeGreaterThan(0)

    // IDs should NOT be sequential 1,2,3,...,N
    const isSequential = ids.every((id: number, i: number) => id === i + 1)
    expect(isSequential).toBe(false)

    // Max ID should be much larger than count (proves non-sequential)
    const maxId = Math.max(...ids)
    expect(maxId).toBeGreaterThan(ids.length * 10)
  })

  test('DI-6: Sub-entity endpointy — addresses, contacts, history pre partner 1', async ({
    authenticatedPage: page,
  }) => {
    // Addresses for partner 1 (ICC s.r.o.)
    const addresses = await getPartnerAddresses(page.request, 1)
    expect(Array.isArray(addresses)).toBe(true)
    expect(addresses.length).toBeGreaterThanOrEqual(1)

    // Check address shape
    const addr = addresses[0]
    expect(addr).toHaveProperty('address_type')
    expect(addr).toHaveProperty('street')
    expect(addr).toHaveProperty('city')
    expect(addr).toHaveProperty('country_code')
    expect(addr.partner_id).toBe(1)

    // History for partner 1
    const history = await getPartnerHistory(page.request, 1)
    expect(Array.isArray(history)).toBe(true)
    expect(history.length).toBeGreaterThanOrEqual(1)

    // History entry shape check
    const histEntry = history[0]
    expect(histEntry).toHaveProperty('history_id')
    expect(histEntry).toHaveProperty('partner_id')
    expect(histEntry).toHaveProperty('changed_by')
  })

  test('DI-7: Diakritika a case-insensitive search', async ({
    authenticatedPage: page,
  }) => {
    // Case-insensitive: "hoffer" lowercase = "HOFFER" uppercase
    const lowerResult = await searchPartners(page.request, 'hoffer')
    const upperResult = await searchPartners(page.request, 'HOFFER')
    expect(lowerResult.total).toBe(upperResult.total)
    expect(lowerResult.total).toBeGreaterThanOrEqual(1)

    // Diacritics: "Komárno" search should return results
    const diacResult = await searchPartners(page.request, 'Komárno')
    expect(diacResult.total).toBeGreaterThanOrEqual(1)

    // Verify the results actually contain the search term in city
    const cities = diacResult.items.map((p: { city: string }) => p.city)
    const hasKomarno = cities.some((c: string) => c.includes('Komárno'))
    expect(hasKomarno).toBe(true)
  })

  test('DI-8: Versioning — migračné záznamy s changed_by=migration', async ({
    authenticatedPage: page,
  }) => {
    // Check history for 3 different partners
    const partnerIds = [1, 2, 3]

    for (const pid of partnerIds) {
      const history = await getPartnerHistory(page.request, pid)
      expect(Array.isArray(history)).toBe(true)
      expect(history.length).toBeGreaterThanOrEqual(1)

      // First history entry should be migration
      const migrationEntry = history.find(
        (h: { changed_by: string }) => h.changed_by === 'migration'
      )
      expect(migrationEntry).toBeTruthy()
      expect(migrationEntry.modify_id).toBe(0)
    }
  })
})
