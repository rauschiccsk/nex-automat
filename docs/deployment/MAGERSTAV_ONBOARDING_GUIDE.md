# NEX Automat - Návod na používanie
## Automatické spracovanie dodávateľských faktúr

**Zákazník:** Mágerstav s.r.o.  
**Systém:** NEX Automat v2.0 - Supplier Invoice Loader  
**Verzia:** 1.0  
**Dátum:** 2. december 2025

---

## Ako to funguje?

NEX Automat automaticky spracováva faktúry od dodávateľov, ktoré prídu emailom. Systém:

1. ✅ Prijme email s faktúrou (PDF príloha)
2. ✅ Extrahuje údaje z faktúry (dodávateľ, číslo faktúry, suma...)
3. ✅ Uloží faktúru do databázy
4. ✅ Vytvorí ISDOC XML súbor pre NEX Genesis
5. ✅ Pripraví faktúru na import do NEX Genesis systému

**Všetko prebieha automaticky bez zásahu človeka.**

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
- Veľkosť: do 10 MB
- Štruktúra: Slovenské faktúry s IČO, DIČ, číslo faktúry

### ⚠️ Nepodporované:
- Obrázky faktúr (JPG, PNG) - prosím skonvertujte na PDF
- Word dokumenty (DOC, DOCX)
- Excel súbory (XLS, XLSX)
- Zipované súbory

---

## Ako zistím že faktúra bola spracovaná?

### Spôsob 1: Automatické potvrdenie (Plánované)

V budúcnosti dostanete automatický email s potvrdením, že faktúra bola úspešne spracovaná.

### Spôsob 2: Kontaktovať podporu

Ak potrebujete overiť že faktúra bola spracovaná, kontaktujte:

**Podpora:**  
Email: rausch@icc.sk  
Tel: +421 ...

---

## Čo sa stane s faktúrou?

Po úspešnom spracovaní:

1. **PDF faktúra** - uložená na serveri
2. **ISDOC XML** - vygenerovaný pre NEX Genesis
3. **Databázový záznam** - vytvorený v SQLite
4. **PostgreSQL staging** - pripravená na import do NEX Genesis

**Faktúra je pripravená na import do NEX Genesis systému.**

---

## Časté otázky (FAQ)

### Môžem odoslať jednu faktúru viackrát?

Áno, systém automaticky deteguje duplicitné faktúry. Ak odošlete tú istú faktúru 2x, systém ju spracuje len raz a o duplicite vás informuje.

### Ako dlho trvá spracovanie?

Typicky **30-60 sekúnd** po odoslaní emailu. Pre veľké faktúry (5+ MB) to môže trvať až 2 minúty.

### Čo ak príde chybný email?

Systém spracováva len PDF prílohy. Ak email nemá PDF prílohu alebo PDF nie je faktúra, systém ho ignoruje.

### Môžem odoslať viac faktúr naraz?

Áno, môžete priložiť viac PDF súborov do jedného emailu. Každá faktúra bude spracovaná samostatne.

### Funguje to aj cez víkend?

Áno, systém beží 24/7 a spracováva faktúry kedykoľvek prídu.

---

## Čo robiť ak nastane problém?

### Príznaky problému:

- Faktúra nebola spracovaná po 5 minútach
- Dostali ste error email od systému
- Faktúra má nesprávne údaje

### Postup pri probléme:

1. **Počkajte 5 minút** - systém môže byť dočasne zaneprázdnený
2. **Skúste odoslať znova** - možno bol problém dočasný
3. **Kontaktujte podporu:**
   - Email: **rausch@icc.sk**
   - Telefón: **+421 ...**
   - Pošlite:
     - Pôvodnú faktúru (PDF)
     - Čas kedy ste ju odoslali
     - Popis problému

**Podpora odpovie do 24 hodín.**

---

## Technické detaily (Pre IT oddelenie)

### Systémová architektúra:

- **Email endpoint:** magerstavinvoice@gmail.com
- **n8n Workflow:** n8n-SupplierInvoiceEmailLoader (ICC Server)
- **API endpoint:** https://magerstav-invoices.icc.sk
- **Service:** NEXAutomat (Windows Service na Magerstav serveri)
- **Database:** SQLite + PostgreSQL staging
- **Monitoring:** Health check - https://magerstav-invoices.icc.sk/health

### Zálohovanie:

- PDF faktúry: `C:\Deployment\nex-automat\data\pdf\`
- XML súbory: `C:\Deployment\nex-automat\data\xml\`
- SQLite DB: `C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\invoices.db`

### Error notifikácie:

Email notifikácie o chybách sú zasielané na: **rausch@icc.sk**

### API Key:

Pre prístup k API používa n8n workflow API key: `magerstav-PWjo...`

---

## História zmien

### Verzia 1.0 (2. december 2025)
- Prvé nasadenie do produkcie
- Základná funkcionalita spracovávania faktúr
- Automatická detekcia duplicitných faktúr
- Integrácia s NEX Genesis cez PostgreSQL staging

---

## Kontakt

**ICC Komárno - NEX Automat Support**

📧 Email: rausch@icc.sk  
🌐 Web: https://icc.sk  
📍 Adresa: ICC Komárno, Komárno, Slovakia

---

**Ďakujeme že používate NEX Automat!** 🚀