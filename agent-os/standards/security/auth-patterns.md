# Authentication Patterns

Supabase OAuth integration.

## OAuth Flow

```javascript
async function signInWithGoogle() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: window.location.origin + window.location.pathname
    }
  });
}
```

## Session Handling

- Sessions managed by Supabase client
- Tokens stored in localStorage by Supabase SDK
- UI updates via `onAuthStateChange` listener

## API Keys

**Safe to expose in frontend:**
- `SUPABASE_ANON_KEY` — Public anon key (Row Level Security enforced)

**Never expose:**
- `SUPABASE_SERVICE_KEY` — Server-side only (bypasses RLS)

## Current Status

Auth is implemented but database backend not yet activated:
- OAuth login/logout works
- User info displayed in UI
- No data persistence yet (future Supabase integration)
