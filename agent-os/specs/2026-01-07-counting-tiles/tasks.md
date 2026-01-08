# Task Breakdown: Counting Tiles (Interactive Tile Selection)

## Overview
Total Tasks: 4 Task Groups with 28 Sub-tasks

This feature adds interactive tile selection to help elderly and stroke recovery users count tiles by ink color on the existing Stroop puzzle grid, with auto-fill capability to streamline answer entry.

## Task List

### Core Selection Logic

#### Task Group 1: Selection State Management and Tile Interaction
**Dependencies:** None

- [x] 1.0 Complete selection state management and tile interaction
  - [x] 1.1 Write 4-6 focused tests for tile selection logic
    - Test that selectedTiles Set initializes empty
    - Test that clicking a tile adds its index to selectedTiles
    - Test that clicking a selected tile removes it from selectedTiles (toggle behavior)
    - Test that selectedTiles.clear() empties all selections
    - Test that generatePuzzle() clears all selections
  - [x] 1.2 Add selection state variables to module scope (lines ~801-813 pattern)
    - Add `let selectedTiles = new Set()` for tracking selected tile indices
    - Add `let soundEnabled = false` with LocalStorage validation pattern
    - Follow existing state variable patterns: `validateSoundEnabled()` function
  - [x] 1.3 Modify renderPuzzleDisplay() to support selection (lines ~1098-1108)
    - Add `data-index` attribute to each puzzle-cell div for selection tracking
    - Add click handler to each cell that calls `toggleTileSelection(index)`
    - Apply 'selected' class based on `selectedTiles.has(index)`
  - [x] 1.4 Implement toggleTileSelection(index) function
    - If index in selectedTiles, remove it; otherwise add it
    - Update the specific tile's class (add/remove 'selected')
    - Play selection sound if soundEnabled is true and tile is being selected
  - [x] 1.5 Add selection clearing to generatePuzzle() (lines ~1167-1176)
    - Add `selectedTiles.clear()` at start of generatePuzzle() function
    - Ensure UI reflects cleared state when puzzle regenerates
  - [x] 1.6 Ensure selection logic tests pass
    - Run ONLY the 4-6 tests written in 1.1
    - Verify toggle behavior works correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 1.1 pass
- Clicking tiles toggles their selection state
- Selection state persists until manually cleared or new puzzle generated
- generatePuzzle() resets all selections

### Visual Styling

#### Task Group 2: Selection Visual States and CSS
**Dependencies:** Task Group 1

- [x] 2.0 Complete selection visual styling
  - [x] 2.1 Write 2-4 focused tests for visual state classes
    - Test that selected tiles have 'selected' class applied
    - Test that unselected tiles do not have 'selected' class
    - Test that focus state is visually distinct from selection state
  - [x] 2.2 Add CSS for .puzzle-cell.selected state (after lines ~120-130)
    - Use `box-shadow: inset 4px 4px 8px rgba(0,0,0,0.3)` for pronounced inset effect
    - Use `transform: translate(2px, 2px)` to reinforce "pressed" appearance
    - Remove hover scale effect for selected tiles: `.puzzle-cell.selected:hover { transform: translate(2px, 2px); }`
  - [x] 2.3 Add CSS for .puzzle-cell:focus state (keyboard navigation)
    - Add visible focus outline: `outline: 3px solid #2563eb; outline-offset: 2px;`
    - Ensure focus is visually distinct from selection (outline vs inset shadow)
  - [x] 2.4 Add CSS for combined .puzzle-cell.selected:focus state
    - Maintain both inset shadow and focus outline simultaneously
    - Ensure elderly/low-vision users can distinguish both states
  - [x] 2.5 Ensure visual state tests pass
    - Run ONLY the 2-4 tests written in 2.1
    - Verify visual states render correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 2.1 pass
- Selected tiles show pronounced inset/depression effect
- Focus state is clearly visible and distinct from selection
- Hover effect only applies to unselected tiles

### Keyboard Navigation and Accessibility

#### Task Group 3: Keyboard Navigation and Auto-Fill
**Dependencies:** Task Groups 1-2

- [x] 3.0 Complete keyboard navigation and auto-fill functionality
  - [x] 3.1 Write 4-6 focused tests for keyboard and auto-fill behavior
    - Test that arrow keys move focus between grid tiles
    - Test that spacebar toggles selection on focused tile
    - Test that Tab key enters/exits grid focus context
    - Test that clicking color swatch fills input with selectedTiles.size
    - Test that auto-fill counts ALL selected tiles regardless of color
  - [x] 3.2 Implement roving tabindex pattern for puzzle grid
    - Add `tabindex="0"` to first tile, `tabindex="-1"` to others
    - Add `role="grid"` to puzzle-grid container
    - Add `role="gridcell"` to each puzzle-cell
  - [x] 3.3 Add keyboard event handler for grid navigation
    - ArrowUp/Down/Left/Right moves focus based on grid dimensions
    - Spacebar toggles selection on currently focused tile
    - Update tabindex values as focus moves (roving tabindex)
    - Handle edge cases (first row up, last row down, etc.)
  - [x] 3.4 Modify renderAnswerInputs() for auto-fill (lines ~1267-1319)
    - Add click handler to .color-swatch elements
    - On swatch click: get count from `selectedTiles.size`
    - Set corresponding input value: `document.getElementById('answer-' + token).value = count`
    - Add `cursor: pointer` style to .color-swatch
  - [x] 3.5 Add ARIA attributes for screen reader support
    - Add `aria-pressed="true/false"` to tiles based on selection state
    - Update aria-pressed when selection toggles
    - Add `aria-label` to color swatches: "Auto-fill with selected tile count"
  - [x] 3.6 Ensure keyboard and auto-fill tests pass
    - Run ONLY the 4-6 tests written in 3.1
    - Verify keyboard navigation works in all grid sizes
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- Arrow keys navigate between tiles in grid pattern
- Spacebar toggles tile selection
- Tab enters/exits grid focus
- Clicking color swatch auto-fills count of all selected tiles

### UI Controls and Localization

#### Task Group 4: Clear Button, Sound Toggle, and Localization
**Dependencies:** Task Groups 1-3

- [x] 4.0 Complete UI controls and localization
  - [x] 4.1 Write 3-5 focused tests for UI controls and localization
    - Test that "Clear Selections" button clears all tile selections
    - Test that sound toggle updates soundEnabled state and LocalStorage
    - Test that new UI text keys render correctly in all 4 languages
  - [x] 4.2 Add new UI text keys to ui_text.json
    - Add `clear_selections_btn` with translations: zh-TW ("清除選擇"), english ("Clear Selections"), spanish ("Borrar Selecciones"), vietnamese ("Xoa lua chon")
    - Add `sound_toggle_label` with translations: zh-TW ("選擇音效"), english ("Selection Sound"), spanish ("Sonido de Seleccion"), vietnamese ("Am thanh chon")
  - [x] 4.3 Add "Clear Selections" button to puzzle controls area
    - Add button after existing controls in puzzle-container
    - Use `class="secondary"` for consistent styling with "Clear" answers button
    - Add `id="clearSelectionsBtn"` for event binding
    - Add `data-i18n="clear_selections_btn"` for localization
  - [x] 4.4 Implement clearAllSelections() function
    - Call `selectedTiles.clear()`
    - Remove 'selected' class from all .puzzle-cell elements
    - Bind to clearSelectionsBtn click event
  - [x] 4.5 Add sound toggle control to controls section
    - Add checkbox input with label for sound toggle
    - Use `id="soundToggle"` and `data-i18n` attribute
    - Style consistently with existing control layout
  - [x] 4.6 Implement sound toggle functionality
    - Load initial state from LocalStorage key: `colorFocusSoundEnabled`
    - Save preference on toggle change
    - Default to OFF (unchecked) for accessibility
  - [x] 4.7 Implement selection sound playback
    - Create short, pleasant sound using Web Audio API or HTML5 Audio
    - Play only on tile selection (not deselection)
    - Respect soundEnabled state before playing
  - [x] 4.8 Update updateAllUIText() function for new translatable elements
    - Add handling for clearSelectionsBtn text
    - Add handling for soundToggle label text
  - [x] 4.9 Ensure UI controls and localization tests pass
    - Run ONLY the 3-5 tests written in 4.1
    - Verify all 4 languages display correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-5 tests written in 4.1 pass
- "Clear Selections" button clears all tile selections without affecting answer inputs
- Sound toggle persists preference in LocalStorage
- Sound plays only when enabled and tile is selected
- All new text properly localized in zh-TW, English, Spanish, Vietnamese

### Testing

#### Task Group 5: Test Review and Integration Verification
**Dependencies:** Task Groups 1-4

- [x] 5.0 Review existing tests and verify feature integration
  - [x] 5.1 Review tests from Task Groups 1-4
    - Review the 9 tests from Task Group 1 (selection logic) in tile-selection.test.ts
    - Review the 4 tests from Task Group 2 (visual states) in tile-visual-states.test.ts
    - Review the 11 tests from Task Group 3 (keyboard/auto-fill) in keyboard-navigation.test.ts
    - Review the 9 tests from Task Group 4 (UI controls) in ui-controls-localization.test.ts
    - Total existing tests: 33 tests for counting tiles feature
  - [x] 5.2 Analyze test coverage gaps for counting tiles feature only
    - Identified gaps: end-to-end workflows, edge cases (all tiles selected, clear then auto-fill)
    - Focus ONLY on gaps related to this spec's feature requirements
    - Prioritize end-to-end workflows: select tiles -> tap swatch -> verify count
  - [x] 5.3 Write up to 6 additional strategic tests if needed
    - Added 6 new integration tests in counting-tiles-integration.test.ts
    - Focus on integration: full workflow from tile selection to auto-fill
    - Test edge cases: selecting all tiles, empty selection auto-fill, generatePuzzle clearing
  - [x] 5.4 Run feature-specific tests only
    - Run ONLY tests related to counting tiles feature
    - Total: 39 tests (33 original + 6 integration tests)
    - All critical workflows pass
    - Feature integrates smoothly with existing puzzle functionality

**Acceptance Criteria:**
- All feature-specific tests pass (39 tests total)
- End-to-end workflow works: select tiles, tap swatch, count fills input
- No more than 6 additional tests added when filling gaps (exactly 6 added)
- Feature integrates smoothly with existing puzzle functionality

## Execution Order

Recommended implementation sequence:
1. **Task Group 1: Selection State Management** - Foundation for all other functionality
2. **Task Group 2: Visual Styling** - Make selection visible to users
3. **Task Group 3: Keyboard Navigation and Auto-Fill** - Core accessibility and convenience features
4. **Task Group 4: UI Controls and Localization** - Polish with clear button, sound, and translations
5. **Task Group 5: Test Review** - Verify complete integration

## Technical Notes

### Files to Modify
- `/home/user/projects/ColorFocus/frontend/puzzle.html` - Main application (CSS, JS, HTML)
- `/home/user/projects/ColorFocus/shared/ui_text.json` - New localization keys

### Existing Patterns to Follow
- State variables at module scope (lines ~801-813)
- LocalStorage get/set with validation functions
- Button styling: `.secondary` class for secondary actions
- Localization: `data-i18n` attributes and `getUIText()` function
- Puzzle reset pattern in `generatePuzzle()` (lines ~1167-1176)

### Key Implementation Details
- Selection state: JavaScript Set of tile indices
- Sound storage key: `colorFocusSoundEnabled`
- Default sound: OFF (opt-in for accessibility)
- Touch targets: Already meet 44x44px via existing puzzle-cell sizing
- Roving tabindex: First tile tabindex="0", others tabindex="-1"
