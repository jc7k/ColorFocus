# Release Workflow

Complete release workflow: test, deploy, verify, and update documentation.

## PHASE 1: Pre-Release Checks

### 1.1 Check Git Status

```bash
git status
git log --oneline -5
```

Ensure:
- Working directory is clean (or changes are intentional)
- You're on the correct branch (usually main)

### 1.2 Run All Tests

```bash
uv run pytest -v
cd frontend && pnpm test
```

If any tests fail, STOP. Do not release with failing tests.

### 1.3 Check Sync

Run `/sync-check` to verify shared JSON files are consistent.

## PHASE 2: Deploy

```bash
vercel --prod
```

Note the deployment URL from the output.

## PHASE 3: Verify Deployment

### 3.1 Smoke Test

Navigate to https://colorfocus.vercel.app and verify:
- [ ] Page loads without errors
- [ ] Puzzle grid displays correctly
- [ ] New puzzle generation works
- [ ] Language switching works (EN, ES, ZH, VI)
- [ ] Grid size changes work
- [ ] Spacing options work

### 3.2 Check Console

Verify no JavaScript errors in browser console.

### 3.3 Test on Mobile

If possible, check responsive behavior at mobile breakpoint.

## PHASE 4: Update Roadmap (If Applicable)

If this release completes a roadmap item:

1. Read `/agent-os/product/roadmap.md`
2. Mark completed items with [x]
3. Commit the roadmap update

## PHASE 5: Create Release Summary

Generate a release summary:

```
RELEASE COMPLETE
================

Deployed: [timestamp]
URL: https://colorfocus.vercel.app

Changes in this release:
- [List recent commits or features]

Verification:
- Tests: ✓ All passing
- Sync: ✓ JSON files consistent
- Live site: ✓ Smoke test passed

Roadmap items completed:
- [x] [Item if any]

Next priorities:
- [ ] [Next roadmap item]
```

## PHASE 6: Commit Release Notes (Optional)

If significant release, offer to:
1. Tag the release in git
2. Update any version numbers
3. Create GitHub release

## Safety Checklist

Before every release, verify:
- [ ] All tests pass
- [ ] No accessibility regressions
- [ ] Shared JSON files are in sync
- [ ] Recent changes reviewed
- [ ] No sensitive data exposed
