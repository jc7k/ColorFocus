"""
Spanish language support tests for ColorFocus.

These tests verify that Spanish language support is correctly implemented
in the shared JSON data files (color_labels.json and ui_text.json).

Updated for accessible color palette (2025-12-27):
- New 8-color palette: BLACK, BROWN, PURPLE, BLUE, GRAY, PINK, ORANGE, YELLOW
- Language key renamed from "chinese" to "zh-TW"
- Updated width multipliers
"""

import json
import re
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
COLOR_LABELS_JSON_PATH = PROJECT_ROOT / "shared" / "color_labels.json"
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"

# Expected Spanish translations for color labels (updated for accessible palette)
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

# All 8 color tokens (updated for accessible palette)
EXPECTED_COLOR_TOKENS = {"BLACK", "BROWN", "PURPLE", "BLUE", "GRAY", "PINK", "ORANGE", "YELLOW"}

# All supported languages (updated: chinese -> zh-TW)
ALL_SUPPORTED_LANGUAGES = ["zh-TW", "english", "vietnamese", "spanish"]


def load_color_labels() -> dict:
    """Load the color_labels.json file."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestSpanishColorLabels:
    """
    Verify Spanish color labels in shared/color_labels.json.

    These tests ensure the Spanish translations are correctly defined
    for all 8 colors in the color_labels.json file.
    """

    def test_color_labels_json_contains_spanish_key_for_all_colors(self):
        """
        Test that shared/color_labels.json contains spanish key for all 8 colors.

        This verifies the JSON data structure includes Spanish translations
        for the new accessible palette colors.
        """
        color_labels = load_color_labels()

        for token in EXPECTED_COLOR_TOKENS:
            assert token in color_labels, f"Missing color token: {token}"
            assert "spanish" in color_labels[token], (
                f"Color {token} missing 'spanish' key"
            )

    def test_spanish_color_labels_use_expected_values(self):
        """
        Test that Spanish color labels use expected values.

        Expected translations for accessible palette:
        BLACK=Negro, BROWN=Cafe, PURPLE=Morado, BLUE=Azul,
        GRAY=Gris, PINK=Rosa, ORANGE=Naranja, YELLOW=Amarillo
        """
        color_labels = load_color_labels()

        for token, expected_label in EXPECTED_SPANISH_LABELS.items():
            actual_label = color_labels[token]["spanish"]
            assert actual_label == expected_label, (
                f"Spanish label for {token} should be '{expected_label}', got '{actual_label}'"
            )


class TestSpanishUIText:
    """
    Verify Spanish UI text translations in shared/ui_text.json.

    These tests ensure the Spanish translations are correctly defined
    for all UI text entries in the ui_text.json file.
    """

    def test_ui_text_json_contains_spanish_key_for_all_entries(self):
        """
        Test that shared/ui_text.json contains spanish key for all 40+ UI text entries.

        This verifies every UI text entry includes a Spanish translation.
        """
        ui_text = load_ui_text()

        # There should be at least 40 entries
        assert len(ui_text) >= 40, (
            f"Expected at least 40 UI text entries, got {len(ui_text)}"
        )

        for key, translations in ui_text.items():
            assert "spanish" in translations, (
                f"UI text entry '{key}' missing 'spanish' key"
            )
            # Verify Spanish translation is not empty
            assert translations["spanish"].strip() != "", (
                f"UI text entry '{key}' has empty Spanish translation"
            )

    def test_language_descriptor_spanish_entry_exists(self):
        """
        Test that language_descriptor_spanish entry exists with translations in all four languages.

        Expected translations (updated for zh-TW):
        - zh-TW: "西班牙語單詞"
        - english: "Spanish word"
        - vietnamese: "tu tieng Tay Ban Nha"
        - spanish: "palabra en espanol"
        """
        ui_text = load_ui_text()

        assert "language_descriptor_spanish" in ui_text, (
            "UI text should contain 'language_descriptor_spanish' entry"
        )

        descriptor = ui_text["language_descriptor_spanish"]

        # Verify all four language translations exist
        expected_languages = ["zh-TW", "english", "vietnamese", "spanish"]
        for lang in expected_languages:
            assert lang in descriptor, (
                f"language_descriptor_spanish missing '{lang}' translation"
            )


class TestBackendSpanishLanguageEnum:
    """
    Verify Spanish language support in backend Language enum.

    These tests ensure the Language enum includes SPANISH value
    and that get_color_label() works correctly with Spanish.
    """

    def test_language_enum_includes_spanish_value(self):
        """
        Test that Language enum includes SPANISH value.

        This verifies the backend Language StrEnum has been updated
        to include SPANISH as a valid language option.
        """
        from backend.app.constants.color_labels import Language

        # Verify SPANISH is a valid Language enum member
        assert hasattr(Language, "SPANISH"), (
            "Language enum should have SPANISH member"
        )
        assert Language.SPANISH is not None, (
            "Language.SPANISH should not be None"
        )

    def test_language_spanish_value_equals_spanish_string(self):
        """
        Test that Language.SPANISH.value equals "spanish".

        This verifies the enum value matches the JSON key used
        in color_labels.json and ui_text.json.
        """
        from backend.app.constants.color_labels import Language

        assert Language.SPANISH.value == "spanish", (
            f"Language.SPANISH.value should be 'spanish', got '{Language.SPANISH.value}'"
        )

    def test_get_color_label_works_with_spanish_for_all_colors(self):
        """
        Test that get_color_label() works with Language.SPANISH for all 8 colors.

        This verifies the backend can retrieve Spanish labels for all color tokens
        by loading from the shared color_labels.json file.
        """
        from backend.app.constants.color_labels import Language, get_color_label
        from backend.app.constants.colors import ColorToken

        for token in ColorToken:
            label = get_color_label(token, Language.SPANISH)
            expected_label = EXPECTED_SPANISH_LABELS[token.value]
            assert label == expected_label, (
                f"Spanish label for {token.value} should be '{expected_label}', got '{label}'"
            )


class TestFrontendSpanishLanguageSupport:
    """
    Verify Spanish language support in frontend puzzle.html.

    These tests ensure the frontend properly supports Spanish:
    - Language dropdown includes Spanish option
    - VALID_LANGUAGES array includes "spanish"
    - widthMultipliers object includes "spanish" entry
    """

    def test_language_dropdown_includes_spanish_option(self):
        """
        Test that language dropdown includes Spanish option with value "spanish".

        This verifies the HTML select element for language includes
        an option element with value="spanish" and text "Spanish".
        """
        html_content = load_puzzle_html()

        # Look for Spanish option in language select
        # Pattern matches: <option value="spanish">Spanish</option>
        spanish_option_pattern = r'<option\s+value="spanish"\s*>Spanish</option>'
        match = re.search(spanish_option_pattern, html_content)

        assert match is not None, (
            "Language dropdown should include <option value=\"spanish\">Spanish</option>"
        )

    def test_valid_languages_array_includes_spanish(self):
        """
        Test that VALID_LANGUAGES array includes "spanish".

        This verifies the JavaScript constant VALID_LANGUAGES contains
        "spanish" as a valid language option for validation.
        """
        html_content = load_puzzle_html()

        # Look for VALID_LANGUAGES array containing spanish
        # Pattern matches: const VALID_LANGUAGES = [...'spanish'...]
        valid_languages_pattern = r"const\s+VALID_LANGUAGES\s*=\s*\[([^\]]+)\]"
        match = re.search(valid_languages_pattern, html_content)

        assert match is not None, (
            "VALID_LANGUAGES array declaration not found in puzzle.html"
        )

        array_content = match.group(1)
        assert "'spanish'" in array_content or '"spanish"' in array_content, (
            "VALID_LANGUAGES array should include 'spanish'"
        )

    def test_width_multipliers_includes_spanish_entry(self):
        """
        Test that widthMultipliers object includes "spanish" entry.

        This verifies the calculatePuzzleFontSize function includes
        a spanish entry in the widthMultipliers object for proper font sizing.
        """
        html_content = load_puzzle_html()

        # Look for widthMultipliers object containing spanish
        # Pattern matches widthMultipliers = { ... spanish: ... }
        width_multipliers_pattern = r"widthMultipliers\s*=\s*\{([^}]+)\}"
        match = re.search(width_multipliers_pattern, html_content)

        assert match is not None, (
            "widthMultipliers object declaration not found in puzzle.html"
        )

        object_content = match.group(1)
        assert "spanish:" in object_content or "spanish :" in object_content, (
            "widthMultipliers object should include 'spanish' entry"
        )

    def test_dynamic_font_sizing_supports_spanish(self):
        """
        Test that dynamic font sizing supports Spanish language.

        Updated for accessible palette - Spanish multiplier is now 4.8
        (longest word: "Amarillo" = 8 chars)
        """
        html_content = load_puzzle_html()

        # Verify widthMultipliers includes spanish with updated value
        assert "spanish: 4.8" in html_content or "spanish:4.8" in html_content, (
            "widthMultipliers should include spanish with value 4.8"
        )

        # Verify dynamic font calculation formula exists (0.8 factor for 80% text width)
        assert "cellWidth * 0.8" in html_content or "cellWidth*0.8" in html_content, (
            "Dynamic font calculation should use cellWidth * 0.8 formula"
        )


class TestSpanishLanguageIntegration:
    """
    Integration tests for Spanish language support.

    These tests verify that Spanish works correctly across all layers
    and that language switching between all four languages works properly.
    """

    def test_spanish_color_labels_max_length_within_budget(self):
        """
        Test that Spanish color labels do not exceed 8 character budget.

        Per new accessible palette: Maximum word length is 8 characters (Amarillo).
        This ensures Spanish text fits within grid cells properly.
        """
        color_labels = load_color_labels()
        max_length = 8

        for token in EXPECTED_COLOR_TOKENS:
            spanish_label = color_labels[token]["spanish"]
            assert len(spanish_label) <= max_length, (
                f"Spanish label for {token} ('{spanish_label}') exceeds {max_length} "
                f"character budget with {len(spanish_label)} characters"
            )

    def test_all_language_descriptors_include_spanish_translation(self):
        """
        Test that all language descriptor entries include Spanish translation.

        Updated for zh-TW: Verifies language_descriptor_zh-TW, language_descriptor_english,
        language_descriptor_vietnamese, and language_descriptor_spanish all
        have Spanish translations for proper language switching.
        """
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
        """
        Test that critical user workflow UI elements have Spanish translations.

        Verifies the core workflow: buttons for checking answers, section headers,
        and result messages all have proper Spanish translations.
        """
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
            assert len(spanish_text) > 0, (
                f"Critical UI element '{key}' Spanish translation is empty"
            )

    def test_all_four_languages_have_consistent_structure_in_color_labels(self):
        """
        Test that all four languages have consistent structure in color_labels.json.

        Updated for zh-TW: Verifies that switching between zh-TW, english, vietnamese,
        and spanish works correctly by ensuring all languages are present for all colors.
        """
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
        """
        Test that Spanish translations use appropriate vocabulary for target users.

        Per spec: words should be commonly understood and appropriate for
        elderly/stroke patient users. Verifies no abbreviations or truncated words.
        """
        color_labels = load_color_labels()

        # Check that Spanish labels are complete words (no truncation)
        for token, expected_label in EXPECTED_SPANISH_LABELS.items():
            actual_label = color_labels[token]["spanish"]
            # Labels should not contain periods (which would indicate abbreviation)
            assert "." not in actual_label, (
                f"Spanish label for {token} appears to be abbreviated: '{actual_label}'"
            )
            # Labels should match expected commonly understood words
            assert actual_label == expected_label, (
                f"Spanish label for {token} should be '{expected_label}', got '{actual_label}'"
            )
