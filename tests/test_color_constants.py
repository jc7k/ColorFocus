"""
Comprehensive tests for color constants in ColorFocus.

This module consolidates all color constant validation tests, including:
- JSON structure validation (colors.json)
- Python ColorToken enum validation
- COLORS dictionary validation
- Accessibility validation (luminance, contrast)

Uses shared fixtures from conftest.py to avoid duplication.
"""

import pytest

from conftest import (
    REQUIRED_COLOR_TOKENS,
    REMOVED_COLOR_TOKENS,
    EXPECTED_HEX_VALUES,
    HEX_PATTERN,
    hex_to_rgb,
    calculate_relative_luminance,
    calculate_contrast_ratio,
    load_colors,
)


class TestColorsJsonStructure:
    """Test that colors.json is valid JSON with correct structure."""

    def test_colors_json_is_valid_json(self, colors_data):
        """Test that colors.json exists and is valid JSON."""
        assert isinstance(colors_data, dict), "colors.json root should be an object"

    def test_all_required_tokens_present(self, colors_data):
        """Test that all 8 required color tokens are present."""
        for token in REQUIRED_COLOR_TOKENS:
            assert token in colors_data, f"Missing required color token: {token}"

    def test_old_tokens_not_present(self, colors_data):
        """Test that old tokens (CYAN, AMBER, MAGENTA) are removed."""
        for token in REMOVED_COLOR_TOKENS:
            assert token not in colors_data, f"Old token {token} should be removed"

    def test_exactly_8_tokens(self, colors_data):
        """Test that colors.json has exactly 8 color tokens."""
        assert len(colors_data) == 8, f"Expected 8 color tokens, got {len(colors_data)}"

    def test_flat_hex_structure(self, colors_data):
        """Test that colors.json uses flat hex values (no variant nesting)."""
        for token, value in colors_data.items():
            assert isinstance(value, str), (
                f"{token} should be a flat hex string, got {type(value).__name__}"
            )


class TestHexValueFormat:
    """Test that all color values are valid hex format (#RRGGBB)."""

    def test_all_hex_values_are_valid_format(self, colors_data):
        """Test that all 8 color values are valid hex format."""
        invalid_values = []
        for token, hex_value in colors_data.items():
            if not HEX_PATTERN.match(hex_value):
                invalid_values.append(f"{token}: {hex_value}")
        assert not invalid_values, f"Invalid hex values found: {invalid_values}"

    def test_hex_values_match_expected(self, colors_data):
        """Test that hex values match the expected accessible palette."""
        for token_name, expected_hex in EXPECTED_HEX_VALUES.items():
            actual_hex = colors_data.get(token_name)
            assert actual_hex is not None, f"Missing token: {token_name}"
            assert actual_hex.upper() == expected_hex.upper(), (
                f"{token_name}: Expected {expected_hex}, got {actual_hex}"
            )


class TestColorTokenEnum:
    """Test that ColorToken StrEnum contains all 8 token names."""

    def test_color_token_has_exactly_8_members(self):
        """Test that ColorToken enum has exactly 8 members."""
        from backend.app.constants.colors import ColorToken
        assert len(ColorToken) == 8, f"Expected 8 ColorToken values, got {len(ColorToken)}"

    def test_color_token_contains_all_required_tokens(self):
        """Test that ColorToken enum has all required accessible palette tokens."""
        from backend.app.constants.colors import ColorToken
        enum_values = [token.value for token in ColorToken]
        for token_name in REQUIRED_COLOR_TOKENS:
            assert token_name in enum_values, f"ColorToken missing: {token_name}"

    def test_old_tokens_removed_from_enum(self):
        """Test that old tokens (CYAN, AMBER, MAGENTA) are removed."""
        from backend.app.constants.colors import ColorToken
        enum_values = [token.value for token in ColorToken]
        for old_token in REMOVED_COLOR_TOKENS:
            assert old_token not in enum_values, f"Old token {old_token} should be removed"

    def test_color_variant_not_importable(self):
        """Test that ColorVariant is not available for import (removed)."""
        try:
            from backend.app.constants.colors import ColorVariant
            pytest.fail("ColorVariant should not exist in colors module")
        except ImportError:
            pass  # Expected - ColorVariant should not be importable


class TestColorsDict:
    """Test that Python COLORS dictionary matches source JSON."""

    def test_colors_dict_contains_all_8_colors(self):
        """Test that COLORS dict has all 8 new palette colors."""
        from backend.app.constants.colors import COLORS, ColorToken
        assert len(COLORS) == 8, f"Expected 8 colors, got {len(COLORS)}"
        for token_name in REQUIRED_COLOR_TOKENS:
            token = ColorToken(token_name)
            assert token in COLORS, f"COLORS missing token: {token_name}"

    def test_colors_dict_returns_flat_hex_strings(self):
        """Test that COLORS returns flat hex strings (not variant dicts)."""
        from backend.app.constants.colors import COLORS, ColorToken
        for token in ColorToken:
            hex_value = COLORS[token]
            assert isinstance(hex_value, str), (
                f"COLORS[{token}] should return str, got {type(hex_value).__name__}"
            )
            assert HEX_PATTERN.match(hex_value), (
                f"COLORS[{token}] should be #RRGGBB format, got {hex_value}"
            )

    def test_colors_dict_matches_source_json(self):
        """Test that COLORS dict hex values match source JSON exactly."""
        from backend.app.constants.colors import COLORS, ColorToken
        source_colors = load_colors()
        for token_name, expected_hex in source_colors.items():
            token_enum = ColorToken(token_name)
            actual_hex = COLORS[token_enum]
            assert actual_hex.upper() == expected_hex.upper(), (
                f"Hex mismatch for {token_name}: expected {expected_hex}, got {actual_hex}"
            )


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


class TestLuminanceSeparation:
    """Test that colors meet minimum luminance separation for accessibility."""

    def test_colors_have_luminance_separation(self, colors_data):
        """Test that colors have sufficient luminance spread across the spectrum."""
        luminance_values = {}
        for token in REQUIRED_COLOR_TOKENS:
            hex_value = colors_data[token]
            rgb = hex_to_rgb(hex_value)
            luminance = calculate_relative_luminance(rgb)
            luminance_values[token] = luminance

        min_lum = min(luminance_values.values())
        max_lum = max(luminance_values.values())
        spread = max_lum - min_lum

        # Expect at least 0.5 spread (50% of luminance range)
        assert spread >= 0.5, f"Insufficient luminance spread: {spread:.3f} (expected >= 0.5)"

    def test_no_identical_luminance_values(self, colors_data):
        """Test that no two colors have identical luminance values."""
        luminance_values = {}
        for token in REQUIRED_COLOR_TOKENS:
            hex_value = colors_data[token]
            rgb = hex_to_rgb(hex_value)
            luminance = round(calculate_relative_luminance(rgb), 4)

            if luminance in luminance_values:
                existing_token = luminance_values[luminance]
                pytest.fail(f"{token} and {existing_token} have identical luminance: {luminance}")

            luminance_values[luminance] = token

    def test_dark_colors_meet_contrast_threshold(self, colors_data):
        """Test that dark-oriented colors have sufficient contrast against white."""
        white_luminance = 1.0
        dark_colors = ["BLACK", "BROWN", "PURPLE", "BLUE"]
        min_contrast = 3.0

        low_contrast = []
        for token in dark_colors:
            hex_value = colors_data[token]
            rgb = hex_to_rgb(hex_value)
            luminance = calculate_relative_luminance(rgb)
            contrast = calculate_contrast_ratio(white_luminance, luminance)

            if contrast < min_contrast:
                low_contrast.append(f"{token}: {contrast:.2f}:1")

        assert not low_contrast, f"Dark colors with insufficient contrast: {low_contrast}"

    def test_maximum_luminance_contrast_pair(self, colors_data):
        """Test that BLACK and YELLOW have maximum luminance contrast (>10:1)."""
        black_rgb = hex_to_rgb(colors_data["BLACK"])
        yellow_rgb = hex_to_rgb(colors_data["YELLOW"])

        black_lum = calculate_relative_luminance(black_rgb)
        yellow_lum = calculate_relative_luminance(yellow_rgb)

        contrast = calculate_contrast_ratio(yellow_lum, black_lum)

        assert contrast >= 10.0, (
            f"BLACK and YELLOW contrast should be >= 10:1, got {contrast:.2f}:1"
        )
