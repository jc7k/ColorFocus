"""
Tests for backend color constants after accessible color palette update.

These tests verify that:
1. ColorToken enum has exactly 8 members matching new palette
2. COLORS dict loads all 8 colors with valid hex values
3. Old tokens (CYAN, AMBER, MAGENTA) are not present in ColorToken
4. _load_colors_from_json correctly parses flat hex structure

Part of Task Group 2: Python Constants Update
"""

import re
from pathlib import Path


# Expected new color tokens for accessible palette
NEW_PALETTE_TOKENS = ["BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"]

# Old tokens that should be removed
OLD_TOKENS_REMOVED = ["CYAN", "AMBER", "MAGENTA"]

# Expected hex values for new palette
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

# Hex color pattern (#RRGGBB)
HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


class TestColorTokenEnumNewPalette:
    """Test that ColorToken enum has exactly 8 members matching new accessible palette."""

    def test_color_token_has_exactly_8_members(self):
        """Test that ColorToken enum has exactly 8 members."""
        from backend.app.constants.colors import ColorToken

        assert len(ColorToken) == 8, f"Expected 8 ColorToken values, got {len(ColorToken)}"

    def test_color_token_contains_all_new_palette_tokens(self):
        """Test that ColorToken enum has all new accessible palette tokens."""
        from backend.app.constants.colors import ColorToken

        enum_values = [token.value for token in ColorToken]

        for token_name in NEW_PALETTE_TOKENS:
            assert token_name in enum_values, f"ColorToken missing new palette token: {token_name}"


class TestOldTokensRemoved:
    """Test that old tokens (CYAN, AMBER, MAGENTA) are not present in ColorToken."""

    def test_old_tokens_not_in_color_token_enum(self):
        """Test that CYAN, AMBER, MAGENTA are removed from ColorToken enum."""
        from backend.app.constants.colors import ColorToken

        enum_values = [token.value for token in ColorToken]

        for old_token in OLD_TOKENS_REMOVED:
            assert old_token not in enum_values, f"Old token {old_token} should be removed from ColorToken"


class TestColorsDict:
    """Test that COLORS dict loads all 8 colors with valid hex values."""

    def test_colors_dict_contains_all_8_colors(self):
        """Test that COLORS dict has all 8 new palette colors."""
        from backend.app.constants.colors import COLORS, ColorToken

        assert len(COLORS) == 8, f"Expected 8 colors in COLORS dict, got {len(COLORS)}"

        for token_name in NEW_PALETTE_TOKENS:
            token = ColorToken(token_name)
            assert token in COLORS, f"COLORS missing token: {token_name}"

    def test_colors_dict_values_are_valid_hex(self):
        """Test that all color values are valid hex format (#RRGGBB)."""
        from backend.app.constants.colors import COLORS

        for token, hex_value in COLORS.items():
            assert isinstance(hex_value, str), f"{token}: Expected string value, got {type(hex_value)}"
            assert HEX_PATTERN.match(hex_value), f"{token}: Invalid hex format: {hex_value}"

    def test_colors_dict_values_match_expected(self):
        """Test that COLORS dict hex values match expected palette."""
        from backend.app.constants.colors import COLORS, ColorToken

        for token_name, expected_hex in EXPECTED_HEX_VALUES.items():
            token = ColorToken(token_name)
            actual_hex = COLORS[token]
            assert actual_hex.upper() == expected_hex.upper(), (
                f"{token_name}: Expected {expected_hex}, got {actual_hex}"
            )


class TestLoadColorsFromJson:
    """Test that _load_colors_from_json correctly parses flat hex structure."""

    def test_load_colors_returns_flat_dict(self):
        """Test that _load_colors_from_json returns Dict[ColorToken, str] (flat structure)."""
        from backend.app.constants.colors import _load_colors_from_json, ColorToken

        colors = _load_colors_from_json()

        # Should return flat dict, not nested with ColorVariant
        for token, value in colors.items():
            assert isinstance(token, ColorToken), f"Key should be ColorToken, got {type(token)}"
            assert isinstance(value, str), f"Value should be str (hex), got {type(value)}"
            assert HEX_PATTERN.match(value), f"Value should be hex format, got {value}"
