"""
Krok 2: Vytvorenie všetkých súborov Claude Tools
Projekt: nex-automat

Tento skript vytvorí všetky potrebné súbory v správnych adresároch.
"""

from pathlib import Path


def create_file(path: Path, content: str):
    """Vytvorí súbor s daným obsahom"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        print(f"  ✅ Vytvorené: {path.relative_to(Path('C:/Development/nex-automat'))}")
        return True
    except Exception as e:
        print(f"  ❌ Chyba pri vytváraní {path}: {e}")
        return False


def create_all_files():
    """Vytvorí všetky Claude Tools súbory"""

    print("\n" + "=" * 60)
    print("KROK 2: Vytvorenie súborov Claude Tools")
    print("=" * 60 + "\n")

    project_root = Path("C:/Development/nex-automat")
    tools_dir = project_root / "tools"

    files_to_create = []

    # Zoznam súborov ktoré sa majú vytvoriť
    # Formát: (relatívna_cesta, placeholder_obsah)

    print("Pripravujem súbory...\n")

    # Python súbory v tools/
    python_files = [
        "installer.py",
        "claude-chat-loader.py",
        "claude-hotkeys.py",
        "artifact-server.py",
        "session-notes-manager.py",
        "context-compressor.py"
    ]

    for filename in python_files:
        files_to_create.append((
            tools_dir / filename,
            f'"""\n{filename} - nex-automat projekt\nTODO: Skopíruj obsah z artifact\n"""\n\nprint("TODO: Implementuj {filename}")\n'
        ))

    # PowerShell súbory v tools/
    ps_files = [
        "start-claude-tools.ps1",
        "stop-claude-tools.ps1"
    ]

    for filename in ps_files:
        files_to_create.append((
            tools_dir / filename,
            f'# {filename} - nex-automat projekt\n# TODO: Skopíruj obsah z artifact\n\nWrite-Host "TODO: Implementuj {filename}"\n'
        ))

    # Browser extension súbory
    extension_dir = tools_dir / "browser-extension" / "claude-artifact-saver"

    extension_files = {
        "manifest.json": '{\n  "manifest_version": 3,\n  "name": "Claude Artifact Saver",\n  "version": "1.0.0"\n}\n',
        "content.js": '// content.js - nex-automat projekt\n// TODO: Skopíruj obsah z artifact\n\nconsole.log("TODO: Implementuj content.js");\n',
        "styles.css": '/* styles.css - nex-automat projekt */\n/* TODO: Skopíruj obsah z artifact */\n',
        "background.js": '// background.js - nex-automat projekt\n// TODO: Skopíruj obsah z artifact\n\nconsole.log("TODO: Implementuj background.js");\n',
        "popup.html": '<!DOCTYPE html>\n<html>\n<head>\n    <title>Claude Artifact Saver</title>\n</head>\n<body>\n    <h1>TODO: Skopíruj obsah z artifact</h1>\n</body>\n</html>\n'
    }

    for filename, content in extension_files.items():
        files_to_create.append((extension_dir / filename, content))

    # README a dokumentácia
    files_to_create.append((
        project_root / "README.md",
        "# Claude Tools - nex-automat projekt\n\nTODO: Skopíruj obsah z artifact\n"
    ))

    files_to_create.append((
        tools_dir / "INSTALLATION_GUIDE.md",
        "# Inštalačný návod\n\nTODO: Skopíruj obsah z artifact\n"
    ))

    # Vytvor všetky súbory
    success_count = 0
    failed_count = 0

    for file_path, content in files_to_create:
        if create_file(file_path, content):
            success_count += 1
        else:
            failed_count += 1

    # Výsledok
    print("\n" + "=" * 60)
    print("VÝSLEDOK:")
    print("=" * 60)
    print(f"  Vytvorených: {success_count}")
    if failed_count > 0:
        print(f"  Chýb: {failed_count}")
    print()

    # Zoznam vytvorených súborov
    print("Vytvorené súbory:\n")
    print("📂 tools/")
    for f in python_files + ps_files + ["INSTALLATION_GUIDE.md"]:
        print(f"  ├── {f}")
    print("  └── browser-extension/")
    print("      └── claude-artifact-saver/")
    for f in extension_files.keys():
        print(f"          ├── {f}")
    print("\n📂 root/")
    print("  └── README.md")

    print("\n" + "=" * 60)
    print("⚠️  DÔLEŽITÉ:")
    print("=" * 60)
    print("Vytvorené súbory obsahujú LEN placeholder obsah.")
    print("Musíš MANUÁLNE skopírovať obsah z artifacts do týchto súborov:")
    print()
    print("1. Otvor každý artifact v tomto chate")
    print("2. Skopíruj obsah")
    print("3. Vlož do príslušného súboru")
    print()
    print("ALEBO použijem automatický skript v kroku 3.")
    print("=" * 60)

    print("\n✅ Krok 2 DOKONČENÝ\n")
    print("Ďalší krok: Automatické naplnenie súborov obsahom z artifacts\n")

    return success_count > 0


if __name__ == "__main__":
    success = create_all_files()
    exit(0 if success else 1)