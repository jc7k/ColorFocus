# Spec Requirements: Spanish Language Support

## Initial Description
Add Spanish as a fourth supported language for ColorFocus, following the same pattern established for Vietnamese language support. This includes both color labels and full UI text localization for all 30+ UI strings.

## Requirements Discussion

### First Round Questions

**Q1:** Which language should be added?
**Answer:** Spanish

**Q2:** For the Spanish color labels, should we use commonly understood color words, or do you have specific regional preferences (e.g., Latin American Spanish vs. Castilian Spanish)?
**Answer:** Use commonly understood color words

**Q3:** Does Spanish require any special text direction or layout considerations?
**Answer:** N/A - Spanish is left-to-right like existing languages (English, Vietnamese)

**Q4:** For typography, should we use any specific font considerations for Spanish, or continue with the current sans-serif approach?
**Answer:** Recommend for best UI/UX and accessibility - users are likely stroke patients and elderly

**Q5:** Spanish words tend to be longer than English (e.g., "ANARANJADO" for orange vs "ORANGE"). How should we handle potential overflow in grid cells?
**Answer:** Need balance - user must recognize word even when truncated/abbreviated. Consider word wrapping as option. Will iterate until it looks right.

**Q6:** Should this include full UI localization (all 30+ UI strings) or just color labels?
**Answer:** Full localization (color labels + all 30+ UI strings)

**Q7:** Should we follow the exact same pattern as Vietnamese implementation?
**Answer:** Yes - follow the exact same pattern used for Vietnamese

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Vietnamese Language Support - Path: `/home/user/projects/ColorFocus/agent-os/specs/2025-12-18-vietnamese-language-support/`
- Feature: Full Localization - Path: `/home/user/projects/ColorFocus/agent-os/specs/2025-12-19-full-localization-and-configurable-grid/`
- Components to potentially reuse: Existing JSON translation structure in `shared/color_labels.json` and `shared/ui_text.json`
- Backend logic to reference: `backend/app/constants/color_labels.py` with Language enum, `backend/app/constants/ui_text.py`

### Follow-up Questions

No follow-up questions needed - answers were comprehensive and clear.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A - No visuals to analyze.

## Requirements Summary

### Functional Requirements

**Spanish Color Labels:**
Add Spanish translations for all 8 canonical colors to `shared/color_labels.json`:

| Color Key | English | Recommended Spanish | Notes |
|-----------|---------|---------------------|-------|
| BLUE | BLUE | AZUL | Short, universally understood |
| ORANGE | ORANGE | NARANJA | Common word, 7 chars (vs ANARANJADO at 10) |
| PURPLE | PURPLE | MORADO | More common than "PURPURA" in everyday use |
| BLACK | BLACK | NEGRO | Short, universally understood |
| CYAN | CYAN | CIAN | Direct cognate, short (4 chars) |
| AMBER | AMBER | AMBAR | Direct cognate with accent (5 chars) |
| MAGENTA | MAGENTA | MAGENTA | Same word in Spanish (7 chars) |
| GRAY | GRAY | GRIS | Short, universally understood |

**Rationale for word choices:**
- Prioritized commonly understood words over technical/formal alternatives
- Selected shorter forms where alternatives exist (NARANJA vs ANARANJADO)
- All words are accessible for stroke patients and elderly users
- Maximum word length is 7 characters (NARANJA, MAGENTA)

**Full UI Localization:**
Add Spanish translations for all 30+ UI strings in `shared/ui_text.json`, including:
- Page title and subtitle
- Task instructions with language descriptor
- Control labels (Language, Grid, Colors, Seed, Match %)
- Button text (Generate, Random, Check Answers, Clear, Reveal, Hide)
- Section headers (Enter Your Answers, Results, Answer Key)
- Result messages (perfect score, good job, needs work)
- Metadata labels
- Difficulty levels (Accessible, Standard, Advanced, Custom)
- Spacing options (Compact, Normal, Relaxed, Spacious)
- Warning messages

**New Language Descriptor:**
Add `language_descriptor_spanish` key with translations in all four languages:
- chinese: "西班牙语单词"
- english: "Spanish word"
- vietnamese: "tu tieng Tay Ban Nha"
- spanish: "palabra en espanol"

### Typography and Accessibility Recommendations

**Font Recommendations for Elderly/Stroke Patients:**
The current sans-serif approach is appropriate. Spanish text should:
- Continue using the existing dynamic font sizing system (`calculatePuzzleFontSize()`)
- Maintain minimum font size thresholds for accessibility
- The existing font stack works well for Spanish (no special Spanish-specific fonts needed)

**Specific accessibility considerations:**
- Spanish uses standard Latin alphabet with minimal diacritics (accent marks: a, e, i, o, u, n)
- Current Unicode support is sufficient
- No RTL or special layout requirements
- Existing high-contrast color scheme works for Spanish text

### Word Length and Display Strategy

**Recommended Approach:**
1. **Primary strategy:** Use shorter Spanish color words where natural alternatives exist
2. **Grid cell sizing:** The existing dynamic sizing should accommodate Spanish words
3. **Word wrapping:** Enable CSS word-wrap/overflow-wrap as fallback for edge cases
4. **Abbreviation policy:** Avoid abbreviations - all recommended words are already recognizable at full length

**Implementation notes:**
- Longest Spanish color word: NARANJA/MAGENTA (7 chars)
- Longest English color word: MAGENTA (7 chars)
- Vietnamese words are similarly short (max 4 chars)
- Spanish fits within existing character budget

### Backend Updates Required

**Language Enum Update:**
Add `SPANISH = "spanish"` to the Language enum in `backend/app/constants/color_labels.py`

**API Response:**
Update puzzle generation to support Spanish language parameter

### Frontend Updates Required

**Language Selector:**
Add Spanish option to language dropdown with value "spanish"

**Locale Detection:**
Spanish can use "es" locale code for any browser-based detection

### Reusability Opportunities

- Follow exact JSON structure from existing `shared/color_labels.json` and `shared/ui_text.json`
- Reuse Language enum pattern from `backend/app/constants/color_labels.py`
- Extend existing localStorage language persistence
- Reuse dynamic font sizing calculation (no Spanish-specific adjustments needed)
- Follow Vietnamese implementation spec as template

### Scope Boundaries

**In Scope:**
- Spanish translations for all 8 color labels
- Spanish translations for all 30+ UI text strings
- Language enum extension for Spanish
- Language selector UI update
- Language descriptor for Spanish
- Testing with Spanish locale

**Out of Scope:**
- Regional Spanish variants (Latin American vs Castilian distinctions)
- Spanish-specific font families
- RTL layout changes (Spanish is LTR)
- Additional languages beyond Spanish
- Accessibility audit beyond current standards

### Technical Considerations

- Follow existing JSON structure exactly (add "spanish" key to each translation object)
- Use proper Spanish diacritics where needed (AMBAR with accent if desired, though AMBAR without accent is also acceptable)
- Maintain UTF-8 encoding throughout
- Test with Spanish keyboard input for any user-facing text fields
- Deployment target remains Vercel (no server-side changes for locale)

### Testing Requirements

- Verify all 8 Spanish color labels display correctly in puzzle grid
- Verify all UI strings render in Spanish when Spanish is selected
- Test language switching between all four languages (Chinese, English, Vietnamese, Spanish)
- Verify language preference persists via localStorage
- Test responsive behavior with Spanish text at various viewport sizes
- Verify Stroop effect works correctly with Spanish color words
