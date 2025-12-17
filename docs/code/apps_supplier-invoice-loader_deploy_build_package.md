# build_package.py

**Path:** `apps\supplier-invoice-loader\deploy\build_package.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Deployment Package Builder
Creates ZIP packages for customer deployments

Usage:
    python build_package.py                    # Interactive mode
    python build_package.py --customer NAME    # Build for specific customer
    python build_package.py --template         # Build template package
    python build_package.py --full            # Build full package with venv

---

## Classes

### PackageBuilder

Deployment package builder

**Methods:**

#### `__init__(self, project_root)`

#### `log(self, message, level)`

Log message with color

#### `should_exclude(self, path)`

Check if file/dir should be excluded

#### `get_version(self)`

Get version from main.py or git

#### `create_manifest(self, package_type, customer_name)`

Create package manifest

#### `build_template_package(self)`

Build template package (no customer-specific files)

#### `build_customer_package(self, customer_name)`

Build customer-specific package

#### `build_full_package(self)`

Build full package including virtual environment

#### `sanitize_env_file(self, env_path)`

Remove sensitive data from .env file

#### `create_quickstart_guide(self)`

Create quick start guide

#### `create_customer_instructions(self, customer_name)`

Create customer-specific instructions

#### `create_full_deploy_script(self)`

Create deployment script for full package

#### `list_packages(self)`

List existing packages

#### `interactive_mode(self)`

Interactive package builder

---

## Functions

### `main()`

Main function

---
