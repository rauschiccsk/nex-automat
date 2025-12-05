# AI/ML Tools - Technológie pre zlepšenie umelej inteligencie

**Dokument:** Schválené AI/ML technológie pre NEX Automat  
**Projekty:** NEX Automat v2.0, NEX Genesis  
**Vytvorené:** 2024-12-04  
**Status:** SCHVÁLENÉ NA IMPLEMENTÁCIU

---

## Úvod

Tento dokument obsahuje technológie pre zlepšenie AI/ML funkcií v NEX Automat. Všetky technológie priamo súvisia so Supplier Classifier projektom a ďalšími ML funkciami.

**Celkový počet:** 4 technológie  
**Celkové náklady:** €12-240/rok (Claude API voliteľne podľa použitia)  
**Časový rámec implementácie:** Fázy 2-4 (po základnom Supplier Classifier)

---

## Prehľadová tabuľka

| Technológia | Účel | Priorita | Náklady | Zložitosť | Benefit |
|-------------|------|----------|---------|-----------|---------|
| **PaddleOCR** | Lepší OCR | 🟡 Stredná | FREE | Nízka | Vyššia presnosť OCR |
| **Camelot** | Extrakcia tabuliek | 🔥 Vysoká | FREE | Nízka | Automatická extrakcia položiek |
| **Claude API** | Inteligentná validácia | 🟡 Stredná | €12-240/rok | Nízka | 99%+ presnosť celkovo |
| **DuckDB** | Rýchle analýzy | 🟡 Stredná-Vysoká | FREE | Nízka | 10-100x rýchlejšie SQL |

---

## 1. PaddleOCR

### Základné informácie

**Typ:** OCR nástroj (rozpoznávanie textu z obrázkov)  
**Účel:** Možno lepšia alternatíva k Tesseract pre rozpoznávanie textu na faktúrach  
**Priorita:** 🟡 STREDNÁ  
**Náklady:** ZADARMO (open-source)

### Popis

PaddleOCR je open-source OCR nástroj od čínskej firmy Baidu. Je často presnejší než Tesseract, najmä pri faktúrach zlej kvality (rozmazané, šikmé, s rušivým pozadím).

**Základný rozdiel oproti Tesseract:**
- **Tesseract:** Starší, overený, funguje dobre na čistých dokumentoch
- **PaddleOCR:** Novší, často lepší na horších dokumentoch

**Kedy je PaddleOCR lepší:**
- Zlá kvalita skenu (rozmazané, tmavé)
- Šikmé faktúry (nie sú rovné)
- Rôzne veľkosti písma na jednej stránke
- Zložité pozadie

### Použitie pre NEX Automat / Genesis

**Hlavný use case:**

Máš Tesseract, ktorý funguje OK (povedzme 90% presnosť). PaddleOCR by mohol zvýšiť presnosť na 95%.

**Stratégia použitia (2 možnosti):**

**Možnosť A: Náhrada Tesseract**
- Nahradiť Tesseract s PaddleOCR úplne
- Ak PaddleOCR je konzistentne lepší na tvojich faktúrach

**Možnosť B: Kombinovaný prístup (odporúčam)**
- Primárne: Tesseract (rýchly, overený)
- Fallback: Ak Tesseract má nízku istotu → skús PaddleOCR
- Využívaš výhody oboch

**Implementácia:**
```
1. Faktúra príde
2. Tesseract OCR (rýchle)
3. Ak text je krátky alebo nekvalitný:
   → Spusti PaddleOCR (pomalšie, ale presnejšie)
4. Použi lepší výsledok
```

### Výhody

✅ **Možno lepšia presnosť** - hlavne na zlých skenoch  
✅ **Zadarmo a open-source**  
✅ **Malé modely** - ~10 MB vs 100 MB Tesseract  
✅ **Podpora GPU** - ak by si mal, zrýchli 10x  
✅ **Jednoduché použitie** - podobné API ako Tesseract

### Nevýhody

⚠️ **Nemusí byť vždy lepší** - závisí od kvality tvojich faktúr  
⚠️ **Čínska dokumentácia** - ale anglická existuje tiež  
⚠️ **Menšia komunita** - než Tesseract (ale stále aktívna)

### Technické požiadavky

**RAM:** ~200-500 MB počas OCR  
**CPU:** Podobné ako Tesseract  
**Inštalácia:** pip install paddleocr  
**Čas nastavenia:** 30 minút inštalácia + 2-3 hodiny testovanie  
**Prvý benefit:** Po otestovaní na reálnych faktúrach

### Stratégia implementácie

**Fáza 1: Testovanie (týždeň)**
- Vyber 100 reprezentatívnych faktúr
- Spusti Tesseract na všetkých
- Spusti PaddleOCR na všetkých
- Porovnaj presnosť
- Rozhodnutie: použiť alebo nie?

**Fáza 2: Integrácia (ak je lepší)**
- Integrovať do AI Service
- Nastaviť fallback logiku
- Testovať v produkcii

### Rozhodnutie

**✅ OTESTOVAŤ A POTOM ROZHODNÚŤ**

Určite stojí za to otestovať. Ak je PaddleOCR lepší na tvojich faktúrach, použiť ho. Ak nie, zostať pri Tesseract.

---

## 2. Camelot

### Základné informácie

**Typ:** Nástroj na extrakciu tabuliek z PDF  
**Účel:** Automaticky extrahovať tabuľku s položkami z faktúry bez manuálnych šablón  
**Priorita:** 🔥 VYSOKÁ  
**Náklady:** ZADARMO (open-source)

### Popis

Camelot je Python knižnica špecializovaná na extrakciu tabuliek z PDF dokumentov. Dokáže nájsť tabuľky a prekonvertovať ich do štruktúrovaných dát (pandas DataFrame).

**Problém, ktorý rieši:**

Faktúry majú tabuľku s položkami:
```
Položka          Množstvo    Cena    Suma
────────────────────────────────────────
Tovar A          10          50€     500€
Tovar B          5           100€    500€
────────────────────────────────────────
SPOLU:                               1000€
```

**Súčasný stav (bez Camelot):**
- Musíš vytvoriť šablónu pre každého dodávateľa
- "Tabuľka začína na riadku 15, končí na riadku 30"
- Keď dodávateľ zmení formát → šablóna prestane fungovať
- Veľa manuálnej práce

**S Camelot:**
- Automaticky nájde tabuľku v PDF
- Extrahuje riadky a stĺpce
- Získaš štruktúrované dáta
- Funguje aj keď dodávateľ zmení formát

### Použitie pre NEX Automat / Genesis

**Hlavný use case: Automatická extrakcia položiek z faktúr**

**Workflow:**
```
1. Príde faktúra (PDF)
2. Supplier Classifier identifikuje dodávateľa
3. Camelot nájde tabuľku s položkami
4. Extrahuje:
   - Popis položky
   - Množstvo
   - Jednotková cena
   - Celková cena
   - DPH
5. Uložíš do databázy NEX Genesis
```

**Benefit:**
- Žiadne manuálne šablóny pre každého dodávateľa
- Funguje automaticky
- Adaptívne - prispôsobí sa zmenám vo formáte

**Konkrétny príklad:**

Máš 20 dodávateľov. Bez Camelot musíš vytvoriť 20 šablón a udržiavať ich. S Camelot: jeden univerzálny kód, ktorý funguje pre všetkých.

### Výhody

✅ **Obrovské zjednodušenie** - žiadne šablóny  
✅ **Zadarmo a open-source**  
✅ **Presné** - dobré rozpoznávanie tabuliek  
✅ **Jednoduché použitie** - pár riadkov kódu  
✅ **Výstup ako pandas DataFrame** - ľahko spracovateľné  
✅ **Adaptívne** - funguje aj keď sa formát zmení

### Nevýhody

⚠️ **Nie 100% presné** - veľmi zložité tabuľky môžu robiť problémy  
⚠️ **Pomalšie** - analýza tabuľky trvá 2-5 sekúnd  
⚠️ **Potrebuje kvalitné PDF** - skenované obrázky môžu byť problematické

### Technické požiadavky

**Závislosti:** ghostscript (pre PDF spracovanie)  
**RAM:** ~200-500 MB počas spracovania  
**CPU:** Minimálne  
**Čas spracovania:** 2-5 sekúnd per faktúra  
**Inštalácia:** pip install camelot-py

### Stratégia implementácie

**Fáza 1: Prototyp (týždeň)**
- Otestovať na 50 faktúrach od rôznych dodávateľov
- Vyhodnotiť presnosť extrakcie
- Identifikovať problematické formáty

**Fáza 2: Integrácia (týždeň)**
- Integrovať do AI Service workflow
- Pridať po Supplier Classifier kroku
- Error handling pre zlyhané extrakcie

**Fáza 3: Produkcia (týždeň)**
- Testovať na reálnych faktúrach
- Fallback na manuálne šablóny ak Camelot zlyhá
- Monitoring úspešnosti

### Alternatívy

**Tabula-py**
- Podobná knižnica
- Rýchlejšia, ale menej presná
- **Verdikt:** Camelot je presnejší pre zložité tabuľky

**Manuálne šablóny**
- Presné, ale veľa práce
- Musíš vytvoriť pre každého dodávateľa
- **Verdikt:** Camelot je flexibilnejší a jednoduchší

### Rozhodnutie

**✅ POUŽÍVAME**

Určite áno. Extrakcia položiek je jedna z najnáročnejších častí spracovania faktúr. Camelot to môže výrazne zjednodušiť a zautomatizovať.

---

## 3. Claude API

### Základné informácie

**Typ:** Prístup k veľkému jazykovému modelu (LLM)  
**Účel:** Inteligentná validácia faktúr a riešenie zložitých prípadov  
**Priorita:** 🟡 STREDNÁ  
**Náklady:** ~€12-240/rok (podľa počtu faktúr)

### Popis

Claude API je programatické rozhraní k Claude AI (presne tento model, s ktorým práve hovoríš). Namiesto toho aby si sa pýtal v chate, tvoja aplikácia sa môže opýtať automaticky z kódu.

**Predstav si to takto:**

```
Ty v chate: "Je táto faktúra podozrivá?"
Ja v chate: "Áno, suma je 4x vyššia než obvykle..."

S API (automaticky):
Python kód → pošle faktúru → Claude API → vráti odpoveď
```

### Použitie pre NEX Automat / Genesis

**Use cases:**

### **1. Inteligentná validácia faktúr**

Tvoj ML model má 95% presnosť. Pre tých 5% nejasných prípadov použiješ Claude API:

```
Scenár:
ML model: "Som si istý len na 76% že toto je Magna"
→ Pošli faktúru Claude API
→ Claude: "Áno, je to Magna. Na hlavičke je logo a IČO sedí."
→ Výsledok: Vysoká presnosť aj pre nejasné prípady
```

### **2. Detekcia anomálií s vysvetlením**

```
Scenár:
ML model: "Táto faktúra je podozrivá (anomaly score: 0.82)"
→ Claude API: "Prečo je podozrivá?"
→ Claude: "Suma 8000€ je 4x vyššia než priemerná faktúra 
           od Magna (2000€). Mohlo by ísť o väčší nákup 
           alebo chybu. Odporúčam manuálnu kontrolu."
→ Operátor dostane zrozumiteľné vysvetlenie
```

### **3. Spracovanie neštandardných faktúr**

```
Scenár:
Príde faktúra v úplne novom formáte
ML model: "Neviem spracovať"
→ Claude API: "Extrahuj IČO, sumu, dátum z tohto PDF"
→ Claude: Nájde a extrahuje dáta aj z neznámeho formátu
→ Flexibilné spracovanie bez nového trénovania
```

### **4. Inteligentné odpovede pre používateľov**

```
Scenár:
Operátor: "Prečo systém označil túto faktúru?"
→ Claude API vygeneruje zrozumiteľné vysvetlenie
→ "Faktúra bola označená pretože obsahuje nezvyčajne 
   vysokú DPH sadzbu 25% namiesto štandardných 20%"
```

### Výhody

✅ **Inteligentná vrstva nad ML** - rieši nejasné prípady  
✅ **Flexibilné** - dokáže spracovať čokoľvek, netreba trénovať  
✅ **Vysvetlenia** - nie len výsledok, ale aj PREČO  
✅ **Lacné** - ~€0.005 per faktúra (0.5 centu)  
✅ **Continuous improvement** - Anthropic zlepšuje model  
✅ **Zero-shot learning** - funguje bez trénovania

### Nevýhody

⚠️ **Náklady** - nie zadarmo (ale lacné)  
⚠️ **Latencia** - API volanie trvá 1-3 sekundy  
⚠️ **Závislosť na externe** - potrebuješ internet  
⚠️ **Privacy** - dáta idú na Anthropic servery (ale GDPR compliant)

### Náklady

**Cenník Claude Sonnet 4:**
- $3 per 1 milión vstupných tokenov
- $15 per 1 milión výstupných tokenov

**Priemerná faktúra:**
- Vstup: ~500 tokenov (text faktúry + dotaz)
- Výstup: ~200 tokenov (odpoveď)
- **Cena: ~$0.005 (0.5 centu) per faktúra**

**Mesačné náklady (príklady):**

```
Scenár 1: Malý objem
50 faktúr/mesiac, 5% použije API = 2-3 faktúry
→ €0.01-0.02/mesiac (zanedbateľné)

Scenár 2: Stredný objem
500 faktúr/mesiac, 5% použije API = 25 faktúr
→ €1-2/mesiac

Scenár 3: Veľký objem
5000 faktúr/mesiac, 10% použije API = 500 faktúr
→ €20-25/mesiac

Roční náklady: €12-300/rok (podľa objemu)
```

### Technické požiadavky

**API kľúč:** Potrebuješ účet na Anthropic  
**Integrácia:** Jednoduchá Python knižnica  
**Internet:** Potrebné pripojenie  
**Čas response:** 1-3 sekundy per request

### Stratégia použitia

**Odporúčaný prístup:**

```
PRIMÁRNE: Tvoj ML model (rýchle, lacné, offline)
   ↓
   Ak ML má vysokú istotu (>85%):
   → Použi ML výsledok ✅
   ↓
   Ak ML má nízku istotu (<85%):
   → Claude API validácia ✅
   ↓
VÝSLEDOK: 99%+ presnosť celkovo
```

**Kedy použiť Claude API:**

✅ **ANO** - Pre 5-10% nejasných prípadov (fallback)  
✅ **ANO** - Pre validáciu kritických faktúr (veľké sumy)  
✅ **ANO** - Pre vysvetlenia rozhodnutí AI  
✅ **ANO** - Pre detekciu anomálií s kontextom  
❌ **NIE** - Pre každú faktúru (zbytočné, drahé, pomalé)

### Implementácia

**Fáza 1: Prototyp (týždeň)**
- Registrácia Anthropic účtu
- Získanie API kľúča
- Testovanie na 20 faktúrach
- Vyhodnotenie kvality odpovedí

**Fáza 2: Integrácia (týždeň)**
- Integrácia do AI Service
- Fallback logika (ML confidence < 85% → Claude API)
- Error handling a retry logika
- Caching odpovedí

**Fáza 3: Monitoring (ongoing)**
- Sledovanie nákladov
- Sledovanie použitia (koľko % faktúr)
- Optimalizácia prompt-ov pre lepšie výsledky

### Alternatívy

**OpenAI GPT-4**
- Podobný ako Claude
- Drahší ($10 per 1M tokenov input)
- **Verdikt:** Claude má lepší pomer cena/výkon

**Lokálne LLM (Llama 3)**
- Zadarmo
- Potrebuje GPU (€2000+ investícia)
- Horšia kvalita než Claude
- **Verdikt:** Claude API je jednoduchšie a lepšie

**Žiadna inteligentná vrstva**
- Len tvoj ML model
- Menej presné pre nejasné prípady
- **Verdikt:** Claude API pridáva hodnotu

### Rozhodnutie

**✅ POUŽÍVAME (pre fallback a validáciu)**

Určite áno. Pridáva inteligentnú vrstvu pre zložité prípady, ktoré ML model nevie dobre spracovať. Náklady sú nízke (€12-240/rok) a benefit je vysoký (99%+ presnosť).

---

## 4. DuckDB

### Základné informácie

**Typ:** Analytická databáza  
**Účel:** Super rýchle SQL dotazy a analýza dát (10-100x rýchlejšie než bežné spôsoby)  
**Priorita:** 🟡 STREDNÁ-VYSOKÁ  
**Náklady:** ZADARMO (open-source)

### Popis

DuckDB je ako "SQLite pre analytiku". Je to malá, rýchla databáza optimalizovaná na analýzu dát. Hlavná výhoda: **môžeš robiť SQL dotazy priamo na CSV súboroch, bez toho aby si ich musel importovať do databázy**.

**Kľúčová vlastnosť:**

Môžeš napísať SQL dotaz PRIAMO na CSV súbor - bez importu, bez čakania.

**Prečo je to rýchle:**
- Optimalizované pre analýzu stĺpcov (columnar storage)
- Efektívne využitie CPU a pamäte
- Nepotrebuje server (embedded databáza)
- Paralelné spracovanie dát

### Použitie pre NEX Automat / Genesis

**Use cases:**

### **1. Okamžité (ad-hoc) analýzy faktúr**

"Ad-hoc" = spontánne, jednorazové dotazy keď niečo potrebuješ zistiť TERAZ.

Príklady spontánnych otázok:
- "Koľko sme minuli u Magna tento mesiac?"
- "Ktorý dodávateľ má najvyššiu priemernú sumu?"
- "Ktoré faktúry mali nízku istotu ML modelu?"

**Bez DuckDB (pomalé):**
```
1. Export dát z databázy do CSV (5 minút)
2. Import do Excelu alebo pandas (2 minúty)
3. Analýza (5 minút)
= 12 minút čakania
```

**S DuckDB (rýchle):**
```
SQL dotaz priamo na CSV súbor
= 2 sekundy celkom!
```

### **2. Reporty pre zákazníkov**

Mesačné súhrny, štatistiky, trendy - všetko rýchlo vygenerované SQL dotazmi.

### **3. Analýza výkonu ML modelu**

Rýchlo zistíš kde má ML model problémy:
- Ktorí dodávatelia majú najnižšiu presnosť?
- Kedy má model najčastejšie nízku istotu?
- Trendy presnosti v čase

### **4. Explorácia dát pre nové funkcie**

Keď skúšaš novú ideu, potrebuješ rýchlo analyzovať dáta. DuckDB ti umožní experimentovať bez toho, aby si menil produkčnú databázu.

### Výhody

✅ **Extrémne rýchle** - 10-100x než pandas pre veľké dáta  
✅ **SQL syntax** - ak vieš SQL, už to vieš  
✅ **Dotazy na súbory** - CSV, Parquet, JSON priamo  
✅ **Žiadny server** - embedded, jednoduché ako SQLite  
✅ **Zadarmo a open-source**  
✅ **Malé** - žiadna inštalácia servera  
✅ **Efektívne** - nízke využitie pamäte

### Nevýhody

⚠️ **Nie na transakcie** - len na čítanie a analytiku  
⚠️ **Nie náhrada PostgreSQL** - PostgreSQL je stále hlavná databáza

### Porovnanie výkonu

**Úloha: Analýza 1 milión faktúr**

```
Pandas:
- Načítanie CSV: 30 sekúnd
- Groupby agregácia: 10 sekúnd
- Celkom: 40 sekúnd
- RAM: 4 GB

DuckDB:
- SQL dotaz priamo na CSV: 2 sekundy
- Celkom: 2 sekundy
- RAM: 500 MB

= 20x rýchlejšie, 8x menej pamäte!
```

### Technické požiadavky

**Inštalácia:** pip install duckdb  
**RAM:** Minimálne, efektívne využitie  
**CPU:** Využíva paralelné spracovanie  
**Čas naučenia:** Ak vieš SQL, okamžite

### Kedy použiť vs kedy nepoužiť

**✅ POUŽIŤ DuckDB keď:**
- Potrebuješ rýchlu analýzu dát
- Chceš vytvoriť report
- Exploruješ dáta pre novú funkciu
- Pandas je pomalý
- SQL ti vyhovuje viac než Python

**❌ NEPOUŽÍVAŤ DuckDB keď:**
- Potrebuješ transakcie (používaj PostgreSQL)
- Potrebuješ real-time updates (používaj PostgreSQL)
- Potrebuješ perzistentné ukladanie (používaj PostgreSQL)

**Vzťah k PostgreSQL:**

PostgreSQL a DuckDB sa DOPĹŇAJÚ:
- **PostgreSQL** = hlavná databáza (transakcie, perzistencia)
- **DuckDB** = rýchle analýzy (reporty, explorácia)

### Implementácia

**Fáza 1: Prototyp (deň)**
- Inštalácia
- Prvé SQL dotazy na existujúce CSV exporty
- Vyhodnotenie rýchlosti

**Fáza 2: Integrácia (týždeň)**
- Vytvorenie knižnice často používaných dotazov
- Integrácia do Streamlit dashboardov
- Dokumentácia dotazov

**Fáza 3: Produkčné použitie (ongoing)**
- Používanie pre pravidelné reporty
- Ad-hoc analýzy podľa potreby
- Optimalizácia dotazov

### Alternatívy

**Pandas**
- Python štandard pre dáta
- Pomalšie pre veľké súbory
- **Verdikt:** DuckDB je rýchlejšie, ale pandas stále potrebuješ

**PostgreSQL**
- Tvoja hlavná databáza
- Pre transakcie a perzistentné dáta
- **Verdikt:** Dopĺňajú sa - PostgreSQL = hlavná, DuckDB = analýzy

**Apache Spark**
- Pre VEĽMI veľké dáta (terabajty)
- Zložité nastavenie
- **Verdikt:** Zbytočne zložité pre tvoje potreby

**Excel/LibreOffice Calc**
- Limit ~1 milión riadkov
- Pomalé
- **Verdikt:** DuckDB je profesionálnejšie

### Rozhodnutie

**✅ POUŽÍVAME (pre analýzy a reporty)**

Určite áno. DuckDB výrazne zrýchli ad-hoc analýzy a tvorbu reportov. Je to perfektný nástroj pre exploráciu dát a generovanie štatistík.

---

## Implementačný plán

### Fáza 2: Po Supplier Classifier (Mesiace 3-4)

**Týždeň 1: PaddleOCR testovanie**
- Inštalácia PaddleOCR
- Test na 100 reprezentatívnych faktúrach
- Porovnanie s Tesseract
- Rozhodnutie: použiť alebo nie

**Týždeň 2-3: Camelot integrácia**
- Inštalácia Camelot
- Prototyp extrakcie tabuliek
- Integrácia do AI Service workflow
- Testovanie na reálnych faktúrach

**Týždeň 4: DuckDB setup**
- Inštalácia DuckDB
- Vytvorenie prvých analytických dotazov
- Integrácia do Streamlit dashboardu

### Fáza 3: Pokročilé funkcie (Mesiace 4-6)

**Mesiac 4: Claude API prototyp**
- Registrácia Anthropic účtu
- Testovanie na 20 nejasných faktúrach
- Vyhodnotenie kvality a nákladov

**Mesiac 5: Claude API integrácia**
- Integrácia do AI Service
- Fallback logika
- Monitoring nákladov

**Mesiac 6: Optimalizácia**
- Fine-tuning všetkých komponentov
- Optimalizácia nákladov Claude API
- Performance tuning

---

## Celkové náklady

```
Technológia          Náklady/mesiac    Náklady/rok
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PaddleOCR            FREE              €0
Camelot              FREE              €0
DuckDB               FREE              €0
Claude API           €1-20/mesiac      €12-240/rok
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CELKOM:              €1-20/mesiac      €12-240/rok
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Poznámka: Claude API náklady závisia od objemu faktúr
a % faktúr, ktoré potrebujú validáciu (typicky 5-10%)
```

---

## Očakávané benefity

### Kvantitatívne

**Presnosť:**
- OCR presnosť: 90% → 95% (PaddleOCR)
- Automatická extrakcia položiek: 0% → 85%+ (Camelot)
- Celková presnosť: 95% → 99%+ (Claude API fallback)

**Výkon:**
- Analytické dotazy: 10-100x rýchlejšie (DuckDB)
- Extrakcia položiek: automatická namiesto manuálnej

**Čas:**
- Vytváranie šablón: 0 hodín (Camelot nahrádza)
- Ad-hoc analýzy: minúty namiesto hodín (DuckDB)
- Riešenie nejasných prípadov: automatické (Claude API)

### Kvalitatívne

✅ **Vyšší stupeň automatizácie** - menej manuálnej práce  
✅ **Lepšia kvalita dát** - presnejší OCR, automatická extrakcia  
✅ **Flexibilnejšie riešenie** - adaptuje sa na zmeny formátov  
✅ **Inteligentnejšie rozhodovanie** - vysvetlenia a validácia  
✅ **Rýchlejšie analýzy** - okamžité odpovede na otázky

---

## Technické požiadavky servera

**Aktuálna konfigurácia NEX Genesis Server:**
- CPU: 12 jadier ✅
- RAM: 128 GB ✅
- Disk: SSD ✅

**Dodatočné využitie po nasadení AI/ML Tools:**
- PaddleOCR: ~500 MB RAM (počas OCR)
- Camelot: ~500 MB RAM (počas extrakcie)
- DuckDB: ~500 MB RAM (počas analýzy)
- Claude API: minimálne (len HTTP requesty)
- **CELKOM: ~1.5 GB RAM dodatočne (1% z 128 GB)** ✅

**Verdikt:** Žiadny problém, server má dostatok zdrojov.

---

## Porovnanie s alternatívami

### PaddleOCR vs Tesseract

| Vlastnosť | Tesseract | PaddleOCR |
|-----------|-----------|-----------|
| Presnosť (čisté PDF) | 95% | 96% |
| Presnosť (zlé PDF) | 85% | 92% |
| Rýchlosť (CPU) | Rýchle | Stredné |
| Rýchlosť (GPU) | N/A | Veľmi rýchle |
| Veľkosť modelu | 100 MB | 10 MB |
| Komunita | Veľká | Stredná |
| **Odporúčanie** | ✅ Začať tu | ⭐ Otestovať ako upgrade |

### Camelot vs manuálne šablóny

| Vlastnosť | Manuálne šablóny | Camelot |
|-----------|------------------|---------|
| Presnosť | 99% | 85-95% |
| Čas nastavenia | 30 min/dodávateľ | 5 min celkom |
| Údržba | Vysoká | Minimálna |
| Flexibilita | Nízka | Vysoká |
| Počet šablón | 20+ | 0 |
| **Odporúčanie** | ❌ Veľa práce | ✅ Automatické |

### Claude API vs lokálny LLM

| Vlastnosť | Claude API | Lokálny LLM |
|-----------|-----------|-------------|
| Kvalita | Výborná | Dobrá |
| Náklady (mesačne) | €1-20 | €0 |
| Náklady (setup) | €0 | €2000+ (GPU) |
| Latencia | 1-3s | <1s |
| Údržba | Žiadna | Vysoká |
| **Odporúčanie** | ✅ Jednoduché | ❌ Zbytočne zložité |

### DuckDB vs Pandas

| Vlastnosť | Pandas | DuckDB |
|-----------|--------|---------|
| Rýchlosť (malé dáta) | Rýchle | Rýchle |
| Rýchlosť (veľké dáta) | Pomalé | 10-100x rýchlejšie |
| Syntax | Python | SQL |
| Použitie pamäte | Vysoké | Nízke |
| Dotazy na súbory | Nie | Áno |
| **Odporúčanie** | ✅ Stále používať | ⭐ Pridať pre analýzy |

---

## Integrácia s existujúcim stackom

**Ako sa AI/ML Tools integrujú s Quick Wins:**

```
QUICK WINS (Základ):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Redis → Caching ML predikcií
Sentry → Error tracking
Docker → Kontajnerizácia
Grafana → Monitoring
Streamlit → Dashboardy

AI/ML TOOLS (Nadstavba):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PaddleOCR → Lepší OCR input pre ML
Camelot → Automatická extrakcia dát
Claude API → Inteligentná validácia
DuckDB → Analýzy pre Grafana/Streamlit

= Synergický efekt: celok je viac než súčet častí
```

---

## Ďalšie kroky

Po úspešnej implementácii AI/ML Tools môžeš pokračovať na:

**Infrastructure & Scaling**
- RabbitMQ (rady správ pre vysoký objem)
- TimescaleDB (časové rady v PostgreSQL)
- MinIO (úložisko PDF súborov)

**Advanced Features**
- Hugging Face NER modely (pokročilá extrakcia)
- Layout Analysis (rozpoznávanie štruktúry dokumentov)
- Anomaly Detection modely (detekcia podvodov)

---

## Záver

Týchto 4 AI/ML technológií poskytuje:
- ✅ Vyššiu presnosť spracovania faktúr (95% → 99%+)
- ✅ Automatizáciu extrakcie položiek (namiesto šablón)
- ✅ Inteligentnú validáciu zložitých prípadov
- ✅ Rýchle analytické možnosti
- ✅ Minimálne náklady (€12-240/rok)
- ✅ Jednoduchú integráciu s existujúcim stackom

**Všetky technológie sú schválené a pripravené na implementáciu v Fázach 2-4.**

---

**Posledná aktualizácia:** 2024-12-04  
**Status:** FINÁLNA VERZIA  
**Predchádzajúci dokument:** Quick Wins Technology Guide  
**Ďalší krok:** Implementácia podľa plánu

---

**KONIEC DOKUMENTU**