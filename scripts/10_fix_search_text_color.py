"""
Fix: Change search editor text color to black for better readability.
"""
import os

TARGET_FILE = r"packages\shared-pyside6\shared_pyside6\ui\quick_search.py"

OLD_STYLE = '''    def _setup_appearance(self) -> None:
        """Setup green background and styling."""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #90EE90;
                border: 1px solid #228B22;
                padding: 2px 4px;
                font-size: 12px;
            }
        """)'''

NEW_STYLE = '''    def _setup_appearance(self) -> None:
        """Setup green background and styling."""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #90EE90;
                color: #000000;
                border: 1px solid #228B22;
                padding: 2px 4px;
                font-size: 12px;
            }
        """)'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_STYLE not in content:
        print("ERROR: OLD_STYLE not found")
        return False

    content = content.replace(OLD_STYLE, NEW_STYLE)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("- Search text color changed to black")
    return True


if __name__ == "__main__":
    main()