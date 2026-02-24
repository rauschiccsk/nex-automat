# NEX Automat - Návrh adresárovej štruktúry

## 1. Aktuálny stav

```
apps/
├── andros-invoice-worker/        # ANDROS-špecifický Temporal worker
├── btrieve-loader/               # Btrieve API (venv32 - samostatne kvôli 32-bit)
├── nex-brain/                    # AI/RAG systém
├── supplier-invoice-editor/      # Desktop PyQt5
├── supplier-invoice-staging/     # Desktop PySide6
├── supplier-invoice-staging-web/ # React frontend
├── supplier-invoice-worker/      # Temporal workflow
```

**Poznámka:** Existujúce priečinky zostávajú bez zmeny. Časom sa začlenia do novej štruktúry.

---

## 2. Navrhovaná štruktúra

```
nex-automat/
│
├── apps/
│   │
│   ├── backend/                    # 🆕 Hlavný FastAPI backend (NEX Automat Web)
│   │   ├── src/
│   │   │   ├── api/
│   │   │   │   ├── routes/         # API endpoints
│   │   │   │   ├── deps.py         # Dependencies (auth, db session)
│   │   │   │   └── main.py         # FastAPI app
│   │   │   ├── core/
│   │   │   │   ├── config.py       # Settings
│   │   │   │   ├── security.py     # JWT, hashing
│   │   │   │   └── database.py     # DB connection
│   │   │   ├── models/             # SQLAlchemy models
│   │   │   ├── schemas/            # Pydantic schemas
│   │   │   └── services/           # Business logic
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── web/                        # 🆕 React frontend (NEX Automat Web)
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── stores/             # Zustand
│   │   │   ├── api/                # API client
│   │   │   └── App.tsx
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── andros-invoice-worker/        # ✅ Bez zmeny
│   ├── btrieve-loader/               # ✅ Bez zmeny (venv32)
│   ├── nex-brain/                    # ✅ Bez zmeny
│   ├── supplier-invoice-editor/      # ✅ Bez zmeny
│   ├── supplier-invoice-staging/     # ✅ Bez zmeny
│   ├── supplier-invoice-staging-web/ # ✅ Bez zmeny
│   └── supplier-invoice-worker/      # ✅ Bez zmeny
│
├── packages/                       # ✅ Zdieľané balíky (bez zmeny)
│   ├── nex-shared/
│   ├── nex-staging/
│   ├── nexdata/
│   └── shared-pyside6/
│
├── tools/                          # Pomocné nástroje
│   ├── rag/                        # RAG server
│   └── mcp_rag_server.py
│
├── docs/
│   ├── knowledge/                  # RAG knowledge base
│   │   ├── architecture/           # 🆕 Architektúra dokumenty
│   │   ├── database/
│   │   └── modules/
│   └── api/                        # API dokumentácia
│
├── config/                         # Konfigurácie
├── scripts/                        # Deployment, maintenance skripty
└── docker/                         # Docker súbory
```

---

## 3. Zmeny oproti aktuálnemu stavu

| Zmena | Popis |
|-------|-------|
| `apps/backend/` | 🆕 Nový FastAPI pre NEX Automat Web |
| `apps/frontend/web/` | 🆕 Nový React frontend |
| Existujúce priečinky | ✅ Zostávajú bez zmeny (začlenia sa časom) |

---

## 4. Backend štruktúra (detail)

```
apps/backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Login, logout, refresh token
│   │   │   ├── users.py         # CRUD používatelia
│   │   │   ├── groups.py        # CRUD skupiny
│   │   │   ├── modules.py       # Zoznam modulov, práva
│   │   │   └── health.py        # Health check
│   │   ├── deps.py              # get_db, get_current_user
│   │   └── main.py              # FastAPI app, CORS, routers
│   │
│   ├── core/
│   │   ├── config.py            # Settings (pydantic-settings)
│   │   ├── security.py          # JWT, password hashing
│   │   └── database.py          # SQLAlchemy engine, session
│   │
│   ├── models/                  # SQLAlchemy ORM
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── module.py
│   │   ├── permission.py
│   │   └── audit.py
│   │
│   ├── schemas/                 # Pydantic schemas
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── auth.py
│   │   └── common.py
│   │
│   └── services/                # Business logic
│       ├── auth_service.py
│       ├── user_service.py
│       └── permission_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_users.py
│
├── alembic/                     # DB migrations
│   ├── versions/
│   └── env.py
│
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## 5. Frontend štruktúra (detail)

```
apps/frontend/
├── web/                              # React web aplikácia
│   ├── src/
│   │   │
│   │   ├── nex-manager/              # 🆕 Module Manager (jadro)
│   │   │   ├── ModuleManager.ts      # Registrácia, lifecycle
│   │   │   ├── ModuleRegistry.ts     # Zoznam všetkých modulov
│   │   │   ├── PermissionService.ts  # Kontrola práv
│   │   │   ├── LicenseService.ts     # Kontrola licencií
│   │   │   └── types.ts              # ModuleDefinition, Permission
│   │   │
│   │   ├── modules/                  # 🆕 Všetky moduly (40+)
│   │   │   │
│   │   │   ├── base/                 # 📋 Bázová evidencia
│   │   │   │   ├── partners/         # PAB - Partneri
│   │   │   │   │   ├── PartnersModule.tsx
│   │   │   │   │   ├── PartnersList.tsx
│   │   │   │   │   ├── PartnerDetail.tsx
│   │   │   │   │   ├── PartnerForm.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── products/         # GSC - Tovar
│   │   │   │   ├── weights/          # VAH - Váhy
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── stock/                # 📦 Sklad
│   │   │   │   ├── stock-cards/      # STK - Skladové karty
│   │   │   │   ├── receipts/         # IMB - Príjemky
│   │   │   │   ├── issues/           # OMB - Výdajky
│   │   │   │   ├── transfers/        # PMB - Presuny
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── sales/                # 💰 Odbyt
│   │   │   │   ├── invoices/         # ICB - Odberateľské faktúry
│   │   │   │   ├── orders/           # ODB - Zákazky
│   │   │   │   ├── quotes/           # PON - Ponuky
│   │   │   │   ├── delivery-notes/   # DOD - Dodacie listy
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── purchase/             # 🛒 Zásobovanie
│   │   │   │   ├── supplier-invoices/  # ISB - Dodávateľské faktúry
│   │   │   │   ├── purchase-orders/    # OBJ - Objednávky
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── accounting/           # 📊 Účtovníctvo
│   │   │   │   ├── journal/          # JRN - Účtovný denník
│   │   │   │   ├── trial-balance/    # ACT - Predvaha
│   │   │   │   ├── vat/              # VTR - DPH
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── pos/                  # 🏪 Pokladnice
│   │   │   │   ├── config/           # Konfigurácia
│   │   │   │   ├── closures/         # Uzávierky
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── system/               # ⚙️ Systém
│   │   │   │   ├── users/            # Používatelia
│   │   │   │   ├── groups/           # Skupiny práv
│   │   │   │   ├── settings/         # Nastavenia
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── _shared/              # Zdieľané pre moduly
│   │   │       ├── ModuleLayout.tsx  # Spoločný layout
│   │   │       ├── CatalogModule.tsx # Base pre katalógy
│   │   │       ├── DocumentModule.tsx # Base pre doklady
│   │   │       └── MockModule.tsx    # Placeholder
│   │   │
│   │   ├── components/               # Globálne komponenty
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── TabBar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── CommandLine.tsx
│   │   │   │   ├── InfoPanel.tsx
│   │   │   │   └── Breadcrumbs.tsx
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Toast.tsx
│   │   │       ├── LookupPopup.tsx
│   │   │       ├── DataTable.tsx
│   │   │       └── Form.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useModule.ts
│   │   │   ├── usePermissions.ts
│   │   │   └── useShortcuts.ts
│   │   │
│   │   ├── stores/                   # Zustand
│   │   │   ├── authStore.ts
│   │   │   ├── tabStore.ts
│   │   │   ├── moduleStore.ts
│   │   │   └── uiStore.ts
│   │   │
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── auth.ts
│   │   │   └── modules.ts
│   │   │
│   │   ├── types/
│   │   ├── styles/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── README.md
│
└── mobile/                           # 🔮 Budúce mobilné apps
    └── README.md
```

---

## 6. Module Generator

### 6.1 Účel

Automatické generovanie štruktúry modulov z definičných súborov. 40+ modulov manuálne = neefektívne a nekonzistentné.

### 6.2 Štruktúra

```
tools/
└── module-generator/
    ├── generator.ts              # Hlavný generátor
    ├── templates/
    │   ├── catalog/              # Šablóny pre katalógové moduly
    │   │   ├── Module.tsx.hbs
    │   │   ├── List.tsx.hbs
    │   │   ├── Detail.tsx.hbs
    │   │   ├── Form.tsx.hbs
    │   │   └── index.ts.hbs
    │   └── document/             # Šablóny pre dokladové moduly
    │       ├── Module.tsx.hbs
    │       ├── List.tsx.hbs
    │       ├── Header.tsx.hbs
    │       ├── Items.tsx.hbs
    │       └── index.ts.hbs
    └── definitions/              # Definície modulov (YAML)
        ├── base/
        │   ├── partners.yaml
        │   └── products.yaml
        ├── stock/
        │   ├── stock-cards.yaml
        │   └── receipts.yaml
        └── sales/
            └── invoices.yaml
```

### 6.3 Príklad definície modulu (YAML)

```yaml
# definitions/base/partners.yaml
module:
  code: PAB
  name: Evidencia partnerov
  category: base
  type: catalog
  icon: 👥
  shortcut: par

entity:
  name: Partner
  table: partners
  
fields:
  - name: code
    type: string
    label: Kód
    required: true
    unique: true
    maxLength: 20
    
  - name: name
    type: string
    label: Názov
    required: true
    maxLength: 100
    searchable: true
    
  - name: ico
    type: string
    label: IČO
    maxLength: 8
    
  - name: dic
    type: string
    label: DIČ
    maxLength: 12
    
  - name: ic_dph
    type: string
    label: IČ DPH
    maxLength: 14
    
  - name: address
    type: object
    label: Adresa
    fields:
      - name: street
        type: string
        label: Ulica
      - name: city
        type: string
        label: Mesto
      - name: zip
        type: string
        label: PSČ
      - name: country
        type: string
        label: Krajina
        default: SK
        
  - name: is_customer
    type: boolean
    label: Odberateľ
    default: false
    
  - name: is_supplier
    type: boolean
    label: Dodávateľ
    default: false

list:
  columns:
    - field: code
      width: 100
    - field: name
      width: 300
    - field: ico
      width: 100
    - field: address.city
      width: 150
  defaultSort: name
  
permissions:
  - can_access
  - can_insert
  - can_modify
  - can_delete
  - can_print
  - can_export
```

### 6.4 Použitie generátora

```bash
# Generovať jeden modul
npm run generate:module -- --def=base/partners.yaml

# Generovať všetky moduly v kategórii
npm run generate:module -- --category=base

# Generovať všetky moduly
npm run generate:module -- --all

# Preview bez generovania
npm run generate:module -- --def=base/partners.yaml --dry-run
```

### 6.5 Generovaná štruktúra

```
modules/base/partners/
├── PartnersModule.tsx      # Hlavný komponent modulu
├── PartnersList.tsx        # Zoznam (DataTable)
├── PartnerDetail.tsx       # Detail záznamu (InfoPanel)
├── PartnerForm.tsx         # Formulár (Create/Edit)
├── partners.api.ts         # API volania
├── partners.types.ts       # TypeScript typy
├── partners.schema.ts      # Zod validácia
└── index.ts                # Export
```

### 6.6 Výhody

| Výhoda | Popis |
|--------|-------|
| Konzistencia | Všetky moduly majú rovnakú štruktúru |
| Rýchlosť | 40 modulov za minúty, nie dni |
| Údržba | Zmena šablóny = regenerácia všetkých |
| Dokumentácia | YAML definície = živá dokumentácia |
| Validácia | Typová kontrola definícií |

---

## 7. Implementačný plán

| Fáza | Úloha | Priorita |
|------|-------|----------|
| 1 | Vytvoriť `apps/backend/` skeleton | 🔴 Vysoká |
| 2 | Vytvoriť `apps/web/` skeleton | 🔴 Vysoká |
| 3 | Zlúčiť `supplier-invoice-*` | 🟡 Stredná |
| 4 | Presunúť `andros-invoice-worker` | 🟡 Stredná |
| 5 | Vytvoriť `docs/knowledge/architecture/` | 🟢 Nízka |

---

## 7. Rozhodnutia na potvrdenie

| # | Otázka | Návrh |
|---|--------|-------|
| 1 | Názov backend priečinka | `backend` alebo `api`? |
| 2 | Názov frontend priečinka | `web` alebo `frontend`? |
| 3 | Zlúčenie supplier-invoice teraz alebo neskôr? | Neskôr (po stabilizácii) |
| 4 | `btrieve-loader` - premenovať? | Nie (funguje, nechať) |