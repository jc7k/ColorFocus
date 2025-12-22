# Task Breakdown: Spanish Language Support

## Overview
Total Tasks: 16

This feature adds Spanish as a fourth supported language for ColorFocus, including color labels and full UI text localization for all 40+ UI strings, following the established Vietnamese implementation pattern.

## Task List

### Data Layer

#### Task Group 1: Shared JSON Data Updates
**Dependencies:** None

- [x] 1.0 Complete shared data layer updates
  - [x] 1.1 Write 3-4 focused tests for Spanish language data
    - Test that `shared/color_labels.json` contains "spanish" key for all 8 colors
    - Test that Spanish color labels use expected values (AZUL, NARANJA, MORADO, NEGRO, CIAN, AMBAR, MAGENTA, GRIS)
    - Test that `shared/ui_text.json` contains "spanish" key for all 40+ UI text entries
    - Test that `language_descriptor_spanish` entry exists with translations in all four languages
  - [x] 1.2 Update `shared/color_labels.json` with Spanish translations
    - Add "spanish" key to each of the 8 color objects alongside existing "chinese", "english", and "vietnamese" keys
    - Spanish translations: BLUE="AZUL", ORANGE="NARANJA", PURPLE="MORADO", BLACK="NEGRO", CYAN="CIAN", AMBER="AMBAR", MAGENTA="MAGENTA", GRAY="GRIS"
    - Maintain UTF-8 encoding for potential diacritics
  - [x] 1.3 Update `shared/ui_text.json` with Spanish translations
    - Add "spanish" key to all 40+ existing UI text entries
    - Translations for page title, subtitle, task instructions, control labels
    - Translations for button text: Generate, Random, Check Answers, Clear, Reveal, Hide
    - Translations for section headers: Enter Your Answers, Results, Answer Key
    - Translations for result messages: perfect score, good job, needs work
    - Translations for metadata labels: Seed, Colors, Grid, Congruent
    - Translations for difficulty levels: Accessible, Standard, Advanced, Custom
    - Translations for spacing options: Compact, Normal, Relaxed, Spacious
    - Translations for warning messages
  - [x] 1.4 Add `language_descriptor_spanish` entry to `shared/ui_text.json`
    - Add translations for all four languages:
      - chinese: "西班牙语单词"
      - english: "Spanish word"
      - vietnamese: "tu tieng Tay Ban Nha"
      - spanish: "palabra en espanol"
  - [x] 1.5 Ensure data layer tests pass
    - Run ONLY the 3-4 tests written in 1.1
    - Verify JSON structure is valid for both files
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-4 tests written in 1.1 pass
- `shared/color_labels.json` contains Spanish labels for all 8 colors
- `shared/ui_text.json` contains Spanish translations for all 40+ UI text entries
- `language_descriptor_spanish` key exists with all four language translations
- JSON files remain valid and properly formatted

---

### Backend Layer

#### Task Group 2: Backend Language Enum Update
**Dependencies:** Task Group 1

- [x] 2.0 Complete backend updates
  - [x] 2.1 Write 2-3 focused tests for backend Spanish support
    - Test that `Language` enum includes SPANISH value
    - Test that `Language.SPANISH.value` equals "spanish"
    - Test that `get_color_label()` works with `Language.SPANISH` for all 8 colors
  - [x] 2.2 Update `backend/app/constants/color_labels.py` Language enum
    - Add `SPANISH = "spanish"` to the `Language` StrEnum class
    - Update docstring to include Spanish in the supported languages list
    - No changes needed to `_load_labels_from_json()` as it dynamically loads all language keys from JSON
  - [x] 2.3 Ensure backend tests pass
    - Run ONLY the 2-3 tests written in 2.1
    - Verify Language enum works correctly with Spanish
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-3 tests written in 2.1 pass
- `Language.SPANISH` enum value exists and equals "spanish"
- `get_color_label()` returns correct Spanish labels for all color tokens
- Backend module loads without errors

---

### Frontend Layer

#### Task Group 3: Frontend Language Support
**Dependencies:** Task Groups 1-2

- [x] 3.0 Complete frontend updates
  - [x] 3.1 Write 3-4 focused tests for frontend Spanish support
    - Test that language dropdown includes Spanish option with value "spanish"
    - Test that VALID_LANGUAGES array includes "spanish"
    - Test that widthMultipliers object includes "spanish" entry
    - Test that selecting Spanish updates puzzle grid cell text to Spanish labels
  - [x] 3.2 Add Spanish option to language dropdown in `frontend/puzzle.html`
    - Add `<option value="spanish">Spanish</option>` to the language select element
    - Position after Vietnamese option to maintain alphabetical order by language name
  - [x] 3.3 Add "spanish" to VALID_LANGUAGES array in `frontend/puzzle.html`
    - Update: `const VALID_LANGUAGES = ['chinese', 'english', 'vietnamese', 'spanish'];`
    - Existing `validateLanguage()` function will automatically support the new language value
  - [x] 3.4 Add Spanish font width multiplier to `calculatePuzzleFontSize()` function
    - Add spanish entry to widthMultipliers object: `spanish: 4.2`
    - Spanish words are similar length to English (max 7 chars: NARANJA, MAGENTA)
    - Add spanish entry to maxFontSizes objects (same values as English: 14 mobile, 16 desktop)
  - [x] 3.5 Ensure frontend tests pass
    - Run ONLY the 3-4 tests written in 3.1
    - Verify language dropdown renders with 4 options
    - Verify Spanish selection updates all display elements
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 3-4 tests written in 3.1 pass
- Language dropdown includes Spanish as fourth option
- VALID_LANGUAGES array includes "spanish"
- Font sizing works correctly for Spanish text (similar to English)
- Selecting Spanish updates puzzle grid, answer labels, and answer key to Spanish

---

### Testing

#### Task Group 4: Test Review and Gap Analysis
**Dependencies:** Task Groups 1-3

- [x] 4.0 Review existing tests and fill critical gaps only
  - [x] 4.1 Review tests from Task Groups 1-3
    - Review the 3-4 tests written by data layer (Task 1.1)
    - Review the 2-3 tests written by backend layer (Task 2.1)
    - Review the 3-4 tests written by frontend layer (Task 3.1)
    - Total existing tests: approximately 8-11 tests
  - [x] 4.2 Analyze test coverage gaps for Spanish language feature only
    - Identify critical user workflows that lack test coverage
    - Focus ONLY on gaps related to this spec's feature requirements
    - Prioritize end-to-end workflow: select Spanish -> see Spanish labels -> check answers
    - Do NOT assess entire application test coverage
  - [x] 4.3 Write up to 5 additional strategic tests if needed
    - Add maximum of 5 new tests to fill identified critical gaps
    - Focus on integration: Spanish selection affects all UI elements consistently
    - Test language switching between all four languages works correctly
    - Test language preference persists via localStorage for Spanish
    - Skip edge cases, performance tests unless business-critical
  - [x] 4.4 Run feature-specific tests only
    - Run ONLY tests related to Spanish language support feature
    - Expected total: approximately 13-16 tests maximum
    - Verify all critical workflows pass
    - Do NOT run the entire application test suite

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 13-16 tests total)
- Critical user workflow covered: select Spanish -> puzzle displays Spanish -> answers work correctly
- No more than 5 additional tests added when filling gaps
- Testing focused exclusively on Spanish language support feature

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Shared JSON Data Updates** - Add Spanish translations to both `color_labels.json` and `ui_text.json` files first, as all other groups depend on this data layer.

2. **Task Group 2: Backend Language Enum Update** - Add SPANISH to the Language enum in `color_labels.py`. This depends on Task Group 1 being complete.

3. **Task Group 3: Frontend Language Support** - Add Spanish option to the language dropdown, update VALID_LANGUAGES array, and add font width multiplier. This depends on Task Groups 1-2 being complete.

4. **Task Group 4: Test Review and Gap Analysis** - Review all tests and fill gaps. This must wait until Task Groups 1-3 are complete.

---

## Files to Modify

| File | Task Group | Changes |
|------|------------|---------|
| `shared/color_labels.json` | 1 | Add "spanish" key to all 8 color objects |
| `shared/ui_text.json` | 1 | Add "spanish" key to all 40+ UI text entries, add `language_descriptor_spanish` |
| `backend/app/constants/color_labels.py` | 2 | Add `SPANISH = "spanish"` to Language enum, update docstring |
| `frontend/puzzle.html` | 3 | Add Spanish dropdown option, add to VALID_LANGUAGES, add to widthMultipliers |
| `tests/test_spanish_language.py` (new) | 1, 2, 3, 4 | New test file for Spanish language feature |

---

## Spanish Translation Reference

### Color Labels

| Color Token | English | Spanish |
|-------------|---------|---------|
| BLUE | BLUE | AZUL |
| ORANGE | ORANGE | NARANJA |
| PURPLE | PURPLE | MORADO |
| BLACK | BLACK | NEGRO |
| CYAN | CYAN | CIAN |
| AMBER | AMBER | AMBAR |
| MAGENTA | MAGENTA | MAGENTA |
| GRAY | GRAY | GRIS |

**Notes:**
- Maximum word length is 7 characters (NARANJA, MAGENTA)
- All words are commonly understood and appropriate for elderly/stroke patient users
- No abbreviations or truncated words used

### UI Text Categories to Translate

1. **Page Elements:** page_title, subtitle
2. **Task Instructions:** task_label, task_instruction, language_descriptor_spanish
3. **Control Labels:** language_label, grid_label, colors_label, seed_label, match_label, difficulty_label, spacing_label
4. **Buttons:** generate_btn, random_btn, check_btn, clear_btn, reveal_btn, hide_btn
5. **Section Headers:** enter_answers_header, results_header, answer_key_header
6. **Results:** result_perfect, result_good, result_needs_work, result_colors_correct, result_accuracy, result_total_off
7. **Metadata:** metadata_seed, metadata_colors, metadata_grid, metadata_congruent
8. **Difficulty Levels:** difficulty_accessible, difficulty_standard, difficulty_advanced, difficulty_custom
9. **Spacing Options:** spacing_compact, spacing_normal, spacing_relaxed, spacing_spacious
10. **Warnings:** reveal_warning

---

## Technical Notes

- Spanish uses standard Latin alphabet requiring no special font considerations
- Existing system-ui font stack supports Spanish characters including accented vowels
- Existing high-contrast color scheme works for Spanish text
- Current minimum font size thresholds remain appropriate
- Spanish text direction is left-to-right (same as existing languages)
- No backend API endpoint changes required
- Deployment target remains Vercel (no server-side changes needed)
