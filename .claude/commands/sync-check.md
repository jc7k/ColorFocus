# Sync Check

Verify that shared JSON source-of-truth files are properly consumed by both frontend and backend.

## PHASE 1: Read Source Files

Read the shared JSON files:
- `/shared/colors.json`
- `/shared/color_labels.json`
- `/shared/ui_text.json`

## PHASE 2: Check Backend Consumption

Verify Python constants match shared JSON:
- `backend/app/constants/colors.py` — ColorToken enum should match colors.json
- `backend/app/constants/color_labels.py` — Labels should match color_labels.json

Check that:
1. All color tokens in colors.json exist in the Python enum
2. All hex values match
3. All language labels match

## PHASE 3: Check Frontend Consumption

Verify frontend imports match shared JSON:
- `frontend/puzzle.html` — Should import from /shared/*.json

Check that:
1. Import paths are correct
2. No hardcoded color values that should come from JSON
3. Language labels are loaded from shared source

## PHASE 4: Report

Provide a sync status report:

```
Sync Check Results:

colors.json:
  ✓ Backend: 8/8 tokens match
  ✓ Frontend: imports correctly

color_labels.json:
  ✓ Backend: all languages match
  ✓ Frontend: imports correctly

ui_text.json:
  ✓ Frontend: imports correctly

[If any mismatches, list them specifically with file locations]
```

If mismatches found, suggest specific fixes.
