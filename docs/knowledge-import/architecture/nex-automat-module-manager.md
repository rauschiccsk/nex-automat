# NEX Automat - Výber technológie a Module Manager

## 1. Rozhodnutia

| Otázka | Rozhodnutie | Dôvod |
|--------|-------------|-------|
| Technológia | **Web (React + FastAPI)** | Viď sekcia 3 |
| Multi-monitor | Len jeden monitor | Nie je potrebný |
| Limit tabov | Bez limitu | Používateľ si spravuje sám |
| SALLY (eKasa) | **PySide6** | Samostatný projekt |

## 2. Prehľad projektov

| Projekt | Technológia | Účel |
|---------|-------------|------|
| NEX Automat | Web (React + FastAPI) | ERP systém, Module Manager |
| SALLY | PySide6 | Elektronická registračná pokladňa |

## 3. Zdôvodnenie výberu Web technológie

### 3.1 Analýza prostredia zákazníkov

| Faktor | Hodnota | Vyhovuje |
|--------|---------|----------|
| Počet používateľov | do 20 | Web ✅ |
| Pracovné miesto | kancelária + remote | Web ✅ |
| Počítače | rôzne (staršie aj novšie) | Web ✅ |
| Klávesové skratky | nie sú kritické | Web ✅ |
| Tlač dokladov | málo, väčšina elektronicky | Web ✅ |
| Multi-monitor | nepotrebný | Web ✅ |

### 3.2 Výhody Web riešenia

| Výhoda | Popis |
|--------|-------|
| **Žiadna inštalácia** | Zákazník otvorí browser a pracuje |
| **Automatické aktualizácie** | Deploy na server = všetci majú novú verziu |
| **Remote prístup** | Práca z domu bez VPN/RDP |
| **Rôzne zariadenia** | Windows, Mac, Linux, tablet |
| **Moderné UI** | React ekosystém, komponenty, animácie |
| **Jednoduchšia údržba** | Jeden server, nie 20 inštalácií |

### 3.3 Technologický stack

| Vrstva | Technológia |
|--------|-------------|
| Frontend | React + TypeScript |
| UI komponenty | Tailwind CSS + shadcn/ui |
| State management | Zustand alebo React Query |
| Backend API | FastAPI (Python) |
| Databáza | PostgreSQL |
| Autentifikácia | JWT tokeny |
| Workflow engine | Temporal.io |
| Cache | Redis |

## 4. Architektúra Web aplikácie

```
┌─────────────────────────────────────────────────────────────┐
│                      BROWSER                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 React Frontend                         │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                 │  │
│  │  │ Sidebar │ │ Tab Bar │ │ Content │                 │  │
│  │  └─────────┘ └─────────┘ └─────────┘                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                      HTTPS/WSS
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       SERVER                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  FastAPI Backend                       │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                 │  │
│  │  │   API   │ │  Auth   │ │ Business│                 │  │
│  │  │ Routes  │ │ Service │ │  Logic  │                 │  │
│  │  └─────────┘ └─────────┘ └─────────┘                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ PostgreSQL  │    │  Temporal   │    │    Redis    │     │
│  │  Database   │    │  Workflows  │    │   (cache)   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 5. Manažér programových modulov

### 5.1 Čo to je?

Centrálny komponent, ktorý:
- Eviduje všetky dostupné moduly (41+)
- Kontroluje licencie a práva
- Spravuje otvorené moduly (taby)
- Poskytuje navigáciu a vyhľadávanie

### 5.2 Hlavné funkcie

| Funkcia | Popis |
|---------|-------|
| **Registrácia** | Každý modul sa zaregistruje s metadátami |
| **Licenčná kontrola** | Overí, či zákazník má modul zakúpený |
| **Prístupová kontrola** | Overí, či používateľ má právo vstúpiť |
| **Otvorenie modulu** | Vytvorí nový tab alebo aktivuje existujúci |
| **Multi-instance** | Umožní otvoriť ten istý modul viackrát |
| **Zatvorenie** | Kontrola neuložených zmien pred zatvorením |

### 5.3 Workflow otvorenia modulu

```
Používateľ klikne na modul (sidebar/command palette)
         │
         ▼
┌─────────────────────────┐
│ Licenčná kontrola       │ → Nemá licenciu → Zobraziť info
└─────────────────────────┘
         │ OK
         ▼
┌─────────────────────────┐
│ Prístupová kontrola     │ → Nemá právo → Zobraziť info
└─────────────────────────┘
         │ OK
         ▼
┌─────────────────────────┐
│ Už je otvorený?         │ → Áno → Aktivovať existujúci tab
└─────────────────────────┘        (alebo otvoriť nový ak multi-instance)
         │ Nie
         ▼
┌─────────────────────────┐
│ Vytvoriť nový tab       │
│ Načítať dáta modulu     │
│ Zobraziť UI             │
└─────────────────────────┘
```

### 5.4 Kategórie modulov

| Kategória | Ikona | Príklady |
|-----------|-------|----------|
| Bázová evidencia | 📋 | Tovar, Partneri, Váhy |
| Obchodná činnosť | 💼 | Cenníky, Akcie, Zmluvy |
| Zásobovanie | 🛒 | Objednávky, Dodacie listy, Faktúry dodávateľov |
| Sklad | 📦 | Skladové karty, Príjemky, Výdajky, Presuny |
| Odbyt | 💰 | Ponuky, Zákazky, Dodacie listy, Faktúry |
| Pokladnice | 🏪 | Konfigurácia, Predaj, Uzávierky |
| Účtovníctvo | 📊 | Denník, Predvaha, Interné doklady, DPH |
| Systém | ⚙️ | Nastavenia, Používatelia, Údržba |

### 5.5 Typy modulov

| Typ | Charakteristika | Príklady |
|-----|-----------------|----------|
| **Katalógový** | Master data, jeden zoznam | GSC (tovar), PAB (partneri) |
| **Dokladový** | Knihy, hlavičky + položky | ICB (faktúry), IMB (príjemky) |
| **Výkazový** | Generované zostavy | ACT (predvaha), VTR (DPH) |
| **Konfiguračný** | Nastavenia systému | KEY (parametre), SYS (systém) |

### 5.6 Životný cyklus modulu

| Fáza | Popis |
|------|-------|
| **Registrácia** | Pri štarte aplikácie sa modul zaregistruje |
| **Otvorenie** | Vytvorenie UI, načítanie dát |
| **Aktivácia** | Tab sa stane aktívnym (prepnutie) |
| **Deaktivácia** | Tab stratí fokus |
| **Zatvorenie** | Kontrola zmien, uvoľnenie zdrojov |

## 6. Integrácia s NEX Genesis

| Aspekt | Riešenie |
|--------|----------|
| Paralelný beh | Nie, NEX Genesis zostáva len ako archív |
| Migrácia dát | Jednorázový import do PostgreSQL |
| Prístup k archívu | Read-only pripojenie na Btrieve (ak potrebné) |

## 7. Mock moduly (aktuálna fáza)

V aktuálnej fáze budú všetky moduly mock - zobrazia len informáciu:

```
┌─────────────────────────────────────────┐
│  📦 GSC - Evidencia tovaru              │
│                                         │
│  Tento modul bude implementovaný        │
│  v ďalšej fáze projektu.                │
│                                         │
│  Plánované funkcie:                     │
│  • Katalóg tovaru a služieb             │
│  • Cenníky a akcie                      │
│  • Import/Export                        │
│                                         │
└─────────────────────────────────────────┘
```