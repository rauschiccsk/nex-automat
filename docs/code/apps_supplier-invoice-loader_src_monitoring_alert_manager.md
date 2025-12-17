# alert_manager.py

**Path:** `apps\supplier-invoice-loader\src\monitoring\alert_manager.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Alert Manager for email notifications
Supports critical alerts, daily summaries, and weekly reports

---

## Classes

### AlertLevel(str, Enum)

Alert severity levels

---

### AlertType(str, Enum)

Alert types

---

### Alert

Alert data structure

**Methods:**

#### `to_dict(self)`

Convert to dictionary

---

### AlertConfig

Alert manager configuration

---

### AlertManager

Email alert manager

**Methods:**

#### `__init__(self, config)`

Initialize alert manager

Args:
    config: Alert configuration

#### `send_alert(self, alert)`

Send single alert email

Args:
    alert: Alert to send

Returns:
    True if sent successfully

#### `send_critical_alert(self, title, message, alert_type, details)`

Send critical alert

Args:
    title: Alert title
    message: Alert message
    alert_type: Type of alert
    details: Additional details

Returns:
    True if sent successfully

#### `send_warning(self, title, message, alert_type, details)`

Send warning alert

Args:
    title: Alert title
    message: Alert message
    alert_type: Type of alert
    details: Additional details

Returns:
    True if sent successfully

#### `send_daily_summary(self, invoice_stats, system_stats, errors)`

Send daily summary report

Args:
    invoice_stats: Invoice processing statistics
    system_stats: System health statistics
    errors: List of errors from the day

Returns:
    True if sent successfully

#### `send_weekly_report(self, weekly_stats, trends, recommendations)`

Send weekly report

Args:
    weekly_stats: Statistics for the week
    trends: Performance trends
    recommendations: System recommendations

Returns:
    True if sent successfully

#### `check_health_and_alert(self, health_status)`

Check health status and send alerts if needed

Args:
    health_status: Health status from HealthMonitor

Returns:
    List of alerts sent

#### `_send_email(self, subject, body, recipients)`

Send email via SMTP

Args:
    subject: Email subject
    body: Email body (HTML or plain text)
    recipients: List of recipient email addresses

Returns:
    True if sent successfully

#### `_format_alert_email(self, alert)`

Format alert as HTML email

#### `_format_details_html(self, details)`

Format details dictionary as HTML

#### `_format_daily_summary(self, invoice_stats, system_stats, errors)`

Format daily summary as HTML

#### `_format_errors_html(self, errors)`

Format errors list as HTML

#### `_format_weekly_report(self, weekly_stats, trends, recommendations)`

Format weekly report as HTML

#### `_format_dict_as_list(self, data)`

Format dictionary as HTML list items

#### `get_alert_history(self, level, alert_type, since)`

Get alert history with optional filters

Args:
    level: Filter by alert level
    level_type: Filter by alert type
    since: Filter by timestamp

Returns:
    Filtered list of alerts

---
