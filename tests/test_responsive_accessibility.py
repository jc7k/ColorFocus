"""
Tests for responsive design and accessibility implementation.

These tests verify that the donation feature elements are properly
responsive across mobile breakpoints and meet accessibility standards.

This test file covers Task Group 4: Responsive Design and Accessibility.
"""

import re
from conftest import load_puzzle_html, load_puzzle_css


def find_media_query_content(css: str, max_width: int) -> str:
    """
    Find all CSS rules within a specific media query block using bracket counting.

    Args:
        css: The full CSS content
        max_width: The max-width value to search for (e.g., 480 or 375)

    Returns:
        The CSS content within the media query block
    """
    # Find the start of the media query
    pattern = rf"@media\s*\(\s*max-width:\s*{max_width}px\s*\)"
    match = re.search(pattern, css)
    if not match:
        return ""

    # Find the opening brace after the media query
    start_idx = match.end()
    while start_idx < len(css) and css[start_idx] != "{":
        start_idx += 1

    if start_idx >= len(css):
        return ""

    # Count braces to find the matching closing brace
    brace_count = 0
    content_start = start_idx + 1
    idx = start_idx

    while idx < len(css):
        if css[idx] == "{":
            brace_count += 1
        elif css[idx] == "}":
            brace_count -= 1
            if brace_count == 0:
                return css[content_start:idx]
        idx += 1

    return ""


class TestResponsiveDesign:
    """
    Verify responsive design implementation for donation feature elements.

    These tests ensure the header link and QR code section scale appropriately
    across mobile breakpoints (480px and 375px).
    """

    def test_header_link_has_minimum_touch_target_on_mobile(self):
        """
        Test that the header donation link meets 44x44px minimum touch target at 480px.

        Per WCAG 2.1 guidelines, touch targets should be at least 44x44 CSS pixels
        to ensure usability on mobile devices.
        """
        css_content = load_puzzle_css()
        mobile_css = find_media_query_content(css_content, 480)

        # Verify donation-link has min-height in 480px media query
        assert ".donation-link" in mobile_css, (
            "donation-link styles should be defined in 480px media query"
        )

        # Check for min-height: 44px or CSS custom property equivalent
        # The implementation may use literal 44px or var(--btn-min-height) which resolves to 44px
        has_min_height = (
            "min-height: 44px" in mobile_css or "min-height:44px" in mobile_css or
            "min-height: var(--btn-min-height)" in mobile_css
        )
        assert has_min_height, (
            "donation-link should have min-height (44px or var(--btn-min-height)) at 480px breakpoint "
            "to meet minimum touch target requirements"
        )

        # Also verify flex alignment for vertical centering (in base CSS)
        # The base .donation-link uses display: inline-flex for alignment
        has_flex_display = (
            "display: inline-flex" in css_content or "display:inline-flex" in css_content or
            "display: flex" in css_content or "display:flex" in css_content
        )
        assert has_flex_display, (
            "donation-link should use display: flex/inline-flex for proper touch target alignment"
        )

    def test_qr_code_scales_at_480px_breakpoint(self):
        """
        Test that the QR code scales to 120px at 480px breakpoint.

        The QR code should be smaller on mobile but still scannable (120px).
        """
        css_content = load_puzzle_css()
        mobile_css = find_media_query_content(css_content, 480)

        # Verify donation-qr has width: 120px in 480px media query
        assert ".donation-qr" in mobile_css, (
            "donation-qr styles should be defined in 480px media query"
        )

        assert "width: 120px" in mobile_css or "width:120px" in mobile_css, (
            "donation-qr should have width: 120px at 480px breakpoint"
        )

    def test_qr_code_scales_at_375px_breakpoint(self):
        """
        Test that the QR code scales to 100px at 375px breakpoint.

        On extra small devices, the QR code should be 100px to fit smaller screens
        while remaining scannable.
        """
        css_content = load_puzzle_css()
        small_mobile_css = find_media_query_content(css_content, 375)

        # Verify donation-qr has width: 100px in 375px media query
        assert ".donation-qr" in small_mobile_css, (
            "donation-qr styles should be defined in 375px media query"
        )

        assert "width: 100px" in small_mobile_css or "width:100px" in small_mobile_css, (
            "donation-qr should have width: 100px at 375px breakpoint"
        )


class TestAccessibility:
    """
    Verify accessibility attributes for donation feature elements.

    These tests ensure proper semantic HTML, alt text, and keyboard navigation
    support for screen readers and assistive technologies.
    """

    def test_qr_code_has_descriptive_alt_text(self):
        """
        Test that the QR code image has descriptive alt text.

        The alt text should explain the purpose of the QR code so screen reader
        users understand what scanning it will do.
        """
        html_content = load_puzzle_html()

        # Verify alt text includes key information about Buy Me A Coffee
        # The alt attribute may appear before or after the class attribute
        assert 'alt="QR code to support ColorFocus via Buy Me A Coffee"' in html_content, (
            "QR code should have complete descriptive alt text"
        )

        # Verify the image has both the donation-qr class and descriptive alt
        assert 'class="donation-qr"' in html_content, (
            "QR code image should have class='donation-qr'"
        )

    def test_header_link_has_proper_semantic_attributes(self):
        """
        Test that the header donation link has proper semantic HTML structure.

        The link should use an <a> tag with:
        - Valid href attribute
        - target="_blank" for new tab
        - rel="noopener noreferrer" for security
        - Meaningful text content (via localization)
        """
        html_content = load_puzzle_html()

        # Check for anchor element with all required attributes
        expected_href = "https://buymeacoffee.com/xwje4mbv3l"

        # Verify href attribute
        assert f'href="{expected_href}"' in html_content, (
            f"Donation link should have href='{expected_href}'"
        )

        # Verify target="_blank"
        assert 'target="_blank"' in html_content, (
            "Donation link should have target='_blank'"
        )

        # Verify security attributes
        assert 'rel="noopener noreferrer"' in html_content, (
            "Donation link should have rel='noopener noreferrer' for security"
        )

        # Verify localization attribute
        assert 'data-i18n="support_link_text"' in html_content, (
            "Donation link should have data-i18n attribute for localization"
        )

    def test_header_link_has_visible_focus_state(self):
        """
        Test that the header donation link has visible focus styles for keyboard navigation.

        Users navigating with keyboard should see a clear visual indicator
        when the donation link is focused. This can be via outline or box-shadow.
        """
        css_content = load_puzzle_css()

        # Check for .donation-link:focus styles
        focus_pattern = r"\.donation-link:focus\s*\{[^}]+\}"
        focus_match = re.search(focus_pattern, css_content, re.DOTALL)
        assert focus_match, (
            "donation-link should have :focus styles defined"
        )

        # Verify there's a visible focus indicator (outline or box-shadow)
        # Apple-esque design may use box-shadow instead of outline for softer appearance
        focus_styles = re.search(r"\.donation-link:focus\s*\{([^}]*)\}", css_content)
        if focus_styles:
            focus_content = focus_styles.group(1)
            # Accept either visible outline OR box-shadow as valid focus indicator
            has_visible_outline = "outline:" in focus_content and "outline: none" not in focus_content.lower()
            has_box_shadow = "box-shadow:" in focus_content
            assert has_visible_outline or has_box_shadow, (
                "donation-link:focus should have visible focus indicator (outline or box-shadow)"
            )
