"""Invoice Processing Workflow - Main Temporal workflow."""

from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.email_activities import (
        EmailMessage,
        fetch_unread_emails,
        mark_email_processed,
    )
    from activities.invoice_activities import (
        UploadResult,
        upload_invoice_to_api,
        validate_pdf,
    )


@dataclass
class WorkflowResult:
    """Result of invoice processing workflow."""

    emails_processed: int
    invoices_uploaded: int
    errors: list[str]


@workflow.defn
class InvoiceProcessingWorkflow:
    """
    Workflow for processing supplier invoices from email.

    Flow:
    1. Fetch unread emails from IMAP
    2. Extract PDF attachments
    3. Validate PDFs
    4. Upload to FastAPI
    5. Mark emails as processed
    """

    @workflow.run
    async def run(self) -> WorkflowResult:
        """Execute the invoice processing workflow."""
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            backoff_coefficient=2.0,
            maximum_attempts=3,
            maximum_interval=timedelta(minutes=1),
        )

        errors: list[str] = []
        invoices_uploaded = 0

        # Step 1: Fetch unread emails
        workflow.logger.info("Fetching unread emails...")
        emails: list[EmailMessage] = await workflow.execute_activity(
            fetch_unread_emails,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy,
        )

        if not emails:
            workflow.logger.info("No unread emails with PDF attachments")
            return WorkflowResult(emails_processed=0, invoices_uploaded=0, errors=[])

        workflow.logger.info(f"Processing {len(emails)} emails...")

        # Step 2-5: Process each email
        for email_msg in emails:
            workflow.logger.info(f"Processing email: {email_msg.subject}")

            for attachment in email_msg.attachments:
                # Step 3: Validate PDF
                is_valid = await workflow.execute_activity(
                    validate_pdf,
                    args=[attachment.content],
                    start_to_close_timeout=timedelta(seconds=30),
                )

                if not is_valid:
                    errors.append(f"Invalid PDF: {attachment.filename}")
                    continue

                # Step 4: Upload to FastAPI
                result: UploadResult = await workflow.execute_activity(
                    upload_invoice_to_api,
                    args=[attachment.filename, attachment.content],
                    start_to_close_timeout=timedelta(minutes=1),
                    retry_policy=retry_policy,
                )

                if result.success:
                    invoices_uploaded += 1
                else:
                    errors.append(f"{attachment.filename}: {result.message}")

            # Step 5: Mark email as processed
            await workflow.execute_activity(
                mark_email_processed,
                args=[email_msg.uid],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )

        workflow.logger.info(
            f"Workflow complete: {invoices_uploaded} invoices uploaded, {len(errors)} errors"
        )

        return WorkflowResult(
            emails_processed=len(emails),
            invoices_uploaded=invoices_uploaded,
            errors=errors,
        )
