# Investigate Issue

Systematically debug and investigate a reported issue.

## PHASE 1: Gather Information

Ask the user:
1. What is the issue? (Brief description)
2. What is the expected behavior?
3. What is the actual behavior?
4. Steps to reproduce (if known)
5. Where was this observed? (Live site, local dev, tests)

## PHASE 2: Reproduce

### 2.1 If Live Site Issue

Use browser tools to:
1. Navigate to https://colorfocus.vercel.app
2. Follow reproduction steps
3. Check console for errors
4. Take snapshot of current state

### 2.2 If Test Failure

Run the specific failing test:
```bash
uv run pytest tests/[test_file].py::[test_name] -v
```

### 2.3 If Local Dev Issue

Start local server and reproduce:
```bash
python3 -m http.server 8080
```

## PHASE 3: Identify Scope

Determine which layer the issue is in:

1. **Frontend only** — JavaScript, CSS, HTML in puzzle.html
2. **Backend only** — Python code in backend/app/
3. **Shared data** — JSON files in /shared/
4. **Cross-platform** — Sync issue between frontend and backend

## PHASE 4: Trace the Code Path

Based on scope, read relevant files:

### Frontend Issues
- `frontend/puzzle.html` — Main app logic
- Check the specific function related to the issue

### Backend Issues
- `backend/app/services/puzzle_generator.py` — Puzzle generation
- `backend/app/constants/` — Color and label constants
- `backend/app/models/` — Data structures

### Data Issues
- `/shared/colors.json`
- `/shared/color_labels.json`
- `/shared/ui_text.json`

## PHASE 5: Identify Root Cause

Document:
1. What code path leads to the issue
2. What condition triggers the bug
3. Why the current code behaves incorrectly

## PHASE 6: Propose Fix

Present the fix:

```
ROOT CAUSE:
[Explanation of why the bug occurs]

AFFECTED FILES:
- [file1.py:line_number]
- [file2.html:line_number]

PROPOSED FIX:
[Description of the fix]

CHANGES REQUIRED:
1. [Specific change 1]
2. [Specific change 2]

RISK ASSESSMENT:
- Low/Medium/High
- [What else might be affected]
```

## PHASE 7: Confirm Before Fixing

Ask the user:
```
I've identified the issue and have a proposed fix.
Would you like me to:

1. Implement the fix now
2. Explain the fix in more detail first
3. Create a spec for a more comprehensive solution
```

## Notes

- Always read the code before proposing fixes
- Check if there are existing tests for the affected code
- Consider edge cases and accessibility impact
- Keep fixes minimal and focused
