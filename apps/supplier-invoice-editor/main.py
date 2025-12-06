#!/usr/bin/env python3
"""
Invoice Editor - Main Application Entry Point
Qt5 desktop application for ISDOC invoice approval
"""

import sys
from pathlib import Path

# Add nex-shared to path
nex_shared_path = Path(__file__).parent.parent.parent / 'packages' / 'nex-shared'
if str(nex_shared_path) not in sys.path:
    sys.path.insert(0, str(nex_shared_path))

import sys
import logging
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.main_window import MainWindow
from utils.config import Config


def setup_logging():
    """Configure application logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"supplier_invoice_editor_{datetime.now():%Y%m%d}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def main():
    """Main application entry point"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Invoice Editor starting...")

    try:
        # Load configuration
        config = Config()
        logger.info(f"Configuration loaded from: {config.config_path}")

        # Enable High DPI scaling
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("Invoice Editor")
        app.setOrganizationName("ICC Komárno")

        # Create and show main window
        logger.info("Creating main window...")
        window = MainWindow(config)
        window.show()

        logger.info("Application ready")

        # Run event loop
        exit_code = app.exec_()

        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code

    except Exception as e:
        logger.exception("Fatal error during startup")

        # Show error dialog if possible
        try:
            QMessageBox.critical(
                None,
                "Fatal Error",
                f"Application failed to start:\n\n{str(e)}\n\nCheck logs for details."
            )
        except:
            pass

        return 1


if __name__ == "__main__":
    sys.exit(main())
