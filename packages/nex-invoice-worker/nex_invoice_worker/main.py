"""Entry point for the shared invoice worker.

Runs the Temporal worker with tenant-specific configuration.
Usage:
    WORKER_TENANT=supplier python -m nex_invoice_worker.main
    WORKER_TENANT=andros python -m nex_invoice_worker.main
"""

from nex_invoice_worker.workers.main_worker import main

if __name__ == "__main__":
    main()
