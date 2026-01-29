"""
Claude Chat Loader - nex-automat projekt
Automatické načítanie a vloženie init promptu do nového chatu
"""

import time
from datetime import datetime
from pathlib import Path

import keyboard
import pyperclip

try:
    from config import SESSION_NOTES_DIR
except ImportError:
    SESSION_NOTES_DIR = Path("/init_chat")


class ChatLoader:
    def __init__(self):
        self.session_notes_dir = Path(SESSION_NOTES_DIR)
        self.init_prompt_file = self.session_notes_dir / "INIT_PROMPT_NEW_CHAT.md"
        self.session_notes_file = self.session_notes_dir / "SESSION_NOTES.md"

    def load_and_paste_init_prompt(self):
        """Načíta init prompt a vloží ho do chatu"""
        try:
            if not self.init_prompt_file.exists():
                self.show_notification("❌ Init prompt neexistuje", error=True)
                self.create_basic_init_prompt()
                return

            # Načítaj obsah
            content = self.init_prompt_file.read_text(encoding="utf-8")

            # Pridaj timestamp
            enhanced_content = f"""[Načítané: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]

{content}
"""

            # Skopíruj do schránky
            pyperclip.copy(enhanced_content)

            # Notifikácia
            char_count = len(enhanced_content)
            self.show_notification(f"✅ Init prompt v schránke ({char_count:,} znakov)")

            # Automatické vloženie po 2 sekundách
            print("⏳ Vkladám za 2 sekundy...")
            time.sleep(2)

            # Simuluj Ctrl+V
            keyboard.send("ctrl+v")
            print("✅ Vložené!")

        except Exception as e:
            self.show_notification(f"❌ Chyba: {e}", error=True)

    def create_basic_init_prompt(self):
        """Vytvor základný init prompt ak neexistuje"""
        print("📝 Vytváram základný init prompt...")

        basic_prompt = """# INIT PROMPT - Nový chat (nex-automat)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

[Tu bude automaticky vygenerovaný kontext z predchádzajúceho chatu]

## AKTUÁLNY PROJEKT
- NEX Automat v2.0
- Development: C:\\Development\\nex-automat
- Deployment: C:\\Development\\nex-automat-deployment

## WORKFLOW
Development → Git → Deployment

---

Pokračujem tam kde sme skončili v predchádzajúcom chate.
"""

        self.session_notes_dir.mkdir(parents=True, exist_ok=True)
        self.init_prompt_file.write_text(basic_prompt, encoding="utf-8")
        print(f"✅ Vytvorený: {self.init_prompt_file}")

    def quick_load_session_notes(self):
        """Rýchle načítanie session notes (bez paste)"""
        try:
            if not self.session_notes_file.exists():
                self.show_notification("❌ Session notes neexistujú", error=True)
                return

            content = self.session_notes_file.read_text(encoding="utf-8")
            pyperclip.copy(content)

            line_count = len(content.split("\n"))
            self.show_notification(f"✅ Session notes v schránke ({line_count} riadkov)")

        except Exception as e:
            self.show_notification(f"❌ Chyba: {e}", error=True)

    def show_notification(self, message: str, error: bool = False):
        """Zobraz konzolové notifikáciu"""
        if error:
            print(f"\n{'=' * 60}")
            print(f"⚠️ CHYBA: {message}")
            print(f"{'=' * 60}\n")
        else:
            print(f"\n✅ {message}\n")

    def get_file_info(self):
        """Zobraz informácie o súboroch"""
        print("\n" + "=" * 60)
        print("📂 CLAUDE CHAT LOADER - nex-automat")
        print("=" * 60)

        files = [("Init Prompt", self.init_prompt_file), ("Session Notes", self.session_notes_file)]

        for name, file_path in files:
            if file_path.exists():
                size = file_path.stat().st_size
                modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                print(f"\n{name}:")
                print(f"  📄 {file_path}")
                print(f"  📏 {size:,} bytov")
                print(f"  🕐 {modified.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n{name}:")
                print(f"  ❌ Neexistuje: {file_path}")

        print("\n" + "=" * 60 + "\n")


def main():
    """Hlavná funkcia - spustí sa ako samostatný proces"""
    loader = ChatLoader()

    print("\n" + "=" * 60)
    print("🚀 Claude Chat Loader - AKTÍVNY (nex-automat)")
    print("=" * 60)
    print("\nHotkey: Ctrl+Alt+L = Load & paste init prompt")
    print("Stlač Ctrl+C pre ukončenie")
    print("\n" + "=" * 60 + "\n")

    # Zobraz info o súboroch
    loader.get_file_info()

    # Registruj hotkey
    keyboard.add_hotkey("ctrl+alt+l", loader.load_and_paste_init_prompt)

    # Čakaj na stlačenie
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Claude Chat Loader ukončený")


if __name__ == "__main__":
    main()
