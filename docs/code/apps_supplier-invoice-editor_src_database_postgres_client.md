# postgres_client.py

**Path:** `apps\supplier-invoice-editor\src\database\postgres_client.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

PostgreSQL Client - Database connection using pg8000 (Pure Python)

---

## Classes

### PostgresClient

PostgreSQL database client using pg8000

**Methods:**

#### `__init__(self, config)`

Initialize PostgreSQL client

Args:
    config: Configuration object

#### `_get_connection_params(self)`

Get connection parameters from config

#### `get_connection(self)`

Get database connection (context manager)

Usage:
    with client.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM table")

#### `execute_query(self, query, params, fetch)`

Execute SQL query

Args:
    query: SQL query string
    params: Query parameters
    fetch: Whether to fetch results

Returns:
    List of result dictionaries if fetch=True, None otherwise

#### `execute_many(self, query, params_list)`

Execute query with multiple parameter sets

Args:
    query: SQL query string
    params_list: List of parameter tuples

Returns:
    Number of affected rows

#### `transaction(self)`

Transaction context manager

Usage:
    with client.transaction() as conn:
        cur = conn.cursor()
        cur.execute("INSERT ...")
        cur.execute("UPDATE ...")
        # Auto-commit on success, rollback on exception

#### `test_connection(self)`

Test database connection

Returns:
    True if connection successful

#### `close(self)`

Close connections (pg8000 connections are closed in context managers)

---
