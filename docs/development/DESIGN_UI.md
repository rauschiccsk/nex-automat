# NEX Manager — UI Design Tokens

Single source of truth for colors, radii, and surface elevation across the
NEX Manager web frontend (`apps/frontend/nex-manager`). All visual decisions
live here; components consume tokens, never raw hex.

- **Token source**: `src/index.css` `@theme` block (Tailwind v4)
- **Consumed by**: shell components (Tailwind utility classes), `BaseGrid`,
  `BaseAgGrid` (CSS custom properties read at runtime)
- **Scope**: dark mode only — light mode uses Tailwind / AG Grid balham
  defaults which already match the light shell

---

## Why this exists

Before Phase K, dark-mode colors lived in three places:

1. App shell — Tailwind classes (`dark:bg-gray-900`, `dark:bg-gray-800`)
2. `BaseAgGrid` — hex literals inline in JS (`#111827`, `#1f2937`, …)
3. Legacy `BaseGrid` — its own Tailwind classes

Same intent, three definitions. Phase K consolidates to one definition (the
`@theme` block) that both Tailwind and AG Grid read from.

---

## Token reference

### Surfaces

| Token | Value | Tailwind utility | Used for |
|---|---|---|---|
| `--color-surface-base` | `#111827` (gray-900) | `bg-surface-base` | App shell, sidebar, grid body |
| `--color-surface-elevated` | `#1f2937` (gray-800) | `bg-surface-elevated` | Header, tabbar, grid header, row hover, selected tab |
| `--color-surface-translucent` | `rgba(31, 41, 55, 0.5)` | n/a (used in JS only) | Grid zebra stripe (odd rows) |

**Elevation rule**: a surface that sits visually *above* another uses
`surface-elevated`. Hover and active states also bump one level — a row
hovered on `surface-base` becomes `surface-elevated`.

### Borders

| Token | Value | Tailwind utility | Used for |
|---|---|---|---|
| `--color-border-subtle` | `#374151` (gray-700) | `border-border-subtle` | Cell borders, dividers between sections |

### Content (text)

| Token | Value | Tailwind utility | Used for |
|---|---|---|---|
| `--color-content-primary` | `#f3f4f6` (gray-100) | `text-content-primary` | Body text in grids and headers |

Decision: grids use the higher-contrast `gray-100` (not the shell's lighter
`gray-300`) because rows are 24px tall — readability beats shell uniformity.
This is intentional, not a drift.

### Accents

| Token | Value | Tailwind utility | Used for |
|---|---|---|---|
| `--color-accent-selected` | `#1e3a8a` (blue-900) | `bg-accent-selected` | Selected row in grids |

### Radii

| Token | Value | Tailwind utility | Used for |
|---|---|---|---|
| `--radius-input` | `4px` | `rounded-input` | Filter inputs, small text inputs (matches shell input rounding) |

---

## How to consume tokens

### From a shell / Tailwind component

```tsx
<div className="dark:bg-surface-base dark:text-content-primary">
  ...
</div>
```

Tailwind v4 generates these utilities automatically from the `@theme` block.

### From AG Grid (`BaseAgGrid`)

AG Grid v35 JS Theming API takes hex strings, so we read CSS variables at
runtime:

```ts
const css = getComputedStyle(document.documentElement)
const token = (name: string) => css.getPropertyValue(name).trim()

themeBalham.withPart(colorSchemeDark).withParams({
  backgroundColor: token('--color-surface-base'),
  foregroundColor: token('--color-content-primary'),
  // ...
})
```

This is intentionally in `BaseAgGrid.tsx` only — no other component should
re-implement this pattern. If you need an AG Grid color outside `BaseAgGrid`,
add it to that file's params object.

### Inline styles (last resort)

```tsx
<div style={{ backgroundColor: 'var(--color-surface-base)' }} />
```

Avoid this — prefer Tailwind utility classes whenever possible.

---

## Adding a new token

1. Add the variable to the `@theme` block in `src/index.css` with a
   semantic name (`surface-*`, `content-*`, `border-*`, `accent-*`,
   `radius-*`) — never a palette name like `gray-700`.
2. Update the table above (token, value, utility, usage).
3. If AG Grid needs it, wire it in `BaseAgGrid.tsx` `theme` useMemo.
4. Document the *why* if the choice is non-obvious (e.g. zebra translucency
   uses 50% so it works without changing on row hover).

---

## Anti-patterns

- ❌ Hardcoded hex (`#111827`) anywhere in `.tsx` / `.ts` files
- ❌ Tailwind palette classes (`bg-gray-900`) in *new* code — use
  `bg-surface-base` instead. Existing `dark:bg-gray-900` etc. across the
  shell will be migrated incrementally; do not block PRs on it.
- ❌ Per-component CSS variables (`--my-component-bg`) — extend the global
  `@theme` block instead so the token is reusable.
- ❌ AG Grid CSS overrides outside `src/index.css` — keep all `.ag-*`
  overrides in one place for discoverability.

---

## Phase K decisions log

| Decision | Choice | Rationale |
|---|---|---|
| Token mechanism | Tailwind v4 `@theme` block | Single source generates Tailwind utilities + JS-readable CSS vars; aligned with D-008 (Tailwind v4) |
| Zebra stripes in AG Grid | Yes — `rgba(31,41,55,0.5)` on odd rows | Legacy NEX Genesis convention; helps eye tracking on 250k-row catalogs |
| Filter input border-radius | Yes — 4px override | Consistency with rest of shell inputs (otherwise filter inputs are sharp-cornered while everything else is rounded) |
| Body text color in grids | `gray-100` (not shell's `gray-300`) | Readability at 24px row height beats shell uniformity |

Approved by Director on 2026-04-28.
