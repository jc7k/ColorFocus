"""
Spanish language label and backend tests for ColorFocus.

These tests verify Spanish language support in:
- shared/color_labels.json (color translations)
- shared/ui_text.json (UI text translations)
- Backend Language enum and get_color_label() function
"""

import json
from pathlib import Path


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


def load_color_labels() -> dict:
    """Load the color_labels.json file."""
    with open(COLOR_LABELS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestSpanishColorLabels:
    """Verify Spanish color labels in shared/color_labels.json."""

    def test_color_labels_json_contains_spanish_key_for_all_colors(self):
        """Test that color_labels.json contains spanish key for all 8 colors."""
        color_labels = load_color_labels()

        for token in EXPECTED_COLOR_TOKENS:
            assert token in color_labels, f"Missing color token: {token}"
            assert "spanish" in color_labels[token], (
                f"Color {token} missing 'spanish' key"
            )

    def test_spanish_color_labels_use_expected_values(self):
        """Test that Spanish color labels use expected values."""
        color_labels = load_color_labels()

        for token, expected_label in EXPECTED_SPANISH_LABELS.items():
            actual_label = color_labels[token]["spanish"]
            assert actual_label == expected_label, (
                f"Spanish label for {token} should be '{expected_label}', got '{actual_label}'"
            )


class TestSpanishUIText:
    """Verify Spanish UI text translations in shared/ui_text.json."""

    def test_ui_text_json_contains_spanish_key_for_all_entries(self):
        """Test that ui_text.json contains spanish key for all UI text entries."""
        ui_text = load_ui_text()

        assert len(ui_text) >= 40, (
            f"Expected at least 40 UI text entries, got {len(ui_text)}"
        )

        for key, translations in ui_text.items():
            assert "spanish" in translations, (
                f"UI text entry '{key}' missing 'spanish' key"
            )
            assert translations["spanish"].strip() != "", (
                f"UI text entry '{key}' has empty Spanish translation"
            )

    def test_language_descriptor_spanish_entry_exists(self):
        """Test that language_descriptor_spanish entry exists with all four languages."""
        ui_text = load_ui_text()

        assert "language_descriptor_spanish" in ui_text, (
            "UI text should contain 'language_descriptor_spanish' entry"
        )

        descriptor = ui_text["language_descriptor_spanish"]

        expected_languages = ["zh-TW", "english", "vietnamese", "spanish"]
        for lang in expected_languages:
            assert lang in descriptor, (
                f"language_descriptor_spanish missing '{lang}' translation"
            )


class TestBackendSpanishLanguageEnum:
    """Verify Spanish language support in backend Language enum."""

    def test_language_enum_includes_spanish_value(self):
        """Test that Language enum includes SPANISH value."""
        from backend.app.constants.color_labels import Language

        assert hasattr(Language, "SPANISH"), (
            "Language enum should have SPANISH member"
        )
        assert Language.SPANISH is not None

    def test_language_spanish_value_equals_spanish_string(self):
        """Test that Language.SPANISH.value equals 'spanish'."""
        from backend.app.constants.color_labels import Language

        assert Language.SPANISH.value == "spanish", (
            f"Language.SPANISH.value should be 'spanish', got '{Language.SPANISH.value}'"
        )

    def test_get_color_label_works_with_spanish_for_all_colors(self):
        """Test that get_color_label() works with Language.SPANISH for all colors."""
        from backend.app.constants.color_labels import Language, get_color_label
        from backend.app.constants.colors import ColorToken

        for token in ColorToken:
            label = get_color_label(token, Language.SPANISH)
            expected_label = EXPECTED_SPANISH_LABELS[token.value]
            assert label == expected_label, (
                f"Spanish label for {token.value} should be '{expected_label}', got '{label}'"
            )
