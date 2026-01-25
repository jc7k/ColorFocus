# Platform Consumer Pattern

How to consume shared JSON in Python and TypeScript.

## Python Pattern

```python
from enum import StrEnum
from pathlib import Path
import json

class ColorToken(StrEnum):
    BLACK = "BLACK"
    # ... one entry per JSON key

def _load_from_json():
    # Resolve relative to THIS file, not cwd
    json_path = Path(__file__).parent.parent.parent.parent / "shared" / "colors.json"
    with open(json_path) as f:
        return json.load(f)

COLORS = _load_from_json()  # Load at import time
```

## TypeScript Pattern

```typescript
import colorsData from '../../../shared/colors.json';

export enum ColorToken {
  BLACK = 'BLACK',
  // ... one entry per JSON key
}

export const COLORS: Record<ColorToken, string> = colorsData;
```

## Common Mistakes

- **Wrong path resolution**: Always use `Path(__file__)` in Python, not hardcoded paths
- **Missing enum sync**: When JSON keys change, update StrEnum in both platforms
- **Load timing**: Load at module import time, not per-function-call
