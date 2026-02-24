"""
ANDROS Invoice Worker - Main Temporal Worker.

Runs Temporal worker for processing MARSO invoices.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from activities.postgres_activities import (
    check_invoice_exists_activity,
    save_invoice_to_postgres_activity,
    update_invoice_status_activity,
)
from activities.supplier_api_activities import (
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
from config.settings import get_settings
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.api_invoice_workflow import ANDROSInvoiceWorkflow, SingleInvoiceWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Run the Temporal worker."""
    settings = get_settings()

    logger.info(f"Connecting to Temporal at {settings.temporal_address}")
    client = await Client.connect(settings.temporal_address)

    # Create worker with all activities and workflows
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[
            ANDROSInvoiceWorkflow,
            SingleInvoiceWorkflow,
        ],
        activities=[
            # Supplier API activities
            fetch_supplier_config_activity,
            authenticate_supplier_activity,
            fetch_invoice_list_activity,
            fetch_invoice_detail_activity,
            convert_to_unified_activity,
            convert_to_isdoc_activity,
            acknowledge_invoice_activity,
            archive_raw_data_activity,
            post_isdoc_to_pipeline_activity,
            # PostgreSQL activities
            save_invoice_to_postgres_activity,
            check_invoice_exists_activity,
            update_invoice_status_activity,
        ],
    )

    logger.info(
        f"Starting ANDROS Invoice Worker on queue: {settings.temporal_task_queue}"
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
