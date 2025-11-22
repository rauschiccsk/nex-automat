#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deployment Preparation Script
Validates all prerequisites before customer deployment
Based on DAY 4 lessons learned: 2025-11-22
"""

import sys
import os
from pathlib import Path

print("Deployment Preparation Check")
print("=" * 80)
print()
print("Critical Checks (DAY 4 Lessons):")
print()

# Check 1: PostgreSQL Password
pg_pass = os.getenv('POSTGRES_PASSWORD')
if pg_pass:
    print("[OK] POSTGRES_PASSWORD set")
else:
    print("[ERROR] POSTGRES_PASSWORD not set!")
    print("  Fix: setx POSTGRES_PASSWORD \"your_password\"")

# Check 2: API Key  
api_key = os.getenv('LS_API_KEY')
if api_key:
    print("[OK] LS_API_KEY set")
else:
    print("[ERROR] LS_API_KEY not set! (DAY 4 CRITICAL)")
    print("  Fix: setx LS_API_KEY \"your_api_key\"")

# Check 3: Dependencies
print()
print("Checking critical dependencies...")
try:
    import pdfplumber
    print("[OK] pdfplumber installed")
except ImportError:
    print("[ERROR] pdfplumber missing! (DAY 4 CRITICAL)")
    print("  Fix: pip install pdfplumber")

try:
    import pg8000
    print("[OK] pg8000 installed")
except ImportError:
    print("[ERROR] pg8000 missing! (DAY 4 CRITICAL)")
    print("  Fix: pip install pg8000")

print()
print("=" * 80)
print("Review output above and fix any [ERROR] items before deployment")
