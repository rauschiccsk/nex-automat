"""Application setup"""
import sys
import os

# Suppress Qt6 RDP monitor detection warning
os.environ["QT_LOGGING_RULES"] = "qt.qpa.screen=false"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from config.settings import Settings


def main() -> int:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Supplier Invoice Staging")
    app.setOrganizationName("ICC")
    app.setApplicationVersion("1.0.0")

    settings = Settings()
    window = MainWindow(settings)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
