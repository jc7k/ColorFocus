"""
Tests for header donation link implementation.

These tests verify that the donation link in the header section
is correctly implemented with proper attributes, styling, and localization.

This test file covers Task Group 2: Header Donation Link Implementation.
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


class TestHeaderDonationLink:
    """
    Verify header donation link is correctly implemented in puzzle.html.

    These tests ensure the donation link has proper href, security attributes,
    and localization support.
    """

    def test_donation_link_has_correct_href(self):
        """
        Test that the donation link element exists with the correct href.

        The link should point to the Buy Me A Coffee page.
        """
        html_content = load_puzzle_html()
        expected_href = "https://buymeacoffee.com/xwje4mbv3l"

        assert expected_href in html_content, (
            f"Donation link should have href='{expected_href}'"
        )
        # Verify it's in an anchor tag
        assert f'href="{expected_href}"' in html_content, (
            "href should be properly quoted in an anchor element"
        )

    def test_donation_link_opens_in_new_tab(self):
        """
        Test that the donation link has target="_blank" attribute.

        The link should open in a new tab to avoid disrupting the puzzle.
        """
        html_content = load_puzzle_html()

        # Check for target="_blank" attribute
        assert 'target="_blank"' in html_content, (
            "Donation link should have target='_blank' to open in new tab"
        )

    def test_donation_link_has_security_attributes(self):
        """
        Test that the donation link has rel="noopener noreferrer" for security.

        This prevents the new page from accessing the window.opener property
        and protects against tabnabbing attacks.
        """
        html_content = load_puzzle_html()

        # Check for security attributes
        assert 'rel="noopener noreferrer"' in html_content, (
            "Donation link should have rel='noopener noreferrer' for security"
        )

    def test_donation_link_text_is_localized(self):
        """
        Test that the donation link has data-i18n attribute for localization.

        The link text should update when the language is changed,
        using the existing localization system.
        """
        html_content = load_puzzle_html()
        ui_text = load_ui_text()

        # Check for data-i18n attribute referencing support_link_text
        assert 'data-i18n="support_link_text"' in html_content, (
            "Donation link should have data-i18n='support_link_text' attribute"
        )

        # Verify the support_link_text key exists in ui_text.json
        assert "support_link_text" in ui_text, (
            "support_link_text key should exist in ui_text.json"
        )

        # Verify all 4 languages have translations (zh-TW replaces chinese)
        expected_languages = ["zh-TW", "english", "spanish", "vietnamese"]
        for lang in expected_languages:
            assert lang in ui_text["support_link_text"], (
                f"support_link_text should have '{lang}' translation"
            )

        # Check that updateAllUIText handles the donation link
        assert "support_link_text" in html_content, (
            "updateAllUIText should reference support_link_text key"
        )
