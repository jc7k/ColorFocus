"""
Responsive and cross-browser integration tests for ColorFocus.

Task Group 3: Cross-Browser and Responsive Integration.
Tests verify language support, spacing options, and difficulty presets.
"""

import re
from pathlib import Path

from conftest import load_puzzle_js


class TestAllLanguagesAtGridSizes:
    """
    Verify all four languages render correctly at various grid sizes.
    """

    def test_calculate_puzzle_font_size_handles_all_languages(self):
        """Test that calculatePuzzleFontSize handles all four languages."""
        js_content = load_puzzle_js()
        width_multipliers_section = re.search(
            r'widthMultipliers\s*=\s*\{[^}]+\}',
            js_content,
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
        js_content = load_puzzle_js()
        assert 'compact: 1' in js_content or 'compact:1' in js_content, (
            "SPACING_VALUES should have compact: 1"
        )
        assert 'normal: 2' in js_content or 'normal:2' in js_content, (
            "SPACING_VALUES should have normal: 2"
        )
        assert 'relaxed: 6' in js_content or 'relaxed:6' in js_content, (
            "SPACING_VALUES should have relaxed: 6"
        )
        assert 'spacious: 12' in js_content or 'spacious:12' in js_content, (
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
        js_content = load_puzzle_js()
        assert 'DIFFICULTY_PRESETS' in js_content, (
            "DIFFICULTY_PRESETS constant should exist"
        )
        assert 'easy:' in js_content or 'easy :' in js_content, (
            "Easy preset should exist"
        )
        assert 'medium:' in js_content or 'medium :' in js_content, (
            "Medium preset should exist"
        )
        assert 'hard:' in js_content or 'hard :' in js_content, (
            "Hard preset should exist"
        )
        assert 'expert:' in js_content or 'expert :' in js_content, (
            "Expert preset should exist"
        )

    def test_easy_preset_has_75_percent_congruence(self):
        """Test that easy preset uses 75% congruence (low Stroop interference)."""
        js_content = load_puzzle_js()
        easy_section = re.search(
            r'easy:\s*\{[^}]+\}',
            js_content,
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
        js_content = load_puzzle_js()
        expert_section = re.search(
            r'expert:\s*\{[^}]+\}',
            js_content,
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
        js_content = load_puzzle_js()
        # Find the DIFFICULTY_PRESETS block
        presets_match = re.search(
            r'const DIFFICULTY_PRESETS\s*=\s*\{[^;]+\};',
            js_content,
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
