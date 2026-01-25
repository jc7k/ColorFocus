# Frontend Test Patterns

vitest conventions for ColorFocus frontend.

## Run Tests

```bash
cd frontend && pnpm test
```

## Test Structure

```typescript
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load source JSON for comparison
const sourceJson = JSON.parse(
  readFileSync(resolve(__dirname, '../../../shared/colors.json'), 'utf-8')
);

describe('Feature Name', () => {
  it('should verify expected behavior', () => {
    expect(result).toBe(expected);
  });
});
```

## JSON Comparison Pattern

- Load source JSON with `readFileSync` at module level
- Compare TypeScript constants against source JSON
- Validates frontend stays in sync with shared data

## File Naming

- `*.test.ts` for test files
- Place tests alongside source: `colors.ts` → `colors.test.ts`
