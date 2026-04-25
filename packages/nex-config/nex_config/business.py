"""Business rule defaults — payment terms, VAT rates, currency codes.

These are runtime-tunable defaults used as fallbacks when per-tenant or
per-record overrides are absent. In Track 2 Phase 2.3 (backfill) some of
these may be replaced with reads from the Settings API
(`/api/system/settings`); these constants stay as compile-time fallbacks
when settings are unavailable (boot, DB unreachable).
"""

# Default payment due days — used by PAB partner_catalog + legacy partners
# schemas as default for new partner records. Tenant or per-partner overrides
# happen at row level.
DEFAULT_PAYMENT_DUE_DAYS = 14

# Default VAT rate (%) — used by eshop XML export when item-level vat_rate
# is missing. Real per-product rates come from product/order data; this is
# the safety fallback.
DEFAULT_VAT_RATE_PERCENT = 20
