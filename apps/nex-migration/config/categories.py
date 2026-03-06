"""
Migration category definitions with dependency graph.

Each category represents a logical unit of Btrieve → PostgreSQL migration.
Source tables are actual NEX Genesis (Btrieve) .BTR files.
"""

from dataclasses import dataclass, field


@dataclass
class MigrationCategory:
    code: str
    name: str
    description: str
    source_tables: list[str]
    target_tables: list[str]
    dependencies: list[str] = field(default_factory=list)


PAB = MigrationCategory(
    code="PAB",
    name="Katalóg partnerov",
    description="Partneri (zákazníci, dodávatelia) + pomocné tabuľky",
    source_tables=[
        "PAB",  # Partner Address Book — hlavná tabuľka
        "PAYLST",  # Platobné metódy (HOT, KAR, FAK, PRE...)
        "TRPLST",  # Dopravné metódy (KUR, OSO, POS, DOP...)
        "BANKLST",  # Bankový katalóg (kódy bánk SR)
        "PABACC",  # Bankové účty partnerov
        "PASUBC",  # Prevádzky partnerov (pobočky, sklady)
        "PAGLST",  # Kategórie partnerov (dodávatelia, odberatelia)
        "PANOTI",  # Textové polia partnerov (owner_name, notice, description)
        "PACNCT",  # Kontakty partnerov (adresy + osoby)
    ],
    target_tables=[
        "partner_catalog",
        "partner_catalog_extensions",
        "partner_catalog_addresses",
        "partner_catalog_contacts",
        "partner_catalog_bank_accounts",
        "partner_catalog_texts",
    ],
    dependencies=[],
)

GSC = MigrationCategory(
    code="GSC",
    name="Katalóg produktov",
    description="Produkty + skupiny, čiarové kódy, cenníky",
    source_tables=[
        "GSCAT",  # Hlavný katalóg produktov
        "MGLST",  # Produktové skupiny/kategórie
        "FGLST",  # Finančné skupiny
        "SGLST",  # Skladové skupiny
        "BARCODE",  # Čiarové kódy (sekundárne)
        "PLS",  # Cenníky
    ],
    target_tables=["products"],
    dependencies=[],
)

STK = MigrationCategory(
    code="STK",
    name="Skladové karty",
    description="Skladové karty zásob + pohyby",
    source_tables=["STK", "FIF", "STM"],
    target_tables=["stock_cards"],
    dependencies=["GSC"],
)

TSH = MigrationCategory(
    code="TSH",
    name="Dodávateľské dodacie listy",
    description="Príjemky od dodávateľov",
    source_tables=["TSH", "TSI", "TSN"],
    target_tables=["supplier_delivery_notes"],
    dependencies=["PAB", "GSC", "STK"],
)

ICB = MigrationCategory(
    code="ICB",
    name="Odberateľské faktúry",
    description="Faktúry vydané zákazníkom",
    source_tables=["ICB", "ICI"],
    target_tables=["customer_invoices"],
    dependencies=["PAB", "GSC"],
)

ISB = MigrationCategory(
    code="ISB",
    name="Dodávateľské faktúry",
    description="Faktúry prijaté od dodávateľov",
    source_tables=["ISH", "ISI"],
    target_tables=["supplier_invoices"],
    dependencies=["PAB", "GSC"],
)

OBJ = MigrationCategory(
    code="OBJ",
    name="Objednávky",
    description="Objednávky k dodávateľom",
    source_tables=["OBJ", "OBI"],
    target_tables=["purchase_orders"],
    dependencies=["PAB", "GSC"],
)

DOD = MigrationCategory(
    code="DOD",
    name="Dodacie listy",
    description="Dodacie listy odberateľom",
    source_tables=["DOD", "DOI"],
    target_tables=["delivery_notes"],
    dependencies=["PAB", "GSC"],
)

PAYJRN = MigrationCategory(
    code="PAYJRN",
    name="Platobný denník",
    description="Platby a úhrady faktúr",
    source_tables=["PAYJRN"],
    target_tables=["payment_journal"],
    dependencies=["ICB", "ISB"],
)


CATEGORIES: dict[str, MigrationCategory] = {
    "PAB": PAB,
    "GSC": GSC,
    "STK": STK,
    "TSH": TSH,
    "ICB": ICB,
    "ISB": ISB,
    "OBJ": OBJ,
    "DOD": DOD,
    "PAYJRN": PAYJRN,
}


def get_category(code: str) -> MigrationCategory:
    """Get category by code, raise KeyError if not found."""
    if code not in CATEGORIES:
        raise KeyError(
            f"Unknown migration category: {code}. Available: {list(CATEGORIES.keys())}"
        )
    return CATEGORIES[code]


def check_dependencies(code: str, completed: set[str]) -> list[str]:
    """Return list of unmet dependencies for given category."""
    category = get_category(code)
    return [dep for dep in category.dependencies if dep not in completed]


def get_migration_order() -> list[str]:
    """Topological sort — returns categories in valid execution order."""
    order: list[str] = []
    remaining = set(CATEGORIES.keys())
    completed: set[str] = set()

    while remaining:
        ready = [code for code in remaining if not check_dependencies(code, completed)]
        if not ready:
            raise ValueError(f"Circular dependency detected! Remaining: {remaining}")
        order.extend(sorted(ready))
        completed.update(ready)
        remaining -= set(ready)

    return order
