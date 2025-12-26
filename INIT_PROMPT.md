# INIT PROMPT - Supplier Invoice Staging Web UI - Editable Grid

**Projekt:** nex-automat / supplier-invoice-staging-web
**Typ:** React Web UI - editovateľné bunky v gride
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT FOCUS

Implementovať editovateľné bunky v DataGride pre:
- Obchodná marža (%) - zapísať a prepočítať predajnú cenu
- Predajná cena - zapísať a prepočítať maržu
- Celková hodnota faktúry - automatický prepočet

---

## ✅ Čo je hotové

| Komponenta | Status |
|------------|--------|
| Vite + React + TypeScript | ✅ |
| DataGrid s column filters | ✅ |
| Numerický filter (rozsahy) | ✅ |
| Keyboard navigation | ✅ |
| Column config dialog | ✅ |
| Drag & drop (grid + dialog) | ✅ |
| Resize stĺpcov | ✅ |
| Všetky DB stĺpce | ✅ |
| Kompaktný layout | ✅ |

---

## 📋 Next Steps

1. **Editovateľné bunky** - marža, predajná cena
2. **Prepočty** - marža ↔ predajná cena
3. **Celková hodnota** - suma + prepočet
4. Test s reálnym backendom
5. Schvaľovací workflow

---

## 🔍 RAG Query

```
https://rag-api.icc.sk/search?query=supplier_invoice_staging_web+datagrid+editable&limit=5
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
