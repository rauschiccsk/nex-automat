# SESSION ARCHIVE - RAG FastAPI Server + Cloudflare Tunnel Integration

**Session Date:** 2025-12-17  
**Project:** nex-automat RAG Integration  
**Status:** ⚠️ IN PROGRESS - Cloudflare blocking external access  
**Duration:** 4h 30min

---

## SESSION OVERVIEW

Úspešný setup RAG FastAPI servera s Cloudflare Tunnel, ale blokovaný external prístup kvôli Cloudflare Managed Rules. Session pokračuje v ďalšom chate s akčným plánom na definitívne riešenie.

---

## IMPLEMENTED FEATURES

### 1. RAG FastAPI Server Testing ✅

**Cieľ:** Overiť že Claude môže pristupovať k RAG serveru cez web_fetch tool

**Pokusy:**
1. **Ngrok** - verification page blocking ❌
2. **LocalTunnel** - fungoval perfektne ✅ (ale nová URL každý reštart)
3. **Cloudflare Tunnel** - setup úspešný, ale managed rules blocking ⚠️

**LocalTunnel test (úspešný):**
```powershell
lt --port 8765
# URL: https://fruity-toes-wash.loca.lt
```

**Výsledky testov:**
- `/health` - ✅ 200 OK (lokálne + prehliadač)
- `/stats` - ✅ 200 OK (107 docs, 500 chunks)
- `/search?query=product+enrichment` - ✅ funguje

---

### 2. Cloudflare Tunnel Configuration ✅

**Tunnel:** `n8n-tunnel` (f12d0607-ee9b-4465-a30f-2b2b1ff4d02f)

**Config file:** `C:\Users\ZelenePC\.cloudflared\config.yml`

```yaml
tunnel: f12d0607-ee9b-4465-a30f-2b2b1ff4d02f
credentials-file: C:\Users\ZelenePC\.cloudflared\f12d0607-ee9b-4465-a30f-2b2b1ff4d02f.json
ingress:
  # RAG API Server - path /rag/*
  - hostname: n8n.icc.sk
    path: ^/rag(/.*)?$
    service: http://localhost:8765
  # n8n - všetko ostatné
  - hostname: n8n.icc.sk
    service: http://localhost:5678
  # 404 fallback
  - service: http_status:404
```

**URL:** `https://n8n.icc.sk/rag/*`

---

### 3. FastAPI Server Patch ✅

**Problém:** Server nepoznal `/rag` prefix path

**Riešenie:** Pridanie `root_path="/rag"` do FastAPI app

**Script:** `scripts/01_add_root_path.py`

```python
# Patch v tools/rag/server_app.py
app = FastAPI(
    root_path="/rag",  # For Cloudflare Tunnel path routing
    # ... rest of config
)
```

**Výsledok:**
- ✅ `https://n8n.icc.sk/rag/health` - funguje v prehliadači
- ❌ `https://n8n.icc.sk/rag/health` - 403 pre Claude (Anthropic IP)

---

### 4. Cloudflare Security Rules ✅ (ale nefunkčné)

**Created 2 Skip rules:**

**Rule 1:** Allow Anthropic IPs for RAG
- Order: 1 (First)
- Condition: `IP Source Address equals 34.162.230.222`
- Action: Skip
- WAF components: All managed rules ✅

**Rule 2:** Allow RAG API
- Order: 2
- Condition: `URI Path starts with /rag`
- Action: Skip
- WAF components: All managed rules ✅

**Problém:** Pravidlá sú deployed ale stále dostávam 403

---

## IDENTIFIED PROBLEMS

### 1. Cloudflare Managed Rules Blocking ❌

**Evidence z Firewall Events:**
```
Time: Dec 17, 2025 8:51:19 AM
Source IP: 34.162.230.222 (Anthropic)
Path: /rag/health
Host: n8n.icc.sk
Mitigation: Block by Managed rules
```

**Dôvod:**
- Cloudflare Managed Rules majú vyššiu prioritu ako Custom Skip rules
- Free plán má obmedzenia pre bypassovanie managed rules

---

### 2. Skip Rules Nefungujú Pre External IPs ⚠️

**Observácie:**
- Skip rules sú Active a Order: First
- `All managed rules` zaškrtnuté
- V prehliadači (s prihlásením) funguje ✅
- Pre external IPs (Anthropic) stále 403 ❌

**Hypotéza:**
- Managed rules sa vyhodnocujú PRED custom rules
- Alebo Skip action v Free pláne nefunguje pre managed rules

---

## STRATEGIC DECISION

**Zoltán rozhodnutie:**
> "Som v 21. storočí, plánujeme vyvíjať futuristické riešenia. Nedokážeme vyriešiť elementárnu úlohu? Zastavím všetky projekty pokiaľ to nevyriešime."

**Vízia projektu:**
1. **Internal use:** Claude má priamy prístup k projektovej dokumentácii
2. **Product vision:** RAG system ako produkt pre veľké firmy
   - Centrálny repozitár vedomostí
   - Automatická indexácia dokumentov
   - AI-powered search

**Odmietnuté riešenie:**
- ❌ Manuálne kopírovanie dát medzi Claude a RAG
- ❌ Ľudský kuriersky faktor

---

## NEXT STEPS - ACTION PLAN

### Priority: Vyriešiť Cloudflare blocking DEFINITÍVNE

**Možnosti na vyskúšanie:**

### Option 1: Cloudflare Workers ⭐ (NAJVIAC SĽUBNÉ)
**Dôvod:** Workers bežia na edge, môžu úplne bypassovať managed rules

**Implementation:**
```javascript
// worker.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Proxy RAG requests
  if (url.pathname.startsWith('/rag')) {
    const ragUrl = 'http://localhost:8765' + url.pathname.replace('/rag', '')
    return fetch(ragUrl, request)
  }
  
  return fetch(request)
}
```

**Setup:**
1. Workers → Create Service
2. Deploy worker code
3. Workers Routes → `n8n.icc.sk/rag/*`

---

### Option 2: Subdoména `rag.icc.sk`
**Dôvod:** Nová subdoména BEZ managed rules

**Setup:**
1. DNS: `rag.icc.sk` CNAME → tunnel
2. Cloudflare Tunnel config update
3. NO security rules na tejto subdoméne

**Pros:**
- ✅ Clean separation
- ✅ Žiadne konflikty s n8n.icc.sk

**Cons:**
- ❌ Vyžaduje DNS zmenu
- ❌ Verejne dostupná subdoména

---

### Option 3: API Token Authentication
**Dôvod:** Autentifikovaný prístup môže bypassovať managed rules

**Implementation:**
1. RAG server: Pridať API key validation
2. Claude: Posielať API key v header
3. Cloudflare: Povoliť requesty s validným API key

---

### Option 4: User-Agent Whitelist
**Dôvod:** Cloudflare môže povoliť špecifický User-Agent

**Test:**
1. Identifikovať Claude's User-Agent
2. Vytvoriť rule: Allow if User-Agent matches

---

### Option 5: Page Rules (Legacy)
**Dôvod:** Staršie Page Rules môžu mať vyššiu prioritu

**Setup:**
1. Page Rules → Disable Security
2. URL pattern: `n8n.icc.sk/rag/*`

---

## FILES MODIFIED

### 1. RAG Server
- `tools/rag/server_app.py` - Added `root_path="/rag"`

### 2. Cloudflare Config
- `C:\Users\ZelenePC\.cloudflared\config.yml` - Updated ingress rules

### 3. Scripts
- `scripts/01_add_root_path.py` - Patch script for root_path

---

## INFRASTRUCTURE STATUS

### RAG Server ✅
- Running on: http://127.0.0.1:8765
- Status: Healthy
- Database: Connected
- Documents: 107
- Access: Lokálne ✅, External ❌

### Cloudflare Tunnel ✅
- Name: n8n-tunnel
- Status: Running
- URL: https://n8n.icc.sk/rag/*
- Access: Prehliadač ✅, Claude API ❌

### Security Rules ⚠️
- Custom rules: 2 active (Skip)
- Managed rules: Active (blocking)
- Stav: Deployed, ale nefunkčné pre external IPs

---

## LESSONS LEARNED

1. **Cloudflare Free tier má limity** - Skip rules nefungujú na managed rules
2. **Workers sú pravdepodobne jediné riešenie** - bežia pred managed rules
3. **Testovanie multiple prístupov je dôležité** - LocalTunnel fungoval okamžite
4. **Security != barrier** - potrebujeme vyvážené riešenie

---

## COMMITMENT FOR NEXT SESSION

**Zoltán's requirement:**
> "Zastavím všetky projekty pokiaľ to nevyriešime. Spolu sme riešili oveľa zložitejšie veci."

**Action plan:**
1. ⭐ Najprv vyskúšať **Cloudflare Workers** (10 minút setup)
2. Ak nefunguje → **Subdoména rag.icc.sk** (20 minút)
3. Ak nefunguje → **API Token auth** (30 minút)
4. **Nevzdávať sa** až kým nebude funkčné

**Goal:** Claude má priamy prístup k RAG systému bez manuálneho kurierstva.

---

## TECHNICAL NOTES

### Anthropic IP Addresses (observed)
```
34.162.230.222 (primary)
34.34.24.135 (secondary)
2a01:c846:cc3:7200:... (IPv6)
```

### Cloudflare Firewall Events
- Path: `/rag/health`
- Method: GET
- HTTP/1.1
- ASN: 396982 - GOOGLE-CLOUD-PLATFORM
- User-Agent: Mozilla/5.0 AppleWebKit/537.36...

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-17  
**Next Session:** Cloudflare Workers implementation  
**Status:** ⚠️ BLOCKED - Awaiting definitive solution