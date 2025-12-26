# INIT PROMPT - Supplier Invoice Staging Web UI

**Projekt:** nex-automat / supplier-invoice-staging-web
**Typ:** React Web UI pre existujúci FastAPI backend
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT FOCUS

Opraviť drag & drop v dialógu nastavení stĺpcov - ťahanie má fungovať IBA z GripVertical ikony (⋮⋮)

---

## ✅ Čo je hotové

| Komponenta | Status |
|------------|--------|
| Vite + React + TypeScript | ✅ |
| TypeScript typy (xml_* prefixy) | ✅ |
| Mock data (stabilné) | ✅ |
| DataGrid s column filters | ✅ |
| Keyboard navigation | ✅ |
| Column config dialog | ✅ |
| Drag & drop v gride (hlavičky) | ✅ |
| Resize stĺpcov (drag) | ✅ |
| Zoznam faktúr | ✅ |
| Detail faktúry + položky | ✅ |

---

## 🐛 Bug na opravu

Drag & drop v dialógu - konflikt: celý riadok je draggable, ale má byť len GripVertical ikona

---

## 📋 Next Steps

1. **Fix dialog drag** - draggable len na GripVertical
2. Test s reálnym backendom
3. Schvaľovací workflow
4. Docker deployment

---

## 🔍 RAG Query

```
https://rag-api.icc.sk/search?query=supplier_invoice_staging_web+datagrid&limit=5
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
