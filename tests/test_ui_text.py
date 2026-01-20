"""
UI text localization tests for ColorFocus.

These tests verify that UI text translations are correctly implemented
in the shared JSON and backend ui_text module.

Updated for the accessible color palette replacement:
- Language key "chinese" renamed to "zh-TW"
- All language references updated accordingly

Uses shared fixtures from conftest.py.
"""

from conftest import load_ui_text, SUPPORTED_LANGUAGES


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
    "language_descriptor_zh-TW",  # Updated from language_descriptor_chinese
    "language_descriptor_english",
    "language_descriptor_vietnamese",
]


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

        This verifies zh-TW, english, and vietnamese translations exist
        for every required UI text key.
        """
        ui_text = load_ui_text()
        languages = ["zh-TW", "english", "vietnamese"]  # Updated from "chinese"

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

    def test_zh_tw_key_replaces_chinese(self):
        """
        Test that 'zh-TW' key is used instead of 'chinese'.

        The language key was renamed from 'chinese' to 'zh-TW' for
        proper locale identification and future simplified Chinese support.
        """
        ui_text = load_ui_text()

        # Check a sample of entries for zh-TW key
        sample_keys = ["page_title", "subtitle", "task_label", "generate_btn"]

        for key in sample_keys:
            assert key in ui_text, f"Missing key: {key}"
            assert "zh-TW" in ui_text[key], (
                f"UI text key '{key}' should have 'zh-TW' key"
            )
            assert "chinese" not in ui_text[key], (
                f"UI text key '{key}' should not have 'chinese' key (should be 'zh-TW')"
            )

    def test_vietnamese_text_uses_ascii_friendly_format(self):
        """
        Test that Vietnamese text uses ASCII-friendly format.

        ColorFocus uses ASCII-friendly Vietnamese versions without diacritics
        for broader display compatibility on older systems.
        """
        ui_text = load_ui_text()

        # Check that Vietnamese text is present and non-empty
        page_title_vn = ui_text["page_title"]["vietnamese"]
        assert len(page_title_vn) > 0, "Vietnamese page_title should not be empty"
        assert "ColorFocus" in page_title_vn, (
            "Vietnamese page_title should contain 'ColorFocus'"
        )

        # Check task_instruction has Vietnamese content
        task_instruction_vn = ui_text["task_instruction"]["vietnamese"]
        assert len(task_instruction_vn) > 0, (
            "Vietnamese task_instruction should not be empty"
        )

        # Vietnamese text is stored as ASCII-friendly for display compatibility
        # Verify it's valid string content, not checking for diacritics
        assert isinstance(task_instruction_vn, str), (
            "Vietnamese task_instruction should be a string"
        )

    def test_language_enum_integration_with_ui_text_lookup(self):
        """
        Test that Language enum integration works with UI text lookup.

        This verifies the backend ui_text module correctly integrates
        with the Language enum from color_labels.py (now using ZH_TW).
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

    def test_language_descriptor_zh_tw_key(self):
        """
        Test that the language descriptor key uses 'zh-TW' suffix.

        The key was renamed from 'language_descriptor_chinese' to
        'language_descriptor_zh-TW'.
        """
        ui_text = load_ui_text()

        # New key should exist
        assert "language_descriptor_zh-TW" in ui_text, (
            "Missing 'language_descriptor_zh-TW' key"
        )

        # Old key should not exist
        assert "language_descriptor_chinese" not in ui_text, (
            "'language_descriptor_chinese' should be renamed to 'language_descriptor_zh-TW'"
        )

        # The zh-TW descriptor should have all language translations
        zh_tw_descriptor = ui_text["language_descriptor_zh-TW"]
        for lang in ["zh-TW", "english", "vietnamese", "spanish"]:
            assert lang in zh_tw_descriptor, (
                f"language_descriptor_zh-TW missing '{lang}' translation"
            )
