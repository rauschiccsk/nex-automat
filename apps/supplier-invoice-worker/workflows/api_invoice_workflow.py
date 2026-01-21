"""API Invoice Workflow - Temporal workflow for supplier API integration.

This workflow handles fetching and processing invoices from supplier APIs
(MARSO, CONTINENTAL, etc.) as opposed to pdf_invoice_workflow which handles
email-based PDF invoices.
"""

from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.supplier_api_activities import (
        acknowledge_invoice,
        archive_raw_xml,
        fetch_invoice_xml,
        fetch_pending_invoices,
        load_supplier_config,
        parse_invoice_xml,
    )
    # TODO: Import shared activities after implementation
    # from activities.invoice_activities import (
    #     match_products,
    #     save_to_staging,
    #     import_to_nex_genesis,
    # )


@dataclass
class ApiWorkflowInput:
    """Input parameters for API invoice workflow."""

    supplier_id: str  # e.g., "marso", "continental"


@dataclass
class ApiWorkflowResult:
    """Result of API invoice processing workflow."""

    supplier_id: str
    invoices_fetched: int
    invoices_processed: int
    invoices_acknowledged: int
    errors: list[str]


@workflow.defn
class ApiInvoiceWorkflow:
    """
    Workflow for processing supplier invoices from API.

    Flow:
    1. Load supplier config (YAML)
    2. Authenticate with supplier API
    3. Fetch list of pending invoices
    4. For each invoice:
       a) Fetch XML from API
       b) Archive raw XML (filesystem + PostgreSQL)
       c) Parse XML → UnifiedInvoice
       d) Match products (SHARED activity)
       e) Save to staging (SHARED activity)
       f) Acknowledge to supplier API
    5. Trigger NEX Genesis import (SHARED activity)
    """

    @workflow.run
    async def run(self, input: ApiWorkflowInput) -> ApiWorkflowResult:
        """Execute the API invoice processing workflow."""
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            backoff_coefficient=2.0,
            maximum_attempts=3,
            maximum_interval=timedelta(minutes=1),
        )

        errors: list[str] = []
        invoices_fetched = 0
        invoices_processed = 0
        invoices_acknowledged = 0

        workflow.logger.info(f"Starting API workflow for supplier: {input.supplier_id}")

        # Step 1: Load supplier configuration
        workflow.logger.info("Loading supplier configuration...")
        try:
            config = await workflow.execute_activity(
                load_supplier_config,
                args=[input.supplier_id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
        except Exception as e:
            errors.append(f"Failed to load config: {e}")
            return ApiWorkflowResult(
                supplier_id=input.supplier_id,
                invoices_fetched=0,
                invoices_processed=0,
                invoices_acknowledged=0,
                errors=errors,
            )

        # Step 2: Fetch list of pending invoices
        workflow.logger.info("Fetching pending invoices...")
        invoice_ids: list[str] = await workflow.execute_activity(
            fetch_pending_invoices,
            args=[input.supplier_id],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy,
        )

        if not invoice_ids:
            workflow.logger.info("No pending invoices found")
            return ApiWorkflowResult(
                supplier_id=input.supplier_id,
                invoices_fetched=0,
                invoices_processed=0,
                invoices_acknowledged=0,
                errors=[],
            )

        workflow.logger.info(f"Found {len(invoice_ids)} pending invoices")

        # Step 3: Process each invoice
        for invoice_id in invoice_ids:
            workflow.logger.info(f"Processing invoice: {invoice_id}")

            try:
                # Step 3a: Fetch XML
                xml_content = await workflow.execute_activity(
                    fetch_invoice_xml,
                    args=[input.supplier_id, invoice_id],
                    start_to_close_timeout=timedelta(minutes=1),
                    retry_policy=retry_policy,
                )
                invoices_fetched += 1

                # Step 3b: Archive raw XML
                archive_path = await workflow.execute_activity(
                    archive_raw_xml,
                    args=[input.supplier_id, invoice_id, xml_content],
                    start_to_close_timeout=timedelta(seconds=30),
                    retry_policy=retry_policy,
                )
                workflow.logger.info(f"Archived to: {archive_path}")

                # Step 3c: Parse XML to UnifiedInvoice
                invoice_data = await workflow.execute_activity(
                    parse_invoice_xml,
                    args=[input.supplier_id, xml_content],
                    start_to_close_timeout=timedelta(seconds=30),
                )

                # TODO: Step 3d: Match products (SHARED activity)
                # invoice_data = await workflow.execute_activity(
                #     match_products,
                #     args=[invoice_data],
                #     start_to_close_timeout=timedelta(minutes=1),
                #     retry_policy=retry_policy,
                # )

                # TODO: Step 3e: Save to staging (SHARED activity)
                # staging_id = await workflow.execute_activity(
                #     save_to_staging,
                #     args=[invoice_data],
                #     start_to_close_timeout=timedelta(seconds=30),
                #     retry_policy=retry_policy,
                # )

                invoices_processed += 1

                # Step 3f: Acknowledge to supplier
                ack_success = await workflow.execute_activity(
                    acknowledge_invoice,
                    args=[input.supplier_id, invoice_id],
                    start_to_close_timeout=timedelta(seconds=30),
                    retry_policy=retry_policy,
                )

                if ack_success:
                    invoices_acknowledged += 1
                else:
                    errors.append(f"Failed to acknowledge: {invoice_id}")

            except Exception as e:
                error_msg = f"Error processing {invoice_id}: {e}"
                workflow.logger.error(error_msg)
                errors.append(error_msg)

        # TODO: Step 4: Trigger NEX Genesis import
        # if invoices_processed > 0:
        #     await workflow.execute_activity(
        #         import_to_nex_genesis,
        #         args=[staging_ids],
        #         start_to_close_timeout=timedelta(minutes=5),
        #         retry_policy=retry_policy,
        #     )

        workflow.logger.info(
            f"Workflow complete: {invoices_fetched} fetched, "
            f"{invoices_processed} processed, "
            f"{invoices_acknowledged} acknowledged, "
            f"{len(errors)} errors"
        )

        return ApiWorkflowResult(
            supplier_id=input.supplier_id,
            invoices_fetched=invoices_fetched,
            invoices_processed=invoices_processed,
            invoices_acknowledged=invoices_acknowledged,
            errors=errors,
        )
