# Accessibility Audit

Perform a comprehensive accessibility audit of the ColorFocus application.

## PHASE 1: Color Contrast Check

### 1.1 Read Current Colors

Read `/shared/colors.json` to get all color hex values.

### 1.2 Calculate Contrast Ratios

For each color, calculate contrast ratio against white (#FFFFFF) background:
- WCAG AA requires 4.5:1 for normal text
- WCAG AAA requires 7:1 for normal text

Use the formula:
```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B (after gamma correction)
Contrast = (L1 + 0.05) / (L2 + 0.05)
```

### 1.3 Report Contrast Results

```
Color Contrast Audit (against white background):

| Color   | Hex     | Ratio | AA   | AAA  |
|---------|---------|-------|------|------|
| BLUE    | #1E5AA8 | X.X:1 | ✓/✗  | ✓/✗  |
| ORANGE  | #D35400 | X.X:1 | ✓/✗  | ✓/✗  |
...
```

## PHASE 2: Color Blindness Simulation

### 2.1 Analyze Color Pairs

Check that each color is distinguishable from every other color under:
- **Deuteranopia** (red-green, most common)
- **Protanopia** (red-green)
- **Tritanopia** (blue-yellow)

### 2.2 Flag Problem Pairs

List any color pairs that may be confused under color blindness conditions.

## PHASE 3: Font Size Check

### 3.1 Review Font Scaling

Read `frontend/puzzle.html` and check:
- Minimum font size meets accessibility standards (16px minimum recommended)
- Font scaling works correctly at all grid sizes
- Language multipliers are appropriate

### 3.2 Check Viewport Scaling

Verify font sizes at different viewport widths:
- Mobile (480px and below)
- Tablet (768px)
- Desktop (1024px+)

## PHASE 4: Interactive Element Check

### 4.1 Button Sizes

Verify touch targets meet minimum size:
- 44x44px minimum for touch (WCAG 2.1)
- Adequate spacing between interactive elements

### 4.2 Focus Indicators

Check that keyboard navigation shows clear focus states.

## PHASE 5: Motion and Animation

Verify:
- No animations that could cause seizures (flashing >3 times/second)
- Reduced motion preferences are respected
- No disorienting transitions

## PHASE 6: Generate Report

```
ACCESSIBILITY AUDIT REPORT
==========================

Color Contrast: [PASS/FAIL]
- X/8 colors meet WCAG AA
- X/8 colors meet WCAG AAA
- Issues: [list any]

Color Blindness: [PASS/FAIL]
- Deuteranopia: [OK/Issues]
- Protanopia: [OK/Issues]
- Tritanopia: [OK/Issues]
- Problem pairs: [list any]

Font Sizing: [PASS/FAIL]
- Minimum size: Xpx
- Scaling: [OK/Issues]

Touch Targets: [PASS/FAIL]
- Minimum size: Xpx
- Issues: [list any]

Motion: [PASS/FAIL]
- No seizure risks: [Yes/No]

RECOMMENDATIONS:
1. [Priority fixes if any]
2. [Improvements if any]
```

## PHASE 7: Create Issues (Optional)

If issues are found, offer to create GitHub issues or add to a fixes list.
