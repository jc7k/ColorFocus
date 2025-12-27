"""
Tests for JSON structure validation for the accessible color palette replacement.

These tests validate:
1. colors.json contains exactly 8 color tokens with flat hex values
2. color_labels.json contains all 8 colors with 4 language keys including "zh-TW"
3. ui_text.json contains "zh-TW" key (not "chinese") in all entries
4. All hex values are valid 7-character format (#RRGGBB)
"""

import json
import re
from pathlib import Path


# Paths to shared JSON files
SHARED_DIR = Path(__file__).parent.parent / "shared"
COLORS_JSON_PATH = SHARED_DIR / "colors.json"
COLOR_LABELS_JSON_PATH = SHARED_DIR / "color_labels.json"
UI_TEXT_JSON_PATH = SHARED_DIR / "ui_text.json"

# Expected color tokens for the accessible palette
EXPECTED_COLOR_TOKENS = ["BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"]

# Expected language keys
EXPECTED_LANGUAGE_KEYS = ["zh-TW", "english", "spanish", "vietnamese"]

# Hex color pattern (#RRGGBB - exactly 7 characters)
HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestColorsJsonFlatStructure:
    """Test that colors.json contains exactly 8 color tokens with flat hex values."""

    def test_colors_json_contains_exactly_8_tokens(self):
        """Test colors.json has exactly 8 color tokens."""
        colors = load_json(COLORS_JSON_PATH)

        assert len(colors) == 8, f"Expected 8 color tokens, got {len(colors)}"

        for token in EXPECTED_COLOR_TOKENS:
            assert token in colors, f"Missing expected color token: {token}"

    def test_colors_json_has_flat_hex_values(self):
        """Test that each color token maps directly to a hex value (no variants)."""
        colors = load_json(COLORS_JSON_PATH)

        for token, value in colors.items():
            # Value should be a string (hex), not a dict (variants structure)
            assert isinstance(value, str), \
                f"{token} should be a flat hex string, not {type(value).__name__}"
            # Should not have nested 'variants' structure
            assert not isinstance(value, dict), \
                f"{token} should not have nested structure"


class TestColorLabelsLanguageKeys:
    """Test that color_labels.json contains all 8 colors with 4 language keys including 'zh-TW'."""

    def test_color_labels_contains_all_8_colors(self):
        """Test color_labels.json has all 8 expected color tokens."""
        labels = load_json(COLOR_LABELS_JSON_PATH)

        assert len(labels) == 8, f"Expected 8 color entries, got {len(labels)}"

        for token in EXPECTED_COLOR_TOKENS:
            assert token in labels, f"Missing color label entry: {token}"

    def test_color_labels_has_zh_tw_key(self):
        """Test that each color has 'zh-TW' key (not 'chinese')."""
        labels = load_json(COLOR_LABELS_JSON_PATH)

        for token in EXPECTED_COLOR_TOKENS:
            color_entry = labels[token]

            # Must have zh-TW key
            assert "zh-TW" in color_entry, \
                f"{token} is missing 'zh-TW' language key"

            # Must NOT have 'chinese' key (old format)
            assert "chinese" not in color_entry, \
                f"{token} should not have 'chinese' key - should be 'zh-TW'"

            # Verify all 4 language keys are present
            for lang in EXPECTED_LANGUAGE_KEYS:
                assert lang in color_entry, \
                    f"{token} is missing '{lang}' language key"


class TestUiTextLanguageKeys:
    """Test that ui_text.json contains 'zh-TW' key (not 'chinese') in all entries."""

    def test_ui_text_uses_zh_tw_key(self):
        """Test that all ui_text entries use 'zh-TW' instead of 'chinese'."""
        ui_text = load_json(UI_TEXT_JSON_PATH)

        entries_with_chinese = []
        entries_missing_zh_tw = []

        for key, translations in ui_text.items():
            if isinstance(translations, dict):
                if "chinese" in translations:
                    entries_with_chinese.append(key)
                if "zh-TW" not in translations and "english" in translations:
                    # Only check entries that have language keys (not meta keys)
                    entries_missing_zh_tw.append(key)

        assert not entries_with_chinese, \
            f"Entries still using 'chinese' key: {entries_with_chinese}"
        assert not entries_missing_zh_tw, \
            f"Entries missing 'zh-TW' key: {entries_missing_zh_tw}"

    def test_ui_text_language_descriptor_zh_tw(self):
        """Test that language_descriptor uses 'zh-TW' suffix."""
        ui_text = load_json(UI_TEXT_JSON_PATH)

        # Old key should not exist
        assert "language_descriptor_chinese" not in ui_text, \
            "Old 'language_descriptor_chinese' key should be renamed to 'language_descriptor_zh-TW'"

        # New key should exist
        assert "language_descriptor_zh-TW" in ui_text, \
            "Missing 'language_descriptor_zh-TW' key"


class TestHexValueFormat:
    """Test that all hex values in colors.json are valid 7-character format (#RRGGBB)."""

    def test_all_hex_values_are_valid_format(self):
        """Test that all color hex values match #RRGGBB format."""
        colors = load_json(COLORS_JSON_PATH)

        invalid_values = []
        for token, hex_value in colors.items():
            if not HEX_PATTERN.match(hex_value):
                invalid_values.append(f"{token}: {hex_value}")

        assert not invalid_values, \
            f"Invalid hex values found (expected #RRGGBB format): {invalid_values}"

    def test_hex_values_are_exactly_7_characters(self):
        """Test that all hex values are exactly 7 characters (#RRGGBB)."""
        colors = load_json(COLORS_JSON_PATH)

        wrong_length = []
        for token, hex_value in colors.items():
            if len(hex_value) != 7:
                wrong_length.append(f"{token}: {hex_value} (length={len(hex_value)})")

        assert not wrong_length, \
            f"Hex values with wrong length (expected 7): {wrong_length}"
