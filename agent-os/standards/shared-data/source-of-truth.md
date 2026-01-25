# JSON Source of Truth

All canonical data lives in `/shared/*.json`. Platform consumers (Python, TypeScript) import from these files.

**Files:**
- `colors.json` — 8 color tokens with hex values
- `color_labels.json` — Multi-language labels per token
- `ui_text.json` — Full UI localization strings

**Rules:**
- Never duplicate values in consumer code — always import
- TypeScript: `import data from '../../../shared/file.json'`
- Python: Load via `pathlib` relative to module location
- Changes to shared JSON require updating both platform tests

**Why:** Ensures Python backend and TypeScript frontend stay in sync as we migrate to Vercel + Supabase multi-platform deployment.
