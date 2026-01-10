# Deploy to Vercel

Deploy the application to production with pre-flight checks.

## PHASE 1: Pre-flight Checks

Run these checks before deploying:

1. **Git status** — Ensure working directory is clean or changes are intentional
   ```bash
   git status
   ```

2. **Run tests** — Ensure all tests pass
   ```bash
   uv run pytest -v
   cd frontend && pnpm test
   ```

If tests fail, STOP and inform the user. Do not deploy broken code.

## PHASE 2: Deploy

If pre-flight checks pass:

```bash
vercel --prod
```

## PHASE 3: Verify Deployment

After deployment completes:

1. Note the deployment URL from Vercel output
2. Inform the user:

```
Deployment complete!

Production: https://colorfocus.vercel.app
Preview:    [URL from Vercel output if different]

Recommend: Open the live site to verify the deployment works correctly.
```

## Safety Notes

- Never deploy if tests are failing
- If git has uncommitted changes, warn the user but allow deploy if they confirm
