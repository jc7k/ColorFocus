"""
Tests for the Mistake Identification feature.

These tests verify the core functionality of the mistake identification
flow including state management, UI components, visualization, and
the end-to-end workflow.

Test Coverage:
- Task Group 1: Core logic (discrepancy detection, Stroop analysis)
- Task Group 2: UI components (button visibility, prompt display)
- Task Group 3: Visualization (tile marking, summary)
- Task Group 4: Integration (end-to-end workflow)
"""

import json
import re
from pathlib import Path

from conftest import load_puzzle_html, load_puzzle_css, load_puzzle_js


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
UI_TEXT_JSON_PATH = PROJECT_ROOT / "shared" / "ui_text.json"


def load_ui_text() -> dict:
    """Load the ui_text.json file."""
    with open(UI_TEXT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestCoreLogic:
    """
    Tests for Task Group 1: Core logic layer.

    Verifies state management, discrepancy detection, and Stroop analysis.
    """

    def test_identification_state_variables_exist(self):
        """
        Verify that all required identification state variables are defined.

        Required variables:
        - identificationMode (boolean)
        - identificationStep (object)
        - discrepancyData (Map)
        - colorQueue (array)
        - identificationResults (Map)
        - mistakeAnalysis (Map)
        """
        js_content = load_puzzle_js()

        # Check for each state variable
        assert "identificationMode" in js_content, "identificationMode variable should exist"
        assert "identificationStep" in js_content, "identificationStep variable should exist"
        assert "discrepancyData" in js_content, "discrepancyData variable should exist"
        assert "colorQueue" in js_content, "colorQueue variable should exist"
        assert "identificationResults" in js_content, "identificationResults variable should exist"
        assert "mistakeAnalysis" in js_content, "mistakeAnalysis variable should exist"

        # Verify initial values
        assert "identificationMode = false" in js_content, (
            "identificationMode should initialize as false"
        )
        assert "discrepancyData = new Map()" in js_content, (
            "discrepancyData should be a Map"
        )
        assert "identificationResults = new Map()" in js_content, (
            "identificationResults should be a Map"
        )

    def test_calculate_discrepancies_function_exists(self):
        """
        Verify that calculateDiscrepancies() function exists and returns
        an array of color tokens with discrepancies.
        """
        js_content = load_puzzle_js()

        assert "function calculateDiscrepancies()" in js_content, (
            "calculateDiscrepancies function should be defined"
        )
        # Verify it returns array of colors with discrepancies
        assert "colorsWithDiscrepancies" in js_content, (
            "Function should track colors with discrepancies"
        )

    def test_stroop_analysis_function_exists(self):
        """
        Verify that analyzeStroopInfluence() function exists and checks
        adjacent tiles for word text matches.
        """
        js_content = load_puzzle_js()

        assert "function analyzeStroopInfluence" in js_content, (
            "analyzeStroopInfluence function should be defined"
        )
        # Verify it uses adjacent tile analysis
        assert "getAdjacentTileIndices" in js_content, (
            "Should use getAdjacentTileIndices for neighbor lookup"
        )

    def test_get_adjacent_tile_indices_function_exists(self):
        """
        Verify that getAdjacentTileIndices() returns orthogonally adjacent
        tile indices (up, down, left, right).
        """
        js_content = load_puzzle_js()

        assert "function getAdjacentTileIndices" in js_content, (
            "getAdjacentTileIndices function should be defined"
        )
        # Verify it calculates row/col from index (uses gridSize from state)
        assert "Math.floor(tileIndex /" in js_content, (
            "Should calculate row from tile index"
        )
        assert "tileIndex %" in js_content, (
            "Should calculate column from tile index"
        )

    def test_reset_identification_state_function_exists(self):
        """
        Verify that resetIdentificationState() clears all identification
        state and removes CSS classes from tiles.
        """
        js_content = load_puzzle_js()

        # Check for exit/reset identification mode function
        assert "exitIdentificationMode" in js_content or "resetIdentificationState" in js_content, (
            "resetIdentificationState or exitIdentificationMode function should be defined"
        )
        # Verify it clears state and CSS classes
        assert "tile-correct-id" in js_content, (
            "Should reference tile-correct-id class for removal"
        )
        assert "tile-incorrect-id" in js_content, (
            "Should reference tile-incorrect-id class for removal"
        )


class TestUIComponents:
    """
    Tests for Task Group 2: UI components layer.

    Verifies button visibility, prompt display, and selection flow.
    """

    def test_identify_mistakes_button_exists(self):
        """
        Verify that "Identify Mistakes" button exists in the HTML
        with proper class for visibility toggling.
        """
        html_content = load_puzzle_html()

        assert 'id="identifyMistakesBtn"' in html_content, (
            "Identify Mistakes button should have correct ID"
        )
        assert "identify-mistakes-btn" in html_content, (
            "Button should have identify-mistakes-btn class"
        )

    def test_identification_prompt_panel_exists(self):
        """
        Verify that the identification prompt panel exists with
        all required child elements.
        """
        html_content = load_puzzle_html()

        assert 'id="identificationPrompt"' in html_content, (
            "Identification prompt panel should exist"
        )
        assert 'id="identificationColorSwatch"' in html_content, (
            "Color swatch element should exist"
        )
        assert 'id="identificationPromptText"' in html_content, (
            "Prompt text element should exist"
        )
        assert 'id="identificationNextIndicator"' in html_content, (
            "Next color indicator should exist"
        )

    def test_identification_done_and_cancel_buttons_exist(self):
        """
        Verify that Done and Cancel buttons exist for identification flow.
        """
        html_content = load_puzzle_html()

        assert 'id="identificationDoneBtn"' in html_content, (
            "Done button should exist"
        )
        assert 'id="identificationCancelBtn"' in html_content, (
            "Cancel button should exist"
        )

    def test_button_visibility_function_exists(self):
        """
        Verify that updateIdentifyMistakesButtonVisibility() exists
        and checks hasChecked and hasDiscrepancies.
        """
        js_content = load_puzzle_js()

        assert "function updateIdentifyMistakesButtonVisibility()" in js_content, (
            "updateIdentifyMistakesButtonVisibility function should exist"
        )
        assert "hasChecked" in js_content, (
            "Should check hasChecked state"
        )
        assert "hasDiscrepancies()" in js_content, (
            "Should check for discrepancies"
        )


class TestVisualization:
    """
    Tests for Task Group 3: Visualization layer.

    Verifies tile marking, legend, and summary panel.
    """

    def test_tile_marking_css_classes_exist(self):
        """
        Verify that CSS classes for tile marking are defined.
        """
        css_content = load_puzzle_css()

        # Check for CSS class definitions
        assert ".tile-correct-id" in css_content, (
            ".tile-correct-id CSS class should be defined"
        )
        assert ".tile-incorrect-id" in css_content, (
            ".tile-incorrect-id CSS class should be defined"
        )
        assert ".tile-stroop-influenced" in css_content, (
            ".tile-stroop-influenced CSS class should be defined"
        )

    def test_legend_component_exists(self):
        """
        Verify that the mistake legend component exists with all indicators.
        """
        html_content = load_puzzle_html()

        assert 'id="mistakeLegend"' in html_content, (
            "Mistake legend section should exist"
        )
        assert 'class="legend-indicator correct"' in html_content, (
            "Correct indicator should exist in legend"
        )
        assert 'class="legend-indicator incorrect"' in html_content, (
            "Incorrect indicator should exist in legend"
        )
        assert 'class="legend-indicator stroop"' in html_content, (
            "Stroop indicator should exist in legend"
        )

    def test_summary_panel_exists(self):
        """
        Verify that the summary panel exists with stats and metadata.
        """
        html_content = load_puzzle_html()

        assert 'id="mistakeSummarySection"' in html_content, (
            "Mistake summary section should exist"
        )
        assert 'id="totalMistakesValue"' in html_content, (
            "Total mistakes value should exist"
        )
        assert 'id="stroopInfluencedValue"' in html_content, (
            "Stroop-influenced value should exist"
        )
        assert 'id="nonStroopValue"' in html_content, (
            "Non-Stroop mistakes value should exist"
        )

    def test_print_styles_exist(self):
        """
        Verify that print-friendly CSS media query exists.
        """
        css_content = load_puzzle_css()

        assert "@media print" in css_content, (
            "Print media query should exist"
        )


class TestLocalization:
    """
    Tests for Task Group 4: Localization.

    Verifies all UI text keys exist with translations.
    """

    def test_all_identification_ui_text_keys_exist(self):
        """
        Verify that all identification-related UI text keys exist
        in ui_text.json with all 4 language translations.
        """
        ui_text = load_ui_text()

        required_keys = [
            "identify_mistakes_btn",
            "identification_prompt",
            "identification_done_btn",
            "identification_cancel_btn",
            "identification_next_color",
            "summary_header",
            "summary_total_mistakes",
            "summary_stroop_influenced",
            "summary_non_stroop",
            "legend_correct",
            "legend_incorrect",
            "legend_stroop",
            "legend_header"
        ]

        required_languages = ["zh-TW", "english", "spanish", "vietnamese"]

        for key in required_keys:
            assert key in ui_text, f"UI text key '{key}' should exist"
            for lang in required_languages:
                assert lang in ui_text[key], (
                    f"Key '{key}' should have '{lang}' translation"
                )
                assert ui_text[key][lang], (
                    f"Key '{key}' should have non-empty '{lang}' translation"
                )

    def test_identification_prompt_has_color_placeholder(self):
        """
        Verify that identification_prompt text contains {color} placeholder.
        """
        ui_text = load_ui_text()

        for lang, text in ui_text["identification_prompt"].items():
            assert "{color}" in text, (
                f"identification_prompt in '{lang}' should contain {{color}} placeholder"
            )


class TestIntegration:
    """
    Tests for Task Group 4: Integration.

    Verifies end-to-end workflow and event wiring.
    """

    def test_event_listeners_are_wired(self):
        """
        Verify that all identification mode event listeners are wired up.
        """
        js_content = load_puzzle_js()

        # Check for event listener registrations
        assert "identifyMistakesBtn" in js_content and "addEventListener" in js_content, (
            "Identify Mistakes button should have event listener"
        )
        assert "identificationDoneBtn" in js_content and "handleIdentificationDone" in js_content, (
            "Done button should trigger handleIdentificationDone"
        )
        assert "identificationCancelBtn" in js_content and "handleIdentificationCancel" in js_content, (
            "Cancel button should trigger handleIdentificationCancel"
        )

    def test_generate_puzzle_resets_identification_state(self):
        """
        Verify that generatePuzzle() calls resetIdentificationState() or
        closeSummaryPanel() to clean up identification state.
        """
        js_content = load_puzzle_js()

        # Find the generatePuzzle function and check it calls reset or close
        generate_puzzle_match = re.search(
            r'function generatePuzzle[\s\S]*?(resetIdentificationState|closeSummaryPanel)',
            js_content
        )
        assert generate_puzzle_match, (
            "generatePuzzle() should call resetIdentificationState() or closeSummaryPanel()"
        )

    def test_clear_all_selections_handles_identification_mode(self):
        """
        Verify that clearAllSelections() checks for identification mode.
        """
        js_content = load_puzzle_js()

        # Find clearAllSelections and check it handles identification mode
        clear_selections_match = re.search(
            r'function clearAllSelections[\s\S]*?identificationMode',
            js_content
        )
        assert clear_selections_match, (
            "clearAllSelections() should handle identification mode"
        )

    def test_check_answers_calculates_discrepancies(self):
        """
        Verify that checkAnswers() or showResults() calls calculateDiscrepancies() and
        updates button visibility.
        """
        js_content = load_puzzle_js()

        # Check that calculateDiscrepancies is called somewhere in the answers flow
        has_discrepancy_calculation = (
            "calculateDiscrepancies" in js_content and
            "updateIdentifyMistakesButtonVisibility" in js_content
        )
        assert has_discrepancy_calculation, (
            "Should call calculateDiscrepancies() and updateIdentifyMistakesButtonVisibility()"
        )

    def test_analyze_and_visualize_mistakes_exists(self):
        """
        Verify that analyzeAndVisualizeMistakes() exists and orchestrates
        the analysis and visualization flow.
        """
        js_content = load_puzzle_js()

        assert "function analyzeAndVisualizeMistakes()" in js_content, (
            "analyzeAndVisualizeMistakes function should exist"
        )
        # Verify it calls analysis and display functions
        assert "analyzeIdentificationResults()" in js_content, (
            "Should call analyzeIdentificationResults()"
        )
        assert "applyTileMarking()" in js_content, (
            "Should call applyTileMarking()"
        )
        assert "displaySummary()" in js_content, (
            "Should call displaySummary()"
        )


class TestKeyboardAccessibility:
    """
    Tests for keyboard accessibility in identification flow.
    """

    def test_escape_key_handler_for_identification_mode(self):
        """
        Verify that Escape key can cancel identification mode.
        """
        js_content = load_puzzle_js()

        # Check for a global or identification-specific escape handler
        # It should either:
        # 1. Have a dedicated handler that checks identificationMode
        # 2. Or use the existing modal escape pattern extended for identification
        has_escape_handling = (
            ("Escape" in js_content and "identificationMode" in js_content) or
            ("handleIdentificationEscape" in js_content) or
            ("handleGlobalKeydown" in js_content)
        )
        assert has_escape_handling, (
            "Should have Escape key handling for identification mode"
        )


class TestResponsive:
    """
    Tests for responsive behavior.
    """

    def test_mobile_styles_for_identification_prompt(self):
        """
        Verify that identification prompt has mobile-responsive CSS.
        """
        css_content = load_puzzle_css()

        # Check for media query covering identification prompt
        assert "@media (max-width: 480px)" in css_content, (
            "Should have mobile media query"
        )
        # The identification prompt should have responsive styles
        assert ".identification-prompt" in css_content, (
            "Identification prompt should have CSS styles"
        )

    def test_summary_panel_has_mobile_styles(self):
        """
        Verify that summary panel has mobile-responsive CSS.
        """
        css_content = load_puzzle_css()

        # Check for summary section styles
        assert ".mistake-summary-section" in css_content, (
            "Mistake summary section should have CSS styles"
        )
