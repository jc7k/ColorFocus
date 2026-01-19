"""
Additional grid scaling tests for ColorFocus.

Task Group 4: Additional Strategic Tests.
Tests verify cell width formula, proportional scaling, and container limits.
"""

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


def load_puzzle_html() -> str:
    """Load the puzzle.html file."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestCellWidthCalculationFormula:
    """
    Verify cell width calculation formula is correct.
    """

    def test_cell_width_accounts_for_gaps_between_columns(self):
        """Test that cell width calculation subtracts gaps."""
        html = load_puzzle_html()
        assert 'columns - 1' in html or '(columns-1)' in html, (
            "Cell width should account for (columns - 1) gaps"
        )

    def test_cell_width_divided_by_columns(self):
        """Test that available width is divided by number of columns."""
        html = load_puzzle_html()
        assert '/ columns' in html or '/columns' in html, (
            "Cell width should divide by number of columns"
        )


class TestFontSizeProportionalScaling:
    """
    Verify font sizes scale proportionally with cell sizes.
    """

    def test_font_size_calculation_based_on_cell_width(self):
        """Test that font size is calculated based on cell width."""
        html = load_puzzle_html()
        assert 'cellWidth' in html, (
            "cellWidth should be used in font size calculation"
        )

    def test_chinese_multiplier_allows_larger_font(self):
        """Test that zh-TW has smallest multiplier (1.15) for largest font."""
        html = load_puzzle_html()
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            html,
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
        html = load_puzzle_html()
        assert 'function applyPuzzleFontSize' in html or 'applyPuzzleFontSize = function' in html or 'applyPuzzleFontSize()' in html, (
            "applyPuzzleFontSize function should be defined"
        )

    def test_apply_puzzle_font_size_sets_style_on_cells(self):
        """Test that applyPuzzleFontSize sets fontSize style on cells."""
        html = load_puzzle_html()
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
        """Test that 500px max-width prevents puzzle from being too wide."""
        html = load_puzzle_html()
        assert 'max-width: 500px' in html or 'max-width:500px' in html, (
            "Container should have max-width: 500px to limit size on large screens"
        )
        puzzle_grid_section = re.search(
            r'\.puzzle-grid\s*\{[^}]+\}',
            html,
            re.DOTALL
        )
        if puzzle_grid_section:
            section = puzzle_grid_section.group(0)
            assert 'max-width: 100%' not in section and 'max-width:100%' not in section, (
                ".puzzle-grid should not have max-width: 100% in main styles"
            )
