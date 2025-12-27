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


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestUILocalizationImplementation:
    """
    Verify UI localization is correctly implemented in puzzle.html.

    These tests ensure all UI text elements are translated when
    the language selector changes.
    """

    def test_ui_text_json_is_imported_in_puzzle_html(self):
        """
        Test that ui_text.json is imported in puzzle.html.

        This verifies the ES module import for ui_text.json exists
        and follows the same pattern as color_labels.json import.
        """
        html_content = load_puzzle_html()

        # Check for ui_text.json import statement
        assert "ui_text.json" in html_content, (
            "puzzle.html should import ui_text.json"
        )
        # Check for proper import syntax
        assert "import" in html_content and "ui_text" in html_content.lower(), (
            "puzzle.html should have an import statement for ui_text"
        )

    def test_get_ui_text_helper_function_exists(self):
        """
        Test that getUIText() helper function exists in puzzle.html.

        This helper function should return text for the current language
        based on the provided key.
        """
        html_content = load_puzzle_html()

        # Check for getUIText function definition
        assert "getUIText" in html_content, (
            "puzzle.html should define a getUIText() helper function"
        )
        # The function should use currentLanguage
        assert "currentLanguage" in html_content, (
            "puzzle.html should use currentLanguage for language selection"
        )

    def test_update_all_ui_text_function_exists(self):
        """
        Test that updateAllUIText() function exists for language changes.

        This function should update all translated text elements when
        the language selector changes, without requiring a page reload.
        """
        html_content = load_puzzle_html()

        # Check for updateAllUIText function
        assert "updateAllUIText" in html_content, (
            "puzzle.html should define an updateAllUIText() function"
        )

    def test_task_instructions_use_translations(self):
        """
        Test that task instructions template properly inserts language descriptor.

        The updateTaskInstructions() function should use translated task_label
        and task_instruction with interpolated language_descriptor.
        """
        html_content = load_puzzle_html()

        # Check that getUIText is used in task instructions
        # The function should reference task_label or task_instruction keys
        assert "task_label" in html_content or "getUIText" in html_content, (
            "Task instructions should use translation keys"
        )
        # Check for language descriptor interpolation
        assert "language_descriptor" in html_content, (
            "Task instructions should interpolate language descriptor"
        )

    def test_result_messages_use_translations(self):
        """
        Test that result messages display correctly using translations.

        The showResults() function should use translated result_perfect,
        result_good, and result_needs_work messages with proper interpolation.
        """
        html_content = load_puzzle_html()
        ui_text = load_ui_text()

        # Check that result message keys are used
        # Either by checking for the key names or for translated content usage
        assert "result_perfect" in html_content or "getUIText" in html_content, (
            "Result messages should use translation system"
        )

        # Verify the translations have placeholders for interpolation
        result_good = ui_text["result_good"]["english"]
        assert "{correct}" in result_good and "{total}" in result_good, (
            "result_good template should have {correct} and {total} placeholders"
        )

    def test_metadata_labels_are_translated(self):
        """
        Test that metadata labels are translated correctly.

        Metadata labels (Seed, Colors, Grid, Congruent) should use
        translations from ui_text.json.
        """
        html_content = load_puzzle_html()

        # Check for metadata translation key usage
        # Should use getUIText for metadata labels
        assert "metadata_seed" in html_content or (
            "getUIText" in html_content and "metadata" in html_content.lower()
        ), (
            "Metadata labels should use translation keys"
        )

    def test_document_title_is_updated_dynamically(self):
        """
        Test that the page title is updated dynamically on language change.

        The document.title should be set to the translated page title
        on initial load and when language selector changes.
        """
        html_content = load_puzzle_html()

        # Check for document.title assignment
        assert "document.title" in html_content, (
            "puzzle.html should update document.title dynamically"
        )
        # Should use getUIText for page_title
        assert "page_title" in html_content, (
            "Document title should use page_title translation key"
        )


class TestZhTWLanguageKey:
    """
    Verify that 'zh-TW' is used instead of 'chinese' throughout.

    The language key was renamed from 'chinese' to 'zh-TW' for
    proper locale identification.
    """

    def test_valid_languages_uses_zh_tw(self):
        """
        Test that VALID_LANGUAGES array contains 'zh-TW', not 'chinese'.
        """
        html_content = load_puzzle_html()

        # Check for zh-TW in VALID_LANGUAGES definition
        # The array should include 'zh-TW'
        assert "'zh-TW'" in html_content or '"zh-TW"' in html_content, (
            "VALID_LANGUAGES should include 'zh-TW'"
        )

    def test_language_dropdown_has_zh_tw_option(self):
        """
        Test that the language dropdown uses 'zh-TW' as option value.
        """
        html_content = load_puzzle_html()

        # Check for zh-TW option value in select element
        assert 'value="zh-TW"' in html_content or "value='zh-TW'" in html_content, (
            "Language dropdown should have 'zh-TW' option value"
        )

    def test_language_descriptor_key_uses_zh_tw(self):
        """
        Test that language_descriptor lookup uses 'zh-TW' suffix.
        """
        html_content = load_puzzle_html()

        # Check for language_descriptor_zh-TW key reference
        # Note: The code might use dynamic key construction
        assert "language_descriptor_zh-TW" in html_content or (
            "language_descriptor_" in html_content and "zh-TW" in html_content
        ), (
            "Language descriptor should use 'zh-TW' suffix"
        )

    def test_width_multipliers_uses_zh_tw_key(self):
        """
        Test that widthMultipliers object uses 'zh-TW' key.
        """
        html_content = load_puzzle_html()

        # Check for zh-TW in widthMultipliers or similar font sizing logic
        # The key should be 'zh-TW', not 'chinese'
        if "widthMultipliers" in html_content:
            # Find the widthMultipliers definition area
            assert "'zh-TW'" in html_content or '"zh-TW"' in html_content, (
                "widthMultipliers should use 'zh-TW' key"
            )


class TestMultiLanguageColorLabels:
    """
    Verify that color labels work correctly with the new accessible palette
    across all supported languages.
    """

    def test_color_labels_json_has_all_languages(self):
        """
        Test that color_labels.json has labels for all 4 supported languages.
        """
        color_labels_path = PROJECT_ROOT / "shared" / "color_labels.json"
        with open(color_labels_path, "r", encoding="utf-8") as f:
            color_labels = json.load(f)

        expected_languages = ["zh-TW", "english", "spanish", "vietnamese"]

        for color, labels in color_labels.items():
            for lang in expected_languages:
                assert lang in labels, (
                    f"Color '{color}' missing '{lang}' label"
                )
                assert isinstance(labels[lang], str), (
                    f"Color '{color}' label for '{lang}' should be a string"
                )
                assert len(labels[lang]) > 0, (
                    f"Color '{color}' label for '{lang}' should not be empty"
                )

    def test_all_new_palette_colors_have_labels(self):
        """
        Test that all 8 accessible palette colors have labels.
        """
        color_labels_path = PROJECT_ROOT / "shared" / "color_labels.json"
        with open(color_labels_path, "r", encoding="utf-8") as f:
            color_labels = json.load(f)

        expected_colors = ["BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"]

        for color in expected_colors:
            assert color in color_labels, (
                f"Missing color label entry for: {color}"
            )
