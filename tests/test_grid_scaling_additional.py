"""
Additional grid scaling tests for ColorFocus.

Task Group 4: Additional Strategic Tests.
Tests verify cell width formula, proportional scaling, and container limits.
"""

import re
from conftest import load_puzzle_html, load_puzzle_css, load_puzzle_js


class TestCellWidthCalculationFormula:
    """
    Verify cell width calculation formula is correct.
    """

    def test_cell_width_accounts_for_gaps_between_columns(self):
        """Test that cell width calculation subtracts gaps."""
        js_content = load_puzzle_js()
        assert 'columns - 1' in js_content or '(columns-1)' in js_content, (
            "Cell width should account for (columns - 1) gaps"
        )

    def test_cell_width_divided_by_columns(self):
        """Test that available width is divided by number of columns."""
        js_content = load_puzzle_js()
        assert '/ columns' in js_content or '/columns' in js_content, (
            "Cell width should divide by number of columns"
        )


class TestFontSizeProportionalScaling:
    """
    Verify font sizes scale proportionally with cell sizes.
    """

    def test_font_size_calculation_based_on_cell_width(self):
        """Test that font size is calculated based on cell width."""
        js_content = load_puzzle_js()
        assert 'cellWidth' in js_content, (
            "cellWidth should be used in font size calculation"
        )

    def test_chinese_multiplier_allows_larger_font(self):
        """Test that zh-TW has smallest multiplier (1.15) for largest font."""
        js_content = load_puzzle_js()
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            js_content,
            re.DOTALL
        )
        assert width_multipliers_section is not None, (
            "widthMultipliers should be defined"
        )
        section_text = width_multipliers_section.group(0)
        chinese_match = re.search(r"'zh-TW':\s*([\d.]+)", section_text)
        english_match = re.search(r'english:\s*([\d.]+)', section_text)
        assert chinese_match and english_match, (
            "Both zh-TW and English multipliers should be present"
        )
        chinese_mult = float(chinese_match.group(1))
        english_mult = float(english_match.group(1))
        assert chinese_mult < english_mult, (
            f"zh-TW multiplier ({chinese_mult}) should be smaller than "
            f"English ({english_mult}) for larger font size"
        )

    def test_chinese_font_approximately_3_to_4x_larger_than_english(self):
        """Test that zh-TW font is approximately 3x larger than English."""
        js_content = load_puzzle_js()
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            js_content,
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
        assert 2.5 <= ratio <= 4, (
            f"English/zh-TW multiplier ratio ({ratio:.2f}) should be 2.5-4x "
            f"for zh-TW to display larger"
        )


class TestApplyPuzzleFontSizeFunction:
    """
    Verify applyPuzzleFontSize function works correctly.
    """

    def test_apply_puzzle_font_size_function_exists(self):
        """Test that applyPuzzleFontSize function is defined."""
        js_content = load_puzzle_js()
        assert 'function applyPuzzleFontSize' in js_content or 'applyPuzzleFontSize = function' in js_content or 'applyPuzzleFontSize()' in js_content, (
            "applyPuzzleFontSize function should be defined"
        )

    def test_apply_puzzle_font_size_sets_style_on_cells(self):
        """Test that applyPuzzleFontSize sets fontSize style on cells."""
        js_content = load_puzzle_js()
        css = load_puzzle_css()
        assert '.fontSize' in js_content or "fontSize =" in js_content or 'fontSize=' in js_content, (
            "applyPuzzleFontSize should set fontSize style"
        )
        assert '.puzzle-cell' in css, (
            ".puzzle-cell selector should exist"
        )


class TestContainerNotFullViewportOnLargeScreens:
    """
    Verify container doesn't take full viewport on large screens.
    """

    def test_max_width_500px_prevents_excessive_width(self):
        """Test that 500px max-width prevents puzzle from being too wide."""
        css = load_puzzle_css()
        assert 'max-width: 500px' in css or 'max-width:500px' in css, (
            "Container should have max-width: 500px to limit size on large screens"
        )
        puzzle_grid_section = re.search(
            r'\.puzzle-grid\s*\{[^}]+\}',
            css,
            re.DOTALL
        )
        if puzzle_grid_section:
            section = puzzle_grid_section.group(0)
            assert 'max-width: 100%' not in section and 'max-width:100%' not in section, (
                ".puzzle-grid should not have max-width: 100% in main styles"
            )
