<!-- source: screens/loan-detail/ (ui, docs, flow, demo-data) + design-system/design-tokens.yaml -->
<!-- source_hash: ui=9887f116c27f docs=1b4eee2370d8 flow=c2bc47cfbf61 -->
<!-- generated: 2026-07-31T03:22:43Z -->

# Loan Account Detail — Figma Design Handoff Prompts

> Generated from `screens/loan-detail/ui.yaml` (+ `docs.yaml`, `flow.yaml`, `demo-data.yaml`, `design-tokens.yaml`) by `/idea export --mockup`.
> Distinct from `mockups/loan-detail/FIGMA_LINKS.md` (Stitch project links) and `screens/loan-detail/prompts/*.md` (per-state Stitch prompts). This file is prose design-instruction handoff for Figma / Figma AI, structured as six sections.
> Screen: **Loan Account Detail** · Archetype: `detail_screen` · Module: `m04-loan-portfolio` · Initial state: `loading` · Product: MifosX BackOffice — a KMP, offline-first, permission-driven Fineract back-office console.

---

## Section 1: Design System Context

Design this screen inside a calm, dense, clinical Material 3 financial-admin console. The brand identity color is Light Blue `#0091EA` (Figma variable `Color/Primary/Default`), paired with `#FFFFFF` (`Color/OnPrimary/Default`) for large or bold text/icon labels only — at ~2.6:1 contrast, `#0091EA` fill with white text fails WCAG-AA for regular body text, so any text-on-primary surface that isn't a large/bold label should instead use the primary-container pairing: fill `#CBE6FF` (`Color/PrimaryContainer/Default`) with text `#001E30` (`Color/OnPrimaryContainer/Default`), which clears 7:1+. Secondary/accent teal `#00796B` (`Color/Secondary/Default`) and the brighter accent `#00BFA5` (`Color/Accent/Default`) are reserved for positive or primary-action emphasis and should appear no more than twice on this screen — the Active status chip and, if shown, an accent underline on the selected tab.

Set up Figma color variables for every role this screen touches: `Color/Surface/Default` `#FCFCFF`, `Color/OnSurface/Default` `#1A1C1E`, `Color/OnSurfaceVariant/Default` `#42474E`, `Color/SurfaceVariant/Default` `#DEE3EB` (this is also the shimmer-skeleton fill), `Color/Outline/Default` `#72777F`, `Color/OutlineVariant/Default` `#C2C7CF`, `Color/SecondaryContainer/Default` `#B8F2E6` with `Color/OnSecondaryContainer/Default` `#00201A` (Active status chip), `Color/Error/Default` `#BA1A1A` with `Color/OnError/Default` `#FFFFFF`, `Color/ErrorContainer/Default` `#FFDAD6`, `Color/Warning/Default` `#F57C00` with `Color/OnWarning/Default` `#FFFFFF` (the overdue-period indicator and the offline banner's strong variant `#B45309`), and `Color/Success/Default` `#2E7D32` (reserved for a "synced" confirmation state elsewhere, not used on this screen). Wire a dark-theme variable mode too — the tonal flips live in `design-tokens.yaml#colors.dark` (e.g. primary flips to `#6FD3FF`, surface flips to `#1A1C1E`) — but light is this project's default UX surface and should be the frame you design first.

Typography is Roboto for UI text and Roboto Mono for every numeric figure (principal, outstanding, schedule amounts, transaction amounts, dates, ids) so digits align in fixed-width columns. Set up text styles: `Type/TitleLarge` 22px/28px weight 600 for the app-bar title, `Type/BodyLarge` 16px/24px weight 400 for the client name and product name, `Type/BodyMedium` 14px/20px weight 400 for tab labels and secondary copy, `Type/BodySmall` 12px/16px weight 400 for due-dates and transaction ids, `Type/LabelLarge` 14px/20px weight 500 for button labels and the tab row, and a monospace variant of BodyLarge/BodyMedium (Roboto Mono, same sizes) bound wherever a KSh amount, account number, or loan id appears.

Spacing follows an 8pt grid with a 4dp base unit: `Space/XS` 4px, `Space/SM` 8px, `Space/MD` 16px (default content padding), `Space/LG` 24px (section gaps), `Space/XL` 32px. Corner radius is soft: `Radius/SM` 8px for chips, `Radius/MD` 12px for inputs, `Radius/LG` 16px for cards and the content area, `Radius/XL` 28px for buttons. Elevation is intentionally subtle — prefer a 1px `Color/OutlineVariant` border over a drop shadow; where elevation is unavoidable (the bottom-sheet-style action confirmation, if used), use `Elevation/Level1` (`0 1px 2px rgba(0,0,0,0.05)`) on-surface and reserve `Elevation/Level3` (`0 8px 24px rgba(0,0,0,0.12)`) for true overlays only. Minimum touch target is 48×48dp (`touch_targets.comfortable`) for every tappable row and button on this screen; 44dp is the absolute floor and should not be used for primary actions.

Motion on this screen should stay restrained — this project's `design_read` quiet-constraints clamp motion to a low dial, so avoid bouncy or springy curves. Bind Figma smart-animate durations to the token scale: `Motion/Short4` 200ms for tab cross-fades, `Motion/Medium2` 300ms for full state transitions (loading→content, loading→error), and `Motion/Medium3` 350ms for the shimmer pulse loop. Use the `standard` easing curve (`cubic-bezier(0.2, 0, 0, 1)`) as the default for everything on this screen; reserve `emphasized_decelerate` for the one moment something enters attention suddenly (a fresh overdue-period warning appearing after a background refresh).

Icons on this screen are all Material Symbols, sized per the `icon` scale: the app-bar back chevron and overflow are `icon.md` (24px), the client-link trailing chevron is `icon.sm` (20px), the overdue-warning glyph and the schedule-row completion glyphs are `icon.sm` (20px), and the empty-state / error-state centerpiece glyphs are `icon.xl` (48px). Elevation levels map to Figma effect styles `Elevation/Level0` through `Elevation/Level5`; this screen only ever needs `Elevation/Level0` (flat, bordered cards — the default for the summary header and schedule/ledger rows) and, if a confirm-sheet overlay is added, `Elevation/Level3` for that sheet.

A brief accessibility contrast checklist for this screen, since it is a regulated-industry, accessibility-first surface: client name and product name (`Color/OnSurface/Default` on `Color/Surface/Default`) must clear 4.5:1 — it does, at roughly 13.6:1. The Active status chip (`Color/OnSecondaryContainer/Default` on `Color/SecondaryContainer/Default`) must clear 4.5:1 for its label text — verify in Figma's contrast plugin before shipping the chip variant. The overdue-period warning text (`Color/Warning/Default` on `Color/Surface/Default`) is decorative-plus-text — the word "Overdue" itself must be legible independent of the tint, never color-only. Every focus ring uses a 2px `Color/Primary/Default` outline (`border.focus` token) offset 2dp from the focused element's bounds.

## Section 2: Screen Layouts

### Node dimensions (Content state, 393dp-wide frame)

| Node | Width | Height | Notes |
|---|---|---|---|
| App bar | 393dp (fill) | 56dp | fixed, pinned top |
| Summary header (`ld_header`) | 361dp (fill − 2×16dp margin) | hug (~92dp with 3 rows) | Auto Layout vertical, gap 8dp |
| Tab row (`ld_tabs`) | 361dp (fill) | 40dp | 3 equal 120.3dp segments |
| Schedule row | 361dp (fill) | 44dp | ×3 rows = 132dp total, plus 2×1px dividers |
| Transaction row | 361dp (fill) | 44dp minimum | ×3 rows = 132dp+ total |
| Action bar button | 361dp (fill) or equal-split | 48dp (56dp if sole action) | full-width when a single action shows |
| Bottom navigation | 393dp (fill) | 56dp | fixed, pinned bottom |

### Layout — Content state

Structure the frame as a single vertical Auto Layout column, direction Vertical, padding `Space/MD` (16px) on all sides, item spacing `Space/LG` (24px) between the major sections (header, tabs, body, action bar), fill `Color/Surface/Default`. The frame sits below a fixed `app-bar-detail` region (not part of the scrolling Auto Layout — pin it) and above a fixed `bottom-navigation` region (also pinned). Render order top to bottom:

1. **App bar** (`app-bar-detail`, fixed height 56px) — leading back chevron (24dp, `Color/OnSurfaceVariant/Default`), title "Loan 000055231 · Group Business Loan" (`Type/TitleLarge`, `Color/OnSurface/Default`), trailing overflow icon (24dp). Fill `Color/Surface/Default`, bottom border 1px `Color/OutlineVariant/Default`.
2. **Summary header** (`ld_header`, width fill, height hug) — Auto Layout vertical, gap `Space/SM` (8px): row 1 is client name "Grace Wanjiru Mwangi" (`Type/BodyLarge` bold, `Color/OnSurface/Default`) with the Active status-chip pinned to the trailing edge; row 2 is "Principal KSh 60,000.00 · Outstanding KSh 42,500.00" in the monospace BodyMedium style; row 3 is the next-due indicator "Next due: Period 3 · KSh 6,000.00 · 2024-06-06" tinted `Color/Warning/Default` with a small overdue icon, only rendered when a period is overdue.
3. **Tab row** (`ld_tabs`, width fill, height 40px) — a three-segment `segmented_control` (Schedule / Transactions / Details), Auto Layout horizontal, equal-width segments, selected segment fill `Color/SecondaryContainer/Default` with text `Color/OnSecondaryContainer/Default`, unselected segments transparent with text `Color/OnSurfaceVariant/Default`.
4. **Content area** (`content_area`, width fill, height fill, scrollable) — the state-aware tab body. For Schedule: a `data-table`-style stack of three period rows, each row Auto Layout horizontal with period number, due date, principalDue, interestDue, totalDue, and a completion glyph (✓ for `complete: true`, a warning glyph for the overdue incomplete row). For Transactions: a `list-row` stack of three transaction rows (type, date, amount). For Details: a two-column key/value list of loan metadata.
5. **Action bar** (width fill, height hug, gap `Space/SM`) — one or more `button-primary` instances, status+permission filtered, right-aligned or full-width depending on count (single button = full-width; two or more = horizontal row, equal width).

### Layout — Content state, Details tab

When `ld_tabs` has "Details" selected, the content area swaps to a two-column key/value list (Auto Layout vertical, each row Auto Layout horizontal with the key at `Type/BodyMedium`/`Color/OnSurfaceVariant/Default` on the leading 40% and the value at `Type/BodyLarge` (Roboto Mono for numeric/date values) on the trailing 60%). Rows, top to bottom: "Number of repayments" → 12, "Interest rate (p.a.)" → 24.0%, "Submitted" → 2024-03-01, "Approved" → 2024-03-04, "Disbursed" → 2024-03-06, "Expected maturity" → 2025-03-06, "Total repayment to date" → KSh 17,500.00. Each row is 44dp minimum height with a 1px `Color/OutlineVariant/Default` bottom divider, matching the Schedule/Transactions row rhythm so switching tabs doesn't jar the reading rhythm.

### Layout — Loading state

Same Auto Layout skeleton as Content, but every data-bearing node is replaced 1:1 with a `shimmer-skeleton` rectangle of matching dimensions: a rounded rectangle (`Radius/MD`) fill `Color/SurfaceVariant/Default` with a looping left-to-right shimmer gradient (pulse motion, `motion.durations.medium3` 350ms, `easings.standard`). The app bar shows a generic "Loan detail" title (pre-resolve) rather than the real account number, since that data hasn't loaded yet. No tab row content renders — replace it with three equal-width shimmer pills.

### Layout — Empty state

Auto Layout vertical, centered both axes, fill `Color/Surface/Default`, padding `Space/XL` (32px). Contents, in order: a 200×200dp illustration placeholder frame (a simple "document not found" glyph on `Color/SurfaceVariant/Default`), a `Type/TitleLarge` headline "Loan account not found", a `Type/BodyMedium` body line "This loan may have been deleted, or the link you followed is out of date." in `Color/OnSurfaceVariant/Default`, and a `button-secondary` "← Go back" 48dp tall. The app bar retains only the back chevron (no title data, no overflow icon since there's no loan to act on).

### Layout — Error state

Same centered Auto Layout as Empty, but the illustration is replaced with a 64dp error glyph (`Color/Error/Default`), headline "The loan failed to load" (`Type/TitleLarge`), body copy "Check your connection and try again." (`Color/OnSurfaceVariant/Default`), and a full-width `button-primary` "Retry" (`Color/Primary/Default` fill, `Color/OnPrimary/Default` label) at 48dp height.

## Section 3: Component Specifications

**`ld_header` (Summary header)** — Auto Layout vertical container, width fill, padding `Space/MD`, gap `Space/SM`, background `Color/Surface/Default`. Contains a nested horizontal row for client name + status chip, a monospace row for principal/outstanding, and a conditional warning row for the next-due indicator. The status chip is a `status-chip` component variant: fill `Color/SecondaryContainer/Default`, text `Color/OnSecondaryContainer/Default`, `Radius/SM`, label "Active" — build chip variants for every loan status this screen can show (Active, Pending Approval, Approved, Closed, Overdue) as separate Figma component variants so the design system stays honest about the full state space even though only "Active" appears in this demo capture.

**`ld_client_link` (Client link row)** — a `list_item` styled as a tappable row, height 48dp minimum, Auto Layout horizontal, padding `Space/SM` horizontal, containing the client name text (`Type/BodyLarge`, `Color/Primary/Default` to signal tappability) and a trailing chevron-right icon (16dp, `Color/OnSurfaceVariant/Default`). Accessibility label: "Open the borrower's client 360 profile". On tap, navigates to `client-detail-360` for `clientId` 10241.

**`ld_tabs` (Segmented tab row)** — `segmented_control` component, width fill, height 40px, corner radius `Radius/Full` (pill), 1px border `Color/OutlineVariant/Default`, internal 2dp padding. Three equal segments: "Schedule", "Transactions", "Details". Selected segment gets an inner pill fill `Color/SecondaryContainer/Default` inset by 2dp; label color flips to `Color/OnSecondaryContainer/Default` when selected, `Color/OnSurfaceVariant/Default` otherwise. This is a pure state toggle — no loading spinner variant needed since switching tabs never re-fetches.

**`ld_repayment` / `ld_approve` / `ld_disburse` (Action buttons)** — `button-primary` component, 48dp height minimum (56dp for the sole action when it's the only one shown), full corner radius `Radius/XL` (28px), fill `Color/Primary/Default`, label `Color/OnPrimary/Default` in `Type/LabelLarge`. Build a `disabled` variant too (tonal `Color/SurfaceVariant/Default` fill, `Color/OnSurfaceVariant/Default` text) for the case where an action is network-required and the device is offline — the button stays visible but disabled rather than disappearing, per the button-primary-disabled pattern in `COMPONENTS.md`. Labels: "Make Repayment", "Approve", "Disburse".

**`ld_error_retry` (Retry button)** — same `button-primary` component as above, label "Retry", full width, 48dp height, centered under the error illustration.

**Schedule row (data-table row)** — Auto Layout horizontal, height 44dp, padding `Space/SM` vertical / `Space/MD` horizontal, five columns (period, due date, principalDue, interestDue, totalDue) right-aligned numeric columns in Roboto Mono, a trailing completion glyph (a filled check circle `Color/Success/Default` for complete periods, a filled warning triangle `Color/Warning/Default` for the incomplete overdue period). Bottom border 1px `Color/OutlineVariant/Default` between rows.

**Transaction row (list-row)** — Auto Layout horizontal, height 44dp minimum, leading transaction-type label ("Disbursement" / "Repayment", `Type/BodyLarge`), trailing date (`Type/BodySmall`, `Color/OnSurfaceVariant/Default`) stacked over the amount (`Type/BodyLarge` Roboto Mono, `Color/OnSurface/Default`).

**`shimmer-skeleton`** — rounded rectangle, `Radius/MD`, fill `Color/SurfaceVariant/Default`, with a diagonal gradient sweep animated left-to-right over 1.5s, looping, easing `standard`. Build one variant per shape it needs to mimic on this screen: a header-row shimmer (full width, 20dp tall), a two-line shimmer (client + amounts), a tab-row shimmer (three equal pills, 32dp tall), and three schedule-row shimmers (44dp tall each).

**`empty-state`** — Auto Layout vertical, centered, gap `Space/MD`, padding `Space/XL`, containing an illustration frame, headline text style, body text style, and an optional `button-secondary` CTA slot.

### Component states matrix

| Component | idle | active/selected | disabled | error |
|---|---|---|---|---|
| `ld_client_link` | `Color/Primary/Default` text, chevron visible | n/a (navigates, no persistent selected state) | not applicable — always tappable when the loan resolves | not shown in error/loading/empty states |
| `ld_tabs` (per segment) | `Color/OnSurfaceVariant/Default` text, transparent fill | `Color/SecondaryContainer/Default` fill, `Color/OnSecondaryContainer/Default` text | n/a — always interactive once content loads | n/a |
| `ld_repayment` / `ld_approve` / `ld_disburse` | `Color/Primary/Default` fill, `Color/OnPrimary/Default` text | pressed: `Color/PrimaryPressed/Default` `#0072B8` fill | tonal `Color/SurfaceVariant/Default` fill, `Color/OnSurfaceVariant/Default` text (offline / network-required) | not applicable — a failed post surfaces via `repayment_post_failed` inline copy, button stays in idle state, queued for retry |
| `ld_error_retry` | `Color/Primary/Default` fill | pressed: darker shade per state-layer pressed opacity 0.12 | n/a | n/a (this button only exists inside the error state itself) |

## Section 4: Interaction Patterns

### Navigation transitions

| From | To | Trigger | Motion |
|------|-----|---------|--------|
| m04-loan-portfolio (list row) | loan-detail | tap a loan row (`open_loan_detail`) | slide_right, `motion.durations.medium2` 300ms, `easings.standard` |
| m01-dashboard (repayment tile) | loan-detail (Schedule tab pre-selected) | tap the "quick take repayment" tile | slide_right, 300ms, deep-linked directly to the Schedule tab |
| needs-attention-inbox | loan-detail | tap a loan-approved / repayment-due alert row | slide_right, 300ms |
| loan-detail | client-detail-360 | tap `ld_client_link` (`open_client`) | slide_right, 300ms; loan-detail is retained on the back-stack |
| loan-detail (error) | loan-detail (loading) | tap `ld_error_retry` (`retry`) | cross-fade, `motion.durations.short4` 200ms |

### Gesture handling

- **Pull-to-refresh**: not modeled for this screen — the loan aggregate already revalidates automatically in the background under CACHE_FIRST_SWR; a manual pull-to-refresh is out of scope for this iteration.
- **Tab swipe**: the segmented tab row responds to horizontal swipe on the content area as an alternate to tapping a segment, same 200ms cross-fade transition between tab bodies.
- **Long press**: not used on this screen.
- **Scroll**: the content area (schedule / transactions / details body) is independently vertically scrollable; the summary header, tab row, and action bar stay pinned above the fold.

### Animation specifications

| Component | Type | Duration | Easing | Delay |
|-----------|------|----------|--------|-------|
| Tab body swap (`select_tab`) | cross-fade | 200ms | standard | 0ms |
| Shimmer pulse | gradient sweep | 1500ms (loop) | standard | 0ms |
| Loading → Content | fade-in | 300ms | standard_decelerate | 0ms |
| Loading → Error | fade-in | 200ms | standard_decelerate | 0ms |
| Content → Content (background refresh badge) | alpha fade | 250ms | standard | 0ms |
| Any → Empty | fade-in | 300ms | standard_decelerate | 0ms |
| Error → Loading (retry tapped) | cross-fade | 200ms | standard_accelerate | 0ms |

### State transitions (screen-level)

`loading → content` when the loan aggregate resolves (cache-first) with associations. `loading → empty` when the loanId resolves to no account. `loading → error` when the load fails with no cache available. `content → content` when a tab is selected or a lifecycle action is enqueued (summary/schedule update in place, no navigation). `content → client-detail-360` when the client link is tapped. `error → loading` when Retry is tapped.

### Confirmation / outbox feedback

Tapping `ld_repayment`, `ld_approve`, or `ld_disburse` should show a lightweight confirm step (a bottom-sheet or inline dialog — not specified further here, treat as a follow-up design task) before the command is written to `draft_outbox`; on confirm, surface a snackbar "Repayment queued for sync" (or the equivalent per-action copy) using the `snackbar` component (`Color/InverseSurface/Default` fill, `Color/InverseOnSurface/Default` text), auto-dismissing after ~4s.

### Prototype interaction flow (Figma prototype connections)

Wire the following click-through path across your Figma frames so a reviewer can walk the whole loan lifecycle without leaving prototype mode: **Loading frame** → (auto-advance / "on load" trigger, 300ms delay) → **Content frame, Schedule tab selected** (this is the default `selectedTab` on first load). From Content/Schedule: tapping the "Transactions" segment of `ld_tabs` navigates (smart animate, 200ms) to **Content frame, Transactions tab selected**; tapping "Details" navigates to **Content frame, Details tab selected**; all three Content variants share the same pinned app-bar, summary header, and action bar layers so Figma's smart-animate interpolates only the content-area contents. Tapping `ld_client_link` from any Content variant navigates (slide-left, 300ms) to a stand-in **client-detail-360** frame (out of scope for this file — link to that screen's own Figma page if it exists). Tapping the sole visible action-bar button from Content opens a stand-in **confirm sheet** overlay (slide-up, 250ms) with a "Confirm" / "Cancel" pair; "Confirm" returns to the Content frame with a snackbar overlay auto-triggered and auto-dismissed after 4s; "Cancel" simply closes the overlay. Separately, wire **Error frame** → (tap `ld_error_retry`) → **Loading frame** (cross-fade, 200ms) to close the retry loop, and wire **Empty frame** → (tap "Go back") → back to whichever frame represents the calling list (m04-loan-portfolio or m01-dashboard), using Figma's "Back" navigation trigger rather than a hardcoded target so the prototype respects real back-stack behavior.

## Section 5: Content Data

> Zero placeholders. All figures below are sourced verbatim from `demo-data.yaml` — real Fineract shapes for a Group Business Loan.

### Loan summary

```yaml
loan:
  accountNo: "000055231"
  clientId: 10241
  clientName: "Grace Wanjiru Mwangi"
  loanProductName: "Group Business Loan"
  currency: "KES"
  displaySymbol: "KSh"
  principal: "KSh 60,000.00"
  approvedPrincipal: "KSh 60,000.00"
  status: "Active"
  loanBalanceOutstanding: "KSh 42,500.00"
  totalRepayment: "KSh 17,500.00"
  numberOfRepayments: 12
  annualInterestRate: "24.0%"
  submittedOnDate: "2024-03-01"
  approvedOnDate: "2024-03-04"
  actualDisbursementDate: "2024-03-06"
  expectedMaturityDate: "2025-03-06"
```

### Repayment schedule (Schedule tab)

```yaml
periods:
  - period: 1
    dueDate: "2024-04-06"
    principalDue: "KSh 5,000.00"
    interestDue: "KSh 1,200.00"
    totalDue: "KSh 6,200.00"
    complete: true
  - period: 2
    dueDate: "2024-05-06"
    principalDue: "KSh 5,000.00"
    interestDue: "KSh 1,100.00"
    totalDue: "KSh 6,100.00"
    complete: true
  - period: 3
    dueDate: "2024-06-06"
    principalDue: "KSh 5,000.00"
    interestDue: "KSh 1,000.00"
    totalDue: "KSh 6,000.00"
    complete: false
    overdue: true
```

### Transactions ledger (Transactions tab)

```yaml
transactions:
  - id: 990112
    type: "Disbursement"
    date: "2024-03-06"
    amount: "KSh 60,000.00"
  - id: 990455
    type: "Repayment"
    date: "2024-04-05"
    amount: "KSh 6,200.00"
  - id: 990781
    type: "Repayment"
    date: "2024-05-06"
    amount: "KSh 6,100.00"
```

### Action availability by status

```yaml
available_actions:
  active: ["Make repayment"]
  pending_approval: ["Approve"]
  approved: ["Disburse"]
```

### Empty ledger copy

| Component | Field | Value |
|-----------|-------|-------|
| Transactions tab (empty row-list) | message | "No transactions recorded on this loan yet" |
| Empty screen state | headline | "Loan account not found" |
| Empty screen state | body | "This loan may have been deleted, or the link you followed is out of date." |
| Error screen state | headline | "The loan failed to load" |
| Error screen state | body | "Check your connection and try again." |

All currency is Kenyan Shilling (KES, displayed as "KSh") — never render a `$` symbol anywhere on this screen.

### Text content & i18n keys

| Component | Field | Value | i18n key |
|-----------|-------|-------|----------|
| `ld_header` | label | "Loan summary" (header semantic label) | `strings.loandet_header` |
| `ld_client_link` | label | "Grace Wanjiru Mwangi" (bound, not literal) | `strings.loandet_client_link` |
| `ld_tabs` | label | "Schedule / Transactions / Details" | `strings.loandet_tabs` |
| `ld_repayment` | label | "Make Repayment" | `strings.loandet_repayment` |
| `ld_approve` | label | "Approve" | `strings.loandet_approve` |
| `ld_disburse` | label | "Disburse" | `strings.loandet_disburse` |
| `ld_error_retry` | label | "Retry" | `strings.loandet_retry` |

All copy is sourced from the project's i18n string table (`strings.*` keys above, defined per `RULE-IMPL-NO-HARDCODED-STRING-001`) — no literal English string is hardcoded in the implemented Compose layer; the values shown throughout this document are the resolved English default locale, for design-review readability only.

## Section 6: Responsive Rules

### Canvas specification

- Base canvas: 393×852dp (mobile portrait, Pixel 5 reference).
- Status bar: 24dp. Gesture navigation bar: 48dp (or 56dp for 3-button nav).
- Safe content area: 393×770dp after status bar + bottom navigation.

### Touch targets

- Minimum touch target 48×48dp (WCAG 2.5.8) on `ld_client_link`, every action-bar button, `ld_error_retry`, the "Go back" CTA, and each segment of `ld_tabs`.
- Recommended 56dp height for the sole action-bar button when only one lifecycle action is visible.

### Font scaling

- Support system font scaling 85%–200%; do not clip or truncate the summary header, schedule rows, or ledger rows at larger scales — allow the Auto Layout column to grow height rather than clip text.
- Typography scale anchors to `Type/BodyMedium` (14sp); minimum text size after scale-down is 12sp.
- Maximum line length for body copy (empty/error headlines and messages): 60 characters.

### Theme variants

- Light theme (default): use `colors.light.*` tokens as specified throughout this document.
- Dark theme: swap to `colors.dark.*` — primary flips to `#6FD3FF` on `#00344F`, surface flips to `#1A1C1E`, on-surface flips to `#E2E2E6`; the overdue-warning and error roles keep the same semantic mapping with their dark-theme hex values.
- System default: follow the device theme setting; do not hardcode light-only assumptions into the component set.
- High-contrast: increase the schedule/ledger row divider from `Color/OutlineVariant/Default` to `Color/Outline/Default` and prefer the `Color/OutlineVariant/Default`-bordered card treatment over relying on elevation alone.

### Adaptive layout

- Portrait (this spec's primary target): single column, full-width summary/tabs/content-area/action-bar as laid out in Section 2.
- Landscape: two-column split is acceptable — summary header + action bar in a left rail, tab content in the right pane — but is not required for v1.
- Tablet (600dp+): the `navigation-rail` replaces the bottom navigation per `app-shell.yaml`; the loan-detail content area gets a max content width of ~600dp centered, with margin rather than stretching full width.
- Foldable: dual-pane is out of scope for this screen in v1; single-pane behavior is acceptable when unfolded.

### Breakpoints (from `design-tokens.yaml#breakpoints`)

| Breakpoint | Value | Loan-detail layout behavior |
|---|---|---|
| `mobile` | 0dp | Single-column Auto Layout as specified in Section 2 (this document's primary design target) |
| `tablet` | 600dp | Content area caps at ~600dp centered; `navigation-rail` replaces bottom navigation |
| `desktop` | 840dp | Same as tablet, plus a permanent drawer for the 17 permission-filtered module roots alongside the rail |
| `large` | 1240dp | Content area may adopt the optional landscape two-column split described above |

Build the Figma frame set as: one 393dp mobile frame per state (four total: loading, content, empty, error — content additionally needs Schedule/Transactions/Details tab variants, so seven frames in total for full state+tab coverage), plus one 768dp tablet reference frame for the Content/Schedule variant to validate the navigation-rail swap and the capped content width. Desktop/large frames are optional for this iteration since the permission-filtered drawer is out of scope for a single-feature handoff.

## Figma File Organization

Create a single Figma page named "loan-detail" nested under this project's shared design-system file (the one that already holds the `Color/*`, `Type/*`, `Space/*`, `Radius/*` variable collections defined in Section 1 — do not redefine them locally). Within that page, lay out frames left-to-right in this order: Loading, Content/Schedule (the default landing composition), Content/Transactions, Content/Details, Empty, Error, then the 768dp Tablet reference frame. Name each frame exactly `loan-detail / {state}` (e.g. `loan-detail / content-schedule`) so the frame name doubles as a breadcrumb back to `ui.yaml#states`.

Component naming convention: every reusable node built for this screen should be published as a Figma component with the path `LoanDetail/{ComponentId}` mirroring the `ui.yaml#components[].id` values verbatim — `LoanDetail/ld_header`, `LoanDetail/ld_client_link`, `LoanDetail/ld_tabs`, `LoanDetail/ld_repayment`, `LoanDetail/ld_approve`, `LoanDetail/ld_disburse`, `LoanDetail/ld_error_retry` — so a reviewer or an implementer can trace every Figma layer back to the exact `ui.yaml` component id it implements, and so `/idea verify --rule RULE-MOCKUP-AUTO-001` cross-references cleanly. Shared chrome (`app-bar-detail`, `bottom-navigation`, `shimmer-skeleton`, `empty-state`) should instead reference the existing shared-chrome components from `preview/_shared/*` if a matching Figma component already exists in the design-system file, rather than being rebuilt locally — check the design-system file's chrome section first.

Variant properties: build `ld_repayment` / `ld_approve` / `ld_disburse` as three separate component instances (not variants of one generic "action button" component) since each carries a distinct permission gate and label, but give each one a boolean `disabled` variant property so the offline/network-required tonal state can be toggled without duplicating the component. Build `ld_tabs` as a single component with a `selected` variant property (enum: Schedule / Transactions / Details) so the three tab states stay in sync as one source component. Build the schedule-row and transaction-row list items as components with a `complete` (boolean, schedule only) or none (transactions are never "incomplete") variant property, and an `overdue` boolean overlay property for the schedule row.

## Handoff QA Checklist

Before marking this Figma file ready for implementation review, confirm: (1) every color fill and text color in every frame is bound to a `Color/*` variable, zero raw hex swatches remain on any layer; (2) every text layer uses one of the `Type/*` text styles defined in Section 1, zero ad-hoc font-size overrides; (3) every spacing value (padding, gap) in every Auto Layout frame is a multiple of the 4dp base unit and matches a named `Space/*` token where one exists; (4) all seven state/tab frames plus the tablet reference frame exist and are named per the convention above; (5) the prototype click-through wired in Section 4 connects every frame with no dead-end hotspot; (6) every KSh amount matches `demo-data.yaml` verbatim (60,000.00 / 42,500.00 / 17,500.00 principal/outstanding/total-repayment, and the three schedule periods' 5,000/1,200-1,100-1,000/6,200-6,100-6,000 figures) — no rounded or invented figures; (7) the Active status chip, the overdue-period row, and the disabled action-button variant have each been run through Figma's contrast-checker plugin and pass 4.5:1 for their text.

---

## Design Rationale — Why This Screen Looks The Way It Does

This is a **permission-gated, offline-first** detail surface inside a regulated back-office app, and both of those constraints should visibly shape the design rather than being invisible engineering concerns. First, permission-gating: the action bar is never a static row of "Approve / Disburse / Make Repayment" buttons that get disabled when unavailable — a hidden action is *removed entirely*, because the underlying `PermissionEvaluator` re-derives the exact permitted set from the server-issued `PermissionSet` and the loan's current status on every load, and a visually-present-but-disabled button would misrepresent what the signed-in operator is actually authorized to do (a teller who lacks `APPROVE_LOAN` should never see an "Approve" button at all, not a grayed-out one). The one exception is the **disabled variant** used specifically for *network-required-but-currently-offline* — there the operator does hold the permission, but the action genuinely cannot proceed until connectivity returns, which is a meaningfully different signal from "you're not allowed" and is why Section 3's component-states matrix keeps that as its own variant.

Second, offline-first: every read on this screen is designed to render *before* the network responds, from the `loan_cache` Room mirror, and every mutation is designed to *never block on the network* at all — tapping "Make Repayment" enqueues to `draft_outbox` and returns control to the operator immediately with a snackbar confirmation, rather than showing a spinner while a POST round-trips. This is why the loading shimmer only ever appears on the very first open of a loan that has no prior cache entry (the `get_loan_cache_first_opens_offline` scenario in `tests.yaml`) — a returning visit to an already-cached loan should feel instantaneous, with the background-refresh badge doing the "there might be newer data" signaling instead of a blocking spinner. Reviewers evaluating this Figma file against a competing back-office UI should specifically check that neither of these two properties has been "designed away" for visual simplicity — a cleaner-looking screen that shows disabled-not-hidden actions, or that blocks on a spinner during a repayment post, would be a regression against this feature's actual behavioral contract in `ui.yaml` and `data-flow.yaml`.

Third, the currency and locale: every monetary figure on this screen is Kenyan Shilling, rendered with the `KSh` display symbol and always to two decimal places (matching Fineract's `currency.decimalPlaces: 2`), never a bare number and never a `$` sign — this is a Kenya-market back office, and a reviewer should treat a stray `$` anywhere in an implementation as a defect, not a stylistic choice.

## Related

- `idea-layer/mockups/loan-detail/MOCKUP.md` — ASCII wireframes + component inventory for the same four states.
- `idea-layer/exports/loan-detail/SPEC.md` — implementation spec (state model, API endpoints, flow logic).
- `idea-layer/design-system/DESIGN.md` + `design-tokens.yaml` — full token system this document resolves against.
- `idea-layer/mockups/loan-detail/FIGMA_LINKS.md` — Stitch project screen links (separate artifact; not overwritten by this generation).
