# PAB.BTR + PANOTI.BTR → partner_catalog_texts

**Súbor:** PANOTI-partner_catalog_texts.md  
**Verzia:** 1.0  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-11  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**Btrieve súbory:** 
- PAB00000.BTR (Partner Address Book) - pole PABOwner
- PANOTI.BTR (Partner Notes) - poznámkové riadky evidenčnej karty

**PostgreSQL tabuľka:** `partner_catalog_texts`  
**Účel:** Univerzálna tabuľka pre všetky textové polia partnerov s podporou viacjazyčnosti a viacerých riadkov.

**Typy textov:**
- `owner_name` - majiteľ/konateľ spoločnosti (1 riadok na partnera)
- `description` - popis partnera (1 riadok na partnera)
- `notice` - poznámky k partnerovi (N riadkov na partnera)

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
CREATE TABLE partner_catalog_texts (
    -- Primárny kľúč
    id SERIAL PRIMARY KEY,
    
    -- FK na partnera
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Typ textu
    text_type VARCHAR(20) NOT NULL,  -- 'owner_name', 'description', 'notice'
    
    -- Poradové číslo riadku (pre viacriadkové texty)
    line_number INTEGER DEFAULT 0,
    
    -- Text
    text TEXT,
    
    -- Jazyk
    language VARCHAR(5) DEFAULT 'sk',
    
    -- Audit polia
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT unique_partner_text_line UNIQUE (partner_id, text_type, line_number, language),
    CONSTRAINT check_text_type CHECK (text_type IN ('owner_name', 'description', 'notice')),
    CONSTRAINT check_line_number CHECK (line_number >= 0),
    CONSTRAINT check_language CHECK (language IN ('sk', 'en', 'cz', 'de', 'hu'))
);

-- Indexy pre vyhľadávanie
CREATE INDEX idx_partner_texts_partner ON partner_catalog_texts(partner_id);
CREATE INDEX idx_partner_texts_type ON partner_catalog_texts(partner_id, text_type);
CREATE INDEX idx_partner_texts_language ON partner_catalog_texts(language);

-- Trigger pre updated_at
CREATE TRIGGER update_partner_texts_updated_at
    BEFORE UPDATE ON partner_catalog_texts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 3. MAPPING POLÍ

### 3.1 Mapovanie z PAB.BTR (owner_name)

| Btrieve pole | PostgreSQL pole | Hodnota | Poznámka |
|--------------|-----------------|---------|----------|
| PaCode | partner_id | Lookup | FK na partner_catalog |
| PABOwner | text | Direct | Majiteľ/konateľ |
| - | text_type | Fixed | 'owner_name' |
| - | line_number | Fixed | 0 |
| - | language | Fixed | 'sk' |

### 3.2 Mapovanie z PANOTI.BTR (notice)

| Btrieve pole | PostgreSQL pole | Hodnota | Poznámka |
|--------------|-----------------|---------|----------|
| PaCode | partner_id | Lookup | FK na partner_catalog |
| LinNum | line_number | Direct | Poradové číslo riadku |
| Notice | text | Direct | Text poznámky (Str250 → TEXT) |
| - | text_type | Fixed | 'notice' |
| - | language | Fixed | 'sk' |

### 3.3 Polia ktoré SA NEPRENÁŠAJÚ

**Žiadne** - všetky polia z Btrieve sa prenášajú.

---

## 4. BIZNIS LOGIKA

### 4.1 Typy textov

**owner_name** (1 riadok na partnera)
- Majiteľ alebo konateľ spoločnosti
- `line_number = 0` (vždy)
- Príklad: "Ing. Ján Nový"

**description** (1 riadok na partnera)
- Popis partnera, oblast činnosti
- `line_number = 0` (vždy)
- Príklad: "Veľkoobchod s potravinami"

**notice** (N riadkov na partnera)
- Poznámky, špeciálne požiadavky, história komunikácie
- `line_number = 1, 2, 3...`
- Príklady:
  - "VIP zákazník - prioritná doprava"
  - "Platí vždy načas"
  - "Kontakt: Ján Nový, +421 905 123 456"

### 4.2 Viacjazyčnosť

Každý text môže existovať vo viacerých jazykoch:

```sql
-- Slovenčina
partner_id=123, text_type='description', line_number=0, language='sk', text='Veľkoobchod s potravinami'

-- Angličtina
partner_id=123, text_type='description', line_number=0, language='en', text='Wholesale food supplier'
```

### 4.3 UNIQUE constraint

```sql
UNIQUE (partner_id, text_type, line_number, language)
```

**Znamená:**
- Partner môže mať len jeden 'owner_name' v slovenčine
- Partner môže mať 'owner_name' aj v angličtine
- Partner môže mať viacero 'notice' riadkov (line_number 1, 2, 3...)

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### 5.1 Incoming (z iných tabuliek)

```
partner_catalog (FK: partner_id)
    ↓
partner_catalog_texts
```

**ON DELETE CASCADE:** Pri vymazaní partnera sa vymažú všetky jeho textové polia.

### 5.2 Outgoing (do iných tabuliek)

**Žiadne** - toto je dátová tabuľka partnera.

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 CHECK Constraints

```sql
-- Povolené typy textov
CONSTRAINT check_text_type CHECK (text_type IN ('owner_name', 'description', 'notice'))

-- Poradové číslo >= 0
CONSTRAINT check_line_number CHECK (line_number >= 0)

-- Povolené jazyky
CONSTRAINT check_language CHECK (language IN ('sk', 'en', 'cz', 'de', 'hu'))

-- Unique kombinace
CONSTRAINT unique_partner_text_line UNIQUE (partner_id, text_type, line_number, language)
```

### 6.2 Povinné polia

```sql
partner_id NOT NULL
text_type NOT NULL
line_number DEFAULT 0
language DEFAULT 'sk'
```

---

## 7. QUERY PATTERNS

### 7.1 Získať owner_name partnera

```sql
SELECT text AS owner_name
FROM partner_catalog_texts
WHERE partner_id = 123
  AND text_type = 'owner_name'
  AND language = 'sk';
```

### 7.2 Získať všetky poznámky partnera

```sql
SELECT 
    line_number,
    text AS notice_text
FROM partner_catalog_texts
WHERE partner_id = 123
  AND text_type = 'notice'
  AND language = 'sk'
ORDER BY line_number;
```

### 7.3 Získať všetky textové polia partnera

```sql
SELECT 
    text_type,
    line_number,
    text,
    language
FROM partner_catalog_texts
WHERE partner_id = 123
ORDER BY text_type, line_number;
```

### 7.4 Partner s owner_name (JOIN)

```sql
SELECT 
    p.partner_number,
    p.partner_name,
    pt.text AS owner_name
FROM partner_catalog p
LEFT JOIN partner_catalog_texts pt 
    ON p.partner_id = pt.partner_id 
    AND pt.text_type = 'owner_name'
    AND pt.language = 'sk'
WHERE p.partner_number = '12345';
```

### 7.5 Vyhľadávanie v poznámkach

```sql
-- Partneri s kľúčovým slovom v poznámkach
SELECT DISTINCT
    p.partner_number,
    p.partner_name,
    pt.text AS notice_text
FROM partner_catalog p
JOIN partner_catalog_texts pt ON p.partner_id = pt.partner_id
WHERE pt.text_type = 'notice'
  AND pt.text ILIKE '%VIP%'
ORDER BY p.partner_name;
```

### 7.6 Komplexný SELECT s textami

```sql
-- Partner s owner_name a poznámkami
SELECT 
    p.partner_number,
    p.partner_name,
    
    -- Owner name
    (SELECT text FROM partner_catalog_texts 
     WHERE partner_id = p.partner_id 
       AND text_type = 'owner_name' 
       AND language = 'sk' 
     LIMIT 1) AS owner_name,
    
    -- Počet poznámok
    (SELECT COUNT(*) FROM partner_catalog_texts 
     WHERE partner_id = p.partner_id 
       AND text_type = 'notice' 
       AND language = 'sk') AS notice_count

FROM partner_catalog p
WHERE p.partner_number = '12345';
```

---

## 8. PRÍKLAD DÁT

### 8.1 Owner name (z PAB.BTR)

```sql
-- Majiteľ/konateľ v slovenčine
INSERT INTO partner_catalog_texts (
    partner_id, text_type, line_number, text, language,
    created_by
) VALUES
    (1, 'owner_name', 0, 'Ing. Ján Nový', 'sk', 'migration'),
    (2, 'owner_name', 0, 'Mgr. Peter Varga', 'sk', 'migration'),
    (3, 'owner_name', 0, 'Ing. Lukáš Horný, PhD.', 'sk', 'migration');
```

### 8.2 Description (nové v NEX Automat)

```sql
-- Popis partnera v slovenčine a angličtine
INSERT INTO partner_catalog_texts (
    partner_id, text_type, line_number, text, language,
    created_by
) VALUES
    (1, 'description', 0, 'Veľkoobchod s potravinami a nápojmi', 'sk', 'admin'),
    (1, 'description', 0, 'Wholesale food and beverage supplier', 'en', 'admin'),
    
    (2, 'description', 0, 'Maloobchodná sieť so spotrebnou elektronikou', 'sk', 'admin'),
    (2, 'description', 0, 'Retail chain for consumer electronics', 'en', 'admin');
```

### 8.3 Notices (z PANOTI.BTR)

```sql
-- Poznámky k partnerom (viacero riadkov)
INSERT INTO partner_catalog_texts (
    partner_id, text_type, line_number, text, language,
    created_by
) VALUES
    -- Partner 1 - ABC Veľkoobchod
    (1, 'notice', 1, 'VIP zákazník - prioritná doprava', 'sk', 'migration'),
    (1, 'notice', 2, 'Platí vždy načas, 14 dní splatnosť', 'sk', 'migration'),
    (1, 'notice', 3, 'Kontakt: Ján Nový, +421 905 123 456', 'sk', 'migration'),
    (1, 'notice', 4, 'Dôležité: Doručovať len do centrálneho skladu', 'sk', 'migration'),
    
    -- Partner 2 - XYZ Retail
    (2, 'notice', 1, 'Odber len na objednávku', 'sk', 'migration'),
    (2, 'notice', 2, 'Osobný odber v Košiciach', 'sk', 'migration'),
    
    -- Partner 3 - Global Trading
    (3, 'notice', 1, 'Medzinárodný partner - faktúry v EUR', 'sk', 'migration'),
    (3, 'notice', 2, 'Export do ČR - potrebné CLO dokumenty', 'sk', 'migration'),
    (3, 'notice', 3, 'Kontakt: Lukáš Horný, lukash@global-trading.sk', 'sk', 'migration');
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### 9.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. partner_catalog (Btrieve: PAB00000.BTR)       -- Hlavná tabuľka
2. partner_catalog_texts                         -- TÁTO TABUĽKA
   a) owner_name z PAB00000.BTR
   b) notice z PANOTI.BTR
```

### 9.2 Python príklad transformácie

```python
from btrieve import Btrieve
import psycopg2

def migrate_partner_texts_owner():
    """
    Migrácia owner_name z PAB00000.BTR
    """
    pab = Btrieve('C:/NEX/DATA/PAB00000.BTR')
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Migrácia PAB.PABOwner → partner_catalog_texts (owner_name)")
    
    for record in pab.records():
        # Lookup partner_id podľa PaCode
        pa_code = record.get('PaCode', 0)
        
        # Najprv nájdeme partner_id z partner_number
        partner_number = str(pa_code)  # alebo iná transformácia
        
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (partner_number,))
        
        result = cur.fetchone()
        if not result:
            continue
        
        partner_id = result[0]
        
        # Owner name
        owner_name = record.get('PABOwner', '').strip()
        
        if owner_name:
            cur.execute("""
                INSERT INTO partner_catalog_texts (
                    partner_id, text_type, line_number, text, language,
                    created_by, updated_by
                ) VALUES (
                    %s, 'owner_name', 0, %s, 'sk', 'migration', 'migration'
                )
                ON CONFLICT (partner_id, text_type, line_number, language) 
                DO UPDATE SET 
                    text = EXCLUDED.text,
                    updated_by = 'migration',
                    updated_at = CURRENT_TIMESTAMP
            """, (partner_id, owner_name))
            
            print(f"Partner {partner_number}: owner_name = {owner_name}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Migrácia owner_name dokončená")

def migrate_partner_texts_notices():
    """
    Migrácia poznámok z PANOTI.BTR
    """
    panoti = Btrieve('C:/NEX/DATA/PANOTI.BTR')
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Migrácia PANOTI.BTR → partner_catalog_texts (notice)")
    
    for record in panoti.records():
        # Lookup partner_id podľa PaCode
        pa_code = record.get('PaCode', 0)
        partner_number = str(pa_code)
        
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (partner_number,))
        
        result = cur.fetchone()
        if not result:
            print(f"Partner {partner_number} neexistuje, preskakujem.")
            continue
        
        partner_id = result[0]
        
        # Line number a text
        line_number = record.get('LinNum', 0)
        notice_text = record.get('Notice', '').strip()
        
        if notice_text:
            cur.execute("""
                INSERT INTO partner_catalog_texts (
                    partner_id, text_type, line_number, text, language,
                    created_by, updated_by
                ) VALUES (
                    %s, 'notice', %s, %s, 'sk', 'migration', 'migration'
                )
                ON CONFLICT (partner_id, text_type, line_number, language) 
                DO UPDATE SET 
                    text = EXCLUDED.text,
                    updated_by = 'migration',
                    updated_at = CURRENT_TIMESTAMP
            """, (partner_id, line_number, notice_text))
            
            print(f"Partner {partner_number}, line {line_number}: {notice_text}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Migrácia notice dokončená")

# Spustenie migrácie
if __name__ == '__main__':
    # Krok 1: Owner names z PAB.BTR
    migrate_partner_texts_owner()
    
    # Krok 2: Notices z PANOTI.BTR
    migrate_partner_texts_notices()
```

### 9.3 Dôležité poznámky

1. **PaCode mapping:**
   - Zistiť presný formát PaCode (longint)
   - Overiť ako sa mapuje na partner_number (VARCHAR)
   - Použiť rovnakú logiku ako pri partner_catalog_facilities

2. **line_number pre owner_name:**
   - Vždy `line_number = 0`
   - Jeden riadok na partnera

3. **line_number pre notice:**
   - Z Btrieve pole LinNum
   - Zachovať poradie (1, 2, 3...)

4. **Notice pole Str250:**
   - V PANOTI.BTR je Notice Str250 (dlhší text ako v starých verziách)
   - PostgreSQL TEXT pole nemá limit

5. **ON CONFLICT DO UPDATE:**
   - Umožňuje re-run migrácie
   - Aktualizuje existujúce záznamy

6. **Audit polia:**
   - Pri migrácii: `created_by = 'migration'`, `updated_by = 'migration'`
   - Pri manuálnom pridaní: username používateľa

7. **Budúce rozšírenia:**
   - Pridať ďalšie text_type podľa potreby: 'internal_note', 'delivery_instruction'...
   - Rozšíriť jazyky podľa potreby

---

## 10. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_facilities** → `PASUBC-partner_catalog_facilities.md`

---

## 11. VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Komplexná SQL schéma s viacjazyčnosťou
- Mapping z PAB.BTR (owner_name) a PANOTI.BTR (notice)
- Query patterns a príklady
- Python migračný script

---

**Koniec dokumentu partner_catalog_texts.md**