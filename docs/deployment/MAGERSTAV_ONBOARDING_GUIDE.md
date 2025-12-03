# NEX Automat - Návod na používanie
## Automatické spracovanie dodávateľských faktúr

**Zákazník:** Mágerstav s.r.o.  
**Systém:** NEX Automat v2.1 - Supplier Invoice Loader  
**Verzia:** 2.1  
**Dátum:** 2. december 2025  
**Status:** ✅ Production

---

## Ako to funguje?

NEX Automat automaticky spracováva faktúry od dodávateľov, ktoré prídu emailom. Systém:

1. ✅ Prijme email s faktúrou (PDF príloha)
2. ✅ Extrahuje údaje z faktúry (dodávateľ, číslo faktúry, suma...)
3. ✅ Uloží faktúru do databázy
4. ✅ Vytvorí ISDOC XML súbor pre NEX Genesis
5. ✅ Pripraví faktúru na import do NEX Genesis systému
6. ✅ Zobrazí faktúru v desktop aplikácii pre manuálnu kontrolu

**Všetko prebieha automaticky bez zásahu človeka.**

---

## Desktop Aplikácia - NEX Správa faktúr

### Čo je to?

**NEX - Správa faktúr** je desktop aplikácia pre prehľad a manuálnu kontrolu spracovaných faktúr.

### Ako spustiť?

Na desktop obrazovke **double-click** na ikonu:

```
🖥️ NEX - Správa faktúr
```

### Čo dokáže?

- 📋 **Zobrazenie všetkých faktúr** - prehľad všetkých spracovaných faktúr
- 🔍 **Detail faktúry** - zobrazenie všetkých extrahovaných údajov
- 📄 **Náhľad PDF** - priame otvorenie pôvodnej faktúry
- 📊 **Štatistiky** - prehľad počtu faktúr, súm, dodávateľov
- 🔄 **Export do NEX Genesis** - manuálny export vybraných faktúr (plánované)

### Ako používať?

1. **Spustite aplikáciu** - double-click na desktop ikonu
2. **Zoznam faktúr** - vľavo sa zobrazí zoznam všetkých faktúr
3. **Kliknite na faktúru** - vpravo sa zobrazí detail
4. **Tlačidlá:**
   - **Otvoriť PDF** - zobrazí pôvodnú faktúru
   - **Otvoriť XML** - zobrazí ISDOC XML súbor
   - **Export** - (plánované) export do NEX Genesis

---

## Ako odoslať faktúru na spracovanie?

### Spôsob 1: Forward Email (Odporúčaný)

Keď vám príde faktúra od dodávateľa na váš firemný email:

1. Otvorte email s faktúrou
2. Kliknite na **"Preposlať"** / **"Forward"**
3. Do poľa **"Komu"** napíšte: **magerstavinvoice@gmail.com**
4. Kliknite **"Odoslať"**

**Hotovo!** Systém ju automaticky spracuje do 1-2 minút.

### Spôsob 2: Direct Email (Pre manuálne faktúry)

Ak máte faktúru ako PDF súbor na počítači:

1. Vytvorte nový email
2. Do poľa **"Komu"** napíšte: **magerstavinvoice@gmail.com**
3. Do poľa **"Predmet"** napíšte čokoľvek (napr. "Faktúra od dodávateľa")
4. Priložte PDF súbor faktúry
5. Kliknite **"Odoslať"**

---

## Požiadavky na faktúru

### ✅ Podporované formáty:
- PDF súbory (`.pdf`)
- Veľkosť: do 10 MB (priemerná faktúra ~0.5 MB)
- Štruktúra: Slovenské faktúry s IČO, DIČ, číslo faktúry

### ⚠️ Nepodporované:
- Obrázky faktúr (JPG, PNG) - prosím skonvertujte na PDF
- Word dokumenty (DOC, DOCX)
- Excel súbory (XLS, XLSX)
- Zipované súbory

---

## Ako zistím že faktúra bola spracovaná?

### Spôsob 1: Desktop Aplikácia (Odporúčaný)

1. Spustite **"NEX - Správa faktúr"** z desktopovej ikony
2. Faktúra sa zobrazí v zozname (refresh automaticky)
3. Kliknite na faktúru pre detail

### Spôsob 2: Automatické potvrdenie (Plánované)

V budúcnosti dostanete automatický email s potvrdením, že faktúra bola úspešne spracovaná.

### Spôsob 3: Kontaktovať podporu

Ak potrebujete overiť že faktúra bola spracovaná, kontaktujte:

**Podpora:**  
📧 Email: rausch@icc.sk  
📞 Tel: +421905354536 (ICC Komárno)

---

## Čo sa stane s faktúrou?

Po úspešnom spracovaní:

1. **PDF faktúra** - uložená na serveri
2. **ISDOC XML** - vygenerovaný pre NEX Genesis
3. **SQLite databáza** - vytvorený záznam pre históriu
4. **PostgreSQL staging** - pripravená na import do NEX Genesis
5. **Desktop aplikácia** - zobrazená v zozname faktúr

**Faktúra je pripravená na import do NEX Genesis systému.**

---

## Časté otázky (FAQ)

### Môžem odoslať jednu faktúru viackrát?

Áno, systém automaticky deteguje duplicitné faktúry. Ak odošlete tú istú faktúru 2x, systém ju spracuje len raz a o duplicite vás informuje. **Duplicate detection je plne funkčný od verzie 2.1.**

### Ako dlho trvá spracovanie?

Typicky **30-60 sekúnd** po odoslaní emailu. Pre veľké faktúry (5+ MB) to môže trvať až 2 minúty.

### Čo ak príde chybný email?

Systém spracováva len PDF prílohy. Ak email nemá PDF prílohu alebo PDF nie je faktúra, systém ho ignoruje.

### Môžem odoslať viac faktúr naraz?

Áno, môžete priložiť viac PDF súborov do jedného emailu. Každá faktúra bude spracovaná samostatne.

### Funguje to aj cez víkend?

Áno, systém beží 24/7 a spracováva faktúry kedykoľvek prídu.

### Môžem upraviť faktúru v desktop aplikácii?

Aktuálne nie - aplikácia je len na prezeranie. Úprava a export do NEX Genesis je plánovaný v budúcich verziách.

### Kde sa ukladajú faktúry?

Všetky faktúry sú bezpečne uložené na serveri v Mágerstav kancelárii. Zálohuje sa automaticky.

---

## Čo robiť ak nastane problém?

### Príznaky problému:

- Faktúra nebola spracovaná po 5 minútach
- Dostali ste error email od systému
- Faktúra má nesprávne údaje
- Desktop aplikácia sa nespustí
- Faktúra sa nezobrazuje v aplikácii

### Postup pri probléme:

1. **Počkajte 5 minút** - systém môže byť dočasne zaneprázdnený
2. **Refresh desktop aplikácie** - zatvorte a znova spustite
3. **Skúste odoslať znova** - možno bol problém dočasný
4. **Kontaktujte podporu:**
   - 📧 Email: **rausch@icc.sk**
   - 📞 Telefón: **+421 35 7731 221**
   - Pošlite:
     - Pôvodnú faktúru (PDF)
     - Čas kedy ste ju odoslali
     - Screenshot chyby (ak je)
     - Popis problému

**Podpora odpovie do 24 hodín v pracovných dňoch.**

---

## Bezpečnosť a ochrana údajov

### Kde sú moje dáta?

- Všetky faktúry sú uložené **lokálne na vašom serveri** v kancelárii
- Žiadne dáta sa neposielajú do cloudu (okrem Gmail emailu)
- Prístup k serveru majú len autorizovaní zamestnanci

### Kto má prístup k faktúram?

- Len zamestnanci Mágerstav s.r.o. s prístupom na server
- ICC Komárno (technická podpora) - len na požiadanie pre troubleshooting

### Ako sú chránené heslá?

- Všetky heslá sú šifrované
- API kľúče sú generované náhodne
- Prístup k databáze je chránený heslom

---

## Technické detaily (Pre IT oddelenie)

### Systémová architektúra:

- **Email endpoint:** magerstavinvoice@gmail.com
- **n8n Workflow:** n8n-SupplierInvoiceEmailLoader (ICC Server)
- **API endpoint:** https://magerstav-invoices.icc.sk
- **Service:** NEXAutomat (Windows Service na Magerstav serveri)
- **Database:** SQLite + PostgreSQL staging
- **Desktop App:** PyQt5 GUI (Python 3.13)
- **Monitoring:** Health check - https://magerstav-invoices.icc.sk/health

### Lokácie súborov (Magerstav Server):

```
C:\Deployment\nex-automat\
├── apps\
│   ├── supplier-invoice-loader\        # Backend service
│   │   ├── config\invoices.db          # SQLite databáza
│   │   ├── data\pdf\                   # PDF faktúry
│   │   └── data\xml\                   # ISDOC XML súbory
│   │
│   └── supplier-invoice-editor\        # Desktop aplikácia
│       ├── config\config.yaml          # Konfigurácia
│       └── logs\                       # Logy aplikácie
│
└── logs\                               # Service logy
```

### Zálohovanie:

- **PDF faktúry:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\data\pdf\`
- **XML súbory:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\data\xml\`
- **SQLite DB:** `C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\invoices.db`
- **PostgreSQL:** Automatické zálohovanie PostgreSQL 15
- **Odporúčanie:** Backup celého `C:\Deployment\nex-automat\` daily

### Error notifikácie:

Email notifikácie o chybách sú zasielané na: **rausch@icc.sk**

### API Key:

Pre prístup k API používa n8n workflow API key: `magerstav-PWjo...` (nie je potrebné poznať)

### Windows Services:

```
NEXAutomat           - Invoice processing service
postgresql-x64-15    - Database server
CloudflaredMagerstav - Tunnel service (public access)
```

Všetky služby sú nastavené na **Automatic** start.

### Monitoring:

```bash
# Health check (curl alebo prehliadač)
https://magerstav-invoices.icc.sk/health

# Expected response:
{"status":"healthy","timestamp":"2025-12-02T..."}
```

### Reštart služieb (ak potrebné):

```powershell
# PowerShell (Run as Administrator)
Restart-Service NEXAutomat
Get-Service NEXAutomat  # Verify Running
```

---

## História zmien

### Verzia 2.1 (2. december 2025) - Production
- ✅ **Oprava duplicate detection** - duplicitné faktúry sa teraz správne detegujú
- ✅ **Desktop aplikácia** - pridaná "NEX - Správa faktúr" s desktop ikonou
- ✅ **PostgreSQL staging** - faktúry pripravené pre NEX Genesis import
- ✅ **Kompletné testovanie** - all tests passed, 0 chýb v produkcii
- ✅ **Dokumentácia** - kompletný návod pre používateľov a IT

### Verzia 1.0 (November 2025) - Initial
- Prvé nasadenie do produkcie
- Základná funkcionalita spracovávania faktúr
- Integrácia s NEX Genesis cez PostgreSQL staging

---

## Plánované vylepšenia (Roadmap)

### Verzia 2.2 (Q1 2026)
- 📧 Automatické potvrdzovacie emaily po spracovaní
- 📊 Denný sumárny report emailom
- 🔄 Export do NEX Genesis priamo z desktop aplikácie

### Verzia 2.3 (Q2 2026)
- ✏️ Úprava faktúr v desktop aplikácii (pred exportom)
- 🔍 Pokročilé vyhľadávanie a filtrovanie
- 📈 Štatistiky a grafy (dodávatelia, sumy, trendy)

### Verzia 3.0 (Q3 2026)
- 🔄 Automatická synchronizácia s NEX Genesis
- 🌐 Web dashboard (alternatíva k desktop aplikácii)
- 📱 Mobilná aplikácia pre schvaľovanie faktúr

---

## Kontakt

**ICC Komárno - NEX Automat Support**

📧 Email: rausch@icc.sk  
📞 Tel: +421905354536  
🌐 Web: https://icc.sk  
📍 Adresa: ICC Komárno, Komárno, Slovakia

**Pracovné hodiny:**
- Pondelok - Piatok: 8:00 - 16:00
- Víkend: Email support (odpoveď v pracovný deň)

**Emergency kontakt:** rausch@icc.sk (24/7 pre kritické problémy)

---

## Prílohy

### Príloha A: Ukážkový email pre odoslanie faktúry

```
Komu: magerstavinvoice@gmail.com
Predmet: Faktúra od dodávateľa XY
Prílohy: faktura_12345.pdf

Text emailu (voliteľný):
Faktúra č. 12345 od dodávateľa XY.
```

### Príloha B: Screenshot desktop aplikácie

(Dostupné v desktop aplikácii - Help → Documentation)

### Príloha C: Podporované PDF formáty

- PDF/A (odporúčané pre archiváciu)
- PDF 1.4 - 1.7
- Textové PDF (nie skenované obrázky)

---

## Záver

**NEX Automat v2.1** je plne funkčný systém pre automatické spracovanie dodávateľských faktúr.

**Pre bežné používanie:**
1. Posielajte faktúry na **magerstavinvoice@gmail.com**
2. Sledujte spracované faktúry v **"NEX - Správa faktúr"** desktop aplikácii
3. Pri problémoch kontaktujte **rausch@icc.sk**

**Systém beží 24/7 a je plne automatický.**

---

**Ďakujeme že používate NEX Automat!** 🚀

**Verzia dokumentu:** 2.1  
**Posledná aktualizácia:** 2. december 2025  
**Status:** ✅ Production Ready  
**Autor:** ICC Komárno Development Team