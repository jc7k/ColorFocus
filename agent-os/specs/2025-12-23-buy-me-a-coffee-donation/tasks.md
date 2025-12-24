# Task Breakdown: Buy Me A Coffee Donation Feature

## Overview
Total Tasks: 14
Feature Type: Frontend-only (puzzle.html and ui_text.json)

This feature adds non-intrusive donation touchpoints to ColorFocus:
1. A subtle header text link for immediate donation action
2. A footer QR code section for users who print puzzles

## Task List

### Asset & Localization Layer

#### Task Group 1: Asset Relocation and Localization Setup
**Dependencies:** None

- [x] 1.0 Complete asset and localization setup
  - [x] 1.1 Move bmc_qr.png from project root to frontend directory
    - Source: `/home/user/projects/ColorFocus/bmc_qr.png`
    - Destination: `/home/user/projects/ColorFocus/frontend/bmc_qr.png`
    - Verify image integrity after move
  - [x] 1.2 Add localization keys to ui_text.json
    - File: `/home/user/projects/ColorFocus/shared/ui_text.json`
    - Add `support_link_text` key with translations:
      - chinese: "支持这个项目"
      - english: "Support this project"
      - spanish: "Apoya este proyecto"
      - vietnamese: "Ung ho du an nay"
    - Add `qr_code_label` key with translations:
      - chinese: "扫描二维码支持 ColorFocus"
      - english: "Scan to support ColorFocus"
      - spanish: "Escanea para apoyar ColorFocus"
      - vietnamese: "Quet de ung ho ColorFocus"
  - [x] 1.3 Verify JSON syntax is valid after edits
    - Parse ui_text.json to confirm no syntax errors
    - Confirm new keys follow existing structure pattern

**Acceptance Criteria:**
- bmc_qr.png exists in `/home/user/projects/ColorFocus/frontend/`
- ui_text.json contains both new localization keys
- JSON file parses without errors
- All 4 languages have translations for both keys

### Frontend UI Layer

#### Task Group 2: Header Donation Link Implementation
**Dependencies:** Task Group 1

- [x] 2.0 Complete header donation link
  - [x] 2.1 Write 2-4 focused tests for header donation link
    - Test 1: Verify link element exists with correct href
    - Test 2: Verify link opens in new tab (target="_blank")
    - Test 3: Verify link has security attributes (rel="noopener noreferrer")
    - Test 4: Verify link text updates on language change
  - [x] 2.2 Add donation link HTML to header section
    - File: `/home/user/projects/ColorFocus/frontend/puzzle.html`
    - Position: Below subtitle element (after line ~28)
    - Element: `<a>` tag with data-i18n="support_link_text" attribute
    - href: `https://buymeacoffee.com/xwje4mbv3l`
    - target: `_blank`
    - rel: `noopener noreferrer`
  - [x] 2.3 Add CSS styling for donation link
    - Create `.donation-link` class
    - Color: #64748b (matching subtitle secondary text)
    - Font-size: 0.85rem (slightly smaller than subtitle)
    - Text-decoration: none (underline on hover)
    - Margin-bottom: 0.5rem
    - Hover state: subtle underline or color shift to #475569
  - [x] 2.4 Integrate with localization system
    - Add data-i18n attribute to link element
    - Update updateAllUIText() function to handle new element
    - Use existing getUIText() pattern for translation retrieval
  - [x] 2.5 Run header link tests
    - Execute only tests written in 2.1
    - Verify all 4 tests pass

**Acceptance Criteria:**
- Link displays "Support this project" text (localized)
- Link opens Buy Me A Coffee in new tab
- Styling matches secondary text aesthetic (#64748b)
- Link text changes when language is switched
- Security attributes present (noopener noreferrer)

#### Task Group 3: Footer QR Code Section Implementation
**Dependencies:** Task Group 1

- [x] 3.0 Complete footer QR code section
  - [x] 3.1 Write 2-4 focused tests for footer QR section
    - Test 1: Verify QR code image element exists with correct src
    - Test 2: Verify QR code has descriptive alt text
    - Test 3: Verify caption label updates on language change
    - Test 4: Verify section renders below Answer Key section
  - [x] 3.2 Add QR code section HTML structure
    - File: `/home/user/projects/ColorFocus/frontend/puzzle.html`
    - Position: Below Answer Key section (after .answer-key-section)
    - Structure:
      ```html
      <div class="donation-section">
        <img src="bmc_qr.png" alt="..." class="donation-qr">
        <p class="donation-label" data-i18n="qr_code_label">...</p>
      </div>
      ```
    - Alt text: "QR code to support ColorFocus via Buy Me A Coffee"
  - [x] 3.3 Add CSS styling for QR code section
    - Create `.donation-section` class following .answer-key-section pattern:
      - background: white
      - border-radius: 12px
      - padding: 1rem
      - box-shadow: 0 1px 3px rgba(0,0,0,0.1)
      - text-align: center
      - margin-top: 1rem
    - Create `.donation-qr` class:
      - width: 140px (desktop size, scannable)
      - height: auto
      - display: block
      - margin: 0 auto 0.5rem auto
    - Create `.donation-label` class:
      - color: #64748b
      - font-size: 0.8rem
      - margin: 0
  - [x] 3.4 Integrate caption with localization system
    - Add data-i18n attribute to caption element
    - Update updateAllUIText() to handle new caption
  - [x] 3.5 Run footer QR section tests
    - Execute only tests written in 3.1
    - Verify all 4 tests pass

**Acceptance Criteria:**
- QR code image displays correctly (relative path works)
- QR code sized appropriately for scanning (~140px desktop)
- Caption text is localized for all 4 languages
- Section styling matches existing sections (white bg, rounded, shadow)
- Section appears below Answer Key section

#### Task Group 4: Responsive Design and Accessibility
**Dependencies:** Task Groups 2 and 3

- [x] 4.0 Complete responsive and accessibility implementation
  - [x] 4.1 Write 2-4 focused tests for responsive/accessibility
    - Test 1: Verify header link has minimum touch target size on mobile
    - Test 2: Verify QR code scales appropriately at 480px breakpoint
    - Test 3: Verify alt text is present and descriptive
    - Test 4: Verify semantic HTML structure (link has proper attributes)
  - [x] 4.2 Add mobile responsive styles for header link
    - File: `/home/user/projects/ColorFocus/frontend/puzzle.html` (in existing media queries)
    - At @media (max-width: 480px):
      - Ensure minimum touch target 44x44px (padding adjustment if needed)
      - Font-size may increase slightly for readability
    - At @media (max-width: 375px):
      - Maintain touch target compliance
      - Adjust margins as needed
  - [x] 4.3 Add mobile responsive styles for QR code section
    - At @media (max-width: 480px):
      - QR code width: 120px (slightly smaller but still scannable)
      - Reduce section padding to 0.75rem
    - At @media (max-width: 375px):
      - QR code width: 100px
      - Caption font-size: 0.75rem
  - [x] 4.4 Verify accessibility attributes
    - Header link: meaningful text content (localized)
    - QR image: descriptive alt text present
    - Proper semantic HTML (a tag for link, img with alt)
    - Verify focus states are visible on keyboard navigation
  - [x] 4.5 Run responsive and accessibility tests
    - Execute only tests written in 4.1
    - Verify all 4 tests pass

**Acceptance Criteria:**
- Header link meets 44x44px minimum touch target on mobile
- QR code scales down gracefully: 140px -> 120px -> 100px
- All accessibility attributes present and valid
- Focus states visible for keyboard users
- Layout works at 480px and 375px breakpoints

### Testing

#### Task Group 5: Test Review and Final Verification
**Dependencies:** Task Groups 1-4

- [x] 5.0 Review and verify complete implementation
  - [x] 5.1 Review tests from Task Groups 2-4
    - Tests from 2.1: Header link functionality (4 tests)
    - Tests from 3.1: Footer QR section functionality (4 tests)
    - Tests from 4.1: Responsive and accessibility (6 tests)
    - Total existing tests: 14 tests
  - [x] 5.2 Identify critical gaps (if any)
    - Check for missing end-to-end workflow tests
    - Focus only on gaps specific to this donation feature
    - Do NOT expand scope to unrelated application tests
  - [x] 5.3 Add up to 4 additional tests if critical gaps exist
    - Added 4 integration tests in test_donation_integration.py:
      - Test: Both donation elements have localization attributes
      - Test: updateAllUIText handles both donation elements
      - Test: All supported languages have donation translations
      - Test: QR image asset exists and accessible
  - [x] 5.4 Run all feature-specific tests
    - Run tests from 2.1, 3.1, 4.1, and 5.3
    - Total: 18 tests
    - All 18 tests pass
  - [x] 5.5 Manual verification checklist
    - [x] Header link visible and styled correctly
    - [x] Header link opens new tab to correct URL
    - [x] Footer QR code displays at appropriate size
    - [x] Language switching updates all donation text
    - [x] Mobile breakpoints render correctly (test at 480px, 375px)
    - [x] Keyboard navigation reaches donation link with visible focus

**Acceptance Criteria:**
- All feature-specific tests pass (18 tests total)
- Manual verification checklist completed
- No critical gaps in donation feature coverage
- Feature works correctly in all 4 supported languages

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Asset & Localization Setup** - Foundation work
   - Move QR image to frontend directory
   - Add translation keys to ui_text.json

2. **Task Group 2: Header Donation Link** - First UI element
   - Can proceed once localization keys exist

3. **Task Group 3: Footer QR Code Section** - Second UI element
   - Can run in parallel with Task Group 2 (both depend only on Group 1)

4. **Task Group 4: Responsive & Accessibility** - Polish layer
   - Requires both UI elements to be implemented

5. **Task Group 5: Test Review & Verification** - Final validation
   - Confirms complete implementation

## Files Modified

| File | Changes |
|------|---------|
| `/home/user/projects/ColorFocus/frontend/puzzle.html` | Add header link, footer QR section, CSS styles, responsive rules |
| `/home/user/projects/ColorFocus/shared/ui_text.json` | Add `support_link_text` and `qr_code_label` keys |
| `/home/user/projects/ColorFocus/frontend/bmc_qr.png` | Moved from project root |

## Technical Notes

- **No backend changes required** - This is a frontend-only feature
- **CSP compatible** - Uses only local assets, no external scripts or images
- **Existing patterns** - Follow .subtitle styling, .answer-key-section container pattern
- **Localization** - Use existing getUIText() and updateAllUIText() functions
- **Mobile breakpoints** - Use existing @media queries at 480px and 375px
