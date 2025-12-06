"""
Krok 1: Vytvorenie adresárovej štruktúry pre Claude Tools
Projekt: nex-automat
"""

from pathlib import Path


def create_directories():
    """Vytvorí potrebnú adresárovú štruktúru"""

    print("\n" + "=" * 60)
    print("KROK 1: Vytvorenie adresárovej štruktúry")
    print("=" * 60 + "\n")

    project_root = Path("C:/Development/nex-automat")

    # Zoznam adresárov na vytvorenie
    directories = [
        project_root,
        project_root / "tools",
        project_root / "tools" / "browser-extension",
        project_root / "tools" / "browser-extension" / "claude-artifact-saver",
        project_root / "SESSION_NOTES"
    ]

    print("Vytváram adresáre pre projekt nex-automat...\n")

    created_count = 0
    existing_count = 0

    for directory in directories:
        if directory.exists():
            print(f"  ✅ Už existuje: {directory}")
            existing_count += 1
        else:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Vytvorené: {directory}")
                created_count += 1
            except Exception as e:
                print(f"  ❌ Chyba pri vytváraní {directory}: {e}")
                return False

    print("\n" + "=" * 60)
    print("VÝSLEDOK:")
    print("=" * 60)
    print(f"  Vytvorených: {created_count}")
    print(f"  Už existovalo: {existing_count}")
    print()

    # Overenie štruktúry
    print("Overenie štruktúry:\n")
    print_tree(project_root, prefix="")

    print("\n✅ Krok 1 DOKONČENÝ\n")
    print("Ďalší krok: Skopírovať súbory z artifacts do vytvorených adresárov\n")

    return True


def print_tree(directory: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
    """Zobrazí strom adresárov"""
    if current_depth > max_depth:
        return

    if not directory.exists():
        return

    # Zobraz aktuálny adresár
    print(f"{prefix}{directory.name}/")

    if current_depth >= max_depth:
        return

    # Zobraz podadresáre
    try:
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        dirs = [item for item in items if item.is_dir()]

        for i, item in enumerate(dirs):
            is_last = i == len(dirs) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            connector = "└── " if is_last else "├── "

            print(f"{prefix}{connector}{item.name}/")
            print_tree(item, new_prefix, max_depth, current_depth + 1)
    except PermissionError:
        pass


if __name__ == "__main__":
    success = create_directories()
    exit(0 if success else 1)