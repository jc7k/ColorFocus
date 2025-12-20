# Requirements

## Feature: Vietnamese Language Support

### Overview
Add Vietnamese as a supported language for color labels in the ColorFocus Stroop Puzzle.

### Requirements

1. **Vietnamese Color Labels**
   - Add Vietnamese translations for all 8 canonical colors
   - Ensure proper Unicode/diacritical mark support

2. **Language Selection**
   - Add UI control to switch between languages (Chinese, English, Vietnamese)
   - Persist language preference

3. **Data Structure Updates**
   - Update `shared/color_labels.json` with Vietnamese labels
   - Update backend `color_labels.py` if needed

4. **UI Updates**
   - Update puzzle.html to support language switching
   - Display color labels in selected language

### Vietnamese Color Names Reference
- Blue: Xanh dương / Xanh lam
- Orange: Cam
- Purple: Tím
- Black: Đen
- Cyan: Xanh lơ / Xanh ngọc
- Amber/Gold: Vàng hổ phách / Vàng
- Magenta: Hồng cánh sen / Đỏ tươi
- Gray: Xám

### Success Criteria
- User can select Vietnamese from a language dropdown
- Puzzle displays Vietnamese color words
- All 8 colors have accurate Vietnamese translations
- Stroop effect works with Vietnamese labels
