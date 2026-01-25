# References: Stroop Guidance Messaging

## Reference Implementations

### mistakeSummarySection (puzzle.html ~line 1822-1878)
The existing summary panel structure to extend:
- Uses `.mistake-summary-section` container
- Has stats, legend, metadata, and buttons subsections
- Legend section uses `.mistake-legend` with `.legend-items`
- Shows/hides via `.visible` class toggle

### about modal (puzzle.html)
Reference for educational content sections:
- Uses `h3` for section headers
- Paragraph text for explanations
- Mobile-responsive layout

### displaySummary() function (puzzle.html ~line 4242)
Integration point:
- Calculates totalMistakes and stroopInfluencedCount
- Updates DOM elements with values
- Calls localized text via getUIText()
- Shows panel by adding `.visible` class

## CSS Reference Patterns

```css
/* Section container pattern from .mistake-legend */
.mistake-legend {
  background: var(--color-bg-surface);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
}

/* Header pattern */
.mistake-legend h3 {
  font-size: 0.875rem;
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-md);
  color: var(--color-text-primary);
}

/* Text content pattern */
.legend-text {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}
```

## UI Text Key Patterns

```json
{
  "summary_header": {
    "zh-TW": "錯誤分析摘要",
    "english": "Mistake Analysis Summary",
    "spanish": "Resumen de Analisis de Errores",
    "vietnamese": "Tom tat phan tich loi"
  }
}
```
