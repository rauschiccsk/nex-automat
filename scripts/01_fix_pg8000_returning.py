#!/usr/bin/env python3
"""
Fix pg8000 INSERT RETURNING - list index out of range

Problem: pg8000.native.Connection.run() returns empty list for INSERT RETURNING
Solution: Check if result is empty before accessing [0][0]
"""

from pathlib import Path


def main():
    staging_client_path = Path("packages/nex-staging/nex_staging/staging_client.py")

    if not staging_client_path.exists():
        print(f"[ERROR] File not found: {staging_client_path}")
        return False

    content = staging_client_path.read_text(encoding="utf-8")

    # Fix 1: insert_invoice_with_items - safe access to result
    old_code = '''            result = self._run("""
                INSERT INTO supplier_invoice_heads (
                    xml_supplier_ico,
                    xml_supplier_name,
                    xml_supplier_dic,
                    xml_invoice_number,
                    xml_issue_date,
                    xml_due_date,
                    xml_total_with_vat,
                    xml_total_vat,
                    xml_total_without_vat,
                    xml_currency,
                    file_basename,
                    file_status,
                    pdf_file_path,
                    xml_file_path,
                    status,
                    item_count
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, (
                invoice_data.get('supplier_ico'),
                invoice_data.get('supplier_name'),
                invoice_data.get('supplier_dic'),
                invoice_data.get('invoice_number'),
                invoice_data.get('invoice_date'),
                invoice_data.get('due_date'),
                invoice_data.get('total_amount'),
                invoice_data.get('total_vat'),
                invoice_data.get('total_without_vat'),
                invoice_data.get('currency', 'EUR'),
                invoice_data.get('file_basename'),
                invoice_data.get('file_status', 'received'),
                invoice_data.get('pdf_file_path'),
                invoice_data.get('xml_file_path'),
                'pending',
                len(items_data)
            ))

            invoice_id = result[0][0]'''

    new_code = '''            result = self._run("""
                INSERT INTO supplier_invoice_heads (
                    xml_supplier_ico,
                    xml_supplier_name,
                    xml_supplier_dic,
                    xml_invoice_number,
                    xml_issue_date,
                    xml_due_date,
                    xml_total_with_vat,
                    xml_total_vat,
                    xml_total_without_vat,
                    xml_currency,
                    file_basename,
                    file_status,
                    pdf_file_path,
                    xml_file_path,
                    status,
                    item_count
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, (
                invoice_data.get('supplier_ico'),
                invoice_data.get('supplier_name'),
                invoice_data.get('supplier_dic'),
                invoice_data.get('invoice_number'),
                invoice_data.get('invoice_date'),
                invoice_data.get('due_date'),
                invoice_data.get('total_amount'),
                invoice_data.get('total_vat'),
                invoice_data.get('total_without_vat'),
                invoice_data.get('currency', 'EUR'),
                invoice_data.get('file_basename'),
                invoice_data.get('file_status', 'received'),
                invoice_data.get('pdf_file_path'),
                invoice_data.get('xml_file_path'),
                'pending',
                len(items_data)
            ))

            # pg8000.native.run() may return empty list for INSERT RETURNING
            if not result or len(result) == 0:
                raise RuntimeError("INSERT RETURNING failed - no result returned")
            invoice_id = result[0][0]'''

    if old_code not in content:
        print("[ERROR] Old code pattern not found in staging_client.py")
        print("[INFO] File may have been already modified or structure changed")
        return False

    content = content.replace(old_code, new_code)

    staging_client_path.write_text(content, encoding="utf-8")
    print(f"[OK] Fixed: {staging_client_path}")
    print("[INFO] Added safety check for INSERT RETURNING result")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)