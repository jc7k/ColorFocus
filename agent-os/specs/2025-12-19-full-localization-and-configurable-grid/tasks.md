# Task Breakdown: Full UI Localization and Configurable Grid Size

## Overview
Total Tasks: 27 (across 4 task groups)

This feature adds complete UI text localization for Chinese, English, and Vietnamese languages, plus configurable grid sizes from 1x1 to 8x8 with automatic color count limiting.

## Task List

### Data Layer

#### Task Group 1: UI Translation Data
**Dependencies:** None

- [x] 1.0 Complete UI translation data layer
  - [x] 1.1 Write 3-4 focused tests for UI text loading functionality
    - Test that `ui_text.json` loads correctly at module initialization
    - Test that all required UI text keys exist for each language (chinese, english, vietnamese)
    - Test that Vietnamese text contains proper diacritical marks (e.g., accented characters)
    - Test that Language enum integration works with UI text lookup
  - [x] 1.2 Create `shared/ui_text.json` with all translatable UI strings
    - Structure mirrors `color_labels.json`: top-level keys are string identifiers, nested keys are language codes
    - Required UI text keys:
      - `page_title`: Page title text
      - `subtitle`: Subtitle instruction text
      - `task_label`: "Task:" label
      - `task_instruction`: Full task instruction template (with placeholder for language descriptor)
      - `language_label`: "Language:" control label
      - `grid_label`: "Grid:" control label
      - `colors_label`: "Colors:" control label
      - `seed_label`: "Seed:" control label
      - `match_label`: "Match %:" control label
      - `generate_btn`: "Generate" button text
      - `random_btn`: "Random" button text
      - `enter_answers_header`: "Enter Your Answers" section header
      - `check_btn`: "Check Answers" button text
      - `clear_btn`: "Clear" button text
      - `results_header`: "Results" section header
      - `answer_key_header`: "Answer Key" section header
      - `reveal_btn`: "Reveal" button text
      - `hide_btn`: "Hide" button text
      - `reveal_warning`: Warning message about revealing answers
      - `metadata_seed`: "Seed:" metadata label
      - `metadata_colors`: "Colors:" metadata label
      - `metadata_grid`: "Grid:" metadata label
      - `metadata_congruent`: "Congruent:" metadata label
      - `result_perfect`: Perfect score message
      - `result_good`: Good score message template
      - `result_needs_work`: Needs improvement message template
      - `result_colors_correct`: "Colors Correct" label
      - `result_accuracy`: "Accuracy" label
      - `result_total_off`: "Total Off By" label
      - `language_descriptor_chinese`: "Chinese character"
      - `language_descriptor_english`: "English word"
      - `language_descriptor_vietnamese`: "Vietnamese word"
    - Vietnamese translations must use proper diacritical marks
  - [x] 1.3 Create `backend/app/constants/ui_text.py` for Python UI text loading
    - Follow pattern from `color_labels.py`
    - Load JSON at module import time (not per-request)
    - Use existing `Language` enum from `color_labels.py`
    - Provide `get_ui_text(key, language)` function
    - Resolve path: `Path(__file__).parent.parent.parent.parent / "shared" / "ui_text.json"`
  - [x] 1.4 Ensure data layer tests pass
    - Run ONLY the 3-4 tests written in 1.1
    - Verify JSON structure is valid
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-4 tests written in 1.1 pass
- `ui_text.json` contains all required keys with translations for all 3 languages
- Vietnamese text uses proper diacritical marks
- Python module loads translations correctly at import time

---

### Frontend Layer

#### Task Group 2: UI Localization Implementation
**Dependencies:** Task Group 1

- [x] 2.0 Complete UI localization in frontend
  - [x] 2.1 Write 4-5 focused tests for UI localization functionality
    - Test that UI text updates when language selector changes (no page reload)
    - Test that page `<title>` tag updates to match selected language
    - Test that task instructions template properly inserts language descriptor
    - Test that result messages display correctly in each language
    - Test that metadata labels are translated correctly
  - [x] 2.2 Import and load `ui_text.json` in `puzzle.html`
    - Add ES module import similar to existing `color_labels.json` import
    - Create `getUIText(key)` helper function that returns text for `currentLanguage`
  - [x] 2.3 Replace all hardcoded English text with dynamic translations
    - Page title (h1): Use `page_title` key
    - Subtitle paragraph: Use `subtitle` key
    - Task instructions: Use `task_label`, `task_instruction`, and `language_descriptor_*` keys
    - Control labels: Use `language_label`, `grid_label`, `colors_label`, `seed_label`, `match_label` keys
    - Button text: Use `generate_btn`, `random_btn`, `check_btn`, `clear_btn`, `reveal_btn`, `hide_btn` keys
    - Section headers: Use `enter_answers_header`, `results_header`, `answer_key_header` keys
    - Reveal warning: Use `reveal_warning` key
    - Result messages: Use `result_perfect`, `result_good`, `result_needs_work` keys
    - Result labels: Use `result_colors_correct`, `result_accuracy`, `result_total_off` keys
    - Metadata labels: Use `metadata_seed`, `metadata_colors`, `metadata_grid`, `metadata_congruent` keys
  - [x] 2.4 Update page `<title>` tag dynamically on language change
    - Set document.title to translated page title
    - Update on initial load and when language selector changes
  - [x] 2.5 Extend language change event handler to update all UI text
    - Add `updateAllUIText()` function that updates all translated text elements
    - Call from language change event listener (alongside existing render calls)
    - Use safe DOM manipulation (textContent, not innerHTML with dynamic content)
  - [x] 2.6 Update `updateTaskInstructions()` function to use translations
    - Replace hardcoded "Task:" with `task_label` translation
    - Use `task_instruction` template with language descriptor interpolation
    - Get language descriptor from `language_descriptor_*` key based on `currentLanguage`
  - [x] 2.7 Update `showResults()` function to use translated messages
    - Use `result_perfect`, `result_good`, `result_needs_work` translations
    - Interpolate correct/total values into message templates
    - Use translated labels for result stats
  - [x] 2.8 Ensure UI localization tests pass
    - Run ONLY the 4-5 tests written in 2.1
    - Verify all UI text updates on language change
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-5 tests written in 2.1 pass
- All UI text elements are translated when language changes
- Page title updates dynamically
- No hardcoded English text remains in the UI
- Safe DOM manipulation used throughout (no innerHTML with user/dynamic content)

---

#### Task Group 3: Configurable Grid Size
**Dependencies:** Task Group 1

- [x] 3.0 Complete configurable grid size feature
  - [x] 3.1 Write 4-6 focused tests for grid size functionality
    - Test that grid size dropdown renders options 1x1 through 8x8
    - Test that selecting a grid size updates grid CSS `grid-template-columns`
    - Test that color count is auto-limited based on grid size (e.g., 3x3 = max 3 colors)
    - Test that puzzle generates correct number of cells for selected grid size
    - Test that font size calculation adjusts for different grid column counts
    - Test that grid size persists in localStorage (optional validation)
  - [x] 3.2 Add grid size dropdown selector to controls section
    - Position between Language and Colors dropdowns
    - Options: 1x1, 2x2, 3x3, 4x4, 5x5, 6x6, 7x7, 8x8
    - Display format: "NxN" (e.g., "4x4", "8x8")
    - Default selection: 4x4
    - Add corresponding label using translated text (`grid_label` key)
  - [x] 3.3 Add grid size state management and localStorage persistence
    - Create `currentGridSize` state variable (default: 4)
    - Load saved preference from localStorage key `colorFocusGridSize` on init
    - Save to localStorage when grid size changes
    - Add grid size change event listener
  - [x] 3.4 Implement dynamic grid CSS updates
    - Update `.puzzle-grid` element's `grid-template-columns` style
    - Use `repeat(N, 1fr)` where N is the selected grid dimension
    - Apply via inline style or CSS custom property
    - Ensure cells maintain `aspect-ratio: 1` for square cells
  - [x] 3.5 Implement automatic color count limiting
    - Calculate `maxColors = min(8, gridSize)` where gridSize is the NxN dimension
    - Update Colors dropdown to show only options 2 through maxColors
    - If current color selection exceeds new max, clamp to new max
    - Regenerate puzzle after color count adjustment
  - [x] 3.6 Update puzzle generation for variable grid sizes
    - Replace hardcoded `totalCells = 64` with `totalCells = gridSize * gridSize`
    - Update ink distribution logic in `generatePuzzle()` for variable cell counts
    - Update answer counting and validation for variable cell counts
    - Update metadata display to show dynamic grid size (e.g., "3x3", "8x8")
  - [x] 3.7 Update font size calculation for variable grid dimensions
    - Modify `calculatePuzzleFontSize()` to accept grid column count as parameter
    - Adjust cell width calculation: `cellWidth = (gridWidth - gaps) / gridSize`
    - Larger cells (smaller grids) should have proportionally larger fonts
    - Maintain language-specific multipliers (Chinese: 1.15, Vietnamese: 2.6, English: 4.2)
  - [x] 3.8 Update metadata display with translated labels and dynamic grid size
    - Use translated metadata labels from `ui_text.json`
    - Show current grid size in "Grid:" metadata value (e.g., "3x3", "8x8")
    - Update congruent count display to use dynamic total cells
  - [x] 3.9 Ensure configurable grid tests pass
    - Run ONLY the 4-6 tests written in 3.1
    - Verify grid size changes work correctly
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- Grid size dropdown displays all 8 options (1x1 through 8x8)
- Grid CSS updates dynamically when size changes
- Color count is automatically limited based on grid size
- Puzzle generates correct number of cells
- Font sizes scale appropriately for different grid sizes
- Cells remain square at all grid sizes

---

### Testing

#### Task Group 4: Test Review and Gap Analysis
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and fill critical gaps only
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 3-4 tests written by data layer (Task 1.1)
    - Review the 4-5 tests written by UI localization (Task 2.1)
    - Review the 4-6 tests written by grid size feature (Task 3.1)
    - Total existing tests: approximately 11-15 tests
  - [x] 4.2 Analyze test coverage gaps for THIS feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to this spec's feature requirements:
      - Full UI translation switching workflow
      - Grid size + color auto-limiting interaction
      - Language + grid size combined state management
    - Do NOT assess entire application test coverage
    - Prioritize end-to-end workflows over unit test gaps
  - [x] 4.3 Write up to 8 additional strategic tests maximum
    - Add maximum of 8 new tests to fill identified critical gaps
    - Focus areas:
      - Integration: Language change triggers all UI text updates including title
      - Integration: Grid size change triggers color dropdown update + puzzle regeneration
      - Edge case: 1x1 grid with 1 color (minimum configuration)
      - Edge case: 8x8 grid with 8 colors (maximum configuration)
      - State persistence: Refresh page retains language and grid size preferences
      - UI consistency: All three languages display correctly without layout breaks
    - Do NOT write comprehensive coverage for all scenarios
    - Skip performance tests and accessibility tests unless business-critical
  - [x] 4.4 Run feature-specific tests only
    - Run ONLY tests related to this spec's feature (tests from 1.1, 2.1, 3.1, and 4.3)
    - Expected total: approximately 19-23 tests maximum
    - Do NOT run the entire application test suite
    - Verify critical workflows pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 19-23 tests total)
- Critical user workflows for this feature are covered
- No more than 8 additional tests added when filling in testing gaps
- Testing focused exclusively on this spec's feature requirements

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: UI Translation Data** - Create the translation JSON file and Python loading module first, as all other groups depend on this data layer.

2. **Task Group 2: UI Localization Implementation** - Implement the frontend localization using the translation data. This can start once Task Group 1 is complete.

3. **Task Group 3: Configurable Grid Size** - Implement grid size selector and related logic. This can run in parallel with Task Group 2 after Task Group 1 is complete, as they modify different parts of the frontend.

4. **Task Group 4: Test Review and Gap Analysis** - Review all tests and fill gaps. This must wait until Task Groups 1-3 are complete.

---

## Technical Notes

### File Locations
- New file: `/home/user/projects/ColorFocus/shared/ui_text.json`
- New file: `/home/user/projects/ColorFocus/backend/app/constants/ui_text.py`
- Modified file: `/home/user/projects/ColorFocus/frontend/puzzle.html`

### Existing Patterns to Follow
- JSON structure from `shared/color_labels.json`
- Python module loading pattern from `backend/app/constants/color_labels.py`
- Language enum from `backend/app/constants/color_labels.py`
- localStorage persistence pattern from `puzzle.html` (colorFocusLanguage key)
- Safe DOM manipulation patterns already used in `puzzle.html`

### Key Constraints
- Frontend is vanilla HTML/JS with ES modules (no React/Vue)
- Deployment target is Vercel (static frontend hosting)
- No backend API changes required (frontend-only puzzle generation)
- Only square NxN grids supported (no rectangular grids)
- Maximum 8 colors regardless of grid size
