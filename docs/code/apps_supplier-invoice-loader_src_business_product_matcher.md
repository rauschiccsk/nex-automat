# product_matcher.py

**Path:** `apps\supplier-invoice-loader\src\business\product_matcher.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

ProductMatcher - Match invoice items with NEX Genesis products

LIVE QUERIES - No caching, always fresh data from Btrieve

---

## Classes

### MatchResult

Result of product matching attempt

**Methods:**

#### `is_match(self)`

Check if match was found

#### `confidence_level(self)`

Get confidence level description

---

### ProductMatcher

Match invoice items with NEX Genesis products

Uses LIVE queries to Btrieve - no caching for fresh data

**Methods:**

#### `__init__(self, nex_data_path)`

Initialize matcher with NEX Genesis data

Args:
    nex_data_path: Path to NEX Genesis data directory

#### `match_item(self, item_data, min_confidence, max_name_results)`

Main matching logic - tries EAN first, then name matching

LIVE QUERIES - no cache, always fresh from Btrieve

Args:
    item_data: Dictionary with item data (original_* and edited_* fields)
    min_confidence: Minimum confidence threshold for name matching
    max_name_results: Maximum results to consider for name matching

Returns:
    MatchResult with matched product or None

#### `_match_by_ean(self, ean)`

Match by EAN code - LIVE query

Optimized strategy:
1. Search GSCAT.BTR first (95% of products have only 1 barcode)
2. If not found, search BARCODE.BTR (additional barcodes)

Args:
    ean: EAN/barcode string

Returns:
    MatchResult with 0.95 confidence if found

#### `_match_by_name(self, name, min_confidence, max_results)`

Match by fuzzy name matching - LIVE query

Args:
    name: Product name to match
    min_confidence: Minimum similarity threshold (0.0-1.0)
    max_results: Maximum results to fetch from database

Returns:
    MatchResult with confidence based on similarity

#### `_normalize_text(self, text)`

Normalize text for matching

- Remove diacritics (unidecode)
- Convert to lowercase
- Remove special characters
- Normalize whitespace

Args:
    text: Text to normalize

Returns:
    Normalized text

#### `_calculate_similarity(self, text1, text2)`

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

---
