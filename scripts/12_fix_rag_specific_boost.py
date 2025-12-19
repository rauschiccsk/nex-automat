#!/usr/bin/env python
"""
Fix rag_service.py - More specific boost for implementation phases.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

content = FILE_PATH.read_text(encoding="utf-8")

# Replace the boost logic with more specific check
old_code = '''            # Extra boost for structural matches
            if "faz" in query_lower or "implementa" in query_lower:
                # Looking for phases - boost chunks with numbered phases
                if re.search(r"faz[ae]\\s*[123456]", content) or "IMPLEMENT" in r.get("content", "").upper():
                    boost += 0.3'''

new_code = '''            # Extra boost for structural matches
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

if old_code in content:
    content = content.replace(old_code, new_code)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: More specific boost for IMPLEMENTAČNÉ FÁZY")
else:
    print("⚠️ Old code not found exactly. Current boost section:")
    import re
    match = re.search(r"# Extra boost for structural.*?boost \+= 0\.\d", content, re.DOTALL)
    if match:
        print(match.group()[:300])