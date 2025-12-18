# Supplier Invoice Staging - Database Schema

**Category:** specifications
**Created:** 2025-12-18

## Database: supplier_invoice_staging

### Convention
- `xml_*` = Fields from ISDOC XML (immutable, source data)
- `nex_*` = Fields from NEX Genesis (enrichment/matching)

## Table: supplier_invoice_heads

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| xml_invoice_number | VARCHAR(50) | Invoice number from XML |
| xml_variable_symbol | VARCHAR(10) | Variable symbol |
| xml_issue_date | DATE | Issue date |
| xml_tax_point_date | DATE | Tax point date |
| xml_due_date | DATE | Due date |
| xml_currency | VARCHAR(3) | Currency (default EUR) |
| xml_supplier_ico | VARCHAR(20) | Supplier ICO |
| xml_supplier_name | VARCHAR(255) | Supplier name |
| xml_supplier_dic | VARCHAR(20) | Supplier DIC |
| xml_supplier_ic_dph | VARCHAR(20) | Supplier IC DPH |
| xml_iban | VARCHAR(34) | IBAN from XML |
| xml_swift | VARCHAR(20) | SWIFT from XML |
| xml_total_without_vat | DECIMAL(15,2) | Total without VAT |
| xml_total_vat | DECIMAL(15,2) | VAT amount |
| xml_total_with_vat | DECIMAL(15,2) | Total with VAT |
| nex_supplier_id | INTEGER | NEX Genesis supplier ID |
| nex_supplier_modify_id | INTEGER | NEX modify ID |
| nex_iban | VARCHAR(34) | IBAN from NEX |
| nex_swift | VARCHAR(20) | SWIFT from NEX |
| nex_stock_id | INTEGER | Default stock ID |
| nex_book_num | INTEGER | Accounting book number |
| nex_payment_method_id | INTEGER | Payment method |
| nex_price_list_id | INTEGER | Price list ID |
| status | VARCHAR(20) | pending/matched/approved/imported |
| item_count | INTEGER | Number of items (auto-calculated) |
| items_matched | INTEGER | Matched items count (auto-calculated) |
| match_percent | DECIMAL(5,2) | Match percentage (auto-calculated) |
| validation_status | VARCHAR(20) | Validation status |
| validation_errors | TEXT | Validation error messages |
| xml_file_path | VARCHAR(500) | Path to XML file |
| pdf_file_path | VARCHAR(500) | Path to PDF file |
| created_at | TIMESTAMP | Created timestamp |
| updated_at | TIMESTAMP | Updated timestamp (auto) |
| processed_at | TIMESTAMP | Processing timestamp |
| imported_at | TIMESTAMP | Import to NEX timestamp |
| nex_document_id | BIGINT | NEX document ID after import |

### Indexes
- `idx_sih_supplier_ico` - xml_supplier_ico
- `idx_sih_invoice_number` - xml_invoice_number
- `idx_sih_status` - status
- `idx_sih_issue_date` - xml_issue_date
- `idx_sih_nex_supplier` - nex_supplier_id

### Unique Constraint
- `uq_supplier_invoice` - (xml_supplier_ico, xml_invoice_number)

## Table: supplier_invoice_items

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| invoice_head_id | INTEGER FK | Reference to heads |
| xml_line_number | INTEGER | Line number from XML |
| xml_product_name | VARCHAR(255) | Product name from XML |
| xml_seller_code | VARCHAR(50) | Seller's product code |
| xml_ean | VARCHAR(20) | EAN barcode |
| xml_quantity | DECIMAL(10,3) | Quantity |
| xml_unit | VARCHAR(10) | Unit of measure |
| xml_unit_price | DECIMAL(12,4) | Unit price excl. VAT |
| xml_total_price | DECIMAL(12,2) | Total price excl. VAT |
| xml_unit_price_vat | DECIMAL(12,4) | Unit price incl. VAT |
| xml_total_price_vat | DECIMAL(12,2) | Total price incl. VAT |
| xml_vat_rate | DECIMAL(5,2) | VAT rate |
| nex_product_id | INTEGER | NEX product ID |
| nex_product_modify_id | INTEGER | NEX modify ID |
| nex_product_name | VARCHAR(255) | Product name from NEX |
| nex_product_category_id | INTEGER | NEX category ID |
| nex_ean | VARCHAR(20) | EAN from NEX |
| nex_stock_code | VARCHAR(20) | Stock code |
| nex_stock_id | INTEGER | Stock ID |
| nex_facility_id | INTEGER | Facility ID |
| nex_purchase_price | DECIMAL(12,4) | Purchase price from NEX |
| nex_sales_price | DECIMAL(12,4) | Sales price from NEX |
| matched | BOOLEAN | Is matched flag |
| matched_by | VARCHAR(20) | Match method (ean/name/code) |
| match_confidence | DECIMAL(5,2) | Match confidence % |
| match_attempts | INTEGER | Number of match attempts |
| validation_status | VARCHAR(20) | Item validation status |
| validation_errors | TEXT | Item validation errors |
| edited_product_name | VARCHAR(255) | User-edited name |
| edited_quantity | DECIMAL(10,3) | User-edited quantity |
| edited_unit_price | DECIMAL(12,4) | User-edited price |
| created_at | TIMESTAMP | Created timestamp |
| updated_at | TIMESTAMP | Updated timestamp (auto) |
| matched_at | TIMESTAMP | Match timestamp |
| matched_by_user | VARCHAR(50) | User who matched |

### Indexes
- `idx_sii_invoice_head` - invoice_head_id
- `idx_sii_xml_ean` - xml_ean
- `idx_sii_xml_seller_code` - xml_seller_code
- `idx_sii_nex_product` - nex_product_id
- `idx_sii_matched` - matched

### Triggers
- `tr_sih_updated_at` - Auto-update updated_at on heads
- `tr_sii_updated_at` - Auto-update updated_at on items
- `tr_sii_update_head_stats` - Auto-calculate item_count, items_matched, match_percent

## SQL File Location
`apps/supplier-invoice-staging/database/schemas/001_supplier_invoice_staging.sql`