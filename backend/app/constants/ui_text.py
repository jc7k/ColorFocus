"""
UI text module for ColorFocus backend.

This module provides localized UI text strings in multiple languages,
loaded from the shared JSON source of truth.

Path Resolution:
    The shared/ui_text.json file is located at the project root level.
    This module resolves the path relative to this file's location:
    backend/app/constants/ui_text.py -> ../../../shared/ui_text.json

Usage:
    from backend.app.constants.ui_text import (
        get_ui_text,
        UI_TEXT,
    )
    from backend.app.constants.color_labels import Language

    # Get English text (default)
    text = get_ui_text("page_title", Language.ENGLISH)  # "ColorFocus Stroop Puzzle"

    # Get Chinese text
    text = get_ui_text("page_title", Language.CHINESE)  # "ColorFocus Stroop 拼图"

    # Get Vietnamese text
    text = get_ui_text("page_title", Language.VIETNAMESE)  # "ColorFocus - Tro choi Stroop"
"""

import json
from pathlib import Path
from typing import Dict

from backend.app.constants.color_labels import Language


def _load_ui_text_from_json() -> Dict[str, Dict[Language, str]]:
    """
    Load UI text definitions from shared JSON at module import time.

    Returns:
        Dictionary mapping text key to Language to text string.
    """
    # Resolve path: backend/app/constants/ui_text.py -> project_root/shared/ui_text.json
    ui_text_json_path = (
        Path(__file__).parent.parent.parent.parent / "shared" / "ui_text.json"
    )

    with open(ui_text_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    ui_text: Dict[str, Dict[Language, str]] = {}

    for text_key, translations in raw_data.items():
        ui_text[text_key] = {}

        for lang_key, text_value in translations.items():
            lang = Language(lang_key)
            ui_text[text_key][lang] = text_value

    return ui_text


# Load UI text at module import time (not per-request)
UI_TEXT: Dict[str, Dict[Language, str]] = _load_ui_text_from_json()


def get_ui_text(key: str, language: Language = Language.ENGLISH) -> str:
    """
    Get the localized UI text for a key in the specified language.

    Args:
        key: The text key to look up (e.g., "page_title", "generate_btn").
        language: The language for the text (default: ENGLISH).

    Returns:
        The text string for the key in the specified language.

    Raises:
        KeyError: If the key or language is not found in UI_TEXT.
    """
    return UI_TEXT[key][language]
