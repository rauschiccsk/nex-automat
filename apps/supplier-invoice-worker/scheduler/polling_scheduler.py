"""Polling Scheduler - Triggers invoice workflow on schedule."""

import asyncio
import logging
import sys
from datetime import datetime
from uuid import uuid4

from temporalio.client import Client

from config.settings import get_settings
from workflows.pdf_invoice_workflow import InvoiceProcessingWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Polling interval in seconds (default: 5 minutes)
POLL_INTERVAL_SECONDS = 300


async def trigger_workflow(client: Client, task_queue: str) -> None:
    """Trigger a single workflow execution."""
    workflow_id = f"invoice-processing-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"

    logger.info(f"Starting workflow: {workflow_id}")

    result = await client.execute_workflow(
        InvoiceProcessingWorkflow.run,
        id=workflow_id,
        task_queue=task_queue,
    )

    logger.info(
        f"Workflow complete: {result.emails_processed} emails, "
        f"{result.invoices_uploaded} invoices, {len(result.errors)} errors"
    )

    if result.errors:
        for error in result.errors:
            logger.warning(f"  Error: {error}")


async def run_scheduler():
    """Run the polling scheduler."""
    settings = get_settings()

    logger.info(f"Connecting to Temporal at {settings.temporal_address}...")
    client = await Client.connect(settings.temporal_address)

    logger.info(f"Scheduler started. Polling every {POLL_INTERVAL_SECONDS}s")
    logger.info("Press Ctrl+C to stop.")

    while True:
        try:
            await trigger_workflow(client, settings.temporal_task_queue)
        except Exception as e:
            logger.error(f"Workflow failed: {e}")

        logger.info(f"Next poll in {POLL_INTERVAL_SECONDS}s...")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def run_once():
    """Run workflow once (for testing)."""
    settings = get_settings()

    logger.info(f"Connecting to Temporal at {settings.temporal_address}...")
    client = await Client.connect(settings.temporal_address)

    await trigger_workflow(client, settings.temporal_task_queue)


def main():
    """Entry point."""
    try:
        if "--once" in sys.argv:
            logger.info("Running single workflow execution...")
            asyncio.run(run_once())
        else:
            asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()