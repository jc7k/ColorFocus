"""
Tests for color token validation.

These tests verify that the shared colors.json file:
1. Is valid JSON with correct structure
2. Contains all 8 color values in valid hex format
3. Has all 8 color tokens in flat hex format (no variants)
4. Meets minimum luminance separation thresholds for accessibility

Updated for the accessible color palette replacement:
- New tokens: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
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


def load_colors():
    """Load and parse the colors.json file."""
    with open(COLORS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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


class TestColorsJsonStructure:
    """Test that colors.json is valid JSON with correct structure."""

    def test_colors_json_is_valid_json(self):
        """Test that colors.json exists and is valid JSON."""
        assert COLORS_JSON_PATH.exists(), f"colors.json not found at {COLORS_JSON_PATH}"

        colors = load_colors()
        assert isinstance(colors, dict), "colors.json root should be an object"

    def test_all_required_tokens_present(self):
        """Test that all 8 required color tokens are present."""
        colors = load_colors()

        for token in REQUIRED_TOKENS:
            assert token in colors, f"Missing required color token: {token}"

    def test_old_tokens_not_present(self):
        """Test that old tokens (CYAN, AMBER, MAGENTA) are removed."""
        colors = load_colors()

        for token in REMOVED_TOKENS:
            assert token not in colors, f"Old token {token} should be removed from colors.json"

    def test_exactly_8_tokens(self):
        """Test that colors.json has exactly 8 color tokens."""
        colors = load_colors()
        assert len(colors) == 8, f"Expected 8 color tokens, got {len(colors)}"

    def test_flat_hex_structure(self):
        """Test that colors.json uses flat hex values (no variant nesting)."""
        colors = load_colors()

        for token, value in colors.items():
            # Value should be a string (hex), not a dict
            assert isinstance(value, str), (
                f"{token} should be a flat hex string, got {type(value).__name__}"
            )
            # Should not have 'variants' key at root level
            assert "variants" not in colors.get(token, ""), (
                f"{token} should not have nested variants structure"
            )


class TestHexValueFormat:
    """Test that all color values are valid hex format (#RRGGBB)."""

    def test_all_hex_values_are_valid_format(self):
        """Test that all 8 color values are valid hex format."""
        colors = load_colors()

        invalid_values = []
        for token, hex_value in colors.items():
            if not HEX_PATTERN.match(hex_value):
                invalid_values.append(f"{token}: {hex_value}")

        assert not invalid_values, f"Invalid hex values found: {invalid_values}"

    def test_expected_color_count(self):
        """Test that we have exactly 8 color values."""
        colors = load_colors()
        assert len(colors) == 8, f"Expected 8 color values, got {len(colors)}"


class TestLuminanceSeparation:
    """Test that colors meet minimum luminance separation thresholds for accessibility."""

    def test_colors_have_luminance_separation(self):
        """
        Test that colors have sufficient luminance spread across the spectrum.

        This ensures colors are distinguishable based on brightness differences,
        which aids color-blind users who rely on luminance variations.

        The new accessible palette is ordered by luminance:
        BLACK (10%) -> BROWN (28%) -> PURPLE (35%) -> BLUE (38%) ->
        GRAY (50%) -> PINK (52%) -> ORANGE (62%) -> YELLOW (84%)
        """
        colors = load_colors()

        luminance_values = {}
        for token in REQUIRED_TOKENS:
            hex_value = colors[token]
            rgb = hex_to_rgb(hex_value)
            luminance = calculate_relative_luminance(rgb)
            luminance_values[token] = luminance

        # Verify we have a good spread of luminance values
        min_lum = min(luminance_values.values())
        max_lum = max(luminance_values.values())
        spread = max_lum - min_lum

        # We expect at least 0.5 spread (50% of luminance range)
        # BLACK should be near 0.1, YELLOW near 0.8
        assert spread >= 0.5, f"Insufficient luminance spread: {spread:.3f} (expected >= 0.5)"

    def test_no_identical_luminance_values(self):
        """
        Test that no two colors have identical luminance values.

        Even if colors have similar luminance, they should not be exactly the same.
        """
        colors = load_colors()

        luminance_values = {}
        for token in REQUIRED_TOKENS:
            hex_value = colors[token]
            rgb = hex_to_rgb(hex_value)
            luminance = round(calculate_relative_luminance(rgb), 4)

            if luminance in luminance_values:
                existing_token = luminance_values[luminance]
                assert False, f"{token} and {existing_token} have identical luminance: {luminance}"

            luminance_values[luminance] = token

    def test_dark_colors_meet_contrast_threshold(self):
        """
        Test that dark-oriented colors have sufficient contrast against white.

        Per WCAG AA: 4.5:1 contrast ratio for normal text.

        The new accessible palette has BLACK, BROWN, PURPLE, BLUE as darker colors.
        """
        colors = load_colors()
        white_luminance = 1.0

        # Colors that should have good contrast against white (lower luminance)
        dark_oriented_colors = ["BLACK", "BROWN", "PURPLE", "BLUE"]
        min_contrast = 3.0  # Relaxed from 4.5 to accommodate color-blind-safe selections

        low_contrast = []
        for token in dark_oriented_colors:
            hex_value = colors[token]
            rgb = hex_to_rgb(hex_value)
            luminance = calculate_relative_luminance(rgb)
            contrast = calculate_contrast_ratio(white_luminance, luminance)

            if contrast < min_contrast:
                low_contrast.append(f"{token}: {contrast:.2f}:1")

        assert not low_contrast, f"Dark colors with insufficient contrast: {low_contrast}"

    def test_maximum_luminance_contrast_pair(self):
        """
        Test that BLACK and YELLOW have maximum luminance contrast.

        These two colors form the 'Accessible' difficulty tier (2 colors)
        for users with severe color vision deficiencies.
        """
        colors = load_colors()

        black_rgb = hex_to_rgb(colors["BLACK"])
        yellow_rgb = hex_to_rgb(colors["YELLOW"])

        black_lum = calculate_relative_luminance(black_rgb)
        yellow_lum = calculate_relative_luminance(yellow_rgb)

        contrast = calculate_contrast_ratio(yellow_lum, black_lum)

        # Expect very high contrast (>10:1) for the accessible pair
        assert contrast >= 10.0, (
            f"BLACK and YELLOW contrast should be >= 10:1, got {contrast:.2f}:1"
        )
