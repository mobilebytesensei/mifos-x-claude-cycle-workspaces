<!-- source: screens/m01-dashboard/ui.yaml + mockups/m01-dashboard/MOCKUP.md -->
<!-- source_hash: ui=ba1b489223c3 docs=de856d548ba7 -->
<!-- generated: 2026-07-31T03:22:52Z -->

# M01 · Role-adaptive Dashboard — Figma Design Handoff Prompts

> Generated from `screens/m01-dashboard/ui.yaml` + `mockups/m01-dashboard/MOCKUP.md` for Figma AI / manual design handoff.
> Design system: `idea-layer/design-system/design-tokens.yaml` (canonical, resolved) + `DESIGN.md`.
> Archetype: `dashboard` · 6 states · 10 interactive components · Material 3, light theme default.

---

## Section 1: Design System Context

Create a Figma variable collection named **`mifos-x-backoffice-next-gen`** with two modes, `Light` and `Dark`, and seed it from the resolved tokens below so every screen in this handoff draws from one closed palette — never introduce a color, radius, or type size that isn't listed here.

**Color variables — Light mode** (publish each under the group `color/`):

- `color/primary` = `#0091EA`
- `color/on-primary` = `#FFFFFF`
- `color/primary-container` = `#CBE6FF`
- `color/on-primary-container` = `#001E30`
- `color/secondary` = `#00796B`
- `color/on-secondary` = `#FFFFFF`
- `color/secondary-container` = `#B8F2E6`
- `color/on-secondary-container` = `#00201A`
- `color/tertiary` = `#5B5891`
- `color/on-tertiary` = `#FFFFFF`
- `color/error` = `#BA1A1A`
- `color/on-error` = `#FFFFFF`
- `color/error-container` = `#FFDAD6`
- `color/on-error-container` = `#410002`
- `color/success` = `#2E7D32`
- `color/warning` = `#F57C00`
- `color/warning-strong` = `#B45309` (the persistent offline-banner fill, always paired with white text)
- `color/background` = `#FCFCFF`
- `color/on-background` = `#1A1C1E`
- `color/surface` = `#FCFCFF`
- `color/on-surface` = `#1A1C1E`
- `color/surface-variant` = `#DEE3EB`
- `color/on-surface-variant` = `#42474E`
- `color/surface-container-low` = `#F3F4F9`
- `color/surface-container` = `#EDEFF4`
- `color/outline` = `#72777F`
- `color/outline-variant` = `#C2C7CF`

**Color variables — Dark mode** (same variable names, alternate values — wired into the collection for completeness; no dark frame is designed in this pass since light is the default UX surface):

- `color/primary` = `#6FD3FF`
- `color/on-primary` = `#00344F`
- `color/primary-container` = `#004B70`
- `color/on-primary-container` = `#CBE6FF`
- `color/secondary` = `#4FD8C4`
- `color/surface` = `#1A1C1E`
- `color/on-surface` = `#E2E2E6`
- `color/surface-variant` = `#42474E`
- `color/surface-container-low` = `#1A1C1E`
- `color/outline` = `#8C9198`

**Critical accessibility instruction for the design tool.** `color/primary` (`#0091EA`) rendered as a fill with white (`color/on-primary`) text on top measures roughly 2.6:1 contrast — well below the WCAG AA 4.5:1 threshold for body text. Configure every component in this file so that:

- Raw `primary` fills only ever carry large/bold labels or icon-only glyphs (18px+ bold, or icon-only).
- Any text-bearing surface that needs a primary-family fill — the selected bottom-navigation pill is the one example on this screen — uses `primary-container` / `on-primary-container` instead, which passes at 7:1+.
- Treat this as a persistent design constraint on the whole file, not a one-off note for a single component.

**Typography variables.** Create a type-style set named `Roboto`, with `Roboto Mono` reserved as a second family for tabular numerics (KPI values, counts, currency amounts). Publish these text styles:

- `headline-small` — 24px / 32px line-height / weight 600 — the page-level "Dashboard" title.
- `title-large` — 22px / 28px / weight 600 — card titles.
- `title-medium` — 16px / 24px / weight 500 — empty/error headline copy.
- `body-medium` — 14px / 20px / weight 400 — primary card and row copy.
- `body-small` — 12px / 16px / weight 400 — subtitles and timestamps.
- `label-large` — 14px / 20px / weight 500 — button and link labels.
- `label-medium` — 12px / 16px / weight 500 — chip and bottom-nav labels.

Every KPI numeral — "4.2%", "18,204", "KES 1,940,500", "37" — is set in the **Roboto Mono** family at `headline-small` size, so digits align in a column when multiple KPI cards sit side by side.

**Spacing variables** (number-variable group `spacing/`):

- `spacing/xs` = 4
- `spacing/sm` = 8
- `spacing/md` = 16 — default screen padding on phone; inter-card gap in the tile grid.
- `spacing/lg` = 24 — screen padding on tablet/desktop; gap between grid sections (KPI row → quick-actions row → activity list).
- `spacing/xl` = 32 — empty/error frame centered-column padding.
- `spacing/xxl` = 48

**Radius variables:**

- `radius/sm` = 8 — status chips.
- `radius/md` = 12 — shimmer skeleton blocks.
- `radius/lg` = 16 — KPI cards, the generic card component, empty-state illustration.
- `radius/xl` = 28 — buttons, quick-action pills (full pill shape).
- `radius/full` = 9999 — the bottom-navigation selected-item pill indicator.

**Elevation.** This system favors 1px borders over drop shadows, for offline-render performance and visual calm. Configure Figma effect styles as:

- `elevation/level0` — no shadow; a 1px `color/outline` stroke instead. Used on every card and list row.
- `elevation/level1` — a subtle `0px 1px 2px rgba(0,0,0,0.05)` drop shadow. Used on the top app bar only.
- Do not use `level2` or above anywhere on this screen — those are reserved for sheets/dialogs elsewhere in the system.

**Icon system.** Material Symbols, sized via icon variables `icon/sm` = 20, `icon/md` = 24, `icon/lg` = 32. The bottom-navigation icons (`dashboard`, `group`, `receipt_long`, `sync`) render at `icon/md`. The full-screen error icon renders at `icon/lg`.

**Grid / canvas.** Base the mobile frame at 393×852 (Pixel 5 reference), portrait, with a 24px status-bar inset and a 48px gesture-navigation inset at the bottom. Use an 8pt baseline grid throughout.

---

## Section 2: Screen Layouts

Design six frames for this screen, one per state, all sharing the same 393×852 canvas and the same persistent chrome (top app bar + bottom navigation), so a reviewer can flip between them and see only the content region change.

### Frame: Dashboard / Content

- Auto Layout, vertical, direction top-to-bottom, padding `spacing/md` on all sides, item spacing `spacing/lg` between the three content sections (KPI grid, quick-actions row, recent-activity list).
- The top app bar is pinned (not part of the scrolling Auto Layout frame): small M3 app bar, height 56, fill `color/surface`, title "Dashboard" in `headline-small` on `color/on-surface`, a leading hamburger/menu icon (`icon/md`, `color/on-surface`) at the left with 16px inset.
- Scrollable body, first section: a 2-column Auto Layout grid (fixed columns, `spacing/md` gutter) holding the four KPI cards in the fixed order Portfolio-at-Risk, Active Clients, Collections Due, Pending Approvals — each cell is a `kpi-card` component instance (defined in Section 3).
- Second section: a labelled "Quick actions" header (`label-large`, `color/on-surface-variant`, with a thin `color/outline-variant` divider rule above it) containing a horizontal Auto Layout row of up to two `tappable_card` pill instances.
- Third section: a labelled "Recent activity" header holding a vertical Auto Layout stack of `list-row` instances, each row 56px min-height with a leading status icon, a body-medium text line, and a trailing `body-small` relative timestamp right-aligned.
- The bottom navigation is pinned at the frame bottom, height 80 (including safe-area inset), fill `color/surface`, four equal-width items.

### Frame: Dashboard / Loading

- Identical Auto Layout skeleton to the Content frame — same app bar, same bottom-navigation, same grid geometry.
- Every KPI-card cell, quick-action pill, and activity row is replaced with a shimmer placeholder rectangle at the exact same width/height as its real counterpart (`radius/md`, fill `color/surface-variant`).
- Add a looping left-to-right gradient sweep animation, 1.5s duration, ease-linear, authored as a Smart Animate prototype loop.
- No text renders in this frame at all — the point is that a reviewer flipping Loading → Content sees zero layout shift.

### Frame: Dashboard / Empty

- App bar and bottom-navigation unchanged from Content.
- The body region becomes a single centered Auto Layout column (both-axis center alignment), `spacing/xl` padding.
- Contents, top to bottom: an empty-state illustration placeholder (200×200, `color/surface-variant` fill, `radius/lg`); a `title-medium` headline "No dashboard tiles available for your access"; a `body-medium` supporting line "Your current role doesn't grant access to any dashboard card yet."; a text-link styled "View my access" in `label-large` / `color/primary` beneath it.
- The primary-color text-link is acceptable here per the large-bold-label carve-out in Section 1's accessibility instruction.

### Frame: Dashboard / Partial-Tile-Error

- Same Auto Layout skeleton as Content.
- Three of the four KPI cards render normally with live values.
- The fourth (design it as the Portfolio-at-Risk card for this frame) is swapped for its `kpi-card--error` variant: fill remains `color/surface-container-low`, but the numeral region is replaced with a `status-chip-error` pill ("Couldn't load", fill `color/error-container`, text `color/on-error-container`) and a small `[ Retry ]` text-button (`label-large`, `color/error`) beneath it.
- No offline banner is shown in this frame — this is a single-tile failure, not a connectivity failure.

### Frame: Dashboard / No-Network

- Same Auto Layout skeleton as Content.
- Insert a full-width `offline-banner` component instance directly beneath the app bar and above the KPI grid: height 40, fill `color/warning-strong`, text "You're offline — figures may be stale" in `label-large` / white, centered.
- Every KPI card and activity row renders its last-cached value with the same visual treatment as Content — do not gray these out; cached-but-valid data is not an error state.

### Frame: Dashboard / Error

- App bar and bottom-navigation unchanged.
- The body becomes a single centered Auto Layout column: a large `icon/lg` warning-triangle icon in `color/error`, a `title-medium` headline "Couldn't load your dashboard", a `body-medium` supporting line "We couldn't resolve which tiles you can see. Your access is still saved.", and a filled `button-primary` labelled "Retry" beneath it.

### Prototype wiring across the six frames

- Loading auto-advances (Smart Animate, 400ms) to whichever of Content / Empty / Partial-Tile-Error / No-Network / Error is being demonstrated.
- Wire a manual "Simulate Retry" hotspot on the Partial-Tile-Error and Error frames that Smart-Animates back to Content.

---

## Section 3: Component Specifications

### Component: `kpi-card`

- Auto Layout, vertical, fixed width (grid-cell width, ~172px in the 2-column phone grid), padding `spacing/md`.
- Fill `color/surface-container-low`, corner radius `radius/lg`, no stroke — the tonal fill itself provides separation, per DESIGN.md's "borders over shadows" rule. This is the one card type on the screen that uses a tonal fill instead of an outline border.
- Content, top to bottom: a `body-small` / `color/on-surface-variant` title line ("Portfolio at Risk", "Active Clients", "Collections Due Today", "Approvals Waiting" — one instance per KPI); a `headline-small` numeral set in **Roboto Mono** / `color/on-surface` (the actual figure: "4.2%", "18,204", "KES 1,940,500", "37"); a `body-small` / `color/on-surface-variant` subtitle line ("PAR30 · all offices", "across 12 branches", "612 dues", "maker-checker queue").
- Variants: `default` (as above); `error` (numeral region replaced by the inline error treatment from the Partial-Tile-Error frame); `pressed` (8% `color/on-surface` overlay per the M3 state-layer spec); `focused` (2px `color/primary` focus ring, offset 2px).
- Minimum tap target 48×48 regardless of visual card height.
- Interaction: tapping any `kpi-card` fires a navigate action to its target module — see Section 4.

### Component: `tappable_card` (quick-action pill)

- Auto Layout, horizontal, height 48, padding `spacing/sm` horizontal / `spacing/xs` vertical.
- Fill `color/secondary-container`, text/icon color `color/on-secondary-container`, corner radius `radius/xl` (full pill).
- Content: a leading 20px icon (`person_add` for New Client, `payments` for Take Repayment) followed by a `label-large` text label ("New Client", "Take Repayment").
- Variants: `default`; `pressed` (12% `color/on-secondary-container` overlay); `disabled` (fill `color/surface-variant`, text `color/on-surface-variant`, opacity 38% — used when the app is offline and the action requires network, per DESIGN.md's button-primary-disabled convention applied here too).
- This component is entirely **absent** from the canvas — not merely disabled — for a persona lacking its gating permission. Do not design a "locked" visual state; the permission model is fail-closed at the data layer, not a greyed-out affordance.

### Component: `list-row` (recent-activity item)

- Auto Layout, horizontal, height 56 min, padding `spacing/md` horizontal.
- Fill `color/surface`, no corner radius — rows sit inside a plain vertical stack, not individually carded.
- Content: a leading 24px status icon (`check_circle` in `color/success` for approvals, `sync` in `color/on-surface-variant` for sync events, `payments` in `color/secondary` for transactions); a `body-medium` / `color/on-surface` primary text line (the activity description, e.g. "Loan #4471 approved by J. Otieno"); a trailing `body-small` / `color/on-surface-variant` relative-time label right-aligned ("12 min ago", "1 h ago").
- Rows are separated by a 1px `color/outline-variant` hairline.
- Tapping a row deep-links to the referenced entity — see Section 4.

### Component: `offline-banner`

- Auto Layout, horizontal, full-width, height 40, fill `color/warning-strong`.
- Centered content: a small `wifi_off` icon (`icon/sm`, white) and a `label-large` white text line.
- This is the one component permitted to break the "no flat-fill text" AA rule from Section 1, because `warning-strong` (`#B45309`) against white measures well above 4.5:1 — confirm this specific pairing before reusing the pattern elsewhere.

### Component: `status-chip-error`

- Auto Layout, horizontal, height 24, padding `spacing/xs` horizontal.
- Fill `color/error-container`, text `color/on-error-container`, `label-medium`, corner radius `radius/sm` — a small tag, not a pill.
- Used inline inside a failed `kpi-card`, paired with a `[ Retry ]` text button.

### Component: `shimmer-skeleton`

- A plain rectangle, fill `color/surface-variant`, corner radius `radius/md`.
- Add a Figma boolean/variant toggle for `pulsing` vs `static` so the loading-frame animation can be authored once and reused for every placeholder shape on the Loading frame.
- No text, no icon — purely geometric, sized to exactly match the real component it stands in for.

### Component: `empty-state`

- Auto Layout, vertical, center-aligned, padding `spacing/xl`, fill `color/surface`.
- Contents: illustration placeholder (200×200, `color/surface-variant`, `radius/lg`) + `title-medium` headline + `body-medium` supporting copy + a `label-large` text-link in `color/primary`.
- Only ever appears full-frame, centered — never inline.

### Component: `button-primary` / `button-primary-disabled`

- Auto Layout, horizontal, height 48, padding `spacing/md` horizontal, corner radius `radius/xl`.
- Default: fill `color/primary`, text `color/on-primary`, `label-large`, bold.
- Disabled: fill `color/surface-variant`, text `color/on-surface-variant`, opacity 38%.
- Used for "Retry" on the full-screen Error frame.

### Component: `header` (app bar)

- Auto Layout, horizontal, height 56, fill `color/surface`, padding `spacing/md` horizontal, vertically centered.
- Leading: 24px menu/back icon on `color/on-surface`.
- Title: `headline-small`, `color/on-surface`, left-aligned after the leading icon with `spacing/sm` gap.
- No trailing actions on this screen.

### Component: `bottom-navigation`

- Auto Layout, horizontal, height 80 (64 content + 16 safe-area), fill `color/surface`, four equal-width Auto Layout items.
- Each item: vertical Auto Layout, icon (`icon/md`) above a `label-medium` text label.
- Selected-item variant wraps the icon+label pair in a `radius/full` pill of `color/primary-container` with text/icon color `color/on-primary-container` (the AA-safe pairing called out in Section 1).
- Unselected items render icon+label directly in `color/on-surface-variant` with no pill background.

---

## Section 4: Interaction Patterns

Wire the following ten tap targets as Figma prototype hotspots with the specified transition. Every target listed here resolves to an existing screen elsewhere in this project — do not invent a destination frame; link to a placeholder frame named exactly after the target if the destination screen's own Figma file isn't available yet, so the link can be swapped later without renaming.

1. **`kpi_portfolio_at_risk_card`** — tap → Smart Animate, 300ms, `emphasized` easing → navigates to **`report-runner`** (M14 Reports & Audit), pre-scoped to the Portfolio-at-Risk report. Only wire this hotspot on frames where the PAR card is present (it is absent entirely for personas without report access — do not show a disabled state).
2. **`kpi_active_clients_card`** — tap → Smart Animate 300ms → navigates to **`client-list`** (M02 Clients), filtered to active clients.
3. **`kpi_collections_due_card`** — tap → Smart Animate 300ms → navigates to **`collection-sheet`** (M06 Collections), staffId-scoped to the signed-in field officer's route.
4. **`kpi_pending_approvals_card`** — tap → Smart Animate 300ms → navigates to **`checker-inbox`** (M15 Maker-Checker Approvals), scoped to entries this user can approve.
5. **`quick_action_new_client_tile`** — tap → Smart Animate 300ms → navigates to **`client-list`** (M02) and opens the new-client onboarding wizard.
6. **`quick_action_take_repayment_tile`** — tap → Smart Animate 300ms → navigates to loan repayment capture inside **`loan-detail`** (M04).
7. **A row inside `recent_activity_list`** — tap → Smart Animate 300ms → navigates to the entity the row references, or to **`needs-attention-inbox`** if the row is a failed-sync notification.
8. **`retry_tile_button`** (visible only on the Partial-Tile-Error frame) — tap → does **not** navigate; instead an in-place state change: the failing `kpi-card` swaps from its `error` variant back to `default` after a simulated 600ms load. Author this as a Smart Animate transition between two variants of the same card component, not a frame change — every other card on the frame is untouched by this interaction.
9. **`retry_dashboard_button`** (visible only on the Error frame) — tap → Smart Animate 400ms → transitions to the Loading frame, then (as a second linked transition) auto-advances to Content, representing the roster re-resolving from the retained permission set.
10. **`view_access_link`** (visible only on the Empty frame) — tap → Smart Animate 300ms → navigates to **`permission-capability-engine`** (Access & Permissions surface).

**Gesture / transient behavior:**

- The whole scrollable body supports pull-to-refresh — author as a top-of-frame drag interaction if the design tool supports it, otherwise note it as an annotation. A circular refresh indicator in `color/primary` appears at the top and Smart-Animates the frame back into its Loading → Content sequence.
- No swipe-to-dismiss or long-press interactions exist on this screen.

**State-transition summary** (for the prototype's overall flow diagram):

- Loading → Content — happy path, all tiles resolve.
- Loading → Empty — roster resolves to zero permitted tiles.
- Loading → Partial-Tile-Error — roster resolves but ≥1 tile fetch fails.
- Loading → No-Network — offline at load.
- Loading → Error — the roster itself fails to resolve.
- Partial-Tile-Error → Partial-Tile-Error (via `retry_tile_button`, still failing) or → Content (retry succeeded).
- Error → Loading → Content or Error (via `retry_dashboard_button`).
- No-Network → Content (connectivity restored, SWR revalidation).

---

## Section 5: Content Data

All content below is sourced from `demo-data.yaml` and is real, Fineract-shaped sandbox data — never substitute generic placeholder copy anywhere in the Figma file. Currency is always **KES** (Kenyan Shilling) — never a dollar sign.

### Persona: `dash_system_admin`

- Office: Head Office. Permission: `ALL_FUNCTIONS` umbrella — every tile visible, tile_count 6.
- KPI cards: Portfolio at Risk **4.2%** / "PAR30 · all offices"; Active Clients **18,204** / "across 12 branches"; Collections Due Today **KES 1,940,500** / "612 dues"; Approvals Waiting **37** / "maker-checker queue".
- Quick-actions: "New Client" and "Take Repayment" both present (`ALL_FUNCTIONS` grants `CREATE_CLIENT` and `REPAYMENT_LOAN`).
- Recent activity: "Loan #4471 approved by J. Otieno · 12 min ago" (icon: approval/check_circle); "Sync complete · 0 pending · 1 h ago" (icon: sync).

### Persona: `dash_branch_manager`

- Office: Nairobi Branch. Tile_count 3.
- KPI cards: Portfolio at Risk **5.1%** / "PAR30 · Nairobi branch"; Active Clients **2,317** / "Nairobi branch"; Approvals Waiting **8** / "loans awaiting your approval".
- Collections Due card is **absent** (no `READ_COLLECTIONSHEET`). Both quick-action tiles are **absent** (no `CREATE_CLIENT` / `REPAYMENT_LOAN`).
- Recent activity: "3 loans disbursed today · 2 h ago" (icon: approval).

### Persona: `dash_collections_officer`

- Office: Kibera Field Office, staff-scoped. Tile_count 2.
- KPI cards: only Collections Due Today **KES 84,200** / "3 centers · 42 dues · Kibera cluster".
- Quick-action: "Take Repayment" present (no "New Client" — no `CREATE_CLIENT`).
- Recent activity: "Repayment KES 3,000 queued (offline) · just now" (icon: transaction/payments); "Attendance saved · Kibera Center A · 20 min ago" (icon: attendance).

### Persona: `dash_accountant`

- Office: Head Office. Tile_count 1.
- KPI cards: only Active Clients **18,204** / "org-wide (read)".
- No quick-actions present.
- Recent activity: "GL closure Nov-2026 pending review · 3 h ago" (icon: accounting).

### Persona: `dash_auditor`

- Office: Head Office. `ALL_FUNCTIONS_READ`. Tile_count 3.
- KPI cards: Portfolio at Risk **4.2%** / "PAR30 · all offices (read)"; Active Clients **18,204** / "org-wide (read)"; Collections Due Today **KES 1,940,500** / "612 dues (read)".
- Zero quick-action tiles — `ALL_FUNCTIONS_READ` never grants a mutating action.
- Recent activity: "142 audit entries today · 1 h ago" (icon: audit).

### Persona: `dash_no_access`

- Office: Nairobi Branch, freshly-provisioned. Tile_count 0.
- No tiles, no recent-activity rows — renders the Empty frame's copy exactly: "No dashboard tiles available for your access."

### Screen chrome text

- App-bar title = "Dashboard" (`{strings.m01_title}`).
- Bottom-navigation labels = "Home", "Clients", "Collections", "Sync".
- Offline-banner text = "You're offline — figures may be stale".
- Empty-state headline = "No dashboard tiles available for your access", link label = "View my access".
- Error-frame headline = "Couldn't load your dashboard", button label = "Retry".
- Partial-tile-error inline chip = "Couldn't load", inline button = "Retry".

### Icon references (Material Symbols — no invented glyphs)

- `dashboard` — bottom-nav Home.
- `group` — bottom-nav Clients.
- `receipt_long` — bottom-nav Collections.
- `sync` — bottom-nav Sync + recent-activity sync events.
- `person_add` — New Client quick-action.
- `payments` — Take Repayment quick-action + transaction activity rows.
- `check_circle` — approval activity rows.
- `wifi_off` — offline banner.
- `warning` — full-screen error icon.
- `menu` — app-bar leading icon.

---

## Section 6: Responsive Rules

### Canvas specification

- Primary frame: 393×852dp (mobile portrait, Pixel 5 reference).
- Status bar: 24dp.
- Gesture navigation bar: 48dp (or 56dp if the target device profile uses 3-button navigation — annotate both as component-swap variants of the bottom safe-area inset).
- Safe content area beneath the app bar and above the navigation inset: 393×770dp.

### Touch targets

- Every tappable component (KPI card, quick-action pill, activity row, retry buttons, view-access link) must resolve to a minimum 48×48dp hit area even where its visual bounds are smaller (WCAG 2.5.8) — use Figma's tap-area padding on the component's interactive layer rather than inflating the visible card.
- FAB-class controls (not used on this screen, but reserved in the shared library) reserve 56dp diameter with 16dp margin from frame edges.

### Font scaling

- Every text style in Section 1 must remain legible up to 200% system font scale without truncation — verify by duplicating the Content frame with each text style bumped 2× and confirming the Auto Layout containers grow rather than clip.
- Typography is anchored to `body-medium` (14px) as the scaling baseline; minimum rendered size after scaling is 12sp.

### Theme variants

- Light theme is the default and only theme designed in this pass (per `design-tokens.yaml#metadata.theme_default: light`); the Dark-mode variable values from Section 1 exist in the variable collection for future parity but no Dark frame is required here.
- High-contrast mode (if the design system later adds one) should increase card elevation-as-outline (2px `color/outline` instead of 1px) rather than introduce new colors.

### Adaptive layout — tablet (600dp+) and desktop (840dp+)

- Promote the KPI grid from 2 columns to 3–4 columns as width allows (Auto Layout wrap, same `spacing/md` gutter).
- Promote the bottom-navigation to a permanent left-side `NavigationRail` (fixed 80dp width) populated from the full permission-gated module set rather than the illustrative four-item phone set, per `app-shell.yaml#drawer`.
- Screen padding increases from `spacing/md` (16) to `spacing/lg` (24).
- The quick-actions row and recent-activity list remain single-column, right-aligned within the expanded content area rather than stretching full-width, to avoid excessively long line-lengths in the activity feed.

### Foldable / dual-pane

- Not a primary target for this screen.
- If a dual-pane frame is requested later, the KPI grid occupies the left pane and the recent-activity list occupies the right pane as a master-detail split, sharing the same component instances defined in Section 3.

---

## Post-generation checklist

- [ ] All 6 state frames created (Content, Loading, Empty, Partial-Tile-Error, No-Network, Error) sharing one component set.
- [ ] All 10 interaction hotspots wired per Section 4, each resolving to a named target frame (or placeholder-named stand-in).
- [ ] Zero raw hex values typed directly onto a layer — every fill/text color references a published Figma variable from Section 1.
- [ ] Zero placeholder content — every KPI value, persona name, and activity row uses the exact strings from Section 5.
- [ ] Accessibility check re-run on the selected bottom-nav pill and any other primary-family surface to confirm the `primary_container`/`on_primary_container` substitution was actually applied, not `primary`/`on_primary`.
