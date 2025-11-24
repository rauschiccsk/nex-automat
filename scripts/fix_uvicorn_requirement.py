#!/usr/bin/env python
"""Fix uvicorn[standard] -> uvicorn in requirements.txt

Problem: uvicorn[standard] includes httptools which requires C++ compiler.
Solution: Use plain uvicorn without [standard] extras.
"""

from pathlib import Path


def main():
    req_file = Path("apps/supplier-invoice-loader/requirements.txt")

    if not req_file.exists():
        print(f"[FAIL] File not found: {req_file}")
        return 1

    content = req_file.read_text(encoding="utf-8")

    if "uvicorn[standard]" not in content:
        print("[INFO] uvicorn[standard] not found - already fixed or different format")
        return 0

    new_content = content.replace("uvicorn[standard]==0.32.0", "uvicorn==0.32.0")
    req_file.write_text(new_content, encoding="utf-8")

    print("[OK] Fixed: uvicorn[standard]==0.32.0 -> uvicorn==0.32.0")
    return 0


if __name__ == "__main__":
    exit(main())