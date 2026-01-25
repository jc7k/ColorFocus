# Vercel Configuration

Static site configuration for Vercel.

## vercel.json

```json
{
  "rewrites": [
    { "source": "/", "destination": "/frontend/puzzle.html" },
    { "source": "/puzzle", "destination": "/frontend/puzzle.html" }
  ]
}
```

## How It Works

- **Static hosting** — No serverless functions, pure static files
- **Root redirect** — `/` serves `puzzle.html`
- **Auto-deploy** — Push to `main` triggers production deploy

## Directory Structure

Vercel serves from repo root:
- `/frontend/` — Static HTML, CSS, JS
- `/shared/` — JSON files imported by frontend
- `/frontend/bmc_qr.png` — Static assets

## No Build Step

- No `build` command in vercel.json
- No `output` directory specified
- Files served as-is from repo
