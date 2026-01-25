# Standards: Stroop Guidance Messaging

## Applicable Standards

### localization/ui-text-structure
- All user-facing text must be in `shared/ui_text.json`
- Keys use snake_case format (e.g., `guidance_education_header`)
- All 4 languages must have translations: zh-TW, english, spanish, vietnamese
- Dynamic values use {placeholder} syntax

### frontend/single-file-architecture
- All frontend changes go in `frontend/puzzle.html`
- CSS goes in the `<style>` section
- HTML goes in the appropriate document section
- JavaScript goes in the `<script>` section

### accessibility/touch-and-fonts
- Minimum 44px touch targets for any interactive elements
- Font sizes must be readable for elderly users
- Sufficient color contrast ratios
- Mobile responsive at 480px breakpoint

## Implementation Checklist

- [ ] All new UI text has entries in ui_text.json
- [ ] All 4 languages have complete translations
- [ ] CSS follows existing variable naming conventions
- [ ] HTML uses semantic elements with proper IDs for JS access
- [ ] JavaScript functions placed near related code
- [ ] Mobile breakpoint styles included
- [ ] Font sizes match or exceed existing summary section sizes
