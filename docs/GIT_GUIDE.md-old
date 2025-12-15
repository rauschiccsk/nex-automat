# Git Workflow Guide - PyCharm

**Projekt:** NEX Automat v2.0  
**Branching Strategy:** main / develop / hotfix_v2.0

---

## 📌 Základný Prehľad Branches

| Branch        | Účel                        | Push Oprávnenie      |
| ------------- | --------------------------- | -------------------- |
| `main`        | Produkcia (tagged releases) | Len cez merge + tag  |
| `develop`     | Nový vývoj (features)       | Priamy commit & push |
| `hotfix_v2.0` | Bugfixy pre v2.0.x          | Priamy commit & push |

---

## 🔄 1. Prepínanie medzi Branches

### Metóda 1: Pravý Dolný Roh (odporúčané)

1. **Klikni na branch name v pravom dolnom rohu** (napr. "hotfix_v2.0")
2. Zobrazí sa popup okno so zoznamom branches
3. **Vyber branch** z jednej z kategórií:
   - **Local Branches:** branches na tvojom počítači
   - **Remote Branches:** branches na GitHube
4. **Klikni "Checkout"**

### Metóda 2: Cez Menu

```
Git → Branches → [vyber branch] → Checkout
```

### Kontrola Aktuálneho Branch

**Vždy pred commitom skontroluj:**

- Pravý dolný roh PyCharm: zobrazuje aktuálny branch
- Status bar: `Git: [branch-name]`

---

## 💾 2. Commit & Push Workflow

### Pre Nový Vývoj (Features)

```
1. Prepni na: develop
2. Vytvor/uprav súbory
3. Ctrl+K (Commit)
4. Napíš commit message
5. Tlačidlo: "Commit and Push" alebo "Commit"
6. Ak si dal len "Commit", potom: Ctrl+Shift+K (Push)
```

**Commit Message Template:**

```
feat: krátky popis (max 50 znakov)

Detailný popis čo sa zmenilo a prečo.
```

### Pre Bugfix

```
1. Prepni na: hotfix_v2.0
2. Oprav bug
3. Ctrl+K (Commit)
4. Commit message: "fix: popis bugu"
5. Commit and Push
```

**Commit Message Template:**

```
fix: krátky popis bugu

Popis problému a riešenia.
Fixes #issue_number (ak existuje)
```

---

## 🔀 3. Merge Workflow

### Merge Hotfix do Main (Produkcia)

```
1. Prepni na: main
   Git → Branches → main → Checkout

2. Merge hotfix_v2.0 do main:
   Git → Merge → hotfix_v2.0 → Merge

3. Vyriešiť konflikty (ak sú)

4. Push do main:
   Ctrl+Shift+K

5. Merge hotfix_v2.0 aj do develop:
   - Prepni na develop
   - Git → Merge → hotfix_v2.0 → Merge
   - Push
```

### Merge Develop do Main (Release)

```
1. Prepni na: main
2. Git → Merge → develop → Merge
3. Vyriešiť konflikty
4. Push
```

---

## 🏷️ 4. Tagovanie Verzií

### Po Merge do Main - Vytvor Tag

```
1. Uisti sa že si na: main

2. Git → New Tag

3. Zadaj tag name:
   - Pre bugfix: v2.0.1, v2.0.2...
   - Pre minor release: v2.1.0, v2.2.0...
   - Pre major release: v3.0.0

4. Tag message (optional): "Release v2.0.1 - bugfixes"

5. Push tags:
   Git → Push → zaškrtni "Push Tags"
```

---

## 📋 5. Workflow Scenáre

### Scenár A: Vyvíjam Nový Feature

```
✓ Prepni na: develop
✓ Pracuj na feature
✓ Commit & Push do develop
✓ (Neskôr) Merge develop → main (pri release)
```

### Scenár B: Opravujem Bug v Produkcii

```
✓ Prepni na: hotfix_v2.0
✓ Oprav bug
✓ Commit & Push do hotfix_v2.0
✓ Merge hotfix_v2.0 → main
✓ Tag novú verziu (v2.0.1)
✓ Push tags
✓ Merge hotfix_v2.0 → develop (aby develop mal bugfix)
```

### Scenár C: Release Novej Verzie

```
✓ Prepni na: develop
✓ Skontroluj že všetko je hotové
✓ Prepni na: main
✓ Merge develop → main
✓ Tag novú verziu (v2.1.0)
✓ Push main + tags
```

---

## 🚨 6. Dôležité Pravidlá

### ❌ NIKDY

- ❌ Nepushuj priamo do `main` bez merge
- ❌ Nemiešaj hotfixy a features v jednom commite
- ❌ Nezabudni pushnúť tags po vytvorení

### ✅ VŽDY

- ✅ Skontroluj aktuálny branch pred commitom (pravý dolný roh)
- ✅ Píš zrozumiteľné commit messages
- ✅ Taguj verzie v `main` po merge
- ✅ Merge hotfixy aj do `develop`

---

## 🔍 7. Užitočné Skratky

| Akcia    | Skratka         |
| -------- | --------------- |
| Commit   | `Ctrl+K`        |
| Push     | `Ctrl+Shift+K`  |
| Pull     | `Ctrl+T`        |
| Git Log  | `Alt+9` → Git   |
| Branches | Pravý dolný roh |

---

## 📞 Riešenie Problémov

### "Cannot checkout - uncommitted changes"

```
1. Commit alebo stash zmeny
   Git → Uncommitted Changes → Stash Changes
2. Prepni branch
3. Vráť stash:
   Git → Uncommitted Changes → Unstash Changes
```

### "Merge conflict"

```
1. PyCharm automaticky zobrazí konfliktné súbory
2. Klikni na súbor → Resolve Conflict
3. Vyber verziu alebo edituj manuálne
4. Mark as Resolved
5. Commit merge
```

### "Push rejected"

```
1. Pull najprv: Ctrl+T
2. Vyriešiť konflikty
3. Push znova: Ctrl+Shift+K
```

---

## 📚 Ďalšie Zdroje

- [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated:** 2025-11-25  
**Version:** 1.0