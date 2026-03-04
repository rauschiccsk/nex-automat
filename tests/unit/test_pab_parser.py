"""
Unit tests for PAB binary parser — Pascal ShortString handling.

Tests parse_pab_record(), _parse_pascal_string(), _parse_pascal_date(),
_parse_pascal_time() and PAB_FIELDS integrity.
"""

import struct
import sys
from datetime import date, time
from pathlib import Path

import pytest

# Ensure nexdata package is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "nexdata"))


def test_parse_pab_record_basic():
    """Verify basic PAB record parsing: PaCode + PaName."""
    from nexdata.models.pab import PAB_FIELDS, parse_pab_record

    total_size = sum(f[2] for f in PAB_FIELDS)

    # Create test buffer filled with zeros
    buf = bytearray(total_size)
    offset = 0

    # PaCode = 42 (longint, 4 bytes)
    struct.pack_into("<i", buf, offset, 42)
    offset += 4

    # PaName = "Test Partner" (Str30 = 31 bytes: 1 length + 30 chars)
    name = "Test Partner"
    buf[offset] = len(name)
    buf[offset + 1 : offset + 1 + len(name)] = name.encode("cp1250")

    result = parse_pab_record(bytes(buf))
    assert result["PaCode"] == 42
    assert result["PaName"] == "Test Partner"
    # Underscore-prefixed fields must be skipped
    assert "_PaName" not in result


def test_parse_pascal_string_truncation():
    """Length byte > max_len should be clamped to max_len."""
    from nexdata.models.pab import _parse_pascal_string

    buf = bytearray(31)
    buf[0] = 255  # corrupted length > max (30)
    buf[1:6] = b"Hello"
    result = _parse_pascal_string(buf, 0, 30)
    assert len(result) <= 30


def test_parse_pascal_date():
    """Delphi date (days since 1899-12-30) should parse correctly."""
    from nexdata.models.pab import _parse_pascal_date

    buf = bytearray(4)
    # 2024-01-15 = days since 1899-12-30
    days = (date(2024, 1, 15) - date(1899, 12, 30)).days
    struct.pack_into("<i", buf, 0, days)
    result = _parse_pascal_date(buf, 0)
    assert result == date(2024, 1, 15)


def test_parse_pascal_date_zero():
    """Zero date value should return None."""
    from nexdata.models.pab import _parse_pascal_date

    buf = bytearray(4)
    result = _parse_pascal_date(buf, 0)
    assert result is None


def test_parse_pascal_time():
    """Delphi time (ms since midnight) should parse correctly."""
    from nexdata.models.pab import _parse_pascal_time

    buf = bytearray(4)
    # 10:30:45 = (10*3600 + 30*60 + 45) * 1000 ms
    ms = (10 * 3600 + 30 * 60 + 45) * 1000
    struct.pack_into("<i", buf, 0, ms)
    result = _parse_pascal_time(buf, 0)
    assert result == time(10, 30, 45)


def test_record_size():
    """PAB_FIELDS must have exactly 95 fields with total > 1269 bytes."""
    from nexdata.models.pab import PAB_FIELDS

    total = sum(f[2] for f in PAB_FIELDS)
    assert total > 0
    assert len(PAB_FIELDS) == 95
    # BDF record size is 1269, but fields total 1277 (AdvPay added later)
    assert total >= 1269


def test_from_bytes_integration():
    """PABRecord.from_bytes() should produce correct dataclass fields."""
    from nexdata.models.pab import PAB_FIELDS, PABRecord

    total_size = sum(f[2] for f in PAB_FIELDS)
    buf = bytearray(total_size)

    # PaCode = 100
    struct.pack_into("<i", buf, 0, 100)

    # PaName at offset 4, Str30 (31 bytes)
    name = "ACME Corp"
    buf[4] = len(name)
    buf[5 : 5 + len(name)] = name.encode("cp1250")

    record = PABRecord.from_bytes(bytes(buf))
    assert record.pab_code == 100
    assert record.name1 == "ACME Corp"
    assert record.raw_fields is not None
    assert record.raw_fields["PaCode"] == 100


def test_underscore_fields_skipped():
    """Fields starting with _ should not appear in parsed result."""
    from nexdata.models.pab import PAB_FIELDS, parse_pab_record

    total_size = sum(f[2] for f in PAB_FIELDS)
    buf = bytearray(total_size)
    struct.pack_into("<i", buf, 0, 1)

    result = parse_pab_record(bytes(buf))
    for key in result:
        assert not key.startswith("_"), f"Underscore field leaked: {key}"


def test_parse_pascal_string_empty():
    """Zero-length Pascal string should return empty string."""
    from nexdata.models.pab import _parse_pascal_string

    buf = bytearray(31)
    buf[0] = 0  # length = 0
    result = _parse_pascal_string(buf, 0, 30)
    assert result == ""
