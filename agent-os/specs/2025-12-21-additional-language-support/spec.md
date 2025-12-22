# Specification: Spanish Language Support

## Goal
Add Spanish as a fourth supported language for ColorFocus, including color labels and full UI text localization for all 30+ UI strings, following the established Vietnamese implementation pattern.

## User Stories
- As a Spanish-speaking user, I want to see color names and UI text in Spanish so that I can experience the Stroop effect in my native language.
- As an elderly or stroke patient user, I want clear, commonly understood Spanish color words with accessible typography so that I can comfortably use the application.

## Specific Requirements

**Add Spanish color labels to shared/color_labels.json**
- Add "spanish" key to each of the 8 color objects alongside existing "chinese", "english", and "vietnamese" keys
- Use commonly understood Spanish color words prioritizing shorter forms where natural alternatives exist
- Spanish translations: BLUE="AZUL", ORANGE="NARANJA", PURPLE="MORADO", BLACK="NEGRO", CYAN="CIAN", AMBER="AMBAR", MAGENTA="MAGENTA", GRAY="GRIS"
- Maximum word length is 7 characters (NARANJA, MAGENTA), which fits within existing character budget
- Maintain UTF-8 encoding for potential diacritics (AMBAR acceptable without accent)

**Add Spanish UI text translations to shared/ui_text.json**
- Add "spanish" key to all 40+ existing UI text entries
- Translate page title, subtitle, task instructions, control labels, button text, section headers, result messages, metadata labels, difficulty levels, spacing options, and warning messages
- Ensure translations are appropriate for elderly/stroke patient users (clear, simple language)
- Add new "language_descriptor_spanish" entry with translations in all four languages

**Update backend Language enum in color_labels.py**
- Add SPANISH = "spanish" to the Language StrEnum class
- Update docstring to include Spanish in the supported languages list
- No changes needed to _load_labels_from_json() as it dynamically loads all language keys from JSON

**Update frontend language selector in puzzle.html**
- Add Spanish option to language dropdown: `<option value="spanish">Spanish</option>`
- Position after Vietnamese option to maintain alphabetical order by language name

**Update frontend validation for Spanish language**
- Add "spanish" to the VALID_LANGUAGES array in puzzle.html JavaScript
- Existing validation function validateLanguage() will automatically support the new language value
- Existing localStorage persistence will work without modification

**Update font size calculation for Spanish**
- Add Spanish entry to widthMultipliers object in calculatePuzzleFontSize() function
- Spanish words are similar length to English (max 7 chars), so use multiplier similar to English (approximately 4.2)
- Existing dynamic font sizing system will handle Spanish text appropriately

**Ensure accessibility for elderly and stroke patients**
- Spanish uses standard Latin alphabet requiring no special font considerations
- Existing system-ui font stack supports Spanish characters including accented vowels
- Existing high-contrast color scheme works for Spanish text
- Current minimum font size thresholds remain appropriate

**Add language descriptor for Spanish task instructions**
- Add "language_descriptor_spanish" key to ui_text.json with translations: chinese="西班牙语单词", english="Spanish word", vietnamese="tu tieng Tay Ban Nha", spanish="palabra en espanol"
- Task instructions will automatically use the appropriate descriptor when Spanish is selected

## Visual Design
No mockups provided. Follow existing control styling patterns and language selector layout in puzzle.html.

## Existing Code to Leverage

**shared/color_labels.json structure**
- Currently maps color tokens to {chinese, english, vietnamese} label objects
- Extend pattern by adding "spanish" key to each object following exact same structure
- Frontend imports via ES module and backend loads at module init time

**shared/ui_text.json structure**
- Currently contains 40+ UI text keys with translations for chinese, english, vietnamese
- Add "spanish" key to each entry following same pattern
- Both frontend and backend dynamically load all language keys from JSON

**backend/app/constants/color_labels.py Language enum**
- StrEnum with CHINESE, ENGLISH, VIETNAMESE values that map to JSON keys
- Add SPANISH = "spanish" following same pattern
- _load_labels_from_json() will automatically pick up new language from JSON

**frontend puzzle.html language handling**
- VALID_LANGUAGES array controls accepted language values
- validateLanguage() function sanitizes language input
- calculatePuzzleFontSize() uses widthMultipliers object for language-specific font sizing
- getUIText() and getLanguageDescriptor() functions automatically work with new language

**Vietnamese language implementation spec**
- Follow exact implementation pattern used for Vietnamese
- Same JSON structure, same backend enum extension, same frontend dropdown addition

## Out of Scope
- Regional Spanish variants (Latin American vs Castilian distinctions)
- Spanish-specific font families beyond system-ui
- RTL layout changes (Spanish is LTR like existing languages)
- Additional languages beyond Spanish in this spec
- Accessibility audit beyond current standards
- Mobile-specific language selector styling changes
- Backend API endpoint changes for language switching
- Changes to puzzle generation algorithm
- Unit tests for language switching (manual testing sufficient for localization)
- Abbreviations or truncated Spanish color words
