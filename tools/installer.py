"""
Claude Tools Installer - nex-automat projekt
Automatická inštalácia všetkých nástrojov pre efektívnu prácu s claude.ai
"""

import subprocess
import sys
from pathlib import Path


class ClaudeToolsInstaller:
    def __init__(self):
        self.project_root = Path("C:/Development/nex-automat")
        self.tools_dir = self.project_root / "tools"
        self.session_notes_dir = self.project_root / "SESSION_NOTES"

    def check_python(self):
        """Skontroluj Python verziu"""
        print("🔍 Kontrolujem Python...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} je príliš starý")
            print("   Potrebuješ Python 3.8+")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True

    def check_directories(self):
        """Skontroluj/vytvor adresárovú štruktúru"""
        print("\n🔍 Kontrolujem adresáre...")

        dirs = [
            self.project_root,
            self.tools_dir,
            self.session_notes_dir,
            self.tools_dir / "browser-extension" / "claude-artifact-saver",
        ]

        for d in dirs:
            if not d.exists():
                print(f"📁 Vytváram: {d}")
                d.mkdir(parents=True, exist_ok=True)
            else:
                print(f"✅ Existuje: {d}")

        return True

    def install_dependencies(self):
        """Nainštaluj Python dependencies"""
        print("\n📦 Inštalujem dependencies...")

        packages = [
            "pyperclip",
            "keyboard",
            "anthropic",
            "fastapi",
            "uvicorn",
            "pydantic",
        ]

        for pkg in packages:
            print(f"   Inštalujem {pkg}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pkg],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"   ✅ {pkg}")
            except subprocess.CalledProcessError:
                print(f"   ❌ {pkg} - chyba inštalácie")
                return False

        return True

    def create_config(self):
        """Vytvor konfiguračný súbor"""
        print("\n⚙️ Vytváram konfiguráciu...")

        config_content = f"""# Claude Tools Configuration - nex-automat
# Generované: {Path(__file__).name}

PROJECT_ROOT = r"C:\\Development\nex-automat"
TOOLS_DIR = r"C:\\Development\nex-automat\tools"
SESSION_NOTES_DIR = r"C:\\Development\nex-automat\\SESSION_NOTES"

# Artifact Server
ARTIFACT_SERVER_PORT = 8765
ARTIFACT_SERVER_HOST = "localhost"

# Claude API (voliteľné - pre context compressor)
ANTHROPIC_API_KEY = ""  # Vlož sem svoj API key ak chceš použiť compressor

# Hotkeys (Ctrl+Alt+...)
HOTKEY_LOAD_INIT = "l"
HOTKEY_COPY_NOTES = "s"
HOTKEY_GIT_STATUS = "g"
HOTKEY_DEPLOYMENT_INFO = "d"
HOTKEY_NEW_CHAT = "n"
"""

        config_file = self.tools_dir / "config.py"
        config_file.write_text(config_content, encoding="utf-8")
        print(f"✅ Konfigurácia: {config_file}")
        return True

    def create_session_notes_template(self):
        """Vytvor template pre session notes"""
        print("\n📝 Vytváram session notes template...")

        template = """# SESSION NOTES - nex-automat

## CURRENT STATUS
[Aktuálny stav práce]

## NEXT STEPS
1. [Ďalší krok]

## COMPLETED
- [Dokončené úlohy]

## NOTES
[Poznámky]
"""

        notes_file = self.session_notes_dir / "SESSION_NOTES.md"
        if not notes_file.exists():
            notes_file.write_text(template, encoding="utf-8")
            print(f"✅ Template: {notes_file}")
        else:
            print(f"⏭️ Preskakujem (už existuje): {notes_file}")

        return True

    def verify_installation(self):
        """Overenie inštalácie"""
        print("\n🔍 Overujem inštaláciu...")

        required_files = [
            self.tools_dir / "config.py",
            self.tools_dir / "claude-chat-loader.py",
            self.tools_dir / "claude-hotkeys.py",
            self.tools_dir / "artifact-server.py",
            self.tools_dir / "session-notes-manager.py",
            self.tools_dir / "start-claude-tools.ps1",
        ]

        all_ok = True
        for f in required_files:
            if f.exists():
                print(f"✅ {f.name}")
            else:
                print(f"❌ {f.name} - CHÝBA!")
                all_ok = False

        return all_ok

    def print_next_steps(self):
        """Vypíš ďalšie kroky"""
        print("\n" + "=" * 60)
        print("🎉 INŠTALÁCIA DOKONČENÁ!")
        print("=" * 60)
        print("\nĎALŠIE KROKY:")
        print("\n1. SPUSTI NÁSTROJE:")
        print(f"   cd {self.tools_dir}")
        print("   .\\start-claude-tools.ps1")
        print("\n2. HOTKEYS (po spustení):")
        print("   Ctrl+Alt+L - Load init prompt")
        print("   Ctrl+Alt+S - Copy session notes")
        print("   Ctrl+Alt+G - Git status")
        print("   Ctrl+Alt+D - Deployment info")
        print("   Ctrl+Alt+N - New chat template")
        print("\n3. BROWSER EXTENSION (voliteľné):")
        print("   Chrome → Extensions → Load unpacked")
        print(
            f"   Vyber: {self.tools_dir / 'browser-extension' / 'claude-artifact-saver'}"
        )
        print("\n4. CLAUDE API KEY (voliteľné - pre compressor):")
        print(f"   Uprav: {self.tools_dir / 'config.py'}")
        print("   Pridaj: ANTHROPIC_API_KEY = 'sk-ant-...'")
        print("\n" + "=" * 60)

    def run(self):
        """Spusti inštaláciu"""
        print("=" * 60)
        print("Claude Tools - nex-automat projekt")
        print("=" * 60)

        steps = [
            ("Kontrola Python", self.check_python),
            ("Kontrola adresárov", self.check_directories),
            ("Inštalácia dependencies", self.install_dependencies),
            ("Vytvorenie konfigurácie", self.create_config),
            ("Vytvorenie templates", self.create_session_notes_template),
        ]

        for name, func in steps:
            if not func():
                print(f"\n❌ CHYBA pri: {name}")
                print("   Inštalácia prerušená")
                return False

        print("\n✅ Všetky komponenty nainštalované")
        print("\n⚠️ POZNÁMKA: Teraz skopíruj všetky súbory z artifacts")
        print("   do príslušných adresárov:")
        print(f"   - Python skripty → {self.tools_dir}")
        print(f"   - PowerShell skripty → {self.tools_dir}")
        print(f"   - Browser extension → {self.tools_dir / 'browser-extension'}")

        self.print_next_steps()
        return True


if __name__ == "__main__":
    installer = ClaudeToolsInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)
