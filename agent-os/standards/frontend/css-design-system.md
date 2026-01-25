# CSS Design System

Apple-esque design optimized for elderly users and tablet interfaces.

## CSS Variables (`:root`)

```css
/* Colors */
--color-bg-page: #F5F5F7;
--color-bg-card: #FFFFFF;
--color-accent: #0071E3;
--color-success: #34C759;
--color-error: #FF3B30;

/* Typography */
--font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Spacing */
--space-sm: 0.5rem;
--space-md: 0.75rem;
--space-lg: 1rem;
--space-xl: 1.5rem;

/* Border Radius */
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;

/* Touch targets */
--btn-min-height: 44px;
```

## Mobile Breakpoint

```css
@media (max-width: 480px) {
  /* Mobile-specific overrides */
}
```

## Design Principles

- **System fonts** — Fast loading, native feel on all platforms
- **Rounded corners** — Friendly, accessible appearance
- **Subtle shadows** — Depth without distraction
- **High contrast** — Success green, error red, accent blue
