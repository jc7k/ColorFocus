"""
Tests for Python color constants module.

These tests verify that:
1. Python COLORS dictionary matches source JSON structure (flat hex values)
2. ColorToken StrEnum contains all 8 token names for the accessible palette
3. ColorVariant is removed (no longer needed with flat structure)

Updated for the accessible color palette replacement:
- New tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
- Old tokens removed: CYAN, AMBER, MAGENTA
- Flat hex structure (no variant objects)
"""

import json
import re
from pathlib import Path


# Path to the shared colors.json file
COLORS_JSON_PATH = Path(__file__).parent.parent / "shared" / "colors.json"

# Required color tokens (new accessible palette)
REQUIRED_TOKENS = ["BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"]

# Old tokens that should NOT exist
REMOVED_TOKENS = ["CYAN", "AMBER", "MAGENTA"]

# Hex color pattern (#RRGGBB)
HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_source_colors():
    """Load and parse the source colors.json file."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestColorTokenStrEnum:
    """Test that ColorToken StrEnum contains all 8 token names for the accessible palette."""

    def test_color_token_contains_all_new_tokens(self):
        """Test that ColorToken enum has all 8 new accessible palette tokens."""
        from backend.app.constants.colors import ColorToken

        enum_values = [token.value for token in ColorToken]

        for token_name in REQUIRED_TOKENS:
            assert token_name in enum_values, f"ColorToken missing required token: {token_name}"

    def test_color_token_count(self):
        """Test that ColorToken has exactly 8 tokens."""
        from backend.app.constants.colors import ColorToken

        assert len(ColorToken) == 8, f"Expected 8 ColorToken values, got {len(ColorToken)}"

    def test_old_tokens_removed(self):
        """Test that old tokens (CYAN, AMBER, MAGENTA) are removed from ColorToken."""
        from backend.app.constants.colors import ColorToken

        enum_values = [token.value for token in ColorToken]

        for old_token in REMOVED_TOKENS:
            assert old_token not in enum_values, f"Old token {old_token} should be removed from ColorToken"


class TestColorVariantRemoved:
    """Test that ColorVariant enum is removed (no longer needed with flat structure)."""

    def test_color_variant_not_importable(self):
        """Test that ColorVariant is not available for import."""
        try:
            from backend.app.constants.colors import ColorVariant
            assert False, "ColorVariant should not exist in colors module"
        except ImportError:
            pass  # Expected - ColorVariant should not be importable


class TestColorsDict:
    """Test that Python COLORS dictionary matches source JSON structure (flat hex values)."""

    def test_colors_dict_matches_source_json_tokens(self):
        """Test that COLORS dictionary has all tokens from source JSON."""
        from backend.app.constants.colors import COLORS, ColorToken

        source_colors = load_source_colors()

        for token_name in source_colors.keys():
            token_enum = ColorToken(token_name)
            assert token_enum in COLORS, f"COLORS missing token: {token_name}"

    def test_colors_dict_returns_flat_hex_strings(self):
        """Test that COLORS returns flat hex strings (not variant dicts)."""
        from backend.app.constants.colors import COLORS, ColorToken

        for token in ColorToken:
            hex_value = COLORS[token]
            # Should be a string, not a dict
            assert isinstance(hex_value, str), (
                f"COLORS[{token}] should return str, got {type(hex_value).__name__}"
            )
            # Should be valid hex format
            assert HEX_PATTERN.match(hex_value), (
                f"COLORS[{token}] should be #RRGGBB format, got {hex_value}"
            )

    def test_colors_dict_hex_values_match_source(self):
        """Test that COLORS hex values match source JSON exactly."""
        from backend.app.constants.colors import COLORS, ColorToken

        source_colors = load_source_colors()

        for token_name, expected_hex in source_colors.items():
            token_enum = ColorToken(token_name)
            actual_hex = COLORS[token_enum]

            assert actual_hex.upper() == expected_hex.upper(), (
                f"Hex mismatch for {token_name}: expected {expected_hex}, got {actual_hex}"
            )

    def test_colors_dict_count(self):
        """Test that COLORS dict contains exactly 8 colors."""
        from backend.app.constants.colors import COLORS

        assert len(COLORS) == 8, f"Expected 8 colors in COLORS dict, got {len(COLORS)}"


class TestLoadColorsFromJson:
    """Test that _load_colors_from_json correctly parses flat hex structure."""

    def test_load_colors_returns_flat_dict(self):
        """Test that _load_colors_from_json returns Dict[ColorToken, str]."""
        from backend.app.constants.colors import _load_colors_from_json, ColorToken

        colors = _load_colors_from_json()

        for token, value in colors.items():
            assert isinstance(token, ColorToken), f"Key should be ColorToken, got {type(token)}"
            assert isinstance(value, str), f"Value should be str (hex), got {type(value)}"
            assert HEX_PATTERN.match(value), f"Value should be hex format, got {value}"

    def test_load_colors_returns_correct_count(self):
        """Test that _load_colors_from_json returns exactly 8 colors."""
        from backend.app.constants.colors import _load_colors_from_json

        colors = _load_colors_from_json()
        assert len(colors) == 8, f"Expected 8 colors, got {len(colors)}"
