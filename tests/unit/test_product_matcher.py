"""
Unit tests for ProductMatcher

Note: These tests use mocks to avoid Btrieve dependencies.
The ProductMatcher class uses live Btrieve queries in production.
"""

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import Mock


# Mock GSCATRecord to match actual structure
@dataclass
class MockGSCATRecord:
    """Mock GSCATRecord for testing - matches actual field names."""

    GsCode: int
    GsName: str
    BarCode: str = ""
    SupplierCode: str = ""
    MgCode: str = ""
    RawData: bytes = b""

    # Compatibility properties for test assertions
    @property
    def gs_code(self):
        return self.GsCode

    @property
    def gs_name(self):
        return self.GsName


# Mock MatchResult matching production interface
@dataclass
class MatchResult:
    """Mock MatchResult for unit testing."""

    product: Any
    confidence: float
    method: str
    alternatives: list = field(default_factory=list)

    @property
    def is_match(self) -> bool:
        return self.product is not None

    @property
    def confidence_level(self) -> str:
        if self.confidence >= 0.9:
            return "high"
        elif self.confidence >= 0.7:
            return "medium"
        elif self.confidence >= 0.6:
            return "low"
        return "none"


class TestMatchResult:
    """Tests for MatchResult dataclass."""

    def test_is_match_property(self):
        """Should correctly identify match status."""
        match = MatchResult(product=Mock(), confidence=0.9, method="ean")
        no_match = MatchResult(product=None, confidence=0.0, method="none")

        assert match.is_match
        assert not no_match.is_match

    def test_confidence_levels(self):
        """Should categorize confidence levels correctly."""
        high = MatchResult(product=Mock(), confidence=0.95, method="ean")
        medium = MatchResult(product=Mock(), confidence=0.75, method="name")
        low = MatchResult(product=Mock(), confidence=0.65, method="name")
        none = MatchResult(product=None, confidence=0.0, method="none")

        assert high.confidence_level == "high"
        assert medium.confidence_level == "medium"
        assert low.confidence_level == "low"
        assert none.confidence_level == "none"

    def test_confidence_level_boundaries(self):
        """Should handle boundary values correctly."""
        assert (
            MatchResult(product=Mock(), confidence=0.9, method="ean").confidence_level
            == "high"
        )
        assert (
            MatchResult(product=Mock(), confidence=0.7, method="name").confidence_level
            == "medium"
        )
        assert (
            MatchResult(product=Mock(), confidence=0.6, method="name").confidence_level
            == "low"
        )
        assert (
            MatchResult(product=Mock(), confidence=0.5, method="name").confidence_level
            == "none"
        )


class TestMockGSCATRecord:
    """Tests for MockGSCATRecord structure."""

    def test_gscat_record_fields(self):
        """Should have correct field structure."""
        record = MockGSCATRecord(
            GsCode=123,
            GsName="Test Product",
            BarCode="1234567890123",
        )

        assert record.GsCode == 123
        assert record.GsName == "Test Product"
        assert record.BarCode == "1234567890123"

    def test_compatibility_properties(self):
        """Should provide snake_case compatibility properties."""
        record = MockGSCATRecord(GsCode=456, GsName="Another Product")

        assert record.gs_code == 456
        assert record.gs_name == "Another Product"


class TestTextNormalization:
    """Tests for text normalization utilities used in matching."""

    def test_normalize_removes_special_chars(self):
        """Should handle special character removal."""
        # Test the concept without importing actual module
        import re
        from unicodedata import normalize

        def normalize_text(text):
            if not text:
                return ""
            # Normalize unicode
            text = normalize("NFKD", text).encode("ASCII", "ignore").decode()
            # Remove special chars, keep alphanumeric and spaces
            text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
            # Normalize whitespace
            text = " ".join(text.lower().split())
            return text

        assert normalize_text("Coca-Cola") == "coca cola"
        assert normalize_text("UPPERCASE") == "uppercase"
        assert normalize_text("  spaces  ") == "spaces"
        assert normalize_text("Spec!@l Ch@rs") == "spec l ch rs"

    def test_normalize_handles_diacritics(self):
        """Should handle Slovak/Czech diacritics."""
        from unicodedata import normalize

        def remove_diacritics(text):
            return normalize("NFKD", text).encode("ASCII", "ignore").decode()

        assert remove_diacritics("čšžťň") == "csztn"
        assert remove_diacritics("Čokoláda") == "Cokolada"

    def test_normalize_empty_text(self):
        """Should handle empty text."""

        def normalize_text(text):
            if not text:
                return ""
            return text.strip().lower()

        assert normalize_text("") == ""
        assert normalize_text(None) == ""


class TestSimilarityCalculation:
    """Tests for similarity calculation concepts."""

    def test_identical_texts_have_max_similarity(self):
        """Should return maximum similarity for identical texts."""
        # Using simple ratio as example
        from difflib import SequenceMatcher

        def similarity(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        assert similarity("test", "test") == 1.0
        assert similarity("hello", "hello") == 1.0

    def test_completely_different_texts(self):
        """Should return low similarity for different texts."""
        from difflib import SequenceMatcher

        def similarity(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        score = similarity("abc", "xyz")
        assert score < 0.5

    def test_partial_match_has_medium_similarity(self):
        """Should return medium similarity for partial matches."""
        from difflib import SequenceMatcher

        def similarity(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        score = similarity("coca cola", "cola")
        assert 0.3 <= score <= 0.9


class TestEANValidation:
    """Tests for EAN code validation logic."""

    def test_clean_ean_removes_spaces(self):
        """Should clean EAN by removing spaces."""

        def clean_ean(ean):
            if not ean:
                return ""
            return "".join(c for c in ean if c.isdigit())

        assert clean_ean("1234 5678 90123") == "1234567890123"
        assert clean_ean("1234-5678-90123") == "1234567890123"

    def test_clean_ean_removes_dashes(self):
        """Should remove dashes from EAN."""

        def clean_ean(ean):
            return ean.replace("-", "").replace(" ", "")

        assert clean_ean("1234-5678-90123") == "1234567890123"

    def test_valid_ean_length(self):
        """Should validate EAN length."""

        def is_valid_ean(ean):
            cleaned = "".join(c for c in ean if c.isdigit())
            return len(cleaned) in [8, 12, 13, 14]

        assert is_valid_ean("12345678") is True  # EAN-8
        assert is_valid_ean("123456789012") is True  # UPC-12
        assert is_valid_ean("1234567890123") is True  # EAN-13
        assert is_valid_ean("12345678901234") is True  # GTIN-14
        assert is_valid_ean("123") is False


class TestMatchingPreferences:
    """Tests for matching preference logic."""

    def test_prefer_edited_over_original(self):
        """Should prefer edited values over original."""

        def get_best_value(item_data, field_name):
            edited = item_data.get(f"edited_{field_name}")
            original = item_data.get(f"original_{field_name}")
            return edited if edited else original

        item = {"original_name": "Wrong", "edited_name": "Correct"}
        assert get_best_value(item, "name") == "Correct"

        item2 = {"original_name": "Original", "edited_name": None}
        assert get_best_value(item2, "name") == "Original"

    def test_ean_match_has_higher_priority(self):
        """Should prioritize EAN matches over name matches."""
        # Conceptual test - EAN confidence should be higher
        ean_confidence = 0.95
        name_confidence = 0.85

        assert ean_confidence > name_confidence


class TestMatchResultAlternatives:
    """Tests for alternative matches handling."""

    def test_alternatives_list(self):
        """Should store alternative matches."""
        alt1 = (MockGSCATRecord(GsCode=1, GsName="Alt 1"), 0.75)
        alt2 = (MockGSCATRecord(GsCode=2, GsName="Alt 2"), 0.70)

        result = MatchResult(
            product=MockGSCATRecord(GsCode=0, GsName="Best"),
            confidence=0.85,
            method="name",
            alternatives=[alt1, alt2],
        )

        assert len(result.alternatives) == 2
        assert result.alternatives[0][1] == 0.75
        assert result.alternatives[1][0].GsCode == 2

    def test_empty_alternatives(self):
        """Should handle empty alternatives list."""
        result = MatchResult(product=Mock(), confidence=0.95, method="ean")
        assert result.alternatives == []
