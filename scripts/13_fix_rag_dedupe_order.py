#!/usr/bin/env python
"""
Fix rag_service.py - Fix dedupe to use adjusted_score properly.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/rag_service.py")

content = FILE_PATH.read_text(encoding="utf-8")

# Fix _deduplicate_best to properly compare adjusted scores
old_dedupe = '''    def _deduplicate_best(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only BEST chunk per unique filename."""
        best = {}
        for r in results:
            filename = r.get("filename", "")
            score = r.get("adjusted_score", r.get("score", 0))
            if filename not in best or score > best[filename].get("adjusted_score", 0):
                best[filename] = r
        return list(best.values())'''

new_dedupe = '''    def _deduplicate_best(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only BEST chunk per unique filename (by adjusted_score)."""
        best = {}
        for r in results:
            filename = r.get("filename", "")
            current_score = r.get("adjusted_score", r.get("score", 0))
            existing = best.get(filename)
            if existing is None:
                best[filename] = r
            else:
                existing_score = existing.get("adjusted_score", existing.get("score", 0))
                if current_score > existing_score:
                    best[filename] = r
        # Sort by adjusted_score descending
        sorted_results = sorted(best.values(), key=lambda x: x.get("adjusted_score", 0), reverse=True)
        return sorted_results'''

if old_dedupe in content:
    content = content.replace(old_dedupe, new_dedupe)
    FILE_PATH.write_text(content, encoding="utf-8")
    print("✅ Fixed: dedupe now properly compares adjusted_score")
else:
    print("⚠️ Pattern not found, checking current dedupe...")
    if "_deduplicate_best" in content:
        start = content.find("def _deduplicate_best")
        end = content.find("\n    def ", start + 1)
        print(content[start:end][:500])