"""
UI localization frontend tests for ColorFocus.

These tests verify that UI text localization works correctly in the frontend
when switching languages. Tests simulate browser behavior to validate the
localization implementation.

Updated for the accessible color palette replacement:
- Language key "chinese" renamed to "zh-TW"
- VALID_LANGUAGES now uses 'zh-TW' instead of 'chinese'
"""

import json
from pathlib import Path

from conftest import load_puzzle_html, load_puzzle_js, load_puzzle_html_and_js


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestUILocalizationImplementation:
    """
    Verify UI localization is correctly implemented in puzzle.html.

    These tests ensure all UI text elements are translated when
    the language selector changes.
    """

    def test_ui_text_json_is_imported_in_puzzle_html(self):
        """
        Test that ui_text.json is imported in puzzle.html or JS modules.

        This verifies the ES module import for ui_text.json exists
        and follows the same pattern as color_labels.json import.
        """
        js_content = load_puzzle_js()

        # Check for ui_text.json import statement
        assert "ui_text.json" in js_content, (
            "JavaScript modules should import ui_text.json"
        )

    def test_get_ui_text_helper_function_exists(self):
        """
        Test that getUIText() helper function is defined.

        The helper should:
        1. Accept a key parameter
        2. Return translated text for current language
        3. Fall back to English if key not found for language
        """
        js_content = load_puzzle_js()

        assert "function getUIText" in js_content or "getUIText" in js_content, (
            "getUIText helper function should be defined"
        )
        # Check for language fallback pattern
        assert "currentLanguage" in js_content, (
            "getUIText should use currentLanguage state"
        )

    def test_update_all_ui_text_function_exists(self):
        """
        Test that updateAllUIText() function is defined.

        This function should update all UI elements when language changes.
        """
        js_content = load_puzzle_js()

        assert "function updateAllUIText" in js_content or "updateAllUIText" in js_content, (
            "updateAllUIText function should be defined"
        )

    def test_task_instructions_use_translations(self):
        """
        Test that task instructions use getUIText() for localization.
        """
        js_content = load_puzzle_js()

        # Task instructions should call getUIText
        assert "getUIText('task_instruction')" in js_content or "getUIText(\"task_instruction\")" in js_content, (
            "Task instructions should use getUIText for localization"
        )

    def test_result_messages_use_translations(self):
        """
        Test that result messages use getUIText() for localization.
        """
        js_content = load_puzzle_js()

        # Result messages should call getUIText
        has_result_perfect = (
            "getUIText('result_perfect')" in js_content or
            "getUIText(\"result_perfect\")" in js_content
        )
        assert has_result_perfect, (
            "Result messages should use getUIText for localization"
        )

    def test_metadata_labels_are_translated(self):
        """
        Test that metadata labels use getUIText() for localization.
        """
        js_content = load_puzzle_js()

        # Metadata should use translated labels
        has_metadata_seed = (
            "getUIText('metadata_seed')" in js_content or
            "getUIText(\"metadata_seed\")" in js_content
        )
        assert has_metadata_seed, (
            "Metadata labels should use getUIText for localization"
        )

    def test_document_title_is_updated_dynamically(self):
        """
        Test that document title is updated when language changes.
        """
        js_content = load_puzzle_js()

        # Check for dynamic title update
        has_title_update = (
            "document.title" in js_content and
            "getUIText" in js_content
        )
        assert has_title_update, (
            "Document title should be updated dynamically via getUIText"
        )


class TestZhTWLanguageKey:
    """
    Verify 'zh-TW' is used consistently instead of 'chinese'.
    """

    def test_valid_languages_uses_zh_tw(self):
        """
        Test that VALID_LANGUAGES array uses 'zh-TW' key.
        """
        js_content = load_puzzle_js()

        assert "'zh-TW'" in js_content or '"zh-TW"' in js_content, (
            "VALID_LANGUAGES should include 'zh-TW'"
        )
        # Verify 'chinese' is not used as a language key
        assert "VALID_LANGUAGES" not in js_content or "'chinese'" not in js_content, (
            "VALID_LANGUAGES should use 'zh-TW' not 'chinese'"
        )

    def test_language_dropdown_has_zh_tw_option(self):
        """
        Test that language dropdown has zh-TW option.
        """
        html_content = load_puzzle_html()

        assert 'value="zh-TW"' in html_content, (
            "Language dropdown should have zh-TW option"
        )

    def test_language_descriptor_key_uses_zh_tw(self):
        """
        Test that language descriptor uses zh-TW key format.
        """
        js_content = load_puzzle_js()

        # Check for language_descriptor pattern with zh-TW
        assert "language_descriptor" in js_content, (
            "Language descriptor pattern should be used"
        )

    def test_width_multipliers_uses_zh_tw_key(self):
        """
        Test that widthMultipliers object uses 'zh-TW' key.
        """
        js_content = load_puzzle_js()

        assert "'zh-TW'" in js_content, (
            "widthMultipliers should use 'zh-TW' key"
        )


class TestMultiLanguageColorLabels:
    """
    Verify color labels support all languages.
    """

    def test_color_labels_json_has_all_languages(self):
        """
        Test that color_labels.json has all four supported languages.
        """
        color_labels_path = PROJECT_ROOT / "shared" / "color_labels.json"
        with open(color_labels_path, "r", encoding="utf-8") as f:
            color_labels = json.load(f)

        required_languages = ["zh-TW", "english", "spanish", "vietnamese"]

        # Check first color token has all languages
        first_token = list(color_labels.keys())[0]
        for lang in required_languages:
            assert lang in color_labels[first_token], (
                f"Color label for {first_token} should have {lang} translation"
            )

    def test_all_new_palette_colors_have_labels(self):
        """
        Test that all new palette colors have labels in all languages.
        """
        color_labels_path = PROJECT_ROOT / "shared" / "color_labels.json"
        with open(color_labels_path, "r", encoding="utf-8") as f:
            color_labels = json.load(f)

        new_palette_tokens = ['BLACK', 'BROWN', 'PURPLE', 'BLUE', 'GRAY', 'PINK', 'ORANGE', 'YELLOW']
        required_languages = ["zh-TW", "english", "spanish", "vietnamese"]

        for token in new_palette_tokens:
            assert token in color_labels, f"Color label for {token} should exist"
            for lang in required_languages:
                assert lang in color_labels[token], (
                    f"Color label for {token} should have {lang} translation"
                )
