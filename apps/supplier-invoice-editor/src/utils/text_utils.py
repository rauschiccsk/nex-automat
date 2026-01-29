"""
Text utilities for normalization and comparison
Nástroje pre normalizáciu a porovnávanie textu
"""

import unicodedata


def remove_diacritics(text: str) -> str:
    """
    Remove diacritical marks from text

    Converts: "Žeľazničný" -> "Zelaznicny"

    Args:
        text: Input text with diacritics

    Returns:
        Text without diacritical marks
    """
    if not text:
        return ""

    # Normalize to NFD (decomposed form)
    normalized = unicodedata.normalize("NFD", text)

    # Remove combining characters (diacritics)
    without_diacritics = "".join(char for char in normalized if unicodedata.category(char) != "Mn")

    return without_diacritics


def normalize_for_search(text: str) -> str:
    """
    Normalize text for search comparison
    - Remove diacritics
    - Convert to lowercase
    - Strip whitespace

    Args:
        text: Input text

    Returns:
        Normalized text suitable for comparison

    Examples:
        >>> normalize_for_search("  ŽLTÝ Čaj  ")
        'zlty caj'
        >>> normalize_for_search("Košice")
        'kosice'
    """
    if not text:
        return ""

    # Remove diacritics
    text = remove_diacritics(text)

    # Lowercase
    text = text.lower()

    # Strip and normalize whitespace
    text = " ".join(text.split())

    return text


def is_numeric(text: str) -> bool:
    """
    Check if text represents a number

    Args:
        text: Input text

    Returns:
        True if text is numeric

    Examples:
        >>> is_numeric("123")
        True
        >>> is_numeric("12.5")
        True
        >>> is_numeric("abc")
        False
    """
    if not text:
        return False

    try:
        float(text.replace(",", "."))
        return True
    except ValueError:
        return False


def normalize_numeric(text: str) -> str:
    """
    Normalize numeric text for comparison
    - Convert comma to dot
    - Remove leading zeros
    - Strip whitespace

    Args:
        text: Numeric text

    Returns:
        Normalized numeric string

    Examples:
        >>> normalize_numeric("0123")
        '123'
        >>> normalize_numeric("12,5")
        '12.5'
    """
    if not text:
        return ""

    text = text.strip()

    # Replace comma with dot
    text = text.replace(",", ".")

    try:
        # Convert to float and back to remove leading zeros
        num = float(text)
        # Keep original precision
        if "." in text:
            decimals = len(text.split(".")[-1])
            return f"{num:.{decimals}f}"
        else:
            return str(int(num))
    except ValueError:
        return text
