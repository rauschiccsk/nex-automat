"""
Create new chat artifacts: SESSION archive, KNOWLEDGE docs, update ARCHIVE_INDEX,
create INIT_PROMPT, run RAG update.

Run from: C:/Development/nex-automat

Usage:
    python new_chat.py

Then Claude generates content as artifacts, user pastes into script prompts.
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")
SESSION_DATE = datetime.now().strftime("%Y-%m-%d")


def get_next_session_number() -> str:
    """Get next session number for today (01, 02, 03...)."""
    sessions_dir = PROJECT_ROOT / "docs" / "archive" / "sessions"

    if not sessions_dir.exists():
        return "01"

    # Find existing sessions for today
    pattern = f"SESSION_{SESSION_DATE}_*"
    existing = list(sessions_dir.glob(pattern))

    if not existing:
        return "01"

    # Extract numbers and find max
    numbers = []
    for f in existing:
        parts = f.stem.split("_")
        if len(parts) >= 3:
            try:
                num = int(parts[2])
                numbers.append(num)
            except ValueError:
                continue

    if not numbers:
        return "01"

    return f"{max(numbers) + 1:02d}"


def create_session_archive(session_name: str, session_content: str) -> str:
    """Create SESSION_*.md archive file with sequential number."""
    session_num = get_next_session_number()

    archive_dir = PROJECT_ROOT / "docs" / "archive" / "sessions"
    archive_dir.mkdir(parents=True, exist_ok=True)

    filename = f"SESSION_{SESSION_DATE}_{session_num}_{session_name}.md"
    filepath = archive_dir / filename
    filepath.write_text(session_content, encoding="utf-8")
    print(f"✓ Created {filepath.relative_to(PROJECT_ROOT)}")
    return filename


def create_knowledge_doc(category: str, topic: str, content: str) -> str:
    """Create knowledge document in docs/knowledge/{category}/."""
    knowledge_dir = PROJECT_ROOT / "docs" / "knowledge" / category
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{SESSION_DATE}_{topic}.md"
    filepath = knowledge_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"✓ Created {filepath.relative_to(PROJECT_ROOT)}")
    return filename


def update_archive_index(session_filename: str, session_name: str, summary: str):
    """Update ARCHIVE_INDEX.md with new session."""
    index_path = PROJECT_ROOT / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    if not index_path.exists():
        print(f"⚠ {index_path} not found, skipping update")
        return

    content = index_path.read_text(encoding="utf-8")

    # Add new entry after the header row
    new_entry = f"| {SESSION_DATE} | {session_name} | {summary} | sessions/{session_filename} |"

    # Find the table and add entry
    if "| Dátum |" in content or "| Datum |" in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("| Dátum |") or line.startswith("| Datum |"):
                # Insert after header and separator (i+2)
                lines.insert(i + 2, new_entry)
                break
        content = "\n".join(lines)
        index_path.write_text(content, encoding="utf-8")
        print(f"✓ Updated {index_path.relative_to(PROJECT_ROOT)}")
    else:
        print(f"⚠ Could not find table in {index_path}")


def create_init_prompt(init_content: str):
    """Create INIT_PROMPT_NEW_CHAT.md in project root."""
    filepath = PROJECT_ROOT / "INIT_PROMPT_NEW_CHAT.md"
    filepath.write_text(init_content, encoding="utf-8")
    print(f"✓ Created {filepath.relative_to(PROJECT_ROOT)}")


def run_rag_update():
    """Run RAG update for new knowledge files."""
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, "tools/rag/rag_update.py", "--new"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            print(f"✓ RAG update completed")
            if result.stdout:
                # Print just summary lines
                for line in result.stdout.split("\n"):
                    if "Found" in line or "Indexed" in line or "COMPLETE" in line:
                        print(f"  {line.strip()}")
        else:
            print(f"⚠ RAG update failed: {result.stderr}")
    except Exception as e:
        print(f"⚠ Could not run RAG update: {e}")


def read_multiline_input(prompt: str) -> str:
    """Read multiline input until empty line."""
    print(prompt)
    print("(Paste content, then press Enter twice to finish)")
    print("-" * 40)

    lines = []
    empty_count = 0

    while True:
        try:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append("")
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break

    return "\n".join(lines).strip()


def main():
    print()
    print("=" * 60)
    print(" NEW CHAT - Create Session Archive & Knowledge Docs")
    print("=" * 60)
    print()

    # 1. Session name
    session_name = input("Session name (slug, e.g., 'rag-knowledge-system'): ").strip()
    if not session_name:
        print("❌ Session name required!")
        return

    session_summary = input("Session summary (short, for index): ").strip()

    # 2. Session content
    print()
    session_content = read_multiline_input("SESSION ARCHIVE content (markdown):")

    if not session_content:
        print("❌ Session content required!")
        return

    # 3. Knowledge documents (optional, multiple)
    knowledge_docs = []
    print()
    print("-" * 60)
    print("KNOWLEDGE DOCUMENTS (optional)")
    print("Categories: decisions, development, deployment, scripts, specifications")
    print("-" * 60)

    while True:
        print()
        add_knowledge = input("Add knowledge document? (y/n): ").strip().lower()
        if add_knowledge != 'y':
            break

        category = input("  Category (decisions/development/deployment/scripts/specifications): ").strip()
        if category not in ['decisions', 'development', 'deployment', 'scripts', 'specifications']:
            print(f"  ⚠ Invalid category: {category}")
            continue

        topic = input("  Topic slug (e.g., 'db-schema-xml-nex-prefixes'): ").strip()
        if not topic:
            print("  ⚠ Topic required")
            continue

        print()
        content = read_multiline_input(f"  Content for {category}/{topic}:")

        if content:
            knowledge_docs.append((category, topic, content))
            print(f"  ✓ Queued: {category}/{SESSION_DATE}_{topic}.md")

    # 4. Init prompt
    print()
    print("-" * 60)
    init_content = read_multiline_input("INIT_PROMPT content (markdown):")

    if not init_content:
        print("⚠ No init prompt provided, skipping")

    # Execute
    print()
    print("=" * 60)
    print(" CREATING FILES")
    print("=" * 60)
    print()

    # Create session archive
    session_filename = create_session_archive(session_name, session_content)

    # Update archive index
    update_archive_index(session_filename, session_name, session_summary)

    # Create knowledge docs
    for category, topic, content in knowledge_docs:
        create_knowledge_doc(category, topic, content)

    # Create init prompt
    if init_content:
        create_init_prompt(init_content)

    # Run RAG update
    print()
    print("-" * 60)
    print("Running RAG update...")
    run_rag_update()

    # Summary
    print()
    print("=" * 60)
    print(" DONE!")
    print("=" * 60)
    print()
    print("Created files:")
    print(f"  • Session: docs/archive/sessions/{session_filename}")
    for category, topic, _ in knowledge_docs:
        print(f"  • Knowledge: docs/knowledge/{category}/{SESSION_DATE}_{topic}.md")
    if init_content:
        print(f"  • Init prompt: INIT_PROMPT_NEW_CHAT.md")
    print()
    print("Next steps:")
    print("  1. git add -A && git commit -m 'Session archive + knowledge docs'")
    print("  2. Start new chat with INIT_PROMPT_NEW_CHAT.md")


if __name__ == "__main__":
    main()