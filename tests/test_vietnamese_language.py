"""
Vietnamese language support tests for ColorFocus.

These tests verify that Vietnamese language support is correctly implemented
in the shared JSON, backend color label module, and frontend puzzle.html.

This test file covers all Task Groups for Vietnamese Language Support.
"""

import json
import re
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
COLOR_LABELS_JSON_PATH = PROJECT_ROOT / "shared" / "color_labels.json"
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"

# Expected Vietnamese translations with proper diacritical marks
EXPECTED_VIETNAMESE_LABELS = {
    "BLUE": "Xanh",
    "ORANGE": "Cam",
    "PURPLE": "Tím",
    "BLACK": "Đen",
    "CYAN": "Lơ",
    "AMBER": "Vàng",
    "MAGENTA": "Hồng",
    "GRAY": "Xám",
}


def load_color_labels() -> dict:
    """Load the color_labels.json file."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestVietnameseLanguageData:
    """
    Verify Vietnamese language support in shared data and backend.

    These tests ensure the Vietnamese translations are correctly defined
    and can be accessed through the backend Language enum.
    """

    def test_color_labels_json_contains_vietnamese_key_for_all_colors(self):
        """
        Test that shared/color_labels.json contains vietnamese key for all 8 colors.

        This verifies the JSON data structure includes Vietnamese translations.
        """
        color_labels = load_color_labels()

        expected_tokens = {"BLUE", "ORANGE", "PURPLE", "BLACK", "CYAN", "AMBER", "MAGENTA", "GRAY"}

        for token in expected_tokens:
            assert token in color_labels, f"Missing color token: {token}"
            assert "vietnamese" in color_labels[token], (
                f"Color {token} missing 'vietnamese' key"
            )

    def test_vietnamese_labels_use_proper_utf8_encoding(self):
        """
        Test that Vietnamese labels use proper UTF-8 encoding with diacritical marks.

        Vietnamese requires proper encoding for characters with diacritical marks
        such as Tím, Đen, Lơ, Vàng, Hồng, Xám.
        """
        color_labels = load_color_labels()

        # Test specific characters with diacritical marks
        assert color_labels["PURPLE"]["vietnamese"] == "Tím", (
            f"PURPLE should be 'Tím' (with accent), got '{color_labels['PURPLE']['vietnamese']}'"
        )
        assert color_labels["BLACK"]["vietnamese"] == "Đen", (
            f"BLACK should be 'Đen' (with đ), got '{color_labels['BLACK']['vietnamese']}'"
        )
        assert color_labels["CYAN"]["vietnamese"] == "Lơ", (
            f"CYAN should be 'Lơ' (with hook), got '{color_labels['CYAN']['vietnamese']}'"
        )
        assert color_labels["AMBER"]["vietnamese"] == "Vàng", (
            f"AMBER should be 'Vàng' (with accent), got '{color_labels['AMBER']['vietnamese']}'"
        )
        assert color_labels["MAGENTA"]["vietnamese"] == "Hồng", (
            f"MAGENTA should be 'Hồng' (with accent), got '{color_labels['MAGENTA']['vietnamese']}'"
        )
        assert color_labels["GRAY"]["vietnamese"] == "Xám", (
            f"GRAY should be 'Xám' (with accent), got '{color_labels['GRAY']['vietnamese']}'"
        )

    def test_backend_language_enum_includes_vietnamese(self):
        """
        Test that backend Language enum includes VIETNAMESE value.

        This verifies the Python backend can reference Vietnamese as a language option.
        """
        from backend.app.constants.color_labels import Language

        # Check VIETNAMESE enum exists
        assert hasattr(Language, "VIETNAMESE"), (
            "Language enum should have VIETNAMESE member"
        )
        assert Language.VIETNAMESE.value == "vietnamese", (
            f"Language.VIETNAMESE should have value 'vietnamese', got '{Language.VIETNAMESE.value}'"
        )

    def test_get_color_label_works_with_vietnamese(self):
        """
        Test that get_color_label() works with Language.VIETNAMESE for all colors.

        This verifies the full integration of Vietnamese in the backend module.
        """
        from backend.app.constants.color_labels import Language, get_color_label
        from backend.app.constants.colors import ColorToken

        for token in ColorToken:
            label = get_color_label(token, Language.VIETNAMESE)
            expected = EXPECTED_VIETNAMESE_LABELS[token.value]
            assert label == expected, (
                f"get_color_label({token}, VIETNAMESE) expected '{expected}', got '{label}'"
            )


class TestLanguageSelectorUI:
    """
    Verify language selector UI components in puzzle.html.

    These tests validate the HTML structure contains proper language selector
    elements with correct options and accessibility attributes.
    """

    def test_language_dropdown_has_three_options(self):
        """
        Test that language dropdown renders with 3 options: Chinese, English, Vietnamese.

        This verifies the select element includes all supported languages.
        """
        html_content = load_puzzle_html()

        # Check for select element with id="language"
        assert 'id="language"' in html_content, (
            "puzzle.html should have a select element with id='language'"
        )

        # Check for all three language options
        assert 'value="chinese"' in html_content, (
            "Language dropdown should have Chinese option"
        )
        assert 'value="english"' in html_content, (
            "Language dropdown should have English option"
        )
        assert 'value="vietnamese"' in html_content, (
            "Language dropdown should have Vietnamese option"
        )

    def test_language_dropdown_has_accessibility_label(self):
        """
        Test that language dropdown has proper aria-label for accessibility.

        This verifies the select element has the required ARIA attribute.
        """
        html_content = load_puzzle_html()

        # Check for aria-label on the language select element
        assert 'aria-label="Select display language"' in html_content, (
            "Language dropdown should have aria-label='Select display language'"
        )


class TestLanguageSwitchingLogic:
    """
    Verify language switching logic is implemented in puzzle.html JavaScript.

    These tests validate the JavaScript code contains necessary state management
    and event handling for language switching.
    """

    def test_current_language_state_variable_exists(self):
        """
        Test that currentLanguage state variable is initialized in JavaScript.

        This verifies the language state management is implemented.
        """
        html_content = load_puzzle_html()

        # Check for currentLanguage variable initialization with localStorage fallback
        assert "currentLanguage" in html_content, (
            "JavaScript should define currentLanguage variable"
        )
        assert "localStorage.getItem('colorFocusLanguage')" in html_content, (
            "JavaScript should read language preference from localStorage"
        )

    def test_language_change_event_listener_exists(self):
        """
        Test that language change event listener is implemented.

        This verifies the dropdown change triggers re-rendering.
        """
        html_content = load_puzzle_html()

        # Check for event listener on language selector
        assert "addEventListener('change'" in html_content, (
            "JavaScript should add change event listener for language switching"
        )
        assert "localStorage.setItem('colorFocusLanguage'" in html_content, (
            "JavaScript should save language preference to localStorage on change"
        )

    def test_language_descriptors_defined_for_instructions(self):
        """
        Test that language descriptors are defined for task instructions text.

        This verifies the dynamic instruction text can be updated per language.
        """
        html_content = load_puzzle_html()

        # Check for LANGUAGE_DESCRIPTORS object with all three languages
        assert "LANGUAGE_DESCRIPTORS" in html_content, (
            "JavaScript should define LANGUAGE_DESCRIPTORS object"
        )
        assert "'Chinese character'" in html_content or '"Chinese character"' in html_content, (
            "LANGUAGE_DESCRIPTORS should include 'Chinese character'"
        )
        assert "'English word'" in html_content or '"English word"' in html_content, (
            "LANGUAGE_DESCRIPTORS should include 'English word'"
        )
        assert "'Vietnamese word'" in html_content or '"Vietnamese word"' in html_content, (
            "LANGUAGE_DESCRIPTORS should include 'Vietnamese word'"
        )
