"""
Script 14: Migrate Service Management Guide
Removes .md-old extension, creates docs/deployment/SERVICE_MANAGEMENT.md
"""

import os
import shutil
from pathlib import Path


def migrate_service_management():
    """Migrate SERVICE_MANAGEMENT.md-old to .md"""

    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "SERVICE_MANAGEMENT.md-old"
    new_file = repo_root / "docs" / "deployment" / "SERVICE_MANAGEMENT.md"
    doc_index = repo_root / "docs" / "00_DOCUMENTATION_INDEX.md"

    print("🔄 Migrating Service Management Guide...")
    print()

    # 1. Rename file (remove .md-old)
    if old_file.exists():
        shutil.move(str(old_file), str(new_file))
        print(f"✅ Migrated: {old_file.name}")
        print(f"   → {new_file.relative_to(repo_root)}")
    else:
        print(f"❌ Not found: {old_file}")
        return

    print()

    # 2. Update documentation index
    if doc_index.exists():
        with open(doc_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find Deployment section and add entry
        deployment_section = "## 📦 Deployment"

        if deployment_section in content:
            lines = content.split('\n')
            insert_idx = None

            # Find section and look for appropriate place to insert
            for i, line in enumerate(lines):
                if line.strip() == deployment_section:
                    # Find next section or empty line after this section
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith('- '):
                            insert_idx = j
                            break
                        elif lines[j].strip() == '':
                            insert_idx = j
                            break
                    break

            if insert_idx:
                new_entry = "- [Service Management](deployment/SERVICE_MANAGEMENT.md) - Windows service operations guide"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(doc_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {doc_index.relative_to(repo_root)}")
        print("   Added SERVICE_MANAGEMENT.md to deployment section")
    else:
        print(f"⚠️ Documentation index not found")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Created: docs/deployment/SERVICE_MANAGEMENT.md")
    print(f"  • Updated: Documentation index")
    print()


if __name__ == "__main__":
    migrate_service_management()