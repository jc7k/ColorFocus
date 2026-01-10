# Run All Tests

Run both Python and frontend test suites to verify the codebase.

## PHASE 1: Run Python Tests

```bash
uv run pytest -v
```

If tests fail, summarize the failures clearly.

## PHASE 2: Run Frontend Tests

```bash
cd frontend && pnpm test
```

If tests fail, summarize the failures clearly.

## PHASE 3: Report Results

Provide a summary:

```
Test Results:

Python:   ✓ X passed (or ✗ X failed, Y passed)
Frontend: ✓ X passed (or ✗ X failed, Y passed)

[If failures, list the failing test names and brief reason]
```

If all tests pass, confirm the codebase is ready for commit/deploy.
If any tests fail, suggest next steps to fix them.
