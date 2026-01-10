# Add New Color Token

Add a new color token to the ColorFocus color system.

## CRITICAL: Accessibility First

Before adding any color, it MUST be validated for:
- Sufficient contrast against white background (WCAG AA minimum)
- Distinguishability from ALL existing colors for deuteranopia, protanopia, and tritanopia
- Clear visual distinction from existing 8 colors

Use a color blindness simulator (e.g., Coblis, Sim Daltonism) to verify.

## PHASE 1: Gather Requirements

Ask the user:
1. What is the color name? (UPPERCASE, e.g., "TEAL")
2. What is the hex value? (e.g., "#008080")
3. Has this been tested for color blindness accessibility?

If not accessibility-tested, STOP and recommend testing before proceeding.

## PHASE 2: Update Source of Truth

### 2.1 Update `/shared/colors.json`

Add the new color token:

```json
{
  ...existing colors...,
  "NEW_COLOR": "#hexvalue"
}
```

### 2.2 Update `/shared/color_labels.json`

Add labels for ALL supported languages:

```json
{
  ...existing...,
  "NEW_COLOR": {
    "en": "English Name",
    "es": "Spanish Name",
    "zh": "Chinese Character",
    "vi": "Vietnamese Name"
  }
}
```

## PHASE 3: Update Backend

### 3.1 Update `backend/app/constants/colors.py`

Add to the `ColorToken` enum:

```python
class ColorToken(StrEnum):
    ...existing...
    NEW_COLOR = "NEW_COLOR"
```

Update `COLOR_HEX_VALUES` dict:

```python
COLOR_HEX_VALUES = {
    ...existing...,
    ColorToken.NEW_COLOR: "#hexvalue",
}
```

## PHASE 4: Verify Sync

Run `/sync-check` to ensure all files are consistent.

## PHASE 5: Run Tests

Run `/test` to ensure:
- Python tests pass (especially color token tests)
- Frontend tests pass

## PHASE 6: Visual Verification

After deploying, verify the new color:
1. Appears in puzzle grids
2. Is readable against white background
3. Is distinguishable from other colors

## PHASE 7: Report

```
New color token added: [COLOR_NAME]

Hex value: #[hex]
Labels: EN: [x] | ES: [x] | ZH: [x] | VI: [x]

Files modified:
- /shared/colors.json
- /shared/color_labels.json
- backend/app/constants/colors.py

Accessibility: [Verified/Needs verification]

Next: Run /deploy, then /verify to confirm on live site.
```

## Warning

Adding colors increases puzzle complexity. The current 8-color palette was carefully chosen for:
- Maximum distinguishability for color-blind users
- Appropriate difficulty for target users (stroke recovery, elderly)

Consider whether adding colors serves the mission before proceeding.
