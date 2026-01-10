# Commit and Push Changes

Commit all staged and unstaged changes, then push to remote.

## PHASE 1: Check Current State

Run these commands to understand what needs to be committed:

1. `git status` — See all changed files
2. `git diff --stat` — See summary of changes
3. `git log --oneline -3` — See recent commit style

## PHASE 2: Stage and Commit

1. Review the changes and draft a commit message that:
   - Uses imperative mood ("Add feature" not "Added feature")
   - Summarizes the "why" not just the "what"
   - Is concise (1-2 lines)

2. Stage all changes:
   ```bash
   git add -A
   ```

3. Create the commit using a HEREDOC for proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   Your commit message here

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

## PHASE 3: Push to Remote

1. Push to the current branch:
   ```bash
   git push
   ```

2. If the branch has no upstream, set it:
   ```bash
   git push -u origin HEAD
   ```

## PHASE 4: Confirm

After pushing, run `git status` to confirm clean state and inform the user:

```
Changes committed and pushed!

Commit: [short hash] [commit message summary]
Branch: [branch name]
Remote: [remote URL or name]
```

## Safety Notes

- Never force push unless explicitly requested
- Never push to main/master without user confirmation
- If there are merge conflicts, stop and inform the user
