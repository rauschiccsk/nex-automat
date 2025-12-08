"""
NEX Shared - Text Utilities
Utility functions for text processing and cleaning.
"""


def clean_string(value):
    """
    Odstráni null bytes a control characters z reťazcov.
    NEX Genesis Btrieve polia obsahujú \\x00 padding.

    Args:
        value: String alebo iná hodnota na vyčistenie

    Returns:
        Vyčistený string alebo None/original value
    """
    if value is None:
        return None
    if not isinstance(value, str):
        return value

    # Remove null bytes
    cleaned = value.replace('\x00', '')

    # Remove other control characters (except newline, tab)
    cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\t')

    # Strip excess whitespace
    cleaned = cleaned.strip()

    return cleaned if cleaned else None
