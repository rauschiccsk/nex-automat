# NEX Genesis - Terminologický Slovník

**Vytvorené:** 2025-11-26  
**Aktualizované:** 2025-12-13  
**Status:** 📖 Referenčný dokument  
**Verzia:** 1.1

---

## Účel Dokumentu

Tento dokument definuje oficiálnu anglickú terminológiu pre moduly NEX Genesis ERP. Všetok vývoj NEX Automat by mal používať tieto štandardizované termíny pre konzistentnosť.

**Celkovo:** 8 Subsystémov, 31 Modulov

---

## Súvisiace Dokumenty

- [CODING_STANDARDS.md](CODING_STANDARDS.md) - Štandardy kódu
- [DOCUMENT_TYPES.md](../documents/DOCUMENT_TYPES.md) - Typy dokladov
- [DATABASE_INDEX.md](../database/DATABASE_INDEX.md) - Databázová dokumentácia
- [APPLICATIONS_INDEX.md](../applications/APPLICATIONS_INDEX.md) - Aplikácie

---

## Prehľad Subsystémov

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
**Popis:** Základné referenčné dáta zdieľané naprieč všetkými modulmi systému.

| Code | SK | EN | Popis |
|------|----|----|-------|
| USER-MGMT | Evidencia používateľov systému | System User Management | Registrácia a správa používateľov systému - login, heslo, meno a priezvisko. Prístupové práva sa spravujú samostatne. |
| USER-ACCESS | Správa prístupových práv používateľov | User Access Rights Management | Skupinová správa prístupových práv. Práva sa definujú pre skupiny, potom sa skupiny priraďujú používateľom. Používateľ môže mať viacero skupín. Úrovne oprávnení: VIEW (prístup do modulu), CREATE (pridanie záznamov), UPDATE (úprava záznamov), DELETE (odstránenie záznamov). |
| EMPLOYEES | Katalóg vlastných zamestnancov | Employee Catalog | Register zamestnancov spoločnosti - meno, priezvisko, pracovná pozícia, HR poznámky. GDPR chránené. |
| PRODUCTS | Katalóg produktov a služieb | Product and Service Catalog | Hlavný katalóg produktov a služieb obsahujúci stále (zriedkavo sa meniace) údaje: klasifikácia produktov do skupín, identifikačné kódy (PLU, EAN, atď.), DPH skupina, merná jednotka a ďalšie statické atribúty. Neobsahuje ceny ani skladové informácie. |
| PARTNERS | Katalóg obchodných partnerov | Business Partner Catalog | Hlavný katalóg obchodných partnerov - dodávatelia aj zákazníci. Obsahuje stále (zriedkavo sa meniace) údaje: identifikácia spoločnosti (IČO, DIČ), adresy, kontakty, bankové účty a ďalšie statické atribúty. |

**Databázové dokumenty:**
- [GSCAT-product_catalog.md](../database/catalogs/) - Katalóg produktov
- [PAB-partner_catalog.md](../database/catalogs/) - Katalóg partnerov

---

## 2. Stock Management (STK-)

**SK:** Skladové hospodárstvo  
**EN:** Stock Management  
**Popis:** Správa skladov a inventárnych operácií.

| Code | SK | EN | Popis |
|------|----|----|-------|
| STK-INFO | Skladové karty zásob | Stock Information Center | Komplexné informačné centrum pre skladové položky - aktuálne stavy zásob, rezervácie zákazníckych objednávok, FIFO karty a ich stavy, história pohybov, množstvá na objednávke od dodávateľov a desiatky ďalších skladových údajov. |
| STK-RECEIPT-INT | Interné skladové príjemky | Internal Stock Receipts | Interné doklady pre príjem tovaru na sklad bez dodávateľskej dodávky - inventúrny prebytok, nájdený tovar mimo inventúry. |
| STK-ISSUE-INT | Interné skladové výdajky | Internal Stock Issues | Interné doklady pre výdaj tovaru zo skladu bez predaja zákazníkovi - inventúrny nedostatok, vlastná spotreba, likvidácia poškodeného tovaru. |
| STK-TRANSFER-WH | Medziskladový presun | Inter-Warehouse Transfer | Presun tovaru medzi skladmi v rámci toho istého miesta/pobočky. |
| STK-TRANSFER-BR | Medziprevádzkový presun | Inter-Branch Transfer | Presun tovaru do inej pobočky na inej adrese. |
| STK-REPACK | Prebalenie tovaru | Stock Repackaging | Presun tovaru z jednej skladovej karty na inú s prepočtom množstva (X:Y). Používa sa pre prebaľovanie, delenie alebo kombinovanie produktov. |

**Databázové dokumenty:**
- [STK-stock_cards.md](../database/stock/cards/) - Skladové karty
- [STM-stock_card_movements.md](../database/stock/cards/) - Pohyby
- [FIF-stock_card_fifos.md](../database/stock/cards/) - FIFO karty

---

## 3. Production Management (PROD-)

**SK:** Výroba tovaru a polotovaru  
**EN:** Production Management  
**Popis:** Výrobné a montážne operácie.

| Code | SK | EN | Popis |
|------|----|----|-------|
| PROD-ASSEMBLY | Kompletizácia výrobkov | Product Assembly | Kompletizácia produktových balíkov z existujúcich položiek bez výrobnej práce - darčekové koše, akciové balíky, sviatočné balíky (napr. Mikulášske balíčky). |
| PROD-MANUFACTURE | Vlastná výroba | In-House Production | Výroba tovaru zahŕňajúca pracovné procesy - varenie, výroba, spracovanie surovín na hotové alebo polotovary. |

---

## 4. Procurement (PROC-)

**SK:** Obstarávanie tovaru  
**EN:** Procurement  
**Popis:** Nákup a príjem tovaru od dodávateľov.

| Code | SK | EN | Popis |
|------|----|----|-------|
| PROC-PO | Dodávateľské objednávky | Supplier Purchase Orders | Objednávky zadané dodávateľom pre nákup tovaru. |
| PROC-DN | Dodávateľské dodacie listy | Supplier Delivery Notes | Dodacie doklady od dodávateľov slúžiace ako skladové príjemky pre prichádzajúci tovar. |
| PROC-INV | Dodávateľské faktúry | Supplier Invoices | Faktúry prijaté od dodávateľov za dodaný tovar alebo služby. |

**Databázové dokumenty:**
- [TSH-supplier_delivery_heads.md](../database/stock/documents/) - Hlavičky DL
- [TSI-supplier_delivery_items.md](../database/stock/documents/) - Položky DL
- [ISH-supplier_invoice_heads.md](../database/accounting/) - Hlavičky faktúr
- [ISI-supplier_invoice_items.md](../database/accounting/) - Položky faktúr

**NEX Automat aplikácie:**
- [supplier-invoice-loader](../applications/supplier-invoice-loader/) - Automatizácia PROC-INV
- [supplier-invoice-staging](../applications/supplier-invoice-staging/) - Správa staging faktúr

---

## 5. Sales Price Management (PRICE-)

**SK:** Tvorba predajných cien  
**EN:** Sales Price Management  
**Popis:** Správa všetkých foriem predajného oceňovania.

| Code | SK | EN | Popis |
|------|----|----|-------|
| PRICE-LIST | Predajné cenníky | Sales Price Lists | Správa predajných cenníkov pre produkty a služby. Podporuje neobmedzený počet cenníkov (napr. pre rôzne skupiny zákazníkov). |
| PRICE-CHANGE | Požiadavky na zmeny predajných cien | Price Change Requests | Workflow pre návrhy zmien predajných cien. Operátori bez oprávnenia meniť ceny podávajú požiadavky, nadriadený s oprávnením schvaľuje. Používa sa v NEX Automat supplier-invoice-editor pri úprave marže vyžadujúcej zmenu ceny. |
| PRICE-PROMO | Správa akciových cien | Promotional Price Management | Správa akciových/zľavnených cien - časovo limitované špeciálne ponuky s platnosťou (od-do). Akciové ceny majú prioritu pred štandardnými cenníkmi. |
| PRICE-ETAG | Správa elektronických cenoviek | Electronic Price Tag Management | Správa elektronických regálových štítkov (ESL) - hardvérová integrácia s digitálnymi cenovými displejmi v predajni. |

**Databázové dokumenty:**
- [PLSnnnnn-price_list_items.md](../database/sales/) - Predajné cenníky

---

## 6. Sales Management (SALES-)

**SK:** Predaj tovaru (odbyt)  
**EN:** Sales Management  
**Popis:** Predaj a plnenie objednávok pre zákazníkov.

| Code | SK | EN | Popis |
|------|----|----|-------|
| SALES-ORD | Zákaznícke objednávky | Customer Orders | Objednávky prijaté od zákazníkov (napr. e-shop objednávky, telefónne objednávky). |
| SALES-DN | Odberateľské dodacie listy | Customer Delivery Notes | Dodacie doklady pre zákazníkov slúžiace ako skladové výdajky pre odchádzajúci tovar. |
| SALES-INV | Odberateľské faktúry | Customer Invoices | Faktúry vystavené zákazníkom za dodaný tovar alebo služby. |
| SALES-ECR | Elektronické registračné pokladnice | Electronic Cash Registers | Point of sale (POS) systém - elektronické registračné pokladnice pre maloobchodný predaj. |

---

## 7. Financial Management (FIN-)

**SK:** Finančné účtovníctvo  
**EN:** Financial Management  
**Popis:** Hotovostné a bankové operácie.

| Code | SK | EN | Popis |
|------|----|----|-------|
| FIN-BANK | Evidencia bankových výpisov | Bank Statement Records | Zaznamenávanie a spracovanie výpisov z bankových účtov. |
| FIN-PAYMENT | Evidencia prevod príkazov | Payment Orders | Správa odchádzajúcich platobných príkazov dodávateľom a iným stranám. |
| FIN-CASH | Evidencia hotovostných dokladov | Cash Documents | Zaznamenávanie hotovostných transakcií (príjmy a výdavky) mimo maloobchodných pokladníc - správa pokladne. |

**Databázové dokumenty:**
- [PAYJRN-payment_journal.md](../database/accounting/) - Platobný denník

---

## 8. General Ledger Accounting (ACC-)

**SK:** Podvojné účtovníctvo  
**EN:** General Ledger Accounting  
**Popis:** Podvojné účtovníctvo a finančné výkazníctvo.

| Code | SK | EN | Popis |
|------|----|----|-------|
| ACC-SYNTH | Evidencia syntetických účtov | Synthetic Accounts | Správa syntetických (hlavných) účtov v účtovej osnove. |
| ACC-ANALYT | Evidencia analytických účtov | Analytical Accounts | Správa analytických (pod)účtov - detailný rozpad syntetických účtov. |
| ACC-JOURNAL | Denník účtovných zápisov | Accounting Journal | Chronologický záznam všetkých účtovných zápisov (debety a kredity). |
| ACC-LEDGER | Hlavná kniha účtov | General Ledger | Hlavná kniha obsahujúca všetky účtové stavy a transakcie organizované podľa účtov. |
| ACC-REPORTS | Účtovné výkazy | Financial Statements | Účtovné reporty - obratová predvaha, súvaha, výkaz ziskov a strát. |
| ACC-INTERNAL | Interné účtovné doklady | Internal Accounting Documents | Interné doklady pre účtovné zápisy nepochádzajúce z externých transakcií (napr. časové rozlíšenie, úpravy, opravy). |
| ACC-FIXED-ASSET | Evidencia investičného majetku | Fixed Asset Records | Správa dlhodobého/investičného majetku - obstaranie, odpisovanie, vyradenie. |
| ACC-MINOR-ASSET | Evidencia drobného majetku | Minor Asset Records | Správa drobného majetku - položky pod prahom investičného majetku, ale stále sledované. |

---

## Rýchly Prehľad - Všetky Moduly

| Code | EN Name | SK Názov |
|------|---------|----------|
| **Master Data** | | **Všeobecné číselníky** |
| USER-MGMT | System User Management | Evidencia používateľov systému |
| USER-ACCESS | User Access Rights Management | Správa prístupových práv |
| EMPLOYEES | Employee Catalog | Katalóg zamestnancov |
| PRODUCTS | Product and Service Catalog | Katalóg produktov a služieb |
| PARTNERS | Business Partner Catalog | Katalóg obchodných partnerov |
| **Stock Management** | | **Skladové hospodárstvo** |
| STK-INFO | Stock Information Center | Skladové karty zásob |
| STK-RECEIPT-INT | Internal Stock Receipts | Interné skladové príjemky |
| STK-ISSUE-INT | Internal Stock Issues | Interné skladové výdajky |
| STK-TRANSFER-WH | Inter-Warehouse Transfer | Medziskladový presun |
| STK-TRANSFER-BR | Inter-Branch Transfer | Medziprevádzkový presun |
| STK-REPACK | Stock Repackaging | Prebalenie tovaru |
| **Production Management** | | **Výroba** |
| PROD-ASSEMBLY | Product Assembly | Kompletizácia výrobkov |
| PROD-MANUFACTURE | In-House Production | Vlastná výroba |
| **Procurement** | | **Obstarávanie** |
| PROC-PO | Supplier Purchase Orders | Dodávateľské objednávky |
| PROC-DN | Supplier Delivery Notes | Dodávateľské dodacie listy |
| PROC-INV | Supplier Invoices | Dodávateľské faktúry |
| **Sales Price Management** | | **Tvorba cien** |
| PRICE-LIST | Sales Price Lists | Predajné cenníky |
| PRICE-CHANGE | Price Change Requests | Požiadavky na zmeny cien |
| PRICE-PROMO | Promotional Price Management | Správa akciových cien |
| PRICE-ETAG | Electronic Price Tag Management | Správa elektronických cenoviek |
| **Sales Management** | | **Predaj** |
| SALES-ORD | Customer Orders | Zákaznícke objednávky |
| SALES-DN | Customer Delivery Notes | Odberateľské dodacie listy |
| SALES-INV | Customer Invoices | Odberateľské faktúry |
| SALES-ECR | Electronic Cash Registers | Elektronické pokladnice |
| **Financial Management** | | **Finančné účtovníctvo** |
| FIN-BANK | Bank Statement Records | Evidencia bankových výpisov |
| FIN-PAYMENT | Payment Orders | Evidencia platobných príkazov |
| FIN-CASH | Cash Documents | Evidencia hotovostných dokladov |
| **General Ledger Accounting** | | **Podvojné účtovníctvo** |
| ACC-SYNTH | Synthetic Accounts | Evidencia syntetických účtov |
| ACC-ANALYT | Analytical Accounts | Evidencia analytických účtov |
| ACC-JOURNAL | Accounting Journal | Denník účtovných zápisov |
| ACC-LEDGER | General Ledger | Hlavná kniha účtov |
| ACC-REPORTS | Financial Statements | Účtovné výkazy |
| ACC-INTERNAL | Internal Accounting Documents | Interné účtovné doklady |
| ACC-FIXED-ASSET | Fixed Asset Records | Evidencia investičného majetku |
| ACC-MINOR-ASSET | Minor Asset Records | Evidencia drobného majetku |

---

## Pravidlá Používania

### Konvencie Pomenovania

**Pre NEX Automat moduly:**
```
nex-automat-{subsystem}-{module}

Príklady:
- nex-automat-proc-inv       (Automatizácia dodávateľských faktúr)
- nex-automat-sales-ord      (Automatizácia zákazníckych objednávok)
- nex-automat-fin-bank       (Automatizácia bankových výpisov)
- nex-automat-acc-reports    (Automatizácia účtovných výkazov)
```

**Pre referencie v kóde:**
```python
# Použiť Code ako konštantu
MODULE_PROC_INV = "PROC-INV"
MODULE_SALES_ORD = "SALES-ORD"

# Použiť EN názov v dokumentácii
"""Automates Supplier Invoices processing"""
```

### Pravidlá Prekladu

**1. Vždy používať EN termíny v:**
- Kóde (názvy premenných, funkcií, tried)
- API endpointoch
- Databázových tabuľkách/stĺpcoch
- Technickej dokumentácii
- Git commit správach

**2. Používať SK termíny len v:**
- Používateľskom rozhraní (ak je požadované SK UI)
- Dokumentácii pre koncových používateľov
- Komunikácii so zákazníkom

### Príklady Použitia

**Databázové tabuľky:**
```sql
-- Správne
CREATE TABLE supplier_invoices ...
CREATE TABLE customer_orders ...

-- Nesprávne
CREATE TABLE dodavatelske_faktury ...
```

**Python triedy:**
```python
# Správne
class SupplierInvoice:
    pass

class CustomerOrder:
    pass

# Nesprávne
class DodavatelskáFaktúra:
    pass
```

**API endpointy:**
```
# Správne
POST /api/v1/supplier-invoices
GET /api/v1/customer-orders

# Nesprávne
POST /api/v1/dodavatelske-faktury
```

---

## História Dokumentu

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-11-26 | Zoltán Rausch / Claude | Prvá verzia - 8 subsystémov, 31 modulov |
| 1.1 | 2025-12-13 | Zoltán Rausch / Claude | Migrácia do novej štruktúry, pridané odkazy na DB docs a aplikácie |

---

**Vytvoril:** Zoltán Rausch & Claude AI  
**Naposledy aktualizované:** 2025-12-13  
**Status:** 📖 Aktívny referenčný dokument  
**Verzia:** 1.1