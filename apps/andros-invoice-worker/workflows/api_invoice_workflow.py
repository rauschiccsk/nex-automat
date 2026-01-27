"""
Temporal Workflow for ANDROS Supplier API Invoice processing.

Orchestrates fetching invoices from supplier APIs, converting to ISDOC,
saving to PostgreSQL, and posting to the invoice processing pipeline.
"""

from datetime import timedelta
from typing import Any, Dict, List

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
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


@workflow.defn
class ANDROSInvoiceWorkflow:
    """
    Workflow for processing ANDROS invoices from supplier APIs.

    Flow:
    1. Load supplier configuration
    2. Authenticate with supplier API
    3. Fetch list of invoices for date range
    4. For each invoice:
       - Check if already exists in DB
       - Fetch invoice details
       - Convert to UnifiedInvoice format
       - Save to PostgreSQL (supplier_invoice_heads + supplier_invoice_items)
       - Convert to ISDOC XML
       - Archive raw data and XML
       - Post to invoice pipeline (optional)
       - Acknowledge to supplier
    """

    @workflow.run
    async def run(
        self,
        supplier_id: str,
        date_from: str,
        date_to: str,
        customer_code: str = "ANDROS",
        skip_pipeline: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute ANDROS invoice processing workflow.

        Args:
            supplier_id: Supplier identifier (e.g., "marso")
            date_from: Start date (ISO format: YYYY-MM-DD)
            date_to: End date (ISO format: YYYY-MM-DD)
            customer_code: Customer code (default: "ANDROS")
            skip_pipeline: If True, skip posting to invoice pipeline

        Returns:
            Summary of processed invoices
        """
        workflow.logger.info(
            f"Starting ANDROS invoice workflow for {supplier_id}: {date_from} to {date_to}"
        )

        # Retry policy for activities
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(minutes=1),
            maximum_attempts=3,
        )

        # Activity options
        activity_options = {
            "start_to_close_timeout": timedelta(minutes=5),
            "retry_policy": retry_policy,
        }

        results = {
            "supplier_id": supplier_id,
            "customer_code": customer_code,
            "date_from": date_from,
            "date_to": date_to,
            "total_invoices": 0,
            "processed": 0,
            "skipped": 0,
            "failed": 0,
            "saved_to_db": 0,
            "errors": [],
        }

        try:
            # Step 1: Load configuration
            config = await workflow.execute_activity(
                fetch_supplier_config_activity,
                supplier_id,
                **activity_options,
            )
            workflow.logger.info(f"Config loaded for {config['supplier_name']}")

            # Step 2: Authenticate
            auth_success = await workflow.execute_activity(
                authenticate_supplier_activity,
                supplier_id,
                **activity_options,
            )
            if not auth_success:
                raise RuntimeError(f"Authentication failed for {supplier_id}")

            # Step 3: Fetch invoice list
            invoices = await workflow.execute_activity(
                fetch_invoice_list_activity,
                args=[supplier_id, date_from, date_to],
                **activity_options,
            )
            results["total_invoices"] = len(invoices)
            workflow.logger.info(f"Found {len(invoices)} invoices to process")

            if not invoices:
                workflow.logger.info("No invoices to process")
                return results

            # Step 4: Process each invoice
            for invoice in invoices:
                invoice_id = invoice.get("InvoiceId", "unknown")
                try:
                    saved = await self._process_single_invoice(
                        supplier_id,
                        invoice_id,
                        invoice,
                        customer_code,
                        skip_pipeline,
                        activity_options,
                    )
                    if saved:
                        results["processed"] += 1
                        results["saved_to_db"] += 1
                    else:
                        results["skipped"] += 1
                except Exception as e:
                    workflow.logger.error(f"Failed to process invoice {invoice_id}: {e}")
                    results["failed"] += 1
                    results["errors"].append({
                        "invoice_id": invoice_id,
                        "error": str(e),
                    })

        except Exception as e:
            workflow.logger.error(f"Workflow failed: {e}")
            results["errors"].append({"workflow_error": str(e)})
            raise

        workflow.logger.info(
            f"Workflow complete: {results['processed']}/{results['total_invoices']} processed, "
            f"{results['skipped']} skipped, {results['saved_to_db']} saved to DB"
        )
        return results

    async def _process_single_invoice(
        self,
        supplier_id: str,
        invoice_id: str,
        invoice_data: Dict[str, Any],
        customer_code: str,
        skip_pipeline: bool,
        activity_options: Dict[str, Any],
    ) -> bool:
        """
        Process a single invoice through the pipeline.

        Returns:
            True if invoice was processed and saved, False if skipped (already exists)
        """
        workflow.logger.info(f"Processing invoice: {invoice_id}")

        # Check if invoice already exists
        invoice_number = invoice_data.get("InvoiceId", invoice_id)
        exists = await workflow.execute_activity(
            check_invoice_exists_activity,
            args=[invoice_number, supplier_id.upper(), customer_code],
            **activity_options,
        )

        if exists:
            workflow.logger.info(f"Invoice {invoice_id} already exists, skipping")
            return False

        # Fetch full details if needed
        if "Lines" not in invoice_data or not invoice_data["Lines"]:
            invoice_data = await workflow.execute_activity(
                fetch_invoice_detail_activity,
                args=[supplier_id, invoice_id],
                **activity_options,
            )

        # Convert to UnifiedInvoice format
        unified_data = await workflow.execute_activity(
            convert_to_unified_activity,
            args=[supplier_id, invoice_data],
            **activity_options,
        )

        # Save to PostgreSQL (customer_code='ANDROS', supplier_code='MARSO')
        db_result = await workflow.execute_activity(
            save_invoice_to_postgres_activity,
            args=[unified_data, supplier_id, customer_code],
            **activity_options,
        )
        workflow.logger.info(
            f"Invoice {invoice_id} saved to DB: head_id={db_result['head_id']}"
        )

        # Convert to ISDOC XML
        isdoc_xml = await workflow.execute_activity(
            convert_to_isdoc_activity,
            args=[supplier_id, invoice_data],
            **activity_options,
        )

        # Archive raw data and XML
        await workflow.execute_activity(
            archive_raw_data_activity,
            args=[supplier_id, invoice_id, invoice_data, isdoc_xml],
            **activity_options,
        )

        # Post to pipeline (optional)
        if not skip_pipeline:
            await workflow.execute_activity(
                post_isdoc_to_pipeline_activity,
                args=[isdoc_xml, invoice_id, supplier_id],
                **activity_options,
            )

        # Update status in DB
        await workflow.execute_activity(
            update_invoice_status_activity,
            args=[db_result["head_id"], "processed"],
            **activity_options,
        )

        # Acknowledge to supplier
        await workflow.execute_activity(
            acknowledge_invoice_activity,
            args=[supplier_id, invoice_id],
            **activity_options,
        )

        workflow.logger.info(f"Invoice {invoice_id} processed successfully")
        return True


# Backwards-compatible alias
SupplierAPIInvoiceWorkflow = ANDROSInvoiceWorkflow


@workflow.defn
class SingleInvoiceWorkflow:
    """
    Workflow for processing a single invoice by ID.

    Useful for reprocessing failed invoices or manual triggers.
    """

    @workflow.run
    async def run(
        self,
        supplier_id: str,
        invoice_id: str,
        customer_code: str = "ANDROS",
    ) -> Dict[str, Any]:
        """
        Process single invoice.

        Args:
            supplier_id: Supplier identifier
            invoice_id: Invoice ID to process
            customer_code: Customer code (default: "ANDROS")

        Returns:
            Processing result
        """
        workflow.logger.info(f"Processing single invoice: {invoice_id} from {supplier_id}")

        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )
        activity_options = {
            "start_to_close_timeout": timedelta(minutes=5),
            "retry_policy": retry_policy,
        }

        # Authenticate
        await workflow.execute_activity(
            authenticate_supplier_activity,
            supplier_id,
            **activity_options,
        )

        # Fetch invoice
        invoice_data = await workflow.execute_activity(
            fetch_invoice_detail_activity,
            args=[supplier_id, invoice_id],
            **activity_options,
        )

        # Convert to unified format
        unified_data = await workflow.execute_activity(
            convert_to_unified_activity,
            args=[supplier_id, invoice_data],
            **activity_options,
        )

        # Save to PostgreSQL
        db_result = await workflow.execute_activity(
            save_invoice_to_postgres_activity,
            args=[unified_data, supplier_id, customer_code],
            **activity_options,
        )

        # Convert to ISDOC
        isdoc_xml = await workflow.execute_activity(
            convert_to_isdoc_activity,
            args=[supplier_id, invoice_data],
            **activity_options,
        )

        # Archive
        archive_path = await workflow.execute_activity(
            archive_raw_data_activity,
            args=[supplier_id, invoice_id, invoice_data, isdoc_xml],
            **activity_options,
        )

        # Update status
        await workflow.execute_activity(
            update_invoice_status_activity,
            args=[db_result["head_id"], "processed"],
            **activity_options,
        )

        # Acknowledge
        await workflow.execute_activity(
            acknowledge_invoice_activity,
            args=[supplier_id, invoice_id],
            **activity_options,
        )

        return {
            "invoice_id": invoice_id,
            "status": "success",
            "head_id": db_result["head_id"],
            "archive_path": archive_path,
            "customer_code": customer_code,
            "supplier_code": supplier_id.upper(),
        }
