"""
Color constants module for ColorFocus backend.

This module provides type-safe access to the 8 canonical color tokens
and their brightness variants, loaded from the shared JSON source of truth.

Path Resolution:
    The shared/colors.json file is located at the project root level.
    This module resolves the path relative to this file's location:
    backend/app/constants/colors.py -> ../../../shared/colors.json

Usage:
    from backend.app.constants.colors import ColorToken, ColorVariant, COLORS

    # Access a specific color
    blue_base = COLORS[ColorToken.BLUE][ColorVariant.BASE]  # "#2E86DE"

    # Iterate over all tokens
    for token in ColorToken:
        print(token.value, COLORS[token][ColorVariant.BASE])
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Dict


class ColorToken(StrEnum):
    """
    Canonical color tokens for ColorFocus.

    These 8 colors are selected for color-blind accessibility,
    distinguishable across deuteranopia, protanopia, and tritanopia.
    """

    BLUE = "BLUE"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"
    BLACK = "BLACK"
    CYAN = "CYAN"
    AMBER = "AMBER"
    MAGENTA = "MAGENTA"
    GRAY = "GRAY"


class ColorVariant(StrEnum):
    """
    Brightness variants for each color token.

    DARK: Lower lightness (15-20% darker than BASE)
    BASE: Reference color value
    BRIGHT: Higher lightness (15-20% brighter than BASE)

    Note: BLACK token may omit DARK variant per PRD precedent.
    """

    DARK = "DARK"
    BASE = "BASE"
    BRIGHT = "BRIGHT"


def _load_colors_from_json() -> Dict[ColorToken, Dict[ColorVariant, str]]:
    """
    Load color definitions from shared JSON at module import time.

    Returns:
        Dictionary mapping ColorToken to ColorVariant to hex string.
    """
    # Resolve path: backend/app/constants/colors.py -> project_root/shared/colors.json
    colors_json_path = Path(__file__).parent.parent.parent.parent / "shared" / "colors.json"

    with open(colors_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    colors: Dict[ColorToken, Dict[ColorVariant, str]] = {}

    for token_name, token_data in raw_data.items():
        token = ColorToken(token_name)
        colors[token] = {}

        for variant_name, hex_value in token_data["variants"].items():
            variant = ColorVariant(variant_name.upper())
            colors[token][variant] = hex_value

    return colors


# Load colors at module import time (not per-request)
COLORS: Dict[ColorToken, Dict[ColorVariant, str]] = _load_colors_from_json()
