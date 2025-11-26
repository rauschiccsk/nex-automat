# NEX Genesis - Terminology Dictionary

**Project:** NEX Automat  
**Version:** 1.0  
**Created:** 2025-11-26  
**Language:** Slovak (SK) → English (EN)

---

## Overview

This document defines the official English terminology for NEX Genesis ERP modules. All NEX Automat development should use these standardized terms for consistency.

**Total:** 8 Subsystems, 31 Modules

---

## Subsystems Summary

| # | Code Prefix | SK | EN |
|---|-------------|----|----|
| 1 | MASTER- | Všeobecné číselníky | Master Data |
| 2 | STK- | Skladové hospodárstvo | Stock Management |
| 3 | PROD- | Výroba tovaru a polotovaru | Production Management |
| 4 | PROC- | Obstarávanie tovaru | Procurement |
| 5 | PRICE- | Tvorba predajných cien | Sales Price Management |
| 6 | SALES- | Predaj tovaru (odbyt) | Sales Management |
| 7 | FIN- | Finančné účtovníctvo | Financial Management |
| 8 | ACC- | Podvojné účtovníctvo | General Ledger Accounting |

---

## 1. Master Data (MASTER-)

**SK:** Všeobecné číselníky  
**EN:** Master Data  
**Description:** Core reference data shared across all system modules.

| Code | SK | EN | Description |
|------|----|----|-------------|
| USER-MGMT | Evidencia používateľov systému | System User Management | Registration and management of system users - login name, password, first name and last name. Access rights are managed separately. |
| USER-ACCESS | Správa prístupových práv používateľov | User Access Rights Management | Group-based access control. Rights are defined for groups, then groups are assigned to users. User can have multiple groups. Permission levels: VIEW (access module), CREATE (add records), UPDATE (modify records), DELETE (remove records). |
| EMPLOYEES | Katalóg vlastných zamestnancov | Employee Catalog | Registry of company employees - name, surname, job position, HR notes. GDPR protected. |
| PRODUCTS | Katalóg produktov a služieb | Product and Service Catalog | Master catalog of products and services containing permanent (rarely changing) data: product classification into groups, identification codes (PLU, EAN, etc.), VAT group, unit of measure, and other static attributes. Does not contain prices or stock information. |
| PARTNERS | Katalóg obchodných partnerov | Business Partner Catalog | Master catalog of business partners - both suppliers and customers. Contains permanent (rarely changing) data: company identification (ID, VAT number), addresses, contacts, bank accounts, and other static attributes. |

---

## 2. Stock Management (STK-)

**SK:** Skladové hospodárstvo  
**EN:** Stock Management  
**Description:** Warehouse and inventory operations management.

| Code | SK | EN | Description |
|------|----|----|-------------|
| STK-INFO | Skladové karty zásob | Stock Information Center | Comprehensive information hub for stock items - current stock levels, customer order reservations, FIFO cards and their status, stock movements history, quantities on order from suppliers, and dozens of other stock-related data points. |
| STK-RECEIPT-INT | Interné skladové príjemky | Internal Stock Receipts | Internal documents for receiving goods into stock without supplier delivery - inventory surplus, found goods outside inventory count. |
| STK-ISSUE-INT | Interné skladové výdajky | Internal Stock Issues | Internal documents for issuing goods from stock without customer sale - inventory shortage, own consumption, damaged goods disposal. |
| STK-TRANSFER-WH | Medziskladový presun | Inter-Warehouse Transfer | Transfer of goods between warehouses within the same location/branch. |
| STK-TRANSFER-BR | Medziprevádzkový presun | Inter-Branch Transfer | Transfer of goods to another branch located at a different address. |
| STK-REPACK | Prebalenie tovaru | Stock Repackaging | Transfer of goods from one stock card to another with quantity ratio conversion (X:Y). Used for repackaging, splitting, or combining products. |

---

## 3. Production Management (PROD-)

**SK:** Výroba tovaru a polotovaru  
**EN:** Production Management  
**Description:** Manufacturing and assembly operations.

| Code | SK | EN | Description |
|------|----|----|-------------|
| PROD-ASSEMBLY | Kompletizácia výrobkov | Product Assembly | Assembly of product bundles from existing items without production work - gift baskets, promotional packages, holiday bundles (e.g., St. Nicholas gift packs). |
| PROD-MANUFACTURE | Vlastná výroba | In-House Production | Production of goods involving labor/work processes - cooking, manufacturing, processing raw materials into finished or semi-finished products. |

---

## 4. Procurement (PROC-)

**SK:** Obstarávanie tovaru  
**EN:** Procurement  
**Description:** Supplier-side purchasing and goods receiving.

| Code | SK | EN | Description |
|------|----|----|-------------|
| PROC-PO | Dodávateľské objednávky | Supplier Purchase Orders | Orders placed to suppliers for goods procurement. |
| PROC-DN | Dodávateľské dodacie listy | Supplier Delivery Notes | Delivery documents from suppliers serving as stock receipts for incoming goods. |
| PROC-INV | Dodávateľské faktúry | Supplier Invoices | Invoices received from suppliers for delivered goods or services. |

---

## 5. Sales Price Management (PRICE-)

**SK:** Tvorba predajných cien  
**EN:** Sales Price Management  
**Description:** Management of all forms of sales pricing.

| Code | SK | EN | Description |
|------|----|----|-------------|
| PRICE-LIST | Predajné cenníky | Sales Price Lists | Management of sales price lists for products and services. Unlimited number of price lists supported (e.g., for different customer groups). |
| PRICE-CHANGE | Požiadavky na zmeny predajných cien | Price Change Requests | Workflow for sales price change proposals. Operators without price change authority submit requests, supervisor with authority approves. Used in NEX Automat supplier-invoice-editor when margin adjustment requires price change. |
| PRICE-PROMO | Správa akciových cien | Promotional Price Management | Management of promotional/discounted prices - time-limited special offers with validity period (from-to). Promotional prices have priority over standard price lists. |
| PRICE-ETAG | Správa elektronických cenoviek | Electronic Price Tag Management | Management of electronic shelf labels (ESL) - hardware integration with digital price displays in store. |

---

## 6. Sales Management (SALES-)

**SK:** Predaj tovaru (odbyt)  
**EN:** Sales Management  
**Description:** Customer-side sales and order fulfillment.

| Code | SK | EN | Description |
|------|----|----|-------------|
| SALES-ORD | Zákaznícke objednávky | Customer Orders | Orders received from customers (e.g., e-shop orders, phone orders). |
| SALES-DN | Odberateľské dodacie listy | Customer Delivery Notes | Delivery documents for customers serving as stock issues for outgoing goods. |
| SALES-INV | Odberateľské faktúry | Customer Invoices | Invoices issued to customers for delivered goods or services. |
| SALES-ECR | Elektronické registračné pokladnice | Electronic Cash Registers | Point of sale (POS) system - electronic cash registers for retail sales. |

---

## 7. Financial Management (FIN-)

**SK:** Finančné účtovníctvo  
**EN:** Financial Management  
**Description:** Cash and banking operations.

| Code | SK | EN | Description |
|------|----|----|-------------|
| FIN-BANK | Evidencia bankových výpisov | Bank Statement Records | Recording and processing of bank account statements. |
| FIN-PAYMENT | Evidencia prevodných príkazov | Payment Orders | Management of outgoing payment orders to suppliers and other parties. |
| FIN-CASH | Evidencia hotovostných dokladov | Cash Documents | Recording of cash transactions (receipts and disbursements) outside of retail cash registers - petty cash management. |

---

## 8. General Ledger Accounting (ACC-)

**SK:** Podvojné účtovníctvo  
**EN:** General Ledger Accounting  
**Description:** Double-entry bookkeeping and financial reporting.

| Code | SK | EN | Description |
|------|----|----|-------------|
| ACC-SYNTH | Evidencia syntetických účtov | Synthetic Accounts | Management of synthetic (main) accounts in the chart of accounts. |
| ACC-ANALYT | Evidencia analytických účtov | Analytical Accounts | Management of analytical (sub) accounts - detailed breakdown of synthetic accounts. |
| ACC-JOURNAL | Denník účtovných zápisov | Accounting Journal | Chronological record of all accounting entries (debits and credits). |
| ACC-LEDGER | Hlavná kniha účtov | General Ledger | Main ledger containing all account balances and transactions organized by account. |
| ACC-REPORTS | Účtovné výkazy | Financial Statements | Accounting reports - trial balance, balance sheet, profit and loss statement (income statement). |
| ACC-INTERNAL | Interné účtovné doklady | Internal Accounting Documents | Internal documents for accounting entries not originating from external transactions (e.g., accruals, adjustments, corrections). |
| ACC-FIXED-ASSET | Evidencia investičného majetku | Fixed Asset Records | Management of fixed/capital assets - acquisition, depreciation, disposal. |
| ACC-MINOR-ASSET | Evidencia drobného majetku | Minor Asset Records | Management of low-value/minor assets - items below fixed asset threshold but still tracked. |

---

## Quick Reference - All Modules

| Code | EN Name |
|------|---------|
| **Master Data** | |
| USER-MGMT | System User Management |
| USER-ACCESS | User Access Rights Management |
| EMPLOYEES | Employee Catalog |
| PRODUCTS | Product and Service Catalog |
| PARTNERS | Business Partner Catalog |
| **Stock Management** | |
| STK-INFO | Stock Information Center |
| STK-RECEIPT-INT | Internal Stock Receipts |
| STK-ISSUE-INT | Internal Stock Issues |
| STK-TRANSFER-WH | Inter-Warehouse Transfer |
| STK-TRANSFER-BR | Inter-Branch Transfer |
| STK-REPACK | Stock Repackaging |
| **Production Management** | |
| PROD-ASSEMBLY | Product Assembly |
| PROD-MANUFACTURE | In-House Production |
| **Procurement** | |
| PROC-PO | Supplier Purchase Orders |
| PROC-DN | Supplier Delivery Notes |
| PROC-INV | Supplier Invoices |
| **Sales Price Management** | |
| PRICE-LIST | Sales Price Lists |
| PRICE-CHANGE | Price Change Requests |
| PRICE-PROMO | Promotional Price Management |
| PRICE-ETAG | Electronic Price Tag Management |
| **Sales Management** | |
| SALES-ORD | Customer Orders |
| SALES-DN | Customer Delivery Notes |
| SALES-INV | Customer Invoices |
| SALES-ECR | Electronic Cash Registers |
| **Financial Management** | |
| FIN-BANK | Bank Statement Records |
| FIN-PAYMENT | Payment Orders |
| FIN-CASH | Cash Documents |
| **General Ledger Accounting** | |
| ACC-SYNTH | Synthetic Accounts |
| ACC-ANALYT | Analytical Accounts |
| ACC-JOURNAL | Accounting Journal |
| ACC-LEDGER | General Ledger |
| ACC-REPORTS | Financial Statements |
| ACC-INTERNAL | Internal Accounting Documents |
| ACC-FIXED-ASSET | Fixed Asset Records |
| ACC-MINOR-ASSET | Minor Asset Records |

---

## Usage Guidelines

### Naming Conventions

**For NEX Automat modules:**
```
nex-automat-{subsystem}-{module}

Examples:
- nex-automat-proc-inv       (Supplier Invoices automation)
- nex-automat-sales-ord      (Customer Orders automation)
- nex-automat-fin-bank       (Bank Statements automation)
- nex-automat-acc-reports    (Financial Statements automation)
```

**For code references:**
```python
# Use Code as constant
MODULE_PROC_INV = "PROC-INV"
MODULE_SALES_ORD = "SALES-ORD"

# Use EN name in documentation
"""Automates Supplier Invoices processing"""
```

### Translation Rules

1. Always use EN terms in:
   - Code (variable names, function names, class names)
   - API endpoints
   - Database table/column names
   - Technical documentation
   - Git commit messages

2. Use SK terms only in:
   - User interface (if Slovak UI required)
   - End-user documentation
   - Customer communication

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-26 | Zoltán Rausch / Claude | Initial version - 8 subsystems, 31 modules |

---

**End of Document**