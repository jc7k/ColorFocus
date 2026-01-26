"""
Spanish language frontend and integration tests for ColorFocus.

These tests verify Spanish language support in:
- Frontend puzzle.html (dropdown, validation, font sizing)
- Integration across all layers
"""

import json
import re
from pathlib import Path

from conftest import load_puzzle_html, load_puzzle_js


PROJECT_ROOT = Path(__file__).parent.parent
COLOR_LABELS_JSON_PATH = PROJECT_ROOT / "shared" / "color_labels.json"
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"

# Expected Spanish translations for color labels (accessible palette)
EXPECTED_SPANISH_LABELS = {
    "BLACK": "Negro",
    "BROWN": "Cafe",
    "PURPLE": "Morado",
    "BLUE": "Azul",
    "GRAY": "Gris",
    "PINK": "Rosa",
    "ORANGE": "Naranja",
    "YELLOW": "Amarillo",
}

EXPECTED_COLOR_TOKENS = {"BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"}
ALL_SUPPORTED_LANGUAGES = ["zh-TW", "english", "vietnamese", "spanish"]


def load_color_labels() -> dict:
    """Load the color_labels.json file."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestFrontendSpanishLanguageSupport:
    """Verify Spanish language support in frontend puzzle.html."""

    def test_language_dropdown_includes_spanish_option(self):
        """Test that language dropdown includes Spanish option."""
        html_content = load_puzzle_html()

        spanish_option_pattern = r'<option\s+value="spanish"\s*>Spanish</option>'
        match = re.search(spanish_option_pattern, html_content)

        assert match is not None, (
            "Language dropdown should include <option value=\"spanish\">Spanish</option>"
        )

    def test_valid_languages_array_includes_spanish(self):
        """Test that VALID_LANGUAGES array includes 'spanish'."""
        js_content = load_puzzle_js()

        valid_languages_pattern = r"const\s+VALID_LANGUAGES\s*=\s*\[([^\]]+)\]"
        match = re.search(valid_languages_pattern, js_content)

        assert match is not None, (
            "VALID_LANGUAGES array declaration not found in JavaScript modules"
        )

        array_content = match.group(1)
        assert "'spanish'" in array_content or '"spanish"' in array_content, (
            "VALID_LANGUAGES array should include 'spanish'"
        )

    def test_width_multipliers_includes_spanish_entry(self):
        """Test that widthMultipliers object includes 'spanish' entry."""
        js_content = load_puzzle_js()

        width_multipliers_pattern = r"widthMultipliers\s*=\s*\{([^}]+)\}"
        match = re.search(width_multipliers_pattern, js_content)

        assert match is not None, (
            "widthMultipliers object declaration not found in JavaScript modules"
        )

        object_content = match.group(1)
        assert "spanish:" in object_content or "spanish :" in object_content, (
            "widthMultipliers object should include 'spanish' entry"
        )

    def test_dynamic_font_sizing_supports_spanish(self):
        """Test that dynamic font sizing supports Spanish language."""
        js_content = load_puzzle_js()

        assert "spanish: 4.2" in js_content or "spanish:4.2" in js_content, (
            "widthMultipliers should include spanish with value 4.2"
        )

        assert "cellWidth * 0.8" in js_content or "cellWidth*0.8" in js_content, (
            "Dynamic font calculation should use cellWidth * 0.8 formula"
        )


class TestSpanishLanguageIntegration:
    """Integration tests for Spanish language support."""

    def test_spanish_color_labels_max_length_within_budget(self):
        """Test that Spanish color labels do not exceed 8 character budget."""
        color_labels = load_color_labels()
        max_length = 8

        for token in EXPECTED_COLOR_TOKENS:
            spanish_label = color_labels[token]["spanish"]
            assert len(spanish_label) <= max_length, (
                f"Spanish label for {token} ('{spanish_label}') exceeds {max_length} characters"
            )

    def test_all_language_descriptors_include_spanish_translation(self):
        """Test that all language descriptor entries include Spanish translation."""
        ui_text = load_ui_text()

        descriptor_keys = [
            "language_descriptor_zh-TW",
            "language_descriptor_english",
            "language_descriptor_vietnamese",
            "language_descriptor_spanish",
        ]

        for key in descriptor_keys:
            assert key in ui_text, f"Missing language descriptor: {key}"
            assert "spanish" in ui_text[key], (
                f"Language descriptor '{key}' missing 'spanish' translation"
            )
            assert ui_text[key]["spanish"].strip() != "", (
                f"Language descriptor '{key}' has empty Spanish translation"
            )

    def test_critical_workflow_ui_elements_have_spanish_translations(self):
        """Test that critical UI elements have Spanish translations."""
        ui_text = load_ui_text()

        critical_keys = [
            "check_btn",
            "clear_btn",
            "generate_btn",
            "enter_answers_header",
            "results_header",
            "answer_key_header",
            "result_perfect",
            "result_good",
            "result_needs_work",
        ]

        for key in critical_keys:
            assert key in ui_text, f"Missing critical UI element: {key}"
            assert "spanish" in ui_text[key], (
                f"Critical UI element '{key}' missing Spanish translation"
            )
            spanish_text = ui_text[key]["spanish"]
            assert spanish_text.strip() != "", (
                f"Critical UI element '{key}' has empty Spanish translation"
            )

    def test_all_four_languages_have_consistent_structure_in_color_labels(self):
        """Test that all four languages have consistent structure in color_labels.json."""
        color_labels = load_color_labels()

        for token in EXPECTED_COLOR_TOKENS:
            for lang in ALL_SUPPORTED_LANGUAGES:
                assert lang in color_labels[token], (
                    f"Color {token} missing '{lang}' language key"
                )
                label = color_labels[token][lang]
                assert label is not None and label.strip() != "", (
                    f"Color {token} has empty or None '{lang}' label"
                )

    def test_spanish_translations_use_appropriate_vocabulary(self):
        """Test that Spanish translations use appropriate vocabulary."""
        color_labels = load_color_labels()

        for token, expected_label in EXPECTED_SPANISH_LABELS.items():
            actual_label = color_labels[token]["spanish"]
            assert "." not in actual_label, (
                f"Spanish label for {token} appears to be abbreviated: '{actual_label}'"
            )
            assert actual_label == expected_label, (
                f"Spanish label for {token} should be '{expected_label}', got '{actual_label}'"
            )
