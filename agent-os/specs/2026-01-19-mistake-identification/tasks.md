# Task Breakdown: Mistake Identification

## Overview
Total Tasks: 26 (across 4 task groups)

This feature helps users identify which specific tiles they misidentified during a Stroop puzzle, analyze whether Stroop interference contributed to errors, and present findings useful for health professionals supporting cognitive rehabilitation.

## Task List

### Core Logic Layer

#### Task Group 1: State Management and Data Structures
**Dependencies:** None

- [x] 1.0 Complete core state management and data structures
  - [x] 1.1 Write 4-6 focused tests for mistake identification logic
    - Test discrepancy detection (user count vs correct count)
    - Test identification mode state transitions (enter, exit, color cycling)
    - Test tile selection storage during identification flow
    - Test Stroop effect detection for adjacent tiles
  - [x] 1.2 Add identification state variables to puzzle.html
    - `identificationMode` (boolean): Whether identification mode is active
    - `identificationStep` (object): Current color being identified, index in queue
    - `discrepancyData` (object): Map of color tokens to {userCount, correctCount, difference}
    - `colorQueue` (array): Colors with discrepancies to process in order
    - `identificationResults` (object): Map of color tokens to Set of selected tile indices
    - `mistakeAnalysis` (object): Tile-level analysis results (correct, incorrect, stroopInfluenced)
  - [x] 1.3 Implement discrepancy calculation function
    - Compare user answers from input fields against `correctAnswers` object
    - Store discrepancy data per color token (userCount, correctCount, difference)
    - Determine which colors have discrepancies (over-count or under-count)
    - Return array of color tokens with discrepancies for the color queue
  - [x] 1.4 Implement Stroop effect analysis algorithm
    - Input: tile index, user's perceived color for that tile
    - Get orthogonally adjacent tile indices (up/down/left/right) using grid position math
    - Check if any adjacent tile's `word` property matches user's perceived color
    - Return boolean indicating if Stroop interference likely occurred
    - Use existing pattern: `row = Math.floor(index / currentGridSize)`, `col = index % currentGridSize`
  - [x] 1.5 Implement identification state reset function
    - Clear all identification state variables
    - Remove all identification-related CSS classes from tiles
    - Extend existing `clearAllSelections()` to also clear identification state
    - Call on new puzzle generation and when exiting identification mode
  - [x] 1.6 Ensure core logic tests pass
    - Run ONLY the 4-6 tests written in 1.1
    - Verify state transitions work correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 1.1 pass
- State variables correctly track identification flow
- Discrepancy detection accurately compares user answers to correct answers
- Stroop analysis correctly identifies adjacent word text matches
- State reset properly clears all identification data

---

### UI Components Layer

#### Task Group 2: Identification Mode UI
**Dependencies:** Task Group 1 (completed)

- [x] 2.0 Complete identification mode UI components
  - [x] 2.1 Write 4-6 focused tests for UI components
    - Test "Identify Mistakes" button visibility (shows only when discrepancies exist)
    - Test identification prompt display (correct color swatch, localized label)
    - Test "Done" button advances to next color or completes flow
    - Test exit button returns to normal puzzle view
  - [x] 2.2 Add "Identify Mistakes" button to results section
    - Add button element after result message in results section
    - Button text from `getUIText('identify_mistakes_btn')`
    - Show button only when `hasChecked` is true AND discrepancies exist
    - Button click triggers entry into identification mode
    - Style using existing button patterns (`.secondary` or new `.identification` class)
  - [x] 2.3 Create identification prompt panel
    - New section below puzzle grid (or overlay panel)
    - Display current color being identified with color swatch and localized label
    - Instruction text: "Select the tiles you thought were [COLOR]"
    - Use `colorsJson[token]` for swatch color and `colorLabelsJson[token][currentLanguage]` for label
    - Add localization keys to `shared/ui_text.json` for all prompt strings
  - [x] 2.4 Implement guided color selection flow
    - When entering identification mode, populate `colorQueue` from discrepancy data
    - Display prompt for first color in queue
    - Allow user to select/deselect tiles using existing `toggleTileSelection` mechanism
    - "Done" button stores selections in `identificationResults` and advances to next color
    - After last color, trigger analysis and visualization
  - [x] 2.5 Add "Done" and "Cancel" buttons to identification prompt
    - "Done" button confirms selections for current color, advances flow
    - "Cancel" button exits identification mode, returns to normal view
    - Both buttons follow existing button styling patterns
    - Add localization keys for button text
  - [x] 2.6 Ensure identification mode toggles correctly
    - Entering identification mode: hide normal UI elements as needed, show prompt
    - Exiting identification mode: restore normal UI, clear identification state
    - Tiles remain selectable during identification mode
  - [x] 2.7 Ensure UI component tests pass
    - Run ONLY the 4-6 tests written in 2.1
    - Verify button visibility logic works
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 2.1 pass
- "Identify Mistakes" button appears only when errors exist after checking answers
- Identification prompt correctly displays color and instructions
- User can select tiles and advance through color queue
- Cancel properly exits identification mode

---

### Visualization Layer

#### Task Group 3: Mistake Visualization and Summary
**Dependencies:** Task Group 2 (completed)

- [x] 3.0 Complete visualization and summary components
  - [x] 3.1 Write 4-6 focused tests for visualization
    - Test correct tile identification styling (correctly identified tiles)
    - Test incorrect tile identification styling (user thought wrong color)
    - Test Stroop influence indicator styling
    - Test summary panel displays correct counts
  - [x] 3.2 Add CSS classes for tile marking
    - `.tile-correct-id`: Tiles user correctly identified for a color (subtle positive indicator)
    - `.tile-incorrect-id`: Tiles user incorrectly selected (thought it was this color but wasn't)
    - `.tile-stroop-influenced`: Additional indicator for Stroop-influenced mistakes
    - Use border colors, overlay patterns, or icons that don't obscure tile content
    - Ensure accessibility: non-color-only indicators, sufficient contrast
    - Follow existing CSS variable patterns from design system
  - [x] 3.3 Implement tile marking logic after identification flow
    - After user completes all color selections, analyze results
    - For each tile in `identificationResults`, check if tile's actual `inkColor` matches the color user selected it for
    - Mark correctly identified tiles with `.tile-correct-id`
    - Mark incorrectly selected tiles with `.tile-incorrect-id`
    - For incorrect tiles, run Stroop analysis; add `.tile-stroop-influenced` if applicable
    - Store analysis in `mistakeAnalysis` object
  - [x] 3.4 Create legend component for mistake indicators
    - Display after identification completes
    - Show samples of each indicator type with explanation text
    - Include: correct identification, incorrect identification, Stroop-influenced
    - Add localization keys for legend text
  - [x] 3.5 Create summary panel component
    - Display after identification flow completes
    - Show: total mistakes, Stroop-influenced count, non-Stroop mistakes
    - Include puzzle metadata (seed, grid size, language, difficulty) for reproducibility
    - Format suitable for health professionals (clear labels, printable layout)
    - Use existing section styling patterns (`.answer-section`, `.results-section`)
  - [x] 3.6 Add print-friendly CSS for summary
    - Use `@media print` styles
    - Ensure summary panel and marked tiles print clearly
    - Hide unnecessary UI elements when printing
  - [x] 3.7 Ensure visualization tests pass
    - Run ONLY the 4-6 tests written in 3.1
    - Verify tile marking displays correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- Tiles display correct visual indicators based on identification results
- Stroop-influenced tiles have distinct indicator
- Legend clearly explains all indicators
- Summary shows accurate counts and is printable

---

### Localization and Integration Layer

#### Task Group 4: Localization, Integration, and Testing
**Dependencies:** Task Groups 1-3 (all completed)

- [x] 4.0 Complete localization and integration
  - [x] 4.1 Add all UI text localization keys to ui_text.json
    - `identify_mistakes_btn`: "Identify Mistakes" button text
    - `identification_prompt`: "Select the tiles you thought were {color}"
    - `identification_done_btn`: "Done" button text
    - `identification_cancel_btn`: "Cancel" button text
    - `identification_next_color`: "Next: {color}" indicator text
    - `summary_header`: "Mistake Analysis Summary" header
    - `summary_total_mistakes`: "Total Mistakes" label
    - `summary_stroop_influenced`: "Stroop-Influenced" label
    - `summary_non_stroop`: "Other Mistakes" label
    - `legend_correct`: "Correctly identified" legend text
    - `legend_incorrect`: "Incorrectly identified" legend text
    - `legend_stroop`: "Stroop interference likely" legend text
    - Add translations for all 4 languages (zh-TW, english, spanish, vietnamese)
  - [x] 4.2 Wire up all event listeners
    - "Identify Mistakes" button click handler
    - "Done" button click handler
    - "Cancel" button click handler
    - Ensure tile selection works during identification mode
    - Integrate with existing `generatePuzzle()` to clear identification state
  - [x] 4.3 Update `clearAllSelections()` and `generatePuzzle()` functions
    - `clearAllSelections()`: Also clear identification state and visual markers
    - `generatePuzzle()`: Call identification state reset to clear previous analysis
    - Ensure answer key toggle doesn't interfere with identification mode
  - [x] 4.4 Implement keyboard accessibility for identification flow
    - Tab navigation through prompt buttons
    - Arrow keys continue to work for tile navigation
    - Enter/Space activate focused buttons
    - Escape key option to cancel identification mode
  - [x] 4.5 Test responsive behavior on mobile
    - Identification prompt fits on small screens (320px width)
    - Summary panel scrolls if needed
    - Tile markers visible at all grid sizes
    - Touch interactions work for tile selection
  - [x] 4.6 Review and fill critical test gaps only
    - Review tests from Task Groups 1-3 (approximately 12-18 tests)
    - Identify any critical end-to-end workflow gaps
    - Add maximum of 6 additional integration tests if needed
    - Focus on complete user flow: check answers -> identify mistakes -> view summary
  - [x] 4.7 Run all feature-specific tests
    - Run tests from 1.1, 2.1, 3.1, and any added in 4.6
    - Expected total: approximately 18-24 tests maximum
    - Verify all critical workflows pass
    - Do NOT run the entire application test suite

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 18-24 tests total)
- All UI text appears correctly in all 4 supported languages
- Identification flow is keyboard accessible
- Feature works on mobile devices (320px to desktop)
- New puzzle generation properly resets identification state

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Core Logic Layer** - State management, discrepancy detection, Stroop analysis algorithm
2. **Task Group 2: UI Components Layer** - Identification mode UI, prompts, guided selection flow
3. **Task Group 3: Visualization Layer** - Tile marking, legend, summary panel
4. **Task Group 4: Localization and Integration** - UI text, event wiring, accessibility, final testing

## Key Implementation Notes

### Existing Code to Leverage
- **Tile Selection**: Reuse `selectedTiles` Set and `toggleTileSelection(index)` function
- **Answer Checking**: Reference `correctAnswers` object from `checkAnswers()` function
- **Puzzle Data**: Access `currentPuzzle[index].word` and `currentPuzzle[index].inkColor`
- **Grid Position**: Use `row = Math.floor(index / currentGridSize)`, `col = index % currentGridSize`
- **Localization**: Use `getUIText(key)` pattern and extend `shared/ui_text.json`
- **Color Constants**: Use `colorsJson` for hex values, `colorLabelsJson` for localized names

### Accessibility Requirements
- All indicators must use non-color-only cues (icons, patterns, borders)
- Maintain sufficient color contrast ratios
- Support keyboard navigation throughout identification flow
- Static indicators only (no animations per spec)

### Files to Modify
- `/home/user/projects/ColorFocus/frontend/puzzle.html` - Main application file (CSS + JS)
- `/home/user/projects/ColorFocus/shared/ui_text.json` - UI text localization strings
- `/home/user/projects/ColorFocus/frontend/__tests__/` - Test files (if test infrastructure exists)

### Out of Scope (Per Spec)
- Audio feedback for mistake identification
- Animation effects for tile marking
- Backend storage of identification results
- Historical tracking across multiple puzzles
- PDF export (printable HTML view is sufficient)
