# Capability Map Detail — Figma Design Hand-off Prompts

> Generated from `screens/capability-map-detail/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=6a89fb489c5f · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Format: natural-language design instructions per state — paste into Figma AI / share with a designer.
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for numerics).

---

## §DS — Design System Variables (map once in Figma)

Create Figma variables from `design-tokens.yaml`:

- **Color / primary** `#0091EA` · **on-primary** `#FFFFFF` · **primary-container** `#CBE6FF` · **on-primary-container** `#001E30`
- **secondary-container** `#B8F2E6` (satisfied badge) · **error-container** `#FFDAD6` (denied badge) · **on-error-container** `#410002`
- **surface** `#FCFCFF` · **on-surface** `#1A1C1E` · **surface-variant** `#DEE3EB` (shimmer) · **on-surface-variant** `#42474E` · **outline** `#72777F`
- **Type**: title-large 22/28 w600 · title-medium 16/24 w500 · label-large 14/20 w500 · body-medium 14/20 w400 · body-small 12/16 w400 · mono = Roboto Mono 14 for checksum
- **Radius**: card lg 16 · chip xs 4 · **Spacing**: 8pt grid, row-padding 12, section-gap 24 · **Elevation**: prefer 1px outline borders over shadows (density 7)

---

## Screen: Content (Success state)

Design the **content** state of the Capability Map Detail screen for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (small M3, height 56dp, bg `surface #FCFCFF`, 1px bottom border `outline`): a 24dp back arrow leading icon (`on-surface #1A1C1E`, contentDescription "Back") and the title **"Capability Map"** in title-large `on-surface`.

Below, a **metadata header card** (full-width minus 16dp side margins, radius 16dp, bg `surface`, 1px `outline` border, no shadow, 16dp inner padding). Lay out as a two-column key/value grid: **Version** `2026.07.2`, **Source** `remote`, **minApp** `3.4.0`. Below the grid, a full-width row: label "sha256" then the value **`9f2c4a7b…06b1e4`** in **Roboto Mono** (`body-medium`, `on-surface-variant`, selectable), and a trailing **text button "Copy"** (`primary #0091EA` label, 44dp min touch target, contentDescription "Copy the capability map sha256 checksum to the clipboard").

Below the card, a section divider label **"Requirement tree"** (`label-large`, `on-surface-variant`, with a 1px hairline). Then a vertical list of **module requirement nodes** — one per back-office module. Each node is a 48dp-min row: a leading disclosure caret (▸ collapsed / ▾ expanded), the module **label** (`title-medium`, `on-surface`), the required **permission group** (`body-small`, `on-surface-variant`), and a trailing **satisfied/denied status chip**. Satisfied = chip bg `secondary-container #B8F2E6`, ✔ glyph + "Satisfied"; Denied = chip bg `error-container #FFDAD6`, ⊘ glyph + "Denied" (`on-error-container`). Never colour-only — the glyph + text carry the state.

Seed the tree with real demo content: **Loan Portfolio** (group `transaction_loan`, **Denied ⊘**), **Clients** (group `portfolio`, **Satisfied ✔**, shown expanded revealing `READ_CLIENT ✔` and `CREATE_CLIENT ✔` as small mono code chips), **Accounting** (group `accounting`, **Denied ⊘**), **Maker-Checker** (group `authorisation`, **Denied ⊘**). Tapping a node expands it in place (no navigation) to list its required codes with a per-code held/not-held tick.

---

## Screen: Loading

Design the **loading** state. Keep the top app bar identical ("Capability Map", back arrow). Replace the header card and every requirement row with **shimmer skeletons**: bg `surface-variant #DEE3EB`, radius 12dp, 1.2s pulse. Show one card-height skeleton block (matching the metadata card) and four row-height skeleton blocks (matching the tree rows). No real text, no error. This reflects the CapabilityMap being read and each module requirement resolved against the PermissionSet.

---

## Screen: Empty

Design the **empty** state (pre-bootstrap — no CapabilityMap resolved yet). Keep the app bar. Center a vertical empty-state block: a 48dp muted illustration/icon (`on-surface-variant`), then a headline in `title-medium` and the body copy **"No CapabilityMap has been resolved yet — sign in to bootstrap your permitted surface"** in `body-medium` `on-surface-variant`. No CTA button (guidance panel only — resolution happens on auth).

---

## Screen: Error

Design the **error** state (grouping catalog failed, no cache — labels unavailable). Keep the app bar. Center an error block: a 48dp `[!]` error icon in `error #BA1A1A`, a headline, the body copy **"The permission grouping catalog failed to load — group labels are unavailable"** in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (140×48dp, radius 12dp, bg `primary #0091EA`, label `on-primary #FFFFFF` label-large, contentDescription "Retry loading the permission grouping catalog"). Tapping Retry reloads `GET /v1/permissions` and returns to the loading state.

---

## Prototype Interactions

- `cm_module` tap → expand/collapse in place (no navigation).
- `cm_copy_checksum` tap → copy checksum to clipboard, show a brief snackbar "Checksum copied".
- `cm_error_retry` tap → transition Error → Loading → Content.
- System back → return to `permission-capability-engine`.
