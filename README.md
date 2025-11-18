# NEX Automat

**NEX Genesis Automation Platform - Monorepo**

## 📦 Struktura

```
nex-automat/
├── apps/                                # Spustiteľné aplikácie
│   ├── supplier-invoice-loader/         # Email → NEX invoice automation
│   └── supplier-invoice-editor/         # GUI approval workflow
│
├── packages/                            # Zdieľané knižnice
│   ├── invoice-shared/                  # Spoločné pre invoice projekty
│   └── nex-shared/                      # Spoločné pre všetky NEX projekty
│
├── docs/                                # Centrálna dokumentácia
│   ├── SESSION_NOTES.md                 # Aktuálny stav projektu
│   └── INIT_PROMPT_NEW_CHAT.md          # Init prompt pre nový chat
│
├── tools/                               # Build & dev tools
└── pyproject.toml                       # Workspace config
```

## 🚀 Quick Start

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/rauschiccsk/nex-automat.git
cd nex-automat

# Install all dependencies
uv sync

# Run specific app
cd apps/supplier-invoice-loader
uv run python -m src.main
```

## 🔧 Technology Stack

- **Python:** 3.11+
- **Package Manager:** UV (ultrafast, Rust-based)
- **Workspace:** UV native workspace support
- **Apps:** FastAPI, PostgreSQL, n8n integration

## 📚 Documentation

- [Session Notes](docs/SESSION_NOTES.md) - Aktuálny stav projektu
- [Init Prompt](docs/INIT_PROMPT_NEW_CHAT.md) - Pre nový chat
- [Architecture](docs/architecture/)
- [Development Guide](docs/development/)
- [Deployment](docs/deployment/)

## 🏢 Organization

**ICC Komárno** - Innovation & Consulting Center  
**Developer:** Zoltán Rausch (rausch@icc.sk)  
**GitHub:** @rauschiccsk

## 📄 License

Proprietary - ICC Komárno
