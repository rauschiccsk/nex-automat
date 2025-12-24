"""Daily Summary Report Generator"""
import os
import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pg8000

from .config import ReportConfig

logger = logging.getLogger(__name__)


@dataclass
class InvoiceSummary:
    """Single invoice summary for report"""
    invoice_number: str
    supplier_name: str
    issue_date: date
    total_with_vat: Decimal
    status: str
    match_percent: Optional[Decimal]
    item_count: int
    validation_status: Optional[str]
    validation_errors: Optional[str]


@dataclass
class DailyStats:
    """Aggregated daily statistics"""
    report_date: date
    total_invoices: int
    total_amount: Decimal
    by_status: Dict[str, int]
    avg_match_percent: Optional[Decimal]
    error_count: int
    invoices: List[InvoiceSummary]

    # Comparison with previous day
    prev_total_invoices: int = 0
    prev_total_amount: Decimal = Decimal("0")


class DailySummaryReport:
    """Daily summary report generator and sender"""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.template_path = Path(__file__).parent / "templates" / "daily_report.html"

    def _get_connection(self):
        """Get PostgreSQL connection"""
        password = os.environ.get("POSTGRES_PASSWORD", "")
        return pg8000.connect(
            host=self.config.db_host,
            port=self.config.db_port,
            database=self.config.db_name,
            user=self.config.db_user,
            password=password
        )

    def _is_workday(self, d: date) -> bool:
        """Check if date is workday (Mon-Fri)"""
        return d.weekday() < 5

    def fetch_daily_stats(self, report_date: date) -> DailyStats:
        """Fetch statistics for given date"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Main query - invoices for today
            cursor.execute("""
                SELECT 
                    xml_invoice_number,
                    xml_supplier_name,
                    xml_issue_date,
                    xml_total_with_vat,
                    status,
                    match_percent,
                    item_count,
                    validation_status,
                    validation_errors
                FROM supplier_invoice_heads
                WHERE DATE(created_at) = %s
                ORDER BY created_at DESC
            """, (report_date,))

            invoices = []
            for row in cursor.fetchall():
                invoices.append(InvoiceSummary(
                    invoice_number=row[0] or "",
                    supplier_name=row[1] or "",
                    issue_date=row[2],
                    total_with_vat=Decimal(str(row[3] or 0)),
                    status=row[4] or "pending",
                    match_percent=Decimal(str(row[5])) if row[5] else None,
                    item_count=row[6] or 0,
                    validation_status=row[7],
                    validation_errors=row[8]
                ))

            # Aggregations
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COALESCE(SUM(xml_total_with_vat), 0) as total_amount,
                    COALESCE(AVG(match_percent), 0) as avg_match,
                    COUNT(*) FILTER (WHERE validation_status = 'error') as errors
                FROM supplier_invoice_heads
                WHERE DATE(created_at) = %s
            """, (report_date,))

            agg = cursor.fetchone()
            total_invoices = agg[0]
            total_amount = Decimal(str(agg[1]))
            avg_match = Decimal(str(agg[2])) if agg[2] else None
            error_count = agg[3]

            # By status
            cursor.execute("""
                SELECT status, COUNT(*)
                FROM supplier_invoice_heads
                WHERE DATE(created_at) = %s
                GROUP BY status
            """, (report_date,))

            by_status = {row[0]: row[1] for row in cursor.fetchall()}

            # Previous day comparison
            prev_date = report_date - timedelta(days=1)
            cursor.execute("""
                SELECT 
                    COUNT(*),
                    COALESCE(SUM(xml_total_with_vat), 0)
                FROM supplier_invoice_heads
                WHERE DATE(created_at) = %s
            """, (prev_date,))

            prev = cursor.fetchone()
            prev_total = prev[0]
            prev_amount = Decimal(str(prev[1]))

            return DailyStats(
                report_date=report_date,
                total_invoices=total_invoices,
                total_amount=total_amount,
                by_status=by_status,
                avg_match_percent=avg_match,
                error_count=error_count,
                invoices=invoices,
                prev_total_invoices=prev_total,
                prev_total_amount=prev_amount
            )

        finally:
            cursor.close()
            conn.close()

    def render_html(self, stats: DailyStats) -> str:
        """Render HTML report from template"""
        template = self.template_path.read_text(encoding="utf-8")

        # Build invoice rows
        invoice_rows = ""
        for inv in stats.invoices:
            status_class = {
                "pending": "status-pending",
                "matched": "status-matched", 
                "approved": "status-approved",
                "imported": "status-imported",
                "error": "status-error"
            }.get(inv.status, "status-pending")

            match_str = f"{inv.match_percent:.1f}%" if inv.match_percent else "-"

            invoice_rows += f"""
            <tr>
                <td>{inv.supplier_name}</td>
                <td>{inv.invoice_number}</td>
                <td>{inv.issue_date.strftime('%d.%m.%Y') if inv.issue_date else '-'}</td>
                <td class="amount">{inv.total_with_vat:,.2f} €</td>
                <td><span class="{status_class}">{inv.status}</span></td>
                <td>{match_str}</td>
            </tr>
            """

        # Build error section
        error_section = ""
        error_invoices = [i for i in stats.invoices if i.validation_status == "error"]
        if error_invoices:
            error_section = "<h3>⚠️ Chybové faktúry</h3><ul>"
            for inv in error_invoices:
                error_section += f"<li><strong>{inv.supplier_name} - {inv.invoice_number}</strong>: {inv.validation_errors or 'Neznáma chyba'}</li>"
            error_section += "</ul>"

        # Trend indicators
        inv_trend = "↑" if stats.total_invoices > stats.prev_total_invoices else ("↓" if stats.total_invoices < stats.prev_total_invoices else "→")
        amt_trend = "↑" if stats.total_amount > stats.prev_total_amount else ("↓" if stats.total_amount < stats.prev_total_amount else "→")

        # Replace placeholders
        html = template.replace("{{REPORT_DATE}}", stats.report_date.strftime("%d.%m.%Y"))
        html = html.replace("{{TOTAL_INVOICES}}", str(stats.total_invoices))
        html = html.replace("{{TOTAL_AMOUNT}}", f"{stats.total_amount:,.2f}")
        html = html.replace("{{AVG_MATCH}}", f"{stats.avg_match_percent:.1f}" if stats.avg_match_percent else "-")
        html = html.replace("{{ERROR_COUNT}}", str(stats.error_count))
        html = html.replace("{{INVOICE_ROWS}}", invoice_rows)
        html = html.replace("{{ERROR_SECTION}}", error_section)
        html = html.replace("{{INV_TREND}}", inv_trend)
        html = html.replace("{{AMT_TREND}}", amt_trend)
        html = html.replace("{{PREV_INVOICES}}", str(stats.prev_total_invoices))
        html = html.replace("{{PREV_AMOUNT}}", f"{stats.prev_total_amount:,.2f}")

        # Status breakdown
        status_breakdown = ", ".join([f"{k}: {v}" for k, v in stats.by_status.items()]) or "žiadne"
        html = html.replace("{{STATUS_BREAKDOWN}}", status_breakdown)

        return html

    def send_email(self, html_content: str, report_date: date) -> bool:
        """Send email to all recipients"""
        if not self.config.all_recipients:
            logger.warning("No recipients configured")
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 Denný report faktúr - {report_date.strftime('%d.%m.%Y')}"
        msg["From"] = self.config.from_email
        msg["To"] = ", ".join(self.config.all_recipients)

        msg.attach(MIMEText(html_content, "html", "utf-8"))

        try:
            with smtplib.SMTP_SSL(self.config.smtp_host, self.config.smtp_port) as server:
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.sendmail(
                    self.config.from_email,
                    self.config.all_recipients,
                    msg.as_string()
                )
            logger.info(f"Report sent to {len(self.config.all_recipients)} recipients")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def run(self, report_date: Optional[date] = None) -> bool:
        """Run the daily report"""
        report_date = report_date or date.today()

        # Check workday
        if self.config.workdays_only and not self._is_workday(report_date):
            logger.info(f"Skipping report for {report_date} (not a workday)")
            return True

        logger.info(f"Generating daily report for {report_date}")

        # Fetch stats
        stats = self.fetch_daily_stats(report_date)

        # Check if empty
        if stats.total_invoices == 0 and not self.config.send_empty_report:
            logger.info("No invoices today, skipping report")
            return True

        # Render and send
        html = self.render_html(stats)
        return self.send_email(html, report_date)
