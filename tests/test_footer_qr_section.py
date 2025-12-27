"""
Tests for footer QR code section implementation.

These tests verify that the donation QR code section in the footer
is correctly implemented with proper structure, styling, and localization.

This test file covers Task Group 3: Footer QR Code Section Implementation.
"""

import json
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


class TestFooterQRSection:
    """
    Verify footer QR code section is correctly implemented in puzzle.html.

    These tests ensure the QR code image, caption label, and section structure
    are properly implemented with localization support.
    """

    def test_qr_code_image_exists_with_correct_src(self):
        """
        Test that the QR code image element exists with the correct src attribute.

        The image should use a relative path to bmc_qr.png in the frontend directory.
        """
        html_content = load_puzzle_html()

        # Check for img element with bmc_qr.png src (absolute path for Vercel deployment)
        assert 'src="/frontend/bmc_qr.png"' in html_content, (
            "QR code image should have src='/frontend/bmc_qr.png' (absolute path for Vercel)"
        )

        # Verify the image has the donation-qr class
        assert 'class="donation-qr"' in html_content, (
            "QR code image should have class='donation-qr'"
        )

        # Verify the actual image file exists
        assert QR_IMAGE_PATH.exists(), (
            f"QR code image should exist at {QR_IMAGE_PATH}"
        )

    def test_qr_code_has_descriptive_alt_text(self):
        """
        Test that the QR code image has a descriptive alt attribute.

        The alt text should explain the purpose of the QR code for accessibility.
        """
        html_content = load_puzzle_html()

        # Check for descriptive alt text
        assert 'alt="QR code to support ColorFocus via Buy Me A Coffee"' in html_content, (
            "QR code image should have descriptive alt text for accessibility"
        )

    def test_caption_label_updates_on_language_change(self):
        """
        Test that the caption label has data-i18n attribute for localization.

        The caption should update when the language is changed,
        using the existing localization system.
        """
        html_content = load_puzzle_html()
        ui_text = load_ui_text()

        # Check for data-i18n attribute referencing qr_code_label
        assert 'data-i18n="qr_code_label"' in html_content, (
            "Caption label should have data-i18n='qr_code_label' attribute"
        )

        # Verify the qr_code_label key exists in ui_text.json
        assert "qr_code_label" in ui_text, (
            "qr_code_label key should exist in ui_text.json"
        )

        # Verify all 4 languages have translations (zh-TW replaces chinese)
        expected_languages = ["zh-TW", "english", "spanish", "vietnamese"]
        for lang in expected_languages:
            assert lang in ui_text["qr_code_label"], (
                f"qr_code_label should have '{lang}' translation"
            )

        # Check that updateAllUIText handles the donation label
        assert "qr_code_label" in html_content, (
            "updateAllUIText should reference qr_code_label key"
        )

    def test_section_renders_below_answer_key_section(self):
        """
        Test that the donation section appears below the Answer Key section.

        The donation section should be positioned after .answer-key-section
        in the HTML structure.
        """
        html_content = load_puzzle_html()

        # Find positions of both sections
        answer_key_pos = html_content.find('class="answer-key-section"')
        donation_section_pos = html_content.find('class="donation-section"')

        assert answer_key_pos != -1, (
            "Answer Key section should exist in puzzle.html"
        )
        assert donation_section_pos != -1, (
            "Donation section should exist in puzzle.html"
        )
        assert answer_key_pos < donation_section_pos, (
            "Donation section should appear after Answer Key section in HTML"
        )

        # Verify the donation section has proper container structure
        assert '<div class="donation-section">' in html_content, (
            "Donation section should use a div with class='donation-section'"
        )
