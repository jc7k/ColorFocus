# Task Format

Structure for feature task breakdown documents.

## Document Structure

```markdown
# Task Breakdown: [Feature Name]

## Overview
Total Tasks: N (across M task groups)

[One paragraph summary]

## Task List

### [Layer Name]

#### Task Group N: [Group Name]
**Dependencies:** [Previous task group or "None"]

- [ ] N.0 Complete [group summary]
  - [ ] N.1 First subtask
  - [ ] N.2 Second subtask
  - [ ] N.3 Third subtask

**Acceptance Criteria:**
- Criterion 1
- Criterion 2
```

## Numbering Format

Use hierarchical numbering: `X.0`, `X.1`, `X.2`

- `X.0` — Summary task (marked complete when all subtasks done)
- `X.1, X.2, ...` — Individual subtasks

## Task Group Rules

- Group by layer (Core Logic, UI, Visualization, Integration)
- Declare dependencies explicitly
- Include acceptance criteria per group
- Keep groups to 5-8 subtasks max

## Checkbox Usage

- `[ ]` — Pending
- `[x]` — Complete

Mark `X.0` complete only when ALL subtasks (`X.1`, `X.2`, ...) are done.

## Files to Modify Section

End with explicit list of files that will be changed:
```markdown
### Files to Modify
- `/path/to/file.js` - Description of changes
- `/path/to/other.json` - Description of changes
```
