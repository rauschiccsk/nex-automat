"""
Session Notes Manager - nex-automat projekt
Automatická správa a analýza session notes
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from config import PROJECT_ROOT, SESSION_NOTES_DIR
except ImportError:
    PROJECT_ROOT = Path("C:/Development/nex-automat")
    SESSION_NOTES_DIR = Path("/init_chat")


class SessionNotesManager:
    def __init__(self):
        self.project_root = Path(PROJECT_ROOT)
        self.notes_dir = Path(SESSION_NOTES_DIR)
        self.notes_file = self.notes_dir / "SESSION_NOTES.md"
        self.enhanced_file = self.notes_dir / "SESSION_NOTES_ENHANCED.md"

    def analyze_content(self, content: str) -> dict:
        """Analyzuj obsah notes"""
        lines = content.split("\n")

        # Počet riadkov
        line_count = len(lines)

        # Hľadaj rôzne markery
        tasks = len(
            [l for l in lines if re.search(r"(\[ \]|TODO|NEXT)", l, re.IGNORECASE)]
        )
        completed = len(
            [l for l in lines if re.search(r"(\[x\]|DONE|COMPLETED)", l, re.IGNORECASE)]
        )

        # Zisti prioritu/status
        if re.search(r"(CRITICAL|ERROR|URGENT)", content, re.IGNORECASE):
            status = "🔴 Kritický"
            priority = "HIGH"
        elif re.search(r"(NEXT STEP|TODO|PENDING)", content, re.IGNORECASE):
            status = "🟡 Aktívny"
            priority = "MEDIUM"
        else:
            status = "🟢 OK"
            priority = "LOW"

        # Hľadaj sekcie
        sections = {
            "Current Status": bool(
                re.search(r"## CURRENT STATUS", content, re.IGNORECASE)
            ),
            "Next Steps": bool(re.search(r"## NEXT STEPS?", content, re.IGNORECASE)),
            "Completed": bool(re.search(r"## COMPLETED", content, re.IGNORECASE)),
            "Notes": bool(re.search(r"## NOTES", content, re.IGNORECASE)),
        }

        return {
            "lines": line_count,
            "chars": len(content),
            "tasks": tasks,
            "completed": completed,
            "status": status,
            "priority": priority,
            "sections": sections,
            "has_structure": all(sections.values()),
        }

    def get_git_info(self) -> dict:
        """Získaj Git informácie"""
        try:
            # Git branch
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Git status
            status = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Posledný commit
            last_commit = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5,
            )

            return {
                "branch": branch.stdout.strip() if branch.returncode == 0 else "N/A",
                "status": status.stdout.strip() if status.returncode == 0 else "N/A",
                "last_commit": last_commit.stdout.strip()
                if last_commit.returncode == 0
                else "N/A",
                "has_changes": bool(status.stdout.strip())
                if status.returncode == 0
                else False,
            }
        except:
            return {
                "branch": "N/A",
                "status": "N/A",
                "last_commit": "N/A",
                "has_changes": False,
            }

    def enhance_notes(self):
        """Vytvor enhanced verziu notes s metadatami"""
        if not self.notes_file.exists():
            print(f"❌ Session notes neexistujú: {self.notes_file}")
            return False

        # Načítaj obsah
        content = self.notes_file.read_text(encoding="utf-8")

        # Analyzuj
        stats = self.analyze_content(content)
        git_info = self.get_git_info()

        # Vytvor enhanced verziu
        enhanced = f"""# SESSION NOTES - ENHANCED (nex-automat)

**Vygenerované:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status:** {stats["status"]}
**Priorita:** {stats["priority"]}

---

## 📊 ŠTATISTIKY

| Metrika | Hodnota |
|---------|---------|
| Riadkov | {stats["lines"]:,} |
| Znakov | {stats["chars"]:,} |
| Otvorených úloh | {stats["tasks"]} |
| Dokončených úloh | {stats["completed"]} |
| Má štruktúru | {"✅ Áno" if stats["has_structure"] else "❌ Nie"} |

## 🔀 GIT INFO

| Info | Hodnota |
|------|---------|
| Branch | `{git_info["branch"]}` |
| Status | {"⚠️ Máš neuložené zmeny" if git_info["has_changes"] else "✅ Clean"} |
| Last commit | {git_info["last_commit"]} |

---

## 📋 PÔVODNÝ OBSAH

{content}

---

## 🔗 QUICK ACCESS

**Cesty:**
- 📂 Development: `{self.project_root}`
- 📝 Session notes: `{self.notes_file}`

**Hotkeys:**
- `Ctrl+Alt+S` - Copy session notes
- `Ctrl+Alt+G` - Git status
- `Ctrl+Alt+D` - Deployment info
- `Ctrl+Alt+N` - New chat template

**Workflow:**
Development → Git (commit/push) → Deployment

---

*Enhanced by Session Notes Manager*
"""

        # Ulož enhanced verziu
        self.enhanced_file.write_text(enhanced, encoding="utf-8")

        print(f"\n{'=' * 60}")
        print("📊 SESSION NOTES - ANALÝZA (nex-automat)")
        print("=" * 60)
        print(f"\nStatus: {stats['status']}")
        print(f"Priorita: {stats['priority']}")
        print(f"Riadkov: {stats['lines']:,}")
        print(f"Úloh: {stats['tasks']} otvorených, {stats['completed']} dokončených")
        print(f"Štruktúra: {'✅ OK' if stats['has_structure'] else '⚠️ Chýbajú sekcie'}")
        print(f"\nGit branch: {git_info['branch']}")
        print(
            f"Git status: {'⚠️ Neuložené zmeny' if git_info['has_changes'] else '✅ Clean'}"
        )
        print(f"\n✅ Enhanced notes: {self.enhanced_file}")
        print("=" * 60 + "\n")

        return True

    def create_template(self):
        """Vytvor template pre session notes"""
        template = f"""# SESSION NOTES - nex-automat

**Vytvorené:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Projekt:** NEX Automat v2.0

---

## CURRENT STATUS

[Aktuálny stav práce - čo sa práve rieši]

---

## NEXT STEPS

1. [ ] [Prvý nasledujúci krok]
2. [ ] [Druhý nasledujúci krok]

---

## COMPLETED

- [x] [Dokončená úloha 1]
- [x] [Dokončená úloha 2]

---

## NOTES

[Dôležité poznámky, zistenia, riešenia]

---

## ISSUES

[Aktuálne problémy, blockers]

---

*Template vytvorený Session Notes Managerom*
"""

        self.notes_dir.mkdir(parents=True, exist_ok=True)

        if self.notes_file.exists():
            backup = (
                self.notes_dir
                / f"SESSION_NOTES_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )
            self.notes_file.rename(backup)
            print(f"📦 Záloha: {backup}")

        self.notes_file.write_text(template, encoding="utf-8")
        print(f"✅ Template vytvorený: {self.notes_file}")

    def validate_structure(self):
        """Skontroluj či notes majú správnu štruktúru"""
        if not self.notes_file.exists():
            print("❌ Session notes neexistujú")
            return False

        content = self.notes_file.read_text(encoding="utf-8")
        stats = self.analyze_content(content)

        print(f"\n{'=' * 60}")
        print("✅ VALIDÁCIA ŠTRUKTÚRY (nex-automat)")
        print("=" * 60)

        required_sections = ["Current Status", "Next Steps", "Completed", "Notes"]

        for section in required_sections:
            has_it = stats["sections"].get(section, False)
            status_icon = "✅" if has_it else "❌"
            print(f"{status_icon} {section}")

        print("=" * 60 + "\n")

        if stats["has_structure"]:
            print("✅ Štruktúra je kompletná\n")
            return True
        else:
            print("⚠️ Chýbajú niektoré sekcie\n")
            return False


def main():
    """Hlavná funkcia"""
    import sys

    manager = SessionNotesManager()

    if len(sys.argv) < 2:
        print("\nSession Notes Manager (nex-automat) - Použitie:")
        print("  python session-notes-manager.py enhance   - Vytvor enhanced verziu")
        print("  python session-notes-manager.py validate  - Validuj štruktúru")
        print("  python session-notes-manager.py template  - Vytvor nový template")
        print()
        return

    command = sys.argv[1].lower()

    if command == "enhance":
        manager.enhance_notes()
    elif command == "validate":
        manager.validate_structure()
    elif command == "template":
        manager.create_template()
    else:
        print(f"❌ Neznámy príkaz: {command}")


if __name__ == "__main__":
    main()
