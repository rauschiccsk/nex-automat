"""
BaseWindow - Base class for all windows with persistence.
PySide6 version for NEX Automat.
"""

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from shared_pyside6.database import SettingsRepository


class BaseWindow(QMainWindow):
    """
    Base class for all windows in NEX Automat system.

    Features:
    - Automatic window settings load on open
    - Automatic window settings save on close
    - Position validation (multi-monitor support)
    - Maximize state persistence
    - Multi-user support (user_id)

    Usage:
        class MyWindow(BaseWindow):
            def __init__(self):
                super().__init__(
                    window_name="my_unique_window",
                    default_size=(800, 600),
                    default_pos=(100, 100)
                )
                self._setup_ui()
    """

    def __init__(
        self,
        window_name: str,
        default_size: tuple[int, int] = (800, 600),
        default_pos: tuple[int, int] = (100, 100),
        user_id: str = "default",
        auto_load: bool = True,
        parent: QWidget | None = None,
    ):
        """
        Initialize BaseWindow.

        Args:
            window_name: Unique window identifier (e.g., "invoice_editor_main")
            default_size: Default size (width, height) if no settings
            default_pos: Default position (x, y) if no settings
            user_id: User ID for multi-user support
            auto_load: If True, automatically load settings
            parent: Parent widget
        """
        super().__init__(parent)

        self._window_name = window_name
        self._default_size = default_size
        self._default_pos = default_pos
        self._user_id = user_id
        self._repository = SettingsRepository()

        # Set default geometry
        self.resize(*default_size)
        self.move(*default_pos)

        if auto_load:
            self._load_and_apply_settings()

    @property
    def window_name(self) -> str:
        """Return window name."""
        return self._window_name

    def _load_and_apply_settings(self) -> None:
        """Load and apply window settings from DB."""
        settings = self._repository.load_window_settings(self._window_name, self._user_id)

        if settings:
            # Validate position is on visible screen
            x, y = settings["x"], settings["y"]
            width, height = settings["width"], settings["height"]

            if self._is_position_valid(x, y, width, height):
                self.setGeometry(x, y, width, height)
            else:
                # Position not valid, use default
                self.resize(*self._default_size)
                self.move(*self._default_pos)

            # Restore maximized state
            if settings.get("is_maximized", False):
                self.showMaximized()

    def _is_position_valid(self, x: int, y: int, width: int, height: int) -> bool:
        """
        Check if position is valid (visible on any screen).

        Args:
            x, y: Position
            width, height: Size

        Returns:
            True if at least 50x50 pixels are visible on some screen
        """
        window_rect = QRect(x, y, width, height)

        for screen in QApplication.screens():
            screen_rect = screen.availableGeometry()
            intersection = window_rect.intersected(screen_rect)

            # At least 50x50 pixels must be visible
            if intersection.width() >= 50 and intersection.height() >= 50:
                return True

        return False

    def _save_settings(self) -> None:
        """Save window settings to DB."""
        # Don't save if minimized
        if self.isMinimized():
            return

        is_maximized = self.isMaximized()

        # If maximized, save normal geometry
        if is_maximized:
            geometry = self.normalGeometry()
        else:
            geometry = self.geometry()

        self._repository.save_window_settings(
            window_name=self._window_name,
            user_id=self._user_id,
            x=geometry.x(),
            y=geometry.y(),
            width=geometry.width(),
            height=geometry.height(),
            is_maximized=is_maximized,
        )

    def closeEvent(self, event) -> None:
        """Override closeEvent to save settings."""
        self._save_settings()
        super().closeEvent(event)

    def save_window_settings(self) -> None:
        """Manual save window settings (e.g., for Apply button)."""
        self._save_settings()

    def reload_window_settings(self) -> None:
        """Manual reload window settings."""
        self._load_and_apply_settings()

    def get_window_settings(self) -> dict | None:
        """
        Get current window settings from DB.

        Returns:
            dict: Settings or None
        """
        return self._repository.load_window_settings(self._window_name, self._user_id)

    def delete_window_settings(self) -> None:
        """Delete window settings from DB."""
        self._repository.delete_window_settings(self._window_name, self._user_id)
