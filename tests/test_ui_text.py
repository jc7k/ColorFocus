"""
UI text localization tests for ColorFocus.

These tests verify that UI text translations are correctly implemented
in the shared JSON and backend ui_text module.

This test file covers Task Group 1: UI Translation Data.
"""

import json
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"

# Required UI text keys that must be present for each language
REQUIRED_UI_TEXT_KEYS = [
    "page_title",
    "subtitle",
    "task_label",
    "task_instruction",
    "language_label",
    "grid_label",
    "colors_label",
    "seed_label",
    "match_label",
    "generate_btn",
    "random_btn",
    "enter_answers_header",
    "check_btn",
    "clear_btn",
    "results_header",
    "answer_key_header",
    "reveal_btn",
    "hide_btn",
    "reveal_warning",
    "metadata_seed",
    "metadata_colors",
    "metadata_grid",
    "metadata_congruent",
    "result_perfect",
    "result_good",
    "result_needs_work",
    "result_colors_correct",
    "result_accuracy",
    "result_total_off",
    "language_descriptor_chinese",
    "language_descriptor_english",
    "language_descriptor_vietnamese",
]

# Vietnamese text samples that must contain diacritical marks
VIETNAMESE_DIACRITICAL_SAMPLES = {
    "page_title": True,  # Should contain Vietnamese characters
    "subtitle": True,
    "task_label": True,
    "task_instruction": True,
}


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestUITextDataLoading:
    """
    Verify UI text JSON file loading and structure.

    These tests ensure the ui_text.json file is correctly structured
    and can be loaded at module initialization time.
    """

    def test_ui_text_json_loads_correctly(self):
        """
        Test that ui_text.json loads correctly at module initialization.

        This verifies the JSON file exists, is valid JSON, and can be parsed.
        """
        ui_text = load_ui_text()

        assert isinstance(ui_text, dict), (
            "ui_text.json should parse to a dictionary"
        )
        assert len(ui_text) > 0, (
            "ui_text.json should contain at least one key"
        )

    def test_all_required_ui_text_keys_exist_for_each_language(self):
        """
        Test that all required UI text keys exist for each language.

        This verifies chinese, english, and vietnamese translations exist
        for every required UI text key.
        """
        ui_text = load_ui_text()
        languages = ["chinese", "english", "vietnamese"]

        for key in REQUIRED_UI_TEXT_KEYS:
            assert key in ui_text, (
                f"Missing required UI text key: {key}"
            )

            for lang in languages:
                assert lang in ui_text[key], (
                    f"UI text key '{key}' missing '{lang}' translation"
                )
                assert isinstance(ui_text[key][lang], str), (
                    f"UI text key '{key}' {lang} value should be a string"
                )
                assert len(ui_text[key][lang]) > 0, (
                    f"UI text key '{key}' {lang} value should not be empty"
                )

    def test_vietnamese_text_contains_proper_diacritical_marks(self):
        """
        Test that Vietnamese text contains proper diacritical marks.

        Vietnamese uses many diacritical marks (accents). This test verifies
        that common Vietnamese characters with diacritics are present in
        the translations.
        """
        ui_text = load_ui_text()

        # Vietnamese diacritical characters that should appear in proper translations
        # Common diacritical marks: a with accent, e with accent, o with accent, etc.
        vietnamese_diacritical_chars = set("aaooeeuuiAOEUIdaDAaAoOeEuUdDaAoOeE")

        # Check page_title has Vietnamese characters
        page_title_vn = ui_text["page_title"]["vietnamese"]
        # Check for any non-ASCII characters (Vietnamese diacritics)
        has_non_ascii = any(ord(c) > 127 for c in page_title_vn)
        assert has_non_ascii, (
            f"Vietnamese page_title should contain diacritical marks, got: '{page_title_vn}'"
        )

        # Check task_instruction for Vietnamese content
        task_instruction_vn = ui_text["task_instruction"]["vietnamese"]
        has_non_ascii = any(ord(c) > 127 for c in task_instruction_vn)
        assert has_non_ascii, (
            f"Vietnamese task_instruction should contain diacritical marks"
        )

    def test_language_enum_integration_with_ui_text_lookup(self):
        """
        Test that Language enum integration works with UI text lookup.

        This verifies the backend ui_text module correctly integrates
        with the Language enum from color_labels.py.
        """
        from backend.app.constants.ui_text import get_ui_text, UI_TEXT
        from backend.app.constants.color_labels import Language

        # Test basic lookup with each language
        for lang in Language:
            result = get_ui_text("page_title", lang)
            assert isinstance(result, str), (
                f"get_ui_text should return string for {lang}"
            )
            assert len(result) > 0, (
                f"get_ui_text result should not be empty for {lang}"
            )

        # Test that UI_TEXT was loaded at module import time
        assert isinstance(UI_TEXT, dict), (
            "UI_TEXT should be a dictionary loaded at import time"
        )
        assert len(UI_TEXT) > 0, (
            "UI_TEXT should contain entries"
        )

        # Test specific lookup
        english_title = get_ui_text("page_title", Language.ENGLISH)
        assert "ColorFocus" in english_title, (
            f"English page_title should contain 'ColorFocus', got: '{english_title}'"
        )
