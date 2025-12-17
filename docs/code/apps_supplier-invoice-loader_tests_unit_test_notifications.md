# test_notifications.py

**Path:** `apps\supplier-invoice-loader\tests\unit\test_notifications.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Tests for email notifications module

---

## Functions

### `test_notifications_import()`

Test that notifications module can be imported

---

### `test_error_template_generates_html()`

Test that error template generates valid HTML

---

### `test_validation_failed_template_generates_html()`

Test that validation failed template generates valid HTML

---

### `test_daily_summary_template_generates_html()`

Test that daily summary template generates valid HTML

---

### `test_send_email_success(mock_smtp)`

Test successful email sending

---

### `test_send_email_authentication_failure(mock_smtp)`

Test email sending with authentication failure

---

### `test_send_email_multiple_recipients(mock_smtp)`

Test sending to multiple recipients

---

### `test_send_alert_email(mock_send)`

Test send_alert_email wrapper

---

### `test_send_validation_failed_email(mock_send)`

Test send_validation_failed_email wrapper

---

### `test_send_daily_summary(mock_get_stats, mock_send)`

Test send_daily_summary function

---

### `test_send_alert_email_requires_alert_email_config()`

Test that alert email requires ALERT_EMAIL to be configured

---

### `test_test_email_configuration(mock_send)`

Test test_email_configuration function

---

### `test_send_alert_adds_timestamp_if_missing()`

Test that send_alert_email adds timestamp if not provided

---

### `test_real_email_sending(request)`

Integration test: Actually send test email (requires valid SMTP config)

---

### `test_email_templates_no_injection()`

Test that email templates prevent HTML injection

---
