# -*- coding: utf-8 -*-
"""
MARSO Invoice Loader - PDF Data Extraction
Extracts invoice data from MARSO (Hungarian tire supplier) PDF invoices
Bilingual HU/EN format, EU intra-community (0% VAT)
"""

import re
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from decimal import Decimal

logger = logging.getLogger(__name__)


@dataclass
class MarsoInvoiceItem:
    """Jedna položka na MARSO faktúre"""

    line_number: int
    customs_code: str = ""  # Colný kód (4011100000)
    description: str = ""  # Popis pneumatiky
    quantity: Optional[Decimal] = None
    unit: str = "Pcs"
    unit_price: Optional[Decimal] = None
    total: Optional[Decimal] = None
    vat_rate: Optional[Decimal] = Decimal("0")  # EU intra-community = 0%


@dataclass
class MarsoInvoiceData:
    """Kompletné dáta z MARSO faktúry"""

    # Hlavička
    invoice_number: str = ""  # 11925-10338
    issue_date: str = ""  # YYYY.MM.DD
    due_date: str = ""
    tax_point_date: str = ""
    sales_order: str = ""  # VR3696263

    # Sumy
    total_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = Decimal("0")  # 0% VAT
    net_amount: Optional[Decimal] = None
    currency: str = "EUR"

    # Dodávateľ (MARSO)
    supplier_name: str = "MARSO-TYRE Kft."
    supplier_tax_number: str = ""  # 10428342-2-15
    supplier_eu_vat: str = ""  # HU10428342
    supplier_iban: str = ""
    supplier_swift: str = ""
    supplier_address: str = ""

    # Odberateľ
    customer_name: str = ""
    customer_eu_vat: str = ""  # SK2120582200
    customer_address: str = ""

    # Položky
    items: List[MarsoInvoiceItem] = field(default_factory=list)


class MarsoInvoiceExtractor:
    """Extraktor pre MARSO faktúry (maďarský dodávateľ pneumatík)"""

    def __init__(self):
        self.patterns = self._init_patterns()

    def _init_patterns(self) -> Dict[str, str]:
        """Inicializácia regex patterns pre MARSO faktúry"""
        return {
            # Hlavička - MARSO formát (� je pomlčka v PDF encoding)
            "invoice_number": r"Sz.mlasz.m\s*\n\s*\w+\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{5}.\d{5})",
            "sales_order": r"(?:Sales\s+order|Rendel.s\s+sz.m)[.:\s]*(VR\d+)",
            # Sumy - maďarský formát (medzery v tisícoch, čiarka ako desatinná)
            "total_amount": r"(?:Grand\s+total|.sszesen)[:\s]*([\d\s,.]+)\s*EUR",
            "net_amount": r"(?:Net\s+value|Nett.\s+.rt.k)[:\s]*([\d\s,.]+)\s*EUR",
            # Dodávateľ (MARSO)
            "supplier_name": r"Marso\s+Kft",
            "supplier_tax_number": r"(?:Tax\s+number|Ad.sz.m)[.:\s]*(\d{8}.\d.\d{2})",
            "supplier_eu_vat": r"EU\s+VAT\s+No\.[^:]*:\s*(HU\d{8,11})",
            "supplier_iban": r"IBAN[^:]*:\s*([A-Z]{2}\d{2}[\d\s]{20,30})",
            "supplier_swift": r"Swift[^:]*:\s*([A-Z]{6,11})",
            # Odberateľ
            "customer_name": r"Customer\s*/\s*Vev.\s*\n\s*Marso[^\n]+\n[^\n]+\n([^\n]+)",
            "customer_eu_vat": r"EU\s+VAT\s+No\.[^:]*:\s*(SK\d{10})",
        }

    def extract_from_pdf(self, pdf_path: str) -> Optional[MarsoInvoiceData]:
        """
        Hlavná metóda - extrahuje dáta z PDF

        Args:
            pdf_path: Cesta k PDF súboru

        Returns:
            MarsoInvoiceData alebo None ak extraction zlyhal
        """
        try:
            import pdfplumber

            logger.info(f"MARSO: Extracting data from: {pdf_path}")

            # Otvor PDF a extrahuj text
            text = self._extract_text_from_pdf(pdf_path, pdfplumber)

            if not text:
                logger.error("MARSO: No text extracted from PDF")
                return None

            # Extrahuj hlavičku
            invoice_data = self._extract_header(text)

            # Extrahuj položky
            items = self._extract_items(text)
            invoice_data.items = items

            # Ak net_amount nie je, vypočítaj zo sumy položiek
            if not invoice_data.net_amount and items:
                invoice_data.net_amount = sum(item.total for item in items if item.total)

            logger.info(f"MARSO: Extracted: {invoice_data.invoice_number}, {len(items)} items")
            return invoice_data

        except Exception as e:
            logger.error(f"MARSO: Error extracting from PDF: {e}", exc_info=True)
            return None

    def _extract_text_from_pdf(self, pdf_path: str, pdfplumber) -> str:
        """Extrahuje text z PDF pomocou pdfplumber"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _extract_header(self, text: str) -> MarsoInvoiceData:
        """Extrahuje hlavičku faktúry"""
        data = MarsoInvoiceData()

        # Špeciálne spracovanie pre invoice_number a dátumy (sú v jednom riadku)
        # Format: prepayment 2025.10.29 2025.10.29 2025.10.30 11925-10338
        date_line = re.search(
            r"(?:prepayment|transfer)\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{4}\.\d{2}\.\d{2})\s+(\d{5}.\d{5})",
            text,
            re.IGNORECASE,
        )
        if date_line:
            data.issue_date = self._convert_date_format(date_line.group(1))
            data.tax_point_date = self._convert_date_format(date_line.group(2))
            data.due_date = self._convert_date_format(date_line.group(3))
            # Invoice number - nahraď špeciálny znak pomlčkou
            data.invoice_number = re.sub(r"[^0-9]", "-", date_line.group(4))

        # Sales order
        sales_match = re.search(self.patterns["sales_order"], text, re.IGNORECASE)
        if sales_match:
            data.sales_order = sales_match.group(1)

        # EU VAT numbers
        supplier_vat = re.search(self.patterns["supplier_eu_vat"], text)
        if supplier_vat:
            data.supplier_eu_vat = supplier_vat.group(1)

        customer_vat = re.search(self.patterns["customer_eu_vat"], text)
        if customer_vat:
            data.customer_eu_vat = customer_vat.group(1)

        # Tax number
        tax_match = re.search(self.patterns["supplier_tax_number"], text)
        if tax_match:
            data.supplier_tax_number = re.sub(r"[^0-9]", "-", tax_match.group(1))

        # IBAN
        iban_match = re.search(self.patterns["supplier_iban"], text)
        if iban_match:
            data.supplier_iban = re.sub(r"\s+", "", iban_match.group(1))

        # SWIFT
        swift_match = re.search(self.patterns["supplier_swift"], text)
        if swift_match:
            data.supplier_swift = swift_match.group(1)

        # Customer name - Andros s.r.o.
        customer_match = re.search(
            r"Customer\s*/\s*Vev.+?\n.+?\n.+?\n\s*(.+?)\s*\n", text, re.IGNORECASE
        )
        if customer_match:
            data.customer_name = customer_match.group(1).strip()

        # Total amount - formát: "26 295,71 0,00 0,00 26 295,71 EUR"
        # Hľadaj všetky výskyty číslo + EUR a vezmi najväčšie
        all_eur_amounts = re.findall(r"(\d[\d\s]*[,.][\d]+)\s*EUR", text)
        if all_eur_amounts:
            amounts = []
            for amt in all_eur_amounts:
                parsed = self._parse_hungarian_decimal(amt)
                if parsed:
                    amounts.append(parsed)
            if amounts:
                data.total_amount = max(amounts)  # Najväčšia suma je total

        # Hardcoded pre MARSO
        data.supplier_name = "Marso Kft. Nyíregyháza"
        data.currency = "EUR"
        data.tax_amount = Decimal("0")  # EU intra-community

        return data

    def _extract_items(self, text: str) -> List[MarsoInvoiceItem]:
        """
        Extrahuje položky z tabuľky faktúry

        MARSO formát (príklad):
        1 4011100000 Szgk. gumiabroncs 2,00 Pcs 62,27 62,27 124,54
        MATADOR 205/50 R17 93V XL FR MP93 NORDICCA M+S 3PMSF ... (popis na ďalšom riadku)
        """
        items = []

        # Pattern pre MARSO položku
        # line_no customs_code short_desc qty unit list_price unit_price total
        item_pattern = re.compile(
            r"^(\d+)\s+"  # Číslo riadku
            r"(\d{10})\s+"  # Colný kód (10 číslic)
            r"([A-Za-z.]+(?:\s+[A-Za-z.]+)*)\s+"  # Krátky popis (Szgk. gumiabroncs)
            r"(\d+[,.]?\d*)\s+"  # Množstvo
            r"(Pcs|pcs)\s+"  # Jednotka
            r"(\d+[,.]?\d*)\s+"  # List price
            r"(\d+[,.]?\d*)\s+"  # Unit price
            r"(\d+[,.]?\d*)",  # Total
            re.MULTILINE,
        )

        # Nájdi všetky položky
        matches = list(item_pattern.finditer(text))

        for i, match in enumerate(matches):
            line_no = int(match.group(1))
            customs_code = match.group(2)
            short_desc = match.group(3).strip()
            quantity = self._parse_hungarian_decimal(match.group(4))
            unit = match.group(5)
            unit_price = self._parse_hungarian_decimal(match.group(7))  # unit price je group 7
            total = self._parse_hungarian_decimal(match.group(8))

            # Nájdi plný popis na nasledujúcom riadku (obsahuje značku pneumatiky)
            end_pos = match.end()
            next_match_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            between_text = text[end_pos:next_match_pos]

            # Prvý riadok za položkou je plný popis
            desc_match = re.search(r"\n([A-Z][A-Z0-9\s/]+(?:R\d{2}|/\d{2})[^\n]+)", between_text)
            full_description = desc_match.group(1).strip() if desc_match else short_desc

            item = MarsoInvoiceItem(
                line_number=line_no,
                customs_code=customs_code,
                description=full_description,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                total=total,
                vat_rate=Decimal("0"),
            )
            items.append(item)

        logger.info(f"MARSO: Extracted {len(items)} items from table")
        return items

    def _convert_date_format(self, date_str: str) -> str:
        """
        Konvertuje YYYY.MM.DD na DD.MM.YYYY

        Args:
            date_str: Dátum v MARSO formáte (2025.01.15)

        Returns:
            Dátum v SK formáte (15.01.2025)
        """
        try:
            # Odstráň medzery
            date_str = date_str.replace(" ", "")

            # Parsuj YYYY.MM.DD
            match = re.match(r"(\d{4})\.(\d{2})\.(\d{2})", date_str)
            if match:
                year, month, day = match.groups()
                return f"{day}.{month}.{year}"

            return date_str
        except:
            return date_str

    def _parse_hungarian_decimal(self, value: Optional[str]) -> Optional[Decimal]:
        """
        Parsuje maďarský formát čísla na Decimal

        Maďarský formát: 2 647,40 (medzery v tisícoch, čiarka ako desatinná)
        Výstup: 2647.40

        Args:
            value: String s číslom

        Returns:
            Decimal alebo None
        """
        if not value:
            return None
        try:
            # Odstráň medzery (tisíce)
            value = value.replace(" ", "")
            # Zmeň čiarku na bodku (desatinná)
            value = value.replace(",", ".")
            return Decimal(value)
        except:
            return None


# Pomocná funkcia pre použitie v main.py
def extract_marso_invoice(pdf_path: str) -> Optional[MarsoInvoiceData]:
    """
    Wrapper funkcia pre extrahovanie MARSO faktúr

    Usage:
        from extractors.marso_extractor import extract_marso_invoice
        data = extract_marso_invoice("/path/to/marso_invoice.pdf")
        if data:
            print(f"Invoice: {data.invoice_number}")
            print(f"Items: {len(data.items)}")
            for item in data.items:
                print(f"  {item.customs_code} {item.description}: {item.total} EUR")
    """
    extractor = MarsoInvoiceExtractor()
    return extractor.extract_from_pdf(pdf_path)


def detect_marso_invoice(text: str) -> bool:
    """
    Detekuje či text pochádza z MARSO faktúry

    Args:
        text: Text extrahovaný z PDF

    Returns:
        True ak je to MARSO faktúra
    """
    marso_indicators = [
        r"MARSO",
        r"HU\d{8,11}",  # Hungarian EU VAT
        r"\d{5}-\d{5}",  # MARSO invoice number format
        r"Számla",  # Hungarian word for invoice
        r"Fizetési\s+határidő",  # Hungarian "due date"
    ]

    for pattern in marso_indicators:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def detect_marso_invoice_from_pdf(pdf_path: str) -> bool:
    """
    Detekuje či PDF je MARSO faktúra

    Args:
        pdf_path: Cesta k PDF súboru

    Returns:
        True ak je to MARSO faktúra
    """
    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            # Stačí prvá strana
            if pdf.pages:
                text = pdf.pages[0].extract_text() or ""
                return detect_marso_invoice(text)
    except Exception as e:
        logger.warning(f"Error detecting MARSO invoice: {e}")
    return False


def convert_to_standard_invoice_data(marso_data: MarsoInvoiceData):
    """
    Konvertuje MarsoInvoiceData na štandardný InvoiceData formát

    Args:
        marso_data: MARSO invoice data

    Returns:
        InvoiceData objekt kompatibilný s ISDOC generátorom
    """
    from src.extractors.ls_extractor import InvoiceData, InvoiceItem

    # Konvertuj položky
    items = []
    for mi in marso_data.items:
        item = InvoiceItem(
            line_number=mi.line_number,
            item_code=mi.customs_code,  # Colný kód ako item_code
            ean_code="",
            description=mi.description,
            quantity=mi.quantity,
            unit=mi.unit,
            unit_price_no_vat=mi.unit_price,  # MARSO je bez DPH (EU intra)
            unit_price_with_vat=mi.unit_price,  # Rovnaké (0% DPH)
            total_with_vat=mi.total,
            vat_rate=Decimal("0"),  # EU intra-community
            discount_percent=None,
        )
        items.append(item)

    # Konvertuj hlavičku
    invoice = InvoiceData(
        invoice_number=marso_data.invoice_number,
        issue_date=marso_data.issue_date,
        due_date=marso_data.due_date,
        tax_point_date=marso_data.tax_point_date,
        total_amount=marso_data.total_amount,
        tax_amount=Decimal("0"),  # EU intra-community = 0% DPH
        net_amount=marso_data.total_amount,  # Net = Total pre 0% DPH
        currency=marso_data.currency,
        # Dodávateľ - MARSO (maďarský)
        supplier_name=marso_data.supplier_name,
        supplier_ico="",  # Maďarsko nemá IČO
        supplier_dic=marso_data.supplier_tax_number,  # Tax number ako DIČ
        supplier_icdph=marso_data.supplier_eu_vat,  # HU VAT
        supplier_address="",
        # Odberateľ
        customer_name=marso_data.customer_name,
        customer_ico="",  # Vyplní sa z DB lookup ak treba
        customer_dic="",
        customer_icdph=marso_data.customer_eu_vat,  # SK VAT
        customer_address="",
        # Bankové údaje
        bank_name="K&H Bank",
        iban=marso_data.supplier_iban,
        bic=marso_data.supplier_swift,
        variable_symbol=marso_data.invoice_number.replace("-", ""),  # 1192510338
        constant_symbol="",
        items=items,
    )

    return invoice


def extract_marso_as_standard(pdf_path: str):
    """
    Extrahuje MARSO faktúru a vráti štandardný InvoiceData

    Toto je hlavná funkcia pre integráciu do pipeline.

    Args:
        pdf_path: Cesta k PDF

    Returns:
        InvoiceData alebo None
    """
    marso_data = extract_marso_invoice(pdf_path)
    if marso_data:
        return convert_to_standard_invoice_data(marso_data)
    return None
