#!/usr/bin/env python3
r"""
NEX Automat v2.0 - Fresh Deployment Script
Automates complete deployment from Git clone to running service.

Run from: C:\Deployment (or target deployment directory parent)
Usage: python deploy_fresh.py [--backup-path C:\path\to\backup]

Requirements:
- Python 3.13+ 32-bit installed
- Git installed
- PostgreSQL running
- NSSM available (C:\Tools\nssm or specified backup)
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
REPO_URL = "https://github.com/rauschiccsk/nex-automat.git"
SERVICE_NAME = "NEX-Automat-Loader"
PYTHON_VERSION = "3.13-32"


class DeploymentError(Exception):
    pass


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ", "OK": "[OK]", "FAIL": "[FAIL]", "WARN": "[!]", "STEP": ">>>"}
    print(f"[{ts}] {icons.get(level, '*')} {msg}")


def run_cmd(cmd, cwd=None, check=True, capture=False):
    """Run command and return result."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, shell=True, check=check,
            capture_output=capture, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            raise DeploymentError(f"Command failed: {cmd}\n{e.stderr if capture else ''}")
        return e


def check_prerequisites():
    """Check all prerequisites are met."""
    log("Checking prerequisites...", "STEP")

    # Check Python
    try:
        result = run_cmd(f"py -{PYTHON_VERSION} --version", capture=True)
        log(f"Python: {result.stdout.strip()}", "OK")
    except:
        raise DeploymentError(f"Python {PYTHON_VERSION} not found. Install Python 3.13 32-bit.")

    # Check Git
    try:
        result = run_cmd("git --version", capture=True)
        log(f"Git: {result.stdout.strip()}", "OK")
    except:
        raise DeploymentError("Git not found. Install Git.")

    # Check PostgreSQL
    try:
        run_cmd("pg_isready -h localhost -p 5432", capture=True)
        log("PostgreSQL: Running", "OK")
    except:
        log("PostgreSQL: Not running or pg_isready not in PATH", "WARN")

    # Check POSTGRES_PASSWORD
    if os.environ.get("POSTGRES_PASSWORD"):
        log("POSTGRES_PASSWORD: Set", "OK")
    else:
        log("POSTGRES_PASSWORD: Not set - will need to set before service start", "WARN")


def clone_repository(deploy_path: Path):
    """Clone repository from GitHub."""
    log(f"Cloning repository to {deploy_path}...", "STEP")

    if deploy_path.exists():
        raise DeploymentError(f"Directory already exists: {deploy_path}")

    run_cmd(f"git clone {REPO_URL} {deploy_path}")
    log("Repository cloned", "OK")


def create_venv(deploy_path: Path):
    """Create Python virtual environment."""
    log("Creating virtual environment...", "STEP")

    venv_path = deploy_path / "venv32"
    run_cmd(f"py -{PYTHON_VERSION} -m venv {venv_path}")
    log(f"Virtual environment created: {venv_path}", "OK")

    return venv_path


def install_dependencies(deploy_path: Path, venv_path: Path):
    """Install all Python dependencies."""
    log("Installing dependencies...", "STEP")

    pip = venv_path / "Scripts" / "pip.exe"

    # Main requirements
    req_file = deploy_path / "apps" / "supplier-invoice-loader" / "requirements.txt"
    if req_file.exists():
        run_cmd(f'"{pip}" install -r "{req_file}"')
        log("Main requirements installed", "OK")

    # Scripts requirements
    scripts_req = deploy_path / "scripts" / "requirements.txt"
    if scripts_req.exists():
        run_cmd(f'"{pip}" install -r "{scripts_req}"')
        log("Scripts requirements installed", "OK")

    # Additional packages (not in requirements.txt)
    additional = "fastapi uvicorn pdfplumber pg8000 pypdf Pillow httpx"
    run_cmd(f'"{pip}" install {additional}')
    log("Additional packages installed", "OK")

    # Local packages
    invoice_shared = deploy_path / "packages" / "invoice-shared"
    if invoice_shared.exists():
        run_cmd(f'"{pip}" install -e "{invoice_shared}"')
        log("invoice-shared package installed", "OK")


def create_directories(deploy_path: Path):
    """Create required directories."""
    log("Creating directories...", "STEP")

    dirs = ["logs", "backups", "test_results"]
    for d in dirs:
        (deploy_path / d).mkdir(exist_ok=True)

    log(f"Directories created: {', '.join(dirs)}", "OK")



def copy_from_templates(deploy_path: Path):
    """Copy configuration templates when no backup exists."""
    log("Copying from templates (clean installation)...", "STEP")

    config_dir = deploy_path / "apps" / "supplier-invoice-loader" / "config"

    templates = [
        ("config.yaml.template", "config.yaml"),
        ("config_customer.py.template", "config_customer.py"),
    ]

    for template_name, target_name in templates:
        template = config_dir / template_name
        target = config_dir / target_name

        if template.exists() and not target.exists():
            shutil.copy2(template, target)
            log(f"Created from template: {target_name}", "OK")
        elif target.exists():
            log(f"Already exists: {target_name}", "INFO")
        else:
            log(f"Template not found: {template_name}", "WARN")

    # Try to find NSSM
    nssm_dst = deploy_path / "tools" / "nssm"
    if not nssm_dst.exists():
        alt_nssm = Path(r"C:\Tools\nssm")
        if alt_nssm.exists():
            shutil.copytree(alt_nssm, nssm_dst)
            log(f"Copied NSSM from {alt_nssm}", "OK")
        else:
            log("NSSM not found - install manually to tools/nssm/", "WARN")

    log("", "WARN")
    log("IMPORTANT: Edit config files before starting service!", "WARN")
    log(f"  1. Edit: {config_dir / 'config.yaml'}", "WARN")
    log(f"  2. Edit: {config_dir / 'config_customer.py'}", "WARN")
    log("  3. Generate new security.encryption_key", "WARN")


def copy_from_backup(deploy_path: Path, backup_path: Path):
    """Copy configuration files from backup."""
    log(f"Copying files from backup: {backup_path}...", "STEP")

    files_to_copy = [
        ("apps/supplier-invoice-loader/config/config.yaml", True),
        ("apps/supplier-invoice-loader/config/config_customer.py", True),
    ]

    dirs_to_copy = [
        ("tools/nssm", True),
        ("apps/supplier-invoice-loader/tests/samples", False),
    ]

    # Copy files
    for rel_path, required in files_to_copy:
        src = backup_path / rel_path
        dst = deploy_path / rel_path

        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            log(f"Copied: {rel_path}", "OK")
        elif required:
            log(f"Missing required file: {rel_path}", "WARN")
        else:
            log(f"Optional file not found: {rel_path}", "INFO")

    # Copy directories
    for rel_path, required in dirs_to_copy:
        src = backup_path / rel_path
        dst = deploy_path / rel_path

        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            log(f"Copied directory: {rel_path}", "OK")
        elif required:
            # Try alternative NSSM location
            if "nssm" in rel_path:
                alt_nssm = Path(r"C:\Tools\nssm")
                if alt_nssm.exists():
                    shutil.copytree(alt_nssm, dst)
                    log(f"Copied NSSM from {alt_nssm}", "OK")
                else:
                    log(f"NSSM not found at {backup_path / rel_path} or {alt_nssm}", "WARN")
            else:
                log(f"Missing required directory: {rel_path}", "WARN")


def find_nssm(deploy_path: Path) -> Path:
    """Find NSSM executable."""
    locations = [
        deploy_path / "tools" / "nssm" / "win64" / "nssm.exe",
        deploy_path / "tools" / "nssm" / "win32" / "nssm.exe",
        Path(r"C:\Tools\nssm\win64\nssm.exe"),
        Path(r"C:\Tools\nssm\win32\nssm.exe"),
    ]

    for loc in locations:
        if loc.exists():
            return loc

    raise DeploymentError("NSSM not found. Install NSSM or copy to tools/nssm/")


def install_service(deploy_path: Path, venv_path: Path):
    """Install and configure Windows service."""
    log("Installing Windows service...", "STEP")

    nssm = find_nssm(deploy_path)
    python_exe = venv_path / "Scripts" / "python.exe"
    main_py = deploy_path / "apps" / "supplier-invoice-loader" / "main.py"

    # Remove existing service
    run_cmd(f'"{nssm}" stop {SERVICE_NAME}', check=False)
    run_cmd(f'"{nssm}" remove {SERVICE_NAME} confirm', check=False)

    # Install new service
    run_cmd(f'"{nssm}" install {SERVICE_NAME} "{python_exe}"')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} AppParameters "{main_py}"')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} AppDirectory "{deploy_path}"')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} AppStdout "{deploy_path}\\logs\\service-stdout.log"')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} AppStderr "{deploy_path}\\logs\\service-stderr.log"')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} AppRestartDelay 5000')
    run_cmd(f'"{nssm}" set {SERVICE_NAME} Start SERVICE_AUTO_START')

    # Set environment variables
    postgres_pw = os.environ.get("POSTGRES_PASSWORD", "")
    if postgres_pw:
        run_cmd(f'"{nssm}" set {SERVICE_NAME} AppEnvironmentExtra POSTGRES_PASSWORD={postgres_pw}')
        run_cmd(f'"{nssm}" set {SERVICE_NAME} AppEnvironmentExtra +PYTHONIOENCODING=utf-8')

    log(f"Service {SERVICE_NAME} installed", "OK")


def start_service(deploy_path: Path):
    """Start the Windows service."""
    log("Starting service...", "STEP")

    nssm = find_nssm(deploy_path)
    run_cmd(f'"{nssm}" start {SERVICE_NAME}')

    # Check status
    import time
    time.sleep(3)

    result = run_cmd(f'"{nssm}" status {SERVICE_NAME}', capture=True)
    status = result.stdout.replace('\x00', '').strip()

    if "SERVICE_RUNNING" in status:
        log(f"Service started: {status}", "OK")
    else:
        log(f"Service status: {status}", "WARN")
        log("Check logs\\service-stderr.log for errors", "WARN")


def run_validation(deploy_path: Path, venv_path: Path):
    """Run validation tests."""
    log("Running validation tests...", "STEP")

    python = venv_path / "Scripts" / "python.exe"

    # Preflight check
    preflight = deploy_path / "scripts" / "preflight_check.py"
    if preflight.exists():
        result = run_cmd(f'"{python}" "{preflight}"', cwd=deploy_path, check=False, capture=True)
        print(result.stdout)
        if "6/6 passed" in result.stdout:
            log("Preflight check: 6/6 PASS", "OK")
        else:
            log("Preflight check: Some checks failed", "WARN")


def print_summary(deploy_path: Path):
    """Print deployment summary."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"Location: {deploy_path}")
    print(f"Service: {SERVICE_NAME}")
    print()
    print("Next steps:")
    print("1. Verify service: python scripts\\manage_service.py status")
    print("2. Run tests: python scripts\\day5_error_handling_tests.py")
    print("3. Check logs: python scripts\\manage_service.py logs")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="NEX Automat Fresh Deployment")
    parser.add_argument("--target", "-t", default="nex-automat",
                        help="Target directory name (default: nex-automat)")
    parser.add_argument("--backup-path", "-b", type=Path,
                        help="Path to backup/existing deployment for config files")
    parser.add_argument("--skip-service", action="store_true",
                        help="Skip service installation")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip validation tests")

    args = parser.parse_args()

    # Determine paths
    base_path = Path.cwd()
    deploy_path = base_path / args.target
    backup_path = args.backup_path or base_path / f"{args.target}.backup"

    print("=" * 60)
    print("NEX AUTOMAT v2.0 - FRESH DEPLOYMENT")
    print("=" * 60)
    print(f"Target: {deploy_path}")
    print(f"Backup: {backup_path}")
    print("=" * 60)

    try:
        # Step 1: Prerequisites
        check_prerequisites()

        # Step 2: Clone
        clone_repository(deploy_path)

        # Step 3: Virtual environment
        venv_path = create_venv(deploy_path)

        # Step 4: Dependencies
        install_dependencies(deploy_path, venv_path)

        # Step 5: Directories
        create_directories(deploy_path)

        # Step 6: Copy from backup
        if backup_path.exists():
            copy_from_backup(deploy_path, backup_path)
        else:
            log(f"No backup found at {backup_path}", "WARN")
            copy_from_templates(deploy_path)

        # Step 7: Service
        if not args.skip_service:
            install_service(deploy_path, venv_path)
            start_service(deploy_path)

        # Step 8: Validation
        if not args.skip_validation:
            run_validation(deploy_path, venv_path)

        # Summary
        print_summary(deploy_path)

        return 0

    except DeploymentError as e:
        log(f"Deployment failed: {e}", "FAIL")
        return 1
    except Exception as e:
        log(f"Unexpected error: {e}", "FAIL")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())