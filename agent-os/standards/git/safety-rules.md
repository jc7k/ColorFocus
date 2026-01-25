# Git Safety Rules

Protections to prevent accidental data loss.

## Never Do Without Explicit Request

- `git push --force` — Can destroy remote history
- `git reset --hard` — Loses uncommitted work
- `git checkout .` — Discards all changes
- `git clean -f` — Deletes untracked files
- `git branch -D` — Force-deletes branch

## Main Branch Protection

- **Never force push to main** — Warn even if explicitly requested
- Ask for confirmation before pushing large changesets to main
- Prefer PR workflow for risky changes

## Conflict Handling

- **Stop immediately** on merge conflicts
- Do not attempt auto-resolution
- Report conflict details to user and await guidance

## Pre-Commit Hooks

- If commit fails due to pre-commit hook:
  - **Create NEW commit** after fixing issues
  - **Never use --amend** (would modify wrong commit)
  - **Never use --no-verify** to skip hooks

## Safe Defaults

- Stage specific files, not `git add -A` (avoids secrets)
- Always `git status` before and after operations
- Prefer `git push -u origin HEAD` for new branches
