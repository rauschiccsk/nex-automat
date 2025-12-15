# NEX Automat v2.0 - Go-Live Checklist

**Zákazník:** Mágerstav s.r.o.  
**Systém:** Supplier Invoice Loader  
**Target Go-Live:** 2025-11-27  
**Zodpovedný:** ICC Komárno  

---

## Prehľad pripravenosti

| Oblasť         | Status | Poznámka              |
| -------------- | ------ | --------------------- |
| Infraštruktúra | ✅      | Server ready          |
| Aplikácia      | ✅      | Deployed & running    |
| Databáza       | ✅      | PostgreSQL configured |
| Testovanie     | ✅      | 100% pass rate        |
| Dokumentácia   | 🔄     | In progress           |
| Školenie       | ⏳      | Pending               |
| Monitoring     | ⏳      | Pending               |

---

## 1. Infraštruktúra (T-3 dni)

### 1.1 Server

- [x] Windows Server dostupný
- [x] Python 3.13.7 32-bit nainštalovaný
- [x] PostgreSQL 16 nainštalovaný a bežiaci
- [x] NSSM nainštalovaný (C:\Tools\nssm)
- [x] Deployment adresár vytvorený (C:\Deployment\nex-automat)
- [x] Dostatočný disk space (>100GB free)

### 1.2 Sieť

- [x] Server dostupný v sieti
- [ ] Firewall pravidlá nastavené (port 8000 ak potrebné)
- [ ] Prístup k NEX Genesis serveru overený

### 1.3 Zálohovanie

- [x] Backup stratégia definovaná
- [x] Automatické zálohy nakonfigurované
- [ ] Test obnovy zo zálohy vykonaný
- [ ] Záloha pred Go-Live vytvorená

---

## 2. Aplikácia (T-2 dni)

### 2.1 Deployment

- [x] Kód nasadený do C:\Deployment\nex-automat
- [x] Virtual environment vytvorený (venv32)
- [x] Všetky dependencies nainštalované
- [x] Config.yaml správne nakonfigurovaný

### 2.2 Windows Service

- [x] NEX-Automat-Loader služba vytvorená
- [x] Služba beží (SERVICE_RUNNING)
- [x] Auto-start pri štarte systému
- [x] Recovery nastavenia (restart on failure)

### 2.3 Environment Variables

- [x] POSTGRES_PASSWORD nastavené
- [x] LS_API_KEY nastavené (ak potrebné)
- [ ] Overené po reštarte servera

---

## 3. Databáza (T-2 dni)

### 3.1 PostgreSQL

- [x] Databáza invoice_staging vytvorená
- [x] Schéma migrovaná
- [x] Používateľ postgres s heslom
- [x] Connection pooling nakonfigurovaný

### 3.2 Dáta

- [ ] Produkčné dáta importované (ak existujú)
- [ ] Testovacie dáta vymazané
- [x] Indexy vytvorené

### 3.3 Performance

- [x] Query performance overený (<1ms)
- [x] Connection time overený (<200ms)

---

## 4. Testovanie (T-1 deň)

### 4.1 Automatické testy

- [x] Error handling tests: 12/12 PASS
- [x] Performance tests: 6/6 PASS
- [x] Preflight checks: 6/6 PASS

### 4.2 Manuálne testy

- [ ] End-to-end spracovanie faktúry
- [ ] Overenie výstupu v NEX Genesis
- [ ] Test s reálnou faktúrou zákazníka

### 4.3 Záťažové testy

- [x] Concurrent processing tested
- [x] Memory leak check passed
- [x] Throughput validated (0.5+ files/sec)

---

## 5. Dokumentácia (T-1 deň)

### 5.1 Technická dokumentácia

- [x] SESSION_NOTES.md aktuálne
- [x] PROJECT_MANIFEST.json vygenerovaný
- [x] KNOWN_ISSUES.md aktualizovaný

### 5.2 Prevádzková dokumentácia

- [x] RECOVERY_PROCEDURES.md vytvorený
- [ ] OPERATIONS_GUIDE.md vytvorený
- [ ] TROUBLESHOOTING.md dokončený

### 5.3 Zákaznícka dokumentácia

- [ ] Používateľská príručka
- [ ] Quick Reference Card
- [ ] FAQ dokument

---

## 6. Školenie (T-1 deň)

### 6.1 Administrátorské školenie

- [ ] Správa služby (start/stop/restart)
- [ ] Čítanie logov
- [ ] Základné troubleshooting
- [ ] Backup a obnova

### 6.2 Používateľské školenie

- [ ] Ako nahrať faktúry
- [ ] Kontrola stavu spracovania
- [ ] Čo robiť pri chybe

### 6.3 Dokumenty školenia

- [ ] Školiace materiály pripravené
- [ ] Kontaktné údaje odovzdané
- [ ] SLA podmienky vysvetlené

---

## 7. Monitoring (T-1 deň)

### 7.1 Health Checks

- [ ] Service status monitoring
- [ ] Database connectivity check
- [ ] Disk space monitoring

### 7.2 Alerting

- [ ] Email notifikácie pri výpadku
- [ ] Eskalácia definovaná
- [ ] On-call kontakty

### 7.3 Logging

- [x] Application logs nakonfigurované
- [x] Log rotation nastavený
- [ ] Centrálny log collection (ak potrebné)

---

## 8. Go-Live Day (D-Day)

### 8.1 Pred spustením (ráno)

- [ ] Final backup vytvorený
- [ ] Všetky služby overené
- [ ] Preflight check: 6/6 PASS
- [ ] Zákazník informovaný

### 8.2 Spustenie

- [ ] Service start overený
- [ ] Prvá faktúra spracovaná
- [ ] Výstup v NEX Genesis overený
- [ ] Zákazník potvrdil funkčnosť

### 8.3 Po spustení (1h)

- [ ] Monitoring aktívny
- [ ] Žiadne chyby v logoch
- [ ] Performance normálny
- [ ] Zákazník spokojný

### 8.4 Po spustení (24h)

- [ ] Stabilita overená
- [ ] Všetky faktúry spracované
- [ ] Zákazník reportoval OK
- [ ] Dokumentácia odovzdaná

---

## 9. Post Go-Live (D+1 až D+7)

### 9.1 Monitoring

- [ ] Denná kontrola logov
- [ ] Performance trending
- [ ] Incident tracking

### 9.2 Podpora

- [ ] Helpdesk pripravený
- [ ] Eskalácia funguje
- [ ] SLA plnené

### 9.3 Optimalizácia

- [ ] Feedback od zákazníka
- [ ] Performance tuning ak potrebné
- [ ] Dokumentácia aktualizovaná

---

## Kritické kontakty

| Rola         | Meno        | Telefón  | Email            |
| ------------ | ----------- | -------- | ---------------- |
| Project Lead | [ICC]       | +421 XXX | xxx@icc.sk       |
| Technik      | [ICC]       | +421 XXX | xxx@icc.sk       |
| Zákazník IT  | [Mágerstav] | +421 XXX | xxx@magerstav.sk |
| Zákazník PM  | [Mágerstav] | +421 XXX | xxx@magerstav.sk |

---

## Rollback plán

**Ak Go-Live zlyhá:**

1. Zastaviť službu: `python scripts\manage_service.py stop`
2. Obnoviť DB zo zálohy
3. Informovať zákazníka
4. Analyzovať príčinu
5. Naplánovať nový termín

**Kritéria pre rollback:**

- Service nenaštartuje do 15 min
- Kritické chyby v spracovaní
- Zákazník požaduje zastavenie

---

## Sign-off

| Položka           | Podpis   | Dátum    |
| ----------------- | -------- | -------- |
| Infraštruktúra OK | ________ | ________ |
| Aplikácia OK      | ________ | ________ |
| Testovanie OK     | ________ | ________ |
| Dokumentácia OK   | ________ | ________ |
| Školenie OK       | ________ | ________ |
| Go-Live Approved  | ________ | ________ |

---

**Vytvorené:** 2025-11-24  
**Verzia:** 1.0