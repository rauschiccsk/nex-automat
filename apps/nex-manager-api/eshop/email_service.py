"""E-shop email notification service using Stalwart SMTP (localhost:25)."""

import asyncio
import html
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class EshopEmailService:
    """E-shop email notification service using Stalwart SMTP."""

    SMTP_HOST = "localhost"
    SMTP_PORT = 25

    def __init__(self, tenant: dict):
        self.sender = tenant.get("smtp_from", "")
        self.admin_email = tenant.get("admin_email", "")
        self.brand_name = tenant.get("brand_name", "E-shop")
        self.domain = tenant.get("domain", "")
        self.primary_color = tenant.get("primary_color", "#2E7D32")

    # ------------------------------------------------------------------
    # Public async methods
    # ------------------------------------------------------------------

    async def send_order_confirmation(self, order: dict, items: list[dict]) -> None:
        """Send order confirmation email to customer."""
        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = order.get("customer_email", "")
        currency = html.escape(str(order.get("currency", "EUR")))
        total_vat = order.get("total_amount_vat", 0)
        payment_method = html.escape(str(order.get("payment_method", "")))

        items_html = self._build_items_table(items, currency)
        billing_html = self._build_address_block("Fakturacna adresa", order, "billing")
        shipping_html = self._build_address_block(
            "Dorucovacia adresa", order, "shipping"
        )

        body = f"""
        <h2 style="color:{self.primary_color};">Dakujeme za Vasu objednavku!</h2>
        <p>Vazeny/a {customer_name},</p>
        <p>Vasa objednavka <strong>{order_number}</strong> bola uspesne prijata.</p>

        <h3>Polozky objednavky</h3>
        {items_html}

        <table width="100%" cellpadding="4" cellspacing="0">
          <tr>
            <td style="text-align:right; font-weight:bold; font-size:16px;">
              Celkom s DPH: {float(total_vat):.2f} {currency}
            </td>
          </tr>
        </table>

        {billing_html}
        {shipping_html}

        <h3>Platba</h3>
        <p>Sposob platby: <strong>{payment_method}</strong></p>

        <p style="margin-top:20px; color:#666;">
          O zmene stavu Vasej objednavky Vas budeme informovat e-mailom.
        </p>
        """

        subject = f"Objednavka {order_number} bola prijata \u2014 {self.brand_name}"
        full_html = self._build_html_email(body)
        await self._send_email(customer_email, subject, full_html)

    async def send_payment_confirmation(self, order: dict, items: list[dict]) -> None:
        """Send payment confirmation email to customer."""
        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = order.get("customer_email", "")
        currency = html.escape(str(order.get("currency", "EUR")))
        total_vat = order.get("total_amount_vat", 0)

        items_html = self._build_items_table(items, currency)

        body = f"""
        <h2 style="color:{self.primary_color};">Platba bola prijata</h2>
        <p>Vazeny/a {customer_name},</p>
        <p>Platba za objednavku <strong>{order_number}</strong> bola uspesne spracovana.</p>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#f0f7f0; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Cislo objednavky:</strong></td>
            <td style="text-align:right;">{order_number}</td>
          </tr>
          <tr>
            <td><strong>Zaplatena suma:</strong></td>
            <td style="text-align:right; font-weight:bold;">
              {float(total_vat):.2f} {currency}
            </td>
          </tr>
        </table>

        <h3>Polozky objednavky</h3>
        {items_html}

        <p>Objednavka bude coskoro odoslana.</p>
        """

        subject = (
            f"Platba za objednavku {order_number} bola prijata \u2014 {self.brand_name}"
        )
        full_html = self._build_html_email(body)
        await self._send_email(customer_email, subject, full_html)

    async def send_shipping_notification(self, order: dict) -> None:
        """Send shipping notification email to customer."""
        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = order.get("customer_email", "")
        tracking_number = html.escape(str(order.get("tracking_number", "")))
        tracking_link = order.get("tracking_link", "")
        tracking_link_escaped = html.escape(tracking_link)

        tracking_html = ""
        if tracking_number:
            tracking_html += (
                f"<p><strong>Cislo zasielky:</strong> {tracking_number}</p>"
            )
        if tracking_link:
            tracking_html += (
                f'<p><a href="{tracking_link_escaped}" '
                f'style="background:{self.primary_color}; color:#fff; '
                f"padding:10px 20px; text-decoration:none; border-radius:4px; "
                f'display:inline-block;">Sledovat zasielku</a></p>'
            )

        body = f"""
        <h2 style="color:{self.primary_color};">Objednavka bola odoslana</h2>
        <p>Vazeny/a {customer_name},</p>
        <p>Vasa objednavka <strong>{order_number}</strong> bola odoslana.</p>

        {tracking_html}

        <p style="margin-top:20px; color:#666;">
          Dorucenie ocakavajte v priebehu 1-3 pracovnych dni.
        </p>
        """

        subject = f"Objednavka {order_number} bola odoslana \u2014 {self.brand_name}"
        full_html = self._build_html_email(body)
        await self._send_email(customer_email, subject, full_html)

    async def send_admin_new_order(self, order: dict, items: list[dict]) -> None:
        """Send new order notification to admin."""
        if not self.admin_email:
            logger.warning("Admin email not configured, skipping admin notification")
            return

        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = html.escape(str(order.get("customer_email", "")))
        customer_phone = html.escape(str(order.get("customer_phone", "")))
        currency = html.escape(str(order.get("currency", "EUR")))
        total_vat = order.get("total_amount_vat", 0)
        payment_method = html.escape(str(order.get("payment_method", "")))
        note = html.escape(str(order.get("note", "")))

        items_html = self._build_items_table(items, currency)
        billing_html = self._build_address_block("Fakturacna adresa", order, "billing")
        shipping_html = self._build_address_block(
            "Dorucovacia adresa", order, "shipping"
        )

        body = f"""
        <h2 style="color:{self.primary_color};">Nova objednavka {order_number}</h2>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#fff3e0; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Zakaznik:</strong></td>
            <td>{customer_name}</td>
          </tr>
          <tr>
            <td><strong>Email:</strong></td>
            <td>{customer_email}</td>
          </tr>
          <tr>
            <td><strong>Telefon:</strong></td>
            <td>{customer_phone}</td>
          </tr>
          <tr>
            <td><strong>Sposob platby:</strong></td>
            <td>{payment_method}</td>
          </tr>
          <tr>
            <td><strong>Celkom s DPH:</strong></td>
            <td style="font-weight:bold;">{float(total_vat):.2f} {currency}</td>
          </tr>
        </table>

        <h3>Polozky</h3>
        {items_html}

        {billing_html}
        {shipping_html}

        {"<h3>Poznamka</h3><p>" + note + "</p>" if note else ""}
        """

        subject = f"[NOVA OBJEDNAVKA] {order_number} \u2014 {customer_name}"
        full_html = self._build_html_email(body)
        await self._send_email(self.admin_email, subject, full_html)

    async def send_admin_payment_failed(self, order: dict) -> None:
        """Send payment failed notification to admin."""
        if not self.admin_email:
            logger.warning("Admin email not configured, skipping admin notification")
            return

        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = html.escape(str(order.get("customer_email", "")))
        currency = html.escape(str(order.get("currency", "EUR")))
        total_vat = order.get("total_amount_vat", 0)
        payment_method = html.escape(str(order.get("payment_method", "")))
        comgate_tid = html.escape(str(order.get("comgate_transaction_id", "") or ""))

        body = f"""
        <h2 style="color:#c62828;">Neuspesna platba</h2>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#ffebee; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Objednavka:</strong></td>
            <td>{order_number}</td>
          </tr>
          <tr>
            <td><strong>Zakaznik:</strong></td>
            <td>{customer_name} ({customer_email})</td>
          </tr>
          <tr>
            <td><strong>Suma:</strong></td>
            <td>{float(total_vat):.2f} {currency}</td>
          </tr>
          <tr>
            <td><strong>Sposob platby:</strong></td>
            <td>{payment_method}</td>
          </tr>
          <tr>
            <td><strong>Comgate Transaction ID:</strong></td>
            <td>{comgate_tid}</td>
          </tr>
        </table>
        """

        subject = f"[NEUSPESNA PLATBA] {order_number} \u2014 {customer_name}"
        full_html = self._build_html_email(body)
        await self._send_email(self.admin_email, subject, full_html)

    async def send_lead_welcome_email(self, tenant: dict, lead: dict) -> None:
        """Pošle welcome email s discount kódom novému leadovi."""
        subject = "Vaša 50% zľava na Oasis EM-1 je pripravená!"
        expires_at = lead["expires_at"]
        expires_str = (
            expires_at.strftime("%d.%m.%Y")
            if hasattr(expires_at, "strftime")
            else str(expires_at)
        )
        domain = tenant.get("domain", self.domain)
        company = tenant.get("company_name") or tenant.get(
            "tenant_name", self.brand_name
        )

        body = f"""Dobrý deň{" " + lead["first_name"] if lead.get("first_name") else ""},

Ďakujeme za Váš záujem o Oasis EM-1!

Pripravili sme pre Vás špeciálnu zľavu 50% na prvý nákup.

Váš zľavový kód: {lead["discount_code"]}

Kód je platný do {expires_str}.
Použite ho pri objednávke na {domain}.

Oasis EM-1 je certifikovaná pôdna pomocná látka,
ktorá regeneruje pôdu a zvyšuje úrodnosť bez chémie.

S pozdravom,
Tím {company}
{domain}"""
        await self._send_email(
            to=lead["email"],
            subject=subject,
            html_body=self._build_html_email(
                f"<pre style='font-family:inherit;'>{body}</pre>"
            ),
        )

    async def send_lead_reminder_email(
        self, tenant: dict, lead: dict, days_remaining: int
    ) -> None:
        """Mesačný reminder o zľave."""
        subject = f"Vaša 50% zľava vyprší o {days_remaining} dní!"
        expires_at = lead["expires_at"]
        expires_str = (
            expires_at.strftime("%d.%m.%Y")
            if hasattr(expires_at, "strftime")
            else str(expires_at)
        )
        domain = tenant.get("domain", self.domain)
        company = tenant.get("company_name") or tenant.get(
            "tenant_name", self.brand_name
        )

        body = f"""Dobrý deň{" " + lead["first_name"] if lead.get("first_name") else ""},

Strážime pre Vás 50% zľavu na Oasis EM-1.

Váš zľavový kód: {lead["discount_code"]}
Platnosť do: {expires_str}
Zostáva: {days_remaining} dní

Nepremeškajte príležitosť vyskúšať certifikovanú
pôdnu pomocnú látku za polovičnú cenu.

Objednajte na: https://{domain}

S pozdravom,
Tím {company}"""
        await self._send_email(
            to=lead["email"],
            subject=subject,
            html_body=self._build_html_email(
                f"<pre style='font-family:inherit;'>{body}</pre>"
            ),
        )

    # ------------------------------------------------------------------
    # Private helper methods
    # ------------------------------------------------------------------

    def _build_html_email(self, body_html: str) -> str:
        """Wrap body content in branded HTML email layout."""
        brand = html.escape(self.brand_name)
        domain = html.escape(self.domain)
        color = html.escape(self.primary_color)

        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; background:#f5f5f5; font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:20px;">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#fff; border-radius:8px;">
        <tr><td style="background:{color}; padding:20px; text-align:center; border-radius:8px 8px 0 0;">
          <h1 style="color:#fff; margin:0;">{brand}</h1>
        </td></tr>
        <tr><td style="padding:30px;">
          {body_html}
        </td></tr>
        <tr><td style="padding:15px; text-align:center; color:#999; font-size:12px; border-top:1px solid #eee;">
          {brand} | {domain}<br>
          Tento e-mail bol odoslany automaticky, neodpovedajte nan.
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    def _build_items_table(self, items: list[dict], currency: str) -> str:
        """Build HTML table of order items."""
        rows = ""
        for item in items:
            name = html.escape(str(item.get("name", "")))
            qty = item.get("quantity", 0)
            unit_price_vat = float(item.get("unit_price_vat", 0))
            line_total = unit_price_vat * qty
            curr = html.escape(currency)
            rows += (
                f"<tr>"
                f'<td style="border-bottom:1px solid #eee;">{name}</td>'
                f'<td style="text-align:center; border-bottom:1px solid #eee;">'
                f"{qty}</td>"
                f'<td style="text-align:right; border-bottom:1px solid #eee;">'
                f"{line_total:.2f} {curr}</td>"
                f"</tr>"
            )

        return (
            '<table width="100%" cellpadding="8" cellspacing="0" '
            'style="border-collapse:collapse;">'
            '<tr style="background:#f5f5f5;">'
            '<th style="text-align:left; border-bottom:2px solid #ddd;">Polozka</th>'
            '<th style="text-align:center; border-bottom:2px solid #ddd;">Mnozstvo</th>'
            '<th style="text-align:right; border-bottom:2px solid #ddd;">Cena s DPH</th>'
            "</tr>"
            f"{rows}"
            "</table>"
        )

    def _build_address_block(self, title: str, order: dict, prefix: str) -> str:
        """Build HTML address block (billing or shipping)."""
        name = html.escape(str(order.get(f"{prefix}_name", "") or ""))
        if not name:
            return ""
        name2 = html.escape(str(order.get(f"{prefix}_name2", "") or ""))
        street = html.escape(str(order.get(f"{prefix}_street", "") or ""))
        city = html.escape(str(order.get(f"{prefix}_city", "") or ""))
        zip_code = html.escape(str(order.get(f"{prefix}_zip", "") or ""))
        country = html.escape(str(order.get(f"{prefix}_country", "") or ""))

        lines = [name]
        if name2:
            lines.append(name2)
        if street:
            lines.append(street)
        if city or zip_code:
            lines.append(f"{zip_code} {city}".strip())
        if country:
            lines.append(country)

        return (
            f"<h3>{html.escape(title)}</h3>"
            f'<p style="line-height:1.6;">{"<br>".join(lines)}</p>'
        )

    async def _send_email(self, to: str, subject: str, html_body: str) -> None:
        """Send email via SMTP. Never raises — errors are logged."""
        if not self.sender:
            logger.warning("SMTP sender not configured, skipping email to %s", to)
            return

        msg = MIMEMultipart("alternative")
        msg["From"] = f"{self.brand_name} <{self.sender}>"
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_sync, msg, to)

    def _send_sync(self, msg: MIMEMultipart, to: str) -> None:
        """Synchronous SMTP send — runs in executor."""
        try:
            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.send_message(msg)
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to, e)
