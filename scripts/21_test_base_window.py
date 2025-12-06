"""
Test BaseWindow funkcionality
Inline import pre testing bez package installation.
"""
import sys
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import Qt, QRect

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Inline WindowSettingsDB
class WindowSettingsDB:
    """Database layer for window settings."""
    _instance = None
    _db_path = None

    def __new__(cls, db_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._db_path = db_path or r"C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db"
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        db_path = Path(self._db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS window_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                window_name TEXT NOT NULL,
                x INTEGER, y INTEGER,
                width INTEGER, height INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                window_state INTEGER DEFAULT 0,
                UNIQUE(user_id, window_name)
            )
        """)
        conn.commit()
        conn.close()

    def save(self, window_name: str, x: int, y: int, width: int, height: int,
             window_state: int = 0, user_id: str = "Server") -> bool:
        try:
            conn = sqlite3.connect(Path(self._db_path))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM window_settings WHERE user_id = ? AND window_name = ?",
                          (user_id, window_name))
            cursor.execute("""
                INSERT INTO window_settings
                (user_id, window_name, x, y, width, height, window_state, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, window_name, x, y, width, height, window_state, datetime.now()))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Save error: {e}")
            return False

    def load(self, window_name: str, user_id: str = "Server") -> Optional[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(Path(self._db_path))
            cursor = conn.cursor()
            cursor.execute("""
                SELECT x, y, width, height, window_state
                FROM window_settings WHERE user_id = ? AND window_name = ?
            """, (user_id, window_name))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'x': row[0], 'y': row[1],
                    'width': row[2], 'height': row[3],
                    'window_state': row[4] if len(row) > 4 else 0
                }
            return None
        except Exception as e:
            logger.error(f"Load error: {e}")
            return None


# Inline WindowPersistenceManager
class WindowPersistenceManager:
    """Window persistence manager."""
    MIN_X = -3840
    MIN_Y = 0
    MIN_WIDTH = 400
    MIN_HEIGHT = 300
    MAX_WIDTH = 3840
    MAX_HEIGHT = 2160

    @classmethod
    def validate_position(cls, x: int, y: int, width: int, height: int) -> bool:
        return (x >= cls.MIN_X and y >= cls.MIN_Y and
                cls.MIN_WIDTH <= width <= cls.MAX_WIDTH and
                cls.MIN_HEIGHT <= height <= cls.MAX_HEIGHT)

    @classmethod
    def get_safe_position(cls, settings: Optional[Dict[str, Any]],
                         default_size: Tuple[int, int] = (800, 600),
                         default_pos: Tuple[int, int] = (100, 100)) -> Dict[str, Any]:
        if settings is None:
            return {'x': default_pos[0], 'y': default_pos[1],
                    'width': default_size[0], 'height': default_size[1],
                    'window_state': 0}

        x, y = settings.get('x', default_pos[0]), settings.get('y', default_pos[1])
        width, height = settings.get('width', default_size[0]), settings.get('height', default_size[1])

        if not cls.validate_position(x, y, width, height):
            return {'x': default_pos[0], 'y': default_pos[1],
                    'width': default_size[0], 'height': default_size[1],
                    'window_state': 0}

        return {'x': x, 'y': y, 'width': width, 'height': height,
                'window_state': settings.get('window_state', 0)}


# Inline BaseWindow
class BaseWindow(QMainWindow):
    """Base window with automatic persistence."""

    def __init__(self, window_name: str,
                 default_size: Tuple[int, int] = (800, 600),
                 default_pos: Tuple[int, int] = (100, 100),
                 user_id: str = "Server", auto_load: bool = True, parent=None):
        super().__init__(parent)

        self._window_name = window_name
        self._default_size = default_size
        self._default_pos = default_pos
        self._user_id = user_id
        self._db = WindowSettingsDB()
        self._persistence = WindowPersistenceManager()

        if auto_load:
            self._load_and_apply_settings()

    def _load_and_apply_settings(self):
        settings = self._db.load(self._window_name, self._user_id)
        safe = self._persistence.get_safe_position(settings, self._default_size, self._default_pos)

        self.setGeometry(safe['x'], safe['y'], safe['width'], safe['height'])

        if safe.get('window_state', 0) == 2:
            self.setWindowState(Qt.WindowMaximized)
            logger.info(f"Window '{self._window_name}' loaded as MAXIMIZED")
        else:
            logger.info(f"Window '{self._window_name}' loaded at ({safe['x']}, {safe['y']}) [{safe['width']}x{safe['height']}]")

    def _save_settings(self):
        if self.isMaximized():
            norm = self.normalGeometry()
            self._db.save(self._window_name, norm.x(), norm.y(), norm.width(), norm.height(), 2, self._user_id)
            logger.info(f"Window '{self._window_name}' saved as MAXIMIZED")
        else:
            x, y, w, h = self.x(), self.y(), self.width(), self.height()
            if self._persistence.validate_position(x, y, w, h):
                self._db.save(self._window_name, x, y, w, h, 0, self._user_id)
                logger.info(f"Window '{self._window_name}' saved at ({x}, {y}) [{w}x{h}]")

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)

    @property
    def window_name(self):
        return self._window_name


# Test Window
class TestWindow(BaseWindow):
    def __init__(self):
        super().__init__(window_name="test_base_window", default_size=(600, 400), default_pos=(200, 200))
        self.setWindowTitle("BaseWindow Test")
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        info = QLabel(
            "BaseWindow Test\n\n"
            "1. Presúvaj okno\n"
            "2. Mení veľkosť\n"
            "3. Maximalizuj\n"
            "4. Zavri aplikáciu\n"
            "5. Spusti znova\n\n"
            "→ Okno sa otvorí v rovnakom stave"
        )
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        btn_max = QPushButton("Maximize")
        btn_max.clicked.connect(self.showMaximized)
        layout.addWidget(btn_max)

        btn_norm = QPushButton("Normal")
        btn_norm.clicked.connect(self.showNormal)
        layout.addWidget(btn_norm)


def main():
    print("=" * 80)
    print("BASEWINDOW TEST")
    print("=" * 80)

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()