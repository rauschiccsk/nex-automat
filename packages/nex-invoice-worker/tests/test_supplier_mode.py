"""Tests for supplier (ICC) mode of nex-invoice-worker."""

import os
from unittest import mock

import pytest

from nex_invoice_worker.config.tenant import WorkerTenant, get_tenant
from nex_invoice_worker.config.settings import Settings


class TestSupplierTenant:
    """Test tenant detection in supplier mode."""

    def test_default_tenant_is_supplier(self):
        """Default tenant should be supplier when WORKER_TENANT is not set."""
        with mock.patch.dict(os.environ, {}, clear=False):
            # Remove WORKER_TENANT if set
            env = {k: v for k, v in os.environ.items() if k != "WORKER_TENANT"}
            with mock.patch.dict(os.environ, env, clear=True):
                tenant = get_tenant()
                assert tenant == WorkerTenant.SUPPLIER
                assert tenant.value == "supplier"

    def test_explicit_supplier_tenant(self):
        """Explicit WORKER_TENANT=supplier should work."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "supplier"}):
            tenant = get_tenant()
            assert tenant == WorkerTenant.SUPPLIER

    def test_supplier_task_queue(self):
        """Supplier mode should use supplier-invoice-queue."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "supplier"}):
            settings = Settings()
            assert settings.temporal_task_queue == "supplier-invoice-queue"

    def test_supplier_customer_code(self):
        """Supplier mode should use ICC customer code."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "supplier"}):
            settings = Settings()
            assert settings.customer_code == "ICC"

    def test_supplier_settings_has_imap(self):
        """Supplier settings should have IMAP fields."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "supplier"}):
            settings = Settings()
            assert settings.imap_host == "imap.gmail.com"
            assert settings.imap_port == 993


class TestSupplierModels:
    """Test models in supplier mode."""

    def test_invoice_status_is_str_enum(self):
        """InvoiceStatus should inherit from str for JSON serialization."""
        from nex_invoice_worker.models.unified_invoice import InvoiceStatus

        assert isinstance(InvoiceStatus.PENDING, str)
        assert InvoiceStatus.PENDING == "pending"

    def test_unified_invoice_creation(self):
        """UnifiedInvoice should be creatable with required fields."""
        from datetime import datetime
        from nex_invoice_worker.models.unified_invoice import (
            InvoiceStatus,
            UnifiedInvoice,
        )

        invoice = UnifiedInvoice(
            source_type="api",
            supplier_id="marso",
            supplier_name="MARSO",
            invoice_number="TEST-001",
            invoice_date=datetime.now(),
            external_invoice_id="EXT-001",
            total_without_vat=100.0,
            total_vat=20.0,
            total_with_vat=120.0,
            items=[],
            fetched_at=datetime.now(),
            status=InvoiceStatus.PENDING,
        )
        assert invoice.invoice_number == "TEST-001"
        assert invoice.currency == "EUR"
