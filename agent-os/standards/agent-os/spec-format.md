# Spec Format

Structure for feature specification documents.

## Required Sections (in order)

1. **Goal** — One paragraph explaining what the feature achieves
2. **User Stories** — Bulleted list in "As a [user], I want [feature] so that [benefit]" format
3. **Specific Requirements** — Grouped by sub-feature, detailed behavior specs
4. **Existing Code to Leverage** — Functions, patterns, variables to reuse
5. **Out of Scope** — Explicit list of what this spec does NOT include

## Section Details

### Goal
Single paragraph, 2-3 sentences max. Focus on user value.

### User Stories
```markdown
- As a [user type], I want [feature] so that [benefit]
- As a [user type], I want [feature] so that [benefit]
```

### Specific Requirements
Group related requirements under bold headers:
```markdown
**Feature Area Name**
- Requirement 1
- Requirement 2
```

### Existing Code to Leverage
List reusable code with file locations:
```markdown
**Function Name (`variableName`)**
- What it does
- How to use it
- File location
```

### Out of Scope
Explicit exclusions prevent scope creep:
```markdown
- Feature X (future phase)
- Edge case Y (not needed for MVP)
```
