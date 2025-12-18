# ColorFocus – Product Requirements Document (PRD)

## 1. Product Overview

**Project Name:** ColorFocus
**Tagline:** Evidence‑based visual attention and cognitive control puzzles, accessible by design.

ColorFocus is a lightweight web application that generates evidence‑based cognitive puzzles focused on **visual search, attention control, and interference inhibition**. It is designed for older adults, post‑stroke users, and caregivers, with strong accessibility guarantees, including color‑blind‑safe modes.

The core puzzle is a Stroop‑style **word jungle grid**, where users must ignore word meaning and count occurrences of displayed colors.

The system is built to support:

* On‑demand puzzle generation
* Deterministic answer keys
* Caregiver scoring and trend tracking
* Safe LLM‑assisted content generation without hallucinations

---

## 2. Target Users

### Primary Users

* Older adults experiencing mild cognitive decline
* Post‑stroke patients in home‑based recovery

### Secondary Users

* Family caregivers
* Occupational therapists
* Clinicians using lightweight at‑home cognitive screening tools

---

## 3. Core Cognitive Skills Trained

* Selective attention
* Visual search and scanning
* Inhibitory control (Stroop interference)
* Working memory (count tracking)

The product intentionally avoids measuring color perception itself. All designs minimize perceptual confounds so errors reflect cognitive processes, not vision limitations.

---

## 4. Core Puzzle Definition

### Puzzle Format

* Grid‑based word jungle (default: 8×8)
* Each cell contains a **color word**
* Each word is rendered in a **different ink color**

### Task Instruction

"Ignore the word meaning. Count how many times each color appears on the page based on the ink color."

---

## 5. Color System (Orthogonal, Color-Blind-Safe, Adjustable Brightness)

The color system is designed to minimize perceptual interference across aging vision, common color blindness types, and low-contrast environments. The system separates **hue selection** from **brightness control** and enforces **single-character Chinese labels** for all grid content.

### 5.1 Core Design Principles

* Avoid red–green and blue–yellow confusion axes
* Maximize luminance separation between colors
* Preserve hue identity while adjusting brightness
* Enforce single-character labels to minimize visual and cognitive load
* Ensure errors reflect cognition, not vision limitations

---

### 5.2 Canonical Color Tokens and Labels

All colors are defined by a canonical token, a **single-character Chinese label**, and hex color variants. Multi-character labels are not permitted in grids.

| Token   | Label | Meaning      | Base Hex |
| ------- | ----- | ------------ | -------- |
| BLUE    | 藍     | Blue         | #2E86DE  |
| ORANGE  | 橙     | Orange       | #E67E22  |
| PURPLE  | 紫     | Purple       | #9C27B0  |
| BLACK   | 黑     | Black        | #2B2B2B  |
| CYAN    | 青     | Cyan / Teal  | #17A2B8  |
| AMBER   | 金     | Amber / Gold | #F4B400  |
| MAGENTA | 品     | Magenta      | #D81B60  |
| GRAY    | 灰     | Gray         | #757575  |

---

### 5.3 Brightness Variants (Per Token)

Each color token supports luminance variants. Hue must remain constant. Only brightness may change.

Example (BLUE):

* BLUE_DARK: #1F4E79
* BLUE_BASE: #2E86DE
* BLUE_BRIGHT: #6BB6FF

This pattern applies to all tokens.

---

### 5.4 Runtime Brightness Selection

* Default: BASE
* Optional user toggle: "Increase contrast" → BRIGHT
* No automatic switching without user consent

---

### 5.5 Label Legend Requirement

When any non-basic label (e.g., 金, 品) is used, the UI must display a **one-time legend** at the start of a session:

* 金 = 琥珀色 (Amber)
* 品 = 洋紅色 (Magenta)

The legend is not shown during the task itself.

---

## 6. Puzzle Generation Rules

### 6.1 Grid Parameters

* Rows: configurable (default 8)
* Columns: configurable (default 8)

### 6.2 Color Set Selection

* Maximum colors per puzzle: 4
* Colors must be selected from canonical tokens
* Accessibility mode restricts available sets

### 6.3 Distribution Constraints

* Near-uniform distribution
* No identical per-color counts
* Default per-color range (8×8): 14–18

### 6.4 Spatial Constraints

* High spatial entropy
* Maximum adjacent identical colors: 2
* No large contiguous color blocks

---

## 7. Accessibility Requirements

* Color‑blind‑safe default palette
* Large, sans‑serif fonts
* Adjustable grid spacing
* Printable layout support
* No reliance on color alone for UI controls

---

## 8. Scoring & Answer Keys

### Automatic Outputs

* Frequency count per color
* Total cell count validation
* Answer key generation

### Scoring Metrics (Phase 2)

* Accuracy per color
* Total error count
* Time to completion
* Error distribution patterns

---

## 9. Caregiver & Dashboard (Phase 2)

* Weekly performance summaries
* Trend visualization
* Color‑specific error heatmaps
* Exportable PDF reports

---

## 10. LLM Safety & Determinism

If LLMs are used for generation:

* Schema‑locked color tokens only
* Deterministic validation pass required
* Automatic rejection if constraints are violated

This prevents hallucinated colors, mismatched counts, or invalid puzzles.

---

## 11. Non‑Goals

* Diagnosing medical conditions
* Measuring color vision
* Competitive gamification

---

## 12. Success Criteria

* Users can complete puzzles without color confusion
* Caregivers can reliably score without manual recounts
* Generated puzzles are reproducible and verifiable

---

## 13. Difficulty Tiers & Color Sets

The system supports structured difficulty tiers by varying color sets, grid size, and brightness demands.

### Tier 1: Accessible / Recovery

* Colors: BLUE, ORANGE, BLACK, AMBER
* Brightness: BRIGHT
* Grid: 6×6 or 8×8

### Tier 2: Standard Cognitive Training

* Colors: BLUE, ORANGE, PURPLE, BLACK
* Brightness: BASE
* Grid: 8×8

### Tier 3: Advanced / Research

* Colors: BLUE, CYAN, MAGENTA, AMBER
* Brightness: BASE or DARK
* Grid: 8×8 or 10×10

---

## 14. Color Token Registry (Authoritative)

All puzzles must reference colors via token IDs. Rendering layers select brightness variants.

```json
{
  "BLUE": {
    "label": "藍",
    "variants": {
      "dark": "#1F4E79",
      "base": "#2E86DE",
      "bright": "#6BB6FF"
    }
  },
  "ORANGE": {
    "label": "橙",
    "variants": {
      "dark": "#B65D13",
      "base": "#E67E22",
      "bright": "#FFB366"
    }
  },
  "PURPLE": {
    "label": "紫",
    "variants": {
      "dark": "#6A1B9A",
      "base": "#9C27B0",
      "bright": "#CE93D8"
    }
  },
  "BLACK": {
    "label": "黑",
    "variants": {
      "base": "#2B2B2B",
      "bright": "#4A4A4A"
    }
  }
```

---

## 15. Non-Goals (Updated)

* Measuring color vision
* Automatically changing color hues for accessibility
* Realtime LLM-based puzzle generation

