"""
Fix: Right-align numeric columns (Suma, Match%) and format to 2 decimal places.
"""
import os

TARGET_FILE = r"apps\supplier-invoice-staging\ui\main_window.py"

# Update _populate_model to handle alignment and formatting
OLD_POPULATE = '''    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''

NEW_POPULATE = '''    # Columns that should be right-aligned and formatted as decimals
    NUMERIC_COLUMNS = {"total_amount", "match_percent"}

    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")

                # Format numeric columns
                if col_key in self.NUMERIC_COLUMNS and value is not None:
                    try:
                        text = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        text = str(value) if value is not None else ""
                else:
                    text = str(value) if value is not None else ""

                item = QStandardItem(text)
                item.setEditable(False)

                # Right-align numeric columns
                if col_key in self.NUMERIC_COLUMNS:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_POPULATE not in content:
        print("ERROR: OLD_POPULATE not found")
        return False

    content = content.replace(OLD_POPULATE, NEW_POPULATE)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("- Suma and Match% now right-aligned")
    print("- Formatted to 2 decimal places")
    return True


if __name__ == "__main__":
    main()