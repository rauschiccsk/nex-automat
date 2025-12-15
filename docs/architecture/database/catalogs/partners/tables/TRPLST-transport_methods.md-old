# TRPLST.BTR → transport_methods

**Kategória:** Catalogs - Číselníky  
**NEX Genesis:** TRPLST.BTR  
**NEX Automat:** `transport_methods`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj

**NEX Genesis (Btrieve):**
- TRPLST.BTR = číselník spôsobov dopravy
- Identifikácia len cez textový kód (TrsCode: "KUR", "OSO", "POS"...)
- Duplikácia názvov v PAB.BTR (IcTrsName, IsTrsName)

**NEX Automat (PostgreSQL):**
- **transport_methods** - číselník dopravných metód
- Pridané numerické ID (transport_method_id) pre konzistenciu
- Eliminácia duplikácie - názvy len v číselníku

**Účel:**
- Spôsoby dopravy tovaru (kuriér, osobný odber, pošta...)
- Referencované z partner_catalog_extensions
- Použité pri vytváraní príjemiek a výdajok

---

## KOMPLEXNÁ SQL SCHÉMA

### transport_methods

**Tabuľka:** `transport_methods`  
**Popis:** Spôsoby dopravy tovaru (kuriér, osobný odber, pošta...)

```sql
CREATE TABLE transport_methods (
    transport_method_id SERIAL PRIMARY KEY,
    
    -- Základné údaje
    transport_method_code VARCHAR(10) UNIQUE NOT NULL,
    transport_method_name VARCHAR(100) NOT NULL,
    
    -- Príznaky
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit záznamu
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transport_methods_code ON transport_methods(transport_method_code);
CREATE INDEX idx_transport_methods_active ON transport_methods(is_active) WHERE is_active = TRUE;

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_transport_methods_updated_at
    BEFORE UPDATE ON transport_methods
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Popis |
|---------------|-----|---|-------------------|-----|-------|
| - | - | → | transport_method_id | SERIAL | **NOVÉ!** Numerické ID (1, 2, 3...) |
| TrsCode | Str3 | → | transport_method_code | VARCHAR(10) | Kód metódy ("KUR", "OSO"...) |
| TrsName | Str30 | → | transport_method_name | VARCHAR(100) | Názov metódy |
| ModUser | Str8 | → | created_by, updated_by | VARCHAR(30) | Audit |
| ModDate, ModTime | Date+Time | → | created_at, updated_at | TIMESTAMP | Audit |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Typ | Dôvod neprenášania |
|---------------|-----|--------------------|
| _TrsName | Str20 | Vyhľadávacie pole - PostgreSQL full-text search |
| Sended | byte | Sync flag - zastaralé |

---

## BIZNIS LOGIKA

### 1. Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
```sql
transport_method_id SERIAL PRIMARY KEY  -- 1, 2, 3, 4...
```

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**TrsCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre API integrácie

### 2. Typické dopravné metódy

| Kód | Názov | Použitie |
|-----|-------|----------|
| KUR | Kuriér | Kuriérska služba (GLS, DPD...) |
| OSO | Osobný odber | Vyzdvihnutie na sklade |
| POS | Poštou | Slovenská pošta |
| DOP | Vlastná doprava | Dovoz vlastným autom |
| ZAS | Zásielkovňa | Packeta, Zásielkovňa.sk |
| EXP | Expresná zásielka | Expresné doručenie do 24h |

### 3. Použitie v partner_catalog_extensions

```sql
-- Zákaznícka dopravná metóda
customer_transport_method_id INTEGER 
FOREIGN KEY REFERENCES transport_methods(transport_method_id)

-- Dodávateľská dopravná metóda
supplier_transport_method_id INTEGER
FOREIGN KEY REFERENCES transport_methods(transport_method_id)
```

---

## VZŤAHY S INÝMI TABUĽKAMI

### transport_methods ← partner_catalog_extensions

```sql
-- Partneri s kuriérskou dopravou
SELECT 
    pc.partner_name,
    tm.transport_method_name
FROM partner_catalog pc
INNER JOIN partner_catalog_extensions pce ON pc.partner_id = pce.partner_id
INNER JOIN transport_methods tm ON pce.customer_transport_method_id = tm.transport_method_id
WHERE tm.transport_method_code = 'KUR';
```

### transport_methods ← receipt_documents (BEZ FK!)

```sql
-- Príjemky s dopravnou metódou
-- ARCHÍVNY DOKUMENT - transport_method_id môže byť NULL!
SELECT 
    r.receipt_number,
    r.transport_method_name,  -- denormalizované
    tm.transport_method_name AS current_name
FROM receipt_documents r
LEFT JOIN transport_methods tm ON r.transport_method_id = tm.transport_method_id;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Unikátny kód

```sql
transport_method_code VARCHAR(10) UNIQUE NOT NULL
```

### 2. Povinné polia

```sql
transport_method_code NOT NULL
transport_method_name NOT NULL
```

---

## QUERY PATTERNS

### Zoznam aktívnych dopravných metód

```sql
SELECT 
    transport_method_id,
    transport_method_code,
    transport_method_name
FROM transport_methods
WHERE is_active = TRUE
ORDER BY transport_method_name;
```

### Získať transport_method_id z kódu

```sql
-- Pri migrácii: TrsCode → transport_method_id
SELECT transport_method_id 
FROM transport_methods 
WHERE transport_method_code = 'KUR';
```

### Štatistika použitia dopravných metód

```sql
SELECT 
    tm.transport_method_name,
    COUNT(DISTINCT pce.partner_id) AS customer_count,
    COUNT(DISTINCT pse.partner_id) AS supplier_count
FROM transport_methods tm
LEFT JOIN partner_catalog_extensions pce ON tm.transport_method_id = pce.customer_transport_method_id
LEFT JOIN partner_catalog_extensions pse ON tm.transport_method_id = pse.supplier_transport_method_id
GROUP BY tm.transport_method_name
ORDER BY customer_count DESC;
```

---

## PRÍKLAD DÁT

```sql
INSERT INTO transport_methods (transport_method_code, transport_method_name, created_by) VALUES
('KUR', 'Kuriér', 'admin'),
('OSO', 'Osobný odber', 'admin'),
('POS', 'Poštou', 'admin'),
('DOP', 'Vlastná doprava', 'admin'),
('ZAS', 'Zásielkovňa', 'admin'),
('EXP', 'Expresná zásielka', 'admin'),
('PAL', 'Paletová preprava', 'admin');
```

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Generovanie transport_method_id

```python
# TRPLST.BTR → transport_methods
# transport_method_id sa automaticky generuje (SERIAL)

# Krok 1: Načítať všetky záznamy z TRPLST.BTR
trplst_records = read_btrieve_file('TRPLST.BTR')

# Krok 2: INSERT do PostgreSQL
for record in trplst_records:
    cursor.execute("""
        INSERT INTO transport_methods (
            transport_method_code,
            transport_method_name,
            created_by,
            created_at,
            updated_by,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        record['TrsCode'],
        record['TrsName'],
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime']),
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime'])
    ))
```

### 2. Vytvorenie mapping dictionary

```python
# Po migrácii TRPLST → transport_methods
# Vytvoríme dictionary pre rýchle mapovanie

transport_methods_map = {}
cursor.execute("SELECT transport_method_id, transport_method_code FROM transport_methods")
for row in cursor.fetchall():
    transport_methods_map[row['transport_method_code']] = row['transport_method_id']

# Použitie pri migrácii PAB.BTR
customer_transport_method_id = transport_methods_map.get(record['IcTrsCode'])
supplier_transport_method_id = transport_methods_map.get(record['IsTrsCode'])
```

### 3. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **TRPLST.BTR** → transport_methods
2. ✅ Vytvoriť mapping dictionary (TrsCode → transport_method_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_extensions (použiť mapping)

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_extensions** → `PAB-partner_catalog.md`
- **receipt_documents** → ⏳ Todo (skladové doklady)
- **issue_documents** → ⏳ Todo (skladové doklady)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** ✅ Pripravené na review