"""
Session Script 06: Create ProductMatcher Implementation
Creates product_matcher.py with EAN and name matching logic
"""
from pathlib import Path


def main():
    business_dir = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\business")
    target_file = business_dir / "product_matcher.py"

    print("=" * 60)
    print("Phase 2: Creating ProductMatcher")
    print("=" * 60)

    # Ensure directory exists
    business_dir.mkdir(parents=True, exist_ok=True)

    matcher_content = '''"""
ProductMatcher - Match invoice items with NEX Genesis products

Implements two-stage matching:
1. EAN matching (BARCODE -> GSCAT) - 95% confidence
2. Name fuzzy matching - 60-90% confidence based on similarity
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict
from decimal import Decimal

from rapidfuzz import fuzz
from unidecode import unidecode

from nexdata.repositories.gscat_repository import GSCATRepository
from nexdata.repositories.barcode_repository import BARCODERepository
from nexdata.models.gscat import GSCATRecord


@dataclass
class MatchResult:
    """Result of product matching attempt"""
    product: Optional[GSCATRecord]
    confidence: float  # 0.0 - 1.0
    method: str  # 'ean', 'name', 'none'
    alternatives: List[Tuple[GSCATRecord, float]] = field(default_factory=list)

    @property
    def is_match(self) -> bool:
        """Check if match was found"""
        return self.product is not None

    @property
    def confidence_level(self) -> str:
        """Get confidence level description"""
        if self.confidence >= 0.9:
            return "high"
        elif self.confidence >= 0.7:
            return "medium"
        elif self.confidence >= 0.6:
            return "low"
        else:
            return "none"


class ProductMatcher:
    """Match invoice items with NEX Genesis products"""

    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        self.gscat_repo = GSCATRepository(nex_data_path)
        self.barcode_repo = BARCODERepository(nex_data_path)

        # Load data into memory for fast access
        self._products_cache: Dict[int, GSCATRecord] = {}
        self._barcode_cache: Dict[str, int] = {}
        self._load_caches()

    def _load_caches(self):
        """Load products and barcodes into memory"""
        # Load all products
        for product in self.gscat_repo.get_all():
            self._products_cache[product.gs_code] = product

        # Load all barcodes
        for barcode in self.barcode_repo.get_all():
            # Normalize and cache
            normalized = barcode.bar_code.strip()
            if normalized:
                self._barcode_cache[normalized] = barcode.gs_code

        print(f"[ProductMatcher] Loaded {len(self._products_cache)} products, {len(self._barcode_cache)} barcodes")

    def match_item(
        self, 
        item_data: Dict,
        min_confidence: float = 0.6
    ) -> MatchResult:
        """
        Main matching logic - tries EAN first, then name matching

        Args:
            item_data: Dictionary with item data (original_* and edited_* fields)
            min_confidence: Minimum confidence threshold for name matching

        Returns:
            MatchResult with matched product or None
        """
        # Get name and EAN (prefer edited over original)
        name = item_data.get('edited_name') or item_data.get('original_name', '')
        ean = item_data.get('edited_ean') or item_data.get('original_ean', '')

        # Try EAN matching first (highest confidence)
        if ean and ean.strip():
            result = self._match_by_ean(ean.strip())
            if result.product:
                return result

        # Try name matching (medium confidence)
        if name and name.strip():
            result = self._match_by_name(name.strip(), min_confidence)
            if result.product:
                return result

        # No match found
        return MatchResult(
            product=None,
            confidence=0.0,
            method='none'
        )

    def _match_by_ean(self, ean: str) -> MatchResult:
        """
        Match by EAN code via BARCODE table

        Args:
            ean: EAN/barcode string

        Returns:
            MatchResult with 0.95 confidence if found
        """
        # Normalize EAN (remove spaces, dashes)
        ean_normalized = ean.replace(' ', '').replace('-', '').strip()

        # Lookup in barcode cache
        gs_code = self._barcode_cache.get(ean_normalized)

        if gs_code:
            product = self._products_cache.get(gs_code)
            if product:
                return MatchResult(
                    product=product,
                    confidence=0.95,
                    method='ean'
                )

        # No match
        return MatchResult(
            product=None,
            confidence=0.0,
            method='none'
        )

    def _match_by_name(
        self, 
        name: str, 
        min_confidence: float
    ) -> MatchResult:
        """
        Match by fuzzy name matching

        Args:
            name: Product name to match
            min_confidence: Minimum similarity threshold (0.0-1.0)

        Returns:
            MatchResult with confidence based on similarity
        """
        # Normalize input name
        name_normalized = self._normalize_text(name)

        if not name_normalized:
            return MatchResult(
                product=None,
                confidence=0.0,
                method='none'
            )

        # Find matches across all products
        matches = []

        for gs_code, product in self._products_cache.items():
            # Skip discontinued products
            if product.discontinued:
                continue

            # Normalize product name
            product_name = self._normalize_text(product.gs_name)

            if not product_name:
                continue

            # Calculate similarity
            score = self._calculate_similarity(name_normalized, product_name)

            # Add to matches if above threshold
            if score >= min_confidence:
                matches.append((product, score))

        # No matches found
        if not matches:
            return MatchResult(
                product=None,
                confidence=0.0,
                method='none'
            )

        # Sort by score (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)

        # Get best match
        best_product, best_score = matches[0]

        # Get alternatives (top 5 excluding best)
        alternatives = matches[1:6]

        return MatchResult(
            product=best_product,
            confidence=best_score,
            method='name',
            alternatives=alternatives
        )

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for matching

        - Remove diacritics (unidecode)
        - Convert to lowercase
        - Remove special characters
        - Normalize whitespace

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        if not text:
            return ""

        # Remove diacritics
        text = unidecode(text)

        # Lowercase
        text = text.lower()

        # Keep only alphanumeric and spaces
        text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts

        Uses rapidfuzz token_set_ratio which:
        - Ignores word order
        - Handles partial matches
        - Returns 0-100 score

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0.0 - 1.0)
        """
        # Use token_set_ratio for flexible matching
        score = fuzz.token_set_ratio(text1, text2)

        # Convert to 0.0-1.0 range
        return score / 100.0

    def get_stats(self) -> Dict:
        """Get matcher statistics"""
        active_products = sum(
            1 for p in self._products_cache.values() 
            if not p.discontinued
        )

        return {
            'total_products': len(self._products_cache),
            'active_products': active_products,
            'discontinued_products': len(self._products_cache) - active_products,
            'total_barcodes': len(self._barcode_cache)
        }
'''

    # Write file
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(matcher_content)

    print(f"✅ Created {target_file.name}")
    print(f"   Location: {target_file}")

    print("\nImplemented:")
    print("  - MatchResult dataclass")
    print("  - ProductMatcher class")
    print("  - EAN matching (via BARCODE cache)")
    print("  - Name fuzzy matching (via rapidfuzz)")
    print("  - Text normalization (unidecode)")
    print("  - In-memory caching")

    print("\n" + "=" * 60)
    print("✅ Phase 2 Step 1 complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())