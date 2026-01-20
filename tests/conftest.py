"""
Shared test fixtures and utilities for ColorFocus test suite.

This module centralizes common constants, paths, and helper functions
used across multiple test files to reduce duplication and improve
maintainability.
"""

import json
import re
from pathlib import Path

import pytest


# =============================================================================
# Path Constants
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
SHARED_DIR = PROJECT_ROOT / "shared"

COLORS_JSON_PATH = SHARED_DIR / "colors.json"
COLOR_LABELS_JSON_PATH = SHARED_DIR / "color_labels.json"
UI_TEXT_JSON_PATH = SHARED_DIR / "ui_text.json"
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


# =============================================================================
# Color Palette Constants
# =============================================================================

# Required color tokens for the accessible palette (ordered by luminance)
REQUIRED_COLOR_TOKENS = [
    "BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"
]

# Old tokens that should NOT exist (removed for accessibility)
REMOVED_COLOR_TOKENS = ["CYAN", "AMBER", "MAGENTA"]

# Expected hex values for the accessible palette
EXPECTED_HEX_VALUES = {
    "BLACK": "#1A1A1A",
    "BROWN": "#8B4513",
    "PURPLE": "#7B4BAF",
    "BLUE": "#0066CC",
    "GRAY": "#808080",
    "PINK": "#E75480",
    "ORANGE": "#FF8C00",
    "YELLOW": "#FFD700",
}


# =============================================================================
# Validation Patterns
# =============================================================================

# Hex color pattern (#RRGGBB)
HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


# =============================================================================
# Supported Languages
# =============================================================================

SUPPORTED_LANGUAGES = ["zh-TW", "english", "vietnamese", "spanish"]


# =============================================================================
# Helper Functions
# =============================================================================

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def calculate_relative_luminance(rgb: tuple[int, int, int]) -> float:
    """
    Calculate relative luminance per WCAG 2.1 specification.

    Formula: L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    where R, G, B are linearized sRGB values.
    """
    def linearize(c: int) -> float:
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def calculate_contrast_ratio(l1: float, l2: float) -> float:
    """Calculate contrast ratio between two luminance values."""
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# =============================================================================
# Fixtures - JSON Data Loaders
# =============================================================================

@pytest.fixture
def colors_data() -> dict:
    """Load and return the colors.json data."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def color_labels_data() -> dict:
    """Load and return the color_labels.json data."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def ui_text_data() -> dict:
    """Load and return the ui_text.json data."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def puzzle_html_content() -> str:
    """Load and return the puzzle.html content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


# =============================================================================
# Standalone Loader Functions (for use outside fixtures)
# =============================================================================

def load_colors() -> dict:
    """Load and parse the colors.json file."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_color_labels() -> dict:
    """Load and parse the color_labels.json file."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ui_text() -> dict:
    """Load and parse the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()
