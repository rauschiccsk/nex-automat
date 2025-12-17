"""
Text utilities for normalization and comparison.
Used by QuickSearch for diacritic-insensitive search.
"""
import unicodedata


def remove_diacritics(text: str) -> str:
    """
    Remove diacritical marks from text.

    Converts: "Žeľazničný" -> "Zelaznicny"

    Args:
        text: Input text with diacritics

    Returns:
        Text without diacritical marks
    """
    if not text:
        return text

    # Normalize to NFD (decomposed form), remove combining marks
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(
        char for char in normalized 
        if unicodedata.category(char) != 'Mn'
    )


def normalize_for_search(text: str) -> str:
    """
    Normalize text for search comparison.
    - Remove diacritics
    - Convert to lowercase
    - Strip whitespace

    Args:
        text: Input text

    Returns:
        Normalized text suitable for comparison
    """
    if not text:
        return ""
    return remove_diacritics(str(text)).lower().strip()


def is_numeric(text: str) -> bool:
    """
    Check if text represents a number.

    Args:
        text: Input text

    Returns:
        True if text is numeric
    """
    if not text:
        return False
    try:
        float(str(text).replace(',', '.'))
        return True
    except ValueError:
        return False


def normalize_numeric(text: str) -> str:
    """
    Normalize numeric text for comparison.
    - Convert comma to dot
    - Strip whitespace

    Args:
        text: Numeric text

    Returns:
        Normalized numeric string
    """
    if not text:
        return ""
    return str(text).replace(',', '.').strip()
