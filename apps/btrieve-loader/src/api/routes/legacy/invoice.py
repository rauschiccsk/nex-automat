"""
Legacy Invoice Processing Routes.

Extracted from original main.py for backward compatibility.
All endpoints maintain the same behavior and paths.
"""

import base64
import hashlib
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from nex_staging import StagingClient

from src.api import models
from src.business.isdoc_service import generate_isdoc_xml
from src.business.product_matcher import ProductMatcher
from src.database import database
from src.extractors.ls_extractor import extract_invoice_data
from src.extractors.marso_extractor import (
    detect_marso_invoice_from_pdf,
    extract_marso_as_standard,
)
from src.utils import config, monitoring, notifications

router = APIRouter()

# Start time for uptime calculation
START_TIME = time.time()

# Global ProductMatcher instance (initialized on startup)
product_matcher: ProductMatcher | None = None


# ============================================================================
# AUTHENTICATION
# ============================================================================


async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    """Verify API key from X-API-Key header."""
    if not x_api_key:
        raise HTTPException(status_code=422, detail="Missing X-API-Key header")

    if x_api_key != config.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return x_api_key


ApiKey = Annotated[str, Depends(verify_api_key)]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def init_product_matcher() -> ProductMatcher | None:
    """Initialize ProductMatcher if NEX Genesis is enabled."""
    global product_matcher
    if config.NEX_GENESIS_ENABLED:
        try:
            product_matcher = ProductMatcher(config.NEX_DATA_PATH)
            print(f"[OK] ProductMatcher initialized: {config.NEX_DATA_PATH}")
            return product_matcher
        except Exception as e:
            print(f"[ERROR] Failed to initialize ProductMatcher: {e}")
            return None
    else:
        print("[WARNING] NEX Genesis enrichment disabled")
        return None


def move_files_to_staging(
    pdf_path: Path,
    xml_path: Path,
    file_basename: str,
    pg_conn,
    invoice_id: int,
) -> tuple:
    """
    Move PDF and XML files from RECEIVED to STAGING directory.
    Update file_status in PostgreSQL.
    """
    try:
        staged_pdf_path = config.STAGING_DIR / f"{file_basename}.pdf"
        staged_xml_path = config.STAGING_DIR / f"{file_basename}.xml"

        if pdf_path.exists():
            shutil.move(str(pdf_path), str(staged_pdf_path))
            print(f"[OK] PDF moved to staging: {staged_pdf_path}")
        else:
            print(f"[WARN] PDF not found for moving: {pdf_path}")
            staged_pdf_path = None

        if xml_path.exists():
            shutil.move(str(xml_path), str(staged_xml_path))
            print(f"[OK] XML moved to staging: {staged_xml_path}")
        else:
            print(f"[WARN] XML not found for moving: {xml_path}")
            staged_xml_path = None

        pg_conn.run(
            """
            UPDATE supplier_invoice_heads
            SET file_status = 'staged',
                pdf_file_path = :pdf_path,
                xml_file_path = :xml_path,
                updated_at = NOW()
            WHERE id = :inv_id
            """,
            pdf_path=str(staged_pdf_path) if staged_pdf_path else None,
            xml_path=str(staged_xml_path) if staged_xml_path else None,
            inv_id=invoice_id,
        )
        print(f"[OK] Updated file_status to 'staged' for invoice {invoice_id}")

        return (staged_pdf_path, staged_xml_path)

    except Exception as e:
        print(f"[FAIL] Failed to move files to staging: {e}")
        return (None, None)


# ============================================================================
# PUBLIC ENDPOINTS (no auth required)
# ============================================================================


@router.get("/")
async def root():
    """Root endpoint - service information."""
    return {
        "service": "Supplier Invoice Loader",
        "version": "2.0.0",
        "status": "running",
    }


@router.get("/health")
async def health():
    """Health check endpoint - for monitoring systems."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@router.get("/metrics")
async def metrics():
    """Metrics endpoint - basic metrics in JSON format."""
    uptime = int(time.time() - START_TIME)

    try:
        stats = database.get_stats()
        total_processed = stats.get("total", 0)
    except Exception:
        total_processed = 0

    return {
        "uptime_seconds": uptime,
        "app_invoices_processed_total": total_processed,
        "app_info": {"version": "2.0.0", "customer": config.CUSTOMER_NAME},
    }


@router.get("/stats")
async def stats():
    """Statistics endpoint - database statistics."""
    try:
        database.init_database()
        stats = database.get_stats()
        if "total" in stats and "total_invoices" not in stats:
            stats["total_invoices"] = stats["total"]
        return stats
    except Exception as e:
        return {
            "total_invoices": 0,
            "total": 0,
            "by_status": {},
            "by_nex_status": {},
            "by_customer": {},
            "duplicates": 0,
            "error": str(e),
        }


# ============================================================================
# PROTECTED ENDPOINTS (require authentication)
# ============================================================================


@router.get("/status")
async def status(_api_key: ApiKey):
    """Detailed status endpoint - requires authentication."""
    try:
        db_stats = database.get_stats()
        db_healthy = True
    except Exception as e:
        db_stats = {"error": str(e)}
        db_healthy = False

    storage_health = monitoring.check_storage_health()
    storage_ok = storage_health.get("storage_healthy", False)

    return {
        "status": "healthy" if db_healthy and storage_ok else "degraded",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": "healthy" if db_healthy else "error",
            "storage": "healthy" if storage_ok else "warning",
            "smtp": "unknown",
        },
        "statistics": db_stats,
        "uptime_seconds": int(time.time() - START_TIME),
    }


@router.get("/invoices")
async def list_invoices(
    _api_key: ApiKey,
    limit: int = 100,
):
    """List invoices - requires authentication."""
    try:
        database.init_database()
        invoices = database.get_all_invoices(limit=limit)
        return {"count": len(invoices), "invoices": invoices}
    except Exception as e:
        return {"count": 0, "invoices": [], "error": str(e)}


@router.post("/invoice")
async def process_invoice(
    request: models.InvoiceRequest,
    _api_key: ApiKey,
):
    """
    Process invoice - requires authentication.

    Main endpoint for invoice processing from n8n workflow.

    Workflow:
    1. Decode and save PDF
    2. Extract invoice data from PDF
    3. Save to SQLite database
    4. Generate ISDOC XML
    5. Save XML to disk
    6. [Optional] Save to PostgreSQL staging database
    """
    try:
        # 1. Decode PDF file
        pdf_data = base64.b64decode(request.file_b64)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_pdf_filename = f"{timestamp}_temp_{request.filename}"
        pdf_path = config.PDF_DIR / temp_pdf_filename

        pdf_path.write_bytes(pdf_data)
        print(f"[OK] PDF saved: {pdf_path}")

        file_hash = hashlib.md5(pdf_data).hexdigest()

        database.init_database()
        is_duplicate_found = database.is_duplicate(
            file_hash=file_hash,
            customer_name=None,
        )

        if is_duplicate_found:
            print(f"[WARN] Duplicate invoice detected: file_hash={file_hash}")
            return {
                "success": True,
                "message": "Duplicate invoice detected - already processed",
                "duplicate": True,
                "file_hash": file_hash,
                "received_date": request.received_date,
            }

        # 2. Extract data from PDF
        if detect_marso_invoice_from_pdf(str(pdf_path)):
            print("[INFO] Detected MARSO invoice - using MARSO extractor")
            invoice_data = extract_marso_as_standard(str(pdf_path))
        else:
            print("[INFO] Using L&Š extractor (default)")
            invoice_data = extract_invoice_data(str(pdf_path))

        if not invoice_data:
            raise Exception("Failed to extract data from PDF")

        print(f"[OK] Data extracted: Invoice {invoice_data.invoice_number}")

        # 3. Save to SQLite database
        database.save_invoice(
            customer_name=invoice_data.customer_name,
            invoice_number=invoice_data.invoice_number,
            invoice_date=invoice_data.issue_date,
            total_amount=float(invoice_data.total_amount) if invoice_data.total_amount else 0.0,
            file_path=str(pdf_path),
            file_hash=file_hash,
            status="received",
        )
        print(f"[OK] Saved to SQLite: {invoice_data.invoice_number}")

        # 4. Rename PDF and generate XML
        file_basename = f"{timestamp}_{invoice_data.invoice_number}"
        final_pdf_filename = f"{file_basename}.pdf"
        final_pdf_path = config.PDF_DIR / final_pdf_filename
        pdf_path.rename(final_pdf_path)
        pdf_path = final_pdf_path
        print(f"[OK] PDF renamed: {pdf_path}")

        xml_filename = f"{file_basename}.xml"
        xml_path = config.XML_DIR / xml_filename

        isdoc_xml = generate_isdoc_xml(invoice_data, str(xml_path))
        print(f"[OK] ISDOC XML generated: {xml_path}")

        # 5. Save to PostgreSQL staging database (if enabled)
        postgres_saved = False
        postgres_invoice_id = None

        if config.POSTGRES_STAGING_ENABLED:
            try:
                pg_config = {
                    "host": config.POSTGRES_HOST,
                    "port": config.POSTGRES_PORT,
                    "database": config.POSTGRES_DATABASE,
                    "user": config.POSTGRES_USER,
                    "password": config.POSTGRES_PASSWORD,
                }

                with StagingClient(config=pg_config) as pg_client:
                    is_duplicate = pg_client.check_duplicate_invoice(
                        invoice_data.supplier_ico, invoice_data.invoice_number
                    )

                    if is_duplicate:
                        print(f"[WARN] Invoice already exists in PostgreSQL: {invoice_data.invoice_number}")
                    else:
                        invoice_pg_data = {
                            "supplier_ico": invoice_data.supplier_ico,
                            "supplier_name": invoice_data.supplier_name,
                            "supplier_dic": invoice_data.supplier_dic,
                            "invoice_number": invoice_data.invoice_number,
                            "invoice_date": invoice_data.issue_date,
                            "due_date": invoice_data.due_date,
                            "total_amount": invoice_data.total_amount,
                            "total_vat": invoice_data.tax_amount,
                            "total_without_vat": invoice_data.net_amount,
                            "currency": invoice_data.currency,
                            "file_basename": file_basename,
                            "file_status": "received",
                            "pdf_file_path": str(pdf_path),
                            "xml_file_path": str(xml_path),
                        }

                        items_pg_data = []
                        for item in invoice_data.items:
                            items_pg_data.append(
                                {
                                    "line_number": item.line_number,
                                    "name": item.description,
                                    "quantity": item.quantity,
                                    "unit": item.unit,
                                    "price_per_unit": item.unit_price_no_vat,
                                    "ean": item.ean_code,
                                    "vat_rate": item.vat_rate,
                                }
                            )

                        postgres_invoice_id = pg_client.insert_invoice_with_items(
                            invoice_pg_data, items_pg_data, isdoc_xml
                        )

                        if postgres_invoice_id:
                            postgres_saved = True
                            print(f"[OK] Saved to PostgreSQL: invoice_id={postgres_invoice_id}")

                            staged_pdf, staged_xml = move_files_to_staging(
                                pdf_path,
                                xml_path,
                                file_basename,
                                pg_client._conn,
                                postgres_invoice_id,
                            )
                            if staged_pdf:
                                pdf_path = staged_pdf
                            if staged_xml:
                                xml_path = staged_xml
                        else:
                            print("[FAIL] Failed to save to PostgreSQL staging")

            except Exception as pg_error:
                print(f"[WARN] PostgreSQL staging error: {pg_error}")

        return {
            "success": True,
            "message": "Invoice processed successfully",
            "invoice_number": invoice_data.invoice_number,
            "customer_name": invoice_data.customer_name,
            "total_amount": float(invoice_data.total_amount) if invoice_data.total_amount else 0.0,
            "items_count": len(invoice_data.items),
            "pdf_saved": str(pdf_path),
            "xml_saved": str(xml_path),
            "file_basename": file_basename,
            "sqlite_saved": True,
            "postgres_staging_enabled": config.POSTGRES_STAGING_ENABLED,
            "postgres_saved": postgres_saved,
            "postgres_invoice_id": postgres_invoice_id,
            "received_date": request.received_date,
        }

    except Exception as e:
        print(f"[FAIL] Invoice processing failed: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Invoice processing failed: {str(e)}")


# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================


@router.post("/admin/test-email")
async def admin_test_email(_api_key: ApiKey):
    """Admin endpoint - send test email."""
    try:
        result = notifications.send_test_email()
        return {
            "success": result,
            "message": "Test email sent successfully" if result else "Failed to send test email",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")


@router.post("/admin/send-summary")
async def admin_send_summary(_api_key: ApiKey):
    """Admin endpoint - send daily summary."""
    try:
        result = notifications.send_daily_summary()
        return {
            "success": result,
            "message": "Daily summary sent successfully" if result else "Failed to send summary",
        }
    except Exception as e:
        return {"success": False, "message": f"Failed to send summary: {str(e)}"}
