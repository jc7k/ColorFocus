# Specification: Vietnamese Language Support

## Goal
Add Vietnamese as a third supported language for color labels in the ColorFocus Stroop Puzzle, enabling users to switch between Chinese, English, and Vietnamese color word displays.

## User Stories
- As a Vietnamese-speaking user, I want to see color names in Vietnamese so that I can experience the Stroop effect in my native language.
- As any user, I want to select my preferred language from a dropdown so that I can practice with familiar or unfamiliar color words.

## Specific Requirements

**Add Vietnamese labels to shared/color_labels.json**
- Add "vietnamese" key to each color object alongside existing "chinese" and "english" keys
- Use short-form Vietnamese translations for single-character consistency with Chinese labels
- Vietnamese translations: BLUE="Xanh", ORANGE="Cam", PURPLE="Tim", BLACK="Den", CYAN="Lo", AMBER="Vang", MAGENTA="Hong", GRAY="Xam"
- Ensure proper UTF-8 encoding for Vietnamese diacritical marks (e.g., "Tim" with acute accent)

**Update backend Language enum in color_labels.py**
- Add VIETNAMESE = "vietnamese" to the Language StrEnum class
- No changes needed to _load_labels_from_json() as it dynamically loads all language keys
- No changes needed to get_color_label() function as it uses the Language enum directly

**Add language selector dropdown to puzzle.html controls**
- Add a new control-group with label "Language:" and a select element with id="language"
- Include options: Chinese (value="chinese"), English (value="english"), Vietnamese (value="vietnamese")
- Default selection should be Chinese to match current behavior
- Position the dropdown in the existing controls flex container alongside Colors, Seed, and Match % controls

**Implement language switching functionality in JavaScript**
- Create a currentLanguage state variable initialized to "chinese"
- Add event listener on the language select element to update currentLanguage and re-render
- Modify puzzle grid rendering to use colorLabelsJson[cell.word][currentLanguage] instead of hardcoded .chinese
- Modify answer input labels to use colorLabelsJson[token][currentLanguage]
- Modify answer key labels to use colorLabelsJson[token][currentLanguage]

**Persist language preference in localStorage**
- On language change, save preference: localStorage.setItem('colorFocusLanguage', currentLanguage)
- On page load, restore preference: localStorage.getItem('colorFocusLanguage') || 'chinese'
- Update select element value to match restored preference before initial generatePuzzle() call

**Update task instructions text dynamically**
- Change static "Chinese character" text to be language-aware
- Use "Chinese character" for chinese, "English word" for english, "Vietnamese word" for vietnamese
- Update instructions on language change along with puzzle re-render

**Ensure proper font rendering for Vietnamese diacritics**
- The existing system-ui font stack should support Vietnamese characters
- Test that diacritical marks (acute, grave, hook, tilde, dot below) render correctly
- Vietnamese characters should display at same visual size as Chinese characters in puzzle grid

**Maintain accessibility compliance**
- Add aria-label to language select: "Select display language"
- Ensure language dropdown is keyboard-navigable (native select behavior)
- Language changes should not disrupt screen reader announcement flow

## Visual Design
No mockups provided. Follow existing control styling patterns in puzzle.html.

## Existing Code to Leverage

**shared/color_labels.json structure**
- Currently maps color tokens to {chinese, english} label objects
- Extend pattern by adding "vietnamese" key to each object
- Frontend imports this via ES module: import colorLabelsJson from '../shared/color_labels.json'

**backend/app/constants/color_labels.py Language enum**
- StrEnum with CHINESE and ENGLISH values that map to JSON keys
- Add VIETNAMESE following same pattern
- _load_labels_from_json() will automatically pick up new language from JSON

**puzzle.html controls section (lines 358-381)**
- Existing control-group pattern with label + input/select pairs
- Copy structure for language selector dropdown
- Consistent styling with .control-group class

**puzzle.html renderAnswerInputs() and renderAnswerKey() functions**
- Both use colorLabelsJson[token].chinese for labels
- Parameterize to use currentLanguage variable instead
- Same change needed in puzzle grid cell rendering (line 535)

**puzzle.html generatePuzzle() function**
- Currently hardcodes .chinese access on colorLabelsJson
- Modify to reference currentLanguage state variable
- Call this function when language changes to re-render with new labels

## Out of Scope
- Adding additional languages beyond Vietnamese in this spec
- Translating UI text (buttons, headings, instructions) beyond color labels
- Right-to-left language support
- Language detection based on browser locale
- Backend API endpoints for language switching (frontend-only change)
- Modifying color values or adding new colors
- Changes to puzzle generation algorithm
- Mobile-specific language selector styling
- Unit tests for language switching (manual testing sufficient)
- Full-form Vietnamese translations (using short forms only)
