"""
Log Manager for centralized logging with rotation and retention
Provides structured logging with automatic cleanup
"""

import logging
import logging.handlers
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass
import sys


@dataclass
class LogConfig:
    """Log manager configuration"""

    log_dir: Path
    log_filename: str = "supplier_invoice_loader.log"
    log_level: str = "INFO"

    # Rotation settings
    max_bytes: int = 10 * 1024 * 1024  # 10 MB
    backup_count: int = 5  # Keep 5 rotated files

    # Retention settings
    retention_days: int = 30

    # Format settings
    use_json: bool = False
    include_process_info: bool = True

    # Console output
    console_output: bool = True
    console_level: str = "INFO"


class JsonFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


class LogManager:
    """Centralized log management system"""

    def __init__(self, config: LogConfig):
        """
        Initialize log manager

        Args:
            config: Log configuration
        """
        self.config = config
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration"""
        # Create log directory
        self.config.log_dir.mkdir(parents=True, exist_ok=True)

        # Get root logger
        self.logger = logging.getLogger()
        self.logger.setLevel(getattr(logging, self.config.log_level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Add file handler with rotation
        log_file = self.config.log_dir / self.config.log_filename
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.config.max_bytes,
            backupCount=self.config.backup_count,
            encoding="utf-8",
        )

        # Set formatter
        if self.config.use_json:
            file_formatter = JsonFormatter()
        else:
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )

        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, self.config.log_level.upper()))
        self.logger.addHandler(file_handler)

        # Add console handler if enabled
        if self.config.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(getattr(logging, self.config.console_level.upper()))
            self.logger.addHandler(console_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get logger instance

        Args:
            name: Logger name (defaults to root)

        Returns:
            Logger instance
        """
        if name:
            return logging.getLogger(name)
        return self.logger

    def cleanup_old_logs(self, days: Optional[int] = None) -> int:
        """
        Remove log files older than retention period

        Args:
            days: Number of days to retain (uses config if not specified)

        Returns:
            Number of files deleted
        """
        retention_days = days or self.config.retention_days
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        deleted_count = 0

        # Find all log files
        for log_file in self.config.log_dir.glob("*.log*"):
            try:
                # Get file modification time
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)

                # Delete if older than retention period
                if file_time < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    self.logger.info(f"Deleted old log file: {log_file.name}")

            except Exception as e:
                self.logger.error(f"Error deleting log file {log_file}: {e}")

        return deleted_count

    def get_log_files(self) -> List[Path]:
        """
        Get list of all log files

        Returns:
            List of log file paths
        """
        return sorted(self.config.log_dir.glob("*.log*"))

    def get_log_stats(self) -> Dict:
        """
        Get log statistics

        Returns:
            Dictionary with log statistics
        """
        log_files = self.get_log_files()

        total_size = sum(f.stat().st_size for f in log_files)

        stats = {
            "log_directory": str(self.config.log_dir),
            "total_files": len(log_files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "current_log": str(self.config.log_dir / self.config.log_filename),
            "retention_days": self.config.retention_days,
            "log_level": self.config.log_level,
            "files": [],
        }

        for log_file in log_files:
            file_stat = log_file.stat()
            stats["files"].append(
                {
                    "name": log_file.name,
                    "size_kb": round(file_stat.st_size / 1024, 2),
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                }
            )

        return stats

    def analyze_logs(
        self, level: Optional[str] = None, since: Optional[datetime] = None, limit: int = 100
    ) -> List[Dict]:
        """
        Analyze log entries

        Args:
            level: Filter by log level
            since: Filter by timestamp
            limit: Maximum number of entries

        Returns:
            List of log entries
        """
        entries = []
        current_log = self.config.log_dir / self.config.log_filename

        if not current_log.exists():
            return entries

        try:
            with open(current_log, "r", encoding="utf-8") as f:
                for line in f:
                    if self.config.use_json:
                        try:
                            entry = json.loads(line)

                            # Apply filters
                            if level and entry.get("level") != level.upper():
                                continue

                            if since:
                                entry_time = datetime.fromisoformat(entry.get("timestamp", ""))
                                if entry_time < since:
                                    continue

                            entries.append(entry)

                        except json.JSONDecodeError:
                            continue
                    else:
                        # Parse standard format
                        if level and level.upper() not in line:
                            continue

                        entries.append({"raw": line.strip()})

                    if len(entries) >= limit:
                        break

        except Exception as e:
            self.logger.error(f"Error analyzing logs: {e}")

        return entries

    def get_error_summary(self, hours: int = 24) -> Dict:
        """
        Get summary of errors in recent period

        Args:
            hours: Number of hours to analyze

        Returns:
            Error summary statistics
        """
        since = datetime.now() - timedelta(hours=hours)

        errors = self.analyze_logs(level="ERROR", since=since, limit=1000)
        critical = self.analyze_logs(level="CRITICAL", since=since, limit=1000)

        summary = {
            "period_hours": hours,
            "error_count": len(errors),
            "critical_count": len(critical),
            "total_issues": len(errors) + len(critical),
            "recent_errors": errors[:10],  # Last 10 errors
            "recent_critical": critical[:10],  # Last 10 critical
        }

        return summary

    def set_level(self, level: str):
        """
        Change log level dynamically

        Args:
            level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        log_level = getattr(logging, level.upper())
        self.logger.setLevel(log_level)

        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.setLevel(log_level)

        self.config.log_level = level.upper()
        self.logger.info(f"Log level changed to {level.upper()}")

    def rotate_logs(self):
        """Force log rotation"""
        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.doRollover()
                self.logger.info("Log rotation triggered manually")


def setup_logging(
    log_dir: str = "logs", log_level: str = "INFO", use_json: bool = False, console: bool = True
) -> LogManager:
    """
    Quick setup for logging

    Args:
        log_dir: Log directory path
        log_level: Log level
        use_json: Use JSON formatting
        console: Enable console output

    Returns:
        LogManager instance
    """
    config = LogConfig(
        log_dir=Path(log_dir), log_level=log_level, use_json=use_json, console_output=console
    )

    return LogManager(config)
