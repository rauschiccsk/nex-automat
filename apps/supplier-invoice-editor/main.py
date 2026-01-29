"""
Supplier Invoice Editor - Main Entry Point
"""

import sys

from PyQt5.QtWidgets import QApplication
from src.config import Config
from src.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Supplier Invoice Editor")
    app.setOrganizationName("ICC Komárno")

    # Initialize config
    config = Config()

    # Create and show main window
    window = MainWindow(config)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
