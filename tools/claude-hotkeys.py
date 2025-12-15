"""
Claude Hotkeys - nex-automat projekt
Klávesové skratky pre časté operácie
"""

import keyboard
import pyperclip
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from config import PROJECT_ROOT, SESSION_NOTES_DIR
except ImportError:
    PROJECT_ROOT = Path("C:/Development/nex-automat")
    SESSION_NOTES_DIR = Path("/init_chat")

class ClaudeHotkeys:
    def __init__(self):
        self.project_root = Path(PROJECT_ROOT)
        self.session_notes_dir = Path(SESSION_NOTES_DIR)
        self.deployment_root = Path("C:/Development/nex-automat-deployment")

    def setup_hotkeys(self):
        """Registruj všetky hotkeys"""

        hotkeys = [
            ('ctrl+windows+s', self.copy_session_notes, "Copy Session Notes"),
            ('ctrl+windows+g', self.show_git_status, "Git Status"),
            ('ctrl+windows+d', self.show_deployment_info, "Deployment Info"),
            ('ctrl+windows+n', self.new_chat_template, "New Chat Template"),
            ('ctrl+windows+i', self.show_info, "Show Info"),
        ]

        print("\n" + "="*60)
        print("⌨️  CLAUDE HOTKEYS - nex-automat")
        print("="*60)
        print("\nDostupné skratky (Ctrl+Win+...):")

        for hotkey, func, desc in hotkeys:
            keyboard.add_hotkey(hotkey, func)
            key = hotkey.split('+')[-1].upper()
            print(f"  {key} - {desc}")

        print("\nStlač Ctrl+C pre ukončenie")
        print("="*60 + "\n")

    def copy_session_notes(self):
        """Skopíruj session notes do schránky"""
        notes_file = self.session_notes_dir / "SESSION_NOTES.md"

        if not notes_file.exists():
            self.notify("❌ Session notes neexistujú")
            return

        content = notes_file.read_text(encoding='utf-8')
        pyperclip.copy(content)

        lines = len(content.split('\n'))
        chars = len(content)
        self.notify(f"✅ Session notes v schránke ({lines} riadkov, {chars:,} znakov)")

    def show_git_status(self):
        """Zobraz a skopíruj Git status"""
        try:
            # Git status
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                self.notify("❌ Git chyba - nie si v Git repozitári?")
                return

            status = result.stdout.strip()

            if not status:
                status = "✅ Žiadne zmeny (working tree clean)"

            # Pridaj header
            output = f"""GIT STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project: {self.project_root}

{status}
"""

            pyperclip.copy(output)
            print("\n" + "="*60)
            print(output)
            print("="*60)
            print("✅ Git status skopírovaný do schránky\n")

        except subprocess.TimeoutExpired:
            self.notify("❌ Git timeout - príliš pomalý")
        except FileNotFoundError:
            self.notify("❌ Git nenájdený - nie je nainštalovaný?")
        except Exception as e:
            self.notify(f"❌ Git chyba: {e}")

    def show_deployment_info(self):
        """Info o deployment prostredí"""

        # Zisti či deployment existuje
        deployment_exists = self.deployment_root.exists()

        info = f"""DEPLOYMENT INFO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📂 CESTY:
Development:  {self.project_root}
Deployment:   {self.deployment_root}
              {'✅ Existuje' if deployment_exists else '❌ Neexistuje'}

🔄 WORKFLOW:
1. Development → úpravy v development prostredí
2. Git → commit & push
3. Deployment → deploy zo scriptu

⚠️ DÔLEŽITÉ:
- NIKDY nerob úpravy priamo v Deployment
- Vždy edituj v Development
- Deployment je read-only kópia

📋 QUICK ACTIONS:
- Git status: Ctrl+Win+G
- Session notes: Ctrl+Win+S
"""

        pyperclip.copy(info)
        print("\n" + info)
        print("✅ Deployment info skopírované do schránky\n")

    def new_chat_template(self):
        """Template pre žiadosť o nový chat"""
        template = "novy chat"
        pyperclip.copy(template)
        self.notify("✅ 'novy chat' v schránke - vlož do Claude a stlač Enter")

    def show_info(self):
        """Zobraz kompletnú info o projekte"""

        # Zisti Git branch
        try:
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            git_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "N/A"
        except:
            git_branch = "N/A"

        # Zisti posledný commit
        try:
            commit_result = subprocess.run(
                ['git', 'log', '-1', '--oneline'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            last_commit = commit_result.stdout.strip() if commit_result.returncode == 0 else "N/A"
        except:
            last_commit = "N/A"

        # Session notes info
        notes_file = self.session_notes_dir / "SESSION_NOTES.md"
        if notes_file.exists():
            notes_size = notes_file.stat().st_size
            notes_modified = datetime.fromtimestamp(notes_file.stat().st_mtime)
            notes_info = f"{notes_size:,} B | {notes_modified.strftime('%Y-%m-%d %H:%M')}"
        else:
            notes_info = "❌ Neexistujú"

        info = f"""
{"="*60}
PROJECT INFO - nex-automat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{"="*60}

📂 PROJECT:
   NEX Automat v2.0
   {self.project_root}

🔀 GIT:
   Branch: {git_branch}
   Last:   {last_commit}

📝 SESSION NOTES:
   {notes_info}

⌨️  HOTKEYS (Ctrl+Win+...):
   S - Copy Session Notes
   G - Git Status
   D - Deployment Info
   N - New Chat Template
   I - This Info

{"="*60}
"""

        print(info)
        pyperclip.copy(info)
        self.notify("✅ Project info v schránke")

    def notify(self, message: str):
        """Zobraz notifikáciu"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")

    def run(self):
        """Spusti hotkey listener"""
        self.setup_hotkeys()

        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Claude Hotkeys ukončené")

def main():
    hotkeys = ClaudeHotkeys()
    hotkeys.run()

if __name__ == "__main__":
    main()