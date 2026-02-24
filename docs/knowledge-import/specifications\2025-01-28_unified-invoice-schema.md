# Unified Supplier Invoice Schema

**Category:** specifications
**Created:** 2025-01-28
**Status:** PRODUCTION

## Overview

Jednotná databázová schéma pre elektronické faktúry používaná na všetkých serveroch:
- ANDROS Server (nex_automat DB)
- MAGERSTAV Server (supplier_invoice_staging DB)

## Table: supplier_invoice_heads (47 columns)

### Multi-tenant Identification
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | SERIAL | NO | Primary key |
| customer_code | VARCHAR(50) | NO | Customer identifier (ANDROS, MAGERSTAV) |
| supplier_code | VARCHAR(50) | NO | Supplier identifier (MARSO, LL, etc.) |

### XML Source Data (xml_*)
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| xml_invoice_number | VARCHAR(50) | NO | Invoice number from XML |
| xml_variable_symbol | VARCHAR(10) | YES | Variable symbol |
| xml_issue_date | DATE | YES | Issue date |
| xml_due_date | DATE | YES | Due date |
| xml_tax_point_date | DATE | YES | Tax point date |
| xml_delivery_date | DATE | YES | Delivery date |
| xml_currency | VARCHAR(3) | YES | Currency (EUR) |
| xml_supplier_ico | VARCHAR(20) | NO | Supplier ICO |
| xml_supplier_dic | VARCHAR(20) | YES | Supplier DIC |
| xml_supplier_ic_dph | VARCHAR(20) | YES | Supplier IC DPH |
| xml_supplier_name | VARCHAR(255) | YES | Supplier name |
| xml_iban | VARCHAR(34) | YES | IBAN from XML |
| xml_swift | VARCHAR(20) | YES | SWIFT from XML |
| xml_total_without_vat | NUMERIC(15,2) | NO | Total excl. VAT |
| xml_total_vat | NUMERIC(15,2) | NO | VAT amount |
| xml_total_with_vat | NUMERIC(15,2) | NO | Total incl. VAT |

### NEX Genesis Enrichment (nex_*)
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| nex_supplier_id | INTEGER | YES | NEX supplier ID |
| nex_supplier_modify_id | INTEGER | YES | NEX modify ID |
| nex_iban | VARCHAR(34) | YES | IBAN from NEX |
| nex_swift | VARCHAR(20) | YES | SWIFT from NEX |
| nex_stock_id | INTEGER | YES | Default stock ID |
| nex_book_num | INTEGER | YES | Accounting book |
| nex_payment_method_id | INTEGER | YES | Payment method |
| nex_price_list_id | INTEGER | YES | Price list ID |
| nex_document_id | INTEGER | YES | NEX document ID |
| nex_invoice_doc_id | VARCHAR(50) | YES | Invoice doc ID |
| nex_delivery_doc_id | VARCHAR(50) | YES | Delivery doc ID |

### Processing Status
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| source_type | VARCHAR(20) | YES | Source: xml, api |
| status | VARCHAR(20) | YES | pending/matched/approved/imported |
| item_count | INTEGER | YES | Number of items |
| items_matched | INTEGER | YES | Matched items count |
| match_percent | NUMERIC(5,2) | YES | Match percentage |
| validation_status | VARCHAR(20) | YES | Validation status |
| validation_errors | JSONB | YES | Validation errors |

### File References
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| file_basename | VARCHAR(255) | YES | Original filename |
| file_status | VARCHAR(20) | YES | File processing status |
| xml_file_path | VARCHAR(500) | YES | Path to XML |
| pdf_file_path | VARCHAR(500) | YES | Path to PDF |
| isdoc_xml | TEXT | YES | Full ISDOC XML content |

### Timestamps
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| fetched_at | TIMESTAMPTZ | YES | API fetch time |
| created_at | TIMESTAMPTZ | YES | Record created |
| updated_at | TIMESTAMPTZ | YES | Record updated |
| processed_at | TIMESTAMPTZ | YES | Processing time |
| imported_at | TIMESTAMPTZ | YES | NEX import time |

## Table: supplier_invoice_items (40 columns)

### Identification
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | SERIAL | NO | Primary key |
| head_id | INTEGER | NO | FK to heads |
| xml_line_number | INTEGER | YES | Line number |

### XML Source Data
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| xml_seller_code | VARCHAR(50) | YES | Seller product code |
| xml_ean | VARCHAR(20) | YES | EAN barcode |
| xml_product_name | VARCHAR(255) | YES | Product name |
| xml_quantity | NUMERIC(10,3) | NO | Quantity |
| xml_unit | VARCHAR(10) | YES | Unit of measure |
| xml_unit_price | NUMERIC(12,4) | NO | Unit price excl. VAT |
| xml_unit_price_vat | NUMERIC(12,4) | YES | Unit price incl. VAT |
| xml_total_price | NUMERIC(12,2) | NO | Total excl. VAT |
| xml_total_price_vat | NUMERIC(12,2) | YES | Total incl. VAT |
| xml_vat_rate | NUMERIC(5,2) | YES | VAT rate |

### NEX Genesis Enrichment
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| nex_product_id | INTEGER | YES | NEX product ID |
| nex_product_modify_id | INTEGER | YES | NEX modify ID |
| nex_product_name | VARCHAR(255) | YES | Product name from NEX |
| nex_product_category_id | INTEGER | YES | Category ID |
| nex_ean | VARCHAR(20) | YES | EAN from NEX |
| nex_plu | INTEGER | YES | PLU code |
| nex_stock_code | VARCHAR(20) | YES | Stock code |
| nex_stock_id | INTEGER | YES | Stock ID |
| nex_facility_id | INTEGER | YES | Facility ID |
| nex_purchase_price | NUMERIC(12,4) | YES | Purchase price |
| nex_sales_price | NUMERIC(12,4) | YES | Sales price |
| nex_category | INTEGER | YES | Category |
| nex_name | VARCHAR(255) | YES | Name from NEX |
| in_nex | BOOLEAN | YES | Exists in NEX |

### Matching Status
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| matched | BOOLEAN | YES | Is matched |
| matched_by | VARCHAR(20) | YES | Match method (ean/name/code) |
| match_confidence | NUMERIC(5,2) | YES | Confidence % |
| match_attempts | INTEGER | YES | Attempt count |
| matched_at | TIMESTAMPTZ | YES | Match timestamp |
| matched_by_user | VARCHAR(50) | YES | User who matched |

### User Edits
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| edited_product_name | VARCHAR(255) | YES | User-edited name |
| edited_quantity | NUMERIC(10,3) | YES | User-edited qty |
| edited_unit_price | NUMERIC(12,4) | YES | User-edited price |

### Timestamps
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| created_at | TIMESTAMPTZ | YES | Record created |
| updated_at | TIMESTAMPTZ | YES | Record updated |

## Indexes

- `idx_sih_customer_supplier` - (customer_code, supplier_code)
- `idx_sih_status` - status
- `idx_sih_issue_date` - xml_issue_date
- `idx_sii_head_id` - head_id
- `idx_sii_xml_ean` - xml_ean
- `idx_sii_matched` - matched

## Unique Constraints

- `uq_supplier_invoice` - (customer_code, supplier_code, xml_invoice_number)

## Migration History

- 2025-12-18: Initial schema (supplier-invoice-staging)
- 2025-01-27: ANDROS multi-tenant schema
- 2025-01-28: MAGERSTAV aligned to ANDROS schema
