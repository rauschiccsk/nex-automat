#!/usr/bin/env python3
"""
Script 09: Update RAG Config
Session: RAG Implementation Phase 2

Updates config/rag_config.yaml with complete configuration
Location: scripts/09_update_rag_config.py
"""

from pathlib import Path
import yaml

COMPLETE_CONFIG = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'database': 'nex_automat_rag',
        'user': 'postgres',
        'password': 'your_password_here',  # User will update this
        'pool_min_size': 2,
        'pool_max_size': 10
    },
    'embedding': {
        'model_name': 'sentence-transformers/all-MiniLM-L6-v2',
        'dimension': 384,
        'batch_size': 32,
        'max_seq_length': 512,
        'device': None,
        'cache_dir': None
    },
    'vector_index': {
        'index_type': 'hnsw',
        'm': 16,
        'ef_construction': 64,
        'ef_search': 40
    },
    'chunking': {
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'min_chunk_size': 100
    },
    'search': {
        'default_limit': 10,
        'similarity_threshold': 0.7,
        'hybrid_alpha': 0.5
    }
}


def main():
    print("=" * 60)
    print("  Script 09: Update RAG Config")
    print("=" * 60)
    print()

    config_path = Path("C:/Development/nex-automat/config/rag_config.yaml")

    print(f"Config file: {config_path}")
    print()

    # Backup existing config if it exists
    if config_path.exists():
        backup_path = config_path.with_suffix('.yaml.backup')
        print(f"Creating backup: {backup_path}")
        config_path.rename(backup_path)
        print("✓ Backup created")
        print()

    # Write complete config
    print("Writing updated config...")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(COMPLETE_CONFIG, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Config written: {config_path}")
    print()

    # Instructions
    print("=" * 60)
    print("  IMPORTANT: Update PostgreSQL Password")
    print("=" * 60)
    print()
    print("Edit config/rag_config.yaml and update:")
    print("  database.password: 'your_password_here'")
    print()
    print("Then test config loading:")
    print("  python -m tools.rag.config")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())