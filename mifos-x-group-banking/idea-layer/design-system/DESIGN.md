# Design System — MifosSave

> Per-project design reference for **MifosSave** (mifos-x-group-banking) — an
> offline-first KMP community-banking app digitizing VSLA / ROSCA / ASCA / SHG
> group savings, lending, and share-out via Mifos Fineract.

Generated from §branding + §design_tokens + design_read on 2026-06-04.
Per RULE-DESIGN-MD-001 — this is the single source uploaded to Stitch and
consumed by every downstream design skill.

---

## Brand

| Field | Value |
|---|---|
| Display name | MifosSave |
| Tagline | Save together. Lend together. Grow together. |
| Logo concept | 5 members ringed around a shared corpus pool — VSLA/ROSCA visual metaphor. Primary green ring + members, amber center = pooled fund. |
| Voice / tone | Trustworthy, practical, calm — a digital ledger that mirrors the paper one. |

## Aesthetic

| Dial | Value | Meaning |
|---|---|---|
| Family | `minimalist-ui` | Clean financial admin |
| Variance | 3 / 10 | Grid-aligned, predictable |
| Motion | 3 / 10 | Subtle transitions only |
| Density | 7 / 10 | Dense financial dashboards |

**Quiet constraints**: `accessibility-first`, `regulated-industry`.

## Color tokens

### Primary (Material Green 800)
| Token | Value | Use |
|---|---|---|
| `--primary-900` | `#1B5E20` | Pressed states |
| `--primary-700` | `#2E7D32` | **Base primary** — app bars, primary CTAs |
| `--primary-500` | `#43A047` | Hover, focus highlight |
| `--primary-100` | `#C8E6C9` | Backgrounds, badges |

### Accent (Material Amber 700)
| Token | Value | Use |
|---|---|---|
| `--accent-700` | `#FF8F00` | **Base accent** — pooled fund visual, share-out emphasis |
| `--accent-500` | `#FFB300` | Hover |
| `--accent-100` | `#FFE082` | Backgrounds |

### Semantic
| Token | Value | Use |
|---|---|---|
| `--success` | `#2E7D32` | Approved, repaid, on-track (same as primary) |
| `--warning` | `#F57C00` | Overdue, attention |
| `--danger` | `#C62828` | Defaulted, rejected, fraud |
| `--info` | `#1565C0` | System notices |

### Neutral
| Token | Value | Use |
|---|---|---|
| `--bg-canvas` | `#FFFFFF` | Cards, sheets |
| `--bg-subtle` | `#FAFAFA` | App background |
| `--bg-muted` | `#F5F5F5` | Filled inputs |
| `--border-subtle` | `#EEEEEE` | Dividers |
| `--border-default` | `#E0E0E0` | Borders |
| `--text-primary` | `#212121` | Body text |
| `--text-secondary` | `#616161` | Metadata |
| `--text-disabled` | `#9E9E9E` | Disabled |

## Typography

- **Family**: Roboto (Android default) + SF Pro (iOS default) — system stack
- **Family mono**: Roboto Mono / SF Mono — for amounts in tables

| Size | px | line-height | weight |
|---|---|---|---|
| xs | 12 | 16 | 400 |
| sm | 14 | 20 | 400 |
| base | 16 | 24 | 400 |
| lg | 18 | 28 | 500 |
| xl | 20 | 28 | 500 |
| h3 | 24 | 32 | 600 |
| h2 | 30 | 36 | 600 |
| h1 | 36 | 44 | 700 |

## Spacing — 8dp grid

`xs:4 · sm:8 · md:12 · base:16 · lg:24 · xl:32 · 2xl:48`

## Radius — medium preset

`sm:8 · md:12 · base:16 · lg:24 · full:9999`

Reason: VSLA groups handle physical currency notes (rounded forms feel
friendly + tangible); medium radii also test better with low-literacy
users who interpret "card edges" as separate paper documents.

## Motion — gentle preset

`fast:150ms · base:200ms · slow:300ms` · easing: `cubic-bezier(0.4, 0, 0.2, 1)`

Respect `prefers-reduced-motion`: collapse all transitions to 0ms.

## Elevation

`sm` 1dp · `base` 2dp · `md` 4dp · `lg` 8dp — used sparingly; the
admin surfaces favor borders over shadows for offline-render performance.

## Component conventions

- **Top app bar** — primary fill (#2E7D32), white text, 56dp height
- **Bottom nav** — 4-5 tabs, primary-tinted active, surface-fill rest
- **Cards** — `--bg-canvas` fill, `--border-subtle` border, `medium` radius
- **Tables** — Roboto Mono for amounts; 44dp row height (touch-target safe)
- **Status chips** — semantic palette (success/warning/danger/info); 12sp text
- **FAB** — accent #FF8F00 fill for member-add / new-claim primary actions
- **Bottom sheets** — drag handle, 16dp top radius, 24dp inset

## Accessibility

- **Contrast**: WCAG AA across all text + interactive elements
- **Touch targets**: minimum 44×44dp
- **Focus ring**: 2dp solid `--primary-700`, 2dp offset
- **Reduced motion**: respected via prefers-reduced-motion media query
- **Text scaling**: support up to 200% font scale without layout breakage
- **Screen reader**: every interactive element has aria-label or visible text

## Offline-first considerations

Per §technical_decisions, this app must work fully offline with eventual
Fineract sync. Design implications:

- Sync-status indicator visible on every primary surface (top app bar)
- Disabled-state styling clear when an action requires network (e.g.
  remote loan-approval)
- Optimistic UI for in-group operations (savings deposits, share-out
  calculations); rollback styling for sync conflicts (warning palette)
- "Last synced" timestamp on every list view
