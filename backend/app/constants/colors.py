"""
Color constants module for ColorFocus backend.

This module provides type-safe access to the 8 canonical color tokens,
loaded from the shared JSON source of truth. The color palette is
optimized for accessibility, using luminance-ordered colors that remain
distinguishable for users with color vision deficiencies, elderly users,
and stroke recovery patients.

Path Resolution:
    The shared/colors.json file is located at the project root level.
    This module resolves the path relative to this file's location:
    backend/app/constants/colors.py -> ../../../shared/colors.json

Usage:
    from backend.app.constants.colors import ColorToken, COLORS

    # Access a specific color hex value
    blue_hex = COLORS[ColorToken.BLUE]  # "#0066CC"

    # Iterate over all tokens
    for token in ColorToken:
        print(token.value, COLORS[token])
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Dict


class ColorToken(StrEnum):
    """
    Canonical color tokens for ColorFocus.

    These 8 colors are selected for accessibility, ordered by luminance
    from darkest to lightest. The palette is designed to be distinguishable
    across deuteranopia, protanopia, and tritanopia color vision deficiencies.

    Luminance order (10% to 84%):
        BLACK (10%) -> BROWN (28%) -> PURPLE (35%) -> BLUE (38%) ->
        GRAY (50%) -> PINK (52%) -> ORANGE (62%) -> YELLOW (84%)

    Excluded colors (by design):
        - Red: Confuses with brown/orange for color-blind users
        - Green: Vietnamese "xanh" ambiguity + color blindness issues
        - Cyan/Teal: Too similar to blue for elderly users
        - White: Reserved for background
    """

    BLACK = "BLACK"
    BROWN = "BROWN"
    PURPLE = "PURPLE"
    BLUE = "BLUE"
    GRAY = "GRAY"
    PINK = "PINK"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"


def _load_colors_from_json() -> Dict[ColorToken, str]:
    """
    Load color definitions from shared JSON at module import time.

    The colors.json file uses a flat structure mapping token names
    directly to hex values (e.g., {"BLACK": "#1A1A1A", ...}).

    Returns:
        Dictionary mapping ColorToken to hex string.
    """
    # Resolve path: backend/app/constants/colors.py -> project_root/shared/colors.json
    colors_json_path = Path(__file__).parent.parent.parent.parent / "shared" / "colors.json"

    with open(colors_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    colors: Dict[ColorToken, str] = {}

    for token_name, hex_value in raw_data.items():
        token = ColorToken(token_name)
        colors[token] = hex_value

    return colors


# Load colors at module import time (not per-request)
COLORS: Dict[ColorToken, str] = _load_colors_from_json()
