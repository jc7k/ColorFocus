# Add New Language

Add a new language to the ColorFocus application.

## PHASE 1: Gather Requirements

Ask the user:
1. What is the language name and code? (e.g., "French" / "fr")
2. Do you have translations for all 8 color labels?
   - BLUE, ORANGE, PURPLE, BLACK, CYAN, AMBER, MAGENTA, GRAY

If the user doesn't have translations, offer to help research them but note they should be verified by a native speaker.

## PHASE 2: Update Shared JSON Files

### 2.1 Update `/shared/color_labels.json`

Add the new language code and all 8 color translations:

```json
{
  "BLUE": { ..., "NEW_CODE": "translation" },
  "ORANGE": { ..., "NEW_CODE": "translation" },
  ...
}
```

### 2.2 Update `/shared/ui_text.json`

Add UI translations for the new language:
- App title
- Instructions
- Button labels
- Settings labels

## PHASE 3: Update Backend

### 3.1 Update `backend/app/constants/color_labels.py`

Add the new language to the `Language` enum:

```python
class Language(StrEnum):
    ...
    NEW_CODE = "NEW_CODE"
```

## PHASE 4: Update Frontend

### 4.1 Update `frontend/puzzle.html`

Add the language option to the language selector dropdown.

## PHASE 5: Calculate Font Multiplier

Determine the font scaling multiplier for the new language:
1. Find the longest color word in the new language
2. Count its characters
3. Calculate multiplier (roughly: characters × 0.6)

Add to the `LANGUAGE_MULTIPLIERS` object in puzzle.html.

## PHASE 6: Verify

1. Run `/sync-check` to verify JSON consistency
2. Run `/test` to ensure tests pass
3. Run `/verify` to check live behavior (after deploy)

## PHASE 7: Report

```
New language added: [Language Name] ([code])

Files modified:
- /shared/color_labels.json
- /shared/ui_text.json
- backend/app/constants/color_labels.py
- frontend/puzzle.html

Font multiplier: [X.X] (based on longest word: "[word]")

Next: Run /test, then /deploy to push changes live.
```

## Important Notes

- All translations should be verified by a native speaker
- Consider cultural context for color names (some colors have different cultural meanings)
- Test with the actual font to ensure characters render correctly
