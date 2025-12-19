"""
Create tenant-specific knowledge base structure.

Structure:
  docs/knowledge/
    shared/           # Available to all tenants (existing docs)
    tenants/
      icc/            # ICC-specific knowledge
      andros/         # ANDROS-specific knowledge
"""
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Development\nex-automat")
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "knowledge"

# Tenant directories to create
TENANTS = ["icc", "andros"]

# README content for tenant directories
TENANT_README = '''# {tenant} Knowledge Base

Tenant-specific documents for **{tenant}**.

## Structure

```
{tenant}/
├── processes/     # Business processes
├── hr/            # HR documentation  
├── technical/     # Technical guides
└── README.md
```

## Indexing

Documents in this directory are automatically tagged with `tenant: {tenant}` 
when indexed to RAG. They will only appear in searches for this tenant.

## Adding Documents

1. Place `.md` files in appropriate subdirectory
2. Run: `python tools/rag/rag_update.py --tenant {tenant}`

'''

SHARED_README = '''# Shared Knowledge Base

Documents available to **all tenants**.

## Current Content

- `strategic/` - Product strategy documents (NEX Brain, etc.)
- `processes/` - Common business processes
- `reference/` - Reference documentation

## Indexing

Documents here have no tenant tag and appear in all tenant searches.

'''


def main():
    print("=" * 60)
    print("Create Tenant Knowledge Structure")
    print("=" * 60)

    # Create shared directory (rename existing if needed)
    shared_dir = KNOWLEDGE_DIR / "shared"
    if not shared_dir.exists():
        shared_dir.mkdir(parents=True)
        print(f"\n✅ Created: {shared_dir}")

    # Create shared README
    shared_readme = shared_dir / "README.md"
    if not shared_readme.exists():
        shared_readme.write_text(SHARED_README, encoding="utf-8")
        print(f"✅ Created: {shared_readme}")

    # Create tenants directory
    tenants_dir = KNOWLEDGE_DIR / "tenants"
    tenants_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n✅ Created: {tenants_dir}")

    # Create tenant subdirectories
    for tenant in TENANTS:
        tenant_dir = tenants_dir / tenant
        tenant_dir.mkdir(exist_ok=True)

        # Subdirectories
        (tenant_dir / "processes").mkdir(exist_ok=True)
        (tenant_dir / "hr").mkdir(exist_ok=True)
        (tenant_dir / "technical").mkdir(exist_ok=True)

        # README
        readme = tenant_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                TENANT_README.format(tenant=tenant.upper()),
                encoding="utf-8"
            )

        print(f"✅ Created: {tenant_dir}/")

    # Show final structure
    print("\n" + "=" * 60)
    print("Knowledge Base Structure:")
    print("=" * 60)
    print(f"""
docs/knowledge/
├── shared/              # All tenants (existing strategic/, etc.)
│   └── README.md
└── tenants/
    ├── icc/
    │   ├── processes/
    │   ├── hr/
    │   ├── technical/
    │   └── README.md
    └── andros/
        ├── processes/
        ├── hr/
        ├── technical/
        └── README.md
""")

    print("Next steps:")
    print("1. Move existing shared docs to docs/knowledge/shared/")
    print("2. Add tenant-specific docs to docs/knowledge/tenants/{tenant}/")
    print("3. Run indexer with tenant detection")


if __name__ == "__main__":
    main()