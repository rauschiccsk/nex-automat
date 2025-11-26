# NEX Automat - Vízia projektu

**Projekt:** NEX Automat  
**Verzia dokumentu:** 1.0  
**Dátum:** 2025-11-26  

---

## 1. VÍZIA

**NEX Automat = Kompletná automatizácia podnikových procesov**

Cieľom projektu je nahradiť manuálne, chybové a časovo náročné procesy automatizovanými riešeniami pre zákazníkov používajúcich NEX Genesis ERP.

---

## 2. PROBLÉM

### 2.1 Súčasný stav (manuálne procesy)

- **Ľudský faktor** = hlavný zdroj chýb
- **Prepisovanie údajov** z PDF do systému
- **Identifikácia tovaru** na základe EAN kódov
- **Kontrola súm** a marží
- **Časová náročnosť** - minúty až hodiny na jeden doklad

### 2.2 Typické chyby

- Nesprávne množstvo alebo cena
- Zámena produktov (podobné EAN)
- Chyby pri výpočte marže
- Zabudnuté položky
- Duplicitné zaevidovanie

---

## 3. RIEŠENIE

### 3.1 Automatizácia

Nahradenie manuálnych krokov automatizovanými:

| Manuálne | Automatizované |
|----------|----------------|
| Otvorenie emailu | IMAP trigger (n8n) |
| Čítanie PDF | AI/Regex extrakcia |
| Prepisovanie údajov | XML → Staging DB |
| Identifikácia tovaru | NEX Lookup (EAN → PLU) |
| Kontrola súm | Automatická validácia |
| Zaevidovanie dokladu | Btrieve zápis |

### 3.2 Overený, dôveryhodný proces

- **Konzistentnosť** - rovnaký výsledok pri rovnakom vstupe
- **Transparentnosť** - každý krok je logovateľný
- **Kontrola** - operátor validuje pred finálnym zápisom

---

## 4. STRATÉGIA

### 4.1 Postupná cesta

```
Čiastočná automatizácia → Úplná automatizácia
```

**Fáza 1 (v2.0):** Human-in-the-loop
- Automatické spracovanie až po GUI
- Operátor kontroluje a schvaľuje
- Systém zapisuje do NEX Genesis

**Fáza 2 (budúcnosť):** Plná automatizácia
- AI validácia nahrádza operátora
- Automatické priradenie tovarových skupín
- Priamy email od dodávateľa

### 4.2 Prečo postupne?

1. **Dôvera zákazníka** - musí vidieť, že systém funguje správne
2. **Učenie systému** - zbieranie dát pre AI zlepšovanie
3. **Minimalizácia rizika** - chyby zachytí operátor

---

## 5. HODNOTA PRE ZÁKAZNÍKA

### 5.1 Kvantifikovateľné prínosy

| Metrika | Pred | Po |
|---------|------|-----|
| Čas na faktúru | 10-30 min | 1-2 min |
| Chybovosť | 5-10% | <1% |
| Denne spracovaných | 10-20 | 50-100+ |

### 5.2 Úspora FTE

- **Mágerstav:** 0.5-1 FTE
- **Väčší zákazníci:** 1-3 FTE

### 5.3 Ďalšie prínosy

- Eliminácia ľudských chýb
- Rýchlejšie naskladnenie tovaru
- Lepšia kontrola marží
- Audit trail (história zmien)

---

## 6. CIEĽOVÉ SKUPINY

### 6.1 Pilotní zákazníci

| Zákazník | Typ | Status |
|----------|-----|--------|
| Mágerstav s.r.o. | Stavebný materiál | 🟡 GO-LIVE |
| ANDROS | (budúci) | ⚪ Plánovaný |
| ICC | Interný | ⚪ Plánovaný |

### 6.2 Ideálny zákazník

- Používa NEX Genesis ERP
- Vysoký objem dodávateľských faktúr
- Štandardizovaní dodávatelia (konzistentný formát PDF)
- Motivácia zefektívniť procesy

---

## 7. SCOPE v2.0

### 7.1 V scope

- ✅ Spracovanie dodávateľských faktúr
- ✅ Vytvorenie produktových kariet
- ✅ Zaevidovanie dodávateľského DL
- ✅ Požiadavky na zmenu cien

### 7.2 Mimo scope

- ❌ Automatické naskladnenie (robí NEX Genesis)
- ❌ AI automatické priradenie skupín
- ❌ Priamy email bez operátora

---

## 8. KRITÉRIÁ ÚSPECHU

### 8.1 Technické

- [ ] 100% úspešnosť extrakcie pre L&Š faktúry
- [ ] <5 sekúnd doba spracovania
- [ ] 0% dátových strát

### 8.2 Biznis

- [ ] Zákazník používa systém denne
- [ ] Zníženie času na faktúru o 80%+
- [ ] Pozitívna spätná väzba

### 8.3 GO-LIVE kritériá

- [ ] End-to-end workflow funguje
- [ ] Operátor vie používať GUI
- [ ] Dáta sa správne zobrazia v NEX Genesis

---

## 9. DLHODOBÁ VÍZIA

### 9.1 NEX Automat ako platforma

```
NEX Automat
├── Supplier Invoice Processing (v2.0) ← TU SME
├── Customer Order Processing (budúci)
├── Inventory Management (budúci)
├── Financial Reporting (budúci)
└── ... ďalšie moduly
```

### 9.2 Migrácia NEX Genesis → NEX Automat

- Postupný prechod na moderné technológie
- Python, PostgreSQL, n8n ako základ
- Zachovanie kompatibility s Btrieve (prechodné obdobie)

---

**Dokument vytvorený:** 2025-11-26  
**Autor:** Claude AI + Zoltán Rausch