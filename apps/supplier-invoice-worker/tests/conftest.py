"""Pytest fixtures for supplier-invoice-worker tests."""

import pytest


@pytest.fixture
def marso_invoice_json():
    """Sample MARSO API response."""
    return {
        "InvoiceId": "11926-00447",
        "SalesId": "VR1234567",
        "Kelt": "2026-01-15",
        "Teljesites": "2026-01-15",
        "Hatarido": "2026-01-30",
        "InvName": "ANDROS s.r.o.",
        "InvZipCode": "94501",
        "InvCity": "Komárno",
        "InvStreet": "Hradná 123",
        "InvCountryRegionId": "SK",
        "Netto": 1000.00,
        "Afa": 200.00,
        "Brutto": 1200.00,
        "Penznem": "EUR",
        "Lines": [
            {
                "ItemId": "ABC123456",
                "ItemName": "Michelin Pilot Sport 4 225/45R17",
                "Qty": 4,
                "SalesUnit": "Db",
                "Netto": 250.00,
                "Afa": 50.00,
                "Brutto": 300.00,
                "ItemGroupid": "140",
            },
            {
                "ItemId": "DEF789012",
                "ItemName": "Continental PremiumContact 6 205/55R16",
                "Qty": 2,
                "SalesUnit": "Db",
                "Netto": 500.00,
                "Afa": 100.00,
                "Brutto": 600.00,
                "ItemGroupid": "140",
            },
        ],
    }


@pytest.fixture
def marso_config_dict():
    """Sample MARSO configuration as dict."""
    return {
        "supplier_id": "marso",
        "supplier_name": "MARSO Hungary Kft.",
        "auth_type": "api_key_body",
        "protocol": "soap",
        "wsdl_url": "http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl",
        "soap_method": "CallComax",
        "message_types": {"invoice_list": "CustInvoiceList"},
        "request_params": {"sender": "WebCatHU", "receiver": "Ax"},
        "response_format": "json",
        "api_key": "test_key",
    }
