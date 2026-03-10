# NEX Automat — Database Schemas

## ESHOP Module (6 tabuliek)

### eshop_tenants
| Column | Type | Constraints |
|--------|------|-------------|
| tenant_id | SERIAL | PK |
| company_name | VARCHAR(255) | NOT NULL |
| partner_id | INTEGER | FK → partners |
| domain | VARCHAR(255) | NOT NULL, UNIQUE |
| brand_name | VARCHAR(255) | NOT NULL |
| logo_url | VARCHAR(500) | |
| primary_color | VARCHAR(7) | DEFAULT '#2E7D32' |
| api_token | VARCHAR(255) | NOT NULL, UNIQUE |
| comgate_merchant_id | VARCHAR(50) | |
| comgate_secret | VARCHAR(255) | |
| comgate_test_mode | BOOLEAN | DEFAULT true |
| fulfillment_provider | VARCHAR(50) | DEFAULT 'fullpost' |
| mufis_api_key | VARCHAR(255) | |
| mufis_webhook_url | VARCHAR(500) | |
| smtp_from | VARCHAR(255) | |
| admin_email | VARCHAR(255) | |
| currency | VARCHAR(3) | DEFAULT 'EUR' |
| vat_rate_default | NUMERIC(5,2) | DEFAULT 20.00 |
| default_lang | VARCHAR(2) | DEFAULT 'sk' |
| is_active | BOOLEAN | DEFAULT true |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

Trigger: eshop_update_timestamp

### eshop_products
| Column | Type | Constraints |
|--------|------|-------------|
| product_id | SERIAL | PK |
| tenant_id | INTEGER | FK → eshop_tenants, NOT NULL |
| sku | VARCHAR(50) | NOT NULL |
| barcode | VARCHAR(50) | |
| name | VARCHAR(255) | NOT NULL |
| short_description | VARCHAR(500) | |
| description | TEXT | |
| image_url | VARCHAR(500) | |
| price | NUMERIC(10,2) | NOT NULL |
| price_vat | NUMERIC(10,2) | NOT NULL |
| vat_rate | NUMERIC(5,2) | NOT NULL |
| stock_quantity | INTEGER | NOT NULL, DEFAULT 0 |
| weight | NUMERIC(8,3) | |
| is_active | BOOLEAN | DEFAULT true |
| sort_order | INTEGER | DEFAULT 0 |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

Unique: (tenant_id, sku)
Indexes: tenant_id, (tenant_id, sku), (tenant_id, is_active)
Trigger: eshop_update_timestamp

### eshop_orders
| Column | Type | Constraints |
|--------|------|-------------|
| order_id | SERIAL | PK |
| tenant_id | INTEGER | FK → eshop_tenants, NOT NULL |
| order_number | VARCHAR(50) | NOT NULL, UNIQUE |
| customer_email | VARCHAR(255) | NOT NULL |
| customer_name | VARCHAR(255) | NOT NULL |
| customer_phone | VARCHAR(50) | |
| lang | VARCHAR(2) | DEFAULT 'sk' |
| billing_name | VARCHAR(255) | |
| billing_name2 | VARCHAR(255) | |
| billing_street | VARCHAR(255) | |
| billing_city | VARCHAR(255) | |
| billing_zip | VARCHAR(20) | |
| billing_country | VARCHAR(2) | |
| shipping_name | VARCHAR(255) | |
| shipping_name2 | VARCHAR(255) | |
| shipping_street | VARCHAR(255) | |
| shipping_city | VARCHAR(255) | |
| shipping_zip | VARCHAR(20) | |
| shipping_country | VARCHAR(2) | |
| ico | VARCHAR(20) | |
| dic | VARCHAR(20) | |
| eu_vat_number | VARCHAR(20) | |
| total_amount | NUMERIC(10,2) | NOT NULL |
| total_amount_vat | NUMERIC(10,2) | NOT NULL |
| currency | VARCHAR(3) | DEFAULT 'EUR' |
| payment_method | VARCHAR(50) | |
| payment_status | VARCHAR(20) | DEFAULT 'pending' |
| comgate_transaction_id | VARCHAR(100) | |
| shipping_type | VARCHAR(50) | |
| shipping_price | NUMERIC(10,2) | DEFAULT 0 |
| delivery_point_group | VARCHAR(50) | |
| delivery_point_id | VARCHAR(50) | |
| tracking_number | VARCHAR(100) | |
| tracking_link | VARCHAR(500) | |
| multiple_packages | BOOLEAN | DEFAULT false |
| status | VARCHAR(20) | DEFAULT 'new' |
| note | TEXT | |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

Indexes: tenant_id, (tenant_id, status), order_number, (tenant_id, customer_email), updated_at DESC, created_at DESC
Trigger: eshop_update_timestamp

### eshop_order_items
| Column | Type | Constraints |
|--------|------|-------------|
| item_id | SERIAL | PK |
| order_id | INTEGER | FK → eshop_orders, NOT NULL |
| product_id | INTEGER | FK → eshop_products |
| sku | VARCHAR(50) | NOT NULL |
| name | VARCHAR(255) | NOT NULL |
| quantity | INTEGER | NOT NULL |
| unit_price | NUMERIC(10,2) | NOT NULL |
| unit_price_vat | NUMERIC(10,2) | NOT NULL |
| vat_rate | NUMERIC(5,2) | NOT NULL |
| item_type | VARCHAR(20) | DEFAULT 'product' |

Indexes: order_id
Note: item_type can be 'product' or 'discount' (negative price for discounts)

### eshop_order_status_history
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PK |
| order_id | INTEGER | FK → eshop_orders, NOT NULL |
| old_status | VARCHAR(20) | |
| new_status | VARCHAR(20) | NOT NULL |
| changed_by | VARCHAR(100) | |
| note | TEXT | |
| created_at | TIMESTAMP | DEFAULT NOW() |

Indexes: order_id

### eshop_leads
| Column | Type | Constraints |
|--------|------|-------------|
| lead_id | SERIAL | PK |
| tenant_id | INTEGER | FK → eshop_tenants, NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| first_name | VARCHAR(100) | |
| last_name | VARCHAR(100) | |
| phone | VARCHAR(50) | |
| discount_code | VARCHAR(50) | NOT NULL, UNIQUE |
| discount_percentage | NUMERIC(5,2) | NOT NULL, DEFAULT 50.00 |
| registered_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| expires_at | TIMESTAMPTZ | NOT NULL |
| first_order_id | INTEGER | FK → eshop_orders |
| reminder_count | INTEGER | NOT NULL, DEFAULT 0 |
| last_reminder_at | TIMESTAMPTZ | |
| gdpr_consent | BOOLEAN | NOT NULL, DEFAULT false |
| gdpr_consent_at | TIMESTAMPTZ | |
| is_active | BOOLEAN | NOT NULL, DEFAULT true |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

Indexes: tenant_id, email, discount_code, expires_at (partial: is_active=true)
Unique: (tenant_id, email)
Trigger: eshop_leads_update_timestamp
