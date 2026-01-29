"""
Test MARSO extractor integration into pipeline.
Tests detection routing and ISDOC XML generation.
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.business.isdoc_service import generate_isdoc_xml
from src.extractors.ls_extractor import extract_invoice_data
from src.extractors.marso_extractor import detect_marso_invoice_from_pdf, extract_marso_as_standard

# Test PDF paths
MARSO_PDF = r"C:\Test\szamla_masolat_5641876501.pdf"
# LS_PDF = r"C:\NEX_AN\IMPORT\LS\PDF\20250929_232558_32510374_FAK.pdf"


def test_marso_detection_and_extraction():
    """Test MARSO invoice detection and extraction."""
    print("=" * 80)
    print("MARSO Integration Test")
    print("=" * 80)

    pdf_path = MARSO_PDF

    if not Path(pdf_path).exists():
        print(f"ERROR: Test PDF not found: {pdf_path}")
        return False

    # 1. Test detection
    print(f"\n[1/4] Testing MARSO detection on: {pdf_path}")
    is_marso = detect_marso_invoice_from_pdf(pdf_path)
    print(f"      Detected as MARSO: {is_marso}")

    if not is_marso:
        print("      ERROR: Should be detected as MARSO!")
        return False
    print("      OK - Correctly identified as MARSO invoice")

    # 2. Test extraction with routing logic (same as main.py)
    print("\n[2/4] Testing extraction with routing logic...")
    if detect_marso_invoice_from_pdf(pdf_path):
        print("      Using MARSO extractor...")
        invoice_data = extract_marso_as_standard(pdf_path)
    else:
        print("      Using L&S extractor...")
        invoice_data = extract_invoice_data(pdf_path)

    if not invoice_data:
        print("      ERROR: Extraction returned None!")
        return False

    print(f"      OK - Extracted invoice: {invoice_data.invoice_number}")
    print(f"         Supplier: {invoice_data.supplier_name}")
    print(f"         Customer: {invoice_data.customer_name}")
    print(f"         Issue date: {invoice_data.issue_date}")
    print(f"         Due date: {invoice_data.due_date}")
    print(f"         Total amount: {invoice_data.total_amount}")
    print(f"         Currency: {invoice_data.currency}")
    print(f"         Items count: {len(invoice_data.items)}")

    # 3. Test ISDOC XML generation
    print("\n[3/4] Testing ISDOC XML generation...")
    test_xml_path = r"C:\Test\marso_test_output.xml"

    try:
        generate_isdoc_xml(invoice_data, test_xml_path)
        print(f"      OK - XML generated: {test_xml_path}")
    except Exception as e:
        print(f"      ERROR generating XML: {e}")
        return False

    # 4. Verify XML was created
    print("\n[4/4] Verifying XML file...")
    if Path(test_xml_path).exists():
        size = Path(test_xml_path).stat().st_size
        print(f"      OK - XML file exists, size: {size} bytes")

        # Show first few lines
        with open(test_xml_path, encoding="utf-8") as f:
            lines = f.readlines()[:10]
            print("\n      First 10 lines of generated XML:")
            for line in lines:
                print(f"      {line.rstrip()}")
    else:
        print("      ERROR: XML file was not created!")
        return False

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED!")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = test_marso_detection_and_extraction()
    sys.exit(0 if success else 1)
