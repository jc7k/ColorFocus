# Specification: Counting Tiles (Interactive Tile Selection)

## Goal
Add an interactive tile selection feature to help elderly and stroke recovery users count tiles by ink color on the existing Stroop puzzle grid, with auto-fill capability to streamline answer entry.

## User Stories
- As an elderly user, I want to tap tiles to mark them as "counted" so that I can keep track while counting tiles of a specific ink color
- As a stroke recovery patient, I want to tap a color swatch to auto-fill my count so that I can avoid manual number entry errors

## Specific Requirements

**Tile Selection Visual State**
- Tiles toggle between selected and unselected states on click/tap
- Selected tiles display a pronounced inset/depression effect using CSS box-shadow inset
- Use transform to shift tile slightly down/right to reinforce "pressed" appearance
- Maintain existing hover effect (scale 1.08) for unselected tiles only
- Selected state must be clearly visible to users with various visual abilities

**Tile Selection Interaction**
- Click/tap toggles selection state (first click selects, second click deselects)
- Selection state managed via JavaScript Set or array of tile indices
- Tile elements need data attribute or index tracking for selection management
- Touch targets already meet 44x44px minimum via existing puzzle-cell sizing

**Keyboard Navigation**
- Arrow keys (up/down/left/right) move focus between tiles in grid pattern
- Spacebar toggles selection on currently focused tile
- Focus state must be visually distinct from selection state
- Tab key enters/exits the tile grid focus context
- Implement roving tabindex pattern for efficient keyboard navigation within grid

**Auto-Fill from Color Swatches**
- Tapping/clicking a color swatch in the answer section counts ALL currently selected tiles
- Auto-fill populates the count number into that color's input field
- No validation or color-matching at auto-fill time (user is responsible for selecting correct tiles)
- Color swatch elements need click handler added (currently passive display elements)

**Clear All Selections Button**
- Add "Clear Selections" button in the puzzle controls area
- Button clears all tile selections without affecting answer inputs
- Use secondary button styling consistent with existing "Clear" answers button
- Button label should be localized via ui_text.json

**Auto-Clear on New Puzzle**
- Tile selections automatically clear when generatePuzzle() is called
- Applies to both "Generate" and "Random" button actions
- Reset selection state at start of generatePuzzle function alongside other state resets

**Optional Sound Effect**
- Play a brief, pleasant sound when tile is selected (not on deselection)
- Sound effect setting stored in LocalStorage (key: colorFocusSoundEnabled)
- Default sound setting is OFF (opt-in for accessibility)
- Add sound toggle control in the controls section
- Use Web Audio API or HTML5 Audio element for sound playback

**Localization Support**
- Add new UI text keys to ui_text.json for: clear_selections_btn, sound_toggle_label
- Follow existing pattern of translations for zh-TW, english, spanish, vietnamese
- Update updateAllUIText() function to handle new translatable elements

## Existing Code to Leverage

**Puzzle Cell Rendering (puzzle.html lines 1098-1108)**
- renderPuzzleDisplay() creates puzzle-cell div elements in a forEach loop
- Add selection state class and click handler during cell creation
- Cell elements can store index via data-index attribute for selection tracking

**Answer Input Grid (puzzle.html lines 1267-1319)**
- renderAnswerInputs() creates answer-item elements with color swatches
- Color swatch elements (.color-swatch) can receive click handlers for auto-fill
- Input fields already have IDs like answer-${token} for programmatic value setting

**State Management Pattern (puzzle.html lines 801-813)**
- Existing state variables follow let declarations at module scope
- LocalStorage pattern: localStorage.getItem/setItem with validation functions
- Add selectedTiles Set and soundEnabled boolean following same pattern

**Generate Puzzle Reset Pattern (puzzle.html lines 1167-1176)**
- generatePuzzle() resets hasChecked, answerKeyRevealed, and UI states at start
- Add selectedTiles.clear() and tile UI reset in same location

**Button Styling (puzzle.html lines 77-105)**
- Existing button and button.secondary CSS classes for consistent styling
- Use button.secondary for "Clear Selections" button

## Out of Scope
- Count badge showing "X selected" overlaid on individual tiles
- Undo/redo functionality for individual tile selections
- Color-matching validation (only counting tiles that match the target swatch color)
- Smart counting that filters selected tiles by their actual ink color
- Any modifications to the existing "Check Answers" validation logic
- Haptic feedback on mobile devices
- Animation for selection state transitions beyond the inset effect
- Multi-select gestures (drag to select multiple tiles)
- Selection persistence across browser sessions (selections are ephemeral)
- Sound customization options (volume, different sound choices)
