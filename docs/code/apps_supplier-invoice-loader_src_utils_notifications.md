# notifications.py

**Path:** `apps\supplier-invoice-loader\src\utils\notifications.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Email Notifications
Handles all email alerts and notifications

---

## Functions

### `_error_template(error_type, error_message, details)`

Template for error alert emails

Args:
    error_type: Type of error (e.g., "PDF Processing Failed", "Database Error")
    error_message: Error message
    details: Additional details (invoice_id, filename, stack trace, etc.)

Returns:
    HTML email body

---

### `_validation_failed_template(invoice_data, reason)`

Template for validation failure emails

Args:
    invoice_data: Invoice data that failed validation
    reason: Reason for validation failure

Returns:
    HTML email body

---

### `_daily_summary_template(stats)`

Template for daily summary emails

Args:
    stats: Statistics dictionary from database.get_stats()

Returns:
    HTML email body

---

### `_send_email(to, subject, html_body, text_body)`

Send email via SMTP

Args:
    to: Recipient email address (comma-separated for multiple)
    subject: Email subject
    html_body: HTML email body
    text_body: Plain text body (optional, falls back to HTML stripped)

Returns:
    True if sent successfully, False otherwise

---

### `send_alert_email(error_type, error_message, details)`

Send error alert email

Args:
    error_type: Type of error (e.g., "PDF Processing Failed")
    error_message: Error message
    details: Additional details (invoice_id, filename, stack_trace, etc.)

Returns:
    True if sent successfully, False otherwise

Example:
    send_alert_email(
        "PDF Extraction Failed",
        "Could not extract text from PDF",
        {
            'invoice_id': 42,
            'filename': 'invoice.pdf',
            'stack_trace': traceback.format_exc()
        }
    )

---

### `send_validation_failed_email(invoice_data, reason)`

Send validation failure notification

Args:
    invoice_data: Invoice data that failed validation
    reason: Reason for validation failure

Returns:
    True if sent successfully, False otherwise

Example:
    send_validation_failed_email(
        {'filename': 'invoice.pdf', 'from': 'sender@example.com'},
        'No PDF attachment found in email'
    )

---

### `send_daily_summary()`

Send daily summary email with processing statistics

Typically called by cron job or scheduled task at end of day

Returns:
    True if sent successfully, False otherwise

Example:
    # In cron: 0 23 * * * /path/to/python -c "from src.utils from src.utils import notifications; notifications.send_daily_summary()"
    send_daily_summary()

---

### `test_email_configuration()`

Test email configuration by sending a test email

Returns:
    True if test email sent successfully, False otherwise

Example:
    python -c "from src.utils from src.utils import notifications; notifications.test_email_configuration()"

---

### `send_test_email()`

Alias for test_email_configuration() for backward compatibility

Returns:
    True if test email sent successfully, False otherwise

---
