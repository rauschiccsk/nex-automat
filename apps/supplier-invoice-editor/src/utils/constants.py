"""
Konštanty pre identifikáciu okien a dialógov.

Window names používajú prefix 'sie' (Supplier Invoice Editor)
pre odlíšenie od iných aplikácií v zdieľanej window_settings.db.
"""

# Application prefix pre rozlíšenie okien rôznych aplikácií
APP_PREFIX = "sie"

# Main windows
WINDOW_MAIN = f"{APP_PREFIX}_main_window"
WINDOW_INVOICE_DETAIL = f"{APP_PREFIX}_invoice_detail"

# Dialogs (pre budúcnosť)
DIALOG_SETTINGS = f"{APP_PREFIX}_settings_dialog"
DIALOG_ABOUT = f"{APP_PREFIX}_about_dialog"

# Future windows (rezervované pre dokumentáciu)
# WINDOW_REPORTS = f"{APP_PREFIX}_reports_window"
# WINDOW_STATISTICS = f"{APP_PREFIX}_statistics_window"

# Grid identifiers
GRID_INVOICE_LIST = "invoice_list"
GRID_INVOICE_ITEMS = "invoice_items"
