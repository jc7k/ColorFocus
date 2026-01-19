"""
Responsive and cross-browser integration tests for ColorFocus.

Task Group 3: Cross-Browser and Responsive Integration.
Tests verify language support, spacing options, and difficulty presets.
"""

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
PUZZLE_HTML_PATH = PROJECT_ROOT / "frontend" / "puzzle.html"


def load_puzzle_html() -> str:
    """Load the puzzle.html file."""
    with open(PUZZLE_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestAllLanguagesAtGridSizes:
    """
    Verify all four languages render correctly at various grid sizes.
    """

    def test_calculate_puzzle_font_size_handles_all_languages(self):
        """Test that calculatePuzzleFontSize handles all four languages."""
        html = load_puzzle_html()
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
        """Test that SPACING_VALUES constant has all spacing options."""
        html = load_puzzle_html()
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
        """Test that DIFFICULTY_PRESETS constant exists with all tiers."""
        html = load_puzzle_html()
        assert 'DIFFICULTY_PRESETS' in html, (
            "DIFFICULTY_PRESETS constant should exist"
        )
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
        """Test that accessible preset uses 3x3 grid."""
        html = load_puzzle_html()
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
        """Test that advanced preset uses 8x8 grid."""
        html = load_puzzle_html()
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
