"""
Cleanup Script for Development and Deployment Environments
Removes test data, temporary files, logs, and cache
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime


class EnvironmentCleanup:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.is_development = "Development" in str(self.current_dir)
        self.is_deployment = "Deployment" in str(self.current_dir)

        self.removed_files = 0
        self.removed_dirs = 0
        self.freed_bytes = 0

    def format_size(self, bytes_count):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} TB"

    def remove_file(self, file_path):
        """Remove single file"""
        try:
            size = file_path.stat().st_size
            file_path.unlink()
            self.removed_files += 1
            self.freed_bytes += size
            return True
        except Exception as e:
            print(f"  [ERROR] Failed to remove {file_path.name}: {e}")
            return False

    def remove_directory(self, dir_path):
        """Remove directory"""
        try:
            # Calculate size before removal
            total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
            file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())

            shutil.rmtree(dir_path)
            self.removed_dirs += 1
            self.removed_files += file_count
            self.freed_bytes += total_size
            return True
        except Exception as e:
            print(f"  [ERROR] Failed to remove {dir_path.name}: {e}")
            return False

    def cleanup_python_cache(self):
        """Remove __pycache__ directories"""
        print("\n[1/8] Cleaning Python cache...")

        cache_dirs = list(self.current_dir.rglob("__pycache__"))

        if cache_dirs:
            print(f"  Found {len(cache_dirs)} __pycache__ directories")
            for cache_dir in cache_dirs:
                if self.remove_directory(cache_dir):
                    print(f"  Removed: {cache_dir.relative_to(self.current_dir)}")
        else:
            print("  No cache directories found")

    def cleanup_test_coverage(self):
        """Remove test coverage files"""
        print("\n[2/8] Cleaning test coverage...")

        patterns = [
            ".coverage",
            "htmlcov",
            ".pytest_cache",
            "coverage.xml"
        ]

        for pattern in patterns:
            for item in self.current_dir.rglob(pattern):
                if item.is_file():
                    if self.remove_file(item):
                        print(f"  Removed: {item.relative_to(self.current_dir)}")
                elif item.is_dir():
                    if self.remove_directory(item):
                        print(f"  Removed: {item.relative_to(self.current_dir)}/")

    def cleanup_backup_files(self):
        """Remove backup files"""
        print("\n[3/8] Cleaning backup files...")

        patterns = ["*.backup", "*.bak", "*.old"]

        for pattern in patterns:
            for backup_file in self.current_dir.rglob(pattern):
                if backup_file.is_file():
                    if self.remove_file(backup_file):
                        print(f"  Removed: {backup_file.relative_to(self.current_dir)}")

    def cleanup_logs(self):
        """Clean old log files"""
        print("\n[4/8] Cleaning log files...")

        log_patterns = [
            "logs/*.log",
            "apps/*/logs/*.log",
            "*.log"
        ]

        for pattern in log_patterns:
            for log_file in self.current_dir.glob(pattern):
                if log_file.is_file():
                    # Keep recent logs in deployment
                    if self.is_deployment:
                        age_days = (datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)).days
                        if age_days < 7:
                            print(f"  Keeping recent log: {log_file.name}")
                            continue

                    if self.remove_file(log_file):
                        print(f"  Removed: {log_file.relative_to(self.current_dir)}")

    def cleanup_temp_files(self):
        """Remove temporary files"""
        print("\n[5/8] Cleaning temporary files...")

        temp_patterns = ["*.tmp", "*.temp", "~*"]

        for pattern in temp_patterns:
            for temp_file in self.current_dir.rglob(pattern):
                if temp_file.is_file():
                    if self.remove_file(temp_file):
                        print(f"  Removed: {temp_file.relative_to(self.current_dir)}")

    def cleanup_sqlite_databases(self):
        """Clean SQLite test databases"""
        print("\n[6/8] Cleaning SQLite databases...")

        # Only in development or if explicitly requested
        if self.is_development:
            for db_file in self.current_dir.rglob("*.db"):
                # Skip if in production config directory
                if "config" in str(db_file.parent):
                    print(f"  Skipping production DB: {db_file.name}")
                    continue

                if self.remove_file(db_file):
                    print(f"  Removed: {db_file.relative_to(self.current_dir)}")
        else:
            print("  Skipped (deployment environment)")

    def cleanup_egg_info(self):
        """Remove .egg-info directories"""
        print("\n[7/8] Cleaning .egg-info directories...")

        for egg_dir in self.current_dir.rglob("*.egg-info"):
            if egg_dir.is_dir():
                if self.remove_directory(egg_dir):
                    print(f"  Removed: {egg_dir.relative_to(self.current_dir)}/")

    def cleanup_build_artifacts(self):
        """Remove build artifacts"""
        print("\n[8/8] Cleaning build artifacts...")

        build_dirs = ["build", "dist"]

        for build_dir_name in build_dirs:
            for build_dir in self.current_dir.rglob(build_dir_name):
                if build_dir.is_dir() and build_dir.parent.name in ["packages", "apps"]:
                    if self.remove_directory(build_dir):
                        print(f"  Removed: {build_dir.relative_to(self.current_dir)}/")

    def print_summary(self):
        """Print cleanup summary"""
        print("\n" + "=" * 80)
        print("CLEANUP SUMMARY")
        print("=" * 80)
        print()
        print(
            f"Environment:    {'Development' if self.is_development else 'Deployment' if self.is_deployment else 'Unknown'}")
        print(f"Files removed:  {self.removed_files}")
        print(f"Dirs removed:   {self.removed_dirs}")
        print(f"Space freed:    {self.format_size(self.freed_bytes)}")
        print()
        print("=" * 80)

    def run(self):
        """Run cleanup"""
        print("=" * 80)
        print("ENVIRONMENT CLEANUP")
        print("=" * 80)
        print()
        print(f"Location: {self.current_dir}")
        print(f"Type: {'Development' if self.is_development else 'Deployment' if self.is_deployment else 'Unknown'}")
        print()

        # Confirm in deployment
        if self.is_deployment:
            print("WARNING: Running cleanup in DEPLOYMENT environment!")
            response = input("Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Cleanup cancelled")
                return 1

        self.cleanup_python_cache()
        self.cleanup_test_coverage()
        self.cleanup_backup_files()
        self.cleanup_logs()
        self.cleanup_temp_files()
        self.cleanup_sqlite_databases()
        self.cleanup_egg_info()
        self.cleanup_build_artifacts()

        self.print_summary()

        return 0


if __name__ == "__main__":
    cleanup = EnvironmentCleanup()
    sys.exit(cleanup.run())