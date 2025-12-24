# Specification: Buy Me A Coffee Donation Feature

## Goal
Add non-intrusive donation touchpoints to ColorFocus that allow users to support the project via Buy Me A Coffee, using a header text link for immediate action and a footer QR code for users who may print puzzles.

## User Stories
- As a user who enjoys ColorFocus, I want to easily find a way to support the project so that I can contribute to its continued development.
- As a caregiver or therapist printing puzzles, I want to see a QR code on printed materials so that I can donate later without interrupting my workflow.

## Specific Requirements

**Header Donation Link**
- Add a text link reading "Support this project" positioned in the header area below the subtitle
- Style the link using the existing secondary text color (#64748b) to match the subtitle styling
- Link must open in a new tab using target="_blank" with rel="noopener noreferrer" for security
- Link URL: https://buymeacoffee.com/xwje4mbv3l
- Position should be subtle and non-intrusive, not competing with the main puzzle UI

**Footer QR Code Display**
- Display the bmc_qr.png image in a new section below the Answer Key section
- QR code should be reasonably sized for scanning (approximately 120-150px on desktop, scaled appropriately for mobile)
- Include a subtle label below the QR code explaining its purpose (localized)
- The QR code image is a static local asset; no clickable link wrapper needed (users scan with phone camera)

**Asset Relocation**
- Move bmc_qr.png from project root to /home/user/projects/ColorFocus/frontend/ directory
- Reference the image using a relative path from puzzle.html

**Localization**
- Add new translation keys to /home/user/projects/ColorFocus/shared/ui_text.json for all donation-related text
- Translations required for: Chinese, English, Spanish, Vietnamese
- Keys needed: "support_link_text" (header link), "qr_code_label" (footer caption)
- Use existing getUIText() function pattern for retrieving translations

**Responsive Styling**
- Header link should remain visible and appropriately sized on mobile (minimum touch target 44x44px per accessibility standards)
- QR code section should scale down gracefully on smaller screens
- Follow existing mobile breakpoints at 480px and 375px from puzzle.html

**Accessibility**
- Header link must have meaningful link text (the localized "Support this project" text)
- QR code image must have descriptive alt text explaining it links to Buy Me A Coffee
- Maintain proper semantic HTML structure

## Visual Design

**`/home/user/projects/ColorFocus/bmc_qr.png`**
- Buy Me A Coffee branded QR code with yellow coffee cup logo embedded in center
- Black dotted pattern on white background, standard square QR format
- Original size approximately 700x700 pixels; will need CSS sizing constraints
- High contrast design works well against app's light gray (#f8fafc) background
- No border or frame needed; the QR code is self-contained

## Existing Code to Leverage

**Subtitle styling in puzzle.html (lines 24-28)**
- Use .subtitle class pattern: color #64748b, font-size 0.9rem, margin-bottom 1rem
- Header donation link should match this secondary text aesthetic
- Apply similar hover state considerations (subtle underline or color shift)

**Localization pattern using ui_text.json**
- Extend existing JSON structure with new keys following established format
- Use getUIText() function (line 688-698) to retrieve translated strings
- Follow updateAllUIText() pattern (line 798-850) for applying translations on language change

**Mobile responsive breakpoints (lines 359-495)**
- Follow @media (max-width: 480px) breakpoint for mobile adjustments
- Follow @media (max-width: 375px) for extra small devices
- Apply consistent padding/margin reductions on mobile

**Section container styling (e.g., .answer-key-section lines 299-320)**
- Use similar white background, border-radius 12px, padding 1rem, box-shadow pattern for footer QR section
- Maintain consistent visual hierarchy with existing sections

## Out of Scope
- A/B testing infrastructure or multiple design variants
- Donation popups, modals, or interstitial prompts
- Click tracking, analytics, or conversion measurement
- Donation goal displays or progress indicators
- Buy Me A Coffee widget embedding or external script loading
- Changes to Content Security Policy (use local assets only)
- Any prominent, attention-grabbing, or animated donation prompts
- Integration with payment processing or donation receipts
- Multiple donation platform options (Buy Me A Coffee only)
- Backend API endpoints or donation logging
