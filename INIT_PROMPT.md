# INIT PROMPT - Supplier Invoice Staging Web UI

**Projekt:** nex-automat / supplier-invoice-staging-web
**Typ:** React Web UI pre existujúci FastAPI backend
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT FOCUS

Opraviť TypeScript typy a mock data podľa správnej DB schémy (xml_* prefixy)

---

## ✅ Čo je hotové

| Komponenta | Status |
|------------|--------|
| Vite + React + TypeScript | ✅ |
| Tailwind + Shadcn/ui | ✅ |
| Layout (Header, Sidebar) | ✅ |
| DataGrid s column filters | ✅ |
| Keyboard navigation | ✅ |
| Column configuration (⚙️) | ✅ |
| Zoznam faktúr | ✅ |
| Detail faktúry + položky | ✅ |

---

## 📋 Next Steps

1. **Aktualizovať TypeScript typy** - xml_* prefixy podľa DB schémy
2. **Opraviť mock data** - zodpovedať reálnej štruktúre
3. Test s reálnym backendom
4. Schvaľovací workflow
5. Docker deployment

---

## 🔍 RAG Query

```
https://rag-api.icc.sk/search?query=supplier_invoice_heads+supplier_invoice_items+schema&limit=5
```

---

## 📁 Umiestnenie

```
C:\Development\nex-automat\apps\supplier-invoice-staging-web\
```

## 🚀 Spustenie

```bash
cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npm run dev
# http://localhost:5173
```
