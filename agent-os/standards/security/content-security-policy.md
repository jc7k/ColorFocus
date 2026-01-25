# Content Security Policy

CSP header to prevent XSS and injection attacks.

## Current Policy

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://lh3.googleusercontent.com;
  connect-src 'self' https://*.supabase.co;
">
```

## Directives Explained

| Directive | Allowed | Why |
|-----------|---------|-----|
| `default-src` | 'self' | Baseline: only same-origin |
| `script-src` | 'self', 'unsafe-inline', cdn.jsdelivr.net | Inline JS in single-file, Supabase SDK |
| `style-src` | 'self', 'unsafe-inline' | Inline CSS in single-file |
| `img-src` | 'self', data:, lh3.googleusercontent.com | User avatars from Google |
| `connect-src` | 'self', *.supabase.co | API calls to Supabase |

## Known Tradeoffs

- `'unsafe-inline'` required for single-file architecture
- Future: extract CSS/JS to files and remove unsafe-inline
