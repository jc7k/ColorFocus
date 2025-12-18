# Color Token Research and Validation

This document describes the research findings and validation methodology used to select the color-blind-safe hex values for the ColorFocus color token system.

## Source References

### PRD Section 5.2 - Base Color Values
The following base hex values were provided in the PRD as starting points:

| Token   | Base Hex | Meaning      |
|---------|----------|--------------|
| BLUE    | #2E86DE  | Blue         |
| ORANGE  | #E67E22  | Orange       |
| PURPLE  | #9C27B0  | Purple       |
| BLACK   | #2B2B2B  | Black        |
| CYAN    | #17A2B8  | Cyan / Teal  |
| AMBER   | #F4B400  | Amber / Gold |
| MAGENTA | #D81B60  | Magenta      |
| GRAY    | #757575  | Gray         |

### PRD Section 14 - Validated Variants
The PRD provided pre-validated variants for BLUE, ORANGE, PURPLE, and BLACK:

- **BLUE**: dark=#1F4E79, base=#2E86DE, bright=#6BB6FF
- **ORANGE**: dark=#B65D13, base=#E67E22, bright=#FFB366
- **PURPLE**: dark=#6A1B9A, base=#9C27B0, bright=#CE93D8
- **BLACK**: base=#2B2B2B, bright=#4A4A4A (no dark variant)

## Color-Blind Accessibility Validation

### Target Conditions
Colors were validated for distinguishability across three common types of color vision deficiency:

1. **Deuteranopia** (red-green, most common, ~6% of males)
2. **Protanopia** (red-green, ~1% of males)
3. **Tritanopia** (blue-yellow, ~0.01% of population)

### Design Principles Applied

Per PRD Section 5.1:
- Avoid red-green and blue-yellow confusion axes
- Maximize luminance separation between colors
- Preserve hue identity while adjusting brightness
- No information conveyed by color alone (text labels always present)

### Color Selection Rationale

1. **BLUE (#2E86DE)**: Safe anchor color, distinguishable across all CVD types due to unique blue channel dominance

2. **ORANGE (#E67E22)**: High luminance warm color, distinct from blue on luminance axis even for protanopia/deuteranopia

3. **PURPLE (#9C27B0)**: Occupies unique position between red and blue, distinguishable by blue component

4. **BLACK (#2B2B2B)**: Achromatic, relies purely on luminance (darkest color in set)

5. **CYAN (#17A2B8)**: Blue-green hue with different luminance than BLUE, maintains distinction

6. **AMBER (#F4B400)**: Highest luminance color, distinctive even when hue perception is impaired

7. **MAGENTA (#D81B60)**: Pinkish-red with blue undertones, distinct from pure red confusion zone

8. **GRAY (#757575)**: Neutral achromatic, mid-range luminance provides baseline reference

## HSL-Based Brightness Variant Calculation

### Methodology
Variants were calculated by adjusting HSL lightness values while keeping hue constant:

- **DARK variant**: Reduce lightness by ~15-20% from BASE
- **BRIGHT variant**: Increase lightness by ~15-20% from BASE
- **Hue**: Remains constant across all variants of each token

### HSL Reference Values

| Token   | Variant | Hex     | HSL Approximation        |
|---------|---------|---------|--------------------------|
| BLUE    | dark    | #1F4E79 | hsl(209, 59%, 30%)       |
| BLUE    | base    | #2E86DE | hsl(209, 75%, 53%)       |
| BLUE    | bright  | #6BB6FF | hsl(209, 100%, 71%)      |
| ORANGE  | dark    | #B65D13 | hsl(27, 81%, 39%)        |
| ORANGE  | base    | #E67E22 | hsl(27, 80%, 52%)        |
| ORANGE  | bright  | #FFB366 | hsl(27, 100%, 70%)       |
| PURPLE  | dark    | #6A1B9A | hsl(291, 70%, 35%)       |
| PURPLE  | base    | #9C27B0 | hsl(291, 64%, 42%)       |
| PURPLE  | bright  | #CE93D8 | hsl(291, 47%, 71%)       |
| BLACK   | base    | #2B2B2B | hsl(0, 0%, 17%)          |
| BLACK   | bright  | #4A4A4A | hsl(0, 0%, 29%)          |
| CYAN    | dark    | #0D6977 | hsl(187, 79%, 26%)       |
| CYAN    | base    | #17A2B8 | hsl(187, 79%, 41%)       |
| CYAN    | bright  | #5DD3E8 | hsl(187, 75%, 64%)       |
| AMBER   | dark    | #B88600 | hsl(44, 100%, 36%)       |
| AMBER   | base    | #F4B400 | hsl(44, 100%, 48%)       |
| AMBER   | bright  | #FFCF4D | hsl(44, 100%, 65%)       |
| MAGENTA | dark    | #9C1244 | hsl(337, 79%, 34%)       |
| MAGENTA | base    | #D81B60 | hsl(337, 78%, 48%)       |
| MAGENTA | bright  | #F06292 | hsl(337, 82%, 66%)       |
| GRAY    | dark    | #4A4A4A | hsl(0, 0%, 29%)          |
| GRAY    | base    | #757575 | hsl(0, 0%, 46%)          |
| GRAY    | bright  | #A0A0A0 | hsl(0, 0%, 63%)          |

## WCAG Contrast Considerations

### Background Context
Per PRD, puzzles are displayed on a consistent light/white background for older adults.

### Contrast Analysis
- **Dark colors** (BLACK, PURPLE, BLUE, CYAN, GRAY, MAGENTA) achieve 3:1+ contrast against white
- **Light colors** (ORANGE, AMBER) have inherently lower contrast against white but are distinguishable by luminance differences
- **Text labels** (Chinese characters) are always present alongside colors per PRD Section 5.1

### Luminance Distribution
Colors are distributed across the luminance spectrum:
- Darkest: BLACK (~0.02)
- Mid-dark: PURPLE, BLUE (~0.09-0.15)
- Mid: CYAN, MAGENTA, GRAY (~0.14-0.20)
- Mid-light: ORANGE (~0.30)
- Lightest: AMBER (~0.48)

This spread ensures that even users with significant color vision impairment can distinguish colors based on perceived brightness differences.

## Validation Tests

The following automated tests verify color token compliance:

1. **Structure validation**: JSON format, required tokens, variants object
2. **Hex format validation**: All 23-24 values match #RRGGBB pattern
3. **Variant completeness**: All non-BLACK tokens have dark/base/bright
4. **Luminance separation**: Colors span minimum 0.3 luminance range
5. **No identical luminance**: Each color has unique luminance value
6. **Dark color contrast**: Dark-oriented colors meet 3:1 minimum against white

Run tests with: `uv run pytest tests/test_color_tokens.py -v`
