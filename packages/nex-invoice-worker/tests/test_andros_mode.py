"""Tests for andros mode of nex-invoice-worker."""

import os
from unittest import mock

import pytest

from nex_invoice_worker.config.tenant import WorkerTenant, get_tenant
from nex_invoice_worker.config.settings import Settings


class TestAndrosTenant:
    """Test tenant detection in andros mode."""

    def test_andros_tenant(self):
        """WORKER_TENANT=andros should select andros mode."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "andros"}):
            tenant = get_tenant()
            assert tenant == WorkerTenant.ANDROS
            assert tenant.value == "andros"

    def test_andros_task_queue(self):
        """Andros mode should use andros-invoice-queue."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "andros"}):
            settings = Settings()
            assert settings.temporal_task_queue == "andros-invoice-queue"

    def test_andros_customer_code(self):
        """Andros mode should use ANDROS customer code."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "andros"}):
            settings = Settings()
            assert settings.customer_code == "ANDROS"

    def test_andros_settings_has_postgres(self):
        """Andros settings should have PostgreSQL fields."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "andros"}):
            settings = Settings()
            assert settings.postgres_host == "localhost"
            assert settings.postgres_port == 5432
            assert settings.postgres_db is not None

    def test_andros_postgres_dsn(self):
        """Andros settings should provide postgres_dsn property."""
        with mock.patch.dict(
            os.environ,
            {
                "WORKER_TENANT": "andros",
                "POSTGRES_PASSWORD": "testpass",
            },
        ):
            settings = Settings()
            dsn = settings.postgres_dsn
            assert "postgresql://" in dsn
            assert "testpass" in dsn


class TestAndrosAdapter:
    """Test MARSO adapter in andros mode."""

    def test_andros_marso_ico(self):
        """Andros mode should use ANDROS-specific IČO."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "andros"}):
            from nex_invoice_worker.adapters.marso_adapter import _SUPPLIER_ICO

            assert _SUPPLIER_ICO[WorkerTenant.ANDROS] == "10428342215"

    def test_supplier_marso_ico(self):
        """Supplier mode should use supplier-specific IČO."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "supplier"}):
            from nex_invoice_worker.adapters.marso_adapter import _SUPPLIER_ICO

            assert _SUPPLIER_ICO[WorkerTenant.SUPPLIER] == "10428342"


class TestTenantEnum:
    """Test WorkerTenant enum."""

    def test_invalid_tenant_raises_error(self):
        """Invalid tenant value should raise ValueError."""
        with mock.patch.dict(os.environ, {"WORKER_TENANT": "invalid"}):
            with pytest.raises(ValueError):
                get_tenant()

    def test_tenant_is_str_enum(self):
        """WorkerTenant should be a str enum."""
        assert isinstance(WorkerTenant.SUPPLIER, str)
        assert isinstance(WorkerTenant.ANDROS, str)
