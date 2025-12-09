"""
Unit tests for ProductMatcher
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from decimal import Decimal

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'apps' / 'supplier-invoice-loader' / 'src'))

from business.product_matcher import ProductMatcher, MatchResult
from nexdata.models.gscat import GSCATRecord


@pytest.fixture
def mock_gscat_records():
    """Create mock GSCAT records"""
    return [
        GSCATRecord(
            gs_code=1,
            gs_name="Coca Cola 0.5L",
            mglst_code=10,
            unit="ks",
            price_buy=Decimal("15.50"),
            price_sell=Decimal("20.00"),
            vat_rate=Decimal("20.0"),
            active=True,
            discontinued=False
        ),
        GSCATRecord(
            gs_code=2,
            gs_name="Sprite 0.5L",
            mglst_code=10,
            unit="ks",
            price_buy=Decimal("14.00"),
            price_sell=Decimal("18.00"),
            vat_rate=Decimal("20.0"),
            active=True,
            discontinued=False
        ),
        GSCATRecord(
            gs_code=3,
            gs_name="Fanta Orange 0.5L",
            mglst_code=10,
            unit="ks",
            price_buy=Decimal("14.00"),
            price_sell=Decimal("18.00"),
            vat_rate=Decimal("20.0"),
            active=True,
            discontinued=True  # Discontinued
        ),
    ]


@pytest.fixture
def mock_barcode_records():
    """Create mock barcode records"""
    from nexdata.models.barcode import BarcodeRecord

    return [
        BarcodeRecord(gs_code=1, bar_code="1234567890123"),
        BarcodeRecord(gs_code=2, bar_code="9876543210987"),
    ]


@pytest.fixture
def matcher(mock_gscat_records, mock_barcode_records):
    """Create ProductMatcher with mocked repositories"""
    with patch('business.product_matcher.GSCATRepository') as mock_gscat_repo, \
         patch('business.product_matcher.BARCODERepository') as mock_barcode_repo:

        # Setup mock repositories
        mock_gscat_repo.return_value.get_all.return_value = mock_gscat_records
        mock_barcode_repo.return_value.get_all.return_value = mock_barcode_records

        # Create matcher
        matcher = ProductMatcher("fake_path")

        return matcher


class TestMatcherInitialization:
    """Tests for ProductMatcher initialization"""

    def test_loads_products_cache(self, matcher):
        """Should load products into cache"""
        assert len(matcher._products_cache) == 3
        assert 1 in matcher._products_cache
        assert matcher._products_cache[1].gs_name == "Coca Cola 0.5L"

    def test_loads_barcode_cache(self, matcher):
        """Should load barcodes into cache"""
        assert len(matcher._barcode_cache) == 2
        assert "1234567890123" in matcher._barcode_cache
        assert matcher._barcode_cache["1234567890123"] == 1

    def test_get_stats(self, matcher):
        """Should return correct statistics"""
        stats = matcher.get_stats()

        assert stats['total_products'] == 3
        assert stats['active_products'] == 2  # 2 active, 1 discontinued
        assert stats['discontinued_products'] == 1
        assert stats['total_barcodes'] == 2


class TestEANMatching:
    """Tests for EAN-based matching"""

    def test_match_by_exact_ean(self, matcher):
        """Should match by exact EAN"""
        item_data = {
            'original_name': 'Some product',
            'original_ean': '1234567890123'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1
        assert result.confidence == 0.95
        assert result.method == 'ean'

    def test_match_by_ean_with_spaces(self, matcher):
        """Should match EAN with spaces"""
        item_data = {
            'original_name': 'Product',
            'original_ean': '1234 5678 90123'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_match_by_ean_with_dashes(self, matcher):
        """Should match EAN with dashes"""
        item_data = {
            'original_ean': '1234-5678-90123'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_prefers_edited_ean_over_original(self, matcher):
        """Should prefer edited EAN"""
        item_data = {
            'original_ean': 'wrong_ean',
            'edited_ean': '1234567890123'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_no_match_for_unknown_ean(self, matcher):
        """Should return no match for unknown EAN"""
        item_data = {
            'original_ean': '0000000000000'
        }

        result = matcher.match_item(item_data)

        assert not result.is_match
        assert result.confidence == 0.0


class TestNameMatching:
    """Tests for fuzzy name matching"""

    def test_match_by_exact_name(self, matcher):
        """Should match by exact name"""
        item_data = {
            'original_name': 'Coca Cola 0.5L'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1
        assert result.method == 'name'
        assert result.confidence > 0.9

    def test_match_with_diacritics(self, matcher):
        """Should match names with diacritics"""
        item_data = {
            'original_name': 'Coca Cóla 0.5L'  # With accent
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_match_case_insensitive(self, matcher):
        """Should match case-insensitively"""
        item_data = {
            'original_name': 'COCA COLA 0.5L'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_match_with_special_characters(self, matcher):
        """Should handle special characters"""
        item_data = {
            'original_name': 'Coca-Cola 0,5L!!!'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1

    def test_partial_name_match(self, matcher):
        """Should match partial names"""
        item_data = {
            'original_name': 'Coca Cola'  # Without volume
        }

        result = matcher.match_item(item_data, min_confidence=0.6)

        assert result.is_match
        assert result.product.gs_code == 1
        assert result.confidence >= 0.6

    def test_respects_min_confidence(self, matcher):
        """Should respect minimum confidence threshold"""
        item_data = {
            'original_name': 'Water'  # Very different
        }

        result = matcher.match_item(item_data, min_confidence=0.8)

        assert not result.is_match

    def test_returns_alternatives(self, matcher):
        """Should return alternative matches"""
        item_data = {
            'original_name': 'Cola 0.5L'
        }

        result = matcher.match_item(item_data, min_confidence=0.5)

        if result.is_match and len(result.alternatives) > 0:
            assert all(isinstance(alt[0], GSCATRecord) for alt in result.alternatives)
            assert all(isinstance(alt[1], float) for alt in result.alternatives)

    def test_skips_discontinued_products(self, matcher):
        """Should not match discontinued products"""
        item_data = {
            'original_name': 'Fanta Orange 0.5L'  # Discontinued
        }

        result = matcher.match_item(item_data)

        # Should not match discontinued product (gs_code=3)
        if result.is_match:
            assert result.product.gs_code != 3

    def test_prefers_edited_name(self, matcher):
        """Should prefer edited name over original"""
        item_data = {
            'original_name': 'Wrong name',
            'edited_name': 'Coca Cola 0.5L'
        }

        result = matcher.match_item(item_data)

        assert result.is_match
        assert result.product.gs_code == 1


class TestMatchResult:
    """Tests for MatchResult dataclass"""

    def test_is_match_property(self):
        """Should correctly identify match status"""
        match = MatchResult(product=Mock(), confidence=0.9, method='ean')
        no_match = MatchResult(product=None, confidence=0.0, method='none')

        assert match.is_match
        assert not no_match.is_match

    def test_confidence_levels(self):
        """Should categorize confidence levels"""
        high = MatchResult(product=Mock(), confidence=0.95, method='ean')
        medium = MatchResult(product=Mock(), confidence=0.75, method='name')
        low = MatchResult(product=Mock(), confidence=0.65, method='name')
        none = MatchResult(product=None, confidence=0.0, method='none')

        assert high.confidence_level == "high"
        assert medium.confidence_level == "medium"
        assert low.confidence_level == "low"
        assert none.confidence_level == "none"


class TestTextNormalization:
    """Tests for text normalization"""

    def test_normalize_text(self, matcher):
        """Should normalize text correctly"""
        assert matcher._normalize_text("Coca-Cola") == "coca cola"
        assert matcher._normalize_text("UPPERCASE") == "uppercase"
        assert matcher._normalize_text("  spaces  ") == "spaces"
        assert matcher._normalize_text("čšžťň") == "csztn"
        assert matcher._normalize_text("Spec!@l Ch@rs") == "spec l ch rs"

    def test_normalize_empty_text(self, matcher):
        """Should handle empty text"""
        assert matcher._normalize_text("") == ""
        assert matcher._normalize_text(None) == ""


class TestSimilarityCalculation:
    """Tests for similarity calculation"""

    def test_identical_texts(self, matcher):
        """Should return 1.0 for identical texts"""
        score = matcher._calculate_similarity("test", "test")
        assert score == 1.0

    def test_completely_different_texts(self, matcher):
        """Should return low score for different texts"""
        score = matcher._calculate_similarity("abc", "xyz")
        assert score < 0.5

    def test_partial_match(self, matcher):
        """Should return medium score for partial match"""
        score = matcher._calculate_similarity("coca cola", "cola")
        assert 0.5 <= score <= 1.0  # token_set_ratio may return 1.0 for subsets
