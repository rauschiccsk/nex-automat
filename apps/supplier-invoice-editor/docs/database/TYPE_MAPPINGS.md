# Data Type Mappings - Btrieve ↔ PostgreSQL

## 📋 Quick Reference

This document defines type conversions between NEX Genesis (Btrieve/Delphi) and PostgreSQL.

### Core Mappings

| Btrieve (Delphi) | PostgreSQL | Python | Notes |
|------------------|------------|--------|-------|
| `longint` (4 bytes) | `INTEGER` | `int` | Standard integer |
| `double` (8 bytes) | `NUMERIC(12,2)` | `Decimal` | **Money - use NUMERIC!** |
| `string[n]` | `VARCHAR(n*2.5)` | `str` | UTF-8 overhead |
| `boolean` (1 byte) | `BOOLEAN` | `bool` | 0=false, 1=true |
| `TDateTime` (date) | `DATE` | `date` | Days since 1899-12-30 |
| `TDateTime` (time) | `TIME` | `time` | Milliseconds since midnight |

### Critical Rules

1. ✅ **Money:** Always use `NUMERIC(12,2)`, never `FLOAT` or `DOUBLE`
2. ✅ **Encoding:** CP852/Windows-1250 → UTF-8
3. ✅ **Dates:** Delphi base = 1899-12-30 (not UNIX 1970-01-01!)
4. ✅ **Strings:** PostgreSQL VARCHAR ≈ 2.5x Btrieve size
5. ✅ **NULL:** Btrieve uses sentinel values (0, empty string)

---

## 🔢 Numeric Types

### Integer Conversions

```python
# Btrieve → PostgreSQL
gs_code = struct.unpack('<i', data[0:4])[0]  # longint (4 bytes)
# PostgreSQL: INTEGER

# PostgreSQL → Btrieve  
gs_code = 12345
data = struct.pack('<i', gs_code)
```

### Money (CRITICAL!)

```python
from decimal import Decimal

# Btrieve → PostgreSQL
price = struct.unpack('<d', data[216:224])[0]  # double
price_decimal = Decimal(str(round(price, 2)))  # Exact!
# PostgreSQL: NUMERIC(12,2)

# ❌ NEVER DO THIS:
# price = float(price)  # Loses precision!
```

---

## 📝 String Conversions

### Encoding

```python
# Btrieve → PostgreSQL
name = data[4:84].decode('cp852', errors='ignore').rstrip('\x00 ')
# Result: "Čokoláda Milka" (UTF-8)

# PostgreSQL → Btrieve
name = "Čokoláda Milka"
name_bytes = name.encode('cp852')[:80].ljust(80, b'\x00')
```

### Common Slovak/Czech Characters

| Character | CP852 | UTF-8 |
|-----------|-------|-------|
| č | 0x8D | 0xC48D |
| ľ | 0x9C | 0xC4BE |
| ž | 0xAB | 0xC5BE |
| ô | 0x93 | 0xC3B4 |
| á | 0xA0 | 0xC3A1 |

---

## 📅 Date/Time Conversions

### Delphi TDateTime

Delphi uses `double`:
- **Integer part:** Days since 1899-12-30
- **Fractional part:** Time of day

```python
from datetime import datetime, timedelta

def decode_delphi_date(days: int) -> datetime:
    """Convert Delphi date to Python"""
    base_date = datetime(1899, 12, 30)  # ⚠️ NOT 1970-01-01!
    return base_date + timedelta(days=days)

def encode_delphi_date(dt: datetime) -> int:
    """Convert Python datetime to Delphi"""
    base_date = datetime(1899, 12, 30)
    return (dt - base_date).days

# Example
days = 45977
date = decode_delphi_date(days)
# Result: 2025-11-12

def decode_delphi_time(milliseconds: int) -> datetime:
    """Convert Delphi time to Python"""
    base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(milliseconds=milliseconds)

def encode_delphi_time(dt: datetime) -> int:
    """Convert Python time to Delphi"""
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return int((dt - midnight).total_seconds() * 1000)
```

---

## ✅ Complete Field Examples

### GSCAT (Product) Record

| Field | Btrieve | Size | PostgreSQL | Python |
|-------|---------|------|------------|--------|
| GsCode | longint | 4 | INTEGER | int |
| GsName | string[80] | 80 | VARCHAR(200) | str |
| PriceBuy | double | 8 | NUMERIC(12,2) | Decimal |
| PriceSell | double | 8 | NUMERIC(12,2) | Decimal |
| VatRate | double | 8 | NUMERIC(5,2) | Decimal |
| Active | boolean | 1 | BOOLEAN | bool |
| ModDate | longint | 4 | DATE | date |

### Invoice Record

| Field | Btrieve | Size | PostgreSQL | Python |
|-------|---------|------|------------|--------|
| SupplierICO | string[20] | 20 | VARCHAR(20) | str |
| InvoiceNumber | string[50] | 50 | VARCHAR(50) | str |
| InvoiceDate | longint | 4 | DATE | date |
| TotalAmount | double | 8 | NUMERIC(12,2) | Decimal |
| Currency | string[3] | 3 | VARCHAR(3) | str |
| Status | string[20] | 20 | VARCHAR(20) | str |

---

## ⚠️ Common Mistakes

### 1. Wrong Encoding
```python
# ❌ WRONG
name = data.decode('utf-8')  # Garbled: "�okol�da"

# ✅ CORRECT  
name = data.decode('cp852')  # Clean: "Čokoláda"
```

### 2. Float for Money
```python
# ❌ WRONG
price = 99.99
stored = float(price)  # → 99.98999999...

# ✅ CORRECT
from decimal import Decimal
price = Decimal('99.99')  # Exact
```

### 3. Wrong Date Base
```python
# ❌ WRONG
date = datetime(1970, 1, 1) + timedelta(days=45977)
# Result: 2095-11-24 (wrong!)

# ✅ CORRECT
date = datetime(1899, 12, 30) + timedelta(days=45977)  
# Result: 2025-11-12 (correct!)
```

---

## 📚 Reference Implementation

All conversions are implemented in:
- **`src/models/gscat.py`** - Complete example with all types
- **`src/models/barcode.py`** - Simple example
- **`src/models/pab.py`** - Complex strings
- **`src/models/mglst.py`** - Hierarchical data

---

## 🧪 Testing

```python
# tests/test_type_conversions.py
def test_round_trip_conversion():
    """Test that data survives Btrieve → PG → Btrieve"""
    from src.models import GSCATRecord
    from decimal import Decimal

    # Create original
    original = GSCATRecord(
        gs_code=123,
        gs_name="Čokoláda Milka",
        price_sell=Decimal('99.99'),
        active=True
    )

    # Convert to Btrieve bytes
    btrieve_bytes = original.to_bytes()

    # Convert back
    restored = GSCATRecord.from_bytes(btrieve_bytes)

    # Verify
    assert restored.gs_code == original.gs_code
    assert restored.gs_name == original.gs_name
    assert restored.price_sell == original.price_sell
    assert restored.active == original.active
```

---

## 📖 Summary

**Remember:**
1. Money → NUMERIC (not FLOAT!)
2. Strings → CP852 encoding
3. Dates → Base 1899-12-30
4. NULL → Sentinel values
5. Test both directions

**Full implementation available in `src/models/` package.**

---

*For detailed examples and complete conversion functions, see the models implementation.*
