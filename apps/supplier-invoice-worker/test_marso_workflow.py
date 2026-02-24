"""Test script for MARSO API workflow."""

import asyncio
import logging
from datetime import date, datetime, timedelta
from uuid import uuid4

from config.settings import get_settings
from temporalio.client import Client
from workflows.api_invoice_workflow import SupplierAPIInvoiceWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def test_marso_workflow():
    """Test MARSO supplier API workflow."""
    settings = get_settings()

    logger.info(f"Connecting to Temporal at {settings.temporal_address}...")
    client = await Client.connect(settings.temporal_address)

    # Test date range: last 7 days
    date_to = date.today()
    date_from = date_to - timedelta(days=7)

    workflow_id = (
        f"marso-api-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"
    )

    logger.info(f"Starting MARSO workflow: {workflow_id}")
    logger.info(f"Date range: {date_from.isoformat()} to {date_to.isoformat()}")

    try:
        result = await client.execute_workflow(
            SupplierAPIInvoiceWorkflow.run,
            args=["marso", date_from.isoformat(), date_to.isoformat()],
            id=workflow_id,
            task_queue=settings.temporal_task_queue,
        )

        logger.info("=" * 60)
        logger.info("WORKFLOW COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Supplier: {result['supplier_id']}")
        logger.info(f"Date range: {result['date_from']} to {result['date_to']}")
        logger.info(f"Total invoices found: {result['total_invoices']}")
        logger.info(f"Successfully processed: {result['processed']}")
        logger.info(f"Failed: {result['failed']}")

        if result["errors"]:
            logger.warning(f"Errors encountered: {len(result['errors'])}")
            for error in result["errors"]:
                logger.warning(f"  - {error}")

        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        raise


def main():
    """Entry point."""
    try:
        asyncio.run(test_marso_workflow())
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
