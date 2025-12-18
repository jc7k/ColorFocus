"""
Tests for Python color constants module.

These tests verify that:
1. Python COLORS dictionary matches source JSON structure
2. ColorToken StrEnum contains all 8 token names
3. ColorVariant StrEnum contains all 3 variant names
"""

import json
from pathlib import Path


# Path to the shared colors.json file
COLORS_JSON_PATH = Path(__file__).parent.parent / "shared" / "colors.json"

# Required color tokens
REQUIRED_TOKENS = ["BLUE", "ORANGE", "PURPLE", "BLACK", "CYAN", "AMBER", "MAGENTA", "GRAY"]

# Required variants
REQUIRED_VARIANTS = ["DARK", "BASE", "BRIGHT"]


def load_source_colors():
    """Load and parse the source colors.json file."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestColorTokenStrEnum:
    """Test that ColorToken StrEnum contains all 8 token names."""

    def test_color_token_contains_all_tokens(self):
        """Test that ColorToken enum has all 8 required token names."""
        from backend.app.constants.colors import ColorToken

        enum_values = [token.value for token in ColorToken]

        for token_name in REQUIRED_TOKENS:
            assert token_name in enum_values, f"ColorToken missing required token: {token_name}"

    def test_color_token_count(self):
        """Test that ColorToken has exactly 8 tokens."""
        from backend.app.constants.colors import ColorToken

        assert len(ColorToken) == 8, f"Expected 8 ColorToken values, got {len(ColorToken)}"


class TestColorVariantStrEnum:
    """Test that ColorVariant StrEnum contains all 3 variant names."""

    def test_color_variant_contains_all_variants(self):
        """Test that ColorVariant enum has all 3 required variant names."""
        from backend.app.constants.colors import ColorVariant

        enum_values = [variant.value for variant in ColorVariant]

        for variant_name in REQUIRED_VARIANTS:
            assert variant_name in enum_values, f"ColorVariant missing required variant: {variant_name}"

    def test_color_variant_count(self):
        """Test that ColorVariant has exactly 3 variants."""
        from backend.app.constants.colors import ColorVariant

        assert len(ColorVariant) == 3, f"Expected 3 ColorVariant values, got {len(ColorVariant)}"


class TestColorsDict:
    """Test that Python COLORS dictionary matches source JSON structure."""

    def test_colors_dict_matches_source_json_tokens(self):
        """Test that COLORS dictionary has all tokens from source JSON."""
        from backend.app.constants.colors import COLORS, ColorToken

        source_colors = load_source_colors()

        for token_name in source_colors.keys():
            token_enum = ColorToken(token_name)
            assert token_enum in COLORS, f"COLORS missing token: {token_name}"

    def test_colors_dict_hex_values_match_source(self):
        """Test that COLORS hex values match source JSON exactly."""
        from backend.app.constants.colors import COLORS, ColorToken, ColorVariant

        source_colors = load_source_colors()

        for token_name, token_data in source_colors.items():
            token_enum = ColorToken(token_name)

            for variant_name, hex_value in token_data["variants"].items():
                variant_enum = ColorVariant(variant_name.upper())

                if variant_enum in COLORS[token_enum]:
                    assert COLORS[token_enum][variant_enum] == hex_value, (
                        f"Hex mismatch for {token_name}.{variant_name}: "
                        f"expected {hex_value}, got {COLORS[token_enum][variant_enum]}"
                    )
