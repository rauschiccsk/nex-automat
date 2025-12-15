# PAYLST.BTR → payment_methods

**Kategória:** Catalogs - Číselníky  
**NEX Genesis:** PAYLST.BTR  
**NEX Automat:** `payment_methods`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj

**NEX Genesis (Btrieve):**
- PAYLST.BTR = číselník foriem úhrady faktúr
- Identifikácia len cez textový kód (PayCode: "HOT", "KAR", "FAK"...)
- Duplikácia názvov v PAB.BTR (IcPayName, IsPayName)

**NEX Automat (PostgreSQL):**
- **payment_methods** - číselník platobných metód
- Pridané numerické ID (payment_method_id) pre konzistenciu
- Eliminácia duplikácie - názvy len v číselníku

**Účel:**
- Formy úhrady faktúr (hotovosť, karta, faktúra...)
- Referencované z partner_catalog_extensions
- Použité pri vytváraní faktúr a dokladov

---

## KOMPLEXNÁ SQL SCHÉMA

### payment_methods

**Tabuľka:** `payment_methods`  
**Popis:** Formy úhrady faktúr (hotovosť, karta, faktúra, prevodom...)

```sql
CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    
    -- Základné údaje
    payment_method_code VARCHAR(10) UNIQUE NOT NULL,
    payment_method_name VARCHAR(100) NOT NULL,
    
    -- Príznaky
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit záznamu
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_methods_code ON payment_methods(payment_method_code);
CREATE INDEX idx_payment_methods_active ON payment_methods(is_active) WHERE is_active = TRUE;

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_payment_methods_updated_at
    BEFORE UPDATE ON payment_methods
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Popis |
|---------------|-----|---|-------------------|-----|-------|
| - | - | → | payment_method_id | SERIAL | **NOVÉ!** Numerické ID (1, 2, 3...) |
| PayCode | Str3 | → | payment_method_code | VARCHAR(10) | Kód metódy ("HOT", "KAR"...) |
| PayName | Str20 | → | payment_method_name | VARCHAR(100) | Názov metódy |
| ModUser | Str8 | → | created_by, updated_by | VARCHAR(30) | Audit |
| ModDate, ModTime | Date+Time | → | created_at, updated_at | TIMESTAMP | Audit |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Typ | Dôvod neprenášania |
|---------------|-----|--------------------|
| _PayName | Str20 | Vyhľadávacie pole - PostgreSQL full-text search |

---

## BIZNIS LOGIKA

### 1. Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
```sql
payment_method_id SERIAL PRIMARY KEY  -- 1, 2, 3, 4...
```

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**PayCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre API integrácie

### 2. Typické platobné metódy

| Kód | Názov | Použitie |
|-----|-------|----------|
| HOT | Hotovosť | Okamžitá platba v hotovosti |
| KAR | Platobná karta | Okamžitá platba kartou |
| FAK | Faktúra | Odložená platba (splatnosť) |
| PRE | Prevodom | Bankový prevod |
| ZAL | Zálohová faktúra | Platba vopred |
| DOB | Dobierka | Platba pri doručení |

### 3. Použitie v partner_catalog_extensions

```sql
-- Zákaznícka platobná metóda
customer_payment_method_id INTEGER 
FOREIGN KEY REFERENCES payment_methods(payment_method_id)

-- Dodávateľská platobná metóda
supplier_payment_method_id INTEGER
FOREIGN KEY REFERENCES payment_methods(payment_method_id)
```

---

## VZŤAHY S INÝMI TABUĽKAMI

### payment_methods ← partner_catalog_extensions

```sql
-- Partneri s platbou kartou
SELECT 
    pc.partner_name,
    pm.payment_method_name,
    pce.customer_payment_term_days
FROM partner_catalog pc
INNER JOIN partner_catalog_extensions pce ON pc.partner_id = pce.partner_id
INNER JOIN payment_methods pm ON pce.customer_payment_method_id = pm.payment_method_id
WHERE pm.payment_method_code = 'KAR';
```

### payment_methods ← invoices (BEZ FK!)

```sql
-- Faktúry s platobnou metódou
-- ARCHÍVNY DOKUMENT - payment_method_id môže byť NULL!
SELECT 
    i.invoice_number,
    i.payment_method_name,  -- denormalizované
    pm.payment_method_name AS current_name
FROM invoices i
LEFT JOIN payment_methods pm ON i.payment_method_id = pm.payment_method_id;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Unikátny kód

```sql
payment_method_code VARCHAR(10) UNIQUE NOT NULL
```

### 2. Povinné polia

```sql
payment_method_code NOT NULL
payment_method_name NOT NULL
```

---

## QUERY PATTERNS

### Zoznam aktívnych platobných metód

```sql
SELECT 
    payment_method_id,
    payment_method_code,
    payment_method_name
FROM payment_methods
WHERE is_active = TRUE
ORDER BY payment_method_name;
```

### Získať payment_method_id z kódu

```sql
-- Pri migrácii: PayCode → payment_method_id
SELECT payment_method_id 
FROM payment_methods 
WHERE payment_method_code = 'HOT';
```

### Štatistika použitia platobných metód

```sql
SELECT 
    pm.payment_method_name,
    COUNT(DISTINCT pce.partner_id) AS customer_count,
    COUNT(DISTINCT pse.partner_id) AS supplier_count
FROM payment_methods pm
LEFT JOIN partner_catalog_extensions pce ON pm.payment_method_id = pce.customer_payment_method_id
LEFT JOIN partner_catalog_extensions pse ON pm.payment_method_id = pse.supplier_payment_method_id
GROUP BY pm.payment_method_name
ORDER BY customer_count DESC;
```

---

## PRÍKLAD DÁT

```sql
INSERT INTO payment_methods (payment_method_code, payment_method_name, created_by) VALUES
('HOT', 'Hotovosť', 'admin'),
('KAR', 'Platobná karta', 'admin'),
('FAK', 'Faktúra', 'admin'),
('PRE', 'Prevodom', 'admin'),
('ZAL', 'Zálohová faktúra', 'admin'),
('DOB', 'Dobierka', 'admin'),
('CHE', 'Šekom', 'admin'),
('INK', 'Inkaso', 'admin');
```

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Generovanie payment_method_id

```python
# PAYLST.BTR → payment_methods
# payment_method_id sa automaticky generuje (SERIAL)

# Krok 1: Načítať všetky záznamy z PAYLST.BTR
paylst_records = read_btrieve_file('PAYLST.BTR')

# Krok 2: INSERT do PostgreSQL
for record in paylst_records:
    cursor.execute("""
        INSERT INTO payment_methods (
            payment_method_code,
            payment_method_name,
            created_by,
            created_at,
            updated_by,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        record['PayCode'],
        record['PayName'],
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime']),
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime'])
    ))
```

### 2. Vytvorenie mapping dictionary

```python
# Po migrácii PAYLST → payment_methods
# Vytvoríme dictionary pre rýchle mapovanie

payment_methods_map = {}
cursor.execute("SELECT payment_method_id, payment_method_code FROM payment_methods")
for row in cursor.fetchall():
    payment_methods_map[row['payment_method_code']] = row['payment_method_id']

# Použitie pri migrácii PAB.BTR
customer_payment_method_id = payment_methods_map.get(record['IcPayCode'])
supplier_payment_method_id = payment_methods_map.get(record['IsPayCode'])
```

### 3. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **PAYLST.BTR** → payment_methods
2. ✅ Vytvoriť mapping dictionary (PayCode → payment_method_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_extensions (použiť mapping)

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_extensions** → `PAB-partner_catalog.md`
- **invoices** → ⏳ Todo (archívne dokumenty)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** ✅ Pripravené na review