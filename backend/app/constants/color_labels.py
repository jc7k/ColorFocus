"""
Color labels module for ColorFocus backend.

This module provides human-readable labels for color tokens in multiple languages,
loaded from the shared JSON source of truth.

Path Resolution:
    The shared/color_labels.json file is located at the project root level.
    This module resolves the path relative to this file's location:
    backend/app/constants/color_labels.py -> ../../../shared/color_labels.json

Usage:
    from backend.app.constants.color_labels import (
        Language,
        get_color_label,
        COLOR_LABELS,
    )

    # Get Chinese label (default)
    label = get_color_label(ColorToken.BLUE)  # "藍"

    # Get English label
    label = get_color_label(ColorToken.BLUE, Language.ENGLISH)  # "BLUE"

    # Get Vietnamese label
    label = get_color_label(ColorToken.BLUE, Language.VIETNAMESE)  # "Xanh"

    # Get Spanish label
    label = get_color_label(ColorToken.BLUE, Language.SPANISH)  # "AZUL"
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Dict

from backend.app.constants.colors import ColorToken


class Language(StrEnum):
    """
    Supported languages for color labels.

    CHINESE: Traditional Chinese single characters (default)
    ENGLISH: English color names in uppercase
    VIETNAMESE: Vietnamese color names with proper diacritical marks
    SPANISH: Spanish color names in uppercase
    """

    CHINESE = "chinese"
    ENGLISH = "english"
    VIETNAMESE = "vietnamese"
    SPANISH = "spanish"


def _load_labels_from_json() -> Dict[ColorToken, Dict[Language, str]]:
    """
    Load color label definitions from shared JSON at module import time.

    Returns:
        Dictionary mapping ColorToken to Language to label string.
    """
    # Resolve path: backend/app/constants/color_labels.py -> project_root/shared/color_labels.json
    labels_json_path = (
        Path(__file__).parent.parent.parent.parent / "shared" / "color_labels.json"
    )

    with open(labels_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    labels: Dict[ColorToken, Dict[Language, str]] = {}

    for token_name, label_data in raw_data.items():
        token = ColorToken(token_name)
        labels[token] = {}

        for lang_key, label_value in label_data.items():
            lang = Language(lang_key)
            labels[token][lang] = label_value

    return labels


# Load labels at module import time (not per-request)
COLOR_LABELS: Dict[ColorToken, Dict[Language, str]] = _load_labels_from_json()


def get_color_label(token: ColorToken, language: Language = Language.CHINESE) -> str:
    """
    Get the human-readable label for a color token in the specified language.

    Args:
        token: The ColorToken to get a label for.
        language: The language for the label (default: CHINESE).

    Returns:
        The label string for the color in the specified language.

    Raises:
        KeyError: If the token or language is not found in COLOR_LABELS.
    """
    return COLOR_LABELS[token][language]
