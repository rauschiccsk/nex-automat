"""MuFis status mapping — Hungarian statuses to internal order statuses.

MuFis sends order statuses in Hungarian. This module maps them to our
internal status keys used in eshop_orders.status column.
"""

import logging

logger = logging.getLogger(__name__)

# Internal order statuses (11 statuses)
ORDER_STATUSES: dict[str, str] = {
    "new": "Nová",
    "paid": "Zaplatená",
    "processing": "Spracováva sa",
    "label_printed": "Štítok vytlačený",
    "ready_for_pickup": "Pripravená na odovzdanie",
    "shipped": "Odoslaná",
    "ready_for_collection": "Na výdajnom mieste",
    "delivered": "Doručená",
    "returning": "Na ceste späť",
    "returned": "Vrátená",
    "cancelled": "Zrušená",
}

# MuFis Hungarian status → internal status mapping
# Keys are LOWERCASED for case-insensitive matching
MUFIS_STATUS_MAP: dict[str, str] = {
    "összeszedve": "processing",  # Picked/collected
    "csomagolás alatt": "processing",  # Packaging in progress
    "becsomagolva": "processing",  # Packaged
    "futárcímke nyomtatva": "label_printed",  # Courier label printed
    "átadásra kész": "ready_for_pickup",  # Ready for handover
    "futárnak átadva": "shipped",  # Handed to courier
    "futárcégnél": "shipped",  # At courier company
    "box - átvételre vár": "ready_for_collection",  # Box - waiting for pickup
    "kézbesítve": "delivered",  # Delivered
    "úton vissza": "returning",  # On the way back
    "visszaküldve": "returned",  # Returned
    # --- English aliases (for direct API calls / tests) ---
    "shipped": "shipped",
    "delivered": "delivered",
    "processing": "processing",
    "cancelled": "cancelled",
}


def map_mufis_status(mufis_status: str) -> str:
    """Map MuFis Hungarian status to internal order status.

    Matching is case-insensitive. Unknown statuses default to 'processing'
    with a WARNING log.

    Args:
        mufis_status: MuFis status string (Hungarian)

    Returns:
        Internal status key (e.g., 'delivered', 'shipped')
    """
    normalized = mufis_status.strip().lower()
    mapped = MUFIS_STATUS_MAP.get(normalized)
    if mapped is None:
        logger.warning(
            "Unknown MuFis status: '%s' — defaulting to 'processing'",
            mufis_status,
        )
        return "processing"
    return mapped


def is_valid_status(status_key: str) -> bool:
    """Check if status is a valid internal order status key."""
    return status_key in ORDER_STATUSES


def get_status_label(status_key: str, lang: str = "sk") -> str:
    """Get human-readable label for internal status.

    Args:
        status_key: Internal status key (e.g., 'delivered')
        lang: Language code (currently only 'sk' supported)

    Returns:
        Human-readable label or status_key if not found
    """
    return ORDER_STATUSES.get(status_key, status_key)
