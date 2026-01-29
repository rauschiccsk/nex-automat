"""
ProductMatcher - Match invoice items with NEX Genesis products

LIVE QUERIES - No caching, always fresh data from Btrieve
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.models.gscat import GSCATRecord
from nexdata.repositories.barcode_repository import BARCODERepository
from nexdata.repositories.gscat_repository import GSCATRepository
from rapidfuzz import fuzz
from unidecode import unidecode


@dataclass
class MatchResult:
    """Result of product matching attempt"""

    product: GSCATRecord | None
    confidence: float  # 0.0 - 1.0
    method: str  # 'ean', 'name', 'none'
    alternatives: list[tuple[GSCATRecord, float]] = field(default_factory=list)

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
    """
    Match invoice items with NEX Genesis products

    Uses LIVE queries to Btrieve - no caching for fresh data
    """

    def __init__(self, nex_data_path: str):
        """
        Initialize matcher with NEX Genesis data

        Args:
            nex_data_path: Path to NEX Genesis data directory
        """
        # Create BtrieveClient with config
        btrieve_config = {"database_path": nex_data_path}
        self.btrieve = BtrieveClient(config_or_path=btrieve_config)
        self.gscat_repo = GSCATRepository(self.btrieve)
        self.barcode_repo = BARCODERepository(self.btrieve)

    def match_item(
        self, item_data: dict, min_confidence: float = 0.6, max_name_results: int = 20
    ) -> MatchResult:
        """
        Main matching logic - tries EAN first, then name matching

        LIVE QUERIES - no cache, always fresh from Btrieve

        Args:
            item_data: Dictionary with item data (original_* and edited_* fields)
            min_confidence: Minimum confidence threshold for name matching
            max_name_results: Maximum results to consider for name matching

        Returns:
            MatchResult with matched product or None
        """
        # Get name and EAN (prefer edited over original)
        name = item_data.get("edited_name") or item_data.get("original_name", "")
        ean = item_data.get("edited_ean") or item_data.get("original_ean", "")

        # Try EAN matching first (highest confidence)
        if ean and ean.strip():
            result = self._match_by_ean(ean.strip())
            if result.product:
                return result

        # Try name matching (medium confidence)
        if name and name.strip():
            result = self._match_by_name(name.strip(), min_confidence, max_name_results)
            if result.product:
                return result

        # No match found
        return MatchResult(product=None, confidence=0.0, method="none")

    def _match_by_ean(self, ean: str) -> MatchResult:
        """
        Match by EAN code - LIVE query

        Optimized strategy:
        1. Search GSCAT.BTR first (95% of products have only 1 barcode)
        2. If not found, search BARCODE.BTR (additional barcodes)

        Args:
            ean: EAN/barcode string

        Returns:
            MatchResult with 0.95 confidence if found
        """
        # Normalize EAN (remove spaces, dashes)
        ean_normalized = ean.replace(" ", "").replace("-", "").strip()

        if not ean_normalized:
            return MatchResult(product=None, confidence=0.0, method="none")

        # STEP 1: Search in GSCAT (primary barcode) - 95% hit rate
        product = self.gscat_repo.find_by_barcode(ean_normalized)

        if product and not product.discontinued:
            return MatchResult(product=product, confidence=0.95, method="ean")

        # STEP 2: Search in BARCODE (additional barcodes) - 5% hit rate
        barcode_record = self.barcode_repo.find_by_barcode(ean_normalized)

        if barcode_record:
            # Get product from GSCAT
            product = self.gscat_repo.get_by_code(barcode_record.gs_code)

            if product and not product.discontinued:
                return MatchResult(product=product, confidence=0.95, method="ean")

        # No match
        return MatchResult(product=None, confidence=0.0, method="none")

    def _match_by_name(self, name: str, min_confidence: float, max_results: int) -> MatchResult:
        """
        Match by fuzzy name matching - LIVE query

        Args:
            name: Product name to match
            min_confidence: Minimum similarity threshold (0.0-1.0)
            max_results: Maximum results to fetch from database

        Returns:
            MatchResult with confidence based on similarity
        """
        # Normalize input name
        name_normalized = self._normalize_text(name)

        if not name_normalized:
            return MatchResult(product=None, confidence=0.0, method="none")

        # LIVE query - get potential matches from GSCAT
        # Repository will return active products only
        products = self.gscat_repo.search_by_name(name_normalized, limit=max_results)

        if not products:
            return MatchResult(product=None, confidence=0.0, method="none")

        # Calculate similarity for each product
        matches = []

        for product in products:
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
            return MatchResult(product=None, confidence=0.0, method="none")

        # Sort by score (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)

        # Get best match
        best_product, best_score = matches[0]

        # Get alternatives (top 5 excluding best)
        alternatives = matches[1:6]

        return MatchResult(
            product=best_product, confidence=best_score, method="name", alternatives=alternatives
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
        text = "".join(c if c.isalnum() or c.isspace() else " " for c in text)

        # Normalize whitespace
        text = " ".join(text.split())

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
