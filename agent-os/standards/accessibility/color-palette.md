# Color Palette Design

8 colors ordered by luminance (10% to 84%), optimized for color vision deficiencies.

**Palette:**
```
BLACK   #1A1A1A  10%
BROWN   #8B4513  28%
PURPLE  #7B4BAF  35%
BLUE    #0066CC  38%
GRAY    #808080  50%
PINK    #E75480  52%
ORANGE  #FF8C00  62%
YELLOW  #FFD700  84%
```

**Excluded Colors:**
- **Red** — Confuses with brown/orange for deuteranopia/protanopia (8% of males)
- **Green** — Red-green color blindness; also Vietnamese "xanh" ambiguity
- **Cyan/Teal** — Too similar to blue for elderly users
- **White** — Reserved for background

**Difficulty Tiers:**
- Accessible: 2 colors (Black, Yellow) — max luminance contrast
- Standard: 4 colors (Black, Blue, Orange, Yellow)
- Advanced: 8 colors (full palette)

**Rules:**
- Validate new colors with CVD simulators before adding
- Maintain minimum 15% luminance gap between adjacent colors
- Document rationale when excluding a color
