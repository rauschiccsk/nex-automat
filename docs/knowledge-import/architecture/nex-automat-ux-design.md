# NEX Automat - UX Design

## 1. Prehľad

| Parameter | Hodnota |
|-----------|---------|
| Platforma | Web (React + TypeScript) |
| Min. rozlíšenie | 1366×768 |
| Cieľové zariadenia | Desktop (notebook, monitor) |
| Farebná schéma | Svetlá + tmavá (toggle) |
| Primárna farba | Modrá |
| Hustota UI | Vzdušná (moderná) |

## 2. Hlavné okno - Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Logo    NEX Automat              🔔  👤 Ján Kováč  ☀️/🌙  │ Header │
├─────────┬───────────────────────────────────────────────────────────┤
│         │ [GSC Tovar] [ICB Faktúry] [PAB Partneri]        [×]      │
│ Sidebar ├───────────────────────────────────────────────────────────┤
│         │ Sklad > Príjemky > PR-2024-00123              Breadcrumbs │
│  📋     ├───────────────────────────────────────────────────────────┤
│  Bázová │                                                           │
│         │                                                           │
│  📦     │                      Content Area                         │
│  Sklad  │                                                           │
│         │                      (aktívny modul)                      │
│  💰     │                                                           │
│  Odbyt  │                                                           │
│         │                                                           │
│  ⭐     │                                                           │
│ Obľúbené│                                                           │
│         │                                                           │
│  🕐     │                                                           │
│ Nedávne │                                                           │
├─────────┴───────────────────────────────────────────────────────────┤
│ > of                                                    Command Line│
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Komponenty hlavného okna

| Komponent | Pozícia | Popis |
|-----------|---------|-------|
| Header | Hore | Logo, názov, notifikácie, používateľ, dark mode |
| Sidebar | Vľavo | Kategórie modulov, obľúbené, nedávne |
| Tab bar | Pod headerom | Otvorené moduly (Chrome štýl) |
| Breadcrumbs | Pod tab bar | Navigačná cesta v module |
| Content | Stred | Obsah aktívneho modulu |
| Command Line | Dole | Rýchle príkazy a skratky |

### 2.2 Sidebar

| Vlastnosť | Hodnota |
|-----------|---------|
| Pozícia | Ľavá strana |
| Šírka | Nastaviteľná (drag) |
| Zbaliteľnosť | Áno (collapse na ikony) |
| Min. šírka | 48px (len ikony) |
| Max. šírka | 300px |
| Default | 220px |

**Sekcie sidebaru:**

| Sekcia | Ikona | Obsah |
|--------|-------|-------|
| Kategórie | 📋📦💰... | Stromová štruktúra modulov |
| Obľúbené | ⭐ | Používateľom označené moduly |
| Nedávne | 🕐 | Posledných 10 otvorených modulov |

### 2.3 Tab bar

| Vlastnosť | Hodnota |
|-----------|---------|
| Štýl | Chrome-like |
| Pozícia | Pod headerom |
| Limit tabov | Bez limitu |
| Scroll | Horizontálny ak veľa tabov |
| Zatváranie | Tlačidlo × na tabe |
| Reordering | Drag & drop |

## 3. Command Line

Spodná lišta pre rýchle príkazy. Aktivuje sa automaticky pri písaní.

### 3.1 Fungovanie

| Akcia | Výsledok |
|-------|----------|
| Začnem písať | Fokus na command line |
| `of` + Enter | Otvorí modul podľa skratky |
| `Esc` | Zruší command line |
| `/help` | Zobrazí nápovedu |

### 3.2 Príklady skratiek (default)

| Skratka | Modul |
|---------|-------|
| `of` | Odberateľské faktúry (ICB) |
| `df` | Dodávateľské faktúry (ISB) |
| `tov` | Evidencia tovaru (GSC) |
| `par` | Evidencia partnerov (PAB) |
| `skl` | Skladové karty (STK) |
| `pri` | Príjemky (IMB) |
| `vyd` | Výdajky (OMB) |

### 3.3 Konfigurácia skratiek

Používateľ môže zmeniť skratky v nastaveniach. Ukladajú sa per-user.

## 4. Komponenty

### 4.1 Lookup popup (výber záznamu)

Kombinácia dropdown + modal pre výber partnera, tovaru, atď.

**Rýchly výber (dropdown):**
```
┌─────────────────────────────────┐
│ Partner: [ANDR              🔍] │
│          ┌─────────────────────┐│
│          │ ANDROS s.r.o.       ││
│          │ ALFA Trading        ││
│          │ ─────────────────── ││
│          │ 🔎 Rozšírené hľadanie││
│          └─────────────────────┘│
└─────────────────────────────────┘
```

**Rozšírené hľadanie (modal):**
```
┌─────────────────────────────────────────────────────────────┐
│ Výber partnera                                          [×] │
├─────────────────────────────────────────────────────────────┤
│ Hľadať: [                    ] [Hľadaj]                     │
│                                                             │
│ Filtre: [Odberatelia ▼] [Aktívni ▼] [Región ▼]             │
├─────────────────────────────────────────────────────────────┤
│ Kód      │ Názov              │ IČO        │ Mesto         │
│──────────┼────────────────────┼────────────┼───────────────│
│ ANDR     │ ANDROS s.r.o.      │ 12345678   │ Komárno       │
│ ALFA     │ ALFA Trading       │ 87654321   │ Bratislava    │
│ BETA     │ BETA s.r.o.        │ 11223344   │ Košice        │
├─────────────────────────────────────────────────────────────┤
│                               [Zrušiť]  [Vybrať]            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Info panel (detail záznamu)

Pozícia: Pravá strana content area (slide-in panel).

```
┌────────────────────────────────────┬──────────────────────┐
│                                    │ Detail partnera   [×]│
│         Zoznam partnerov           ├──────────────────────┤
│                                    │ ANDROS s.r.o.        │
│  [ANDR] ANDROS s.r.o.    ◀ selected│                      │
│  [ALFA] ALFA Trading               │ IČO: 12345678        │
│  [BETA] BETA s.r.o.                │ DIČ: 2012345678      │
│                                    │ IČ DPH: SK2012345678 │
│                                    │                      │
│                                    │ Adresa:              │
│                                    │ Hlavná 123           │
│                                    │ 945 01 Komárno       │
│                                    │                      │
│                                    │ Kontakt:             │
│                                    │ 📧 info@andros.sk    │
│                                    │ 📞 +421 35 123 456   │
└────────────────────────────────────┴──────────────────────┘
```

| Vlastnosť | Hodnota |
|-----------|---------|
| Šírka | 300-400px |
| Animácia | Slide-in z pravej strany |
| Zatváranie | Tlačidlo × alebo Esc |
| Resize | Nie |

### 4.3 Notifikácie

**Toast (úspech, info):**
```
                                    ┌────────────────────────┐
                                    │ ✅ Faktúra uložená     │
                                    │    ICB-2024-00456      │
                                    └────────────────────────┘
```

| Vlastnosť | Hodnota |
|-----------|---------|
| Pozícia | Pravý horný roh |
| Trvanie | 3-5 sekúnd |
| Typy | success, info, warning, error |
| Stack | Max 3 naraz |

**Inline (chyby, validácia):**
```
┌─────────────────────────────────────┐
│ IČO: [123456789              ]      │
│      ⚠️ IČO musí mať 8 číslic       │
└─────────────────────────────────────┘
```

## 5. Klávesové skratky

### 5.1 Globálne (vždy fungujú)

| Skratka | Akcia |
|---------|-------|
| `Esc` | Zavrieť modal/panel, zrušiť akciu |
| `Ctrl+S` | Uložiť |
| `Ctrl+W` | Zavrieť aktívny tab |
| `Ctrl+Tab` | Ďalší tab |
| `Ctrl+Shift+Tab` | Predchádzajúci tab |
| `Ctrl+1..9` | Prepnúť na tab 1-9 |

### 5.2 V module (konfigurovateľné)

| Skratka (default) | Akcia |
|-------------------|-------|
| `Ctrl+N` | Nový záznam |
| `Ctrl+E` | Editovať |
| `Delete` | Zmazať (s potvrdením) |
| `Ctrl+F` | Hľadať |
| `Ctrl+P` | Tlač |
| `Enter` | Otvoriť/potvrdiť |

### 5.3 Konfigurácia

Používateľ môže zmeniť skratky v Nastavenia > Klávesové skratky. Systém kontroluje konflikty.

## 6. Dark Mode

| Prvok | Light | Dark |
|-------|-------|------|
| Pozadie | #FFFFFF | #1E1E1E |
| Pozadie sidebar | #F5F5F5 | #252525 |
| Text | #1A1A1A | #E0E0E0 |
| Primárna | #2563EB | #3B82F6 |
| Border | #E5E5E5 | #404040 |

Toggle v headeri (ikona ☀️/🌙). Ukladá sa do preferencií používateľa.

## 7. Responzivita

| Rozlíšenie | Správanie |
|------------|-----------|
| < 1366px | Nie je podporované |
| 1366×768 | Sidebar default collapsed |
| 1920×1080+ | Plný layout |

## 8. Rozhodnutia

| Otázka | Rozhodnutie |
|--------|-------------|
| Sidebar pozícia | Ľavá |
| Sidebar šírka | Nastaviteľná (48-300px) |
| Tab bar | Chrome štýl, pod headerom |
| Dark mode | Áno, toggle |
| Command line | Dole, auto-focus pri písaní |
| Lookup popup | Dropdown + modal kombinácia |
| Info panel | Pravý slide-in panel |
| Notifikácie | Toast + inline |
| Klávesové skratky | Moderné, konfigurovateľné |
| Min. rozlíšenie | 1366×768 |