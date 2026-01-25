# Visual Boundaries

Dark borders on colored elements for users with reduced color discrimination.

## Border Spec

- **2px solid border** on all colored UI elements
- Use theme-aware border color (currently `#1A1A1A`)
- Ensures cell boundaries are visible even when adjacent colors are similar

## Elements Requiring Borders

```css
.puzzle-cell {
  border: 2px solid #1A1A1A;
}

.color-swatch {
  border: 2px solid #1A1A1A;
}

.answer-key-item .color-swatch {
  border: 2px solid #1A1A1A;
}
```

## Why

- Elderly users and those with reduced color discrimination need clear boundaries
- Prevents adjacent similar colors (e.g., Blue/Purple) from blending together
- Border must contrast against lightest color (Yellow #FFD700)
