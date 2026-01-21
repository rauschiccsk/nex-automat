"""Main Temporal Worker - Registers workflows and activities."""

import asyncio
import logging
import sys

from temporalio.client import Client
from temporalio.worker import Worker

from activities.email_activities import fetch_unread_emails, mark_email_processed
from activities.invoice_activities import upload_invoice_to_api, validate_pdf
from config.settings import get_settings
from workflows.pdf_invoice_workflow import InvoiceProcessingWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def run_worker():
    """Start the Temporal worker."""
    settings = get_settings()

    logger.info(f"Connecting to Temporal at {settings.temporal_address}...")

    client = await Client.connect(settings.temporal_address)

    logger.info(f"Starting worker on queue: {settings.temporal_task_queue}")

    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[InvoiceProcessingWorkflow],
        activities=[
            fetch_unread_emails,
            mark_email_processed,
            upload_invoice_to_api,
            validate_pdf,
        ],
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