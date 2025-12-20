# Task Breakdown: Vietnamese Language Support

## Overview
Total Tasks: 18

This feature adds Vietnamese as a third supported language for color labels in the ColorFocus Stroop Puzzle, enabling users to switch between Chinese, English, and Vietnamese color word displays.

## Task List

### Data Layer

#### Task Group 1: Shared Data and Backend Updates
**Dependencies:** None

- [x] 1.0 Complete data layer updates
  - [x] 1.1 Write 3-4 focused tests for Vietnamese language support
    - Test that `shared/color_labels.json` contains vietnamese key for all 8 colors
    - Test that Vietnamese labels use proper UTF-8 encoding (diacritical marks)
    - Test that backend `Language` enum includes VIETNAMESE value
    - Test that `get_color_label()` works with `Language.VIETNAMESE`
  - [x] 1.2 Update `shared/color_labels.json` with Vietnamese translations
    - Add "vietnamese" key to each color object alongside "chinese" and "english"
    - Vietnamese translations: BLUE="Xanh", ORANGE="Cam", PURPLE="Tím", BLACK="Đen", CYAN="Lơ", AMBER="Vàng", MAGENTA="Hồng", GRAY="Xám"
    - Ensure proper UTF-8 encoding for Vietnamese diacritical marks
  - [x] 1.3 Update backend `Language` enum in `backend/app/constants/color_labels.py`
    - Add `VIETNAMESE = "vietnamese"` to the `Language` StrEnum class
    - Update docstring to document Vietnamese support
  - [x] 1.4 Ensure data layer tests pass
    - Run ONLY the 3-4 tests written in 1.1
    - Verify JSON structure is valid
    - Verify backend can load and use Vietnamese labels

**Acceptance Criteria:**
- The 3-4 tests written in 1.1 pass
- `shared/color_labels.json` contains Vietnamese labels for all 8 colors
- Backend `Language.VIETNAMESE` enum value exists and works with `get_color_label()`
- UTF-8 diacritical marks render correctly

---

### Frontend Layer

#### Task Group 2: Language Selector UI Component
**Dependencies:** Task Group 1

- [x] 2.0 Complete language selector UI
  - [x] 2.1 Write 2-3 focused tests for language selector functionality
    - Test that language dropdown renders with 3 options (Chinese, English, Vietnamese)
    - Test that language dropdown has proper aria-label for accessibility
    - Test that language change event triggers re-render of puzzle grid
  - [x] 2.2 Add language selector dropdown to puzzle.html controls section
    - Add new control-group with label "Language:" and select element with id="language"
    - Include options: Chinese (value="chinese"), English (value="english"), Vietnamese (value="vietnamese")
    - Default selection should be Chinese to match current behavior
    - Follow existing control-group styling pattern
  - [x] 2.3 Implement accessibility attributes for language selector
    - Add `aria-label="Select display language"` to the select element
    - Ensure keyboard navigation works (tab focus, arrow key selection)
  - [x] 2.4 Ensure language selector UI tests pass
    - Run ONLY the 2-3 tests written in 2.1
    - Verify dropdown renders correctly
    - Verify accessibility attributes are present

**Acceptance Criteria:**
- The 2-3 tests written in 2.1 pass
- Language dropdown appears in controls section
- Dropdown has 3 options: Chinese, English, Vietnamese
- Dropdown is keyboard-navigable with proper ARIA label

---

#### Task Group 3: Language Switching Functionality
**Dependencies:** Task Group 2

- [x] 3.0 Complete language switching logic
  - [x] 3.1 Write 2-3 focused tests for language switching behavior
    - Test that selecting a language updates the puzzle grid cell text
    - Test that answer input labels update to match selected language
    - Test that answer key labels update to match selected language
  - [x] 3.2 Create currentLanguage state variable and event listener
    - Add `let currentLanguage = 'chinese'` state variable in JavaScript
    - Add event listener on language select element to update currentLanguage
    - Call `generatePuzzle()` or render functions when language changes
  - [x] 3.3 Modify puzzle grid rendering to use selected language
    - Update cell text rendering: `colorLabelsJson[cell.word][currentLanguage]`
    - Ensure grid re-renders when language changes without regenerating puzzle data
  - [x] 3.4 Modify answer input labels to use selected language
    - Update `renderAnswerInputs()` to use `colorLabelsJson[token][currentLanguage]`
  - [x] 3.5 Modify answer key labels to use selected language
    - Update `renderAnswerKey()` to use `colorLabelsJson[token][currentLanguage]`
  - [x] 3.6 Ensure language switching tests pass
    - Run ONLY the 2-3 tests written in 3.1
    - Verify all display elements update when language changes

**Acceptance Criteria:**
- The 2-3 tests written in 3.1 pass
- Puzzle grid displays color words in selected language
- Answer input labels display in selected language
- Answer key labels display in selected language
- Switching language updates all displays without losing puzzle state

---

#### Task Group 4: Language Persistence and Dynamic Text
**Dependencies:** Task Group 3

- [x] 4.0 Complete persistence and dynamic text updates
  - [x] 4.1 Write 2 focused tests for persistence and dynamic text
    - Test that language preference saves to localStorage on change
    - Test that language preference loads from localStorage on page load
  - [x] 4.2 Implement localStorage persistence for language preference
    - On language change: `localStorage.setItem('colorFocusLanguage', currentLanguage)`
    - On page load: `localStorage.getItem('colorFocusLanguage') || 'chinese'`
    - Set select element value to match loaded preference
  - [x] 4.3 Update task instructions text to be language-aware
    - Change static "Chinese character" text in `.task-instructions` div
    - Use "Chinese character" for chinese, "English word" for english, "Vietnamese word" for vietnamese
    - Create helper function `getLanguageDescriptor(lang)` to return appropriate text
  - [x] 4.4 Ensure persistence and dynamic text tests pass
    - Run ONLY the 2 tests written in 4.1
    - Verify localStorage read/write works correctly
    - Verify task instructions update with language selection

**Acceptance Criteria:**
- The 2 tests written in 4.1 pass
- Language preference persists across page reloads
- Task instructions text updates to match selected language
- Default language is Chinese if no preference is stored

---

### Testing

#### Task Group 5: Test Review and Gap Analysis
**Dependencies:** Task Groups 1-4

- [x] 5.0 Review existing tests and fill critical gaps only
  - [x] 5.1 Review tests from Task Groups 1-4
    - Review the 3-4 tests written by data layer (Task 1.1)
    - Review the 2-3 tests written by UI component (Task 2.1)
    - Review the 2-3 tests written by language switching (Task 3.1)
    - Review the 2 tests written by persistence (Task 4.1)
    - Total existing tests: approximately 9-12 tests
  - [x] 5.2 Analyze test coverage gaps for Vietnamese language feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to this spec's feature requirements
    - Prioritize end-to-end workflow: select Vietnamese -> see Vietnamese labels -> check answers
  - [x] 5.3 Write up to 5 additional strategic tests if needed
    - Add maximum of 5 new tests to fill identified critical gaps
    - Focus on integration: language selection affects all UI elements consistently
    - Skip edge cases, performance tests unless business-critical
  - [x] 5.4 Run feature-specific tests only
    - Run ONLY tests related to Vietnamese language support feature
    - Expected total: approximately 12-17 tests maximum
    - Verify all critical workflows pass

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 12-17 tests total)
- Critical user workflow covered: select Vietnamese -> puzzle displays Vietnamese -> answers work correctly
- No more than 5 additional tests added when filling gaps
- Testing focused exclusively on Vietnamese language support feature

---

## Execution Order

Recommended implementation sequence:

1. **Data Layer (Task Group 1)** - Add Vietnamese translations to shared JSON and update backend enum
2. **Language Selector UI (Task Group 2)** - Add dropdown UI component with accessibility
3. **Language Switching Logic (Task Group 3)** - Implement JavaScript state management and rendering updates
4. **Persistence and Dynamic Text (Task Group 4)** - Add localStorage persistence and update instructions text
5. **Test Review (Task Group 5)** - Review coverage and fill critical gaps

---

## Files to Modify

| File | Task Group | Changes |
|------|------------|---------|
| `shared/color_labels.json` | 1 | Add "vietnamese" key to all 8 color objects |
| `backend/app/constants/color_labels.py` | 1 | Add `VIETNAMESE = "vietnamese"` to Language enum |
| `frontend/puzzle.html` | 2, 3, 4 | Add language dropdown, update JS rendering logic, add localStorage |
| `tests/test_vietnamese_language.py` (new) | 1, 5 | New test file for Vietnamese language feature |

---

## Notes

- Vietnamese translations specified in spec: BLUE="Xanh", ORANGE="Cam", PURPLE="Tím", BLACK="Đen", CYAN="Lơ", AMBER="Vàng", MAGENTA="Hồng", GRAY="Xám"
- UTF-8 encoding is critical for proper display of Vietnamese diacritical marks
- The existing puzzle.html uses ES modules with JSON imports, which will automatically pick up the updated color_labels.json
- Language switching should not regenerate the puzzle (seed stays the same), only re-render the display text
