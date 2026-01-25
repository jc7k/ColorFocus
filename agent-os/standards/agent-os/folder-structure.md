# Spec Folder Structure

Naming and organization for feature specification folders.

## Folder Naming

```
agent-os/specs/YYYY-MM-DD-feature-name/
```

- Use date when spec was created
- Use kebab-case for feature name
- Keep names concise but descriptive

## Required Contents

```
YYYY-MM-DD-feature-name/
├── spec.md              # Feature specification
├── tasks.md             # Task breakdown
├── planning/            # Pre-spec exploration
│   ├── raw-idea.md      # Initial notes, brainstorming
│   └── requirements.md  # Refined requirements
└── verifications/       # Post-implementation
    └── final-verification.md
```

## Folder Descriptions

### planning/
Created during spec shaping. Contains:
- `raw-idea.md` — Initial thoughts, user request, rough notes
- `requirements.md` — Refined requirements before formal spec

### verifications/
Created after implementation. Contains:
- `final-verification.md` — Test results, screenshots, sign-off
- `screenshots/` — Optional subfolder for verification images

## Lifecycle

1. **Shape**: Create folder, add `planning/raw-idea.md`
2. **Spec**: Add `spec.md` with formal requirements
3. **Tasks**: Add `tasks.md` with breakdown
4. **Implement**: Work through tasks
5. **Verify**: Add `verifications/final-verification.md`
