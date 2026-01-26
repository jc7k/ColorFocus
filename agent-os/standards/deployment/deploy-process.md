# Deploy Process

Steps to deploy to production.

## Pre-flight Checks

1. **Clean git state** — No uncommitted changes (or confirm intentional)
2. **Tests pass** — `uv run pytest -v` + `cd frontend && pnpm test`

**Do NOT deploy if tests fail.**

## Deploy Command

```bash
vercel --prod --yes
```

The `--yes` flag skips confirmation prompts for CLI automation.

Or use `/deploy` slash command.

## Post-Deploy Verification

1. Open https://colorfocus.vercel.app
2. Generate a puzzle
3. Check answer submission works
4. Verify language switching

## Rollback

If deploy breaks production:
```bash
vercel rollback
```

## Use `/deploy` Command

The `/deploy` slash command runs pre-flight checks automatically.
