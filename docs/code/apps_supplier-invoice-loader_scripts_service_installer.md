# service_installer.py

**Path:** `apps\supplier-invoice-loader\scripts\service_installer.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Windows Service Installer
Supports Windows 11 and Windows Server 2012 R2

This script manages Windows service installation using NSSM or native Windows SC.
NSSM is preferred for better control and features.

Usage:
    python service_installer.py install    # Install service
    python service_installer.py remove     # Remove service
    python service_installer.py status     # Check service status
    python service_installer.py start      # Start service
    python service_installer.py stop       # Stop service
    python service_installer.py restart    # Restart service
    python service_installer.py configure  # Reconfigure service

---

## Classes

### WindowsServiceInstaller

Windows Service Installer for Supplier Invoice Loader

**Methods:**

#### `__init__(self)`

#### `_check_nssm(self)`

Check if NSSM is available

#### `_get_windows_version(self)`

Get Windows version information

#### `is_admin(self)`

Check if running with administrator privileges

#### `run_as_admin(self)`

Restart the script with administrator privileges

#### `run_command(self, command, check)`

Run a command and return result

#### `install_with_nssm(self)`

Install service using NSSM

#### `install_with_sc(self)`

Install service using Windows SC command

#### `_set_recovery_actions(self)`

Set service recovery actions

#### `install_service(self)`

Install the Windows service

#### `remove_service(self)`

Remove the Windows service

#### `start_service(self)`

Start the service

#### `stop_service(self)`

Stop the service

#### `restart_service(self)`

Restart the service

#### `get_service_status(self)`

Get service status

#### `show_status(self)`

Display service status

#### `configure_service(self)`

Interactive service configuration

#### `_configure_startup_type(self)`

Configure service startup type

#### `_configure_recovery(self)`

Configure recovery actions

#### `_configure_environment(self)`

Configure environment variables

#### `_save_service_info(self)`

Save service installation information

#### `download_nssm(self)`

Download and install NSSM

---

## Functions

### `main()`

Main entry point

---
