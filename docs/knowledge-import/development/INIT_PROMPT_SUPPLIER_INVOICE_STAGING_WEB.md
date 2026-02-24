# INIT PROMPT - Supplier Invoice Staging Web UI

**Projekt:** nex-automat / supplier-invoice-staging-web  
**Typ:** Nový React Web UI pre existujúci FastAPI backend  
**Cieľ:** Paralelné používanie s PySide6 desktop aplikáciou  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 Cieľ projektu

Vytvoriť moderný Web UI pre `supplier-invoice-staging` aplikáciu, ktorý:
- Používa existujúci FastAPI backend (`supplier-invoice-loader`)
- Beží paralelne s PySide6 desktop aplikáciou
- Umožňuje mobilný prístup pre schvaľovanie faktúr
- Má moderný dizajn (React + Tailwind + Shadcn/ui)

---

## 🏗️ Architektúra

```
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (existuje)                     │
│              supplier-invoice-loader:8000                   │
└─────────────────────────────────────────────────────────────┘
                    │                    │
         ┌──────────┴──────────┐         │
         ▼                     ▼         ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PySide6 GUI   │  │    Web UI       │  │  Mobil (PWA)    │
│   (existuje)    │  │    (TOTO)       │  │  (budúcnosť)    │
│ supplier-       │  │ supplier-       │  │                 │
│ invoice-staging │  │ invoice-staging │  │                 │
│                 │  │ -web            │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 📁 Umiestnenie v projekte

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/         # FastAPI backend (existuje)
│   ├── supplier-invoice-staging/        # PySide6 GUI (existuje)
│   └── supplier-invoice-staging-web/    # Web UI (NOVÉ)
│       ├── src/
│       │   ├── components/
│       │   │   ├── ui/              # Shadcn komponenty
│       │   │   ├── invoices/
│       │   │   │   ├── InvoiceList.tsx
│       │   │   │   ├── InvoiceCard.tsx
│       │   │   │   ├── InvoiceDetail.tsx
│       │   │   │   ├── InvoiceFilters.tsx
│       │   │   │   └── ApprovalDialog.tsx
│       │   │   ├── dashboard/
│       │   │   │   └── DashboardStats.tsx
│       │   │   └── layout/
│       │   │       ├── Header.tsx
│       │   │       ├── Sidebar.tsx
│       │   │       └── Layout.tsx
│       │   ├── pages/
│       │   │   ├── Dashboard.tsx
│       │   │   ├── Invoices.tsx
│       │   │   ├── InvoiceDetail.tsx
│       │   │   └── Settings.tsx
│       │   ├── api/
│       │   │   ├── client.ts        # Axios instance
│       │   │   ├── invoices.ts      # Invoice API calls
│       │   │   └── types.ts         # TypeScript typy
│       │   ├── hooks/
│       │   │   ├── useInvoices.ts
│       │   │   └── useApproval.ts
│       │   ├── lib/
│       │   │   └── utils.ts
│       │   ├── App.tsx
│       │   ├── main.tsx
│       │   └── index.css
│       ├── public/
│       ├── package.json
│       ├── vite.config.ts
│       ├── tailwind.config.js
│       ├── tsconfig.json
│       ├── Dockerfile
│       └── nginx.conf
```

---

## 🛠️ Technologický stack

| Technológia | Verzia | Účel |
|-------------|--------|------|
| React | 18.x | UI framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| Tailwind CSS | 3.x | Styling |
| Shadcn/ui | latest | UI komponenty |
| TanStack Query | 5.x | Data fetching + cache |
| React Router | 6.x | Routing |
| Axios | 1.x | HTTP klient |
| Lucide React | latest | Ikony |
| React Hook Form | 7.x | Formuláre |
| Zod | 3.x | Validácia |

---

## 🔌 Existujúce API Endpointy

**Base URL:** `http://localhost:8000/api`  
**Auth:** `X-API-Key: andros-api-key-2025`

| Endpoint | Metóda | Popis |
|----------|--------|-------|
| `/invoices` | GET | Zoznam faktúr (s filtrami) |
| `/invoices/{id}` | GET | Detail faktúry |
| `/invoices` | POST | Vytvorenie faktúry |
| `/invoices/{id}` | PUT | Úprava faktúry |
| `/invoices/{id}` | DELETE | Zmazanie faktúry |
| `/invoices/{id}/approve` | PUT | Schválenie faktúry |
| `/invoices/{id}/reject` | PUT | Zamietnutie faktúry |
| `/invoices/{id}/pdf` | GET | PDF súbor faktúry |
| `/health` | GET | Health check |

**Poznámka:** Overiť aktuálne endpointy v Swagger UI: `http://localhost:8000/docs`

---

## 📊 Dátové modely (TypeScript)

```typescript
// src/api/types.ts

export interface Invoice {
  id: number;
  invoice_number: string;
  supplier_name: string;
  supplier_ico: string;
  issue_date: string;
  due_date: string;
  total_amount: number;
  currency: string;
  status: InvoiceStatus;
  pdf_path: string;
  created_at: string;
  updated_at: string;
  items: InvoiceItem[];
}

export type InvoiceStatus = 
  | 'new' 
  | 'pending_approval' 
  | 'approved' 
  | 'rejected' 
  | 'processed';

export interface InvoiceItem {
  id: number;
  description: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  vat_rate: number;
}

export interface InvoiceFilters {
  status?: InvoiceStatus;
  supplier_name?: string;
  date_from?: string;
  date_to?: string;
  search?: string;
}

export interface DashboardStats {
  total_invoices: number;
  pending_approval: number;
  approved_today: number;
  total_amount_this_month: number;
}
```

---

## 🎨 UI Požiadavky

### Farebná schéma
- Primary: Blue (#3B82F6)
- Success: Green (#22C55E)
- Warning: Yellow (#EAB308)
- Error: Red (#EF4444)
- Background: Slate (#F8FAFC)
- Dark mode: Podporovaný

### Stavy faktúr - vizualizácia
| Status | Farba | Ikona | Slovensky |
|--------|-------|-------|-----------|
| new | Gray | 📄 | Nová |
| pending_approval | Yellow | 🟡 | Čaká na schválenie |
| approved | Green | ✅ | Schválená |
| rejected | Red | ❌ | Zamietnutá |
| processed | Blue | 📤 | Spracovaná |

### Stránky
1. **Dashboard** - Štatistiky, grafy, posledné faktúry
2. **Faktúry** - Zoznam s filtrami, vyhľadávanie
3. **Detail faktúry** - Náhľad PDF, položky, schvaľovanie
4. **Nastavenia** - Profil, notifikácie

---

## 🚀 Fázy vývoja

### Fáza 1: Setup projektu (2 hodiny)
- [ ] Vite + React + TypeScript projekt
- [ ] Tailwind CSS konfigurácia
- [ ] Shadcn/ui inštalácia
- [ ] Základná štruktúra priečinkov
- [ ] API klient (Axios)

### Fáza 2: Layout a navigácia (2 hodiny)
- [ ] Header komponent
- [ ] Sidebar/Navigation
- [ ] Layout wrapper
- [ ] React Router setup
- [ ] Dark mode toggle

### Fáza 3: Zoznam faktúr (4 hodiny)
- [ ] InvoiceList komponent
- [ ] InvoiceCard komponent
- [ ] InvoiceFilters komponent
- [ ] Pagination
- [ ] Loading a error states

### Fáza 4: Detail faktúry (3 hodiny)
- [ ] InvoiceDetail stránka
- [ ] PDF náhľad (react-pdf alebo iframe)
- [ ] Položky faktúry tabuľka
- [ ] Stavový badge

### Fáza 5: Schvaľovací workflow (3 hodiny)
- [ ] ApprovalDialog komponent
- [ ] Schválenie s poznámkou
- [ ] Zamietnutie s dôvodom
- [ ] Toast notifikácie
- [ ] Optimistic updates

### Fáza 6: Dashboard (3 hodiny)
- [ ] DashboardStats karty
- [ ] Graf faktúr (Recharts)
- [ ] Posledné faktúry widget
- [ ] Quick actions

### Fáza 7: Polish a deployment (4 hodiny)
- [ ] Responsive design (mobil)
- [ ] Error handling
- [ ] Loading skeletony
- [ ] Dockerfile
- [ ] Nginx konfigurácia
- [ ] Docker Compose integrácia

---

## 📝 Príkazy na spustenie

```bash
# Development
cd apps/supplier-invoice-staging-web
npm install
npm run dev  # http://localhost:5173

# Build
npm run build

# Docker
docker build -t nex-invoice-staging-web .
docker run -p 3000:80 nex-invoice-staging-web
```

---

## 🔗 Užitočné odkazy

- Swagger UI: `http://localhost:8000/docs`
- Existujúci PySide6 kód: `apps/supplier-invoice-staging/`
- Web UI (nový): `apps/supplier-invoice-staging-web/`
- FastAPI backend: `apps/supplier-invoice-loader/`

---

## 📋 Session Priority

**Immediate:** Fáza 1-2 (Setup + Layout)  
**Next:** Fáza 3-4 (Zoznam + Detail)  
**Then:** Fáza 5-6 (Schvaľovanie + Dashboard)  
**Final:** Fáza 7 (Deployment)

---

## ⚠️ Dôležité poznámky

1. **Paralelné použitie** - Web UI a PySide6 bežia súčasne
2. **Rovnaké API** - Žiadne zmeny v backend-e (alebo minimálne)
3. **Responzívny dizajn** - Mobil pre schvaľovanie
4. **Slovenské UI** - Všetky texty po slovensky
5. **PWA ready** - Pripraviť na budúcu PWA konverziu

---

## 🔍 RAG Queries

```
https://rag-api.icc.sk/search?query=supplier-invoice-loader+API+endpoints&limit=5
https://rag-api.icc.sk/search?query=supplier-invoice-staging+PySide6+components&limit=5
https://rag-api.icc.sk/search?query=Invoice+data+model+database+schema&limit=5
```

---

## ✅ Definition of Done

- [ ] Web UI beží na `http://localhost:3000`
- [ ] Zoznam faktúr s filtrami funguje
- [ ] Detail faktúry s PDF náhľadom
- [ ] Schválenie/Zamietnutie funguje
- [ ] Dashboard so štatistikami
- [ ] Responzívny na mobile
- [ ] Docker image pripravený
- [ ] Dokumentácia aktualizovaná