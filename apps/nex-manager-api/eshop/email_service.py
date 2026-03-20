# -*- coding: utf-8 -*-
"""E-shop email notification service using Stalwart SMTP."""

import asyncio
import html
import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

logger = logging.getLogger(__name__)

PAYMENT_METHOD_LABELS = {
    "CARD": "Platba kartou",
    "BANK_TRANSFER": "Bankový prevod",
    "COD": "Dobierka",
    "CASH": "Hotovosť",
}

# PLU mapping for NEX Genesis order import
# Products — mapped by SKU from eshop_products / eshop_order_items
PLU_MAPPING: dict[str, int] = {
    "EM-500": 200,  # Oasis EM-1 500ml (1ks)
    "EM-5L": 202,  # Oasis EM-1 5L
    "EM-500-3PACK": 201,  # Oasis EM-1 Akcia 2+1 zadarmo
    # Shipping methods — resolved by delivery_method / shipping_type
    "SHIPPING_COURIER": 304,  # Dopravné - kuriér na adresu
    "SHIPPING_PACKETA": 303,  # Dopravné - Packeta automat / Z-Point
}
# TODO: MuFis quantity mapping (2+1 → quantity 3) is NOT handled here


class EshopEmailService:
    """E-shop email notification service using Stalwart SMTP."""

    # Default to Docker bridge IP so the container can reach Stalwart on
    # the host.  Override via SMTP_HOST / SMTP_PORT env vars if needed.
    SMTP_HOST = os.environ.get("SMTP_HOST", "172.17.0.1")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))

    def __init__(self, tenant: dict):
        self.sender = tenant.get("smtp_from", "")
        self.admin_email = tenant.get("admin_notification_email") or tenant.get(
            "admin_email", ""
        )
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
        raw_payment = str(order.get("payment_method", ""))
        payment_label = html.escape(PAYMENT_METHOD_LABELS.get(raw_payment, raw_payment))

        items_html = self._build_items_table(items, currency)
        billing_html = self._build_address_block("Fakturačná adresa", order, "billing")
        shipping_html = self._build_address_block(
            "Doručovacia adresa", order, "shipping"
        )

        body = f"""
        <h2 style="color:{self.primary_color};">Ďakujeme za Vašu objednávku!</h2>
        <p>Vážený/á {customer_name},</p>
        <p>Vaša objednávka <strong>{order_number}</strong> bola úspešne prijatá.</p>

        <h3>Položky objednávky</h3>
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
        <p>Spôsob platby: <strong>{payment_label}</strong></p>

        <p style="margin-top:20px; color:#666;">
          O zmene stavu Vašej objednávky Vás budeme informovať e-mailom.
        </p>
        """

        subject = f"Objednávka {order_number} bola prijatá — {self.brand_name}"
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
        <h2 style="color:{self.primary_color};">Platba bola prijatá</h2>
        <p>Vážený/á {customer_name},</p>
        <p>Platba za objednávku <strong>{order_number}</strong> bola úspešne spracovaná.</p>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#f0f7f0; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Číslo objednávky:</strong></td>
            <td style="text-align:right;">{order_number}</td>
          </tr>
          <tr>
            <td><strong>Zaplatená suma:</strong></td>
            <td style="text-align:right; font-weight:bold;">
              {float(total_vat):.2f} {currency}
            </td>
          </tr>
        </table>

        <h3>Položky objednávky</h3>
        {items_html}

        <p>Objednávka bude čoskoro odoslaná.</p>
        """

        subject = (
            f"Platba za objednávku {order_number} bola prijatá — {self.brand_name}"
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
                f"<p><strong>Číslo zásielky:</strong> {tracking_number}</p>"
            )
        if tracking_link:
            tracking_html += (
                f'<p><a href="{tracking_link_escaped}" '
                f'style="background:{self.primary_color}; color:#fff; '
                f"padding:10px 20px; text-decoration:none; border-radius:4px; "
                f'display:inline-block;">Sledovať zásielku</a></p>'
            )

        body = f"""
        <h2 style="color:{self.primary_color};">Objednávka bola odoslaná</h2>
        <p>Vážený/á {customer_name},</p>
        <p>Vaša objednávka <strong>{order_number}</strong> bola odoslaná.</p>

        {tracking_html}

        <p style="margin-top:20px; color:#666;">
          Doručenie očakávajte v priebehu 1\u20133 pracovných dní.
        </p>
        """

        subject = f"Objednávka {order_number} bola odoslaná — {self.brand_name}"
        full_html = self._build_html_email(body)
        await self._send_email(customer_email, subject, full_html)

    async def send_admin_new_order(self, order: dict, items: list[dict]) -> None:
        """Send new order notification to admin with XML attachment."""
        if not self.admin_email:
            logger.warning("Admin email not configured, skipping admin notification")
            return

        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = html.escape(str(order.get("customer_email", "")))
        raw_phone = str(order.get("customer_phone", "") or "")
        customer_phone = html.escape(raw_phone) if raw_phone else "neuvedený"
        currency = html.escape(str(order.get("currency", "EUR")))
        total_vat = order.get("total_amount_vat", 0)
        raw_payment = str(order.get("payment_method", ""))
        payment_label = html.escape(PAYMENT_METHOD_LABELS.get(raw_payment, raw_payment))
        note = html.escape(str(order.get("note", "")))
        order_notes = html.escape(str(order.get("order_notes", "")))

        items_html = self._build_items_table(items, currency)
        billing_html = self._build_address_block("Fakturačná adresa", order, "billing")
        shipping_html = self._build_address_block(
            "Doručovacia adresa", order, "shipping"
        )

        body = f"""
        <h2 style="color:{self.primary_color};">Nová objednávka {order_number}</h2>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#fff3e0; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Zákazník:</strong></td>
            <td>{customer_name}</td>
          </tr>
          <tr>
            <td><strong>Email:</strong></td>
            <td>{customer_email}</td>
          </tr>
          <tr>
            <td><strong>Telefón:</strong></td>
            <td>{customer_phone}</td>
          </tr>
          <tr>
            <td><strong>Spôsob platby:</strong></td>
            <td>{payment_label}</td>
          </tr>
          <tr>
            <td><strong>Celkom s DPH:</strong></td>
            <td style="font-weight:bold;">{float(total_vat):.2f} {currency}</td>
          </tr>
        </table>

        <h3>Položky</h3>
        {items_html}

        {billing_html}
        {shipping_html}

        {"<h3>Poznámka</h3><p>" + note + "</p>" if note else ""}
        {"<h3>Order Notes</h3><p style='color:#c62828;font-weight:bold;'>" + order_notes + "</p>" if order_notes else ""}
        """

        subject = f"[NOVÁ OBJEDNÁVKA] {order_number} — {customer_name}"
        full_html = self._build_html_email(body)

        # Generate XML attachment for NEX Genesis import
        xml_content = self._generate_order_xml(order, items)
        raw_order_number = str(order.get("order_number", "unknown"))
        xml_attachment = MIMEApplication(xml_content.encode("utf-8"), _subtype="xml")
        xml_attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=f"objednavka_{raw_order_number}.xml",
        )

        await self._send_email(
            self.admin_email, subject, full_html, attachments=[xml_attachment]
        )

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
        raw_payment = str(order.get("payment_method", ""))
        payment_label = html.escape(PAYMENT_METHOD_LABELS.get(raw_payment, raw_payment))
        comgate_tid = html.escape(str(order.get("comgate_transaction_id", "") or ""))

        body = f"""
        <h2 style="color:#c62828;">Neúspešná platba</h2>

        <table width="100%" cellpadding="8" cellspacing="0"
               style="background:#ffebee; border-radius:4px; margin:15px 0;">
          <tr>
            <td><strong>Objednávka:</strong></td>
            <td>{order_number}</td>
          </tr>
          <tr>
            <td><strong>Zákazník:</strong></td>
            <td>{customer_name} ({customer_email})</td>
          </tr>
          <tr>
            <td><strong>Suma:</strong></td>
            <td>{float(total_vat):.2f} {currency}</td>
          </tr>
          <tr>
            <td><strong>Spôsob platby:</strong></td>
            <td>{payment_label}</td>
          </tr>
          <tr>
            <td><strong>Comgate Transaction ID:</strong></td>
            <td>{comgate_tid}</td>
          </tr>
        </table>
        """

        subject = f"[NEÚSPEŠNÁ PLATBA] {order_number} — {customer_name}"
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

    def _generate_order_xml(self, order: dict, items: list[dict]) -> str:
        """Generate NEX Genesis-compatible XML order export."""
        root = Element("order")

        # Order header
        SubElement(root, "order_number").text = str(order.get("order_number", ""))
        created = str(order.get("created_at", ""))
        SubElement(root, "date").text = created[:10] if created else ""

        # Customer
        customer = SubElement(root, "customer")
        company = order.get("company_name") or ""
        full_name = f"{order.get('customer_name', '')}".strip() or "neznámy"
        SubElement(customer, "name").text = company or full_name
        SubElement(customer, "email").text = order.get("customer_email", "")
        SubElement(customer, "phone").text = order.get("customer_phone") or "neuvedený"

        # Billing address
        billing = SubElement(customer, "billing_address")
        SubElement(billing, "street").text = order.get("billing_street", "")
        SubElement(billing, "city").text = order.get("billing_city", "")
        SubElement(billing, "zip").text = order.get("billing_postal_code") or order.get(
            "billing_zip", ""
        )
        SubElement(billing, "country").text = order.get("billing_country", "SK")

        # Shipping address (fallback to billing)
        shipping_addr = SubElement(customer, "shipping_address")
        SubElement(shipping_addr, "street").text = order.get(
            "shipping_street"
        ) or order.get("billing_street", "")
        SubElement(shipping_addr, "city").text = order.get(
            "shipping_city"
        ) or order.get("billing_city", "")
        SubElement(shipping_addr, "zip").text = (
            order.get("shipping_zip")
            or order.get("billing_postal_code")
            or order.get("billing_zip", "")
        )
        SubElement(shipping_addr, "country").text = order.get(
            "shipping_country"
        ) or order.get("billing_country", "SK")

        # Packeta delivery point (if applicable)
        packeta_id = order.get("packeta_point_id") or ""
        packeta_name = order.get("packeta_point_name") or ""
        if packeta_id:
            dp = SubElement(root, "delivery_point")
            SubElement(dp, "packeta_id").text = packeta_id
            SubElement(dp, "name").text = packeta_name

        # Payment method
        SubElement(root, "payment_method").text = order.get("payment_method", "")

        # Items
        items_node = SubElement(root, "items")
        for item in items:
            item_node = SubElement(items_node, "item")
            sku = item.get("sku", "")
            plu = PLU_MAPPING.get(sku, 0)

            SubElement(item_node, "plu").text = str(plu)
            SubElement(item_node, "sku").text = sku
            SubElement(item_node, "name").text = item.get("name", "")
            SubElement(item_node, "quantity").text = str(item.get("quantity", 1))
            SubElement(
                item_node, "unit_price_vat"
            ).text = f"{float(item.get('unit_price_vat', 0)):.2f}"
            SubElement(item_node, "vat_rate").text = str(item.get("vat_rate", 20))

        # Shipping as separate line item
        shipping_price = float(order.get("shipping_price", 0) or 0)
        if shipping_price > 0:
            ship_item = SubElement(items_node, "item")
            delivery_method = str(order.get("delivery_method", "")).lower()
            packeta_point = order.get("packeta_point_id") or ""

            if packeta_point or "packeta" in delivery_method:
                ship_plu = PLU_MAPPING["SHIPPING_PACKETA"]
                ship_name = "Dopravné - Packeta"
            else:
                ship_plu = PLU_MAPPING["SHIPPING_COURIER"]
                ship_name = "Dopravné - kuriér na adresu"

            SubElement(ship_item, "plu").text = str(ship_plu)
            SubElement(ship_item, "sku").text = "SHIPPING"
            SubElement(ship_item, "name").text = ship_name
            SubElement(ship_item, "quantity").text = "1"
            SubElement(ship_item, "unit_price_vat").text = f"{shipping_price:.2f}"
            SubElement(ship_item, "vat_rate").text = "20"

        # Total
        SubElement(
            root, "total_vat"
        ).text = f"{float(order.get('total_amount_vat', 0)):.2f}"

        # Pretty-print with XML declaration
        raw_xml = tostring(root, encoding="unicode")
        parsed = minidom.parseString(raw_xml)  # noqa: S318
        return parsed.toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")

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
          Tento e-mail bol odoslaný automaticky, neodpovedajte naň.
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
            '<th style="text-align:left; border-bottom:2px solid #ddd;">Položka</th>'
            '<th style="text-align:center; border-bottom:2px solid #ddd;">Množstvo</th>'
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

    async def _send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        attachments: list | None = None,
    ) -> None:
        """Send email via SMTP. Supports comma-separated recipients and
        optional file attachments. Never raises — errors are logged."""
        if not self.sender:
            logger.warning("SMTP sender not configured, skipping email to %s", to)
            return

        # Support comma-separated recipients (e.g. "a@x.com,b@x.com")
        recipients = [addr.strip() for addr in to.split(",") if addr.strip()]
        if not recipients:
            logger.warning("No valid recipients in '%s'", to)
            return

        # Use mixed multipart when attachments are present, otherwise
        # alternative (HTML-only).
        if attachments:
            msg = MIMEMultipart("mixed")
            # Wrap the HTML in an alternative sub-part so mail clients
            # render it correctly alongside attachments.
            alt_part = MIMEMultipart("alternative")
            alt_part.attach(MIMEText(html_body, "html", "utf-8"))
            msg.attach(alt_part)
            for att in attachments:
                msg.attach(att)
        else:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        msg["From"] = f"{self.brand_name} <{self.sender}>"
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_sync, msg, recipients)

    def _send_sync(self, msg: MIMEMultipart, to: str | list[str]) -> None:
        """Synchronous SMTP send — runs in executor."""
        try:
            with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.send_message(msg)
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to, e)
