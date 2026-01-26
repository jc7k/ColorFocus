# File Size Limits

## Target Range
- **Target:** 300-500 lines per file
- **Refactor trigger:** When a file exceeds 300 lines, consider splitting
- **Hard limit:** No file should exceed 500 lines without documented justification

## Rationale
- Smaller files are easier to review and understand
- Reduces context window usage for AI-assisted development
- Encourages modular, single-responsibility design
- Faster navigation and debugging

## Measuring Lines
- Count all lines including blank lines and comments
- Use `wc -l <file>` for quick checks

## Exceptions
- Generated files (e.g., lock files, build artifacts)
- Third-party code
- CSS stylesheets (single-concern files can exceed limit)
- Files with documented justification in code comments

## When to Split
Split files when they:
1. Exceed 300 lines AND
2. Have multiple distinct responsibilities OR
3. Can be logically grouped into separate modules
