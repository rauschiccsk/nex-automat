# NEX Automat

**Multi-customer SaaS platform for automated invoice processing**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-61%20passing-success.svg)](./apps/supplier-invoice-loader/tests/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Overview

NEX Automat je monorepo projekt obsahujúci aplikácie a zdieľané knižnice pre automatizáciu spracovania dodávateľských faktúr. Projekt je integrovaný s NEX Genesis ERP systémom cez Btrieve databázy.

### Key Features

- ⚡ **Automatické spracovanie faktúr** - extrahovanie dát z PDF
- 📊 **Multi-customer architecture** - podpora viacerých zákazníkov
- 🔄 **PostgreSQL staging** - príprava dát pre invoice-editor
- 📧 **Email notifikácie** - automatické upozornenia
- 🌐 **FastAPI REST API** - moderné API s dokumentáciou
- 🧪 **Comprehensive testing** - 85% test coverage

---

## 🗂️ Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/    # FastAPI service for invoice processing
│   └── supplier-invoice-editor/    # Web UI for invoice editing
│
├── packages/
│   ├── invoice-shared/             # Shared invoice utilities
│   └── nex-shared/                 # NEX Genesis ERP utilities
│
├── docs/                           # Documentation & manifests
└── tools/                          # Development tools
```

### Applications

#### 🔹 Supplier Invoice Loader
FastAPI service pre automatické spracovanie dodávateľských faktúr.

**Features:**
- PDF parsing a OCR
- ISDOC XML generovanie
- Duplikát detekcia
- PostgreSQL staging
- Email notifikácie

**Tech Stack:**
- FastAPI, Uvicorn
- PyPDF, Pillow
- asyncpg, aiosqlite
- Pydantic v2

#### 🔹 Supplier Invoice Editor
Web aplikácia pre manuálnu editáciu a kontrolu faktúr.

**Status:** In development

### Packages

#### 📦 invoice-shared
Zdieľané utility pre prácu s faktúrami.

**Modules:**
- `database/` - PostgreSQL staging client
- `utils/` - Text processing utilities
- `models/` - Data models
- `schemas/` - Pydantic schemas

#### 📦 nex-shared
Utility pre prácu s NEX Genesis ERP (Btrieve).

**Status:** Placeholder

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13.7 32-bit** (Btrieve compatibility)
- **Git**
- **PostgreSQL** (optional, for staging)

### Installation

```powershell
# 1. Clone repository
git clone https://github.com/[username]/nex-automat.git
cd nex-automat

# 2. Create virtual environment
& "C:\Program Files (x86)\Python313-32\python.exe" -m venv venv32

# 3. Activate
.\venv32\Scripts\Activate.ps1

# 4. Install dependencies (in correct order!)
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor
pip install pytest pytest-asyncio pytest-cov black ruff
```

### Verify Installation

```bash
# Run tests
pytest --tb=no -q

# Expected: 61+ passed, 0 failed
```

---

## 💻 Development

### Running Supplier Invoice Loader

```bash
# Activate venv
.\venv32\Scripts\Activate.ps1

# Run server
cd apps/supplier-invoice-loader
python main.py

# API documentation
# http://localhost:8000/docs
```

### Configuration

Create `config/customer_config.py`:

```python
CUSTOMER_NAME = "MAGERSTAV"
API_KEY = "your-api-key"
PDF_DIR = Path("C:/Development/storage/MAGERSTAV/pdf")
XML_DIR = Path("C:/Development/storage/MAGERSTAV/xml")

# PostgreSQL staging (optional)
POSTGRES_STAGING_ENABLED = True
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "invoice_staging"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
```

### API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Service info |
| `/health` | GET | No | Health check |
| `/metrics` | GET | No | Metrics (JSON) |
| `/status` | GET | Yes | Detailed status |
| `/invoice` | POST | Yes | Process invoice |
| `/invoices` | GET | Yes | List invoices |

**Authentication:** API Key in `X-API-Key` header

### Example Request

```bash
curl -X POST http://localhost:8000/invoice \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "file_b64": "JVBERi0xLjQK...",
    "filename": "invoice.pdf",
    "subject": "Invoice #123",
    "from_email": "supplier@example.com",
    "message_id": "msg-123",
    "gmail_id": "gmail-123",
    "received_date": "2025-01-15T10:00:00"
  }'
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# Specific app
pytest apps/supplier-invoice-loader/tests/ -v

# With coverage
pytest --cov=src --cov-report=html

# Quick summary
pytest --tb=no -q
```

### Test Results

**supplier-invoice-loader:**
- ✅ 61/72 tests passing (85% coverage)
- ⏭️ 11 tests skipped
- ❌ 0 tests failing

---

## 📚 Documentation

- **[MONOREPO_GUIDE.md](docs/giudes/MONOREPO_GUIDE.md)** - Development guide
- **[CONTRIBUTING.md](docs/giudes/CONTRIBUTING.md)** - Contribution guidelines
- **[SESSION_NOTES.md](docs/SESSION_NOTES.md)** - Current status & history

### Manifests

Hierarchické JSON manifesty pre efektívne načítavanie projektu:

- `docs/PROJECT_MANIFEST.json` - Root overview
- `docs/apps/*.json` - Per-app details
- `docs/packages/*.json` - Per-package details

Generate manifests:
```bash
python generate_projects_access.py
```

---

## 🛠️ Tools & Scripts

### Manifest Generators

```bash
# TXT format (human-readable)
python generate_project_manifest.py

# JSON format (hierarchical)
python generate_projects_access.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check . --fix

# Type check (optional)
mypy apps/supplier-invoice-loader/
```

---

## 🏗️ Architecture

### Data Flow

```
Email → n8n → FastAPI → PDF Extraction → SQLite
                 ↓
            PostgreSQL Staging → Invoice Editor
                 ↓
            ISDOC XML → NEX Genesis ERP
```

### Technology Stack

**Backend:**
- Python 3.13.7 32-bit
- FastAPI, Uvicorn
- SQLite, PostgreSQL
- asyncpg, aiosqlite

**Processing:**
- PyPDF (PDF parsing)
- Pillow (image processing)
- Custom extractors

**Data Formats:**
- ISDOC XML (Czech invoicing standard)
- JSON (API communication)
- PDF (input documents)

**Infrastructure:**
- Windows Server 2012 R2
- NEX Genesis ERP (Btrieve)
- PostgreSQL 14+

---

## 🔧 Configuration

### Environment Variables

```bash
# Customer identification
CUSTOMER_NAME=MAGERSTAV

# API security
API_KEY=your-secret-key

# Storage paths
PDF_STORAGE_DIR=C:/Development/storage/MAGERSTAV/pdf
XML_STORAGE_DIR=C:/Development/storage/MAGERSTAV/xml

# Database
DB_FILE=C:/Development/storage/MAGERSTAV/invoices.db

# PostgreSQL staging (optional)
POSTGRES_STAGING_ENABLED=true
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=invoice_staging

# Email notifications (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=admin@example.com
```

---

## 📊 Monitoring

### Metrics Endpoints

**JSON format:**
```bash
curl http://localhost:8000/metrics
```

**Prometheus format:**
```bash
curl http://localhost:8000/metrics/prometheus
```

### Available Metrics

- `app_uptime_seconds` - Application uptime
- `app_invoices_processed_total` - Total processed invoices
- `app_invoices_errors_total` - Total errors
- System metrics (CPU, memory, disk)

---

## 🚨 Troubleshooting

### Common Issues

**Problem:** "Invalid Python Interpreter" in PyCharm  
**Solution:** Settings → Python Interpreter → Select `venv32/Scripts/python.exe`

**Problem:** "No matching distribution found for invoice-shared"  
**Solution:** Install packages in correct order (shared first, then apps)

**Problem:** Tests failing after git pull  
**Solution:** 
```bash
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader
pytest
```

See [MONOREPO_GUIDE.md](docs/giudes/MONOREPO_GUIDE.md) for more troubleshooting.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/giudes/CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes & add tests
4. Format code (`black .` & `ruff check . --fix`)
5. Commit (`git commit -m 'feat: add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Create Pull Request

---

## 📝 License

This project is proprietary software.

**Copyright © 2025 ICC Komárno - Innovation & Consulting Center**

---

## 👥 Team

**Maintainer:** Zoltán Rausch (rausch@icc.sk)  
**Organization:** ICC Komárno - Innovation & Consulting Center  
**Experience:** 40 years in software development

---

## 🔗 Related Projects

- **[nex-genesis-server](https://github.com/[org]/nex-genesis-server)** - NEX Genesis ERP integration
- **[uae-legal-agent](https://github.com/[org]/uae-legal-agent)** - Legal document analysis
- **[claude-dev-automation](https://github.com/[org]/claude-dev-automation)** - AI-driven development workflows

---

## 📈 Project Status

**Version:** 2.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2025-11-19

**Migration Status:**
- ✅ Monorepo structure
- ✅ Shared packages
- ✅ Testing infrastructure (61/72 passing)
- ✅ Documentation complete
- ✅ Python environment setup
- 📋 CI/CD pipeline (todo)

---

## 📮 Contact

- **Email:** rausch@icc.sk
- **Organization:** ICC Komárno
- **Location:** Komárno, Slovakia

---

**Made with ❤️ by ICC Komárno**