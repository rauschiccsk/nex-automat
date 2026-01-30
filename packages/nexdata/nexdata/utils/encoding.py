"""
Kamenický (KEYBCS2) encoding utilities for NEX Genesis Btrieve data.

NEX Genesis uses Kamenický encoding (also known as KEYBCS2 or CP895)
for Czech/Slovak text. This was the standard encoding used in
Czech/Slovak DOS systems from 1985-1995.

Reference: https://en.wikipedia.org/wiki/Kamenický_encoding
"""

# Kamenický (KEYBCS2/CP895) encoding table for bytes 128-255
# Bytes 0-127 are standard ASCII
# Bytes 128-171 are Czech/Slovak letters (replacing CP437 graphics)
# Bytes 172-255 are box drawing characters (same as CP437)
_KEYBCS2_TABLE: dict[int, str] = {
    # 0x80-0x8F: Czech/Slovak letters
    0x80: "Č",
    0x81: "ü",
    0x82: "é",
    0x83: "ď",
    0x84: "ä",
    0x85: "Ď",
    0x86: "Ť",
    0x87: "č",
    0x88: "ě",
    0x89: "Ě",
    0x8A: "Ĺ",
    0x8B: "Í",
    0x8C: "ľ",
    0x8D: "ĺ",
    0x8E: "Ä",
    0x8F: "Á",
    # 0x90-0x9F: More Czech/Slovak letters
    0x90: "É",
    0x91: "ž",
    0x92: "Ž",
    0x93: "ô",
    0x94: "ö",
    0x95: "Ó",
    0x96: "ů",
    0x97: "Ú",
    0x98: "ý",
    0x99: "Ö",
    0x9A: "Ü",
    0x9B: "Š",
    0x9C: "Ľ",
    0x9D: "Ý",
    0x9E: "Ř",
    0x9F: "ť",
    # 0xA0-0xAB: More accented letters
    0xA0: "á",
    0xA1: "í",
    0xA2: "ó",
    0xA3: "ú",
    0xA4: "ň",
    0xA5: "Ň",
    0xA6: "Ů",
    0xA7: "Ô",
    0xA8: "š",
    0xA9: "ř",
    0xAA: "ŕ",
    0xAB: "Ŕ",
    # 0xAC-0xFF: Box drawing and other chars use CP437 fallback
}


def decode_keybcs2(data: bytes) -> str:
    """
    Decode Kamenický (KEYBCS2/CP895) encoded bytes to UTF-8 string.

    NEX Genesis uses Kamenický encoding for Czech/Slovak text.
    - Bytes 0-127: ASCII (direct mapping)
    - Bytes 128-171: Czech/Slovak letters
    - Bytes 172-255: Box drawing characters (CP437 fallback)

    Args:
        data: Raw bytes in Kamenický encoding

    Returns:
        UTF-8 decoded string
    """
    result = []
    for byte in data:
        if byte < 128:
            # ASCII range - direct mapping
            result.append(chr(byte))
        elif byte in _KEYBCS2_TABLE:
            # Czech/Slovak characters
            result.append(_KEYBCS2_TABLE[byte])
        else:
            # Box drawing and other chars - try CP437 fallback
            try:
                result.append(bytes([byte]).decode("cp437"))
            except (UnicodeDecodeError, ValueError):
                result.append("?")
    return "".join(result)
