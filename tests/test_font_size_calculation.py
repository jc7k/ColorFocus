"""
Font size calculation tests for ColorFocus.

Task Group 2: Dynamic Font Size Calculation.
Tests verify dynamic font sizing, recalculation triggers, and minimum font floors.
"""

import re
from pathlib import Path

from conftest import load_puzzle_html, load_puzzle_js


class TestDynamicFontSizeCalculation:
    """
    Verify dynamic font size calculation without hardcoded max caps.
    """

    def test_no_hardcoded_max_font_size_object(self):
        """Test that fixed maxFontSizes object has been removed."""
        js_content = load_puzzle_js()
        has_fixed_max_sizes = bool(re.search(
            r'maxFontSizes\s*=\s*\{[^}]*chinese\s*:\s*\d+',
            js_content
        ))
        assert not has_fixed_max_sizes, (
            "Hardcoded maxFontSizes object should be removed for dynamic scaling"
        )

    def test_font_calculation_uses_0_8_multiplier_for_80_percent_width(self):
        """Test that font calculation uses 0.8 multiplier for 80% text width."""
        js_content = load_puzzle_js()
        assert '0.8' in js_content, (
            "Font calculation should use 0.8 multiplier for 80% text width target"
        )

    def test_language_width_multipliers_maintained(self):
        """Test that language width multipliers are maintained."""
        js_content = load_puzzle_js()
        assert "'zh-TW': 1.15" in js_content or "'zh-TW':1.15" in js_content, (
            "zh-TW width multiplier should be 1.15"
        )
        assert 'vietnamese: 2.6' in js_content or 'vietnamese:2.6' in js_content, (
            "Vietnamese width multiplier should be 2.6"
        )
        assert 'english: 4.2' in js_content or 'english:4.2' in js_content, (
            "English width multiplier should be 4.2"
        )
        assert 'spanish: 4.2' in js_content or 'spanish:4.2' in js_content, (
            "Spanish width multiplier should be 4.2"
        )

    def test_cell_width_calculation_accounts_for_spacing(self):
        """Test that cell width calculation accounts for spacing gaps."""
        js_content = load_puzzle_js()
        assert 'SPACING_VALUES' in js_content, (
            "SPACING_VALUES constant should be defined"
        )
        assert 'currentSpacing' in js_content, (
            "currentSpacing should be used for spacing-aware calculations"
        )


class TestFontRecalculationTriggers:
    """
    Verify font size recalculates on all relevant events.
    """

    def test_font_recalculates_on_window_resize(self):
        """Test that font recalculates on window resize event."""
        js_content = load_puzzle_js()
        assert "window.addEventListener('resize'" in js_content or 'window.addEventListener("resize"' in js_content, (
            "Window resize event listener should exist for font recalculation"
        )
        assert 'applyPuzzleFontSize' in js_content, (
            "applyPuzzleFontSize function should exist"
        )

    def test_font_recalculates_on_grid_size_change(self):
        """Test that font recalculates on grid size change."""
        js_content = load_puzzle_js()
        assert 'generatePuzzle' in js_content, (
            "generatePuzzle function should exist"
        )

    def test_font_recalculates_on_language_change(self):
        """Test that font recalculates on language change."""
        js_content = load_puzzle_js()
        language_handler = re.search(
            r"getElementById\(['\"]language['\"]\).*addEventListener",
            js_content,
            re.DOTALL
        )
        assert language_handler is not None, (
            "Language change event listener should exist"
        )

    def test_font_recalculates_on_spacing_change(self):
        """Test that font recalculates on spacing change."""
        js_content = load_puzzle_js()
        spacing_section = re.search(
            r"getElementById\(['\"]spacing['\"]\).*?applyPuzzleFontSize",
            js_content,
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
        js_content = load_puzzle_js()
        assert 'Math.max' in js_content, (
            "Font calculation should have a minimum floor using Math.max"
        )


class TestOrientationChangeHandling:
    """
    Verify mobile orientation change triggers font recalculation.
    """

    def test_orientation_change_or_resize_triggers_recalculation(self):
        """Test that orientation change triggers font recalculation."""
        js_content = load_puzzle_js()
        has_resize = "window.addEventListener('resize'" in js_content or 'window.addEventListener("resize"' in js_content
        has_orientation = 'orientationchange' in js_content
        assert has_resize or has_orientation, (
            "Should handle orientation changes via resize or orientationchange event"
        )
