"""
Tests for donation feature integration.

These tests verify that the donation feature components work together
correctly, focusing on integration between header link, footer QR section,
and the localization system.

This test file covers Task Group 5: Test Review and Final Verification.
"""

import json
import re
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"
QR_IMAGE_PATH = PROJECT_ROOT / "frontend" / "bmc_qr.png"


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_puzzle_html() -> str:
    """Load the puzzle.html file content."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestDonationIntegration:
    """
    Verify donation feature integration between components.

    These tests ensure the header donation link, footer QR section, and
    localization system work together correctly.
    """

    def test_both_donation_elements_have_localization_attributes(self):
        """
        Test that both donation elements (header link and footer label) have
        data-i18n attributes for localization integration.

        This ensures language switching will update both elements simultaneously.
        """
        html_content = load_puzzle_html()

        # Verify header link has data-i18n attribute
        assert 'data-i18n="support_link_text"' in html_content, (
            "Header donation link should have data-i18n attribute"
        )

        # Verify footer label has data-i18n attribute
        assert 'data-i18n="qr_code_label"' in html_content, (
            "Footer donation label should have data-i18n attribute"
        )

        # Verify both elements have unique IDs for JavaScript targeting
        assert 'id="donationLink"' in html_content, (
            "Header donation link should have id='donationLink' for JS updates"
        )
        assert 'id="donationLabel"' in html_content, (
            "Footer donation label should have id='donationLabel' for JS updates"
        )

    def test_update_all_ui_text_handles_both_donation_elements(self):
        """
        Test that the updateAllUIText JavaScript function updates both
        donation-related elements when language changes.

        This verifies the integration between the localization system and
        the donation feature UI elements.
        """
        html_content = load_puzzle_html()

        # Extract JavaScript from the script tag
        script_match = re.search(
            r'<script type="module">(.*?)</script>',
            html_content,
            re.DOTALL
        )
        assert script_match, "Should find module script in puzzle.html"
        js_content = script_match.group(1)

        # Verify updateAllUIText function updates donationLink
        assert "donationLink" in js_content, (
            "JavaScript should reference donationLink element"
        )
        assert "support_link_text" in js_content, (
            "JavaScript should use support_link_text localization key"
        )

        # Verify updateAllUIText function updates donationLabel
        assert "donationLabel" in js_content, (
            "JavaScript should reference donationLabel element"
        )
        assert "qr_code_label" in js_content, (
            "JavaScript should use qr_code_label localization key"
        )

    def test_all_supported_languages_have_donation_translations(self):
        """
        Test that all 4 supported languages have complete translations
        for both donation feature text keys.

        This ensures the feature works correctly in Chinese, English,
        Spanish, and Vietnamese.
        """
        ui_text = load_ui_text()
        expected_languages = ["chinese", "english", "spanish", "vietnamese"]
        donation_keys = ["support_link_text", "qr_code_label"]

        for key in donation_keys:
            assert key in ui_text, f"ui_text.json should contain '{key}'"

            for lang in expected_languages:
                assert lang in ui_text[key], (
                    f"'{key}' should have '{lang}' translation"
                )
                # Verify translation is not empty
                assert ui_text[key][lang].strip(), (
                    f"'{key}' translation for '{lang}' should not be empty"
                )

    def test_qr_image_asset_exists_and_accessible(self):
        """
        Test that the QR code image file exists in the frontend directory
        and is accessible for the puzzle.html page.

        This verifies the asset relocation from project root was successful.
        """
        # Verify QR image exists
        assert QR_IMAGE_PATH.exists(), (
            f"QR code image should exist at {QR_IMAGE_PATH}"
        )

        # Verify file is readable and has content
        assert QR_IMAGE_PATH.stat().st_size > 0, (
            "QR code image file should not be empty"
        )

        # Verify HTML references the correct relative path
        html_content = load_puzzle_html()
        assert 'src="bmc_qr.png"' in html_content, (
            "puzzle.html should reference bmc_qr.png with relative path"
        )
