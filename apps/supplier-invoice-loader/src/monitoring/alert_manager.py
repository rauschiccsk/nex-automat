"""
Alert Manager for email notifications
Supports critical alerts, daily summaries, and weekly reports
"""

import logging
import smtplib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertType(str, Enum):
    """Alert types"""

    SYSTEM = "system"
    DATABASE = "database"
    INVOICE = "invoice"
    DISK_SPACE = "disk_space"
    PERFORMANCE = "performance"
    SUMMARY = "summary"
    REPORT = "report"


@dataclass
class Alert:
    """Alert data structure"""

    level: AlertLevel
    alert_type: AlertType
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "level": self.level.value,
            "type": self.alert_type.value,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


@dataclass
class AlertConfig:
    """Alert manager configuration"""

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    from_email: str
    to_emails: list[str]
    use_tls: bool = True
    use_ssl: bool = False

    # Alert thresholds
    cpu_threshold: float = 90.0
    memory_threshold: float = 90.0
    disk_threshold_critical: float = 90.0
    disk_threshold_warning: float = 80.0
    db_connection_timeout_ms: float = 1000.0

    # Report schedules
    daily_summary_time: str = "18:00"  # HH:MM
    weekly_report_day: int = 0  # 0=Monday
    weekly_report_time: str = "09:00"  # HH:MM


class AlertManager:
    """Email alert manager"""

    def __init__(self, config: AlertConfig):
        """
        Initialize alert manager

        Args:
            config: Alert configuration
        """
        self.config = config
        self._alert_history: list[Alert] = []
        self._last_daily_summary: datetime | None = None
        self._last_weekly_report: datetime | None = None

    def send_alert(self, alert: Alert) -> bool:
        """
        Send single alert email

        Args:
            alert: Alert to send

        Returns:
            True if sent successfully
        """
        try:
            subject = f"[{alert.level.value.upper()}] {alert.title}"
            body = self._format_alert_email(alert)

            return self._send_email(subject=subject, body=body, recipients=self.config.to_emails)

        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False

    def send_critical_alert(
        self,
        title: str,
        message: str,
        alert_type: AlertType = AlertType.SYSTEM,
        details: dict | None = None,
    ) -> bool:
        """
        Send critical alert

        Args:
            title: Alert title
            message: Alert message
            alert_type: Type of alert
            details: Additional details

        Returns:
            True if sent successfully
        """
        alert = Alert(
            level=AlertLevel.CRITICAL,
            alert_type=alert_type,
            title=title,
            message=message,
            details=details or {},
        )

        self._alert_history.append(alert)
        return self.send_alert(alert)

    def send_warning(
        self,
        title: str,
        message: str,
        alert_type: AlertType = AlertType.SYSTEM,
        details: dict | None = None,
    ) -> bool:
        """
        Send warning alert

        Args:
            title: Alert title
            message: Alert message
            alert_type: Type of alert
            details: Additional details

        Returns:
            True if sent successfully
        """
        alert = Alert(
            level=AlertLevel.WARNING,
            alert_type=alert_type,
            title=title,
            message=message,
            details=details or {},
        )

        self._alert_history.append(alert)
        return self.send_alert(alert)

    def send_daily_summary(self, invoice_stats: dict, system_stats: dict, errors: list[str]) -> bool:
        """
        Send daily summary report

        Args:
            invoice_stats: Invoice processing statistics
            system_stats: System health statistics
            errors: List of errors from the day

        Returns:
            True if sent successfully
        """
        subject = f"Daily Summary - {datetime.now().strftime('%Y-%m-%d')}"
        body = self._format_daily_summary(invoice_stats, system_stats, errors)

        result = self._send_email(subject=subject, body=body, recipients=self.config.to_emails)

        if result:
            self._last_daily_summary = datetime.now()

        return result

    def send_weekly_report(self, weekly_stats: dict, trends: dict, recommendations: list[str]) -> bool:
        """
        Send weekly report

        Args:
            weekly_stats: Statistics for the week
            trends: Performance trends
            recommendations: System recommendations

        Returns:
            True if sent successfully
        """
        week_start = datetime.now() - timedelta(days=7)
        subject = f"Weekly Report - Week of {week_start.strftime('%Y-%m-%d')}"
        body = self._format_weekly_report(weekly_stats, trends, recommendations)

        result = self._send_email(subject=subject, body=body, recipients=self.config.to_emails)

        if result:
            self._last_weekly_report = datetime.now()

        return result

    def check_health_and_alert(self, health_status: dict) -> list[Alert]:
        """
        Check health status and send alerts if needed

        Args:
            health_status: Health status from HealthMonitor

        Returns:
            List of alerts sent
        """
        alerts_sent = []

        # Check system metrics
        system = health_status.get("system_metrics", {})

        if system.get("cpu_percent", 0) > self.config.cpu_threshold:
            alert = Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.SYSTEM,
                title="High CPU Usage",
                message=f"CPU usage at {system['cpu_percent']}%",
                details=system,
            )
            if self.send_alert(alert):
                alerts_sent.append(alert)

        if system.get("memory_percent", 0) > self.config.memory_threshold:
            alert = Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.SYSTEM,
                title="High Memory Usage",
                message=f"Memory usage at {system['memory_percent']}%",
                details=system,
            )
            if self.send_alert(alert):
                alerts_sent.append(alert)

        disk_percent = system.get("disk_percent", 0)
        if disk_percent > self.config.disk_threshold_critical:
            alert = Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.DISK_SPACE,
                title="Critical Disk Space",
                message=f"Disk usage at {disk_percent}%, only {system.get('disk_free_gb', 0)}GB free",
                details=system,
            )
            if self.send_alert(alert):
                alerts_sent.append(alert)
        elif disk_percent > self.config.disk_threshold_warning:
            alert = Alert(
                level=AlertLevel.WARNING,
                alert_type=AlertType.DISK_SPACE,
                title="High Disk Usage",
                message=f"Disk usage at {disk_percent}%",
                details=system,
            )
            if self.send_alert(alert):
                alerts_sent.append(alert)

        # Check database
        db_status = health_status.get("database_status", {})
        if not db_status.get("connected", False):
            alert = Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.DATABASE,
                title="Database Connection Failed",
                message=f"Cannot connect to database: {db_status.get('error', 'Unknown error')}",
                details=db_status,
            )
            if self.send_alert(alert):
                alerts_sent.append(alert)

        return alerts_sent

    def _send_email(self, subject: str, body: str, recipients: list[str]) -> bool:
        """
        Send email via SMTP

        Args:
            subject: Email subject
            body: Email body (HTML or plain text)
            recipients: List of recipient email addresses

        Returns:
            True if sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["From"] = self.config.from_email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

            # Add body
            msg.attach(MIMEText(body, "html"))

            # Send via SMTP
            if self.config.use_ssl:
                with smtplib.SMTP_SSL(self.config.smtp_host, self.config.smtp_port) as server:
                    server.login(self.config.smtp_user, self.config.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                    if self.config.use_tls:
                        server.starttls()
                    server.login(self.config.smtp_user, self.config.smtp_password)
                    server.send_message(msg)

            logger.info(f"Email sent: {subject} to {recipients}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def _format_alert_email(self, alert: Alert) -> str:
        """Format alert as HTML email"""

        level_colors = {
            AlertLevel.INFO: "#2196F3",
            AlertLevel.WARNING: "#FF9800",
            AlertLevel.ERROR: "#F44336",
            AlertLevel.CRITICAL: "#D32F2F",
        }

        color = level_colors.get(alert.level, "#757575")

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: {color}; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .details {{ background-color: #f5f5f5; padding: 15px; margin-top: 20px; }}
                .footer {{ color: #757575; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{alert.level.value.upper()}: {alert.title}</h2>
            </div>
            <div class="content">
                <p><strong>Time:</strong> {alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Type:</strong> {alert.alert_type.value}</p>
                <p><strong>Message:</strong></p>
                <p>{alert.message}</p>

                {self._format_details_html(alert.details) if alert.details else ""}
            </div>
            <div class="footer">
                <p>Supplier Invoice Loader - Automated Alert System</p>
            </div>
        </body>
        </html>
        """

        return html

    def _format_details_html(self, details: dict) -> str:
        """Format details dictionary as HTML"""
        html = '<div class="details"><h3>Details:</h3><ul>'
        for key, value in details.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        html += "</ul></div>"
        return html

    def _format_daily_summary(self, invoice_stats: dict, system_stats: dict, errors: list[str]) -> str:
        """Format daily summary as HTML"""

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; }}
                .section {{ padding: 20px; border-bottom: 1px solid #e0e0e0; }}
                .stat {{ display: inline-block; margin: 10px 20px; }}
                .error {{ color: #F44336; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Daily Summary - {datetime.now().strftime("%Y-%m-%d")}</h2>
            </div>

            <div class="section">
                <h3>Invoice Processing</h3>
                <div class="stat">
                    <strong>Processed:</strong> {invoice_stats.get("total_processed", 0)}
                </div>
                <div class="stat">
                    <strong>Failed:</strong> {invoice_stats.get("total_failed", 0)}
                </div>
                <div class="stat">
                    <strong>Success Rate:</strong> {invoice_stats.get("success_rate", 0)}%
                </div>
            </div>

            <div class="section">
                <h3>System Health</h3>
                <div class="stat">
                    <strong>CPU:</strong> {system_stats.get("cpu_percent", 0)}%
                </div>
                <div class="stat">
                    <strong>Memory:</strong> {system_stats.get("memory_percent", 0)}%
                </div>
                <div class="stat">
                    <strong>Disk:</strong> {system_stats.get("disk_percent", 0)}%
                </div>
            </div>

            {self._format_errors_html(errors) if errors else ""}
        </body>
        </html>
        """

        return html

    def _format_errors_html(self, errors: list[str]) -> str:
        """Format errors list as HTML"""
        html = '<div class="section"><h3 class="error">Errors Today:</h3><ul>'
        for error in errors:
            html += f'<li class="error">{error}</li>'
        html += "</ul></div>"
        return html

    def _format_weekly_report(self, weekly_stats: dict, trends: dict, recommendations: list[str]) -> str:
        """Format weekly report as HTML"""

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; }}
                .section {{ padding: 20px; border-bottom: 1px solid #e0e0e0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Weekly Report</h2>
                <p>{(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")} to {datetime.now().strftime("%Y-%m-%d")}</p>
            </div>

            <div class="section">
                <h3>Weekly Statistics</h3>
                <ul>
                    {self._format_dict_as_list(weekly_stats)}
                </ul>
            </div>

            <div class="section">
                <h3>Performance Trends</h3>
                <ul>
                    {self._format_dict_as_list(trends)}
                </ul>
            </div>

            <div class="section">
                <h3>Recommendations</h3>
                <ul>
                    {"".join([f"<li>{rec}</li>" for rec in recommendations])}
                </ul>
            </div>
        </body>
        </html>
        """

        return html

    def _format_dict_as_list(self, data: dict) -> str:
        """Format dictionary as HTML list items"""
        return "".join([f"<li><strong>{k}:</strong> {v}</li>" for k, v in data.items()])

    def get_alert_history(
        self,
        level: AlertLevel | None = None,
        alert_type: AlertType | None = None,
        since: datetime | None = None,
    ) -> list[Alert]:
        """
        Get alert history with optional filters

        Args:
            level: Filter by alert level
            level_type: Filter by alert type
            since: Filter by timestamp

        Returns:
            Filtered list of alerts
        """
        filtered = self._alert_history

        if level:
            filtered = [a for a in filtered if a.level == level]

        if alert_type:
            filtered = [a for a in filtered if a.alert_type == alert_type]

        if since:
            filtered = [a for a in filtered if a.timestamp >= since]

        return filtered
