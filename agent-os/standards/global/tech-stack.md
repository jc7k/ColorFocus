# Technology Stack

Core technology decisions and rationale.

## Frontend

| Choice | Decision | Why |
|--------|----------|-----|
| Framework | Vanilla JS | Simplicity + performance for elderly users |
| Build step | None | Single-file deployment to Vercel |
| CSS | Plain CSS with variables | No preprocessor needed |
| State | localStorage | Simple persistence without backend |

## Backend

| Choice | Decision | Why |
|--------|----------|-----|
| Language | Python 3.11+ | Type hints, StrEnum support |
| Package manager | uv | Speed + simplicity |
| Testing | pytest | Standard, well-supported |
| Database | Supabase (future) | Managed PostgreSQL + Auth |

## Hosting

| Choice | Decision | Why |
|--------|----------|-----|
| Platform | Vercel | Free tier, automatic deployments |
| Architecture | Static files | No server runtime needed |

## Constraints

- No heavy frameworks (React, Vue, Angular)
- No build tools (Webpack, Vite for bundling)
- No external CSS libraries (Tailwind in HTML, Bootstrap)
- Minimize dependencies — fewer things to break
