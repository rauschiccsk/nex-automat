"""
Insert test data into supplier_invoice_staging database.
"""

import os
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "supplier_invoice_staging",
    "user": "postgres",
    "password": os.environ.get("POSTGRES_PASSWORD", "")
}

TEST_INVOICES = [
    {
        "xml_invoice_number": "F2024-001",
        "xml_variable_symbol": "2024001",
        "xml_issue_date": "2024-12-15",
        "xml_due_date": "2024-12-29",
        "xml_currency": "EUR",
        "xml_supplier_ico": "12345678",
        "xml_supplier_name": "METRO Cash & Carry SK",
        "xml_supplier_dic": "2023456789",
        "xml_total_without_vat": 1042.08,
        "xml_total_vat": 208.42,
        "xml_total_with_vat": 1250.50,
        "status": "pending",
        "item_count": 15,
        "match_percent": 45.0
    },
    {
        "xml_invoice_number": "F2024-002",
        "xml_variable_symbol": "2024002",
        "xml_issue_date": "2024-12-14",
        "xml_due_date": "2024-12-28",
        "xml_currency": "EUR",
        "xml_supplier_ico": "87654321",
        "xml_supplier_name": "MAKRO Cash & Carry",
        "xml_supplier_dic": "2098765432",
        "xml_total_without_vat": 741.67,
        "xml_total_vat": 148.33,
        "xml_total_with_vat": 890.00,
        "status": "matched",
        "item_count": 8,
        "match_percent": 100.0
    },
    {
        "xml_invoice_number": "F2024-003",
        "xml_variable_symbol": "2024003",
        "xml_issue_date": "2024-12-13",
        "xml_due_date": "2024-12-27",
        "xml_currency": "EUR",
        "xml_supplier_ico": "11223344",
        "xml_supplier_name": "LIDL Slovenská republika",
        "xml_supplier_dic": "2011223344",
        "xml_total_without_vat": 1750.63,
        "xml_total_vat": 350.12,
        "xml_total_with_vat": 2100.75,
        "status": "processing",
        "item_count": 22,
        "match_percent": 68.0
    },
    {
        "xml_invoice_number": "F2024-004",
        "xml_variable_symbol": "2024004",
        "xml_issue_date": "2024-12-12",
        "xml_due_date": "2024-12-26",
        "xml_currency": "EUR",
        "xml_supplier_ico": "55667788",
        "xml_supplier_name": "TESCO Stores SR",
        "xml_supplier_dic": "2055667788",
        "xml_total_without_vat": 458.54,
        "xml_total_vat": 91.71,
        "xml_total_with_vat": 550.25,
        "status": "pending",
        "item_count": 5,
        "match_percent": 20.0
    },
    {
        "xml_invoice_number": "F2024-005",
        "xml_variable_symbol": "2024005",
        "xml_issue_date": "2024-12-11",
        "xml_due_date": "2024-12-25",
        "xml_currency": "EUR",
        "xml_supplier_ico": "99887766",
        "xml_supplier_name": "BILLA s.r.o.",
        "xml_supplier_dic": "2099887766",
        "xml_total_without_vat": 1500.00,
        "xml_total_vat": 300.00,
        "xml_total_with_vat": 1800.00,
        "status": "matched",
        "item_count": 12,
        "match_percent": 100.0
    },
]

TEST_ITEMS = [
    # Invoice 1 items (F2024-001)
    {"invoice_idx": 0, "xml_line_number": 1, "xml_product_name": "Mlieko polotučné 1L", "xml_ean": "8590123456789",
     "xml_quantity": 10, "xml_unit": "ks", "xml_unit_price": 1.20, "xml_vat_rate": 20.0, "matched": True,
     "matched_by": "ean"},
    {"invoice_idx": 0, "xml_line_number": 2, "xml_product_name": "Chlieb biely 500g", "xml_ean": "8590123456790",
     "xml_quantity": 5, "xml_unit": "ks", "xml_unit_price": 2.50, "xml_vat_rate": 20.0, "matched": False,
     "matched_by": None},
    {"invoice_idx": 0, "xml_line_number": 3, "xml_product_name": "Maslo 82% 250g", "xml_ean": "8590123456791",
     "xml_quantity": 20, "xml_unit": "ks", "xml_unit_price": 3.80, "xml_vat_rate": 20.0, "matched": True,
     "matched_by": "ean"},
    # Invoice 2 items (F2024-002)
    {"invoice_idx": 1, "xml_line_number": 1, "xml_product_name": "Jogurt biely 150g", "xml_ean": "8590123456792",
     "xml_quantity": 30, "xml_unit": "ks", "xml_unit_price": 0.65, "xml_vat_rate": 20.0, "matched": True,
     "matched_by": "ean"},
    {"invoice_idx": 1, "xml_line_number": 2, "xml_product_name": "Syr Eidam 45%", "xml_ean": "8590123456793",
     "xml_quantity": 8, "xml_unit": "ks", "xml_unit_price": 4.20, "xml_vat_rate": 20.0, "matched": True,
     "matched_by": "name"},
    # Invoice 3 items (F2024-003)
    {"invoice_idx": 2, "xml_line_number": 1, "xml_product_name": "Coca Cola 2L", "xml_ean": "5449000000996",
     "xml_quantity": 24, "xml_unit": "ks", "xml_unit_price": 2.10, "xml_vat_rate": 20.0, "matched": True,
     "matched_by": "ean"},
    {"invoice_idx": 2, "xml_line_number": 2, "xml_product_name": "Minerálka Budiš 1.5L", "xml_ean": "8590123456794",
     "xml_quantity": 48, "xml_unit": "ks", "xml_unit_price": 0.55, "xml_vat_rate": 20.0, "matched": False,
     "matched_by": None},
]


def main():
    if not DB_CONFIG["password"]:
        print("ERROR: POSTGRES_PASSWORD environment variable not set!")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Insert invoices
        invoice_ids = []
        for inv in TEST_INVOICES:
            cur.execute("""
                INSERT INTO supplier_invoice_heads (
                    xml_invoice_number, xml_variable_symbol, xml_issue_date, xml_due_date,
                    xml_currency, xml_supplier_ico, xml_supplier_name, xml_supplier_dic,
                    xml_total_without_vat, xml_total_vat, xml_total_with_vat,
                    status, item_count, match_percent
                ) VALUES (
                    %(xml_invoice_number)s, %(xml_variable_symbol)s, %(xml_issue_date)s, %(xml_due_date)s,
                    %(xml_currency)s, %(xml_supplier_ico)s, %(xml_supplier_name)s, %(xml_supplier_dic)s,
                    %(xml_total_without_vat)s, %(xml_total_vat)s, %(xml_total_with_vat)s,
                    %(status)s, %(item_count)s, %(match_percent)s
                ) RETURNING id
            """, inv)
            invoice_ids.append(cur.fetchone()[0])
            print(f"Inserted invoice: {inv['xml_invoice_number']}")

        # Insert items
        for item in TEST_ITEMS:
            invoice_id = invoice_ids[item["invoice_idx"]]
            cur.execute("""
                INSERT INTO supplier_invoice_items (
                    invoice_head_id, xml_line_number, xml_product_name, xml_ean,
                    xml_quantity, xml_unit, xml_unit_price, xml_vat_rate,
                    matched, matched_by
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                invoice_id, item["xml_line_number"], item["xml_product_name"], item["xml_ean"],
                item["xml_quantity"], item["xml_unit"], item["xml_unit_price"], item["xml_vat_rate"],
                item["matched"], item["matched_by"]
            ))
        print(f"Inserted {len(TEST_ITEMS)} items")

        conn.commit()
        cur.close()
        conn.close()

        print(f"\nDone! Inserted {len(TEST_INVOICES)} invoices with {len(TEST_ITEMS)} items.")

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()