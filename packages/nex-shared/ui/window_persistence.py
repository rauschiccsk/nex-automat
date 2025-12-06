"""
Window Persistence Manager
Validácia a persistence logika pre okná.
"""
import logging
from typing import Optional, Dict, Any, Tuple
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

logger = logging.getLogger(__name__)


class WindowPersistenceManager:
    """
    Manager pre window persistence s validáciou a multi-monitor supportom.

    Singleton pattern.
    """

    _instance = None

    # Validačné limity
    MIN_X = -3840  # Support pre dual 4K monitors naľavo
    MIN_Y = 0
    MIN_WIDTH = 400
    MIN_HEIGHT = 300
    MAX_WIDTH = 3840
    MAX_HEIGHT = 2160

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def validate_position(cls, x: int, y: int, width: int, height: int) -> bool:
        """
        Validuje či je window position platná.

        Args:
            x, y: Window position
            width, height: Window size

        Returns:
            bool: True ak je pozícia platná
        """
        is_valid = (
            x >= cls.MIN_X and
            y >= cls.MIN_Y and
            cls.MIN_WIDTH <= width <= cls.MAX_WIDTH and
            cls.MIN_HEIGHT <= height <= cls.MAX_HEIGHT
        )

        if not is_valid:
            logger.warning(
                f"Invalid window position: ({x}, {y}) [{width}x{height}] - "
                f"limits: x>={cls.MIN_X}, y>={cls.MIN_Y}, "
                f"{cls.MIN_WIDTH}<=w<={cls.MAX_WIDTH}, {cls.MIN_HEIGHT}<=h<={cls.MAX_HEIGHT}"
            )

        return is_valid

    @classmethod
    def get_monitor_geometry(cls, screen_index: int = 0) -> Optional[QRect]:
        """
        Vráti geometriu monitora.

        Args:
            screen_index: Index monitora (0 = primary)

        Returns:
            QRect: Geometria monitora alebo None
        """
        try:
            app = QApplication.instance()
            if app is None:
                logger.warning("QApplication instance not found")
                return None

            desktop = app.desktop()
            if screen_index >= desktop.screenCount():
                logger.warning(f"Screen index {screen_index} out of range")
                return None

            return desktop.screenGeometry(screen_index)

        except Exception as e:
            logger.error(f"Error getting monitor geometry: {e}")
            return None

    @classmethod
    def find_monitor_for_position(cls, x: int, y: int) -> int:
        """
        Nájde monitor ktorý obsahuje danú pozíciu.

        Args:
            x, y: Pozícia okna

        Returns:
            int: Index monitora alebo 0 (primary)
        """
        try:
            app = QApplication.instance()
            if app is None:
                return 0

            desktop = app.desktop()
            for i in range(desktop.screenCount()):
                geom = desktop.screenGeometry(i)
                if geom.contains(x, y):
                    return i

            return 0  # Default to primary monitor

        except Exception as e:
            logger.error(f"Error finding monitor: {e}")
            return 0

    @classmethod
    def get_safe_position(cls, 
                         settings: Optional[Dict[str, Any]],
                         default_size: Tuple[int, int] = (800, 600),
                         default_pos: Tuple[int, int] = (100, 100)) -> Dict[str, Any]:
        """
        Vráti bezpečnú pozíciu okna.

        Ak settings sú None alebo invalid, použije default hodnoty.

        Args:
            settings: Načítané settings z DB alebo None
            default_size: Default veľkosť (width, height)
            default_pos: Default pozícia (x, y)

        Returns:
            dict: Safe settings {'x', 'y', 'width', 'height', 'window_state'}
        """
        # Použiť default ak nie sú settings
        if settings is None:
            return {
                'x': default_pos[0],
                'y': default_pos[1],
                'width': default_size[0],
                'height': default_size[1],
                'window_state': 0
            }

        # Validovať settings
        x = settings.get('x', default_pos[0])
        y = settings.get('y', default_pos[1])
        width = settings.get('width', default_size[0])
        height = settings.get('height', default_size[1])
        window_state = settings.get('window_state', 0)

        # Ak je pozícia invalid, opraviť pozíciu ale ZACHOVAŤ rozmery z DB
        if not cls.validate_position(x, y, width, height):
            logger.info(f"Invalid position ({x}, {y}) - correcting but keeping size {width}x{height}")

            # Opraviť len pozíciu - posunúť okno na viditeľnú oblasť
            screen = QApplication.primaryScreen().geometry()

            # Ensure window fits on screen
            x = max(0, min(x, screen.width() - width))
            y = max(0, min(y, screen.height() - height))

            # If still doesn't fit, use default position but KEEP size from DB
            if x < 0 or y < 0:
                x = default_pos[0]
                y = default_pos[1]

            logger.info(f"Corrected position to ({x}, {y}) with original size {width}x{height}")

            return {
                'x': x,
                'y': y,
                'width': width,  # ✅ ZACHOVANÉ z DB!
                'height': height,  # ✅ ZACHOVANÉ z DB!
                'window_state': window_state  # ✅ ZACHOVANÉ z DB!
            }

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'window_state': window_state
        }

    @classmethod
    def log_monitor_info(cls):
        """Log info o všetkých monitoroch (pre debugging)."""
        try:
            app = QApplication.instance()
            if app is None:
                return

            desktop = app.desktop()
            screen_count = desktop.screenCount()

            logger.info(f"Detected {screen_count} monitor(s):")
            for i in range(screen_count):
                geom = desktop.screenGeometry(i)
                logger.info(
                    f"  Monitor {i}: "
                    f"pos=({geom.x()}, {geom.y()}), "
                    f"size={geom.width()}x{geom.height()}"
                )

        except Exception as e:
            logger.error(f"Error logging monitor info: {e}")
