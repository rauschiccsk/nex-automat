"""
Script 11: Archive Mágerstav Deployment Summary
Migrates MAGERSTAV_DEPLOYMET_SUMMARY.md-old to archive/deployments/
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def archive_magerstav_deployment():
    """Archive Mágerstav deployment summary to archive/deployments/"""

    # Paths
    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "MAGERSTAV_DEPLOYMET_SUMMARY.md-old"
    archive_dir = repo_root / "docs" / "archive" / "deployments"
    new_file = archive_dir / "DEPLOYMENT_MAGERSTAV_2025-11-29.md"
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    print("🔄 Archiving Mágerstav Deployment Summary...")
    print()

    # 1. Create archive/deployments directory
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True)
        print(f"✅ Created: {archive_dir.relative_to(repo_root)}")
    else:
        print(f"✓ Exists: {archive_dir.relative_to(repo_root)}")

    # 2. Move and rename file
    if old_file.exists():
        shutil.move(str(old_file), str(new_file))
        print(f"✅ Moved: {old_file.name}")
        print(f"   → {new_file.relative_to(repo_root)}")
    else:
        print(f"❌ Not found: {old_file}")
        return

    print()

    # 3. Update archive index
    if archive_index.exists():
        with open(archive_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the section to insert new entry
        deployment_section = "## Deployment Records"

        if deployment_section in content:
            # Section exists, add to it
            lines = content.split('\n')
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip() == deployment_section:
                    # Find next empty line after section
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() == '':
                            insert_idx = j
                            break
                    break

            if insert_idx:
                new_entry = f"- **2025-11-29** - [Mágerstav Production Deployment](deployments/DEPLOYMENT_MAGERSTAV_2025-11-29.md) - First production deployment, v2.0.0"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)
        else:
            # Add new section
            new_section = f"""
{deployment_section}

- **2025-11-29** - [Mágerstav Production Deployment](deployments/DEPLOYMENT_MAGERSTAV_2025-11-29.md) - First production deployment, v2.0.0

---
"""
            # Insert before final separator if exists
            if content.endswith('---\n'):
                content = content[:-5] + new_section
            else:
                content += '\n' + new_section

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added deployment record entry")
    else:
        print(f"⚠️ Archive index not found: {archive_index}")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Created: docs/archive/deployments/")
    print(f"  • Archived: DEPLOYMENT_MAGERSTAV_2025-11-29.md")
    print(f"  • Updated: Archive index")
    print()


if __name__ == "__main__":
    archive_magerstav_deployment()