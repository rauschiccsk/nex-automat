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

from nex_config.business import DEFAULT_VAT_RATE_PERCENT
from settings.service import get_setting


def _vat_rate() -> int:
    """Read VAT rate from runtime settings, fallback to compile-time default."""
    return int(
        get_setting("business.default_vat_rate_percent", DEFAULT_VAT_RATE_PERCENT)
    )


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
        company_html = self._build_company_section(order)

        color = self.primary_color
        notes_html = ""
        if order.get("order_notes"):
            notes_html = self._build_section(
                "Pozn\u00e1mka k objedn\u00e1vke",
                '<p style="margin:0;">'
                + html.escape(str(order["order_notes"]))
                + "</p>",
            )

        total_html = (
            f'<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:0 0 16px 0;">'
            f'<tr><td style="text-align:right; padding:10px 8px; '
            f"font-weight:700; font-size:16px; "
            f'background:#f0f7f0; border-radius:4px;">'
            f"Celkom s DPH: {float(total_vat):.2f} {currency}"
            f"</td></tr></table>"
        )

        body = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"\u010eakujeme za Va\u0161u objedn\u00e1vku!</h2>"
            f"<p>V\u00e1\u017een\u00fd/\u00e1 {customer_name},</p>"
            f"<p>Va\u0161a objedn\u00e1vka <strong>{order_number}</strong> "
            f"bola \u00faspe\u0161ne prijat\u00e1.</p>"
            f"{items_html}"
            f"{total_html}"
            f"{billing_html}"
            f"{company_html}"
            f"{shipping_html}"
            + self._build_section(
                "Platba",
                f'<p style="margin:0;">Sp\u00f4sob platby: '
                f"<strong>{payment_label}</strong></p>",
            )
            + notes_html
            + '<p style="margin-top:24px; color:#666666; font-size:14px;">'
            "O zmene stavu Va\u0161ej objedn\u00e1vky V\u00e1s budeme "
            "informova\u0165 e-mailom.</p>"
        )

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
        company_html = self._build_company_section(order)

        color = self.primary_color
        notes_html = ""
        if order.get("order_notes"):
            notes_html = self._build_section(
                "Pozn\u00e1mka k objedn\u00e1vke",
                '<p style="margin:0;">'
                + html.escape(str(order["order_notes"]))
                + "</p>",
            )

        info_table = self._build_info_table(
            [
                ("\u010c\u00edslo objedn\u00e1vky", order_number),
                (
                    "Zaplaten\u00e1 suma",
                    f"<strong>{float(total_vat):.2f} {currency}</strong>",
                ),
            ],
            bg="#f0f7f0",
        )

        body = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Platba bola prijat\u00e1</h2>"
            f"<p>V\u00e1\u017een\u00fd/\u00e1 {customer_name},</p>"
            f"<p>Platba za objedn\u00e1vku <strong>{order_number}</strong> "
            f"bola \u00faspe\u0161ne spracovan\u00e1.</p>"
            f"{info_table}"
            f"{items_html}"
            f"{company_html}"
            f"{notes_html}"
            f'<p style="margin-top:20px;">Objedn\u00e1vka bude \u010doskoro '
            f"odoslan\u00e1.</p>"
        )

        subject = (
            f"Platba za objednávku {order_number} bola prijatá — {self.brand_name}"
        )
        full_html = self._build_html_email(body)
        await self._send_email(customer_email, subject, full_html)

    async def send_shipping_notification(
        self,
        order: dict,
        items: list[dict] | None = None,
    ) -> None:
        """Send shipping notification email to customer."""
        order_number = html.escape(str(order.get("order_number", "")))
        customer_name = html.escape(str(order.get("customer_name", "")))
        customer_email = order.get("customer_email", "")
        currency = html.escape(str(order.get("currency", "EUR")))
        tracking_number = html.escape(str(order.get("tracking_number", "")))
        tracking_link = order.get("tracking_link", "")
        tracking_link_escaped = html.escape(tracking_link)
        color = self.primary_color

        tracking_html = ""
        if tracking_number or tracking_link:
            inner = ""
            if tracking_number:
                inner += (
                    f'<p style="margin:0 0 8px 0;">'
                    f"<strong>\u010c\u00edslo z\u00e1sielky:</strong> "
                    f"{tracking_number}</p>"
                )
            if tracking_link:
                inner += (
                    f'<p style="margin:8px 0 0 0; text-align:center;">'
                    f'<a href="{tracking_link_escaped}" '
                    f'style="display:inline-block; padding:12px 28px; '
                    f"background:{color}; color:#ffffff; "
                    f"text-decoration:none; border-radius:6px; "
                    f'font-weight:600;">Sledova\u0165 z\u00e1sielku</a></p>'
                )
            tracking_html = self._build_section(
                "Inform\u00e1cie o z\u00e1sielke",
                inner,
            )

        items_html = ""
        if items:
            items_html = self._build_items_table(items, currency)

        body = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Va\u0161a objedn\u00e1vka bola odoslan\u00e1</h2>"
            f"<p>V\u00e1\u017een\u00fd/\u00e1 {customer_name},</p>"
            f"<p>Va\u0161a objedn\u00e1vka <strong>{order_number}</strong> "
            f"bola odoslan\u00e1.</p>"
            f"{tracking_html}"
            f"{items_html}"
            f'<p style="margin-top:24px; color:#666666; font-size:14px;">'
            f"Doru\u010denie o\u010dak\u00e1vajte v priebehu "
            f"1\u20133 pracovn\u00fdch dn\u00ed.</p>"
        )

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
        company_html = self._build_company_section(order)

        color = self.primary_color
        info_table = self._build_info_table(
            [
                ("Z\u00e1kazn\u00edk", customer_name),
                ("Email", customer_email),
                ("Telef\u00f3n", customer_phone),
                ("Sp\u00f4sob platby", payment_label),
                ("Celkom s DPH", f"<strong>{float(total_vat):.2f} {currency}</strong>"),
            ],
            bg="#fff3e0",
        )

        notes_section = ""
        if note:
            notes_section += self._build_section(
                "Pozn\u00e1mka", f'<p style="margin:0;">{note}</p>'
            )
        if order_notes:
            notes_section += self._build_section(
                "Pozn\u00e1mka od z\u00e1kazn\u00edka",
                f'<p style="margin:0; color:#c62828; font-weight:700;">'
                f"{order_notes}</p>",
            )

        body = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Nov\u00e1 objedn\u00e1vka {order_number}</h2>"
            f"{info_table}"
            f"{items_html}"
            f"{billing_html}"
            f"{company_html}"
            f"{shipping_html}"
            f"{notes_section}"
        )

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

        info_table = self._build_info_table(
            [
                ("Objedn\u00e1vka", order_number),
                ("Z\u00e1kazn\u00edk", f"{customer_name} ({customer_email})"),
                ("Suma", f"{float(total_vat):.2f} {currency}"),
                ("Sp\u00f4sob platby", payment_label),
                ("Comgate Transaction ID", comgate_tid),
            ],
            bg="#ffebee",
        )

        body = (
            f'<h2 style="color:#c62828; margin-top:0;">'
            f"Ne\u00faspe\u0161n\u00e1 platba</h2>"
            f"{info_table}"
        )

        subject = f"[NEÚSPEŠNÁ PLATBA] {order_number} — {customer_name}"
        full_html = self._build_html_email(body)
        await self._send_email(self.admin_email, subject, full_html)

    async def send_lead_welcome_email(self, tenant: dict, lead: dict) -> None:
        """Po\u0161le welcome email s discount k\u00f3dom nov\u00e9mu leadovi."""
        subject = "Va\u0161a 50% z\u013eava na Oasis EM-1 je pripraven\u00e1!"
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
        color = self.primary_color
        greeting = lead.get("first_name", "")
        name_part = f" {html.escape(greeting)}" if greeting else ""
        code = html.escape(str(lead["discount_code"]))
        d_esc = html.escape(domain)

        body_html = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Va\u0161a z\u013eava je pripraven\u00e1!</h2>"
            f"<p>Dobr\u00fd de\u0148{name_part},</p>"
            f"<p>\u010eakujeme za V\u00e1\u0161 z\u00e1ujem o Oasis EM-1!</p>"
            f"<p>Pripravili sme pre V\u00e1s \u0161peci\u00e1lnu "
            f"z\u013eavu <strong>50%</strong> na prv\u00fd n\u00e1kup.</p>"
            f'<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:20px 0; text-align:center;">'
            f'<tr><td style="background:#f0f7f0; padding:20px; '
            f'border-radius:8px; border:2px dashed {color};">'
            f'<span style="font-size:24px; font-weight:700; '
            f'color:{color}; letter-spacing:2px;">{code}</span>'
            f"</td></tr></table>"
            f"<p>K\u00f3d je platn\u00fd do <strong>{expires_str}</strong>."
            f"<br>Pou\u017eite ho pri objedn\u00e1vke na "
            f'<a href="https://{d_esc}" style="color:{color};">{d_esc}</a>.</p>'
            f"<p>Oasis EM-1 je certifikovan\u00e1 p\u00f4dna pomocn\u00e1 "
            f"l\u00e1tka, ktor\u00e1 regeneruje p\u00f4du a zvy\u0161uje "
            f"\u00farodnosc bez ch\u00e9mie.</p>"
            f'<p style="margin-top:24px;">S pozdravom,<br>'
            f"T\u00edm {html.escape(company)}</p>"
        )
        await self._send_email(
            to=lead["email"],
            subject=subject,
            html_body=self._build_html_email(body_html),
        )

    async def send_lead_reminder_email(
        self, tenant: dict, lead: dict, days_remaining: int
    ) -> None:
        """Mesa\u010dn\u00fd reminder o z\u013eave."""
        subject = (
            f"Va\u0161a 50% z\u013eava vypr\u0161\u00ed o {days_remaining} dn\u00ed!"
        )
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
        color = self.primary_color
        greeting = lead.get("first_name", "")
        name_part = f" {html.escape(greeting)}" if greeting else ""
        code = html.escape(str(lead["discount_code"]))
        d_esc = html.escape(domain)

        body_html = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Z\u013eava \u010doskoro vypr\u0161\u00ed!</h2>"
            f"<p>Dobr\u00fd de\u0148{name_part},</p>"
            f"<p>Str\u00e1\u017eime pre V\u00e1s <strong>50% z\u013eavu"
            f"</strong> na Oasis EM-1.</p>"
            f'<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:20px 0; text-align:center;">'
            f'<tr><td style="background:#fff3e0; padding:20px; '
            f'border-radius:8px; border:2px dashed #e65100;">'
            f'<span style="font-size:24px; font-weight:700; '
            f'color:#e65100; letter-spacing:2px;">{code}</span><br>'
            f'<span style="font-size:13px; color:#666;">Platnos\u0165 do: '
            f"{expires_str} &middot; Zost\u00e1va: "
            f"{days_remaining} dn\u00ed</span>"
            f"</td></tr></table>"
            f"<p>Nepreme\u0161kajte pr\u00edle\u017eitos\u0165 vysk\u00fa\u0161a\u0165 "
            f"certifikovan\u00fa p\u00f4dnu pomocn\u00fa l\u00e1tku "
            f"za polovi\u010dn\u00fa cenu.</p>"
            f'<p style="text-align:center; margin:24px 0;">'
            f'<a href="https://{d_esc}" '
            f'style="display:inline-block; padding:14px 36px; '
            f"background:{color}; color:#ffffff; text-decoration:none; "
            f'border-radius:6px; font-weight:700; font-size:15px;">'
            f"Objedna\u0165 teraz</a></p>"
            f'<p style="margin-top:20px;">S pozdravom,<br>'
            f"T\u00edm {html.escape(company)}</p>"
        )
        await self._send_email(
            to=lead["email"],
            subject=subject,
            html_body=self._build_html_email(body_html),
        )

    async def send_password_reset_email(self, email: str, token: str) -> None:
        """Send password reset email with secure link."""
        reset_url = f"https://{self.domain}/reset-password?token={token}"
        color = self.primary_color
        body_html = (
            f'<h2 style="color:{color}; margin-top:0;">'
            f"Obnovenie hesla</h2>"
            f"<p>Dobr\u00fd de\u0148,</p>"
            f"<p>Dostali sme \u017eiados\u0165 o zmenu hesla pre v\u00e1\u0161 "
            f"\u00fa\u010det.</p>"
            f'<p style="text-align:center; margin:28px 0;">'
            f'<a href="{html.escape(reset_url)}" '
            f'style="display:inline-block; padding:14px 36px; '
            f"background:{color}; color:#ffffff; "
            f"text-decoration:none; border-radius:6px; font-weight:700; "
            f'font-size:15px;">Zmeni\u0165 heslo</a></p>'
            f"<p>Ak ste o zmenu hesla ne\u017eiadali, tento email "
            f"m\u00f4\u017eete ignorova\u0165. "
            f"Va\u0161e heslo zostane nezmenen\u00e9.</p>"
            f'<p style="color:#999999; font-size:13px;">'
            f"Link je platn\u00fd 24 hod\u00edn.</p>"
        )
        await self._send_email(
            to=email,
            subject=f"Obnovenie hesla \u2014 {self.brand_name}",
            html_body=self._build_html_email(body_html),
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
        cid = order.get("customer_id")
        SubElement(customer, "customer_id").text = str(cid if cid else 0)
        company = order.get("company_name") or ""
        full_name = f"{order.get('customer_name', '')}".strip() or "neznámy"
        SubElement(customer, "name").text = company or full_name
        SubElement(customer, "email").text = order.get("customer_email", "")
        SubElement(customer, "phone").text = order.get("customer_phone") or "neuvedený"

        # Company details (only if present)
        if order.get("company_name"):
            SubElement(customer, "company_name").text = order["company_name"]
        if order.get("company_ico"):
            SubElement(customer, "company_ico").text = order["company_ico"]
        if order.get("company_dic"):
            SubElement(customer, "company_dic").text = order["company_dic"]
        if order.get("company_ic_dph"):
            SubElement(customer, "company_ic_dph").text = order["company_ic_dph"]

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

        # Items (skip shipping — added separately below with correct PLU)
        items_node = SubElement(root, "items")
        for item in items:
            sku = item.get("sku", "")
            if sku == "SHIPPING":
                continue
            item_node = SubElement(items_node, "item")
            plu = PLU_MAPPING.get(sku, 0)

            SubElement(item_node, "plu").text = str(plu)
            SubElement(item_node, "sku").text = sku
            SubElement(item_node, "name").text = item.get("name", "")
            SubElement(item_node, "quantity").text = str(item.get("quantity", 1))
            SubElement(
                item_node, "unit_price_vat"
            ).text = f"{float(item.get('unit_price_vat', 0)):.2f}"
            SubElement(item_node, "vat_rate").text = str(
                item.get("vat_rate", _vat_rate())
            )

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
            SubElement(ship_item, "vat_rate").text = str(_vat_rate())

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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0; padding:0; background:#f5f5f5; font-family:Arial,Helvetica,sans-serif; -webkit-text-size-adjust:100%;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;">
    <tr><td align="center" style="padding:24px 16px;">
      <!--[if mso]><table width="600" cellpadding="0" cellspacing="0"><tr><td><![endif]-->
      <table cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08); max-width:600px; width:100%;">
        <!-- Header -->
        <tr><td style="background:{color}; padding:28px 32px; text-align:center; border-radius:8px 8px 0 0;">
          <h1 style="color:#ffffff; margin:0; font-size:26px; font-weight:700; letter-spacing:0.5px;">{brand}</h1>
        </td></tr>
        <!-- Body -->
        <tr><td style="padding:32px 32px 24px 32px; color:#333333; font-size:15px; line-height:1.6;">
          {body_html}
        </td></tr>
        <!-- Footer -->
        <tr><td style="padding:20px 32px; text-align:center; color:#999999; font-size:12px; line-height:1.5; border-top:1px solid #eeeeee; border-radius:0 0 8px 8px;">
          {brand} &middot; {domain}<br>
          Tento e-mail bol odoslan\u00fd automaticky, neodpovedajte na\u0148.
        </td></tr>
      </table>
      <!--[if mso]></td></tr></table><![endif]-->
    </td></tr>
  </table>
</body>
</html>"""

    def _build_items_table(self, items: list[dict], currency: str) -> str:
        """Build HTML table of order items (products + shipping)."""
        bdr = "border:1px solid #dee2e6;"
        rows = ""
        for item in items:
            name = html.escape(str(item.get("name", "")))
            qty = item.get("quantity", 0)
            unit_price_vat = float(item.get("unit_price_vat", 0))
            line_total = unit_price_vat * qty
            curr = html.escape(currency)
            is_shipping = item.get("item_type") == "shipping"
            bg = "background:#f8f9fa;" if is_shipping else ""
            prefix = "\U0001f69a " if is_shipping else ""
            rows += (
                f'<tr style="{bg}">'
                f'<td style="{bdr} padding:8px;">{prefix}{name}</td>'
                f'<td style="{bdr} padding:8px; text-align:center;">{qty}</td>'
                f'<td style="{bdr} padding:8px; text-align:right;">'
                f"{line_total:.2f} {curr}</td>"
                "</tr>"
            )

        color = html.escape(self.primary_color)
        return (
            '<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse; {bdr} margin:16px 0;">'
            f'<tr style="background:{color};">'
            f'<th style="{bdr} padding:10px 8px; text-align:left; '
            f'color:#ffffff; font-weight:600;">Polo\u017eka</th>'
            f'<th style="{bdr} padding:10px 8px; text-align:center; '
            f'color:#ffffff; font-weight:600;">Mno\u017estvo</th>'
            f'<th style="{bdr} padding:10px 8px; text-align:right; '
            f'color:#ffffff; font-weight:600;">Cena s DPH</th>'
            "</tr>"
            f"{rows}"
            "</table>"
        )

    def _build_section(self, title: str, content_html: str) -> str:
        """Build a styled section block with left border accent."""
        color = html.escape(self.primary_color)
        return (
            f'<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:20px 0 12px 0;">'
            f"<tr><td>"
            f'<h3 style="color:{color}; margin:0 0 10px 0; font-size:15px; '
            f"font-weight:700; border-bottom:2px solid {color}; "
            f'padding-bottom:6px;">{title}</h3>'
            f'<div style="padding:0 0 0 12px; border-left:3px solid {color};">'
            f"{content_html}"
            f"</div>"
            f"</td></tr></table>"
        )

    def _build_info_table(
        self, rows: list[tuple[str, str]], bg: str = "#f8f9fa"
    ) -> str:
        """Build a bordered key-value info table."""
        bdr = "border:1px solid #dee2e6;"
        html_rows = ""
        for label, value in rows:
            html_rows += (
                f"<tr>"
                f'<td style="{bdr} padding:8px 12px; background:{bg}; '
                f'font-weight:600; width:45%;">{label}</td>'
                f'<td style="{bdr} padding:8px 12px;">{value}</td>'
                f"</tr>"
            )
        return (
            f'<table width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse; {bdr} margin:16px 0;">'
            f"{html_rows}</table>"
        )

    def _build_company_section(self, order: dict) -> str:
        """Build HTML company details section (only for company orders)."""
        company_name = order.get("company_name")
        if not company_name:
            return ""
        name_esc = html.escape(str(company_name))
        lines = [f"<strong>{name_esc}</strong>"]
        ico = order.get("company_ico")
        if ico:
            lines.append(f"I\u010cO: {html.escape(str(ico))}")
        dic = order.get("company_dic")
        if dic:
            lines.append(f"DI\u010c: {html.escape(str(dic))}")
        ic_dph = order.get("company_ic_dph")
        if ic_dph:
            lines.append(f"I\u010c DPH: {html.escape(str(ic_dph))}")
        return self._build_section(
            "Firemn\u00e9 \u00fadaje",
            f'<p style="margin:0; line-height:1.6;">{"<br>".join(lines)}</p>',
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

        lines = [f"<strong>{name}</strong>"]
        if name2:
            lines.append(name2)
        if street:
            lines.append(street)
        if city or zip_code:
            lines.append(f"{zip_code} {city}".strip())
        if country:
            lines.append(country)

        return self._build_section(
            html.escape(title),
            f'<p style="margin:0; line-height:1.6;">{"<br>".join(lines)}</p>',
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
