/** Centralized selectors for E2E tests — keyed by data-testid */

export const sel = {
  // Login
  username: '[data-testid="username"]',
  password: '[data-testid="password"]',
  loginButton: '[data-testid="login-button"]',

  // Layout
  sidebar: '[data-testid="sidebar"]',
  logoutButton: '[data-testid="logout-button"]',

  // PAB List
  partnerGrid: '[data-testid="partner-grid"]',
  partnerSearch: '[data-testid="partner-search"]',
  partnerClassFilter: '[data-testid="partner-class-filter"]',
  createPartnerButton: '[data-testid="create-partner-button"]',

  // PAB Detail
  partnerDetail: '[data-testid="partner-detail"]',
  partnerName: '[data-testid="partner-name"]',
  saveButton: '[data-testid="save-button"]',
  deleteButton: '[data-testid="delete-button"]',
  tab: (name: string) => `[data-testid="tab-${name}"]`,

  // PAB Create Dialog
  createPartnerDialog: '[data-testid="create-partner-dialog"]',
  createPartnerName: '[data-testid="create-partner-name"]',
  createPartnerId: '[data-testid="create-partner-id"]',
  createSubmit: '[data-testid="create-submit"]',
  createCancel: '[data-testid="create-cancel"]',

  // Migration Dashboard
  migrationDashboard: '[data-testid="migration-dashboard"]',
  categoryCard: (cat: string) => `[data-testid="category-card-${cat}"]`,
  runButton: (cat: string) => `[data-testid="run-button-${cat}"]`,

  // Users
  userTable: '[data-testid="user-table"]',
} as const
