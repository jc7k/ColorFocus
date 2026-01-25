# Shape: Stroop Guidance Messaging

## Problem Statement

When users make mistakes influenced by the Stroop effect, they see the summary statistics but don't understand:
1. Why the Stroop effect happens (the neuroscience)
2. What their specific pattern of errors suggests
3. How to improve through practice

## Solution: Educational Guidance Section

Add a guidance section within the mistake summary panel that provides:
- **Education**: Brief explanation of why Stroop interference occurs
- **Pattern Feedback**: Personalized interpretation based on their error distribution
- **Practice Tips**: Actionable advice tailored to their specific pattern

## Scope Decisions

### In Scope
- Educational text about Stroop effect mechanism
- Four pattern categories: high_stroop, moderate_stroop, mixed_errors, non_stroop
- Full 4-language localization
- Elderly-friendly typography (readable sizes, high contrast)
- Mobile responsiveness

### Out of Scope
- Progress tracking over time (future feature)
- Detailed cognitive assessment (medical advice)
- Interactive tutorials or animations
- Sound/audio explanations

## Key Design Decisions

1. **Guidance only shows when mistakes exist** - Perfect scores don't need guidance
2. **Pattern thresholds**: 70%+ high, 40-69% moderate, <40% mixed, 0% non-Stroop
3. **Placed after legend, before metadata** - Natural reading flow
4. **Same styling as legend section** - Visual consistency

## Target Users

- Stroke recovery patients doing cognitive rehabilitation
- Elderly users exercising cognitive function
- Anyone learning about the Stroop effect

## Success Criteria

- Users understand why they made Stroop-influenced mistakes
- Users receive actionable advice for improvement
- All content readable at default font sizes for elderly users
- Works correctly in all 4 supported languages
