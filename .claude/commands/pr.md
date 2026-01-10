# Create Pull Request

Create a pull request with an auto-generated summary.

## PHASE 1: Gather Context

Run these commands to understand the changes:

```bash
git status
git log origin/main..HEAD --oneline
git diff origin/main --stat
```

If there are no commits ahead of main, inform the user there's nothing to PR.

## PHASE 2: Ensure Branch is Pushed

Check if the branch is pushed:
```bash
git push -u origin HEAD
```

## PHASE 3: Analyze Changes

Review the commits and changed files to understand:
- What feature/fix was implemented
- Which files were modified
- Any testing or verification notes

## PHASE 4: Create PR

Use the GitHub CLI to create the PR:

```bash
gh pr create --title "[Brief descriptive title]" --body "$(cat <<'EOF'
## Summary
[2-3 bullet points describing what changed and why]

## Changes
[List of key files/areas modified]

## Test Plan
- [ ] Python tests pass (`uv run pytest -v`)
- [ ] Frontend tests pass (`cd frontend && pnpm test`)
- [ ] Verified on live site

---
Generated with Claude Code
EOF
)"
```

## PHASE 5: Confirm

Provide the PR URL to the user:

```
Pull request created!

PR: [URL]
Title: [title]
Branch: [branch] → main

Next: Review and merge when ready.
```
