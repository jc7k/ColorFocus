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


class TestDifficultyPresetsCongruenceOnly:
    """
    Verify difficulty presets work correctly.
    Difficulty now controls Stroop interference (congruence %) only.
    Grid size and color count are independent settings.
    """

    def test_difficulty_presets_constant_exists(self):
        """Test that DIFFICULTY_PRESETS constant exists with all levels."""
        html = load_puzzle_html()
        assert 'DIFFICULTY_PRESETS' in html, (
            "DIFFICULTY_PRESETS constant should exist"
        )
        assert 'easy:' in html or 'easy :' in html, (
            "Easy preset should exist"
        )
        assert 'medium:' in html or 'medium :' in html, (
            "Medium preset should exist"
        )
        assert 'hard:' in html or 'hard :' in html, (
            "Hard preset should exist"
        )
        assert 'expert:' in html or 'expert :' in html, (
            "Expert preset should exist"
        )

    def test_easy_preset_has_75_percent_congruence(self):
        """Test that easy preset uses 75% congruence (low Stroop interference)."""
        html = load_puzzle_html()
        easy_section = re.search(
            r'easy:\s*\{[^}]+\}',
            html,
            re.DOTALL
        )
        assert easy_section is not None, (
            "Easy preset should be defined"
        )
        section_text = easy_section.group(0)
        assert 'congruencePercent: 75' in section_text or 'congruencePercent:75' in section_text, (
            "Easy preset should have congruencePercent: 75"
        )

    def test_expert_preset_has_0_percent_congruence(self):
        """Test that expert preset uses 0% congruence (max Stroop interference)."""
        html = load_puzzle_html()
        expert_section = re.search(
            r'expert:\s*\{[^}]+\}',
            html,
            re.DOTALL
        )
        assert expert_section is not None, (
            "Expert preset should be defined"
        )
        section_text = expert_section.group(0)
        assert 'congruencePercent: 0' in section_text or 'congruencePercent:0' in section_text, (
            "Expert preset should have congruencePercent: 0"
        )

    def test_presets_do_not_include_grid_size(self):
        """Test that presets only control congruence, not grid size."""
        html = load_puzzle_html()
        # Find the DIFFICULTY_PRESETS block
        presets_match = re.search(
            r'const DIFFICULTY_PRESETS\s*=\s*\{[^;]+\};',
            html,
            re.DOTALL
        )
        assert presets_match is not None, (
            "DIFFICULTY_PRESETS should be defined"
        )
        presets_text = presets_match.group(0)
        # Grid size should NOT be in presets (it's now independent)
        assert 'gridSize' not in presets_text, (
            "DIFFICULTY_PRESETS should not include gridSize (now independent setting)"
        )
