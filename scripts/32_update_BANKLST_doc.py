#!/usr/bin/env python3
"""
Script 32: Update BANKLST-bank_catalog.md
- Add Btrieve file description with DIALS location
- Remove SQL scripts (CREATE, INDEX, TRIGGER, queries)
- Remove Python migration code
- Keep only essential info for module development
"""

from pathlib import Path


def main():
    """Update BANKLST documentation."""

    # Source and target paths
    source = Path('docs/architecture/database/catalogs/partners/tables/BANKLST-bank_catalog.md-old')
    target = Path('docs/architecture/database/catalogs/partners/tables/BANKLST-bank_catalog.md')

    # New content
    new_content = '''# BANKLST.BTR → bank_catalog

**Kategória:** Catalogs - Číselníky  
**NEX Genesis:** BANKLST.BTR  
**NEX Automat:** `bank_catalog`  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na implementáciu

---

## PREHĽAD

### Btrieve súbor
- **Názov:** BANKLST.BTR
- **Umiestnenie:** `C:\\NEX\\YEARACT\\DIALS\\BANKLST.BTR`
  - Premenná časť: `C:\\NEX\\` (root path)
  - Fixná časť: `\\YEARACT\\DIALS\\`
- **Účel:** Číselník bankových ústavov (banks catalog)

### Historický vývoj

**NEX Genesis (Btrieve):**
- BANKLST.BTR = číselník bankových ústavov
- Identifikácia len cez textový kód (BankCode: "1100", "0200"...)
- Slovenský smerovací kód banky

**NEX Automat (PostgreSQL):**
- **bank_catalog** - číselník bánk
- Pridané numerické ID (bank_id) pre konzistenciu
- Zachovaný BankCode pre kompatibilitu

**Účel:**
- Číselník slovenských a zahraničných bánk
- Referencované z partner_catalog_bank_accounts
- Použité pri platobných transakciách

---

## ŠTRUKTÚRA TABUĽKY

### bank_catalog

**Popis:** Číselník bankových ústavov

**Kľúčové polia:**
- `bank_id` - SERIAL PRIMARY KEY (nové numerické ID)
- `bank_code` - VARCHAR(20) UNIQUE NOT NULL (slovenský smerovací kód)
- `bank_name` - VARCHAR(100) NOT NULL
- `bank_seat` - VARCHAR(100) (komplexná adresa)
- `bank_tax_id` - VARCHAR(20) (IČO banky)
- `is_active` - BOOLEAN DEFAULT TRUE
- Audit polia: created_by, created_at, updated_by, updated_at

**Indexy:**
- PRIMARY KEY na bank_id
- UNIQUE INDEX na bank_code
- INDEX na bank_name
- Partial INDEX na is_active WHERE is_active = TRUE

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Popis |
|---------------|-----|---|-------------------|-----|-------|
| - | - | → | bank_id | SERIAL | **NOVÉ!** Numerické ID (1, 2, 3...) |
| BankCode | Str15 | → | bank_code | VARCHAR(20) | Smerovací kód banky |
| BankName | Str30 | → | bank_name | VARCHAR(100) | Názov banky |
| BankAddr + BankCtn + BankZip | Str30+Str30+Str15 | → | bank_seat | VARCHAR(100) | Komplexná adresa banky |
| BankIno | Str15 | → | bank_tax_id | VARCHAR(20) | IČO banky |
| CrtUser | Str8 | → | created_by | VARCHAR(30) | Vytvoril užívateľ |
| CrtDate, CrtTime | Date+Time | → | created_at | TIMESTAMP | Dátum vytvorenia |
| ModUser | Str8 | → | updated_by | VARCHAR(30) | Upravil užívateľ |
| ModDate, ModTime | Date+Time | → | updated_at | TIMESTAMP | Dátum úpravy |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Typ | Dôvod neprenášania |
|---------------|-----|--------------------|
| _BankName | Str15 | Vyhľadávacie pole - PostgreSQL full-text search |
| IbanCode | Str34 | IBAN banky - nevyužíva sa |
| SwftCode | Str20 | SWIFT banky - nevyužíva sa |
| ModNum | word | Verzia záznamu - PostgreSQL má to automaticky |

---

## BIZNIS LOGIKA

### 1. Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
- `bank_id` - SERIAL PRIMARY KEY (automaticky generované: 1, 2, 3...)

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**BankCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre kompatibilitu so slovenským bankovým systémom

### 2. Slovenské bankové kódy

**Formát:** 4-miestny kód

| Kód | Názov banky |
|-----|-------------|
| 1100 | TATRA BANKA a.s. |
| 0200 | Všeobecná úverová banka a.s. |
| 5600 | Prima banka Slovensko a.s. |
| 0900 | Slovenská sporiteľňa a.s. |
| 3100 | Poštová banka a.s. |
| 6500 | ČSOB a.s. |
| 7500 | Československá obchodná banka a.s. |

### 3. Použitie v partner_catalog_bank_accounts

**Relácia:**
- partner_catalog_bank_accounts.bank_id → bank_catalog.bank_id (nullable)

**Prečo nullable:**
- Partner môže mať zahraničný bankový účet (IBAN)
- Banka nemusí byť v našom číselníku
- IBAN je unikátny identifikátor účtu

---

## VZŤAHY S INÝMI TABUĽKAMI

### bank_catalog ← partner_catalog_bank_accounts

**Relácia:** ONE-TO-MANY (voliteľná)
- Jedna banka môže mať mnoho účtov partnerov
- Účet partnera môže nemať priradený bank_id (zahraničná banka)

**Use cases:**
- Partneri s účtom v konkrétnej banke (JOIN cez bank_id)
- Partneri so zahraničným účtom (bank_id IS NULL)
- Štatistika použitia bánk (COUNT účtov per banka)

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Unikátny kód
- `bank_code` musí byť unikátny a neprázdny

### 2. Povinné polia
- `bank_code` - NOT NULL
- `bank_name` - NOT NULL

### 3. Formát kódu
- Slovenské banky: 4-miestny numerický kód (napr. "1100")
- Zahraničné: môže byť alfanumerický

---

## PRÍKLAD DÁT

```sql
INSERT INTO bank_catalog (bank_code, bank_name, bank_seat, bank_tax_id, created_by) VALUES
('1100', 'TATRA BANKA a.s.', 'Hodžovo námestie 3, Bratislava, 81106', '00686930', 'admin'),
('0200', 'Všeobecná úverová banka a.s.', 'Mlynské Nivy 1, Bratislava, 82990', '31320155', 'admin'),
('5600', 'Prima banka Slovensko a.s.', 'Hodžova 11, Žilina, 01001', '31575951', 'admin'),
('0900', 'Slovenská sporiteľňa a.s.', 'Tomášikova 48, Bratislava, 83206', '00151653', 'admin'),
('3100', 'Poštová banka a.s.', 'Dvořákovo nábrežie 4, Bratislava, 81102', '31340890', 'admin'),
('6500', 'ČSOB a.s.', 'Michalská 18, Bratislava, 81585', '36854', 'admin'),
('7500', 'Československá obchodná banka a.s.', 'Michalská 18, Bratislava, 81585', '36854', 'admin'),
('8330', 'UniCredit Bank Czech Republic and Slovakia a.s.', 'Šancová 1/A, Bratislava, 81325', '49240901', 'admin'),
('1200', 'Privat banka a.s.', 'Einsteinova 24, Bratislava, 85101', '00483559', 'admin'),
('5200', 'OTP Banka Slovensko a.s.', 'Štúrova 5, Bratislava, 81302', '31318916', 'admin');
```

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Generovanie bank_id

- bank_id sa automaticky generuje (SERIAL)
- Pri INSERT do PostgreSQL sa neuvádza
- Automatická sekvenčná hodnota: 1, 2, 3...

### 2. Spracovanie adresy

**Transformácia:**
- BankAddr + BankCtn + BankZip → bank_seat
- Spojenie cez čiarku: "ulica, mesto, PSČ"
- NULL hodnoty sa preskakujú

### 3. Vytvorenie mapping dictionary

**Po migrácii:**
- Vytvoriť dictionary: BankCode → bank_id
- Použiť pri migrácii partner_catalog_bank_accounts
- Handling NULL: ak BankCode nie je v číselníku → bank_id = NULL

### 4. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **BANKLST.BTR** → bank_catalog
2. ✅ Vytvoriť mapping dictionary (BankCode → bank_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_bank_accounts
   - bank_id = lookup v dictionary (môže byť NULL!)
   - bank_name = vždy uložiť (denormalizácia pre prípad NULL bank_id)

---

## ROZŠÍRENIA V BUDÚCNOSTI

### Možné pridanie polí:

**Medzinárodné kódy:**
- swift_code VARCHAR(20) - SWIFT/BIC kód
- bic_code VARCHAR(20) - BIC kód

**Kontaktné údaje:**
- bank_website VARCHAR(100)
- bank_phone VARCHAR(30)
- bank_email VARCHAR(100)

**Kategorizácia:**
- bank_country_code VARCHAR(5) DEFAULT 'SK'
- bank_type VARCHAR(20) - 'commercial', 'savings', 'investment'

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_bank_accounts** → `PABACC-partner_catalog_bank_accounts.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na implementáciu
'''

    # Write new content
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(new_content, encoding='utf-8')
    print(f"✅ Created: {target}")

    # Remove old file
    if source.exists():
        source.unlink()
        print(f"✅ Deleted: {source}")

    print("\n✅ BANKLST documentation updated successfully")
    print(f"   - Added Btrieve file description (DIALS location)")
    print(f"   - Removed SQL scripts (CREATE, INDEX, TRIGGER, queries)")
    print(f"   - Removed Python migration code")
    print(f"   - Kept essential mapping and business logic")


if __name__ == '__main__':
    main()