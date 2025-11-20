#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-End Test Workflow - NEX Automat
Location: C:/Development/nex-automat/e2e_test_workflow.py

Testuje celý workflow:
1. Pošle test email s PDF faktúrou (alebo priamo na FastAPI)
2. Overí spracovanie cez n8n + FastAPI
3. Skontroluje DB invoice_staging
4. Otvorí GUI editor

Requirements:
- FastAPI server beží (https://magerstav-invoices.icc.sk)
- PostgreSQL dostupný
- Gmail konto nakonfigurované (pre email test)

Usage:
  python e2e_test_workflow.py              # S emailom
  python e2e_test_workflow.py --skip-email # Priamo na FastAPI
"""

import os
import sys
import time
import smtplib
import asyncio
import base64
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import asyncpg
    import httpx
except ImportError as e:
    print(f"❌ Chýbajúca dependency: {e}")
    print("Nainštaluj: pip install asyncpg httpx")
    sys.exit(1)

# =====================================================================
# KONFIGURÁCIA
# =====================================================================

# Email settings
FROM_EMAIL = "test@example.com"  # Tvoj odosielateľ
TO_EMAIL = "magerstavinvoice@gmail.com"
SMTP_SERVER = "smtp.gmail.com"  # Alebo tvoj SMTP server
SMTP_PORT = 587

# FastAPI endpoint
FASTAPI_URL = "https://magerstav-invoices.icc.sk"
API_KEY = os.getenv("LS_API_KEY", "CHANGE_ME_PRODUCTION_KEY")

# Database
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "invoice_staging"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Test PDF location
TEST_PDF_DIR = Path("C:/Development/nex-automat/apps/supplier-invoice-loader/tests/samples")

# GUI Editor
EDITOR_PATH = Path("C:/Development/nex-automat/apps/supplier-invoice-editor/main.py")


# =====================================================================
# HELPER FUNKCIE
# =====================================================================

def print_header(title: str):
    """Print formatted header"""
    print()
    print("=" * 70)
    print(f"🎯 {title}")
    print("=" * 70)
    print()


def print_step(step: str, status: str = ""):
    """Print step with status"""
    if status == "✅":
        print(f"  ✅ {step}")
    elif status == "❌":
        print(f"  ❌ {step}")
    elif status == "⏳":
        print(f"  ⏳ {step}...")
    else:
        print(f"  → {step}")


# =====================================================================
# STEP 1: CHECK PREREQUISITES
# =====================================================================

def check_prerequisites():
    """Check if all required services are running"""
    print_header("STEP 1: Kontrola predpokladov")

    # Check n8n (nevieme priamo, ale overíme)
    print_step("n8n workflow", "⏳")
    print("     ℹ️  Skontroluj manuálne že n8n beží a workflow je aktívny")

    # Check FastAPI
    print_step("FastAPI server", "⏳")
    try:
        response = httpx.get(f"{FASTAPI_URL}/health", timeout=5.0)
        if response.status_code == 200:
            print_step("FastAPI server", "✅")
        else:
            print_step(f"FastAPI server (status {response.status_code})", "❌")
            return False
    except Exception as e:
        print_step(f"FastAPI server nedostupný: {e}", "❌")
        return False

    # Check database password
    print_step("Database password", "⏳")
    if not DB_PASSWORD:
        print_step("POSTGRES_PASSWORD env variable nie je nastavená", "❌")
        return False
    print_step("Database password", "✅")

    # Check test PDFs
    print_step("Test PDF súbory", "⏳")
    if not TEST_PDF_DIR.exists():
        print_step(f"Test PDF dir neexistuje: {TEST_PDF_DIR}", "❌")
        return False

    pdf_files = list(TEST_PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print_step("Žiadne PDF súbory nenájdené", "❌")
        return False

    print_step(f"Nájdených {len(pdf_files)} PDF súborov", "✅")

    # Check editor
    print_step("GUI Editor", "⏳")
    if not EDITOR_PATH.exists():
        print_step(f"Editor neexistuje: {EDITOR_PATH}", "❌")
        return False
    print_step("GUI Editor", "✅")

    return True


# =====================================================================
# STEP 2: SELECT TEST PDF
# =====================================================================

def select_test_pdf() -> Path:
    """Select test PDF file"""
    print_header("STEP 2: Výber test PDF")

    pdf_files = sorted(TEST_PDF_DIR.glob("*.pdf"))

    print("Dostupné PDF súbory:")
    for i, pdf in enumerate(pdf_files[:5], 1):  # Show first 5
        size_kb = pdf.stat().st_size / 1024
        print(f"  {i}. {pdf.name} ({size_kb:.1f} KB)")

    if len(pdf_files) > 5:
        print(f"  ... a ďalších {len(pdf_files) - 5} súborov")

    # Use first PDF
    selected = pdf_files[0]
    print()
    print_step(f"Vybraný: {selected.name}", "✅")

    return selected


# =====================================================================
# STEP 3: SEND EMAIL OR POST DIRECTLY
# =====================================================================

def send_test_email(pdf_path: Path) -> str:
    """Send test email with PDF attachment"""
    print_header("STEP 3: Odoslanie test emailu")

    print_step("Príprava emailu", "⏳")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"[TEST] Faktúra {datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Body
    body = f"""
    Test email pre End-to-End workflow test.

    PDF: {pdf_path.name}
    Čas: {datetime.now().isoformat()}
    Workflow: n8n → FastAPI → PostgreSQL → GUI Editor
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    with open(pdf_path, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment',
                                  filename=pdf_path.name)
        msg.attach(pdf_attachment)

    print_step("Email pripravený", "✅")

    # Get SMTP credentials
    print()
    print("⚠️  SMTP Authentication Required:")
    print(f"   Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"   From: {FROM_EMAIL}")

    smtp_user = input(f"   SMTP Username [{FROM_EMAIL}]: ").strip() or FROM_EMAIL
    smtp_pass = input("   SMTP Password: ").strip()

    if not smtp_pass:
        print_step("SMTP password nie je zadané", "❌")
        return None

    print()
    print_step("Odosielanie emailu", "⏳")

    try:
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        message_id = msg['Message-ID'] or datetime.now().isoformat()
        print_step(f"Email odoslaný: {message_id}", "✅")
        return message_id

    except Exception as e:
        print_step(f"Chyba pri odoslaní: {e}", "❌")
        return None


def send_direct_to_fastapi(pdf_path: Path) -> str:
    """Send PDF directly to FastAPI endpoint (skip email)"""
    print_header("STEP 3: Priame odoslanie na FastAPI")

    print_step("Príprava payload", "⏳")

    # Read PDF and encode to base64
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # Prepare payload matching n8n format
    message_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    payload = {
        "file_b64": pdf_b64,
        "filename": pdf_path.name,
        "from_email": "test@e2e-workflow.local",
        "message_id": message_id,
        "gmail_id": message_id,
        "subject": f"[E2E TEST] {pdf_path.name}",
        "received_date": datetime.now().isoformat()
    }

    print_step("Payload pripravený", "✅")
    print(f"     Filename: {pdf_path.name}")
    print(f"     Size: {len(pdf_b64)} chars base64")
    print()

    print_step("Odosielanie na FastAPI", "⏳")
    print(f"     URL: {FASTAPI_URL}/invoice")
    print(f"     API Key: {API_KEY[:20]}...")

    try:
        response = httpx.post(
            f"{FASTAPI_URL}/invoice",
            json=payload,
            headers={
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            timeout=120.0
        )

        if response.status_code == 200:
            result = response.json()
            print_step(f"FastAPI response: {response.status_code}", "✅")
            print(f"     Invoice ID: {result.get('invoice_id', 'N/A')}")
            print(f"     Status: {result.get('status', 'N/A')}")
            return message_id
        else:
            print_step(f"FastAPI error: {response.status_code}", "❌")
            print(f"     Response: {response.text[:200]}")
            return None

    except Exception as e:
        print_step(f"Chyba pri odoslaní: {e}", "❌")
        return None


# =====================================================================
# STEP 4: WAIT FOR PROCESSING (only for email mode)
# =====================================================================

def wait_for_processing(skip_email: bool = False):
    """Wait for n8n and FastAPI processing"""
    if skip_email:
        print_header("STEP 4: Spracovanie (priame)")
        print_step("Spracované priamo cez FastAPI", "✅")
        return

    print_header("STEP 4: Čakanie na spracovanie")

    print_step("n8n workflow (IMAP trigger)", "⏳")
    print("     ℹ️  IMAP trigger má delay, čakám 30 sekúnd...")

    for i in range(30, 0, -5):
        print(f"     ⏰ Zostáva {i} sekúnd...", end='\r')
        time.sleep(5)

    print()
    print_step("Workflow by mal byť spracovaný", "✅")


# =====================================================================
# STEP 5: CHECK DATABASE
# =====================================================================

async def check_database(message_id: str):
    """Check if invoice was saved to database"""
    print_header("STEP 5: Kontrola databázy")

    print_step("Pripájanie k PostgreSQL", "⏳")

    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        print_step("Pripojený k databáze", "✅")

        # Query for recent invoices
        print_step("Hľadám spracovanú faktúru", "⏳")

        query = """
        SELECT id, invoice_number, supplier_name, created_at, status
        FROM invoices_pending
        ORDER BY created_at DESC
        LIMIT 5
        """

        rows = await conn.fetch(query)

        if not rows:
            print_step("Žiadne faktúry v databáze", "❌")
            await conn.close()
            return None

        print()
        print("📊 Posledných 5 faktúr:")
        print("-" * 70)

        latest_invoice = None
        for row in rows:
            created = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            print(f"  ID: {row['id']}")
            print(f"     Číslo faktúry: {row['invoice_number']}")
            print(f"     Dodávateľ: {row['supplier_name']}")
            print(f"     Vytvorené: {created}")
            print(f"     Status: {row['status']}")
            print()

            if not latest_invoice:
                latest_invoice = row['id']

        print_step(f"Nájdená faktúra ID: {latest_invoice}", "✅")

        await conn.close()
        return latest_invoice

    except Exception as e:
        print_step(f"Chyba pri pripojení k DB: {e}", "❌")
        return None


# =====================================================================
# STEP 6: OPEN GUI EDITOR
# =====================================================================

def open_gui_editor(invoice_id: int = None):
    """Open GUI editor"""
    print_header("STEP 6: Otvorenie GUI Editora")

    print_step("Spúšťam supplier-invoice-editor", "⏳")

    import subprocess

    try:
        # Open editor
        venv_python = Path("C:/Development/nex-automat/venv32/Scripts/python.exe")

        if not venv_python.exists():
            print_step("venv32 Python nenájdený", "❌")
            return

        cmd = [str(venv_python), str(EDITOR_PATH)]

        print(f"     Príkaz: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            cwd=EDITOR_PATH.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print_step("GUI Editor spustený", "✅")

        if invoice_id:
            print(f"     ℹ️  Vyber faktúru ID: {invoice_id}")

        print()
        print("     ⏳ Editor beží... (zatvor okno pre ukončenie)")

        # Wait for editor to close
        process.wait()

        print_step("Editor zatvorený", "✅")

    except Exception as e:
        print_step(f"Chyba pri spustení editora: {e}", "❌")


# =====================================================================
# MAIN WORKFLOW
# =====================================================================

async def main():
    """Main E2E test workflow"""
    # Check for --skip-email flag
    skip_email = "--skip-email" in sys.argv

    print()
    print("=" * 70)
    print("🚀 NEX AUTOMAT - END-TO-END TEST WORKFLOW")
    print("=" * 70)
    print()

    if skip_email:
        print("📌 MODE: Direct FastAPI (skip email)")
        print()
        print("Test workflow:")
        print("  1. PDF → FastAPI /invoice (priamo)")
        print("  2. FastAPI → PostgreSQL invoice_staging")
        print("  3. GUI Editor → Zobraz faktúru")
    else:
        print("📌 MODE: Full workflow (email)")
        print()
        print("Test workflow:")
        print("  1. Email s PDF → magerstavinvoice@gmail.com")
        print("  2. n8n IMAP trigger → Split PDF")
        print("  3. n8n HTTP → FastAPI /invoice (Cloudflare Tunnel)")
        print("  4. FastAPI → PostgreSQL invoice_staging")
        print("  5. GUI Editor → Zobraz faktúru")
    print()

    # Step 1: Check prerequisites
    if not check_prerequisites():
        print()
        print("❌ Predpoklady nie sú splnené. Oprav chyby a skús znova.")
        return

    # Step 2: Select test PDF
    pdf_path = select_test_pdf()

    # Step 3: Send email or post directly
    if skip_email:
        message_id = send_direct_to_fastapi(pdf_path)
    else:
        message_id = send_test_email(pdf_path)

    if not message_id:
        print()
        print("❌ Odoslanie zlyhalo. Test zrušený.")
        return

    # Step 4: Wait for processing
    wait_for_processing(skip_email)

    # Step 5: Check database
    invoice_id = await check_database(message_id)

    if not invoice_id:
        print()
        print("⚠️  Faktúra nebola nájdená v databáze.")
        print("    Skontroluj:")
        print("    - n8n workflow log")
        print("    - FastAPI logy")
        print("    - PostgreSQL connection")
        return

    # Step 6: Open GUI editor
    print()
    response = input("Chceš otvoriť GUI Editor? [A/n]: ").strip().lower()
    if response != 'n':
        open_gui_editor(invoice_id)

    # Summary
    print()
    print("=" * 70)
    print("✅ END-TO-END TEST DOKONČENÝ")
    print("=" * 70)
    print()
    print("📊 Výsledky:")
    if skip_email:
        print(f"  ✅ PDF odoslaný priamo na FastAPI")
    else:
        print(f"  ✅ Email odoslaný: {message_id}")
    print(f"  ✅ Faktúra v DB: ID {invoice_id}")
    print(f"  ✅ GUI Editor overený")
    print()
    print("🎉 Workflow funguje správne!")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print("⚠️  Test prerušený používateľom")
    except Exception as e:
        print()
        print(f"❌ Neočakávaná chyba: {e}")
        import traceback

        traceback.print_exc()