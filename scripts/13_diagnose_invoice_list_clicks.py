r"""
Script 13: Diagnostika - ako funguje kliknutie na faktúru.

Nájde signály a metódy pre otvorenie detailu faktúry.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
INVOICE_LIST_WIDGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"
MAIN_WINDOW = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def search_in_file(file_path, search_terms):
    """Vyhľadá search_terms v súbore."""
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding='utf-8')
    lines = content.splitlines()

    results = []
    for i, line in enumerate(lines, 1):
        for term in search_terms:
            if term.lower() in line.lower():
                results.append((i, line.strip(), term))

    return results


def main():
    """Analyzuje invoice list widget."""
    print("=" * 70)
    print("DIAGNOSTIKA: Ako sa otvára detail faktúry")
    print("=" * 70)

    # Hľadaj signály pre kliknutie
    click_terms = [
        'clicked', 'doubleClicked', 'activated', 'pressed',
        'selectionChanged', 'currentChanged', 'itemClicked',
        'show_items', 'open_invoice', 'detail', 'items'
    ]

    print("\n1. INVOICE_LIST_WIDGET.PY:")
    print("-" * 70)
    results = search_in_file(INVOICE_LIST_WIDGET, click_terms)

    if results:
        for line_no, line, term in results:
            print(f"  {line_no:4d}: {line[:80]}")
    else:
        print("  ❌ Nenašlo sa nič relevantné")

    print("\n2. MAIN_WINDOW.PY:")
    print("-" * 70)
    results = search_in_file(MAIN_WINDOW, click_terms)

    if results:
        for line_no, line, term in results:
            print(f"  {line_no:4d}: {line[:80]}")
    else:
        print("  ❌ Nenašlo sa nič relevantné")

    print("\n" + "=" * 70)
    print("ZÁVER:")
    print("=" * 70)
    print("Hľadaj riadky s .clicked, .doubleClicked, connect() atď.")
    print("To ukáže kde sa spája signal pre kliknutie na faktúru.")


if __name__ == "__main__":
    main()