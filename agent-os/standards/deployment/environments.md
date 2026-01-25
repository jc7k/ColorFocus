# Environments & URLs

Deployment environments and configuration.

## URLs

| Environment | URL |
|-------------|-----|
| Production | https://colorfocus.vercel.app |
| Preview | Auto-generated per PR/branch |

## Environment Variables

Set in Vercel dashboard (not in code):

- `SUPABASE_URL` — Supabase project URL (future)
- `SUPABASE_ANON_KEY` — Supabase public API key (future)

**Never commit secrets to git.**

## Preview Deployments

- Every PR gets a unique preview URL
- Preview URL shown in Vercel CLI output
- Test changes before merging to main

## Local Development

```bash
python3 -m http.server 8080
# Open http://localhost:8080/frontend/puzzle.html
```
