# Commit Message Format

Conventions for git commit messages.

## Format

```
<imperative verb> <what changed>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Examples

✅ Good:
- `Add mistake identification feature for cognitive assessment`
- `Fix grid overflow on mobile devices`
- `Refactor font scaling to support new languages`

❌ Bad:
- `Added feature` (not imperative)
- `Fixed bug` (too vague)
- `Updates to code` (meaningless)

## Rules

- **Imperative mood**: "Add" not "Added", "Fix" not "Fixed"
- **Concise**: 50 chars for subject line, wrap body at 72
- **Why not what**: Focus on purpose, not mechanics
- **One logical change**: Atomic commits, not kitchen sink

## Co-Author Tag

For AI-assisted commits, include:
```
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Use `/commit` Command

The `/commit` slash command handles formatting automatically.
