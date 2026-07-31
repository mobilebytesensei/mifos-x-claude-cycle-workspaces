# Maker-Checker Inbox — Figma Design Hand-off Prompts

> Generated from `screens/checker-inbox/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=ec6c0c19268b · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for amounts/IDs).

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` · **on-primary** `#FFFFFF` · **primary-container** `#CBE6FF` (selected chip) · **error** `#BA1A1A` (Reject/destructive) · **error-container** `#FFDAD6`
- **surface** `#FCFCFF` · **on-surface** `#1A1C1E` · **on-surface-variant** `#42474E` · **surface-variant** `#DEE3EB` (shimmer) · **outline** `#72777F`
- **warning-strong** `#B45309` (offline-queued banner) · **on-warning** `#FFFFFF`
- **Type**: title-large 22/28 · title-medium 16/24 w500 · label-large 14/20 w500 · body-medium 14/20 · body-small 12/16 · mono = Roboto Mono for KES amounts + account numbers
- **Radius**: chip full/28 · button 28 · row 0 (separators) · **Spacing**: 8pt grid, 12dp row padding, 16dp side margins

---

## Screen: Content (Success state)

Design the **content** state of the Maker-Checker Approvals Inbox for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (56dp, `surface`, 1px bottom `outline`): back arrow (`on-surface`, "Back") and title **"Approvals"** in title-large.

Below the app bar, a **horizontal filter-chip row** (`ci_entity_filter`, scrollable, 12dp padding): chips **All · Loan · Client · Savings · GL**. The active chip uses `primary-container #CBE6FF` fill with `on-primary-container` label; inactive chips are outlined (`outline`, transparent). 44dp min touch height.

Below, a vertical **queue list**. Each row is a two-line card-less list item (full width, 12dp vertical padding, 1px `outline` bottom separator):
- Line 1: an **action · entity** eyebrow in `label-large` uppercase (e.g. "APPROVE · LOAN"), right-aligned **maker** username (`body-small`, `on-surface-variant`) and **made-on** date ("24 Jul").
- Line 2: the **command summary** in `body-medium` `on-surface`, with any KES amount + account number in **Roboto Mono**.
- Trailing: inline **Approve** (filled button, bg `primary #0091EA`, label `on-primary`) and **Reject** (text/outline button, `error #BA1A1A` label). These controls appear **only** on rows the user `canCheck(action,entity)`; unauthorized rows show no controls (read-only). While a decision applies, the row shows a small inline spinner (`resolvingId`).

Seed with 4 real rows: **APPROVE · LOAN** "Approve loan 000055231 · Grace Wanjiru Mwangi · KES 60,000" (maker mercy.achieng); **CREATE · CLIENT** "Create client · Joseph Kamau Njoroge · Nairobi CBD" (peter.kariuki); **WITHDRAWAL · SAVINGS** "Withdraw KES 5,000 · savings 000078012 · Grace Wanjiru Mwangi" (mercy.achieng); **CREATE · JOURNALENTRY** "Manual journal entry · Head Office · KES 250,000" (accountant.njeri).

When offline, show a persistent slim banner below the app bar (`warning-strong #B45309` fill, `on-warning` text): "Offline — decisions will sync when you reconnect."

---

## Screen: Loading

Design the **loading** state. Keep the app bar ("Approvals") and the filter-chip row. Replace the queue rows with **shimmer skeletons**: two-line row skeletons (bg `surface-variant #DEE3EB`, 1.2s pulse) — about 6 of them. No real text, no controls.

---

## Screen: Empty

Design the **empty** ("all clear") state. Keep the app bar. Center a vertical block: a 48dp success/check illustration (`secondary #00796B`), headline **"No commands are waiting for your approval"** in `title-medium`, and a `body-small` `on-surface-variant` sub-line showing the last-checked timestamp ("Last checked 24 Jul, 12:20"). No action buttons.

---

## Screen: Error

Design the **error** state. Keep the app bar. Center an error block: 48dp `[!]` icon in `error #BA1A1A`, body copy **"Couldn't load the checker inbox — showing the last synced queue"** in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (140×48dp, radius 28dp, bg `primary #0091EA`, `on-primary` label, "Retry loading the checker inbox"). Retry → Loading → Content.

---

## Prototype Interactions

- Entity chip tap → filter queue in place (no navigation).
- Approve tap → enqueue decision to outbox, show inline spinner, then the row leaves; snackbar "Approval queued".
- Reject / Delete tap → confirmation dialog first, then enqueue; row leaves with an audit note. Reject uses the destructive `error` accent.
- Retry tap → Error → Loading → Content.
- System back → return to the M01 dashboard.
