# Branch Strategy

When to use branches vs. direct main commits.

## Main Branch

- **Name**: `main` (not master)
- **Protection**: None (small project, fast iteration)
- **Deploy**: Auto-deploys to Vercel on push

## When to Use Feature Branches

**Use a branch for:**
- Multi-file refactors
- New features requiring review
- Changes that might break production
- Collaborative work (Claude branches)

**Commit directly to main for:**
- Small bug fixes
- Documentation updates
- Config tweaks
- Single-file changes

## Branch Naming

For Claude-created branches:
```
claude/<action>-<description>-<random>
claude/implement-next-feature-j7wmY
claude/fix-iphone-support-message-ZoUq8
```

For manual branches:
```
<type>/<description>
feature/add-dark-mode
fix/mobile-overflow
```

## PR Process

Use `/pr` command to create pull requests.
