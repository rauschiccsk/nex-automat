"""
File Mover Service - Archive operations
Moves invoice files from STAGING to ARCHIVE after NEX Genesis import.
"""

import os
import shutil
from pathlib import Path

import pg8000.dbapi

# Archive paths
STAGING_DIR = Path(r"C:\NEX\IMPORT\SUPPLIER-STAGING")
ARCHIVE_PDF_DIR = Path(r"C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\PDF")
ARCHIVE_XML_DIR = Path(r"C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\XML")


def get_db_connection():
    """Get PostgreSQL connection."""
    return pg8000.dbapi.connect(
        host="localhost",
        port=5432,
        database="supplier_invoice_staging",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def move_files_to_archive(
    invoice_id: int, nex_invoice_doc_id: str, nex_delivery_doc_id: str | None = None
) -> tuple[Path | None, Path | None]:
    """
    Move PDF and XML files from STAGING to ARCHIVE directory.
    Rename files to final format: {DF_number}-{DD_number}.pdf|xml
    Update file_status in PostgreSQL to 'archived'.

    Args:
        invoice_id: Invoice ID in PostgreSQL
        nex_invoice_doc_id: NEX Genesis invoice document ID (e.g., DF2500100123)
        nex_delivery_doc_id: NEX Genesis delivery note ID (e.g., DD2500100205), optional

    Returns:
        tuple: (archived_pdf_path, archived_xml_path) or (None, None) on error
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get current file paths and basename
        cursor.execute(
            """
            SELECT file_basename, pdf_file_path, xml_file_path, file_status
            FROM supplier_invoice_heads
            WHERE id = %s
        """,
            (invoice_id,),
        )

        row = cursor.fetchone()
        if not row:
            print(f"[FAIL] Invoice {invoice_id} not found")
            return (None, None)

        file_basename, pdf_path, xml_path, current_status = row

        if current_status == "archived":
            print(f"[SKIP] Invoice {invoice_id} already archived")
            return (None, None)

        if current_status != "staged":
            print(f"[WARN] Invoice {invoice_id} status is '{current_status}', expected 'staged'")

        # Build archive filename
        if nex_delivery_doc_id:
            archive_basename = f"{nex_invoice_doc_id}-{nex_delivery_doc_id}"
        else:
            archive_basename = nex_invoice_doc_id

        archived_pdf_path = None
        archived_xml_path = None

        # Move PDF
        if pdf_path:
            src_pdf = Path(pdf_path)
            if src_pdf.exists():
                dst_pdf = ARCHIVE_PDF_DIR / f"{archive_basename}.pdf"
                shutil.move(str(src_pdf), str(dst_pdf))
                archived_pdf_path = dst_pdf
                print(f"[OK] PDF archived: {dst_pdf}")
            else:
                print(f"[WARN] PDF not found: {src_pdf}")

        # Move XML
        if xml_path:
            src_xml = Path(xml_path)
            if src_xml.exists():
                dst_xml = ARCHIVE_XML_DIR / f"{archive_basename}.xml"
                shutil.move(str(src_xml), str(dst_xml))
                archived_xml_path = dst_xml
                print(f"[OK] XML archived: {dst_xml}")
            else:
                print(f"[WARN] XML not found: {src_xml}")

        # Update database
        cursor.execute(
            """
            UPDATE supplier_invoice_heads 
            SET file_status = 'archived',
                pdf_file_path = %s,
                xml_file_path = %s,
                nex_invoice_doc_id = %s,
                nex_delivery_doc_id = %s,
                updated_at = NOW()
            WHERE id = %s
        """,
            (
                str(archived_pdf_path) if archived_pdf_path else None,
                str(archived_xml_path) if archived_xml_path else None,
                nex_invoice_doc_id,
                nex_delivery_doc_id,
                invoice_id,
            ),
        )

        conn.commit()
        print(f"[OK] Invoice {invoice_id} archived: {archive_basename}")

        return (archived_pdf_path, archived_xml_path)

    except Exception as e:
        print(f"[FAIL] Failed to archive invoice {invoice_id}: {e}")
        if conn:
            conn.rollback()
        return (None, None)
    finally:
        if conn:
            conn.close()


# Example usage (will be called from NEX import function):
# from services.file_mover import move_files_to_archive
# move_files_to_archive(invoice_id=123, nex_invoice_doc_id="DF2500100123", nex_delivery_doc_id="DD2500100205")
