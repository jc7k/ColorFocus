# Spec Requirements: Buy Me A Coffee Donation Button

## Initial Description
Add a "Buy Me A Coffee" donation button/link to ColorFocus. The user wants to add a donation option to the application. They have provided:
- URL: buymeacoffee.com/xwje4mbv3l
- QR code image: bmc_qr.png (already in project root)

This will allow users to support the project financially.

## Requirements Discussion

### First Round Questions

**Q1:** Button Placement - Should the donation link be in the footer area (below the Answer Key section), or in the header area near the title?
**Answer:** Header area - because no one will see it in the footer especially mobile users. Keep it as clean as possible, don't be obnoxious about it.

**Q2:** Visual Style and Prominence - Should we use a subtle text link, a small button with Buy Me A Coffee yellow branding, or a custom-styled button matching the app's existing blue button style?
**Answer:** User feels they need to A/B test this but isn't sure how. Asked for a recommendation.

**Recommendation Provided:** Start with a subtle text link styled consistently with the app's existing secondary elements (slate-gray #64748b color matching the subtitle). Rationale:
- A/B testing requires sufficient traffic volume which a niche accessibility app may not have
- Adding A/B infrastructure conflicts with "keep it clean" goal
- Text links are accessible and work well with screen readers
- Easy to iterate based on qualitative feedback from Buy Me A Coffee dashboard
- Future experimentation can be done via manual version deployments rather than custom infrastructure

**Q3:** QR Code Usage - Should the QR code be displayed in the UI, or is it primarily for printed materials?
**Answer:** User proposes a direct link with "Support this project" in the header AND the QR code in the footer. This provides two donation touchpoints - immediate (header link) and delayed (footer QR for users who may print puzzles).

**Q4:** Localization - Should the donation link text be translated in each language?
**Answer:** Yes, localize the donation link text in all four supported languages (Chinese, English, Spanish, Vietnamese).

**Q5:** Open in New Tab - Should the Buy Me A Coffee link open in a new browser tab?
**Answer:** Yes, open in new tab so users don't lose puzzle progress.

**Q6:** Content Security Policy - Should we update CSP to allow external Buy Me A Coffee assets, or keep things simple with local assets only?
**Answer:** Keep things simple, use only local assets. The existing bmc_qr.png will be used; no external images from buymeacoffee.com.

**Q7:** Exclusions - Any donation-related features to specifically avoid?
**Answer:** Agreed with all three exclusions:
- No popup/modal asking for donations
- No tracking of donation clicks
- No visible donation goal/progress bar

### Existing Code to Reference

No similar existing features identified for reference. The implementation will follow existing patterns in puzzle.html:
- Header text styling (subtitle class uses #64748b color)
- Localization pattern using ui_text.json
- Button/link styling conventions already present

### Follow-up Questions

No follow-up questions needed. All requirements are clear.

## Visual Assets

### Files Provided:
- `bmc_qr.png` (in project root `/home/user/projects/ColorFocus/bmc_qr.png`): Buy Me A Coffee branded QR code with yellow coffee cup logo in center, black dotted pattern on white background. Standard square QR format, approximately 700x700 pixels.

### Visual Insights:
- QR code has Buy Me A Coffee branding (yellow coffee cup) embedded in center
- Black and white design will work well against the app's light gray (#f8fafc) background
- No custom mockups provided; implementation should follow existing UI patterns

## Requirements Summary

### Functional Requirements
- Header donation link: Text link reading "Support this project" (localized) positioned in header area
- Footer QR code: Display bmc_qr.png in footer area below Answer Key section
- Both elements link to: https://buymeacoffee.com/xwje4mbv3l
- Header link opens in new tab (target="_blank" with rel="noopener noreferrer")
- QR code can be static image (users scan with phone camera)
- All donation text must be localized in Chinese, English, Spanish, and Vietnamese

### Reusability Opportunities
- Extend existing ui_text.json with new translation keys for donation text
- Follow existing CSS patterns for secondary/subtle text styling
- Use existing responsive breakpoint patterns for mobile layout

### Scope Boundaries

**In Scope:**
- Header text link with localized "Support this project" text
- Footer QR code display using local bmc_qr.png asset
- Localization of donation link text in all 4 languages
- New tab behavior for external link
- Responsive styling for mobile devices
- Accessible implementation (proper link semantics, alt text for QR image)

**Out of Scope:**
- A/B testing infrastructure
- Donation popups or modals
- Click tracking or analytics
- Donation goal/progress indicators
- Buy Me A Coffee widget embedding
- External asset loading (keeping CSP simple)
- Any intrusive or prominent donation prompts

### Technical Considerations
- No changes needed to Content Security Policy (using local assets only)
- Add new translation keys to `/home/user/projects/ColorFocus/shared/ui_text.json`
- Copy or reference bmc_qr.png from project root to appropriate location
- Header link should use subtle styling (#64748b or similar) to match app aesthetic
- QR code in footer should be reasonably sized (not too large, not too small to scan)
- Ensure proper accessibility: meaningful alt text for QR image, proper link text
- Use rel="noopener noreferrer" on external link for security
