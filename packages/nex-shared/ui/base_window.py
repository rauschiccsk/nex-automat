"""
BaseWindow - univerzálna base trieda pre všetky okná
Automatická window persistence (position, size, maximize state).
"""
import logging
from typing import Optional, Tuple
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

from ..database.window_settings_db import WindowSettingsDB
from .window_persistence import WindowPersistenceManager

logger = logging.getLogger(__name__)


class BaseWindow(QMainWindow):
    """
    Base trieda pre všetky okná v NEX Automat systéme.

    Automaticky:
    - Načíta window settings pri otvorení
    - Uloží window settings pri zatvorení
    - Validuje pozície
    - Podporuje multi-monitor
    - Persistence maximize state

    Použitie:
        class MyWindow(BaseWindow):
            def __init__(self):
                super().__init__(
                    window_name="my_unique_window",
                    default_size=(800, 600),
                    default_pos=(100, 100)
                )
                self.setup_ui()  # Tvoj UI
    """

    def __init__(self,
                 window_name: str,
                 default_size: Tuple[int, int] = (800, 600),
                 default_pos: Tuple[int, int] = (100, 100),
                 user_id: str = "Server",
                 auto_load: bool = True,
                 parent=None):
        """
        Inicializácia BaseWindow.

        Args:
            window_name: Jedinečný identifikátor okna (napr. "invoice_editor_main")
            default_size: Default veľkosť (width, height) ak nie sú settings
            default_pos: Default pozícia (x, y) ak nie sú settings
            user_id: User ID pre multi-user support
            auto_load: Ak True, automaticky načíta settings
            parent: Parent widget
        """
        super().__init__(parent)

        # Store parameters
        self._window_name = window_name
        self._default_size = default_size
        self._default_pos = default_pos
        self._user_id = user_id

        # Initialize managers
        self._db = WindowSettingsDB()
        self._persistence = WindowPersistenceManager()

        # Auto-load settings
        if auto_load:
            self._load_and_apply_settings()

    def _load_and_apply_settings(self):
        """Načíta a aplikuje window settings z DB."""
        try:
            # Load settings from DB
            settings = self._db.load(
                window_name=self._window_name,
                user_id=self._user_id
            )

            # Get safe position (with validation and fallback)
            safe_settings = self._persistence.get_safe_position(
                settings=settings,
                default_size=self._default_size,
                default_pos=self._default_pos
            )

            # Apply position and size separately to avoid frame geometry drift
            # Use move() for position and resize() for size
            self.move(safe_settings['x'], safe_settings['y'])
            self.resize(safe_settings['width'], safe_settings['height'])

            # Apply window state
            if safe_settings.get('window_state', 0) == 2:
                self.setWindowState(Qt.WindowMaximized)
                logger.info(f"Window '{self._window_name}' loaded as maximized")
            else:
                logger.info(
                    f"Window '{self._window_name}' loaded at "
                    f"({safe_settings['x']}, {safe_settings['y']}) "
                    f"[{safe_settings['width']}x{safe_settings['height']}]"
                )

        except Exception as e:
            logger.error(f"Error loading window settings for '{self._window_name}': {e}")
            # Fallback to defaults
            self.move(self._default_pos[0], self._default_pos[1])
            self.resize(self._default_size[0], self._default_size[1])

    def _save_settings(self):
        """Uloží window settings do DB."""
        try:
            if self.isMaximized():
                # Save normalGeometry (position before maximize)
                norm_geom = self.normalGeometry()
                self._db.save(
                    window_name=self._window_name,
                    x=norm_geom.x(),
                    y=norm_geom.y(),
                    width=norm_geom.width(),
                    height=norm_geom.height(),
                    window_state=2,  # Maximized
                    user_id=self._user_id
                )
                logger.info(f"Window '{self._window_name}' saved as maximized")
            else:
                # Normal window - get actual size
                x, y = self.x(), self.y()
                width, height = self.width(), self.height()

                # Validate and correct position if needed
                if not self._persistence.validate_position(x, y, width, height):
                    logger.warning(
                        f"Invalid position for '{self._window_name}': "
                        f"({x}, {y}) [{width}x{height}] - correcting"
                    )
                    # Correct position but keep actual size
                    x = max(0, min(x, 1920 - width))  # Keep on primary monitor
                    y = max(0, min(y, 1080 - height))

                # ALWAYS save (with corrected position if needed)
                self._db.save(
                    window_name=self._window_name,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    window_state=0,  # Normal
                    user_id=self._user_id
                )
                logger.info(
                    f"Window '{self._window_name}' saved at "
                    f"({x}, {y}) [{width}x{height}]"
                )

        except Exception as e:
            logger.error(f"Error saving window settings for '{self._window_name}': {e}")
    def closeEvent(self, event):
        """Override closeEvent to save settings."""
        self._save_settings()
        super().closeEvent(event)

    # Public API

    def save_window_settings(self):
        """Manuálne uloženie window settings (napr. pri Apply button)."""
        self._save_settings()

    def reload_window_settings(self):
        """Manuálne reload window settings."""
        self._load_and_apply_settings()

    def get_window_settings(self) -> Optional[dict]:
        """
        Získaj aktuálne window settings z DB.

        Returns:
            dict: Settings alebo None
        """
        return self._db.load(
            window_name=self._window_name,
            user_id=self._user_id
        )

    def delete_window_settings(self):
        """Vymaž window settings z DB."""
        self._db.delete(
            window_name=self._window_name,
            user_id=self._user_id
        )
        logger.info(f"Deleted settings for window '{self._window_name}'")

    @property
    def window_name(self) -> str:
        """Vráti window name."""
        return self._window_name
