"""
Pytest configuration and shared fixtures
"""

import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (may send real emails, etc.)",
    )


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory"""
    return Path(__file__).parent / "samples"


@pytest.fixture(scope="session")
def sample_invoice_data():
    """Sample invoice data for testing"""
    from decimal import Decimal

    from src.extractors.ls_extractor import InvoiceData, InvoiceItem

    invoice = InvoiceData(
        invoice_number="2025001",
        issue_date="2025-10-06",
        due_date="2025-10-20",
        total_amount=Decimal("1234.56"),
        tax_amount=Decimal("234.56"),
        net_amount=Decimal("1000.00"),
        currency="EUR",
        supplier_name="L & Š, s.r.o.",
        customer_name="Test Customer",
        customer_ico="12345678",
        iban="SK1234567890123456789012",
        variable_symbol="2025001",
    )

    # Add sample items
    invoice.items = [
        InvoiceItem(
            line_number=1,
            description="Test Product 1",
            quantity=Decimal("5"),
            unit="KS",
            unit_price_with_vat=Decimal("10.00"),
            total_with_vat=Decimal("50.00"),
            vat_rate=Decimal("20"),
        ),
        InvoiceItem(
            line_number=2,
            description="Test Product 2",
            quantity=Decimal("10"),
            unit="KS",
            unit_price_with_vat=Decimal("20.00"),
            total_with_vat=Decimal("200.00"),
            vat_rate=Decimal("20"),
        ),
    ]

    return invoice


@pytest.fixture
def mock_config(monkeypatch):
    """Mock configuration for testing"""
    from src.utils import config

    # Mock sensitive values for testing
    monkeypatch.setattr(config, "API_KEY", "test-api-key-12345")
    monkeypatch.setattr(config, "CUSTOMER_NAME", "TESTCUSTOMER")
    monkeypatch.setattr(config, "ALERT_EMAIL", "test@example.com")
    monkeypatch.setattr(config, "SMTP_USER", "test@example.com")
    monkeypatch.setattr(config, "SMTP_PASSWORD", "test-password")

    return config


@pytest.fixture
def temp_database(tmp_path):
    """Create temporary database for testing"""
    import sqlite3

    db_path = tmp_path / "test_invoices.db"

    # Create database with schema
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_hash TEXT UNIQUE NOT NULL,
            pdf_path TEXT NOT NULL,
            xml_path TEXT,
            original_filename TEXT NOT NULL,
            message_id TEXT,
            gmail_id TEXT,
            sender TEXT,
            subject TEXT,
            received_date TEXT,
            invoice_number TEXT,
            issue_date TEXT,
            due_date TEXT,
            total_amount REAL,
            tax_amount REAL,
            net_amount REAL,
            variable_symbol TEXT,
            status TEXT DEFAULT 'pending',
            created_at INTEGER NOT NULL,
            processed_at INTEGER
        )
    """)

    conn.commit()
    conn.close()

    return db_path


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content (minimal valid PDF)"""
    # This is a minimal valid PDF
    return b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000274 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
366
%%EOF"""


@pytest.fixture
def mock_smtp_server(monkeypatch):
    """Mock SMTP server for email testing"""
    import smtplib
    from unittest.mock import MagicMock, Mock

    mock_server = MagicMock()
    mock_smtp = Mock(return_value=mock_server)

    monkeypatch.setattr(smtplib, "SMTP", mock_smtp)

    return mock_server


@pytest.fixture(autouse=True)
def reset_metrics():
    """Reset metrics before each test"""
    from src.utils import monitoring

    # Reset metrics before test
    monitoring.reset_metrics()

    yield

    # Reset again after test (cleanup)
    monitoring.reset_metrics()


@pytest.fixture
def api_client():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    from main import app

    return TestClient(app)


# Hooks for test reporting
def pytest_report_header(config):
    """Add custom header to pytest output"""
    return [
        "Supplier Invoice Loader - Test Suite",
        f"Python: {sys.version.split()[0]}",
        f"Pytest: {pytest.__version__}",
    ]


# ============================================================================
# BTRIEVE API TEST FIXTURES
# ============================================================================


@dataclass
class MockGSCATRecord:
    """Mock GSCAT (Product) record."""

    GsCode: int
    GsName: str
    BarCode: str = ""
    SupplierCode: str = ""
    MgCode: str = "KS"


@dataclass
class MockPABRecord:
    """Mock PAB (Partner) record."""

    pab_code: int
    name1: str
    name2: str = ""
    short_name: str = ""
    street: str = ""
    city: str = ""
    zip_code: str = ""
    country: str = "SK"
    phone: str = ""
    fax: str = ""
    email: str = ""
    web: str = ""
    contact_person: str = ""
    ico: str = ""
    dic: str = ""
    ic_dph: str = ""
    bank_account: str = ""
    bank_code: str = ""
    bank_name: str = ""
    iban: str = ""
    swift: str = ""
    partner_type: int = 3
    payment_terms: int = 14
    credit_limit: float = 0.0
    discount_percent: float = 0.0
    active: bool = True
    vat_payer: bool = True
    note: str = ""
    mod_user: str = ""
    mod_date: datetime | None = None


@dataclass
class MockBARCODERecord:
    """Mock BARCODE record."""

    gs_code: int
    bar_code: str
    mod_user: str = ""
    mod_date: date | None = None
    mod_time: str = ""


@dataclass
class MockMGLSTRecord:
    """Mock MGLST (Product Group) record."""

    mglst_code: int
    name: str  # Also accessible as mglst_name
    parent_code: int = 0
    level: int = 1
    sort_order: int = 0
    active: bool = True
    short_name: str = ""
    show_in_catalog: bool = True
    color_code: str = ""
    default_vat_rate: float = 20.0
    default_unit: str = "ks"
    note: str = ""
    description: str = ""
    mod_user: str = ""
    mod_date: datetime | None = None

    @property
    def mglst_name(self) -> str:
        """Alias for name field."""
        return self.name


@dataclass
class MockTSHRecord:
    """Mock TSH (Document Header) record."""

    doc_number: str
    doc_type: int
    doc_date: date | None
    pab_code: int
    total_amount: float = 0.0
    tax_amount: float = 0.0
    net_amount: float = 0.0
    currency: str = "EUR"
    mod_user: str = ""
    mod_date: datetime | None = None


@dataclass
class MockTSIRecord:
    """Mock TSI (Document Item) record."""

    doc_number: str
    line_number: int
    gs_code: int
    gs_name: str = ""
    quantity: float = 1.0
    unit: str = "KS"
    unit_price: float = 0.0
    total_price: float = 0.0
    vat_rate: float = 20.0


@pytest.fixture
def sample_products():
    """Sample product records for testing."""
    return [
        MockGSCATRecord(
            GsCode=1001,
            GsName="Chlieb biely 500g",
            BarCode="8590001000010",
            SupplierCode="LS001",
        ),
        MockGSCATRecord(
            GsCode=1002,
            GsName="Mlieko plnotučné 1L",
            BarCode="8590001000027",
            SupplierCode="LS002",
        ),
        MockGSCATRecord(
            GsCode=1003,
            GsName="Maslo 250g",
            BarCode="8590001000034",
            SupplierCode="LS003",
        ),
    ]


@pytest.fixture
def sample_partners():
    """Sample partner records for testing."""
    return [
        MockPABRecord(
            pab_code=101,
            name1="L & Š, s.r.o.",
            ico="12345678",
            city="Bratislava",
            partner_type=1,
        ),
        MockPABRecord(
            pab_code=102,
            name1="Test Customer",
            ico="87654321",
            city="Košice",
            partner_type=2,
        ),
        MockPABRecord(
            pab_code=103,
            name1="Univerzálny Partner",
            ico="11223344",
            city="Žilina",
            partner_type=3,
        ),
    ]


@pytest.fixture
def sample_barcodes():
    """Sample barcode records for testing."""
    return [
        MockBARCODERecord(gs_code=1001, bar_code="8590001000099"),
        MockBARCODERecord(gs_code=1002, bar_code="8590001000105"),
    ]


@pytest.fixture
def sample_product_groups():
    """Sample product group records for testing."""
    return [
        MockMGLSTRecord(
            mglst_code=1, name="Potraviny", parent_code=0, level=1, sort_order=1
        ),
        MockMGLSTRecord(
            mglst_code=2, name="Pečivo", parent_code=1, level=2, sort_order=1
        ),
        MockMGLSTRecord(
            mglst_code=3, name="Mliečne výrobky", parent_code=1, level=2, sort_order=2
        ),
    ]


@pytest.fixture
def sample_documents():
    """Sample document header records for testing."""
    return [
        MockTSHRecord(
            doc_number="2025001",
            doc_type=1,
            doc_date=date(2025, 1, 15),
            pab_code=101,
            total_amount=1234.56,
        ),
        MockTSHRecord(
            doc_number="2025002",
            doc_type=2,
            doc_date=date(2025, 1, 16),
            pab_code=102,
            total_amount=999.99,
        ),
    ]


@pytest.fixture
def sample_document_items():
    """Sample document item records for testing."""
    return [
        MockTSIRecord(
            doc_number="2025001",
            line_number=1,
            gs_code=1001,
            gs_name="Chlieb",
            quantity=10,
            unit_price=1.50,
        ),
        MockTSIRecord(
            doc_number="2025001",
            line_number=2,
            gs_code=1002,
            gs_name="Mlieko",
            quantity=5,
            unit_price=1.20,
        ),
    ]


@pytest.fixture
def mock_gscat_repository(sample_products):
    """Mock GSCATRepository."""
    repo = MagicMock()
    repo.get_all.return_value = sample_products
    repo.find_one.side_effect = lambda predicate: next(
        (p for p in sample_products if predicate(p)), None
    )
    repo.find_by_barcode.side_effect = lambda bc: next(
        (p for p in sample_products if p.BarCode == bc), None
    )
    repo.search_by_name.side_effect = lambda q, limit=100: [
        p for p in sample_products if q.lower() in p.GsName.lower()
    ]
    repo.close.return_value = None
    return repo


@pytest.fixture
def mock_pab_repository(sample_partners):
    """Mock PABRepository."""
    repo = MagicMock()
    repo.get_all.return_value = sample_partners
    repo.find_one.side_effect = lambda predicate: next(
        (p for p in sample_partners if predicate(p)), None
    )
    repo.close.return_value = None
    return repo


@pytest.fixture
def mock_barcode_repository(sample_barcodes):
    """Mock BARCODERepository."""
    repo = MagicMock()
    repo.find_by_barcode.side_effect = lambda bc: next(
        (b for b in sample_barcodes if b.bar_code == bc), None
    )
    repo.find.side_effect = lambda predicate, max_results=100: [
        b for b in sample_barcodes if predicate(b)
    ]
    repo.close.return_value = None
    return repo


@pytest.fixture
def mock_mglst_repository(sample_product_groups):
    """Mock MGLSTRepository."""
    repo = MagicMock()
    repo.get_all.return_value = sample_product_groups
    repo.find_one.side_effect = lambda predicate: next(
        (g for g in sample_product_groups if predicate(g)), None
    )
    repo.find.side_effect = lambda predicate, max_results=1000: [
        g for g in sample_product_groups if predicate(g)
    ]
    repo.close.return_value = None
    return repo


@pytest.fixture
def mock_tsh_repository(sample_documents):
    """Mock TSHRepository."""
    repo = MagicMock()
    repo.get_all.return_value = sample_documents
    repo.find_one.side_effect = lambda predicate: next(
        (d for d in sample_documents if predicate(d)), None
    )
    repo.close.return_value = None
    return repo


@pytest.fixture
def mock_tsi_repository(sample_document_items):
    """Mock TSIRepository."""
    repo = MagicMock()
    repo.find.side_effect = lambda predicate, max_results=1000: [
        i for i in sample_document_items if predicate(i)
    ]
    repo.close.return_value = None
    return repo


@pytest.fixture
def api_v1_client():
    """FastAPI test client for new API v1 routes."""
    from fastapi.testclient import TestClient
    from src.main import app

    return TestClient(app)


@pytest.fixture
def api_key_header():
    """API key header for authenticated requests."""
    return {"X-API-Key": "test-api-key"}


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for API tests."""
    from src.core import config

    monkeypatch.setattr(
        config,
        "settings",
        config.Settings(
            api_key="test-api-key",
            btrieve_path=Path("/tmp/btrieve"),
        ),
    )
    # Clear the cache to use new settings
    config.get_settings.cache_clear()
    return config.settings
