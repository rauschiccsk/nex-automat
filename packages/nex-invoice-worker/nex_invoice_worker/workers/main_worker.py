"""Main Temporal Worker - Registers workflows and activities.

Tenant-aware: registers appropriate workflows and activities based on WORKER_TENANT.
"""

import asyncio
import logging
import sys

from nex_invoice_worker.config.settings import get_settings
from nex_invoice_worker.config.tenant import WorkerTenant, get_tenant

from nex_invoice_worker.activities.supplier_api_activities import (
    acknowledge_invoice_activity,
    archive_raw_data_activity,
    authenticate_supplier_activity,
    convert_to_isdoc_activity,
    convert_to_unified_activity,
    fetch_invoice_detail_activity,
    fetch_invoice_list_activity,
    fetch_supplier_config_activity,
    post_isdoc_to_pipeline_activity,
)
from nex_invoice_worker.workflows.api_invoice_workflow import (
    InvoiceAPIWorkflow,
    SingleInvoiceWorkflow,
)
from temporalio.client import Client
from temporalio.worker import Worker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _get_workflows(tenant: WorkerTenant) -> list:
    """Get workflow classes based on tenant."""
    workflows = [InvoiceAPIWorkflow, SingleInvoiceWorkflow]

    if tenant == WorkerTenant.SUPPLIER:
        from nex_invoice_worker.workflows.pdf_invoice_workflow import (
            InvoiceProcessingWorkflow,
        )

        workflows.append(InvoiceProcessingWorkflow)

    return workflows


def _get_activities(tenant: WorkerTenant) -> list:
    """Get activity functions based on tenant."""
    # Shared activities (all tenants)
    activities = [
        acknowledge_invoice_activity,
        archive_raw_data_activity,
        authenticate_supplier_activity,
        convert_to_isdoc_activity,
        convert_to_unified_activity,
        fetch_invoice_detail_activity,
        fetch_invoice_list_activity,
        fetch_supplier_config_activity,
        post_isdoc_to_pipeline_activity,
    ]

    if tenant == WorkerTenant.SUPPLIER:
        from nex_invoice_worker.activities.email_activities import (
            fetch_unread_emails,
            mark_email_processed,
        )
        from nex_invoice_worker.activities.invoice_activities import (
            upload_invoice_to_api,
            validate_pdf,
        )

        activities.extend(
            [
                fetch_unread_emails,
                mark_email_processed,
                upload_invoice_to_api,
                validate_pdf,
            ]
        )

    elif tenant == WorkerTenant.ANDROS:
        from nex_invoice_worker.activities.postgres_activities import (
            check_invoice_exists_activity,
            save_invoice_to_postgres_activity,
            update_invoice_status_activity,
        )

        activities.extend(
            [
                check_invoice_exists_activity,
                save_invoice_to_postgres_activity,
                update_invoice_status_activity,
            ]
        )

    return activities


async def run_worker():
    """Start the Temporal worker."""
    settings = get_settings()
    tenant = get_tenant()

    logger.info(f"Worker tenant: {tenant.value}")
    logger.info(f"Connecting to Temporal at {settings.temporal_address}...")

    client = await Client.connect(settings.temporal_address)

    workflows = _get_workflows(tenant)
    activities = _get_activities(tenant)

    logger.info(f"Starting worker on queue: {settings.temporal_task_queue}")
    logger.info(f"Workflows: {[w.__name__ for w in workflows]}")
    logger.info(f"Activities: {len(activities)} registered")

    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=workflows,
        activities=activities,
    )

    logger.info("Worker started. Press Ctrl+C to stop.")
    await worker.run()


def main():
    """Entry point for the worker."""
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Worker failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
