"""
Update NEX_BRAIN_PRODUCT.md - Telegram Bot vylepšenia
Pridá sekciu s plánovanými vylepšeniami pre Telegram Bot
"""
from pathlib import Path

PRODUCT_DOC = Path("docs/knowledge/strategic/NEX_BRAIN_PRODUCT.md")

# Text na nájdenie (koniec Fázy 4)
FIND_TEXT = '''**Deliverable:** 
- MVP: Telegram bot pre pilotných používateľov
- Finálne: Integrovaný panel v NEX Automat'''

# Nový text s vylepšeniami
REPLACE_TEXT = '''**Deliverable:** 
- MVP: Telegram bot pre pilotných používateľov
- Finálne: Integrovaný panel v NEX Automat

#### Telegram Bot - Plánované vylepšenia

| Priorita | Vylepšenie | Popis |
|----------|------------|-------|
| 🟡 Medium | Formátovanie odpovede | Markdown, emoji, lepšia čitateľnosť |
| 🟡 Medium | História konverzácie | Pamätanie kontextu v rámci session |
| 🟢 Low | Inline tlačidlá | Rýchle akcie, follow-up otázky |
| 🟢 Low | Logging | Ukladanie dotazov do DB pre analytics |
| 🟢 Low | Feedback | Palec hore/dole pre kvalitu odpovede |

#### Produkčné boty (plánované)

| Bot | Firma | Status |
|-----|-------|--------|
| @NexBrainTest_bot | Development | ✅ Funkčný |
| @NexBrainICC_bot | ICC s.r.o. | 🔵 Planned |
| @NexBrainAndros_bot | ANDROS s.r.o. | 🔵 Planned |'''


def main():
    print("=" * 70)
    print("UPDATE: NEX_BRAIN_PRODUCT.md - Telegram vylepšenia")
    print("=" * 70)

    if not PRODUCT_DOC.exists():
        print(f"❌ Súbor neexistuje: {PRODUCT_DOC}")
        return False

    content = PRODUCT_DOC.read_text(encoding='utf-8')

    if FIND_TEXT not in content:
        print("❌ Nenašiel som miesto na vloženie")
        return False

    new_content = content.replace(FIND_TEXT, REPLACE_TEXT)
    PRODUCT_DOC.write_text(new_content, encoding='utf-8')

    print(f"✅ Aktualizovaný: {PRODUCT_DOC}")
    print()
    print("PRIDANÉ:")
    print("  - Tabuľka plánovaných vylepšení Telegram bota")
    print("  - Tabuľka produkčných botov (ICC, ANDROS)")
    print("=" * 70)

    return True


if __name__ == "__main__":
    main()