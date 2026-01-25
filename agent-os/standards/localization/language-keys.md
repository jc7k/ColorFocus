# Language Keys

Language identifier conventions for i18n.

## Current Keys

| Key | Language | Notes |
|-----|----------|-------|
| `zh-TW` | Traditional Chinese | BCP 47 standard |
| `english` | English | Legacy format |
| `spanish` | Spanish | Legacy format |
| `vietnamese` | Vietnamese | Legacy format |

## Future Migration

Plan to standardize all keys to BCP 47:
- `english` → `en`
- `spanish` → `es`
- `vietnamese` → `vi`

## Default Language

- Default: `zh-TW` (app was built for Chinese-speaking stroke patient)
- Fallback: `english` if key/language not found

## Adding New Languages

For now, use lowercase word format to match existing pattern:
- Good: `french`, `german`, `japanese`
- Avoid: `fr`, `de`, `ja` (until full BCP 47 migration)
