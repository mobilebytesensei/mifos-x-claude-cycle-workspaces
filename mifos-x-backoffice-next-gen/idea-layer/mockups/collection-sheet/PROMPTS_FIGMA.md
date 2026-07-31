# Collection Sheet — Figma Design Hand-off Prompts

> Generated from `screens/collection-sheet/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=659dd90d5f6d · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for all amounts).

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` (Save fill) · **on-primary** `#FFFFFF` · **primary-container** `#CBE6FF` (selected nav pill) · **secondary-container** `#B8F2E6` (present-attendance chip)
- **surface** `#FCFCFF` · **on-surface** `#1A1C1E` · **on-surface-variant** `#42474E` · **surface-variant** `#DEE3EB` (currency-field fill + shimmer) · **outline** `#72777F` · **error** `#BA1A1A`
- **Type**: title-large 22 (group headers) · title-medium 16/24 · label-large 14/20 · body-medium 14/20 · body-small 12/16 · mono = Roboto Mono for all amounts + totals
- **Radius**: currency field sm 8 · Save button 28 · **Spacing**: 8pt grid, 16dp row padding, 8dp group indent

---

## Screen: Content (Success state)

Design the **content** state of the Collection Sheet for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (56dp, `surface`): back arrow, title **"Collection Sheet"** with a meeting-date subtitle **"25 Jul 2026"** in `body-small` `on-surface-variant`.

Body: a scrollable **grouped route**. Each group has a **center → group header** (`title-large`/collapsible caret): e.g. "Kawangware Center A → Umoja Women's Group". Under it, per client: the client name row with a right-aligned **attendance toggle** (`cs_attendance`, segmented present/absent/late; present uses `secondary-container #B8F2E6`), then indented **due rows** — each showing the product name + due label (`body-medium` `on-surface-variant`) and an editable **currency field** (`cs_row_amount`, `surface-variant #DEE3EB` fill, radius 8, numeric keyboard, Roboto Mono, prefilled with the due). Seed with real data: **Grace Wanjiru Mwangi** — Group Business Loan due **KES 6,000**, Mandatory Savings due **KES 500**; **Samuel Otieno Odhiambo** — Group Business Loan due **KES 4,500**, Mandatory Savings due **KES 500**. After each group show a **running total** row ("Group total: KES 11,500", Roboto Mono).

Pinned to the sheet foot: a full-width **filled primary button "Save collection sheet"** (`cs_save`, bg `primary #0091EA`, `on-primary` label) — shown only when SAVECOLLECTIONSHEET is held (otherwise capture-only, no Save). Bottom nav (Collections tab selected) when entered via the tab.

---

## Screen: Loading

Design the **loading** state. Keep the app bar. Render 2-3 group blocks with client rows + due fields as **shimmer skeletons** (bg `surface-variant #DEE3EB`, 1.2s pulse). No Save button.

---

## Screen: Empty

Design the **empty** ("nothing due today") state. Keep the app bar. Center a block: a 48dp calendar-check icon (`secondary #00796B`), headline **"Nothing due today"** in `title-medium`, sub-line "No meetings or dues for the selected date." in `body-medium` `on-surface-variant`. No Save.

---

## Screen: Error

Design the **error** state (generate failed no cache, or Save failed hard). Keep the app bar. Center: 48dp `[!]` icon in `error #BA1A1A`, body copy in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (`cs_error_retry`, bg `primary #0091EA`, `on-primary`, "Retry loading the collection sheet"). Note captured amounts are preserved from local state on re-generate. Retry → Loading → Content.

---

## Prototype Interactions

- Currency field edit → recompute per-group + sheet totals in place (no network).
- Attendance toggle → set present/absent/late in place.
- Save tap → enqueue whole route as ONE batch to the outbox; show a queued badge; snackbar "Sheet queued for sync".
- Retry → Error → Loading → Content.
- System back → return to the M01 dashboard.
