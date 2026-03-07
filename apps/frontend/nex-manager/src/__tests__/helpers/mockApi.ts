import { vi } from 'vitest'

interface MockResponse<T = unknown> {
  data: T
  status?: number
  ok?: boolean
}

export function mockFetch(responses: Record<string, MockResponse>) {
  return vi.fn().mockImplementation((url: string, options?: RequestInit) => {
    const method = options?.method || 'GET'
    const key = `${method} ${url}`

    const matchedKey = Object.keys(responses).find((pattern) => {
      if (key === pattern) return true
      const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$')
      return regex.test(key)
    })

    if (matchedKey) {
      const resp = responses[matchedKey]
      return Promise.resolve({
        ok: resp.ok !== false,
        status: resp.status || 200,
        json: () => Promise.resolve(resp.data),
        text: () => Promise.resolve(JSON.stringify(resp.data))
      })
    }

    return Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({ detail: 'Not found' }),
      text: () => Promise.resolve('Not found')
    })
  })
}

export const mockPartners = [
  {
    partner_id: 1,
    partner_name: 'HOFFER SK s.r.o.',
    ico: '36529214',
    dic: '2021897584',
    vat_id: 'SK2021897584',
    is_vat_payer: true,
    is_supplier: true,
    is_customer: true,
    partner_class: 'business',
    street: 'Bratislavská cesta 1798',
    city: 'Komárno',
    zip_code: '94501',
    country_code: 'SK',
    is_active: true,
    modify_id: 0
  },
  {
    partner_id: 2,
    partner_name: 'Continental Barum s.r.o.',
    ico: '45357846',
    dic: '2022984561',
    vat_id: 'CZ2022984561',
    is_vat_payer: true,
    is_supplier: true,
    is_customer: false,
    partner_class: 'business',
    street: 'Objízdná 1628',
    city: 'Otrokovice',
    zip_code: '76502',
    country_code: 'CZ',
    is_active: true,
    modify_id: 0
  },
  {
    partner_id: 3,
    partner_name: 'Ján Kováč',
    ico: null,
    dic: null,
    vat_id: null,
    is_vat_payer: false,
    is_supplier: false,
    is_customer: true,
    partner_class: 'retail',
    street: 'Hlavná 15',
    city: 'Košice',
    zip_code: '04001',
    country_code: 'SK',
    is_active: true,
    modify_id: 0
  }
]

export const mockPartnerDetail = {
  ...mockPartners[0],
  extensions: {
    payment_due_days: 30,
    credit_limit: 50000,
    discount_percent: 5,
    currency: 'EUR'
  },
  addresses: [
    {
      address_id: 1,
      partner_id: 1,
      address_type: 'registered',
      street: 'Bratislavská cesta 1798',
      city: 'Komárno',
      zip_code: '94501',
      country_code: 'SK'
    }
  ],
  contacts: [
    {
      contact_id: 1,
      partner_id: 1,
      address_type: 'registered',
      contact_type: 'email',
      contact_value: 'info@hoffer.sk'
    }
  ],
  bank_accounts: [
    {
      bank_account_id: 1,
      partner_id: 1,
      iban: 'SK3112000000198742637541',
      swift: 'TATRSKBX',
      bank_name: 'Tatra banka',
      is_primary: true
    }
  ],
  categories: [],
  texts: { owner_name: null, description: null, notice: null },
  facilities: [],
  history: [
    {
      version_id: 1,
      partner_id: 1,
      modify_id: 0,
      valid_from: '2025-01-15T10:00:00Z',
      valid_to: null,
      changed_by: 'migration'
    }
  ]
}

export const mockMigrationCategories = [
  { category: 'PAB', status: 'completed', record_count: 164, dependencies: [] },
  { category: 'GSC', status: 'pending', record_count: 0, dependencies: [] },
  { category: 'STK', status: 'pending', record_count: 0, dependencies: ['GSC'] },
  { category: 'TSH', status: 'pending', record_count: 0, dependencies: ['GSC', 'STK'] },
  { category: 'ICB', status: 'pending', record_count: 0, dependencies: ['PAB', 'GSC'] },
  { category: 'ISB', status: 'pending', record_count: 0, dependencies: ['PAB', 'GSC'] },
  { category: 'OBJ', status: 'pending', record_count: 0, dependencies: ['PAB', 'GSC', 'STK'] },
  { category: 'DOD', status: 'pending', record_count: 0, dependencies: ['PAB', 'GSC'] },
  { category: 'PAYJRN', status: 'pending', record_count: 0, dependencies: ['PAB'] }
]

export function setupPabMocks() {
  const fetchMock = mockFetch({
    'GET /api/pab/partners': {
      data: { items: mockPartners, total: mockPartners.length }
    },
    'GET /api/pab/partners/*': {
      data: mockPartnerDetail
    },
    'POST /api/pab/partners': {
      data: { ...mockPartners[0], partner_id: 999 },
      status: 201
    },
    'PUT /api/pab/partners/*': {
      data: { ...mockPartners[0], modify_id: 1 }
    },
    'DELETE /api/pab/partners/*': {
      data: { message: 'Partner deactivated' }
    },
    'GET /api/system/modules': {
      data: [
        { code: 'PAB', name: 'Katalóg partnerov', is_active: true },
        { code: 'MIG', name: 'Migrácia dát', is_active: true },
        { code: 'USR', name: 'Používatelia', is_active: true }
      ]
    }
  })

  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

export function setupMigMocks() {
  const fetchMock = mockFetch({
    'GET /api/migration/categories': {
      data: mockMigrationCategories
    },
    'POST /api/migration/run': {
      data: { status: 'completed', records_processed: 164, errors: [] }
    },
    'POST /api/migration/categories/*/reset': {
      data: { status: 'pending' }
    }
  })

  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}
