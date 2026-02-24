# NEX Automat - Databázová štruktúra Module Manager

## 1. Prehľad tabuliek

| Tabuľka | Účel |
|---------|------|
| `users` | Používatelia systému |
| `groups` | Skupiny práv (účtovníčka, skladník...) |
| `user_groups` | Priradenie používateľov do skupín (M:N) |
| `modules` | Zoznam programových modulov |
| `group_module_permissions` | Práva skupiny k modulu |

## 2. ER Diagram

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   users     │       │ user_groups  │       │   groups    │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id (PK)     │───┐   │ user_id (FK) │   ┌───│ id (PK)     │
│ login_name  │   └──▶│ group_id(FK) │◀──┘   │ code        │
│ full_name   │       └──────────────┘       │ name        │
│ password    │                              │ description │
│ is_active   │                              │ is_active   │
└─────────────┘                              └─────────────┘
                                                    │
                                                    │
                      ┌─────────────────────────────┘
                      │
                      ▼
┌─────────────┐       ┌──────────────────────────┐
│  modules    │       │ group_module_permissions │
├─────────────┤       ├──────────────────────────┤
│ id (PK)     │◀──────│ module_id (FK)           │
│ code        │       │ group_id (FK)            │
│ name        │       │ can_access               │
│ category    │       │ can_insert               │
│ icon        │       │ can_modify               │
│ order_num   │       │ can_delete               │
│ is_active   │       │ can_print                │
└─────────────┘       │ can_export               │
                      │ can_configure            │
                      └──────────────────────────┘
```

## 3. Tabuľka: users

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| id | SERIAL PK | Primárny kľúč |
| login_name | VARCHAR(50) UNIQUE | Prihlasovacie meno |
| full_name | VARCHAR(100) | Celé meno používateľa |
| password_hash | VARCHAR(255) | Hashované heslo (bcrypt) |
| email | VARCHAR(100) | Email (voliteľný) |
| is_active | BOOLEAN | Aktívny účet (default TRUE) |
| last_login | TIMESTAMP | Posledné prihlásenie |
| created_at | TIMESTAMP | Dátum vytvorenia |
| updated_at | TIMESTAMP | Dátum poslednej zmeny |

**Poznámky:**
- Heslo nikdy neukladať v čistom texte
- `login_name` case-insensitive (ukladať lowercase)

## 4. Tabuľka: groups

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| id | SERIAL PK | Primárny kľúč |
| code | VARCHAR(20) UNIQUE | Kód skupiny (ACCOUNTANT, WAREHOUSE...) |
| name | VARCHAR(50) | Názov skupiny (Účtovníčka, Skladník...) |
| description | TEXT | Popis skupiny |
| is_active | BOOLEAN | Aktívna skupina (default TRUE) |
| created_at | TIMESTAMP | Dátum vytvorenia |
| updated_at | TIMESTAMP | Dátum poslednej zmeny |

**Príklady skupín:**

| code | name | description |
|------|------|-------------|
| ADMIN | Administrátor | Plný prístup ku všetkým modulom |
| ACCOUNTANT | Účtovníčka | Účtovníctvo, faktúry, pokladňa |
| WAREHOUSE | Skladník | Sklad, príjemky, výdajky |
| SALES | Obchodník | Ponuky, zákazky, faktúry |
| OPERATOR | Operátor | Základný prístup, len prezeranie |

## 5. Tabuľka: user_groups

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| user_id | INT FK | Odkaz na users.id |
| group_id | INT FK | Odkaz na groups.id |
| assigned_at | TIMESTAMP | Dátum priradenia |
| assigned_by | INT FK | Kto priradil (users.id) |

**Primárny kľúč:** (user_id, group_id)

**Poznámka:** Jeden používateľ môže byť vo viacerých skupinách. Výsledné práva = UNION všetkých skupín (ak má aspoň jedna skupina právo, má ho aj používateľ).

## 6. Tabuľka: modules

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| id | SERIAL PK | Primárny kľúč |
| code | VARCHAR(10) UNIQUE | Kód modulu (GSC, PAB, ICB...) |
| name | VARCHAR(50) | Názov modulu |
| category | VARCHAR(30) | Kategória (stock, sales, accounting...) |
| icon | VARCHAR(10) | Emoji ikona (📦, 💰...) |
| order_num | INT | Poradie v menu |
| is_active | BOOLEAN | Modul aktívny (default TRUE) |
| is_mock | BOOLEAN | Mock modul (default TRUE) |

**Kategórie:**

| category | Názov |
|----------|-------|
| base | Bázová evidencia |
| business | Obchodná činnosť |
| purchase | Zásobovanie |
| stock | Sklad |
| sales | Odbyt |
| pos | Registračné pokladnice |
| accounting | Účtovníctvo |
| system | Systém |

## 7. Tabuľka: group_module_permissions

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| group_id | INT FK | Odkaz na groups.id |
| module_id | INT FK | Odkaz na modules.id |
| can_access | BOOLEAN | Vstup do modulu (E) |
| can_insert | BOOLEAN | Vytvoriť záznam (I) |
| can_modify | BOOLEAN | Upraviť záznam (M) |
| can_delete | BOOLEAN | Zmazať záznam (D) |
| can_print | BOOLEAN | Tlač/Export PDF (P) |
| can_export | BOOLEAN | Export dát (Excel, CSV) |
| can_configure | BOOLEAN | Konfigurácia modulu (V) |

**Primárny kľúč:** (group_id, module_id)

**Mapovanie na NEX Genesis EIDMPVLOA:**

| NEX Genesis | NEX Automat | Popis |
|-------------|-------------|-------|
| E - Enable | can_access | Vstup do modulu |
| I - Insert | can_insert | Pridanie záznamu |
| D - Delete | can_delete | Mazanie záznamu |
| M - Modify | can_modify | Úprava záznamu |
| P - Print | can_print | Tlač |
| V - Property | can_configure | Konfigurácia |
| L - DocLock | (v budúcnosti) | Uzamykanie dokladov |
| O - OwnOpen | (v budúcnosti) | Odomknutie vlastných |
| A - AllOpen | (v budúcnosti) | Odomknutie všetkých |

**Poznámka:** L, O, A práva doplníme neskôr pre dokladové moduly.

## 8. Vyhodnotenie práv používateľa

**Pravidlo:** Používateľ má právo, ak **aspoň jedna** z jeho skupín má toto právo.

```
Príklad:
- Ján Kováč je v skupinách: ACCOUNTANT, OPERATOR
- ACCOUNTANT má can_insert=TRUE pre modul ICB
- OPERATOR má can_insert=FALSE pre modul ICB
- Výsledok: Ján Kováč MÁ právo can_insert pre ICB
```

## 9. Inicializačné dáta

### 9.1 Predvolené skupiny

| code | name |
|------|------|
| ADMIN | Administrátor |
| ACCOUNTANT | Účtovníčka |
| WAREHOUSE | Skladník |
| SALES | Obchodník |
| OPERATOR | Operátor |

### 9.2 Predvolené moduly (mock)

| code | name | category |
|------|------|----------|
| GSC | Evidencia tovaru | base |
| PAB | Evidencia partnerov | base |
| STK | Skladové karty | stock |
| IMB | Príjemky | stock |
| OMB | Výdajky | stock |
| ICB | Odberateľské faktúry | sales |
| ISB | Dodávateľské faktúry | purchase |
| JRN | Účtovný denník | accounting |

### 9.3 Predvolený admin používateľ

| login_name | full_name | groups |
|------------|-----------|--------|
| admin | Administrátor | ADMIN |

## 10. Audit log

### Tabuľka: audit_log

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| id | SERIAL PK | Primárny kľúč |
| timestamp | TIMESTAMP | Kedy sa udalosť stala |
| user_id | INT FK | Kto vykonal akciu |
| action | VARCHAR(50) | Typ akcie |
| entity_type | VARCHAR(50) | Typ entity (user, group, permission...) |
| entity_id | INT | ID entity |
| old_value | JSONB | Pôvodná hodnota |
| new_value | JSONB | Nová hodnota |
| ip_address | VARCHAR(45) | IP adresa |

**Typy akcií (action):**

| action | Popis |
|--------|-------|
| USER_CREATED | Vytvorenie používateľa |
| USER_MODIFIED | Úprava používateľa |
| USER_DEACTIVATED | Deaktivácia používateľa |
| USER_PASSWORD_CHANGED | Zmena hesla |
| USER_LOGIN | Prihlásenie |
| USER_LOGOUT | Odhlásenie |
| USER_LOGIN_FAILED | Neúspešné prihlásenie |
| GROUP_CREATED | Vytvorenie skupiny |
| GROUP_MODIFIED | Úprava skupiny |
| GROUP_DELETED | Zmazanie skupiny |
| USER_ADDED_TO_GROUP | Priradenie do skupiny |
| USER_REMOVED_FROM_GROUP | Odobratie zo skupiny |
| PERMISSION_CHANGED | Zmena práv skupiny k modulu |

## 11. Hierarchia skupín

### Tabuľka: groups (rozšírená)

| Stĺpec | Typ | Popis |
|--------|-----|-------|
| ... | ... | (existujúce stĺpce) |
| parent_id | INT FK NULL | Rodičovská skupina (groups.id) |
| level | INT | Úroveň v hierarchii (0 = root) |

### Príklad hierarchie

```
ADMIN (level 0)
  └── POWER_USER (level 1)
        ├── ACCOUNTANT (level 2)
        ├── WAREHOUSE (level 2)
        └── SALES (level 2)
              └── OPERATOR (level 3)
```

### Pravidlo dedenia

**Rodičovská skupina dedí všetky práva od potomkov.**

```
Príklad:
- OPERATOR má can_access=TRUE pre GSC
- SALES (rodič OPERATOR) automaticky má can_access=TRUE pre GSC
- POWER_USER (rodič SALES) automaticky má can_access=TRUE pre GSC
- ADMIN (rodič POWER_USER) automaticky má can_access=TRUE pre GSC

Navyše:
- ADMIN môže mať explicitne can_configure=TRUE pre GSC
- OPERATOR toto právo NEMÁ (dedenie ide len smerom hore)
```

### Vyhodnotenie práv s hierarchiou

```
Používateľ má právo ak:
1. Aspoň jedna jeho skupina má toto právo, ALEBO
2. Aspoň jedna jeho skupina je rodičom skupiny, ktorá má toto právo
```

## 12. Aktualizovaný ER Diagram

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   users     │       │ user_groups  │       │   groups    │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id (PK)     │───┐   │ user_id (FK) │   ┌───│ id (PK)     │
│ login_name  │   └──▶│ group_id(FK) │◀──┘   │ parent_id   │──┐
│ full_name   │       └──────────────┘       │ level       │  │
│ password    │                              │ code        │  │
│ is_active   │                              │ name        │  │
└─────────────┘                              └─────────────┘◀─┘
                                                    │
                      ┌─────────────────────────────┘
                      ▼
┌─────────────┐       ┌──────────────────────────┐
│  modules    │       │ group_module_permissions │
├─────────────┤       ├──────────────────────────┤
│ id (PK)     │◀──────│ module_id (FK)           │
│ code        │       │ group_id (FK)            │
│ name        │       │ can_access               │
│ category    │       │ can_insert               │
│ ...         │       │ ...                      │
└─────────────┘       └──────────────────────────┘

┌─────────────────────────────────────────────────┐
│                  audit_log                       │
├─────────────────────────────────────────────────┤
│ id (PK)                                         │
│ timestamp                                        │
│ user_id (FK) ───────────────────▶ users.id      │
│ action                                           │
│ entity_type                                      │
│ entity_id                                        │
│ old_value (JSONB)                               │
│ new_value (JSONB)                               │
│ ip_address                                       │
└─────────────────────────────────────────────────┘
```

## 13. Kompletný zoznam tabuliek

| # | Tabuľka | Účel |
|---|---------|------|
| 1 | users | Používatelia systému |
| 2 | groups | Skupiny práv s hierarchiou |
| 3 | user_groups | Priradenie používateľov do skupín |
| 4 | modules | Programové moduly |
| 5 | group_module_permissions | Práva skupiny k modulu |
| 6 | audit_log | Audit všetkých zmien |

## 14. Rozhodnutia

| Otázka | Rozhodnutie |
|--------|-------------|
| Export právo | ✅ Oddelené od tlače (can_export) |
| Audit log | ✅ Áno, tabuľka audit_log |
| Hierarchia skupín | ✅ Áno, parent_id + level |
| Knihové práva | Odložené na neskôr |