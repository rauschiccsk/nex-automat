# PAYJRN → payment_journal

**Verzia:** 1.1  
**Dátum:** 2025-12-15  
**Batch:** 6 (Accounting - dokument 3/3)  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Účel
Denník úhrady faktúr (Payment Journal) je **univerzálny denník** pre evidenciu úhrad dodávateľských aj odberateľských faktúr. Obsahuje všetky typy platieb:
- Bankové úhrady (zo všetkých účtov)
- Hotovostné úhrady (registračná pokladňa)
- Hotovostné úhrady (podniková pokladňa)
- Prevodné príkazy

### Btrieve súbor
- **Názov:** PAYJRN.BTR (single file)
- **Umiestnenie:** `C:\NEX\YEARACT\LEDGER\PAYJRN.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\LEDGER\`
- **Účel:** Univerzálny denník úhrad všetkých faktúr
- **Architektúra:** Single file (nie multi-file ako ISH/ISI)

### PostgreSQL migrácia
**Nový systém (NEX Automat):**
```
payment_journal - jedna tabuľka pre všetky platby
```

### Kľúčová vlastnosť: SPOLOČNÝ DENNÍK ⭐

**Denník obsahuje platby z rôznych dokladov:**
- BV (Bank Statement) - bankový výpis
- PP (Cash Receipt) - pokladničný príjem
- PV (Cash Withdrawal) - pokladničný výdaj
- PQ (Payment Order) - prevodný príkaz

**Denník obsahuje úhrady rôznych typov faktúr:**
- S (Supplier) - dodávateľské faktúry
- C (Customer) - odberateľské faktúry

### Vzťahy
```
payment_journal
    ├──> supplier_invoice_heads (cez invoice_number, invoice_type='S')
    ├──> customer_invoice_heads (cez invoice_number, invoice_type='C')
    ├──> bank_statement_heads (cez payment_document_number, typ BV)
    ├──> cash_receipt_heads (cez payment_document_number, typ PP)
    ├──> cash_withdrawal_heads (cez payment_document_number, typ PV)
    └──> payment_order_heads (cez payment_document_number, typ PQ)
```

### Kľúčové entity
- **Platobný doklad:** payment_document_number (BV2500100123, PP2500100001...)
- **Faktúra:** invoice_number + invoice_type (DF2500000123, OF2500000456...)
- **Partner:** partner_id (len pre filtrovanie)

---

## KONCEPT SÚHRNNEJ PLATBY ⭐

### Príklad: Špedičná firma

**Scenár:**
Špedičná firma doručí balíky pre 10 zákazníkov, inkasuje hotovosť u každého zákazníka, na náš účet pošle všetko jednou sumou (1000 EUR) + zoznam faktúr.

**V bankovom výpise:**
```
BV2500100123, riadok 1 = 1000 EUR od SPEDITÉR s.r.o.
```

**V PAYJRN:**
```
DocNum=BV2500100123, ItmNum=1, CitNum=0  → HLAVIČKA (1000 EUR celkom)
DocNum=BV2500100123, ItmNum=1, CitNum=1  → faktúra OF001 (100 EUR)
DocNum=BV2500100123, ItmNum=1, CitNum=2  → faktúra OF002 (150 EUR)
DocNum=BV2500100123, ItmNum=1, CitNum=3  → faktúra OF003 (80 EUR)
...
DocNum=BV2500100123, ItmNum=1, CitNum=10 → faktúra OF010 (50 EUR)
                                           ─────────────────────
                                           SPOLU: 1000 EUR
```

### Pravidlá CitNum (detail_number)

**CitNum = 0:**
- Hlavička súhrnnej platby (suma všetkých faktúr)
- ALEBO riadna platba (jedna faktúra = CitNum 0)

**CitNum > 0:**
- Detail súhrnnej platby (konkrétna faktúra)
- CitNum 1, 2, 3... = poradie faktúr v súhrnnej platbe

### Riadna platba vs Súhrnná platba

**Riadna platba (jedna faktúra):**
```
DocNum=BV2500100123, ItmNum=2, CitNum=0  → 500 EUR, faktúra DF2500000123
```

**Súhrnná platba (viac faktúr):**
```
DocNum=BV2500100123, ItmNum=3, CitNum=0  → HLAVIČKA (800 EUR celkom)
DocNum=BV2500100123, ItmNum=3, CitNum=1  → faktúra OF020 (300 EUR)
DocNum=BV2500100123, ItmNum=3, CitNum=2  → faktúra OF021 (500 EUR)
```

---

## MAPPING POLÍ

### Platobný doklad

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocNum | Str12 | payment_document_number | VARCHAR(13) | BV2500100123, PP2500100001... |
| ItmNum | word | line_number | INTEGER | Riadok v doklade |
| CitNum | word | detail_number | INTEGER | 0=hlavička/riadna, >0=detail |

### Platobné symboly

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| VarSym | Str15 | variable_symbol | VARCHAR(15) |
| SpcSym | Str20 | specific_symbol | VARCHAR(20) |
| ConSym | Str4 | constant_symbol | VARCHAR(4) |

### Základné údaje

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PayDte | DateType | payment_date | DATE | Dátum úhrady |
| ParNum | longint | partner_id | INTEGER | Len pre filtrovanie |
| ParNam, _ParNam | - | - | - | Snapshot, neprenášame |
| PayIba | Str25 | counterparty_iban | VARCHAR(25) | IBAN protiúčtu |
| PayDes | Str60 | payment_description | VARCHAR(60) | Textový popis |

### Úhrada

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PayDvz | Str3 | payment_currency | VARCHAR(3) | Mena účtu |
| PayCrs | double | payment_rate | DECIMAL(15,6) | Kurz úhrady |
| PayCdt | DateType | rate_date | DATE | Dátum kurzu |
| PayVal | double | payment_amount | DECIMAL(15,2) | Hodnota v mene účtu |
| PayAcv | double | posted_amount_ac | DECIMAL(15,2) | Zaúčtovaná hodnota |

### Faktúra

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| InvDoc | Str12 | invoice_number | VARCHAR(13) | DF2500000123, OF2500000456 |
| InvTyp | Str1 | invoice_type | VARCHAR(1) | S=Supplier, C=Customer |
| InvDvz | Str3 | invoice_currency | VARCHAR(3) | Mena faktúry |
| InvVal | double | invoice_amount | DECIMAL(15,2) | Hodnota v mene faktúry |
| InvCrs | double | invoice_rate | DECIMAL(15,6) | Kurz faktúry |
| InvAcv | double | invoice_amount_ac | DECIMAL(15,2) | Hodnota v účt. mene |

### Audit
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUsr | Str10 | created_by | VARCHAR(8) | - |
| CrtDte + CrtTim | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUsr | Str10 | updated_by | VARCHAR(8) | - |
| ModDte + ModTim | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### NEPRENESENÉ POLIA

**Snapshot partnera:**
- ParNam, _ParNam (názov partnera)

**Kurzové rozdiely:**
- PdvAcv, CdvAcv

**Prevádzkové údaje:**
- WriNum, DocYer, EcuNum

**Mená užívateľov:**
- CrtUsn, ModUsn

**Zastaralé:**
- PayCon (číslo účtu - namiesto IBAN)

---

## BIZNIS LOGIKA

### Typy platieb

**1. Riadna platba (jedna faktúra):**
```sql
SELECT *
FROM payment_journal
WHERE payment_document_number = 'BV2500100123'
  AND line_number = 2
  AND detail_number = 0;

-- Výsledok:
-- payment_amount = 500 EUR
-- invoice_number = 'DF2500000123'
-- invoice_type = 'S'
```

**2. Súhrnná platba (viac faktúr):**
```sql
-- Hlavička
SELECT *
FROM payment_journal
WHERE payment_document_number = 'BV2500100123'
  AND line_number = 1
  AND detail_number = 0;

-- Výsledok:
-- payment_amount = 1000 EUR
-- invoice_number = NULL (hlavička)

-- Detail
SELECT *
FROM payment_journal
WHERE payment_document_number = 'BV2500100123'
  AND line_number = 1
  AND detail_number > 0
ORDER BY detail_number;

-- Výsledok:
-- detail_number=1, invoice_number='OF001', invoice_amount=100
-- detail_number=2, invoice_number='OF002', invoice_amount=150
-- ...
-- detail_number=10, invoice_number='OF010', invoice_amount=50
```

### Validácia súhrnnej platby

```python
def validate_summary_payment(
    payment_document_number: str,
    line_number: int
):
    """
    Validuj súhrnnú platbu - suma detailov = suma hlavičky.
    """
    # Hlavička
    header = db.query("""
        SELECT payment_amount
        FROM payment_journal
        WHERE payment_document_number = %s
          AND line_number = %s
          AND detail_number = 0
    """, [payment_document_number, line_number]).first()
    
    # Detail
    details_sum = db.query("""
        SELECT SUM(invoice_amount)
        FROM payment_journal
        WHERE payment_document_number = %s
          AND line_number = %s
          AND detail_number > 0
    """, [payment_document_number, line_number]).scalar()
    
    if abs(header.payment_amount - details_sum) > 0.01:
        raise ValueError(
            f"Suma detailov ({details_sum}) != suma hlavičky ({header.payment_amount})"
        )
```

### Aktualizácia total_paid v faktúre

```python
def update_invoice_total_paid(invoice_number: str, invoice_type: str):
    """
    Aktualizuj total_paid_ac v hlavičke faktúry.
    """
    # Spočítaj všetky úhrady tejto faktúry
    total_paid = db.query("""
        SELECT SUM(invoice_amount_ac)
        FROM payment_journal
        WHERE invoice_number = %s
          AND invoice_type = %s
          AND detail_number > 0  -- Len detaily, nie hlavičky!
    """, [invoice_number, invoice_type]).scalar() or 0
    
    # Aktualizuj faktúru
    if invoice_type == 'S':
        db.execute("""
            UPDATE supplier_invoice_heads
            SET total_paid_ac = %s,
                remaining_ac = purchase_total_value_ac - %s
            WHERE document_number = %s
        """, [total_paid, total_paid, invoice_number])
    elif invoice_type == 'C':
        db.execute("""
            UPDATE customer_invoice_heads
            SET total_paid_ac = %s,
                remaining_ac = sales_total_value_ac - %s
            WHERE document_number = %s
        """, [total_paid, total_paid, invoice_number])
```

### Typ platobného dokladu

```python
def get_payment_document_type(payment_document_number: str) -> str:
    """
    Zisti typ platobného dokladu z čísla.
    
    Returns:
        'BV' = Bank Statement
        'PP' = Cash Receipt
        'PV' = Cash Withdrawal
        'PQ' = Payment Order
    """
    return payment_document_number[0:2]

# Príklad
doc_type = get_payment_document_type('BV2500100123')
# doc_type = 'BV'
```

---

## VZŤAHY S INÝMI TABUĽKAMI

### Reference na faktúry

```sql
-- Dodávateľské faktúry
payment_journal (N) ──> (1) supplier_invoice_heads
    WHERE invoice_type = 'S'

-- Odberateľské faktúry
payment_journal (N) ──> (1) customer_invoice_heads
    WHERE invoice_type = 'C'
```

**POZNÁMKA:** Foreign key NIE JE definovaný (rôzne tabuľky podľa invoice_type).

### Reference na partnera

```sql
-- Partner (len pre filtrovanie)
payment_journal (N) ──> (1) partner_catalog
    ON DELETE RESTRICT
```

### Reference na platobné doklady

```sql
-- Podľa typu dokladu (BV, PP, PV, PQ)
-- Reference NIE JE definovaný (rôzne tabuľky podľa typu)
```

---

## PRÍKLAD DÁT

### Riadna platba

```sql
INSERT INTO payment_journal (
    payment_document_number, line_number, detail_number,
    variable_symbol, payment_date,
    partner_id, counterparty_iban,
    payment_currency, payment_amount, posted_amount_ac,
    invoice_number, invoice_type, invoice_currency, invoice_amount, invoice_amount_ac,
    created_by, created_at
) VALUES (
    'BV2500100123', 1, 0,
    '2025000456', '2025-01-20',
    456, 'SK1234567890123456789012',
    'EUR', 1815.00, 1815.00,
    'DF2500000123', 'S', 'EUR', 1815.00, 1815.00,
    'zoltan', '2025-01-20 10:00:00'
);
```

### Súhrnná platba

```sql
-- Hlavička
INSERT INTO payment_journal (
    payment_document_number, line_number, detail_number,
    payment_date, partner_id,
    payment_currency, payment_amount, posted_amount_ac,
    payment_description,
    created_by, created_at
) VALUES (
    'BV2500100123', 2, 0,
    '2025-01-20', 789,
    'EUR', 1000.00, 1000.00,
    'Súhrnná platba od SPEDITÉR s.r.o.',
    'zoltan', '2025-01-20 10:00:00'
);

-- Detail
INSERT INTO payment_journal (
    payment_document_number, line_number, detail_number,
    payment_date, partner_id,
    payment_currency, payment_amount,
    invoice_number, invoice_type, invoice_currency, invoice_amount, invoice_amount_ac,
    created_by, created_at
) VALUES 
-- Faktúra 1
('BV2500100123', 2, 1,
 '2025-01-20', 789,
 'EUR', 1000.00,
 'OF2500000100', 'C', 'EUR', 300.00, 300.00,
 'zoltan', '2025-01-20 10:00:00'),

-- Faktúra 2
('BV2500100123', 2, 2,
 '2025-01-20', 789,
 'EUR', 1000.00,
 'OF2500000101', 'C', 'EUR', 450.00, 450.00,
 'zoltan', '2025-01-20 10:00:00'),

-- Faktúra 3
('BV2500100123', 2, 3,
 '2025-01-20', 789,
 'EUR', 1000.00,
 'OF2500000102', 'C', 'EUR', 250.00, 250.00,
 'zoltan', '2025-01-20 10:00:00');
```

---

## MIGRÁCIA

### Jednoduchá migrácia

```python
def migrate_payment_journal_record(record):
    """
    Migruj záznam z PAYJRN.BTR do PostgreSQL.
    """
    insert_payment_journal(
        payment_document_number=record.DocNum,
        line_number=record.ItmNum,
        detail_number=record.CitNum,
        
        # Platobné symboly
        variable_symbol=record.VarSym if record.VarSym else None,
        specific_symbol=record.SpcSym if record.SpcSym else None,
        constant_symbol=record.ConSym if record.ConSym else None,
        
        # Základné údaje
        payment_date=record.PayDte,
        partner_id=record.ParNum if record.ParNum else None,
        counterparty_iban=record.PayIba if record.PayIba else None,
        payment_description=record.PayDes if record.PayDes else None,
        
        # Úhrada
        payment_currency=record.PayDvz,
        payment_rate=record.PayCrs if record.PayCrs else None,
        rate_date=record.PayCdt if record.PayCdt else None,
        payment_amount=record.PayVal,
        posted_amount_ac=record.PayAcv if record.PayAcv else None,
        
        # Faktúra
        invoice_number=record.InvDoc if record.InvDoc else None,
        invoice_type=record.InvTyp if record.InvTyp else None,
        invoice_currency=record.InvDvz if record.InvDvz else None,
        invoice_amount=record.InvVal if record.InvVal else None,
        invoice_rate=record.InvCrs if record.InvCrs else None,
        invoice_amount_ac=record.InvAcv if record.InvAcv else None,
        
        # Audit
        created_by=record.CrtUsr[:8],  # Max 8 znakov
        created_at=combine_datetime(record.CrtDte, record.CrtTim),
        updated_by=record.ModUsr[:8] if record.ModUsr else None,
        updated_at=combine_datetime(record.ModDte, record.ModTim) if record.ModDte else None
    )
```

### Validácia po migrácii

```sql
-- Kontrola počtu záznamov
SELECT COUNT(*) AS total_records
FROM payment_journal;

-- Kontrola unikátnosti
SELECT payment_document_number, line_number, detail_number, COUNT(*)
FROM payment_journal
GROUP BY payment_document_number, line_number, detail_number
HAVING COUNT(*) > 1;

-- Kontrola súhrnných platieb
SELECT 
    payment_document_number,
    line_number,
    SUM(CASE WHEN detail_number = 0 THEN payment_amount ELSE 0 END) AS header_total,
    SUM(CASE WHEN detail_number > 0 THEN invoice_amount ELSE 0 END) AS details_total,
    SUM(CASE WHEN detail_number = 0 THEN payment_amount ELSE 0 END) - 
    SUM(CASE WHEN detail_number > 0 THEN invoice_amount ELSE 0 END) AS difference
FROM payment_journal
WHERE EXISTS (
    SELECT 1 FROM payment_journal p2
    WHERE p2.payment_document_number = payment_journal.payment_document_number
      AND p2.line_number = payment_journal.line_number
      AND p2.detail_number > 0
)
GROUP BY payment_document_number, line_number
HAVING ABS(
    SUM(CASE WHEN detail_number = 0 THEN payment_amount ELSE 0 END) - 
    SUM(CASE WHEN detail_number > 0 THEN invoice_amount ELSE 0 END)
) > 0.01;

-- Kontrola referencií na faktúry
SELECT 
    p.invoice_type,
    COUNT(*) AS total_payments,
    COUNT(DISTINCT p.invoice_number) AS unique_invoices
FROM payment_journal p
WHERE p.detail_number > 0  -- Len detaily
GROUP BY p.invoice_type;
```

---

## POZNÁMKY PRE MIGRÁCIU

### Kľúčové body

1. **SPOLOČNÝ DENNÍK:**
   - Obsahuje platby z rôznych dokladov (BV, PP, PV, PQ)
   - Obsahuje úhrady dodávateľských aj odberateľských faktúr

2. **Single file architektúra:**
   - `PAYJRN.BTR` → jedna tabuľka `payment_journal`
   - Nie multi-file ako ISH/ISI

3. **detail_number = 0:**
   - Hlavička súhrnnej platby (invoice_number = NULL)
   - ALEBO riadna platba (invoice_number != NULL)

4. **detail_number > 0:**
   - Detail súhrnnej platby (konkrétne faktúry)

5. **Validácia súhrnnej platby:**
   - Suma detailov musí byť rovná sume hlavičky

6. **Aktualizácia faktúr:**
   - Po vložení platby aktualizovať total_paid_ac v faktúre

7. **Partner:**
   - Len pre filtrovanie, nie versioning

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `supplier_invoice_heads` - dodávateľské faktúry
- `customer_invoice_heads` - odberateľské faktúry
- `partner_catalog` - partneri (len pre filtrovanie)

**Súvisiace dokumenty:**
- `BV-bank_statement_heads.md` - bankové výpisy
- `PP-cash_receipt_heads.md` - pokladničné príjmy
- `PV-cash_withdrawal_heads.md` - pokladničné výdaje
- `PQ-payment_order_heads.md` - prevodné príkazy

---

**Koniec dokumentu PAYJRN-payment_journal.md v1.1**