# COMPONENTS.md — Mifos-X Back Office NextGen

> Component catalog for the design system. Companion to `DESIGN.md` (spec + token
> bindings) and `design-tokens.yaml` (token SoT). Chrome + pattern components are
> defined in `DESIGN.md#components` front-matter; project composites are defined in
> `idea-layer/components.yaml` (merged over the framework primitive/pattern registries).
> Consumed by `/idea-feature-render` (LLM HD render path), `/idea-feature-stitch`, and
> `/implement` Compose codegen. All styling is token-native — every value below resolves
> to a `design-tokens.yaml` token (never a raw hex/px).

Design language: calm, dense, clinical Material-3 financial-admin console. Light-mode
default. Primary Light-Blue `--primary #0091EA`; Teal `--secondary #00796B` / accent
`--accent #00BFA5` reserved for positive/primary-action emphasis (≤2 accent uses per
screen). Borders (`--outline` / `--outline-variant`) favored over shadows for fast
offline render; elevation kept to `--el-0..2` on-surface, `--el-3` for overlays.

---

## App chrome (shared partials — `preview/_shared/*.html`)

| Component | Role | Token bindings |
|---|---|---|
| **app-bar** / **app-bar-default** / **app-bar-detail** | M3 small top app bar. `default` = menu + title + search + filter (lists/login); `detail` = back + title + overflow (records); base = menu + title + search + notifications. Title is screen-sourced. | fill `--surface`, title `--on-surface` `--fs-title-large`, icons `--on-surface-variant`, border-bottom `--outline-variant` |
| **bottom-navigation** | Phone nav bar. Items Home / Clients / Collections / Sync in the same order on every screen; active item uses the `--primary-container` pill indicator, rest `--on-surface-variant`. | fill `--surface`, indicator `--primary-container`, selected label `--primary`, unselected `--on-surface-variant` |
| **navigation-rail** | Tablet/desktop equivalent of the bottom nav; permission-filtered module roots. | fill `--surface`, selected `--primary`, unselected `--on-surface-variant` |
| **fab** | Teal create action, bottom-end, above the bottom-nav. | fill `--secondary`, label/icon `--on-secondary`, radius `--r-lg`, elevation `--el-2` |
| **offline-banner** | Persistent warning-fill banner shown while offline; figures below may be stale and refresh on next sync. | fill `--warning-strong`, text `--on-primary` |
| **snackbar** | Transient bottom confirmation host. | fill `--inverse-surface`, text `--inverse-on-surface` |

---

## Pattern components (DESIGN.md#components)

| Component | Purpose | Token bindings |
|---|---|---|
| **card** | Dashboard/detail building block. | `--surface` on `--outline` border, radius `--r-lg`, padding `--sp-md`, `--el-1` |
| **kpi-card** | Metric tile on the tonal `--surface-container-low`; value in `--font-mono`. | `--surface-container-low`, value `--fs-headline-large` mono, radius `--r-lg`, `--el-1` |
| **list-row** | Dense single/two-line list item, 44dp min touch target. | `--surface`, primary `--fs-body-large`, meta `--fs-body-small`, divider `--outline-variant` |
| **data-table** | Tabular records; header on `--surface-variant`; numerics in `--font-mono`. | header `--surface-variant`, cell `--on-surface`, mono numerics |
| **status-chip** / **status-chip-error** | Semantic state pills (approved/pending/overdue/failed). | `--secondary-container`/`--error-container`, radius `--r-sm` |
| **button-primary** / **button-primary-disabled** | Primary CTA; disabled = tonal `--surface-variant` fill (network-required action while offline). | `--primary`/`--surface-variant`, text `--on-primary`, radius `--r-xl`, padding `--sp-md` |
| **button-secondary** | Outlined/tonal secondary action. | `--surface` fill, `--primary` text, radius `--r-xl` |
| **text-field** / **text-field-error** | Filled inputs on `--surface-variant`; error variant tints text/helper with error role. | `--surface-variant`, radius `--r-sm`, error `--on-error-container` |
| **banner** | Informational inline banner (e.g. maker-checker pending). | `--secondary-container`, text `--on-secondary-container` |
| **bottom-sheet** | Action/detail sheet with drag handle. | `--surface`, radius `--r-lg` top, `--el-3` |
| **shimmer-skeleton** | Loading placeholder; layout matches content composition block-for-block. | `--surface-variant`, radius `--r-md`, pulse motion |
| **empty-state** | Centered friendly empty message + optional CTA. | `--surface`, text `--on-surface-variant`, padding `--sp-xl` |

---

## Project composite components (`components.yaml`)

| Component | Category | Purpose |
|---|---|---|
| **content_area** | containers | Primary scrollable content slot every screen body hangs its permission-filtered components inside; owns screen-level scroll + safe-area padding; renders the state-aware payload (content/loading/empty/error/no-network). |
| **tappable_card** | surfaces | Card surface with tap/navigation semantics (drives detail navigation). |
| **segmented_control** | navigation | In-screen tab/segment switcher (tab selection = state change, not navigation). |
| **filter_chip_row** | inputs | Horizontally scrollable filter-chip row for list/roster filtering. |
| **group_header** | containers | Section/group header row within grouped lists and settings. |
| **status_banner** | feedback | Connectivity/sync state banner (offline · syncing · synced · queued · error). |
| **currency_field** | inputs | Money input rendering amounts in `--font-mono` with locale currency formatting. |
| **dynamic_form_field** | inputs | Fineract entity-template / datatable-driven dynamic field renderer. |
| **expandable_section** | containers | Collapsible section (loan schedule, ledger, sub-resource lists). |
| **table_header** | containers | Sortable column header row for data tables (numerics right-aligned mono). |

---

## Do's and Don'ts (render + implement)

- Use `--font-mono` for all amounts, balances, account/loan IDs, dates, and timestamps so digits align (CRAFT §7c).
- Keep accent (`--primary`/`--secondary`/`--accent`) to ≤2 visible uses per screen; neutrals carry 70-90% of pixels.
- Match the loading-state `shimmer-skeleton` layout to the content-state composition block-for-block.
- Render a persistent `offline-banner` while offline; tint network-required actions as `button-primary-disabled`.
- Never invent color/spacing/radii — resolve every value to a `design-tokens.yaml` token.
- Never blank a whole dashboard when one tile fails — isolate to that card's inline error with a per-tile retry.
