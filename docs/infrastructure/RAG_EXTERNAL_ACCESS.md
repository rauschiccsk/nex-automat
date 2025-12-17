# RAG External Access - Kompletná Dokumentácia

**Dokument:** RAG_EXTERNAL_ACCESS.md  
**Vytvorené:** 2025-12-17  
**Autor:** Zoltán Rausch & Claude AI  
**Status:** ✅ PRODUCTION  
**Umiestnenie:** `docs/infrastructure/RAG_EXTERNAL_ACCESS.md`

---

## 1. PREHĽAD

### 1.1 Čo je RAG External Access

RAG External Access umožňuje Claude AI priamy prístup k projektovej dokumentácii cez RAG (Retrieval-Augmented Generation) server. Toto je **základná infraštruktúra** pre efektívnu spoluprácu medzi vývojárom a AI asistentom.

### 1.2 Prečo je to dôležité

- **Bez manuálneho kopírovania** - Claude pristupuje k docs priamo
- **Vždy aktuálne informácie** - 107 dokumentov, 500 chunks
- **Kontextové odpovede** - AI vie hľadať v celej dokumentácii
- **Základ pre budúci produkt** - RAG ako služba pre enterprise

### 1.3 Architektúra

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Claude AI     │────▶│  Cloudflare Worker   │────▶│  RAG Server     │
│  (Anthropic)    │     │   (rag-proxy)        │     │  (localhost)    │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
         │                        │                          │
         │                        │                          │
    External IP            rag-api.icc.sk              127.0.0.1:8765
  34.162.230.222          Cloudflare Edge              FastAPI + PostgreSQL
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Cloudflare Tunnel │
                         │   (n8n-tunnel)    │
                         └──────────────────┘
```

---

## 2. KOMPONENTY

### 2.1 RAG Server (lokálny)

| Parameter | Hodnota |
|-----------|---------|
| Host | 127.0.0.1 |
| Port | 8765 |
| Framework | FastAPI |
| Database | PostgreSQL (nex_automat_rag) |
| Dokumenty | 107 |
| Chunks | 500 |
| Root Path | /rag |

**Umiestnenie:** `C:\Development\nex-automat\tools\rag\`

**Hlavné súbory:**
- `server_app.py` - FastAPI aplikácia
- `server.py` - Server manager
- `database.py` - PostgreSQL operácie
- `hybrid_search.py` - Hybridné vyhľadávanie

### 2.2 Cloudflare Tunnel

| Parameter | Hodnota |
|-----------|---------|
| Názov | n8n-tunnel |
| ID | f12d0607-ee9b-4465-a30f-2b2b1ff4d02f |
| Config | C:\Users\ZelenePC\.cloudflared\config.yml |

**Config súbor:**
```yaml
tunnel: f12d0607-ee9b-4465-a30f-2b2b1ff4d02f
credentials-file: C:\Users\ZelenePC\.cloudflared\f12d0607-ee9b-4465-a30f-2b2b1ff4d02f.json

ingress:
  - hostname: n8n.icc.sk
    service: http://localhost:5678
  - hostname: n8n.icc.sk
    path: /rag/*
    service: http://localhost:8765
  - service: http_status:404
```

### 2.3 Cloudflare Worker (rag-proxy)

| Parameter | Hodnota |
|-----------|---------|
| Názov | rag-proxy |
| URL | rag-proxy.iccforai.workers.dev |
| Route | rag-api.icc.sk/* |

**Worker kód:** Viď sekciu 5.1

### 2.4 DNS Záznam

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | rag-api | 192.0.2.1 | ✅ Proxied |

### 2.5 Cloudflare Security Settings

| Nastavenie | Hodnota |
|------------|---------|
| Block AI training bots | Do not block (allow crawlers) |

---

## 3. ENDPOINTY

### 3.1 Health Check
```
GET https://rag-api.icc.sk/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "documents": 107,
  "timestamp": "2025-12-17T09:24:04.438452"
}
```

### 3.2 Search
```
GET https://rag-api.icc.sk/search?query=<text>&limit=<n>
```

**Parametre:**
- `query` - Hľadaný text
- `limit` - Max počet výsledkov (default: 5)

**Response:**
```json
{
  "query": "btrieve",
  "results": [...],
  "count": 5,
  "timestamp": "..."
}
```

### 3.3 Stats
```
GET https://rag-api.icc.sk/stats
```

---

## 4. SPUSTENIE PO REŠTARTE

### 4.1 Poradie spustenia

```
1. PostgreSQL (automaticky ako Windows služba)
2. RAG Server (manuálne)
3. Cloudflare Tunnel (manuálne)
```

### 4.2 Krok za krokom

**Terminal 1 - RAG Server:**
```powershell
cd C:\Development\nex-automat
.\venv\Scripts\Activate.ps1
python -m tools.rag.server start
```

**Terminal 2 - Cloudflare Tunnel:**
```powershell
cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel
```

### 4.3 Overenie funkčnosti

**V prehliadači:**
```
https://rag-api.icc.sk/health
```

**Očakávaný výsledok:**
```json
{"status":"healthy","database":"connected","documents":107,...}
```

### 4.4 Batch skript pre jednoduché spustenie (voliteľné)

Uložiť ako `start-rag-services.bat`:
```batch
@echo off
echo Starting RAG Services...

start "RAG Server" cmd /k "cd C:\Development\nex-automat && .\venv\Scripts\Activate.ps1 && python -m tools.rag.server start"

timeout /t 5

start "Cloudflare Tunnel" cmd /k "cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel"

echo Services started. Check terminals for status.
pause
```

---

## 5. TECHNICKÉ DETAILY

### 5.1 Cloudflare Worker Kód

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers for external access
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Serve robots.txt to allow all crawlers
    if (url.pathname === '/robots.txt') {
      return new Response('User-agent: *\nAllow: /', {
        headers: {
          'Content-Type': 'text/plain',
          ...corsHeaders,
        },
      });
    }
    
    // Build target URL - proxy to Cloudflare Tunnel
    const targetUrl = `https://n8n.icc.sk/rag${url.pathname}${url.search}`;
    
    console.info({ message: 'RAG Proxy request', target: targetUrl });
    
    try {
      // Forward request to RAG server via tunnel
      const response = await fetch(targetUrl, {
        method: request.method,
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Cloudflare-Worker-RAG-Proxy/1.0',
        },
        body: request.method !== 'GET' ? request.body : undefined,
      });
      
      // Clone response and add CORS headers
      const responseBody = await response.text();
      
      return new Response(responseBody, {
        status: response.status,
        headers: {
          ...corsHeaders,
          'Content-Type': response.headers.get('Content-Type') || 'application/json',
        },
      });
    } catch (error) {
      console.error({ message: 'RAG Proxy error', error: error.message });
      return new Response(JSON.stringify({ 
        error: 'Proxy error', 
        details: error.message 
      }), {
        status: 502,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      });
    }
  },
};
```

### 5.2 Prečo Worker namiesto priameho prístupu

**Problém:** Cloudflare Managed Rules blokovali externé IP (vrátane Anthropic/Claude)

**Pokusy ktoré NEFUNGOVALI:**
1. ❌ Security Rules - Skip managed rules pre Anthropic IPs
2. ❌ WAF výnimky
3. ❌ Priamy prístup cez n8n.icc.sk/rag/*

**Riešenie ktoré FUNGUJE:**
- ✅ Cloudflare Worker ako proxy
- ✅ Worker beží na Cloudflare edge (trusted)
- ✅ Vlastná subdoména rag-api.icc.sk
- ✅ robots.txt endpoint pre Claude fetcher
- ✅ "Do not block" AI crawlers setting

---

## 6. TROUBLESHOOTING

### 6.1 RAG Server nereaguje

```powershell
# Skontroluj či beží
netstat -an | findstr 8765

# Reštartuj
cd C:\Development\nex-automat
.\venv\Scripts\Activate.ps1
python -m tools.rag.server start
```

### 6.2 Tunnel nefunguje

```powershell
# Skontroluj status
cloudflared tunnel info n8n-tunnel

# Reštartuj
cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel
```

### 6.3 403 Forbidden z Claude

1. Skontroluj "Block AI training bots" nastavenie v Cloudflare
2. Musí byť: "Do not block (allow crawlers)"
3. Cloudflare Dashboard → icc.sk → Overview → Control AI crawlers

### 6.4 502 Bad Gateway

- RAG server nebeží
- Tunnel nebeží
- Skontroluj obe služby

---

## 7. HISTÓRIA RIEŠENIA

### 7.1 Chronológia (2025-12-17)

| Čas | Aktivita | Výsledok |
|-----|----------|----------|
| 09:00 | Identifikácia problému | 403 z Cloudflare |
| 09:05 | Vytvorenie Worker rag-proxy | Deployed |
| 09:10 | Test cez workers.dev | robots.txt problém |
| 09:15 | Pridanie robots.txt do Worker | Stále nefunguje |
| 09:20 | DNS + Route pre rag-api.icc.sk | 403 pretrváva |
| 09:24 | Zmena "Block AI bots" → Allow | ✅ FUNGUJE! |

### 7.2 Kľúčové ponaučenia

1. **Cloudflare Managed Rules** sú agresívne voči AI crawlers
2. **Workers** bežia na trusted edge - obchádzajú niektoré rules
3. **"Block AI training bots"** blokuje aj legitímne AI prístupy
4. **robots.txt** je potrebný pre Claude's web_fetch

---

## 8. BUDÚCE VYLEPŠENIA

### 8.1 Plánované

- [ ] Windows Service pre RAG server (auto-start)
- [ ] Windows Service pre Cloudflare Tunnel
- [ ] Health monitoring a alerting
- [ ] API key authentication (pre bezpečnosť)

### 8.2 Možné rozšírenia

- Rate limiting na Worker úrovni
- Caching častých queries
- Logging a analytics
- Multi-tenant RAG pre enterprise

---

## 9. SÚVISIACE DOKUMENTY

- `docs/strategic/RAG_IMPLEMENTATION.md` - RAG plán
- `tools/rag/README.md` - RAG modul dokumentácia
- `config/rag_config.yaml` - RAG konfigurácia

---

**Koniec dokumentu RAG_EXTERNAL_ACCESS.md**