"""
RAG API Server startup script.
Starts FastAPI server for RAG system endpoints.
"""

import subprocess
import sys


class RAGServer:
    """RAG API Server manager."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.process: subprocess.Popen | None = None

    def start(self, reload: bool = False, log_level: str = "info"):
        """
        Start RAG API server.

        Args:
            reload: Enable auto-reload on code changes (development mode)
            log_level: Logging level (debug, info, warning, error)
        """
        print("=" * 60)
        print("Starting RAG API Server")
        print("=" * 60)
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        print(f"URL: http://{self.host}:{self.port}")
        print(f"Reload: {reload}")
        print(f"Log Level: {log_level}")
        print("=" * 60)

        # Build uvicorn command
        cmd = [
            "uvicorn",
            "tools.rag.server_app:app",
            "--host",
            self.host,
            "--port",
            str(self.port),
            "--log-level",
            log_level,
        ]

        if reload:
            cmd.append("--reload")

        try:
            # Start server process - capture both stdout and stderr
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            print("\n[OK] Server starting...")
            print(f"\nAccess the API at: http://{self.host}:{self.port}")
            print(f"API docs: http://{self.host}:{self.port}/docs")
            print("\nPress Ctrl+C to stop the server\n")
            print("=" * 60)

            # Stream output
            for line in self.process.stdout:
                print(line, end="")

        except KeyboardInterrupt:
            print("\n\n[!] Received shutdown signal")
            self.stop()

        except Exception as e:
            print(f"\n[ERROR] Failed to start server: {e}")
            sys.exit(1)

    def stop(self):
        """Stop RAG API server."""
        if self.process:
            print("[!] Stopping server...")
            self.process.terminate()

            # Wait for graceful shutdown
            try:
                self.process.wait(timeout=5)
                print("[OK] Server stopped")
            except subprocess.TimeoutExpired:
                print("[!] Force killing server...")
                self.process.kill()
                self.process.wait()
                print("[OK] Server killed")

    def status(self):
        """Check if server is running."""
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.host, self.port))
        sock.close()

        if result == 0:
            print(f"[OK] Server is running on http://{self.host}:{self.port}")
            return True
        else:
            print("[!] Server is not running")
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="RAG API Server Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server
  python -m tools.rag.server start
  
  # Start with auto-reload (development)
  python -m tools.rag.server start --reload
  
  # Start on different port
  python -m tools.rag.server start --port 9000
  
  # Check server status
  python -m tools.rag.server status
        """,
    )

    parser.add_argument("command", choices=["start", "status"], help="Server command")

    parser.add_argument(
        "--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port", type=int, default=8765, help="Server port (default: 8765)"
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes (development mode)",
    )

    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="Logging level (default: info)",
    )

    args = parser.parse_args()

    # Create server instance
    server = RAGServer(host=args.host, port=args.port)

    # Execute command
    if args.command == "start":
        server.start(reload=args.reload, log_level=args.log_level)
    elif args.command == "status":
        server.status()


if __name__ == "__main__":
    main()
