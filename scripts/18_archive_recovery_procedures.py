"""
Script 18: Archive Recovery Procedures
Archives Mágerstav-specific recovery procedures (duplicates RECOVERY_GUIDE)
"""

import os
import shutil
from pathlib import Path


def archive_recovery_procedures():
    """Archive RECOVERY_PROCEDURES.md-old to archive/deployments/"""

    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "RECOVERY_PROCEDURES.md-old"
    archive_dir = repo_root / "docs" / "archive" / "deployments"
    archive_file = archive_dir / "RECOVERY_PROCEDURES_MAGERSTAV_2025-11-24.md"
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    print("🔄 Archiving Recovery Procedures...")
    print()

    # 1. Archive file
    if old_file.exists():
        shutil.move(str(old_file), str(archive_file))
        print(f"✅ Archived: {old_file.name}")
        print(f"   → {archive_file.relative_to(repo_root)}")
        print(f"   (Duplicates RECOVERY_GUIDE.md content)")
    else:
        print(f"❌ Not found: {old_file}")
        return

    print()

    # 2. Update archive index
    if archive_index.exists():
        with open(archive_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find Deployment Records section and add entry
        if "## Deployment Records" in content:
            lines = content.split('\n')
            # Find recovery guide entry and add after it
            insert_idx = None
            for i, line in enumerate(lines):
                if "Recovery Guide" in line and "2025-11-21" in line:
                    insert_idx = i + 1
                    break

            if insert_idx:
                new_entry = "- **2025-11-24** - [Mágerstav Recovery Procedures](deployments/RECOVERY_PROCEDURES_MAGERSTAV_2025-11-24.md) - Quick reference recovery guide (Slovak)"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added recovery procedures entry")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Archived: RECOVERY_PROCEDURES_MAGERSTAV_2025-11-24.md")
    print(f"  • Note: Content duplicates RECOVERY_GUIDE.md")
    print(f"  • Updated: Archive index")
    print()


if __name__ == "__main__":
    archive_recovery_procedures()