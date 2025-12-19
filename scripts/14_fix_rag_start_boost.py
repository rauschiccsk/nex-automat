#!/usr/bin/env python
"""
Fix rag_service.py - Boost only if IMPLEMENTAČNÉ FÁZY is at START of chunk.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

content = FILE_PATH.read_text(encoding="utf-8")

old_boost = '''            # Extra boost for structural matches
            if "faz" in query_lower or "implementa" in query_lower:
                # Looking for phases - boost chunks with ACTUAL phase content
                raw_content = r.get("content", "")
                # Must contain section header or numbered phases
                if "IMPLEMENTAČNÉ FÁZY" in raw_content or "IMPLEMENTACNE FAZY" in raw_content.upper():
                    boost += 0.5  # Strong boost for exact section
                elif "Fáza 1:" in raw_content or "Faza 1:" in raw_content:
                    boost += 0.4  # Boost for phase details
                elif "Foundation" in raw_content and "Knowledge Base" in raw_content:
                    boost += 0.3  # Boost if multiple phases mentioned'''

new_boost = '''            # Extra boost for structural matches
            if "faz" in query_lower or "implementa" in query_lower:
                raw_content = r.get("content", "")
                # Check if section header is at START (first 200 chars) - this is the RIGHT chunk
                start_content = raw_content[:200]
                if "IMPLEMENTAČNÉ FÁZY" in start_content or "## 5." in start_content:
                    boost += 0.8  # Strong boost - this is THE chunk about phases
                elif "Fáza 1:" in start_content or "Foundation" in start_content[:300]:
                    boost += 0.6  # Also good - starts with phase details
                # No boost if IMPLEMENTAČNÉ is buried deep in chunk'''

if old_boost in content:
    content = content.replace(old_boost, new_boost)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: Boost only for chunks where IMPLEMENTAČNÉ FÁZY is at START")
else:
    print("⚠️ Pattern not found")
    # Find current boost section
    idx = content.find("# Extra boost for structural")
    if idx > 0:
        print("Current:", content[idx:idx+500])