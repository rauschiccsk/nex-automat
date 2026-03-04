"""Konfigurácia databázových pripojení."""
import os

# PostgreSQL — hlavná databáza
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # BEZ fallbacku — povinný env var
DB_NAME_MAIN = os.getenv("POSTGRES_DB", "nex_automat")
DB_NAME_STAGING = os.getenv("STAGING_DB", "supplier_invoice_staging")
DB_NAME_RAG = os.getenv("RAG_DB", "nex_automat_rag")
DB_NAME_INVOICES = os.getenv("INVOICES_DB", "nex_invoices")

# NEX Migration — Docker port mapping
NEX_MIGRATION_DB_PORT = int(os.getenv("NEX_MIGRATION_DB_PORT", "9150"))
