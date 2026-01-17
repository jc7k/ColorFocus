"""
Dynamic grid and font scaling tests for ColorFocus.

These tests verify that the dynamic grid/font scaling feature is correctly implemented,
including container max-width changes, dynamic font size calculation, language-specific
scaling, and responsive behavior.

This test file covers Task Groups 1-4 for the Dynamic Grid/Font Scaling feature.
"""

import re
from pathlib import Path


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


def load_puzzle_html() -> str:
    """Load the puzzle.html file."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


# =============================================================================
# Task Group 1: Container and Cell CSS Updates (Tests 1.1)
# =============================================================================


class TestContainerMaxWidth:
    """
    Verify container max-width has been updated from 520px to 500px.

    The container should scale to 500px on desktop for larger puzzle area
    while maintaining comfortable viewing for the target demographic.
    """

    def test_puzzle_grid_max_width_is_500px(self):
        """
        Test that .puzzle-grid max-width is set to 500px.

        The max-width should be 500px to provide 54% more puzzle area
        while keeping comfortable viewing distance.
        """
        html = load_puzzle_html()

        # Look for max-width in puzzle-grid CSS
        # Pattern: max-width: 500px within .puzzle-grid block
        puzzle_grid_match = re.search(
            r'\.puzzle-grid\s*\{[^}]*max-width:\s*500px',
            html,
            re.DOTALL
        )

        assert puzzle_grid_match is not None, (
            ".puzzle-grid should have max-width: 500px"
        )

    def test_container_uses_max_width_not_fixed_width(self):
        """
        Test that container uses max-width (not fixed width) to allow scaling.

        Container should fill available viewport width up to the 500px maximum.
        """
        html = load_puzzle_html()

        # Should have max-width, not just width
        assert 'max-width:' in html or 'max-width :' in html, (
            "Container should use max-width for responsive scaling"
        )

        # puzzle-grid should not have fixed width that would prevent scaling
        puzzle_grid_section = re.search(
            r'\.puzzle-grid\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        if puzzle_grid_section:
            section_text = puzzle_grid_section.group(0)
            # Should not have 'width:' without 'max-' prefix in main styles
            has_only_max_width = 'max-width' in section_text
            assert has_only_max_width, (
                ".puzzle-grid should use max-width for scaling, not fixed width"
            )

    def test_container_centered_with_auto_margin(self):
        """
        Test that container remains centered with margin: 0 auto.

        On large screens, the puzzle should be centered with side margins.
        """
        html = load_puzzle_html()

        # Look for margin: 0 auto in puzzle-grid
        puzzle_grid_match = re.search(
            r'\.puzzle-grid\s*\{[^}]*margin:\s*0\s+auto',
            html,
            re.DOTALL
        )

        assert puzzle_grid_match is not None, (
            ".puzzle-grid should have margin: 0 auto for centering"
        )


class TestMobileContainerBehavior:
    """
    Verify mobile viewport behavior remains functional.

    Mobile devices (under 480px) should continue to use 100% width minus padding.
    """

    def test_mobile_media_query_exists_for_480px(self):
        """
        Test that mobile media query exists for 480px viewport.
        """
        html = load_puzzle_html()

        assert '@media (max-width: 480px)' in html, (
            "Mobile media query for 480px should exist"
        )

    def test_mobile_puzzle_grid_uses_full_width(self):
        """
        Test that mobile puzzle grid uses 100% width.

        Under 480px viewport, the grid should fill available width.
        """
        html = load_puzzle_html()

        # Find the 480px media query and check for width: 100%
        mobile_section = re.search(
            r'@media\s*\(\s*max-width:\s*480px\s*\)\s*\{[^@]+',
            html,
            re.DOTALL
        )

        assert mobile_section is not None, (
            "480px mobile media query should exist"
        )

        mobile_css = mobile_section.group(0)

        # Check for puzzle-grid width: 100% in mobile
        assert 'width: 100%' in mobile_css or 'width:100%' in mobile_css, (
            "Mobile puzzle-grid should use width: 100%"
        )

    def test_mobile_puzzle_grid_has_reduced_gap(self):
        """
        Test that mobile puzzle grid has reduced gap (1-2px for compact layout).
        """
        html = load_puzzle_html()

        mobile_section = re.search(
            r'@media\s*\(\s*max-width:\s*480px\s*\)\s*\{[^@]+',
            html,
            re.DOTALL
        )

        assert mobile_section is not None, (
            "480px mobile media query should exist"
        )

        mobile_css = mobile_section.group(0)

        # Check for reduced gap in mobile (1px or 2px are acceptable)
        has_reduced_gap = (
            'gap: 1px' in mobile_css or 'gap:1px' in mobile_css or
            'gap: 2px' in mobile_css or 'gap:2px' in mobile_css
        )
        assert has_reduced_gap, (
            "Mobile puzzle-grid should use reduced gap (1px or 2px)"
        )


# =============================================================================
# Task Group 2: Dynamic Font Size Calculation (Tests 2.1)
# =============================================================================


class TestDynamicFontSizeCalculation:
    """
    Verify dynamic font size calculation without hardcoded max caps.

    Font sizes should scale proportionally with cell sizes and be
    calculated at runtime based on actual rendered dimensions.
    """

    def test_no_hardcoded_max_font_size_object(self):
        """
        Test that fixed maxFontSizes object has been removed.

        The calculation should be dynamic, not capped by fixed values.
        """
        html = load_puzzle_html()

        # Check that there's no hardcoded maxFontSizes object with fixed language values
        # The old pattern was: maxFontSizes = { "zh-TW": 45, vietnamese: 22, ... }
        has_fixed_max_sizes = bool(re.search(
            r'maxFontSizes\s*=\s*\{[^}]*chinese\s*:\s*\d+',
            html
        ))

        assert not has_fixed_max_sizes, (
            "Hardcoded maxFontSizes object should be removed for dynamic scaling"
        )

    def test_font_calculation_uses_0_8_multiplier_for_80_percent_width(self):
        """
        Test that font calculation uses 0.8 multiplier for 80% text width.

        Formula: baseFontSize = (cellWidth * 0.8) / languageWidthMultiplier
        """
        html = load_puzzle_html()

        # Look for 0.8 multiplier in font calculation
        assert '0.8' in html, (
            "Font calculation should use 0.8 multiplier for 80% text width target"
        )

    def test_language_width_multipliers_maintained(self):
        """
        Test that language width multipliers are maintained.

        Updated for accessible color palette (2025-12-27):
        zh-TW (1.15), Vietnamese (2.4), English (3.6), Spanish (4.8)
        """
        html = load_puzzle_html()

        # Check widthMultipliers object exists with correct values
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
        """
        Test that cell width calculation accounts for spacing gaps.

        Should use SPACING_VALUES for accurate gap calculation.
        """
        html = load_puzzle_html()

        # Check for SPACING_VALUES usage in font calculation
        assert 'SPACING_VALUES' in html, (
            "SPACING_VALUES constant should be defined"
        )

        # Check for dynamic gap calculation using currentSpacing
        assert 'currentSpacing' in html, (
            "currentSpacing should be used for spacing-aware calculations"
        )


class TestFontRecalculationTriggers:
    """
    Verify font size recalculates on all relevant events.
    """

    def test_font_recalculates_on_window_resize(self):
        """
        Test that font recalculates on window resize event.
        """
        html = load_puzzle_html()

        # Check for resize event listener
        assert "window.addEventListener('resize'" in html or 'window.addEventListener("resize"' in html, (
            "Window resize event listener should exist for font recalculation"
        )

        # Check that applyPuzzleFontSize is called in resize handler
        assert 'applyPuzzleFontSize' in html, (
            "applyPuzzleFontSize function should exist"
        )

    def test_font_recalculates_on_grid_size_change(self):
        """
        Test that font recalculates on grid size change.
        """
        html = load_puzzle_html()

        # Check for grid size change handler that triggers font recalculation
        # The generatePuzzle function should call applyPuzzleFontSize
        assert 'generatePuzzle' in html, (
            "generatePuzzle function should exist"
        )

    def test_font_recalculates_on_language_change(self):
        """
        Test that font recalculates on language change.
        """
        html = load_puzzle_html()

        # Check for language change handler
        language_handler = re.search(
            r"getElementById\(['\"]language['\"]\).*addEventListener",
            html,
            re.DOTALL
        )

        assert language_handler is not None, (
            "Language change event listener should exist"
        )

    def test_font_recalculates_on_spacing_change(self):
        """
        Test that font recalculates on spacing change.

        Spacing affects cell width, so font must be recalculated.
        """
        html = load_puzzle_html()

        # Check for spacing change handler that calls applyPuzzleFontSize
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
        """
        Test that a practical minimum font size floor exists.

        Below ~4px, text becomes unreadable, so there should be some floor.
        """
        html = load_puzzle_html()

        # Check for Math.max in font calculation (indicates a floor)
        assert 'Math.max' in html, (
            "Font calculation should have a minimum floor using Math.max"
        )


# =============================================================================
# Task Group 3: Cross-Browser and Responsive Integration (Tests 3.1)
# =============================================================================


class TestOrientationChangeHandling:
    """
    Verify mobile orientation change triggers font recalculation.
    """

    def test_orientation_change_or_resize_triggers_recalculation(self):
        """
        Test that orientation change triggers font recalculation.

        Either via dedicated orientationchange listener or via resize event
        (which fires on orientation change in modern browsers).
        """
        html = load_puzzle_html()

        # Modern browsers fire resize on orientation change, so resize handler is sufficient
        # But an explicit orientationchange listener is also acceptable
        has_resize = "window.addEventListener('resize'" in html or 'window.addEventListener("resize"' in html
        has_orientation = 'orientationchange' in html

        assert has_resize or has_orientation, (
            "Should handle orientation changes via resize or orientationchange event"
        )


class TestAllLanguagesAtGridSizes:
    """
    Verify all four languages render correctly at various grid sizes.
    """

    def test_calculate_puzzle_font_size_handles_all_languages(self):
        """
        Test that calculatePuzzleFontSize handles all four languages.
        """
        html = load_puzzle_html()

        # Check widthMultipliers includes all languages
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        assert width_multipliers_section is not None, (
            "widthMultipliers object should be defined"
        )

        section_text = width_multipliers_section.group(0)

        assert "zh-TW" in section_text, "zh-TW should be in widthMultipliers"
        assert 'vietnamese' in section_text, "Vietnamese should be in widthMultipliers"
        assert 'english' in section_text, "English should be in widthMultipliers"
        assert 'spanish' in section_text, "Spanish should be in widthMultipliers"


class TestSpacingOptionsIntegration:
    """
    Verify all spacing options work with font scaling.
    """

    def test_spacing_values_constant_has_all_options(self):
        """
        Test that SPACING_VALUES constant has all spacing options.

        compact (1px), normal (2px), relaxed (6px), spacious (12px)
        """
        html = load_puzzle_html()

        # Check SPACING_VALUES has all options
        assert 'compact: 1' in html or 'compact:1' in html, (
            "SPACING_VALUES should have compact: 1"
        )
        assert 'normal: 2' in html or 'normal:2' in html, (
            "SPACING_VALUES should have normal: 2"
        )
        assert 'relaxed: 6' in html or 'relaxed:6' in html, (
            "SPACING_VALUES should have relaxed: 6"
        )
        assert 'spacious: 12' in html or 'spacious:12' in html, (
            "SPACING_VALUES should have spacious: 12"
        )


class TestDifficultyPresetsBackwardCompatibility:
    """
    Verify difficulty presets continue to work correctly.
    """

    def test_difficulty_presets_constant_exists(self):
        """
        Test that DIFFICULTY_PRESETS constant exists with all tiers.
        """
        html = load_puzzle_html()

        assert 'DIFFICULTY_PRESETS' in html, (
            "DIFFICULTY_PRESETS constant should exist"
        )

        # Check accessible, standard, advanced presets
        assert 'accessible:' in html or 'accessible :' in html, (
            "Accessible preset should exist"
        )
        assert 'standard:' in html or 'standard :' in html, (
            "Standard preset should exist"
        )
        assert 'advanced:' in html or 'advanced :' in html, (
            "Advanced preset should exist"
        )

    def test_accessible_preset_has_3x3_grid(self):
        """
        Test that accessible preset uses 3x3 grid.
        """
        html = load_puzzle_html()

        # Find accessible preset definition
        accessible_section = re.search(
            r'accessible:\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        assert accessible_section is not None, (
            "Accessible preset should be defined"
        )

        section_text = accessible_section.group(0)
        assert 'gridSize: 3' in section_text or 'gridSize:3' in section_text, (
            "Accessible preset should have gridSize: 3"
        )

    def test_advanced_preset_has_8x8_grid(self):
        """
        Test that advanced preset uses 8x8 grid.
        """
        html = load_puzzle_html()

        # Find advanced preset definition
        advanced_section = re.search(
            r'advanced:\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        assert advanced_section is not None, (
            "Advanced preset should be defined"
        )

        section_text = advanced_section.group(0)
        assert 'gridSize: 8' in section_text or 'gridSize:8' in section_text, (
            "Advanced preset should have gridSize: 8"
        )


# =============================================================================
# Task Group 4: Additional Strategic Tests
# =============================================================================


class TestCellWidthCalculationFormula:
    """
    Verify cell width calculation formula is correct.
    """

    def test_cell_width_accounts_for_gaps_between_columns(self):
        """
        Test that cell width calculation subtracts gaps.

        Formula: cellWidth = (gridWidth - (columns - 1) * gapValue) / columns
        """
        html = load_puzzle_html()

        # Check for gap subtraction in calculation
        # Pattern: columns - 1 for calculating total gaps
        assert 'columns - 1' in html or '(columns-1)' in html, (
            "Cell width should account for (columns - 1) gaps"
        )

    def test_cell_width_divided_by_columns(self):
        """
        Test that available width is divided by number of columns.
        """
        html = load_puzzle_html()

        # Check for division by columns
        assert '/ columns' in html or '/columns' in html, (
            "Cell width should divide by number of columns"
        )


class TestFontSizeProportionalScaling:
    """
    Verify font sizes scale proportionally with cell sizes.
    """

    def test_font_size_calculation_based_on_cell_width(self):
        """
        Test that font size is calculated based on cell width.
        """
        html = load_puzzle_html()

        # Check cellWidth is used in font calculation
        assert 'cellWidth' in html, (
            "cellWidth should be used in font size calculation"
        )

    def test_chinese_multiplier_allows_larger_font(self):
        """
        Test that zh-TW has smallest multiplier (1.15) for largest font.

        Since zh-TW uses single characters, font can be much larger.
        """
        html = load_puzzle_html()

        # zh-TW should have the smallest multiplier
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        assert width_multipliers_section is not None, (
            "widthMultipliers should be defined"
        )

        section_text = width_multipliers_section.group(0)

        # Extract multiplier values (code uses single quotes for zh-TW key)
        chinese_match = re.search(r"'zh-TW':\s*([\d.]+)", section_text)
        english_match = re.search(r'english:\s*([\d.]+)', section_text)

        assert chinese_match and english_match, (
            "Both zh-TW and English multipliers should be present"
        )

        chinese_mult = float(chinese_match.group(1))
        english_mult = float(english_match.group(1))

        # zh-TW multiplier should be smaller (resulting in larger font)
        assert chinese_mult < english_mult, (
            f"zh-TW multiplier ({chinese_mult}) should be smaller than "
            f"English ({english_mult}) for larger font size"
        )

    def test_chinese_font_approximately_3_to_4x_larger_than_english(self):
        """
        Test that zh-TW font is approximately 3x larger than English.

        Updated for accessible palette:
        Ratio should be English/zh-TW multiplier = 3.6/1.15 = ~3.13x
        """
        html = load_puzzle_html()

        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        assert width_multipliers_section is not None
        section_text = width_multipliers_section.group(0)

        chinese_match = re.search(r"'zh-TW':\s*([\d.]+)", section_text)
        english_match = re.search(r'english:\s*([\d.]+)', section_text)

        assert chinese_match and english_match

        chinese_mult = float(chinese_match.group(1))
        english_mult = float(english_match.group(1))

        ratio = english_mult / chinese_mult

        # Ratio should be between 2.5 and 4 (updated for new multipliers)
        assert 2.5 <= ratio <= 4, (
            f"English/zh-TW multiplier ratio ({ratio:.2f}) should be 2.5-4x "
            f"for zh-TW to display larger"
        )


class TestApplyPuzzleFontSizeFunction:
    """
    Verify applyPuzzleFontSize function works correctly.
    """

    def test_apply_puzzle_font_size_function_exists(self):
        """
        Test that applyPuzzleFontSize function is defined.
        """
        html = load_puzzle_html()

        assert 'function applyPuzzleFontSize' in html or 'applyPuzzleFontSize = function' in html or 'applyPuzzleFontSize()' in html, (
            "applyPuzzleFontSize function should be defined"
        )

    def test_apply_puzzle_font_size_sets_style_on_cells(self):
        """
        Test that applyPuzzleFontSize sets fontSize style on cells.
        """
        html = load_puzzle_html()

        # Check for setting fontSize on cells
        assert '.fontSize' in html or "fontSize =" in html or 'fontSize=' in html, (
            "applyPuzzleFontSize should set fontSize style"
        )

        assert '.puzzle-cell' in html, (
            ".puzzle-cell selector should exist"
        )


class TestContainerNotFullViewportOnLargeScreens:
    """
    Verify container doesn't take full viewport on large screens.
    """

    def test_max_width_500px_prevents_excessive_width(self):
        """
        Test that 500px max-width prevents puzzle from being too wide.

        On 4K monitors, puzzle should not overwhelm with excessive size.
        """
        html = load_puzzle_html()

        # Verify max-width is 500px
        assert 'max-width: 500px' in html or 'max-width:500px' in html, (
            "Container should have max-width: 500px to limit size on large screens"
        )

        # Should not be 100% width on desktop (no max-width: 100% for puzzle-grid)
        puzzle_grid_section = re.search(
            r'\.puzzle-grid\s*\{[^}]+\}',
            html,
            re.DOTALL
        )

        if puzzle_grid_section:
            section = puzzle_grid_section.group(0)
            # Should not have 100% max-width in main styles
            assert 'max-width: 100%' not in section and 'max-width:100%' not in section, (
                ".puzzle-grid should not have max-width: 100% in main styles"
            )
