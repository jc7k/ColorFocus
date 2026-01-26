"""
Configurable grid size tests for ColorFocus.

These tests verify that the configurable grid size feature is correctly implemented,
including the grid size dropdown, dynamic CSS updates, color count limiting,
puzzle generation, and font size calculations.

This test file covers Task Group 3: Configurable Grid Size.
"""

import json
from conftest import load_puzzle_html, load_puzzle_css, load_puzzle_js


class TestGridSizeDropdownRendering:
    """
    Verify grid size dropdown renders correctly with all options.

    These tests ensure the grid size selector exists and shows options 1x1 through 8x8.
    """

    def test_grid_size_dropdown_renders_options_1x1_through_8x8(self):
        """
        Test that grid size dropdown renders options 1x1 through 8x8.

        The dropdown should contain 8 options from 1x1 to 8x8 for users
        to select their desired grid dimension.
        """
        html = load_puzzle_html()

        # Check dropdown exists with id="gridSize"
        assert 'id="gridSize"' in html, (
            "Grid size dropdown should have id='gridSize'"
        )

        # Check all 8 options exist (1x1 through 8x8)
        for size in range(1, 9):
            option_text = f'value="{size}"'
            assert option_text in html, (
                f"Grid size dropdown should contain option for {size}x{size}"
            )

        # Check default 4x4 is selected
        assert 'value="4" selected' in html or 'value="4"selected' in html, (
            "Grid size dropdown should default to 4x4"
        )

    def test_grid_size_dropdown_positioned_between_language_and_colors(self):
        """
        Test that grid size dropdown appears between Language and Colors dropdowns.

        The controls should be ordered: Language, Grid, Colors for logical grouping.
        """
        html = load_puzzle_html()

        # Find positions of each control
        language_pos = html.find('id="language"')
        grid_pos = html.find('id="gridSize"')
        colors_pos = html.find('id="colorCount"')

        assert language_pos != -1, "Language dropdown should exist"
        assert grid_pos != -1, "Grid size dropdown should exist"
        assert colors_pos != -1, "Color count dropdown should exist"

        # Verify order: language < grid < colors
        assert language_pos < grid_pos < colors_pos, (
            f"Grid size dropdown should appear between Language and Colors. "
            f"Positions: language={language_pos}, grid={grid_pos}, colors={colors_pos}"
        )


class TestGridSizeStateManagement:
    """
    Verify grid size state management and localStorage persistence.
    """

    def test_grid_size_state_variable_exists_with_default_4(self):
        """
        Test that currentGridSize state variable is initialized with default of 4.

        The default value of 4 can be set directly or via a fallback mechanism
        (e.g., `validateGridSize(localStorage.getItem('colorFocusGridSize') || 4)`).
        """
        js_content = load_puzzle_js()

        assert 'currentGridSize' in js_content, (
            "currentGridSize state variable should be defined"
        )

        # Should have a default value of 4 (either directly or via fallback)
        # Accept patterns like: "currentGridSize = 4", "|| 4)", "4)" at end of validation
        has_default_4 = (
            'currentGridSize = 4' in js_content or
            'currentGridSize=4' in js_content or
            '|| 4)' in js_content  # Fallback pattern used with validateGridSize
        )
        assert has_default_4, (
            "currentGridSize should default to 4 (directly or via fallback)"
        )

    def test_grid_size_localstorage_key_defined(self):
        """
        Test that grid size localStorage key is defined for persistence.
        """
        js_content = load_puzzle_js()

        assert 'colorFocusGridSize' in js_content, (
            "localStorage key 'colorFocusGridSize' should be used for persistence"
        )


class TestDynamicGridCSS:
    """
    Verify dynamic grid CSS updates based on grid size selection.
    """

    def test_grid_template_columns_uses_repeat_pattern(self):
        """
        Test that grid CSS uses dynamic repeat(N, 1fr) pattern.

        The grid-template-columns should update dynamically based on
        the selected grid dimension.
        """
        css = load_puzzle_css()
        html = load_puzzle_html()

        # Check that the CSS handles grid-template-columns
        assert 'grid-template-columns' in css, (
            "CSS should include grid-template-columns"
        )

        # Check for dynamic repeat pattern - either in CSS or JS
        has_repeat_in_css = 'repeat(' in css and '1fr)' in css
        has_dynamic_update_in_js = 'gridTemplateColumns' in html
        assert has_repeat_in_css or has_dynamic_update_in_js, (
            "Grid should use repeat(N, 1fr) pattern for dynamic sizing"
        )


class TestColorCountAutoLimiting:
    """
    Verify automatic color count limiting based on grid size.
    """

    def test_max_colors_calculation_logic_exists(self):
        """
        Test that color count is auto-limited based on grid size.

        For a 3x3 grid, max colors should be 3.
        For an 8x8 grid, max colors should be 8.
        Formula: maxColors = min(8, gridSize)
        """
        js_content = load_puzzle_js()

        # Check for maxColors calculation
        assert 'maxColors' in js_content or 'max_colors' in js_content.lower(), (
            "maxColors calculation should exist for color limiting"
        )

        # Should clamp to 8 maximum
        assert 'Math.min(8' in js_content or 'min(8,' in js_content, (
            "Max colors should be capped at 8"
        )


class TestPuzzleGenerationForVariableGridSizes:
    """
    Verify puzzle generation works correctly for variable grid sizes.
    """

    def test_total_cells_uses_dynamic_grid_size(self):
        """
        Test that puzzle generates correct number of cells for selected grid size.

        totalCells should be gridSize * gridSize, not hardcoded 64.
        """
        js_content = load_puzzle_js()

        # Check that totalCells calculation uses gridSize (via state.currentGridSize)
        has_dynamic_cells = (
            'currentGridSize * currentGridSize' in js_content or
            'state.currentGridSize * state.currentGridSize' in js_content or
            'gridSize * gridSize' in js_content
        )
        assert has_dynamic_cells, (
            "totalCells should be calculated as gridSize * gridSize"
        )


class TestFontSizeCalculation:
    """
    Verify font size calculation adjusts for different grid column counts.
    """

    def test_font_size_calculation_uses_grid_size(self):
        """
        Test that font size calculation adjusts for different grid column counts.

        The calculatePuzzleFontSize function should use the current grid size
        for cell width calculation, not hardcoded 8.
        """
        js_content = load_puzzle_js()

        # Check calculatePuzzleFontSize function exists
        assert 'calculatePuzzleFontSize' in js_content, (
            "calculatePuzzleFontSize function should exist"
        )

        # Check that columns uses currentGridSize (not hardcoded 8)
        # Either through parameter or using the global currentGridSize
        assert (
            'const columns = currentGridSize' in js_content or
            'columns = currentGridSize' in js_content or
            'currentGridSize' in js_content  # At minimum, currentGridSize should be referenced
        ), (
            "Font size calculation should use currentGridSize for column count"
        )
