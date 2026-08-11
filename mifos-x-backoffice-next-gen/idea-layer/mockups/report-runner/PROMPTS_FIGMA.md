<!-- source: screens/report-runner/ui.yaml -->
<!-- source_hash: ui=e5e1521275c6 docs=65310dcfb2a5 -->
<!-- generated: 2026-07-31T00:00:00Z -->

# Report Runner — Figma Design Hand-off Prompts

> Generated from `screens/report-runner/ui.yaml` (+ `docs.yaml`, `flow.yaml`, `demo-data.yaml`) by `/idea-feature-mockup`.
> Design system: `idea-layer/design-system/design-tokens.yaml` · Generated: 2026-07-31.
> Format: natural-language design instructions for Figma AI / a human designer — paste any section as a standalone brief.
> Canvas: 393×852dp (Pixel 5 reference), Material 3, **light theme default** (dark available), Roboto (Roboto Mono for numerics).
> Archetype: `detail_screen` · Module: `m14-reports-search-audit` · Initial state: `loading`.

---

## Section 1: Design System Context

Set up the following as Figma **local variables** (a single collection, `mifos-x-backoffice-next-gen`, with a `light`/`dark` mode pair) before laying out any screen. Every color below is quoted with its resolved hex so the variable can be created directly without resolving a token indirection.

### Colors — Light theme (default UX surface)

Create these as color variables in **light** mode:

- `primary` `#0091EA` — brand identity Light Blue. Use for large/bold filled-button labels and icons only; it is the seed color of the whole system.
- `on-primary` `#FFFFFF` — text/icon drawn on a `primary` fill.
- `primary-container` `#CBE6FF` and `on-primary-container` `#001E30` — prefer this pairing over `primary`/`on-primary` for AA-critical body text on a primary-tinted surface (the raw `on-primary` on `primary` pairing is ~2.6:1, below WCAG-AA 4.5:1 for body text).
- `primary-hover` `#0081D0` and `primary-pressed` `#0072B8` — interaction-state fills for the Run button.
- `secondary` `#00796B` and `on-secondary` `#FFFFFF` — teal accent, used sparingly for the Export action.
- `secondary-container` `#B8F2E6` and `on-secondary-container` `#00201A`.
- `tertiary` `#5B5891` / `on-tertiary` `#FFFFFF` / `tertiary-container` `#E3DFFF` / `on-tertiary-container` `#17124B` — muted indigo for informational chips.
- `error` `#BA1A1A` / `on-error` `#FFFFFF` / `error-container` `#FFDAD6` / `on-error-container` `#410002` — the error state icon, headline, and Retry surface accents.
- `success` `#2E7D32` / `on-success` `#FFFFFF` / `success-container` `#C8E6C9` — not used directly on this read-only screen but kept in the shared palette for consistency with other modules.
- `warning` `#F57C00` / `on-warning` `#FFFFFF` / `warning-container` `#FFDDB8` / `warning-strong` `#B45309` — used for high-risk emphasis when the selected report is Portfolio at Risk (a Chart-type report showing risk bands).
- `background` `#FCFCFF` and `on-background` `#1A1C1E`.
- `surface` `#FCFCFF` and `on-surface` `#1A1C1E` — the app-bar, parameter-form, and result-table background/ink.
- `surface-variant` `#DEE3EB` and `on-surface-variant` `#42474E` — parameter field fills, the table header row, and shimmer-skeleton fills.
- `surface-container-low` `#F3F4F9`, `surface-container` `#EDEFF4`, `surface-container-high` `#E7E9EF` — nested card elevations for the parameter form and result card.
- `outline` `#72777F` and `outline-variant` `#C2C7CF` — 1px hairline borders (this system prefers outline borders over drop shadows).
- `inverse-surface` `#2F3033` / `inverse-on-surface` `#F1F0F4` / `inverse-primary` `#6FD3FF` — for a brief "Checksum copied"-style snackbar if one is ever added to this screen.
- `accent` `#00BFA5` / `on-accent` `#00201A` — bright teal, reserve for at most one emphasis chip per screen (not used more than twice here).

### Figma variable naming map (semantic token → Figma variable)

Name the Figma variables exactly as follows so downstream dev-mode inspection matches the codebase's token names one-to-one:

| Semantic token | Figma variable name | Resolved (light) | Resolved (dark) |
|---|---|---|---|
| `colors.light.primary` | `color/primary` | `#0091EA` | `#6FD3FF` |
| `colors.light.on_primary` | `color/on-primary` | `#FFFFFF` | `#00344F` |
| `colors.light.secondary` | `color/secondary` | `#00796B` | `#4FD8C4` |
| `colors.light.error` | `color/error` | `#BA1A1A` | `#FFB4AB` |
| `colors.light.warning` | `color/warning` | `#F57C00` | `#FFB868` |
| `colors.light.surface` | `color/surface` | `#FCFCFF` | `#1A1C1E` |
| `colors.light.surface_variant` | `color/surface-variant` | `#DEE3EB` | `#42474E` |
| `colors.light.on_surface` | `color/on-surface` | `#1A1C1E` | `#E2E2E6` |
| `colors.light.on_surface_variant` | `color/on-surface-variant` | `#42474E` | `#C2C7CF` |
| `colors.light.outline` | `color/outline` | `#72777F` | `#8C9198` |
| `spacing.md` | `spacing/md` | `16px` | (mode-independent) |
| `spacing.section_gap` | `spacing/section-gap` | `24px` | (mode-independent) |
| `radius.sm` | `radius/sm` | `8px` | (mode-independent) |
| `radius.xl` | `radius/xl` | `28px` | (mode-independent) |
| `typography.body_medium` | `text/body-medium` | 14/20 w400 | (mode-independent) |

### Colors — Dark theme (mode flip)

Create the parallel **dark** mode values: `primary` `#6FD3FF` / `on-primary` `#00344F` / `primary-container` `#004B70` / `on-primary-container` `#CBE6FF`; `secondary` `#4FD8C4` / `on-secondary` `#003731`; `error` `#FFB4AB` / `on-error` `#690005` / `error-container` `#93000A`; `warning` `#FFB868` / `warning-strong` `#E0912F`; `background`/`surface` `#1A1C1E` / `on-surface` `#E2E2E6`; `surface-variant` `#42474E` / `on-surface-variant` `#C2C7CF`; `outline` `#8C9198`. Bind every layer's fill/stroke to the variable, not a hard-coded hex, so toggling the Figma page mode previews both themes.

### Typography

Map these to Figma text styles, family **Roboto** (numerics use **Roboto Mono**):

- `title-large` 22/28 weight 600 — the app-bar report name.
- `title-medium` 16/24 weight 500 — parameter labels, empty/error headlines.
- `label-large` 14/20 weight 500 — button labels, column headers.
- `label-medium` 12/16 weight 500 — helper captions under fields.
- `body-large` 16/24 weight 400 — parameter values.
- `body-medium` 14/20 weight 400 — result-table cell text, guidance copy.
- `body-small` 12/16 weight 400 — footnotes (e.g. "generated at" timestamp).
- **Mono** (Roboto Mono) 14/20 — every result-table numeric cell (Principal, Outstanding), so vertical columns of digits align on the decimal point.

### Spacing & Shape

8pt grid, 4dp base unit: `xs` 4dp, `sm` 8dp, `md` 16dp, `lg` 24dp, `xl` 32dp. This is a dense console (density 7) so use the tuned `row-padding` 12dp for table rows and `section-gap` 24dp between the parameter form and the result card. Corner radius: `sm` 8dp for input fields, `lg` 16dp for cards, `xl` 28dp for filled buttons (Run/Export), `full` for the Retry button's ripple mask only. Elevation is intentionally subtle — prefer a 1px `outline` border over a drop shadow; where a shadow is unavoidable (e.g. a dropdown menu popover) use `level2` (`0 2px 6px rgba(0,0,0,0.08)`).

### WCAG compliance notes

- Body text on `background`/`surface` (`on-surface` `#1A1C1E` on `#FCFCFF`) exceeds 4.5:1 — safe for all body copy.
- Do **not** put `body-medium` text directly on a raw `primary` `#0091EA` fill (contrast ~2.6:1, fails AA). Use `on-primary-container`/`primary-container` for any text-bearing primary-tinted surface; reserve raw `primary`/`on-primary` for large, bold button labels and icons only (the Run button label at `label-large` 14/20 weight 500 is borderline — keep it bold-weighted and short, "Run report", exactly as the M3 button spec intends).
- All interactive targets (Run, Export, Retry, each parameter field, each sortable column header) meet the 48×48dp minimum touch target (`touch_targets.comfortable`).
- Sort direction and error/empty states must never be color-only — pair every color cue with a glyph or label (e.g. the sort arrow glyph, the `[!]` error icon, explicit "No rows" copy).
- Focus indicators: 2dp `focus` ring in `primary`, visible on every focusable field/button for keyboard/switch-access navigation.

---

## Section 2: Screen Layouts

There is one screen, `report-runner`, with four states. All four share the same **Top App Bar** (small M3 variant, 56dp height, `surface` `#FCFCFF` fill, 1px bottom `outline` border, back-arrow leading icon at 24dp in `on-surface`, title = the selected report's name in `title-large`). Bottom navigation is suppressed (this is a detail/leaf screen); there is no FAB.

### Layout: `loading`

- Type: vertical scroll, single column, `md` (16dp) horizontal padding.
- Sections (render order): (1) Top App Bar (fixed), (2) parameter-form shimmer block — 4 stacked skeleton rows (`surface-variant` fill, `sm` radius, 1.2s pulse), each matching the real field's height (56dp). No result card is rendered in this state.
- Component render order: TopAppBar → ShimmerRow×4.

### Layout: `content`

- Type: vertical scroll, single column, `md` (16dp) horizontal padding, `section-gap` (24dp) between the parameter-form card and the result card.
- Sections (render order):
  1. **parameter-form card** — width: full minus 32dp margins; layout: column; contains N `rr_param` fields (Office dropdown, Loan Officer dropdown cascaded from Office, From-date picker, To-date picker, Currency dropdown), each a labeled row (label above field, `label-large` label + `body-large` value), followed by the `rr_run` primary button right-aligned beneath the last field.
  2. **result section** — a divider labeled "Result" (`label-large`, `on-surface-variant`), then either: (a) a **sortable table** (Table-type report) with a `rr_sort`-driven header row (columns right-aligned when numeric, Roboto Mono body) and 3+ data rows, horizontally scrollable if columns overflow 393dp; or (b) a **chart render** (Chart-type report, e.g. Portfolio at Risk) filling the same card footprint. Beneath the result, the `rr_export` secondary button.
- Component render order: TopAppBar → rr_param×N → rr_run → SectionDivider("Result") → (ResultTable[rr_sort×N, rows] | ResultChart) → rr_export.
- **Auto Layout — parameter-form card**: direction vertical, padding 16dp all sides, item spacing 8dp, alignment top-left, hug contents height, fill container width (minus the 16dp screen margin already applied by the parent frame).
- **Auto Layout — result card**: direction vertical, padding 16dp top/bottom, 0dp left/right (the table itself manages its own 16dp inset per row so the horizontal-scroll region can bleed to the card edge), item spacing 12dp (`row-padding`), alignment top-left, hug contents height.

### Layout: `empty`

- Type: vertical scroll; the parameter-form card stays exactly as in `content` (still adjustable); below it, a **centered empty-state block** replaces the result card: 200×200dp illustration placeholder area, `title-medium` headline "No results", `body-medium` guidance copy ("Try widening the date range or choosing a different office"), no CTA button (the existing parameter form already offers the adjust affordance).
- Component render order: TopAppBar → rr_param×N → rr_run → EmptyStateBlock.

### Layout: `error`

- Type: vertical scroll; the parameter-form section is **not** rendered in this state when the failure is `parameters_load_failed` (metadata itself failed) — only the Top App Bar plus a centered error block. When the failure is `report_run_failed` (metadata resolved fine, only the run failed), keep the parameter-form card visible above the error block so the operator's inputs are not lost, matching the `error_run_failed_shows_retry` test scenario.
- Sections (render order, `parameters_load_failed` case): Top App Bar → centered ErrorBlock (48dp `[!]` icon in `error` → headline "Couldn't load report parameters" → body copy → `rr_error_retry` filled primary button, 140×48dp).
- Sections (render order, `report_run_failed` case): Top App Bar → rr_param×N (disabled or read-only) → rr_run → ErrorBlock (headline "Couldn't run this report" → body copy → `rr_error_retry`).

---

## Section 3: Component Specifications

### Component: Top App Bar

Auto Layout: horizontal, 56dp height, full width, padding 4dp/16dp, space-between alignment. Background `surface` `#FCFCFF`, 1px bottom stroke `outline` `#72777F`. Leading: 24×24dp back-arrow icon, `on-surface` `#1A1C1E`, 44dp tap target, contentDescription "Navigate back". Title: `title-large` `on-surface`, single line, ellipsis-truncated, text = the currently selected report's name (e.g. "Active Loans by Loan Officer"). No trailing actions on this screen.

### Component: `rr_param` (dynamic_form_field) — Office / Loan Officer / dates / currency

Dimensions: full width minus 32dp side margins, 56dp height per field, 8dp vertical gap between stacked fields. Corner radius `sm` (8dp). Visual pattern: outlined dropdown/date-picker field — fill `surface-variant` `#DEE3EB`, 1px `outline` stroke, label `label-large` `on-surface-variant` positioned above the field, value `body-large` `on-surface`. For dropdown-type parameters (Office, Loan Officer, Currency), a trailing 20dp chevron icon in `on-surface-variant`; for date-type parameters (From date, To date) a trailing 20dp calendar icon.

- **States**: Loading → the field is replaced entirely by a shimmer block of the same 56dp height (`surface-variant` fill, no border, 1.2s pulse). Content → populated with the resolved option/value. Disabled (dependent parameter not yet resolvable, e.g. Loan Officer before Office is chosen) → 38% opacity overlay, non-interactive.
- **Interaction**: `on_click.action: param_change`, effect `transform_state`. Selecting an Office value cascades — the Loan Officer dropdown's option list re-resolves scoped to the new `officeId` (no full-screen refetch, only the dependent field re-populates).
- **Content** (real, from `demo-data.yaml#parameters`): Office options — "Head Office" (id 1), "Nairobi CBD" (id 3), "Kisumu Central" (id 5). Loan Officer options when Office = Nairobi CBD (id 3) — "Peter Kariuki" (id 41), "Mercy Achieng" (id 45). Selected demo state: Office = Nairobi CBD, Loan Officer = Peter Kariuki.
- **Accessibility**: contentDescription per field, e.g. "Office parameter, currently Nairobi CBD, opens a dropdown of offices"; role: dropdown / date-picker; 48dp minimum touch target on the whole row, not just the chevron.
- **Component variants** (create as a single Figma component with these variant properties): `default` (resting — `outline` 1px stroke, `on-surface-variant` label); `hovered` (desktop/tablet pointer only — stroke brightens to `on-surface-variant`, subtle 8% state-layer overlay); `focused` (2dp `primary` focus ring replaces the `outline` stroke, label color shifts to `primary`); `pressed` (12% `on-surface` state-layer overlay while the dropdown/date-picker is open); `disabled` (38% opacity overlay, non-interactive, used for a not-yet-resolvable dependent parameter). Bind each variant's stroke/fill/label color to the Section 1 variables so theme-mode toggling previews correctly.

### Component: `rr_run` (button, primary, `gated_permission: READ_REPORT`)

Dimensions: 140×48dp minimum (grows to fit label + padding), corner radius `xl` (28dp), right-aligned beneath the parameter form. Fill `primary` `#0091EA`; label "Run report" in `label-large` `on-primary` `#FFFFFF`, bold weight for AA-safe contrast on the primary fill. Disabled state (required parameters not yet set): fill drops to `surface-variant` `#DEE3EB`, label `on-surface-variant` at 38% opacity, non-interactive.

- **Interaction**: `on_click.action: run_report`, effect `call_api` — fires `GET /v1/runreports/{reportName}` with the captured `R_` parameters, cache-first through Store5 keyed by the parameter hash.
- **Accessibility**: contentDescription "Run the selected report with the chosen parameters"; when disabled, additionally announce "disabled, required parameters not set".
- **Component variants**: `default` (fill `primary` `#0091EA`, label `on-primary`); `hovered` (fill `primary-hover` `#0081D0`); `pressed` (fill `primary-pressed` `#0072B8` + 12% state-layer overlay, 100ms short2 transition); `focused` (adds a 2dp `primary` outer focus ring, 2dp offset); `disabled` (fill `surface-variant` `#DEE3EB`, label `on-surface-variant` at 38% opacity, no elevation, non-interactive — required parameters not yet set).

### Component: Result table (sortable, Table-type reports)

Dimensions: full width minus 32dp margins, horizontally scrollable if the column set overflows 361dp (393dp canvas minus margins), row height 44dp (`row-padding` 12dp top/bottom), header row height 48dp. Header row fill `surface-variant` `#DEE3EB`; data rows alternate `surface` `#FCFCFF` / `surface-container-low` `#F3F4F9` for scan-ability; 1px `outline-variant` divider between rows.

- **`rr_sort` (table_header)**: each column header is tappable, `label-large` `on-surface-variant`, numeric columns right-aligned. The active sort column shows a small ▲/▼ glyph in `primary` immediately after the label — sort direction is never color-only.
- **Content** (real, from `demo-data.yaml#run_result` for "Active Loans by Loan Officer"): columns **Client** (STRING), **Account No** (STRING), **Principal** (DECIMAL, KES), **Outstanding** (DECIMAL, KES). Rows: "Grace Wanjiru Mwangi" / "000055231" / "KES 60,000.00" / "KES 42,500.00"; "Samuel Otieno Odhiambo" / "000055240" / "KES 45,000.00" / "KES 31,000.00"; "Fatuma Njeri Kimani" / "000055299" / "KES 52,000.00" / "KES 48,800.00". Principal and Outstanding cells render in **Roboto Mono**, right-aligned so the decimal points align vertically.
- **Interaction**: tapping a header sorts in-VM only (no refetch) — `transform_state`.
- **Accessibility**: table has a group contentDescription "Report result, N rows, sorted by {column} {direction}"; each header announces "Sort by {column name}, currently {ascending/descending/unsorted}".
- **Component variants** (`rr_sort` header cell): `default` (unsorted — `label-large` `on-surface-variant`, no glyph); `hovered` (desktop pointer — 8% state-layer overlay); `pressed` (12% state-layer overlay, 100ms); `focused` (2dp `primary` focus ring around the header cell); `active-ascending` / `active-descending` (label color shifts to `primary`, trailing ▲/▼ glyph in `primary`).

### Component: Result chart (Chart-type reports, e.g. Portfolio at Risk)

Dimensions: full width minus 32dp margins, 240dp height, `radius-lg` (16dp) card with 1px `outline` border (no shadow). Auto Layout: vertical, 16dp padding, 8dp gap between the chart canvas and its legend row. Renders the same result payload as a bar/line chart instead of a table when the selected report's `reportType` is `Chart` (e.g. Portfolio at Risk). Use `warning` `#F57C00` for above-threshold risk bands and `primary` `#0091EA` for the baseline series — never risk-color-only, always pair with a value label. Legend row beneath the chart: two 12×12dp swatches (`primary`, `warning`) each followed by a `label-medium` caption ("Baseline", "At risk") in `on-surface-variant`. Y-axis labels and the KES value callouts render in Roboto Mono, matching the table's numeric typography for visual consistency across report types.

### Component: `rr_export` (button, secondary)

Dimensions: 120×48dp minimum, corner radius `xl` (28dp), positioned bottom-right beneath the result card. Fill `surface` with a `secondary` `#00796B` 1px stroke and `secondary` label (outlined/tonal secondary style), "Export" in `label-large`.

- **Interaction**: `on_click.action: export_report`, effect `share_external` — renders the current result set (respecting the active sort + the applied parameters) to CSV/PDF and hands off to the platform share sheet.
- **States**: disabled until a result exists (no result to export in `loading`/`empty`/pre-run `content`); on export failure, an inline `body-small` error caption appears beneath the button ("Export failed — try again") without disturbing the retained result.
- **Accessibility**: contentDescription "Export the report result"; announce success/failure via a transient live-region message, not a modal.
- **Component variants**: `default` (outlined — `surface` fill, 1px `secondary` `#00796B` stroke, `secondary` label); `hovered` (8% `secondary` state-layer tint over the fill); `pressed` (12% `secondary` state-layer overlay); `focused` (2dp `secondary` focus ring); `disabled` (1px `outline-variant` stroke, `on-surface-variant` label at 38% opacity — no result yet to export).

### Component: Empty-state block

Dimensions: centered column, 200×200dp illustration placeholder area (`on-surface-variant` tinted icon), 16dp gap to `title-medium` headline "No results" (`on-surface`), 8dp gap to `body-medium` guidance copy "No rows returned for the selected parameters — try widening the date range or choosing a different office" (`on-surface-variant`). No CTA button — the parameter form above remains the adjustment affordance.

### Component: Error block + `rr_error_retry`

Dimensions: centered column, 48dp `[!]` icon in `error` `#BA1A1A`, 16dp gap to `title-medium` headline ("Couldn't load report parameters" or "Couldn't run this report" depending on which call failed), 8dp gap to `body-medium` copy in `on-surface-variant`, 16dp gap to the `rr_error_retry` button — 140×48dp, corner radius `md` (12dp), fill `primary` `#0091EA`, label "Retry" `label-large` `on-primary`.

- **Interaction**: `on_click.action: retry`, effect `call_api` — re-resolves the parameter metadata (transitions back to `loading`) or re-runs the report, depending on which step failed.
- **Accessibility**: contentDescription "Retry loading the report catalog"; the whole error block is announced as a single alert region on entry.
- **Component variants**: `default` (fill `primary` `#0091EA`, label `on-primary`, matches `rr_run`'s default styling for visual consistency); `hovered` (fill `primary-hover` `#0081D0`); `pressed` (fill `primary-pressed` `#0072B8` + 12% overlay); `focused` (2dp `primary` outer focus ring). No `disabled` variant — Retry is always actionable once the error block renders.

### Component: Shimmer skeleton (loading state)

Dimensions: mirrors the real field it stands in for (56dp per parameter row). Fill `surface-variant` `#DEE3EB`, corner radius `sm` (8dp), 1.2s ease-in-out pulse animation between 100% and 60% opacity. No text, no icons — purely a placeholder shape. Create as a single component with two variants: `pulsing` (the default, animated state, used while `loading`) and `static` (a non-animated reference frame for designers who need a still screenshot).

### Component: Date-range validation caption (inline, `content` state only)

Dimensions: full width, 20dp height, sits directly beneath the To-date `rr_param` field. Not present in the default demo state (From/To dates are valid) — only renders when the operator picks a To-date earlier than the From-date. Text `body-small` in `error` `#BA1A1A`: "To date must be after the from date." This is a purely client-side validation caption (no network round-trip); its presence also disables `rr_run` until corrected, reusing `rr_run`'s `disabled` variant from above.

### Component summary (Figma components panel)

| ui.yaml id | Figma component name | Variant count | Effect |
|---|---|---|---|
| `rr_param` | `ReportParamField` | 5 (default/hovered/focused/pressed/disabled) | transform_state |
| `rr_run` | `RunReportButton` | 5 (default/hovered/pressed/focused/disabled) | call_api |
| `rr_sort` | `SortableColumnHeader` | 5 (default/hovered/pressed/focused/active) | transform_state |
| `rr_export` | `ExportButton` | 5 (default/hovered/pressed/focused/disabled) | share_external |
| `rr_error_retry` | `RetryButton` | 4 (default/hovered/pressed/focused — no disabled) | call_api |
| n/a | `ShimmerSkeletonRow` | 2 (pulsing/static) | — (loading placeholder) |
| n/a | `ResultTableRow` | 2 (odd/even, for the alternating-row scan pattern) | — |
| n/a | `ResultChartCard` | 1 (single visual, data-driven) | — |
| n/a | `EmptyStateBlock` | 1 | — |
| n/a | `ErrorBlock` | 2 (parameters_load_failed copy / report_run_failed copy) | — |

---

## Section 4: Interaction Patterns

### Prototype interaction flow (Figma prototype tab)

Wire the following click-through in Figma's Prototype tab so the hand-off is testable end-to-end. From `m01-dashboard`, the "Portfolio at Risk" tile → navigates to `report-runner` (`content`, PAR pre-scoped) using a "slide in from right" transition. From `m14-reports-search-audit`, tapping any report row → navigates to `report-runner` (`loading` first, then auto-advances to `content` once parameter resolution completes — simulate with a 400ms delayed transition in the prototype). Within `report-runner`: tapping `rr_run` → "change to" the populated result variant of `content` (smart-animate the result-card region only, everything above stays pinned). Tapping any `rr_sort` header → "change to" a re-ordered `content` variant (smart-animate row positions). Tapping `rr_export` → "open overlay" simulating the native share sheet (a bottom-sheet overlay is an acceptable Figma stand-in for the platform share sheet). Tapping `rr_error_retry` on the `error` frame → "change to" the `loading` frame, then auto-advance back to `content` on a delayed transition, closing the retry loop. Selecting a different Office in `rr_param` → "change to" a `content` variant with the Loan Officer field in its `default` (re-populated) variant rather than `disabled`, after a short 200ms delay simulating the cascade resolve.

### Navigation Transitions

| From | To | Trigger | Animation |
|------|-----|---------|-----------|
| m01-dashboard (PAR tile) | report-runner | tap "Portfolio at Risk" tile | slide_right 300ms, pre-scoped to the PAR report |
| m14-reports-search-audit | report-runner | tap a report row | slide_right 300ms |
| report-runner | platform share sheet | tap `rr_export` | system share-sheet present (native transition) |
| report-runner | (back) | system back / app-bar back arrow | slide_left 300ms |

### Gesture Handling

- **Pull-to-refresh**: none — this screen has no top-level list to refresh; refreshing happens via the explicit Run action.
- **Horizontal scroll**: the result table scrolls horizontally when its column set overflows the 361dp content width (e.g. a wide report with 6+ columns); the parameter form and app-bar remain fixed.
- **Swipe-to-dismiss**: not applicable (no dismissible cards on this screen).
- **Long press**: not applicable.
- **Vertical scroll**: the whole screen body scrolls when the parameter form + result exceed viewport height; the app-bar is pinned.

### Animation Specifications

| Component | Type | Duration | Easing | Delay |
|-----------|------|----------|--------|-------|
| Shimmer skeleton | opacity pulse | 1200ms | standard | 0ms |
| `rr_param` dependent cascade | fade_in (loan-officer options refresh) | 200ms | standard_decelerate | 0ms |
| `rr_run` press | state-layer pressed overlay | 100ms (short2) | standard | 0ms |
| Result table populate | fade_in | 300ms (medium1) | emphasized_decelerate | 0ms |
| Sort re-order | crossfade rows | 250ms (medium1) | standard | 0ms |
| Loading → Error | fade_in | 200ms (short4) | standard | 0ms |
| Any → Empty | fade_in | 300ms (medium1) | standard_decelerate | 0ms |

### State Transitions

- `loading` → `content`: the report's parameter metadata + lookup options resolve.
- `loading` → `error`: the parameter metadata fails to resolve and no cache is available.
- `content` → `content`: a parameter changes, the report runs, a column is sorted, or export is triggered (all in-place, no navigation).
- `content` → `empty`: the run returned zero rows for the chosen parameters.
- `content` → `error`: the run fails hard with no cache.
- `empty` → `content`: parameters are adjusted and the re-run returns rows.
- `error` → `loading`: "Retry" tapped — re-resolves parameters or re-runs.

---

## Section 5: Content Data

> Zero placeholders. All data sourced from `screens/report-runner/demo-data.yaml`. Currency is always **KES** — never `$`/USD.

### Report catalog (`list_reports` picker source)

```yaml
reports:
  - { id: 1, reportName: "Active Loans by Loan Officer", reportType: "Table", reportCategory: "Loan" }
  - { id: 2, reportName: "Client Listing", reportType: "Table", reportCategory: "Client" }
  - { id: 5, reportName: "Portfolio at Risk", reportType: "Chart", reportCategory: "Loan" }
```

### Parameter options (`resolve_report_parameter` source, cascading)

```yaml
OfficeId:
  - { id: 1, name: "Head Office" }
  - { id: 3, name: "Nairobi CBD" }
  - { id: 5, name: "Kisumu Central" }
loanOfficerId (scoped to officeId=3):
  - { id: 41, name: "Peter Kariuki", parentId: 3 }
  - { id: 45, name: "Mercy Achieng", parentId: 3 }
```

### Selected demo run

```yaml
selected:
  reportName: "Active Loans by Loan Officer"
  officeId: 3        # Nairobi CBD
  loanOfficerId: 41   # Peter Kariuki
```

### Run result (`run_report` response, the `content` state's table)

```yaml
run_result:
  reportName: "Active Loans by Loan Officer"
  generatedAt: "2026-07-25T08:15:00Z"
  columnHeaders:
    - { columnName: "Client", columnType: "STRING" }
    - { columnName: "Account No", columnType: "STRING" }
    - { columnName: "Principal", columnType: "DECIMAL" }
    - { columnName: "Outstanding", columnType: "DECIMAL" }
  data:
    - ["Grace Wanjiru Mwangi", "000055231", "KES 60,000.00", "KES 42,500.00"]
    - ["Samuel Otieno Odhiambo", "000055240", "KES 45,000.00", "KES 31,000.00"]
    - ["Fatuma Njeri Kimani", "000055299", "KES 52,000.00", "KES 48,800.00"]
```

### Currency parameter default

The runner's Currency parameter (one of the report's declared `R_` parameters, alongside office/date/loan-officer) defaults to and is displayed as **KES** (Kenyan Shilling) throughout this deployment — the demo roster is Kenya-only, so every monetary cell in the result table (Principal, Outstanding) and every chart value callout renders with a `KES` prefix. Never render `$` or `USD` anywhere on this screen.

### Empty-state copy

```yaml
empty_state:
  message: "No rows returned for the selected parameters"
```

### Text Content (i18n keys, from `_strings/strings.yaml`)

| Component | Field | Value | i18n Key |
|-----------|-------|-------|----------|
| rr_param | label | "Report parameter (office · date · currency · officer)" | `reprun_param` |
| rr_run | label | "Run report" | `reprun_run` |
| rr_sort | label | "Sortable result column" | `reprun_sort` |
| rr_export | label | "Export" | `reprun_export` |
| rr_error_retry | label | "Retry" | `reprun_retry` |

### Image References

None — this screen uses no photographic imagery; the only non-text visual elements are the back-arrow icon, per-parameter chevron/calendar icons, the empty-state illustration placeholder, and the `[!]` error icon, all specified in Section 3 as vector icons resolved from the icon set (sizes per `design-tokens.yaml#icon`), not raster images.

---

## Section 6: Responsive Rules

### Canvas Specification

- Base canvas: 393×852dp (mobile portrait — Pixel 5 reference).
- Status bar: 24dp. Navigation bar: 48dp (gesture) or 56dp (3-button).
- Safe content area: 393×770dp.

### Touch Targets

- Minimum touch target: 48×48dp (WCAG 2.5.8) — applies to every `rr_param` field, `rr_run`, `rr_export`, `rr_error_retry`, and each `rr_sort` column header.
- Recommended: 56dp for the primary action (`rr_run`).
- No FAB on this screen.

### Font Scaling

- Supports system font scaling 85%–200%.
- Typography scale anchored to `body-medium` (14sp).
- Max line length: 60 characters for body/guidance text (empty/error copy wraps rather than truncates).
- Minimum text size after scaling: 12sp — Roboto Mono result numerics should not shrink below this or column alignment degrades.

### Theme Variants

- Light theme (default): use `colors.light.*` — the primary UX surface for this project.
- Dark theme: use `colors.dark.*` (see Section 1).
- System default: follow the device setting.
- High contrast: increase the table row divider from `outline-variant` to `outline`, and favor `primary-container`/`on-primary-container` pairings over raw `primary` fills for any text-bearing surface.

### Adaptive Layout

- Portrait (this spec's primary target): single column, full-width parameter form + result card.
- Landscape: two-column split — parameter form left rail (fixed 320dp), result table/chart fills the remaining width, letting wide result tables show more columns without horizontal scroll.
- Tablet (600dp+): parameter form renders as a persistent left rail (per the back-office `NavigationRail`/permanent-drawer adaptive scaffold); result occupies the remaining canvas.
- Foldable: dual-pane when unfolded — parameter form on one pane, result on the other, mirroring the tablet split.

### Keyboard & Switch-Access Navigation

- Tab order: back arrow → each `rr_param` field in visual (top-to-bottom) order → `rr_run` → each `rr_sort` header (left-to-right) → `rr_export`.
- Every focusable element shows the 2dp `primary` focus ring from Section 1's WCAG notes; no element relies on hover-only affordance.
- Enter/Space activates the focused button or opens the focused dropdown/date-picker; Escape closes an open dropdown without changing its value.
- On the `error` frame, focus moves to the error headline on state entry (screen-reader announcement), then to `rr_error_retry`.

---

## Handoff / QA Checklist

Before considering this hand-off complete, confirm in Figma:

1. **Variables created** — every color/spacing/radius/typography variable in Section 1 exists in the `mifos-x-backoffice-next-gen` collection with both `light` and `dark` mode values populated (no variable left at a single hard-coded hex).
2. **Four state frames present** — `loading`, `content` (both the Table-report and Chart-report sub-variants), `empty`, `error` (both `parameters_load_failed` and `report_run_failed` copy variants) — matching `ui.yaml#states` exactly, no extra or missing frames.
3. **Component variants complete** — every row of the Component summary table above exists as a Figma component with its declared variant count; no orphaned one-off instances that should have been variants of the same component.
4. **Prototype wired** — the full click-through in the Prototype interaction flow (Section 4) is connected and testable in Figma's Present mode, including the retry loop back to `loading`.
5. **Zero placeholder content** — every text layer shows real values from Section 5 (`Grace Wanjiru Mwangi`, `KES 60,000.00`, etc.), never "Lorem ipsum", "Text here", or a token literal like `{{primary}}`.
6. **Currency check** — every monetary value on every frame reads `KES`, never `$` or `USD`.
7. **Accessibility annotations** — contentDescription / accessible-name strings from Section 3 are present as Figma layer annotations (or the equivalent a11y plugin fields) for every interactive component.

