# PAGLST.BTR → partner_categories

**Súbor:** PAGLST-partner_categories.md  
**Verzia:** 1.0  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-11  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**Btrieve súbor:** PAGLST.BTR (Partner Groups List)  
**PostgreSQL tabuľka:** `partner_categories`  
**Účel:** Skupiny partnerov (primárne dodávatelia, rozšírené o odberateľov)

**Historický vývoj:**

**NEX Genesis (Btrieve):**
- ✅ PAGLST.BTR - číselník skupín dodávateľov
- ✅ PAB.BTR pole `PagCode` - odkaz na PAGLST.BTR
- ❌ PGCLST.BTR - **neexistuje** číselník pre odberateľov!
- ⚠️ PAB.BTR pole `PgcCode` - kód bez číselníka (len textová hodnota)

**NEX Automat (PostgreSQL):**
- ✅ Unifikovaný číselník `partner_categories`
- ✅ Podporuje 2 typy: `supplier` (dodávatelia), `customer` (odberatelia)
- ✅ Migrácia z PAGLST.BTR pre `category_type = 'supplier'`
- ✅ Manuálne naplnenie pre `category_type = 'customer'`

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
CREATE TABLE partner_categories (
    -- Primárny kľúč
    category_id SERIAL PRIMARY KEY,
    
    -- Typ kategórie
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('supplier', 'customer')),
    
    -- Základné údaje (Btrieve: PagCode, PagName)
    category_code VARCHAR(10) NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    category_description TEXT,
    
    -- Príznaky
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit záznamu (Btrieve: ModUser, ModDate, ModTime)
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraint
    CONSTRAINT unique_category_type_code UNIQUE (category_type, category_code)
);

-- Indexy
CREATE INDEX idx_partner_categories_type ON partner_categories(category_type);
CREATE INDEX idx_partner_categories_code ON partner_categories(category_type, category_code);
CREATE INDEX idx_partner_categories_active ON partner_categories(is_active) WHERE is_active = TRUE;

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_partner_categories_updated_at
    BEFORE UPDATE ON partner_categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 3. MAPPING POLÍ

### 3.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Identifikátory** |
| PagCode | category_code | Direct | Číslo skupiny (konvertované na VARCHAR) |
| PagName | category_name | Direct | Názov skupiny |
| **Audit údaje** |
| ModUser | updated_by | Direct | Užívateľ ktorý uložil |
| ModDate + ModTime | updated_at | Combine | Dátum a čas zmeny |
| **Nové polia** |
| - | category_type | New | Fixed: 'supplier' pre PAGLST.BTR |
| - | category_description | New | NULL (možno doplniť manuálne) |
| - | is_active | New | Default: TRUE |
| - | created_by | New | Same as updated_by |
| - | created_at | New | Same as updated_at |

### 3.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| _PagName | Vyhľadávacie pole - nie je potrebné (PostgreSQL má ILIKE) |

---

## 4. BIZNIS LOGIKA

### 4.1 Typy kategórií

**Supplier (Dodávateľ):**
- Migrované z PAGLST.BTR
- Skupiny dodávateľov podľa typu tovaru
- Napríklad: "Potraviny", "Elektronika", "Textil"

**Customer (Odberateľ):**
- **Nie sú v NEX Genesis** (číselník neexistoval)
- Manuálne naplnenie v NEX Automat
- Skupiny zákazníkov podľa typu obchodu
- Napríklad: "Maloobchod", "Veľkoobchod", "HoReCa"

### 4.2 Unique constraint

```sql
UNIQUE (category_type, category_code)
```

**Znamená:**
- Kód "001" môže existovať 2x:
  - `category_type = 'supplier'`, `category_code = '001'` (Skupina dodávateľov)
  - `category_type = 'customer'`, `category_code = '001'` (Skupina zákazníkov)

### 4.3 Použitie v PAB.BTR

**NEX Genesis:**
```
PAB.BTR → PagCode (WORD) → PAGLST.BTR → PagCode, PagName
PAB.BTR → PgcCode (WORD) → ❌ Bez číselníka!
```

**NEX Automat:**
```
partner_catalog → partner_catalog_categories → partner_categories
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### 5.1 Incoming (z iných tabuliek)

**Žiadne** - toto je číselník (master data).

### 5.2 Outgoing (do iných tabuliek)

```
partner_categories
    ↓
partner_catalog_categories (mapovacia tabuľka)
    ↓
partner_catalog
```

**ON DELETE RESTRICT:** Pri vymazaní kategórie sa nedovolí, ak je používaná v partner_catalog_categories.

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 CHECK Constraints

```sql
-- Povolené typy kategórií
CONSTRAINT CHECK (category_type IN ('supplier', 'customer'))

-- Unique kombinace typ + kód
CONSTRAINT unique_category_type_code UNIQUE (category_type, category_code)
```

### 6.2 Povinné polia

```sql
category_type NOT NULL
category_code NOT NULL
category_name NOT NULL
```

---

## 7. QUERY PATTERNS

### 7.1 Zoznam skupín dodávateľov

```sql
SELECT 
    category_code,
    category_name,
    category_description
FROM partner_categories
WHERE category_type = 'supplier'
  AND is_active = TRUE
ORDER BY category_code;
```

### 7.2 Zoznam skupín zákazníkov

```sql
SELECT 
    category_code,
    category_name,
    category_description
FROM partner_categories
WHERE category_type = 'customer'
  AND is_active = TRUE
ORDER BY category_code;
```

### 7.3 Všetky kategórie s počtom partnerov

```sql
SELECT 
    pcat.category_type,
    pcat.category_code,
    pcat.category_name,
    COUNT(pcc.partner_id) AS partner_count
FROM partner_categories pcat
LEFT JOIN partner_catalog_categories pcc ON pcat.category_id = pcc.category_id
GROUP BY pcat.category_id, pcat.category_type, pcat.category_code, pcat.category_name
ORDER BY pcat.category_type, pcat.category_code;
```

### 7.4 Partneri v danej kategórii

```sql
-- Dodávatelia v skupine "POT"
SELECT 
    p.partner_number,
    p.partner_name,
    pcat.category_name
FROM partner_catalog p
INNER JOIN partner_catalog_categories pcc ON p.partner_id = pcc.partner_id
INNER JOIN partner_categories pcat ON pcc.category_id = pcat.category_id
WHERE pcat.category_type = 'supplier'
  AND pcat.category_code = 'POT'
  AND p.is_active = TRUE
ORDER BY p.partner_name;
```

### 7.5 Štatistika partnerov podľa skupín

```sql
SELECT 
    pcat.category_type,
    pcat.category_code,
    pcat.category_name,
    COUNT(DISTINCT pcc.partner_id) AS partner_count,
    COUNT(DISTINCT CASE WHEN p.is_supplier THEN pcc.partner_id END) AS supplier_count,
    COUNT(DISTINCT CASE WHEN p.is_customer THEN pcc.partner_id END) AS customer_count
FROM partner_categories pcat
LEFT JOIN partner_catalog_categories pcc ON pcat.category_id = pcc.category_id
LEFT JOIN partner_catalog p ON pcc.partner_id = p.partner_id
GROUP BY pcat.category_type, pcat.category_code, pcat.category_name
ORDER BY pcat.category_type, partner_count DESC;
```

---

## 8. PRÍKLAD DÁT

### 8.1 Skupiny dodávateľov (z PAGLST.BTR)

```sql
-- Migrované z NEX Genesis PAGLST.BTR
INSERT INTO partner_categories (
    category_type, category_code, category_name, 
    created_by, updated_by
) VALUES
    ('supplier', '001', 'Potraviny a nápoje', 'migration', 'migration'),
    ('supplier', '002', 'Elektronika a spotrebiče', 'migration', 'migration'),
    ('supplier', '003', 'Textil a odevy', 'migration', 'migration'),
    ('supplier', '004', 'Stavebný materiál', 'migration', 'migration'),
    ('supplier', '005', 'Chemické výrobky', 'migration', 'migration');
```

### 8.2 Skupiny zákazníkov (nové v NEX Automat)

```sql
-- Nové kategórie pre odberateľov (neboli v NEX Genesis)
INSERT INTO partner_categories (
    category_type, category_code, category_name, category_description,
    created_by
) VALUES
    ('customer', '001', 'Maloobchod', 'Maloobchodní zákazníci', 'admin'),
    ('customer', '002', 'Veľkoobchod', 'Veľkoobchodní zákazníci', 'admin'),
    ('customer', '003', 'HoReCa', 'Hotely, reštaurácie, kaviarne', 'admin'),
    ('customer', '004', 'Firemní zákazníci', 'Korporátni a firemní zákazníci', 'admin'),
    ('customer', '005', 'Distribútori', 'Oficiálni distribútori', 'admin');
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### 9.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. partner_categories (Btrieve: PAGLST.BTR)        -- TÁTO TABUĽKA
2. partner_catalog (Btrieve: PAB00000.BTR)         -- Používa PagCode
3. partner_catalog_categories                       -- Mapovanie partnerov na kategórie
```

### 9.2 Python príklad transformácie

```python
from btrieve import Btrieve
import psycopg2
from datetime import datetime

def migrate_partner_categories():
    """
    Migrácia skupín dodávateľov z PAGLST.BTR
    """
    # Otvorenie Btrieve súboru
    paglst = Btrieve('C:/NEX/DATA/PAGLST.BTR')
    
    # Pripojenie na PostgreSQL
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Migrácia PAGLST.BTR → partner_categories (supplier)")
    
    # Spracovanie každého záznamu
    for record in paglst.records():
        # Transformácia polí
        pag_code = str(record.get('PagCode', 0))  # WORD → VARCHAR
        pag_name = record.get('PagName', '').strip()
        
        # Audit údaje
        mod_user = record.get('ModUser', '').strip() or 'migration'
        mod_date = record.get('ModDate')  # DateType
        mod_time = record.get('ModTime')  # TimeType
        
        # Kombinovanie dátumu a času
        if mod_date and mod_time:
            updated_at = datetime.combine(mod_date, mod_time)
        else:
            updated_at = None
        
        # INSERT do partner_categories
        cur.execute("""
            INSERT INTO partner_categories (
                category_type,
                category_code,
                category_name,
                created_by,
                created_at,
                updated_by,
                updated_at,
                is_active
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (category_type, category_code) DO UPDATE
            SET 
                category_name = EXCLUDED.category_name,
                updated_by = EXCLUDED.updated_by,
                updated_at = EXCLUDED.updated_at
        """, (
            'supplier',  # ✅ Fixne 'supplier' pre PAGLST.BTR
            pag_code,
            pag_name,
            mod_user,
            updated_at or datetime.now(),
            mod_user,
            updated_at or datetime.now(),
            True
        ))
        
        print(f"Migrovaná kategória: [{pag_code}] {pag_name}")
    
    conn.commit()
    
    # Štatistika
    cur.execute("""
        SELECT COUNT(*) FROM partner_categories
        WHERE category_type = 'supplier'
    """)
    count = cur.fetchone()[0]
    
    print(f"\n✅ Migrácia dokončená: {count} skupín dodávateľov")
    
    cur.close()
    conn.close()

# Funkcia pre manuálne naplnenie skupín zákazníkov
def create_customer_categories():
    """
    Vytvorenie skupín zákazníkov (neexistovali v NEX Genesis)
    """
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Vytvorenie partner_categories (customer) - manuálne")
    
    # Predvolené kategórie zákazníkov
    customer_categories = [
        ('001', 'Maloobchod', 'Maloobchodní zákazníci'),
        ('002', 'Veľkoobchod', 'Veľkoobchodní zákazníci'),
        ('003', 'HoReCa', 'Hotely, reštaurácie, kaviarne'),
        ('004', 'Firemní zákazníci', 'Korporátni a firemní zákazníci'),
        ('005', 'Distribútori', 'Oficiálni distribútori'),
    ]
    
    for code, name, desc in customer_categories:
        cur.execute("""
            INSERT INTO partner_categories (
                category_type,
                category_code,
                category_name,
                category_description,
                created_by,
                is_active
            ) VALUES (
                'customer', %s, %s, %s, 'admin', TRUE
            )
            ON CONFLICT (category_type, category_code) DO NOTHING
        """, (code, name, desc))
        
        print(f"Vytvorená kategória: [{code}] {name}")
    
    conn.commit()
    
    # Štatistika
    cur.execute("""
        SELECT COUNT(*) FROM partner_categories
        WHERE category_type = 'customer'
    """)
    count = cur.fetchone()[0]
    
    print(f"\n✅ Vytvorené: {count} skupín zákazníkov")
    
    cur.close()
    conn.close()

# Spustenie migrácie
if __name__ == '__main__':
    # Krok 1: Migrácia z PAGLST.BTR
    migrate_partner_categories()
    
    # Krok 2: Vytvorenie skupín zákazníkov
    create_customer_categories()
```

### 9.3 Dôležité poznámky

1. **PAGLST.BTR → supplier only:**
   - Všetky záznamy z PAGLST.BTR majú `category_type = 'supplier'`
   - PagCode (WORD) sa transformuje na VARCHAR

2. **PgcCode v PAB.BTR nemá číselník:**
   - V NEX Genesis neexistuje PGCLST.BTR
   - PgcCode je len textová hodnota bez metadát
   - V NEX Automat sa migrácia PgcCode rieši:
     - Buď ignoruje (ak nie sú dôležité)
     - Alebo sa vytvoria kategórie customer manuálne

3. **ON CONFLICT DO UPDATE:**
   - Umožňuje re-run migrácie
   - Aktualizuje existujúce záznamy
   - Neruší doplnené dáta (napr. category_description)

4. **_PagName (vyhľadávacie pole):**
   - V Btrieve používané pre case-insensitive vyhľadávanie
   - V PostgreSQL nahradené: `WHERE category_name ILIKE '%xyz%'`
   - Netreba migrovať

5. **Manuálne doplnenie customer categories:**
   - Vytvoriť predvolené skupiny zákazníkov
   - Užívateľ môže pridať vlastné podľa potreby
   - Používať konzistentné kódy (001, 002...)

---

## 10. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_categories** → `PAB-partner_catalog.md` (mapovacia tabuľka)

---

## 11. VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Mapping PAGLST.BTR → partner_categories (supplier)
- Poznámky o neexistencii PGCLST.BTR
- Python migračný script
- Funkcia pre manuálne vytvorenie customer categories

---

**Koniec dokumentu PAGLST-partner_categories.md**