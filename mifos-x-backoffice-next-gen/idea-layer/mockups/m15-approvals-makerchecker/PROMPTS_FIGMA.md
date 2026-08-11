<!-- source: screens/m15-approvals-makerchecker/ (ui, docs, flow, demo-data) + design-system/{DESIGN.md, design-tokens.yaml} -->
<!-- source_hash: ui=32b8c4847ba0 docs=59f5e2c8d232 flow=0f139c16974c -->
<!-- generated: 2026-07-31T03:23:09Z -->

# M15 · Approvals (Maker-Checker) — Figma Design-Handoff Prompts

> Generated from `screens/m15-approvals-makerchecker/ui.yaml` for design handoff / Figma AI. Natural-language design instructions — read top to bottom as a designer brief, not a spec. Same source data as `PROMPTS_STITCH.md`, formatted as prose paragraphs and bulleted variant lists rather than YAML spec blocks. Target platform: Material 3, mobile-first (393×852dp Pixel 5 reference), light theme default with a dark-theme flip available.

---

## Section 1: Design System Context

Design **M15 · Approvals (Maker-Checker)** as part of *Mifos-X Back Office NextGen*, a permission-gated, offline-first administrative console for the Mifos/Fineract core-banking platform. The product mood is calm, clinical, and dense — this is a tool operated all day by accountants, tellers, branch managers, and auditors, so legibility and information density beat decoration. Favor 1px borders and tonal fills over heavy shadows so lists render instantly even when served from an offline cache.

### Color variables (map 1:1 to Figma color styles)

- `color/primary` = `#0091EA` — Approve button fill, bulk-approve button fill, selected segmented-control indicator, active nav-drawer entry. Always paired with `color/on-primary` for large/bold labels and icons only.
- `color/on-primary` = `#FFFFFF` — text/icon on `color/primary` fills.
- `color/primary-container` = `#CBE6FF` — selected filter chip fill, selected segmented-button fill. Pair with `color/on-primary-container`, never with `color/on-primary` (AA-critical text belongs on the container pairing, not the raw primary — the raw primary/white pairing is ~2.6:1, below the 4.5:1 body-text floor).
- `color/on-primary-container` = `#001E30` — text on `color/primary-container`; the AA-safe (7:1+) pairing for any text sitting on a primary-tinted surface.
- `color/secondary` = `#00796B` — reserved accent; not used as a fill on this screen, used sparingly elsewhere (max twice per screen).
- `color/secondary-container` = `#B8F2E6` — group-count badge fill.
- `color/on-secondary-container` = `#00201A` — group-count badge text.
- `color/tertiary` = `#5B5891` — muted indigo, informational-chip role; unused on this screen, kept for palette completeness.
- `color/success` = `#2E7D32` — approved/posted semantic role; not directly painted on M15 (an approved entry simply leaves the queue) but referenced by adjacent screens (needs-attention-inbox) for consistency.
- `color/warning` = `#F57C00` — the "Awaiting approval" pending-badge text.
- `color/warning-container` — tonal fill paired with `color/warning` for the same badge.
- `color/warning-strong` = `#B45309` — persistent offline-banner fill; not used on this screen.
- `color/error` = `#BA1A1A` — Reject label, Delete label, error-state glyph.
- `color/error-container` = `#FFDAD6` / `color/on-error-container` = `#410002` — reserved for an error-state chip variant if one is introduced later.
- `color/surface` = `#FCFCFF` — screen background, app-bar fill, row fill.
- `color/on-surface` = `#1A1C1E` — primary text color.
- `color/surface-variant` = `#DEE3EB` — group-header band fill, shimmer-skeleton fill, locked-row tint base.
- `color/on-surface-variant` = `#42474E` — maker/made-on metadata, group-header label text.
- `color/outline-variant` = `#C2C7CF` — 1px hairline row dividers, chip/segmented-control borders.
- `color/outline` = `#72777F` — stronger border role, used for the payload-panel confirm-dialog border.

Do not introduce any hue outside this closed palette — there are no decoration colors in this system, and never draw a gradient. Every fill/text pairing listed above already passes WCAG AA (≥4.5:1); do not invent a new pairing without checking contrast first.

### Typography variables

- `type/title-medium` (16px / 24px line-height, weight 500) — top app bar screen title "Approvals".
- `type/label-large` (14px / 20px, weight 500) — group-by segmented-control labels, group-header bucket names, all button labels.
- `type/body-medium` (14px / 20px, weight 400) — command-row primary line (action · entity, maker, made-on).
- `type/body-small` (12px / 16px, weight 400) — command-row secondary line (resource reference), empty/error body copy.
- `type/label-medium` (12px / 16px, weight 500) — pending badge, group-count numeral.
- `type/mono-body` (Roboto Mono, 14px / 20px, weight 400) — audit ids, KES amounts, made-on timestamps; the one place digits must align down a column.

Support system font scaling to 200% without breaking the row layout — the two-line command row must be allowed to grow to three lines rather than truncate the maker name or the resource reference.

### Shape, elevation, spacing variables

- `radius/xl` = 28px — buttons, filter chips, segmented-control pill.
- `radius/lg` = 16px — payload inspect panel leading corners, empty-state illustration frame.
- `radius/md` = 12px — reserved, unused directly on this screen.
- `radius/sm` = 8px — pending badge.
- `radius/xs` = 4px — checkbox corner.
- `elevation/level-0` — flat, `outline-variant` 1px border: list rows, group bands.
- `elevation/level-1` — subtle 2dp tonal tint, no visible shadow: the top app bar.
- `elevation/level-2` — 4–8dp lift + scrim: the payload inspect panel only.
- `spacing/md` = 16px — screen padding on phone.
- `spacing/lg` = 24px — screen padding on tablet/desktop.
- `spacing/row-padding` = 12px — dense-console row internal padding (used instead of the general `spacing/md` inside command rows).
- `spacing/section-gap` = 24px — vertical gap between stacked group sections.
- `spacing/sm` = 8px — gap between filter chips.

---

## Section 2: Screen Layouts

Lay out **M15** as a single vertically-scrolling column, no bottom navigation and no floating action button — this screen is reached as a permission-gated destination in the navigation drawer/rail, not as a bottom-tab, and the checker never authors new queued commands here, only acts on ones a maker already submitted.

### Top region (pinned, does not scroll)

- Auto Layout: vertical stack, 0px gap between its two rows, full width, no external padding (each child manages its own).
- Row 1 — top app bar: small Material 3 app bar, `color/surface` fill, `color/on-surface` title text "Approvals", auto leading icon (back on phone push-navigation, hamburger/menu when this is a drawer root), height 56dp, bottom 1px `outline-variant` hairline.
- Row 2 — `group_by_selector`: three-segment Material 3 segmented button reading "Entity · Action · Maker", right-aligned or full-width depending on available space, "Entity" selected by default. Present only in `content` and `submitting` states.
- Row 3 — `filter_bar`: horizontally-scrollable auto-layout row, gap `spacing/sm` (8px), horizontal padding `spacing/sm spacing/md`. Row one of chips is the actionName facet (`All`, `CREATE`, `APPROVE`, `DISBURSE` — populated live from `GET /v1/makercheckers/searchtemplate`, never hardcoded); row two (or an inline continuation) is the entityName facet (`CLIENT`, `LOAN`). Present only in `content` and `submitting` states.

### Content region (scrolls)

- Auto Layout: vertical stack, gap `spacing/sm` (8px) between rows within a group, gap `spacing/section-gap` (24px) between groups, screen-level padding only (`spacing/md` phone / `spacing/lg` tablet+), no additional padding on the list container itself.
- Each group renders as one `group_header` band (full width, `surface-variant` fill, `spacing/xs spacing/md` padding, label-large text reading the bucket name plus a trailing count pill in a `secondary-container` chip) immediately followed by its member `command_row` items, with zero gap between the header and its first row.
- Default `content` state with the default entity grouping renders exactly two group bands in this order: "Clients (1)" containing the CREATE·CLIENT row for audit id 88201, then "Loans (2)" containing the APPROVE·LOAN row for audit id 88202 and the DISBURSE·LOAN row for audit id 88203.
- Each `command_row` Auto Layout: horizontal stack — leading 24dp checkbox slot (`select_toggle`, present only when this checker canCheck the row's action+entity) → a vertical two-line text stack (fills remaining width) → a trailing button row or status chip. Row min-height 64dp, internal padding `spacing/row-padding` (12px).
  - Text-stack line 1 (body-medium, `on-surface`): "{ACTION} · {ENTITY}" left-aligned, maker username and made-on timestamp right-aligned in `on-surface-variant` body-small.
  - Text-stack line 2 (body-small, `on-surface-variant`): the resource reference (e.g. "Amara Wanjiru — KE-CLT-2024-10243" or "loan/482915 (Amara Wanjiru) — KES 75,000") plus a trailing `priority_badge` pill reading "Awaiting approval".
  - Trailing button row (present only when canCheck passes): `Approve` (filled, `primary` fill, `on-primary` label) and `Reject` (outlined, `primary`-colored label on `surface`) — both entirely absent, not disabled, on a row this checker cannot act on.
- Multi-select bar: pinned to the bottom of the content region once ≥1 row is checked (scrolls with content until the last row, then sticks), `surface-container-high` fill, top 1px `outline-variant` divider, "{N} selected" body-medium text plus a filled `Bulk approve` button.
- Final scroll element: `open_needs_attention_link` — plain text-link row, `primary`-colored label-large text "Open Needs Attention →", visible in `content`, `empty`, and `submitting` states.

### Loading layout

- Same pinned app bar; `group_by_selector` and `filter_bar` are absent (not present in their `visible_states`).
- Content region: three `shimmer-skeleton` blocks, each matching a `command_row`'s exact two-line height (64dp) and internal padding, so the transition into real content never causes a layout jump.

### Empty layout

- App bar only, then a centered vertical Auto Layout stack starting roughly a third down the available height, gap `spacing/md`.
- A 200dp illustration frame (`surface-variant` fill, a friendly checkmark/tray glyph), an "All caught up" title (title-medium), a one-line body-small subtitle "No pending approvals in your scope.", a "Last synced: {timestamp}" caption, and `open_needs_attention_link` retained at the very bottom.

### Submitting layout

- Identical structure to `content`, with the acted-upon row's leading checkbox replaced by a small circular progress indicator and its trailing button row replaced by a single disabled "Queued…" chip.
- The acted-upon row alone renders at `opacity/loading` (0.60); every other row keeps full opacity and full interactivity.

### Error layout

- App bar only, then a centered vertical Auto Layout stack: an error glyph in `color/error`, a title-medium headline "Couldn't load your approvals queue", a body-medium explanation, and a filled `Retry` button.
- No list content, no filter row, no segmented control render in this state.

---

## Section 3: Component Specifications

### header

- Role: full-width top app bar container.
- Auto Layout: horizontal, height 56dp, `color/surface` fill, bottom 1px `color/outline-variant` hairline.
- Content: title "Approvals", `type/title-medium`, `color/on-surface`, left-aligned after a 4dp-inset leading icon.
- Variants: default only — present across all five states, never changes.

### group_by_selector

- Role: Material 3 segmented button, three segments "Entity", "Action", "Maker".
- Auto Layout: horizontal, height 40dp, full pill shape (`radius/full`), 1px `outline-variant` border, 2dp internal padding between a segment and the outer edge.
- Variant — default (unselected segment): transparent fill, `on-surface-variant` label-large text.
- Variant — selected: `primary-container` fill, `on-primary-container` label-large text.
- Variant — pressed: 12% `primary` state-layer overlay over the segment being pressed.
- Variant — focused (keyboard/switch access): 2px `primary` focus ring outset 2dp from the segment bounds.
- Visibility: `content` and `submitting` only.

### filter_bar

- Role: horizontally-scrollable row of filter chips.
- Auto Layout: horizontal, scrolling, gap `spacing/sm` (8px), padding `spacing/sm spacing/md`.
- Each chip: 32dp tall, full pill (`radius/full`), label-large text.
- Variant — default (unselected): `surface` fill, 1px `outline-variant` border, `on-surface-variant` text.
- Variant — selected: `primary-container` fill, no border, `on-primary-container` text.
- Variant — hovered (desktop pointer): 8% `on-surface` overlay on an unselected chip.
- Variant — pressed: 12% overlay of the chip's current fill role.
- Chips populate live: actionName ∈ {All, CREATE, APPROVE, DISBURSE}; entityName ∈ {All, CLIENT, LOAN} — from `GET /v1/makercheckers/searchtemplate`, never hardcoded.
- Visibility: `content` and `submitting` only.

### content_area

- Role: the scrollable body container; semantic role `main`.
- Auto Layout: vertical, gap `spacing/section-gap` (24px) between group sections, screen-padding only (no double padding against list items).
- Sub-states (content / loading / empty / error) documented above under Section 2 — the container itself never changes background, only its children.

### group_header

- Role: full-width section band labeling a bucket in the grouped list.
- Auto Layout: horizontal, height 32dp, `surface-variant` fill, `on-surface-variant` text, horizontal padding `spacing/md`, vertical padding `spacing/xs`.
- Content: bucket label (entity name, action name, or maker username depending on active `groupBy`) plus a trailing count pill (`secondary-container` fill, `on-secondary-container` text, label-medium).
- Variant: default only, no interactive states (not tappable in this feature).
- Visibility: `content` and `submitting` only.

### command_row

- Role: list item representing one queued command.
- Auto Layout: horizontal, min-height 64dp, internal padding `spacing/row-padding` (12px).
- Variant — default: `surface` fill, `on-surface` / `on-surface-variant` text, 1px `outline-variant` bottom divider.
- Variant — hovered (desktop pointer): 8% `on-surface` state-layer overlay.
- Variant — pressed: 12% `on-surface` state-layer overlay, brief scale-down 0.98 for ~50ms.
- Variant — focused (keyboard nav): 2px `primary` focus ring around the row bounds.
- Variant — locked/submitting: row content at `opacity/loading` (0.60); leading checkbox replaced by a small spinner; trailing buttons replaced by the disabled "Queued…" chip.
- Variant — disabled (checker cannot canCheck this row at all): no checkbox, no trailing buttons rendered — this is a structural absence, not a grayed-out disabled state.

### select_toggle

- Role: 24dp checkbox controlling bulk-selection membership.
- Variant — unchecked (default): `outline` 1px border, transparent fill, `radius/xs` (4px) corner.
- Variant — checked: `primary` fill, white check glyph.
- Variant — hovered: 8% `primary` overlay ring around the box.
- Variant — pressed: 12% `primary` overlay, check glyph scale-and-fade-in over ~100ms.
- Variant — disabled/locked (row is submitting): reduced-opacity `outline-variant` border, no interaction.
- Absence rule: entirely absent (not disabled) on any row the checker cannot canCheck.

### priority_badge

- Role: small status pill.
- Auto Layout: horizontal, `radius/sm` (8px), horizontal padding 8px, vertical padding 2px, label-medium text.
- Variant — content (the only variant this feature uses): "Awaiting approval" in `warning` text on a `warning-container`-tinted background. This screen does not expose a graded priority scale, only the single queued-and-awaiting status.

### approve_button

- Role: primary commit action for a queued command.
- Variant — default: filled M3 button, `primary` fill, `on-primary` label-large text "Approve", `radius/xl` (28px) pill.
- Sizing: 32dp height when inline in a `command_row`; 40dp height when standalone in the payload panel; horizontal padding `spacing/md`.
- Variant — hovered: 8% `on-primary` overlay.
- Variant — pressed: 12% `on-primary` overlay.
- Variant — focused: 2px `on-primary-container`-colored ring outset 2dp.
- Variant — disabled/locked: `surface-variant` fill, `on-surface-variant` text — reserved for the exact moment this row is submitting; never appears alongside an active checkbox on the same row.
- Absence rule: rendered only on canCheck-gated rows.

### reject_button

- Role: secondary decline action for a queued command.
- Variant — default: outlined M3 button, transparent fill, `primary` 1px border and label-large text "Reject", `radius/xl` pill, same sizing as `approve_button`.
- Variant — hovered: 8% `primary` overlay inside the outline.
- Variant — pressed: 12% `primary` overlay.
- Variant — focused: 2px `primary` ring outset 2dp.
- Semantics: canCheck-gated identically to `approve_button`; the underlying command is always discarded (never executed) once enqueued.

### delete_button

- Role: destructive purge action for a stale/obsolete pending command.
- Variant — default: text/destructive button, `error` label-large text "Delete", no fill.
- Location: inside the payload inspect panel only, not inline in the row.
- Confirm gate: always opens a modal confirm dialog first — title "Delete this pending command?", body explaining it will be purged and never executed, `Cancel` / `Delete` actions, the dialog's `Delete` action in `error` fill with `on-error` text. Only an explicit confirm enqueues the DELETE.

### bulk_approve_button

- Role: commit action across the current multi-selection.
- Variant — default: filled M3 button, `primary` fill, `on-primary` label-large text "Bulk approve", `radius/xl` pill, height 40dp.
- Container: lives inside the multi-select bar — a `surface-container-high`-tinted band with a top `outline-variant` divider, pinned to the bottom of the scroll content.
- Visibility: shown only once `selectedIds` is non-empty.

### open_needs_attention_link

- Role: read-only cross-link into the fan-in needs-attention-inbox.
- Variant — default: plain text button, no fill, `primary` label-large text "Open Needs Attention →", left-aligned, 44dp min touch height.
- Variant — pressed: 8% `primary` overlay behind the text.
- Semantics: a pure read-only jump; never mutates the target inbox on tap.

### retry_button

- Role: the sole interactive recovery action in the error state.
- Variant — default: filled M3 button, `primary` fill, `on-primary` label-large text "Retry", `radius/xl` pill, height 40dp, centered beneath the error headline/body.
- Variant — pressed: 12% `on-primary` overlay.
- Visibility: `error` state only.

---

## Section 4: Interaction Patterns

### Navigation entry

M15 is entered from three places: the permission-gated navigation drawer/rail root (visible only when the signed-in user holds at least one `*_CHECKER` permission or `CHECKER_SUPER_USER`), the M01 dashboard's "Approvals Waiting" tile, and a drill-in tap from an approval row inside needs-attention-inbox. All three land on the same screen at its default `loading` → `content` / `empty` / `error` resolution.

### Group-by switch

Tapping a different segment in `group_by_selector` (Entity → Action, Action → Maker, etc.) re-buckets the already-loaded entries in place — a fade-cross-dissolve of the group headers and rows, roughly 250ms `standard` easing, with **no network request** and no loading state shown. The entries themselves never move visually if their relative order within a bucket is unchanged; only the group boundaries redraw.

### Filter apply

Selecting an actionName or entityName chip in `filter_bar` transitions the whole content region through a brief `loading` shimmer (the re-fetch is real — `GET /v1/makercheckers?actionName=&entityName=` — treat this as a full state transition, not an in-place filter) and back to `content` with the narrowed row set. Clearing all chips (tapping "All" or deselecting the last active chip) re-fetches the full unfiltered queue the same way.

### Open payload

Tapping anywhere on a `command_row` (outside its checkbox and buttons) opens the payload inspect panel:

- On phone: animate as a bottom sheet sliding up over a 32% scrim, `standard_decelerate` easing, ~300ms.
- On tablet/desktop: animate as a side panel sliding in from the trailing edge, splitting the screen into a master list (left) and detail panel (right).
- Panel content: the full command JSON (formatted key/value pairs, values in Roboto Mono), the maker, the made-on timestamp, and — only if the checker canCheck this entry — the same Approve / Reject / Delete controls as the row, rendered at the larger 40dp button size.

### Selection toggle

Tapping `select_toggle` on a row is a pure local state change: the checkbox animates to its checked state (~100ms `short` easing scale-and-fade of the check glyph) and, on the first selection, the multi-select bar slides up from below the visible content over ~200ms. Unchecking the last selected row slides the bar back down and out. No network activity accompanies this interaction.

### Approve / Reject / Delete (single)

Tapping Approve or Reject immediately transitions that one row into its locked/submitting visual — the checkbox and button row are replaced by the "Queued…" chip with a small indeterminate spinner, over a ~150ms cross-fade — while every other row stays exactly as it was. Delete instead first opens the modal confirm dialog described above; only on explicit confirmation does the same locked/submitting transition play. On successful replay, the row plays a ~300ms exit animation (fade + collapse height) and is removed from the list, and its group's count pill decrements; if the group becomes empty its header is removed too.

### Bulk approve

Tapping "Bulk approve" locks every currently-selected row simultaneously (same per-row submitting treatment as a single approve, staggered by ~40ms per row for a pleasant cascade rather than a single instantaneous jump) and clears the multi-select bar once the batch request has been dispatched — not once every reply has landed, since the bar's job is to represent the *selection*, not the in-flight state. Each row resolves independently as its own batch entry succeeds or fails.

### Open Needs Attention

A simple forward navigation transition (standard push/slide, ~300ms) to the needs-attention-inbox screen. No confirm, no loading state — this is a pure read-only jump and never mutates anything in the destination screen.

### Retry

Tapping Retry in the error state immediately transitions to the `loading` shimmer and re-issues the queue fetch; on success it resolves the same way a cold entry would (to content or empty). If the retried fetch instead returns a 403, route to the permission-drift refresh flow rather than looping back to the same error screen — the checker's access may have changed since the app was opened.

---

## Section 5: Content Data

All content below is real demo data sourced from `demo-data.yaml` — zero placeholder text, zero invented values. All monetary amounts are in **KES (Kenyan Shilling)**.

### Entry — audit_id 88201

- action: CREATE · entity: CLIENT · group (entity view): "Clients"
- checker permission required: `CREATE_CLIENT_CHECKER`
- maker: faith.njeri · maker_office: Nairobi CBD Branch
- made_on: 2026-01-15 09:05 · status: Awaiting approval
- resource summary: client "Amara Wanjiru" (external id KE-CLT-2024-10243)
- command payload: firstname `Amara`, lastname `Wanjiru`, officeId `12`, externalId `KE-CLT-2024-10243`, legalFormId `1`, dateOfBirth `1994-03-22`, active `false`, dateFormat `yyyy-MM-dd`, locale `en`

### Entry — audit_id 88202

- action: APPROVE · entity: LOAN · group (entity view): "Loans"
- checker permission required: `APPROVE_LOAN_CHECKER`
- maker: john.kamau · maker_office: Nairobi CBD Branch
- made_on: 2026-01-15 09:12 · status: Awaiting approval
- resource summary: loan/482915 (client Amara Wanjiru)
- command payload: loanId `482915`, approvedOnDate `2026-01-15`, approvedLoanAmount `KES 75,000`, expectedDisbursementDate `2026-01-18`, dateFormat `yyyy-MM-dd`, locale `en`

### Entry — audit_id 88203

- action: DISBURSE · entity: LOAN · group (entity view): "Loans"
- checker permission required: `DISBURSE_LOAN_CHECKER`
- maker: john.kamau · maker_office: Nairobi CBD Branch
- made_on: 2026-01-15 09:40 · status: Awaiting approval
- resource summary: loan/482920 (client Grace Muthoni)
- command payload: loanId `482920`, actualDisbursementDate `2026-01-15`, transactionAmount `KES 120,000`, paymentTypeId `3`, dateFormat `yyyy-MM-dd`, locale `en`

### Grouped views

- groupBy: entity → "Clients" (1): 88201 · "Loans" (2): 88202, 88203
- groupBy: action → "CREATE" (1): 88201 · "APPROVE" (1): 88202 · "DISBURSE" (1): 88203
- groupBy: maker → "faith.njeri" (1): 88201 · "john.kamau" (2): 88202, 88203

### Filter option lists (from `GET /v1/makercheckers/searchtemplate`, demo values)

- actionName ∈ {CREATE, APPROVE, DISBURSE}
- entityName ∈ {CLIENT, LOAN}

### State-copy strings

- Empty title: "All caught up"
- Empty body: "No pending approvals in your scope."
- Empty caption: "Last synced: {most recent successful fetch timestamp, e.g. 2026-01-15 09:40}"
- Error headline: "Couldn't load your approvals queue"
- Error body: "Check your connection and try again."
- Error button label: "Retry"
- Submitting inline chip label: "Queued…" (never "Loading…" — this row is an outbox-pending write, distinct from a network read)

---

## Section 6: Responsive Rules

### Canvas

- Base mobile canvas: 393×852dp (Pixel 5 reference).
- Status bar: 24dp. Gesture nav bar: 48dp (or 56dp for 3-button nav).
- Safe content area: 393×780dp once the 56dp app bar is subtracted.
- Breakpoints: tablet 600dp, desktop 840dp, large 1240dp (per `breakpoints` tokens).

### Phone (0–599dp)

- Single-column list, full-bleed rows.
- Filter chips scroll horizontally rather than wrapping.
- Payload inspect panel opens as a modal bottom sheet covering roughly 85% of the viewport height with a drag handle.

### Tablet (600–839dp) and desktop (≥840dp)

- Navigation promotes to a permanent NavigationRail/drawer — this screen becomes reachable without the drawer overlay.
- Payload inspect panel opens as a persistent side panel (roughly 40% width) beside the master list rather than a bottom sheet, so a checker can review one entry's payload while the list beneath it stays scrollable.
- Filter chips may wrap to two visible rows without scrolling given the extra width.

### Touch targets

- Minimum 48×48dp on every tappable element per `touch_targets.comfortable`.
- The `select_toggle` checkbox's tap target extends beyond its visible 24dp glyph to meet this floor.
- Buttons inside the multi-select bar and payload panel use the 56dp `touch_targets.spacious` sizing since they carry the highest-consequence actions on the screen.

### Font scaling

- Supports system text scaling from 85% to 200%.
- At the upper end, allow the `command_row` secondary line to wrap to a second line rather than truncate the resource reference — truncating a loan amount or client name is never acceptable on an approvals surface.
- Minimum effective text size after any scaling is 12sp.

### Theme

- Light theme is the default and primary reviewed surface for this screen.
- The dark-theme token set exists (`colors.dark.*` in `design-tokens.yaml`) and should be produced as a parallel Figma frame using the same component structure with dark-theme variable bindings — never a hand-tuned one-off.
- Dark-theme primary maps to `#6FD3FF` on `#00344F`; surface maps to `#1A1C1E` on `#E2E2E6` text — the same structural roles, different tonal values.

---

## Handoff Checklist (frame + layer naming)

Name Figma frames and layers so the mapping back to `ui.yaml#components` is unambiguous for the implementing engineer:

- Top-level frame per state: `M15/Loading`, `M15/Content`, `M15/Empty`, `M15/Submitting`, `M15/Error` — one frame per `ui.yaml#states` key, matching the five states enumerated above exactly (no extra, no missing).
- Component instances inside each frame should retain the `ui.yaml#components[].id` as their Figma layer name prefix: `header`, `group_by_selector`, `filter_bar`, `content_area`, `group_header`, `command_row`, `select_toggle`, `priority_badge`, `approve_button`, `reject_button`, `delete_button`, `bulk_approve_button`, `open_needs_attention_link`, `retry_button` — so a design-to-code diff tool can match layer to `testTag` (e.g. `m15-approvals-makerchecker_approve`) without a manual lookup table.
- Publish each interactive component (`command_row`, `select_toggle`, `approve_button`, `reject_button`, `delete_button`, `bulk_approve_button`, `filter_bar` chip, `group_by_selector` segment) as a Figma component with its documented variants (default / hovered / pressed / focused / disabled-or-locked) as variant properties on one component set, not as separate un-linked frames — this keeps the five state-frames above thin (instances + overrides only) and the variant source of truth in one place.
- Before marking the file "ready for dev": confirm every color fill/text pairing in every frame resolves to one of the fifteen `color/*` variables in Section 1 (no raw hex left un-bound to a variable), confirm every frame's `radius`/`spacing` values are token-bound (not hand-typed pixel values), and confirm the three demo entries (audit_id 88201, 88202, 88203) render with their exact real content from Section 5 in the `Content` and `Submitting` frames — a reviewer should be able to read the maker names and KES amounts directly off the canvas without opening the spec.
- Cross-reference `idea-layer/exports/m15-approvals-makerchecker/SPEC.md` for the full ViewModel state/action contract and `idea-layer/exports/m15-approvals-makerchecker/API.md` for the six backing endpoints if any interaction above needs a request/response detail this prompt intentionally keeps at the prose level.
