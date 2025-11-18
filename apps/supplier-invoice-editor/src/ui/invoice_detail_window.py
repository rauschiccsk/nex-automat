"""
Invoice Detail Window - Display and edit invoice with items
"""

import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from decimal import Decimal

from .widgets.invoice_items_grid import InvoiceItemsGrid


class InvoiceDetailWindow(QDialog):
    """Dialog window for invoice detail and editing"""

    # Signal emitted when invoice is saved
    invoice_saved = pyqtSignal(int)  # invoice_id

    def __init__(self, invoice_service, invoice_id, parent=None):
        super().__init__(parent)

        self.invoice_service = invoice_service
        self.invoice_id = invoice_id
        self.logger = logging.getLogger(__name__)

        # Load data
        self.invoice = None
        self.items = []
        self._load_data()

        # Setup UI
        self._setup_ui()
        self._connect_signals()

        self.logger.info(f"Invoice detail window opened for ID: {invoice_id}")

    def _load_data(self):
        """Load invoice and items data"""
        try:
            self.invoice = self.invoice_service.get_invoice_by_id(self.invoice_id)
            if not self.invoice:
                raise ValueError(f"Invoice {self.invoice_id} not found")

            self.items = self.invoice_service.get_invoice_items(self.invoice_id)
            self.logger.info(f"Loaded invoice with {len(self.items)} items")

        except Exception as e:
            self.logger.exception("Failed to load invoice data")
            QMessageBox.critical(
                self,
                "Chyba",
                f"Nepodarilo sa načítať faktúru:\n\n{str(e)}"
            )
            self.reject()

    def _setup_ui(self):
        """Setup window UI"""
        self.setWindowTitle(f"Detail faktúry: {self.invoice['invoice_number']}")
        self.setMinimumSize(1200, 700)

        layout = QVBoxLayout(self)

        # Header group
        header_group = self._create_header_group()
        layout.addWidget(header_group)

        # Items grid
        items_label = QLabel("Položky faktúry:")
        items_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(items_label)

        self.items_grid = InvoiceItemsGrid(self.invoice_service)
        self.items_grid.set_items(self.items)
        layout.addWidget(self.items_grid)

        # Summary
        summary_group = self._create_summary_group()
        layout.addWidget(summary_group)

        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)

        self.logger.info("Invoice detail UI setup complete")

    def _create_header_group(self):
        """Create invoice header group box"""
        group = QGroupBox("Hlavička faktúry")
        layout = QFormLayout(group)

        # Invoice number
        invoice_number = QLabel(self.invoice['invoice_number'])
        invoice_number.setStyleSheet("font-weight: bold;")
        layout.addRow("Číslo faktúry:", invoice_number)

        # Date
        invoice_date = QLabel(self.invoice['invoice_date'])
        layout.addRow("Dátum faktúry:", invoice_date)

        # Supplier
        supplier_text = f"{self.invoice['supplier_name']} (IČO: {self.invoice['supplier_ico']})"
        supplier = QLabel(supplier_text)
        layout.addRow("Dodávateľ:", supplier)

        # Currency
        currency = QLabel(self.invoice['currency'])
        layout.addRow("Mena:", currency)

        # Status
        status_map = {
            'pending': 'Čaká na schválenie',
            'approved': 'Schválené',
            'rejected': 'Odmietnuté'
        }
        status_text = status_map.get(self.invoice['status'], self.invoice['status'])
        status = QLabel(status_text)
        status.setStyleSheet("color: orange; font-weight: bold;")
        layout.addRow("Stav:", status)

        return group

    def _create_summary_group(self):
        """Create summary group box"""
        group = QGroupBox("Súhrn")
        layout = QFormLayout(group)

        # Total will be calculated from items
        self.total_label = QLabel("0.00 EUR")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addRow("Celková suma:", self.total_label)

        self._update_summary()

        return group

    def _create_buttons(self):
        """Create button layout"""
        layout = QHBoxLayout()
        layout.addStretch()

        # Save button
        self.save_button = QPushButton("Uložiť (Ctrl+S)")
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self._on_save)
        layout.addWidget(self.save_button)

        # Cancel button
        cancel_button = QPushButton("Zrušiť (Escape)")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        return layout

    def _connect_signals(self):
        """Connect widget signals"""
        # When items change, update summary
        self.items_grid.items_changed.connect(self._update_summary)

    def _update_summary(self):
        """Update summary totals"""
        items = self.items_grid.get_items()

        total = Decimal('0.00')
        for item in items:
            item_total = Decimal(str(item.get('total_price', 0)))
            total += item_total

        self.total_label.setText(f"{float(total):.2f} {self.invoice['currency']}")

    def _on_save(self):
        """Handle save button click"""
        try:
            self.logger.info("Saving invoice changes...")

            # Get modified items
            items = self.items_grid.get_items()

            # Validate items
            if not items:
                QMessageBox.warning(
                    self,
                    "Upozornenie",
                    "Faktúra nemá žiadne položky!"
                )
                return

            # Save to database
            success = self.invoice_service.save_invoice(self.invoice_id, items)

            if success:
                self.logger.info("Invoice saved successfully")
                QMessageBox.information(
                    self,
                    "Úspech",
                    "Faktúra bola úspešne uložená."
                )

                # Emit signal and close
                self.invoice_saved.emit(self.invoice_id)
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Chyba",
                    "Nepodarilo sa uložiť faktúru."
                )

        except Exception as e:
            self.logger.exception("Failed to save invoice")
            QMessageBox.critical(
                self,
                "Chyba",
                f"Chyba pri ukladaní faktúry:\n\n{str(e)}"
            )

    def keyPressEvent(self, event):
        """Handle key press events"""
        # Ctrl+S to save
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self._on_save()
            event.accept()
        # Escape to cancel
        elif event.key() == Qt.Key_Escape:
            self.reject()
            event.accept()
        else:
            super().keyPressEvent(event)
