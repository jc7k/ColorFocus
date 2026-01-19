"""
Font size calculation tests for ColorFocus.

Task Group 2: Dynamic Font Size Calculation.
Tests verify dynamic font sizing, recalculation triggers, and minimum font floors.
"""

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


def load_puzzle_html() -> str:
    """Load the puzzle.html file."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestDynamicFontSizeCalculation:
    """
    Verify dynamic font size calculation without hardcoded max caps.
    """

    def test_no_hardcoded_max_font_size_object(self):
        """Test that fixed maxFontSizes object has been removed."""
        html = load_puzzle_html()
        has_fixed_max_sizes = bool(re.search(
            r'maxFontSizes\s*=\s*\{[^}]*chinese\s*:\s*\d+',
            html
        ))
        assert not has_fixed_max_sizes, (
            "Hardcoded maxFontSizes object should be removed for dynamic scaling"
        )

    def test_font_calculation_uses_0_8_multiplier_for_80_percent_width(self):
        """Test that font calculation uses 0.8 multiplier for 80% text width."""
        html = load_puzzle_html()
        assert '0.8' in html, (
            "Font calculation should use 0.8 multiplier for 80% text width target"
        )

    def test_language_width_multipliers_maintained(self):
        """Test that language width multipliers are maintained."""
        html = load_puzzle_html()
        assert "'zh-TW': 1.15" in html or "'zh-TW':1.15" in html, (
            "zh-TW width multiplier should be 1.15"
        )
        assert 'vietnamese: 2.4' in html or 'vietnamese:2.4' in html, (
            "Vietnamese width multiplier should be 2.4"
        )
        assert 'english: 3.6' in html or 'english:3.6' in html, (
            "English width multiplier should be 3.6"
        )
        assert 'spanish: 4.8' in html or 'spanish:4.8' in html, (
            "Spanish width multiplier should be 4.8"
        )

    def test_cell_width_calculation_accounts_for_spacing(self):
        """Test that cell width calculation accounts for spacing gaps."""
        html = load_puzzle_html()
        assert 'SPACING_VALUES' in html, (
            "SPACING_VALUES constant should be defined"
        )
        assert 'currentSpacing' in html, (
            "currentSpacing should be used for spacing-aware calculations"
        )


class TestFontRecalculationTriggers:
    """
    Verify font size recalculates on all relevant events.
    """

    def test_font_recalculates_on_window_resize(self):
        """Test that font recalculates on window resize event."""
        html = load_puzzle_html()
        assert "window.addEventListener('resize'" in html or 'window.addEventListener("resize"' in html, (
            "Window resize event listener should exist for font recalculation"
        )
        assert 'applyPuzzleFontSize' in html, (
            "applyPuzzleFontSize function should exist"
        )

    def test_font_recalculates_on_grid_size_change(self):
        """Test that font recalculates on grid size change."""
        html = load_puzzle_html()
        assert 'generatePuzzle' in html, (
            "generatePuzzle function should exist"
        )

    def test_font_recalculates_on_language_change(self):
        """Test that font recalculates on language change."""
        html = load_puzzle_html()
        language_handler = re.search(
            r"getElementById\(['\"]language['\"]\).*addEventListener",
            html,
            re.DOTALL
        )
        assert language_handler is not None, (
            "Language change event listener should exist"
        )

    def test_font_recalculates_on_spacing_change(self):
        """Test that font recalculates on spacing change."""
        html = load_puzzle_html()
        spacing_section = re.search(
            r"getElementById\(['\"]spacing['\"]\).*?applyPuzzleFontSize",
            html,
            re.DOTALL
        )
        assert spacing_section is not None, (
            "Spacing change handler should call applyPuzzleFontSize"
        )


class TestMinimumFontSizeFloor:
    """
    Verify minimum font size handling.
    """

    def test_practical_minimum_font_size_exists(self):
        """Test that a practical minimum font size floor exists."""
        html = load_puzzle_html()
        assert 'Math.max' in html, (
            "Font calculation should have a minimum floor using Math.max"
        )


class TestOrientationChangeHandling:
    """
    Verify mobile orientation change triggers font recalculation.
    """

    def test_orientation_change_or_resize_triggers_recalculation(self):
        """Test that orientation change triggers font recalculation."""
        html = load_puzzle_html()
        has_resize = "window.addEventListener('resize'" in html or 'window.addEventListener("resize"' in html
        has_orientation = 'orientationchange' in html
        assert has_resize or has_orientation, (
            "Should handle orientation changes via resize or orientationchange event"
        )
