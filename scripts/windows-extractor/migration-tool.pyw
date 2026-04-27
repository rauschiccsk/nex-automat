"""
NEX Migration Tool — one-click GUI for per-customer Btrieve → PostgreSQL migration.

Pipeline per click:
  1. Run extract via run_extract.py (subprocess, uses venv32 python) → JSON
  2. SCP JSON to ANDROS per-customer migration drop dir (paramiko)
  3. POST /api/auth/login → JWT (requests)
  4. POST /api/migration/run with JWT → result
  5. Display in UI log

Config: migration-config.json (in same dir as this script)
Credentials: prompted on first migration of session, cached in memory only.

Run: double-click migration-tool.pyw (or python migration-tool.pyw)
Setup: pip install -r requirements.txt (paramiko + requests added)
"""

import json
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from tkinter import (
    END,
    Button,
    Frame,
    Label,
    Scrollbar,
    Text,
    Tk,
    messagebox,
    simpledialog,
)

try:
    import paramiko
    import requests
except ImportError as e:
    raise SystemExit(
        f"Missing dependency: {e.name}. Activate venv32 and "
        "run: pip install -r requirements.txt"
    )


SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "migration-config.json"
RUN_EXTRACT_PATH = (
    SCRIPT_DIR / ".." / ".." / "apps" / "nex-migration" / "run_extract.py"
).resolve()
VENV_PYTHON = SCRIPT_DIR / "venv32" / "Scripts" / "python.exe"
OUTPUT_BASE = SCRIPT_DIR / "output"


class MigrationApp:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("NEX Migration Tool")
        self.root.geometry("760x560")

        # In-memory credential cache (cleared when window closes)
        self.ssh_password: str | None = None
        # {slug: {"user": str, "jwt": str}}
        self.admin_creds: dict[str, dict[str, str]] = {}

        self.config = self._load_config()
        self.buttons: list[Button] = []
        self._build_ui()

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    def _load_config(self) -> dict:
        if not CONFIG_PATH.exists():
            messagebox.showerror("Error", f"Config missing: {CONFIG_PATH}")
            sys.exit(1)
        with CONFIG_PATH.open(encoding="utf-8") as f:
            return json.load(f)

    def _build_ui(self) -> None:
        # Header
        header = Frame(self.root, padx=12, pady=10)
        header.pack(fill="x")
        Label(
            header,
            text="NEX Migration Tool",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        Label(
            header,
            text="One-click PAB migration: extract Btrieve → SCP → load PostgreSQL",
            font=("Segoe UI", 9),
            fg="#555",
        ).pack(anchor="w")

        # Customer buttons
        btn_frame = Frame(self.root, padx=12, pady=4)
        btn_frame.pack(fill="x")

        for slug, info in self.config["customers"].items():
            btn = Button(
                btn_frame,
                text=f"  Migrate {info['name']}  ({slug})  ",
                width=42,
                height=2,
                font=("Segoe UI", 10),
                command=lambda s=slug: self._on_migrate(s),
            )
            btn.pack(pady=4, anchor="w")
            self.buttons.append(btn)

        # Log area
        log_frame = Frame(self.root, padx=12, pady=10)
        log_frame.pack(fill="both", expand=True)
        Label(log_frame, text="Log:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        log_inner = Frame(log_frame)
        log_inner.pack(fill="both", expand=True)
        self.log = Text(log_inner, wrap="word", font=("Consolas", 9), bg="#1e1e1e", fg="#dcdcdc")
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(log_inner, command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.config(yscrollcommand=scrollbar.set)
        # Tags for colored output
        self.log.tag_config("step", foreground="#569cd6")
        self.log.tag_config("ok", foreground="#6a9955")
        self.log.tag_config("err", foreground="#f48771")
        self.log.tag_config("dim", foreground="#888")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _log(self, msg: str, level: str = "info") -> None:
        prefix = {"info": "  ", "ok": "✓ ", "err": "✗ ", "step": "→ ", "dim": "  "}.get(
            level, "  "
        )
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {prefix}{msg}\n"
        self.log.insert(END, line, level if level != "info" else "")
        self.log.see(END)
        self.root.update_idletasks()

    # ------------------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------------------

    def _on_migrate(self, slug: str) -> None:
        # Collect all credentials in main thread BEFORE dispatching worker
        # (tkinter dialogs MUST run on main thread — calling simpledialog from
        # a worker thread fails with "window was deleted before its visibility
        # changed").
        info = self.config["customers"][slug]
        andros = self.config["andros"]

        if self.ssh_password is None:
            pw = simpledialog.askstring(
                "ANDROS SSH password",
                f"Password for {andros['user']}@{andros['host']}",
                show="*",
                parent=self.root,
            )
            if not pw:
                self._log("Cancelled — SSH password required", "err")
                return
            self.ssh_password = pw

        if slug not in self.admin_creds or not self.admin_creds[slug].get("jwt"):
            username = simpledialog.askstring(
                f"Admin login — {info['name']}",
                f"Username for {info['url']}:",
                initialvalue="admin",
                parent=self.root,
            )
            if not username:
                self._log("Cancelled — admin username required", "err")
                return
            password = simpledialog.askstring(
                f"Admin login — {info['name']}",
                f"Password for {username}@{info['url']}:",
                show="*",
                parent=self.root,
            )
            if not password:
                self._log("Cancelled — admin password required", "err")
                return
            # Store password (used by worker to obtain JWT). JWT is set after
            # successful login API call inside the worker.
            self.admin_creds[slug] = {
                "user": username,
                "password": password,
                "jwt": None,
            }

        # Disable all buttons during run
        for b in self.buttons:
            b.config(state="disabled")
        threading.Thread(
            target=self._run_pipeline_safe, args=(slug,), daemon=True
        ).start()

    def _run_pipeline_safe(self, slug: str) -> None:
        try:
            self._run_pipeline(slug)
        finally:
            self.root.after(0, lambda: [b.config(state="normal") for b in self.buttons])

    def _run_pipeline(self, slug: str) -> None:
        info = self.config["customers"][slug]
        self._log("=" * 70, "dim")
        self._log(f"Migrating {info['name']} ({slug})", "step")

        # 1. Extract
        try:
            self._log(f"[1/4] Extract PAB from {info['data_root']}", "step")
            json_path = self._run_extract(slug, info)
            self._log(f"  output: {json_path}", "ok")
        except Exception as e:
            self._log(f"Extract failed: {e}", "err")
            return

        # 2. Transfer
        try:
            self._log(
                f"[2/4] Transfer to {self.config['andros']['user']}@"
                f"{self.config['andros']['host']}:{info['remote_drop_dir']}/PAB/",
                "step",
            )
            self._scp_transfer(json_path, slug, info)
            self._log("  upload complete", "ok")
        except Exception as e:
            self._log(f"Transfer failed: {e}", "err")
            return

        # 3. Auth
        try:
            self._log(f"[3/4] Authenticate to {info['url']}", "step")
            jwt = self._get_jwt(slug, info)
            self._log("  JWT acquired", "ok")
        except Exception as e:
            self._log(f"Auth failed: {e}", "err")
            return

        # 4. Trigger migration
        try:
            self._log("[4/4] Run migration via API", "step")
            result = self._trigger_migration(info["url"], jwt)
            self._log(f"  status: {result.get('status')}", "ok")
            inserted = result.get("target_count", 0)
            errors = result.get("error_count", 0)
            self._log(
                f"  source={result.get('source_count', 0)} "
                f"target={inserted} errors={errors}",
                "ok",
            )
            self._log(f"  message: {result.get('message', '-')}", "ok")
            if errors == 0:
                self._log(f"DONE — {info['name']} migrated successfully", "ok")
            else:
                self._log(
                    f"COMPLETED WITH ERRORS — {errors} records failed", "err"
                )
        except Exception as e:
            self._log(f"Migration trigger failed: {e}", "err")
            return

    # ------------------------------------------------------------------
    # Step implementations
    # ------------------------------------------------------------------

    def _run_extract(self, slug: str, info: dict) -> Path:
        if not VENV_PYTHON.exists():
            raise RuntimeError(
                f"venv32 python not found at {VENV_PYTHON}. Run install.bat first."
            )
        if not RUN_EXTRACT_PATH.exists():
            raise RuntimeError(f"run_extract.py not found at {RUN_EXTRACT_PATH}")

        output_dir = OUTPUT_BASE / f"output-{slug}"
        cmd = [
            str(VENV_PYTHON),
            str(RUN_EXTRACT_PATH),
            "--category",
            "PAB",
            "--data-root",
            info["data_root"],
            "--data-dir",
            str(output_dir),
        ]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, encoding="utf-8"
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"Extract exit {proc.returncode}\n"
                f"stdout: {proc.stdout[-500:]}\n"
                f"stderr: {proc.stderr[-500:]}"
            )
        for line in (proc.stdout or "").strip().splitlines()[-3:]:
            self._log(f"    {line}", "dim")
        json_path = output_dir / "PAB" / "PAB.json"
        if not json_path.exists():
            raise RuntimeError(f"Extract did not produce {json_path}")
        return json_path

    def _scp_transfer(self, local_path: Path, slug: str, info: dict) -> None:
        andros = self.config["andros"]
        # Password was prompted + cached in main thread (_on_migrate)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                andros["host"],
                username=andros["user"],
                password=self.ssh_password,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
            )
        except paramiko.AuthenticationException:
            self.ssh_password = None  # invalidate cache → fresh prompt next click
            raise RuntimeError("SSH password rejected — click again to re-enter")

        remote_dir = f"{info['remote_drop_dir']}/PAB"
        ssh.exec_command(f"mkdir -p {remote_dir}")[1].channel.recv_exit_status()

        remote_path = f"{remote_dir}/PAB.json"
        sftp = ssh.open_sftp()
        try:
            sftp.put(str(local_path), remote_path)
        finally:
            sftp.close()
            ssh.close()

    def _get_jwt(self, slug: str, info: dict) -> str:
        cached = self.admin_creds.get(slug)
        if cached and cached.get("jwt"):
            return cached["jwt"]

        # User + password were prompted + cached in main thread (_on_migrate);
        # we just exchange them for a JWT via the auth API.
        if not cached:
            raise RuntimeError("Admin credentials missing — should be set by main thread")

        username = cached["user"]
        password = cached.get("password")
        if not password:
            raise RuntimeError("Admin password missing from cache")

        try:
            resp = requests.post(
                f"{info['url']}/api/auth/login",
                json={"username": username, "password": password},
                timeout=15,
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Network error: {e}")

        if resp.status_code != 200:
            # Invalidate cached creds so user gets fresh prompt next click
            self.admin_creds.pop(slug, None)
            raise RuntimeError(
                f"Login HTTP {resp.status_code}: {resp.text[:200]}"
            )

        data = resp.json()
        jwt = data.get("access_token") or data.get("token")
        if not jwt:
            raise RuntimeError(f"No access_token in login response: {data}")

        # Replace plaintext password with JWT (smaller surface area in memory)
        self.admin_creds[slug] = {"user": username, "jwt": jwt}
        return jwt

    def _trigger_migration(self, url: str, jwt: str) -> dict:
        try:
            resp = requests.post(
                f"{url}/api/migration/run",
                json={"category": "PAB", "dry_run": False},
                headers={"Authorization": f"Bearer {jwt}"},
                timeout=300,
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Network error: {e}")

        if resp.status_code != 200:
            raise RuntimeError(
                f"Migration HTTP {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()


def main() -> None:
    root = Tk()
    MigrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
