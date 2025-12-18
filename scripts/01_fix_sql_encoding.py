"""
Fix UTF-8 encoding in SQL schema file.
Opravuje poškodené UTF-8 znaky (mojibake) na správne slovenské znaky.
"""

from pathlib import Path

SQL_FILE = Path("apps/supplier-invoice-staging/database/schemas/001_supplier_invoice_staging.sql")

# Mapovanie poškodených sekvencií na správne znaky
ENCODING_FIXES = {
    "ÄŒakÃ¡": "Čaká",
    "PoloÅ¾ky": "Položky",
    "napÃ¡rovanÃ©": "napárované",
    "SchvÃ¡lenÃ©": "Schválené",
    "operÃ¡torom": "operátorom",
    "ImportovanÃ©": "Importované",
    "HlaviÄky": "Hlavičky",
    "faktÃºr": "faktúr",
    "SÃšBORY": "SÚBORY",
    "Å¡tatistÃ­k": "štatistík",
    "hlaviÄke": "hlavičke",
    "hlaviÄky": "hlavičky",
    "dodÃ¡vateÄ¾skÃ½ch": "dodávateľských",
    "poloÅ¾ky": "položky",
    "PomocnÃ¡": "Pomocná",
    "ukladÃ¡me": "ukladáme",
    "pÃ¡rovanie": "párovanie",
    "aktualizÃ¡ciu": "aktualizáciu",
    "KOMENTÃRE": "KOMENTÁRE",
}

def fix_encoding():
    if not SQL_FILE.exists():
        print(f"ERROR: Súbor {SQL_FILE} neexistuje!")
        return False

    print(f"Čítam: {SQL_FILE}")
    content = SQL_FILE.read_text(encoding='utf-8')

    original_content = content
    fixes_applied = 0

    for broken, correct in ENCODING_FIXES.items():
        if broken in content:
            count = content.count(broken)
            content = content.replace(broken, correct)
            print(f"  Opravené: '{broken}' → '{correct}' ({count}x)")
            fixes_applied += count

    if fixes_applied == 0:
        print("Žiadne opravy neboli potrebné - súbor je OK.")
        return True

    # Záloha pôvodného súboru
    backup_file = SQL_FILE.with_suffix('.sql.bak')
    backup_file.write_text(original_content, encoding='utf-8')
    print(f"Záloha vytvorená: {backup_file}")

    # Uloženie opraveného súboru
    SQL_FILE.write_text(content, encoding='utf-8')
    print(f"Uložené: {SQL_FILE}")
    print(f"Celkom opravených: {fixes_applied} výskytov")

    return True

if __name__ == "__main__":
    fix_encoding()