# Client Roster — Figma Design Hand-off Prompts

> Generated from `screens/client-list/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=b8e94faa19cb · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for account nos).

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` · **on-primary** `#FFFFFF` · **primary-container** `#CBE6FF` (selected chip + selected nav pill) · **secondary** `#00796B` (New-client FAB, teal) · **on-secondary** `#FFFFFF`
- **secondary-container** `#B8F2E6` (Active chip) · **warning** `#F57C00` (Pending/Queued accent) · **surface** `#FCFCFF` · **on-surface** `#1A1C1E` · **on-surface-variant** `#42474E` · **surface-variant** `#DEE3EB` (shimmer) · **outline** `#72777F`
- **Type**: title-large 22/28 · title-medium 16/24 · label-large 14/20 · body-medium 14/20 · body-small 12/16 · mono = Roboto Mono for account nos
- **Radius**: FAB lg 16 · chip full/28 · status chip sm 8 · **Spacing**: 8pt grid, 16dp row padding

---

## Screen: Content (Success state)

Design the **content** state of the Client Roster for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (56dp, `surface`): title **"Clients"**, leading menu (☰) when entered as the Clients nav root (back arrow when drilled in).

Below: a **search field** (`cl_search`, full width minus 16dp margins, rounded, `surface-variant` fill, leading 🔍 icon, placeholder "Search name, account no or external id"). Below it, a scrollable **status filter-chip row** (`cl_status_filter`): **All · Pending · Active · Closed** — active chip `primary-container #CBE6FF`, inactive outlined.

Then a single-column **roster list**. Each row (`cl_row`, 2 lines, 12dp padding, 1px `outline` separator): client display name (`body-medium` `on-surface`) with a trailing **status chip** (Active = `secondary-container #B8F2E6`; Pending = `warning #F57C00` tint; Queued = warning tint), and the account no in Roboto Mono; second line = office · assigned staff in `body-small` `on-surface-variant`. Seed with real data: **Grace Wanjiru Mwangi** `000010241` Active · Nairobi CBD · Peter Kariuki; **Samuel Otieno Odhiambo** `000010242` Active · Mercy Achieng; **Amina Hassan Ali** `000010243` **Pending**; **Joseph Kamau Njoroge** (external id KE-CLT-OFFLINE-a91f) shown immediately with a **Queued** indicator (created offline). Infinite scroll loads the next page.

Bottom-end **FAB** (`cl_new_client`): teal `secondary #00796B`, `on-secondary` "+" icon, contentDescription "Start a new client application" — shown **only** when CREATE_CLIENT is held. Bottom navigation bar (Home · **Clients** selected · Collections · Sync), selected pill `primary-container`.

---

## Screen: Loading

Design the **loading** state. Keep the app bar, search field, and filter-chip row. Replace roster rows with ~6 two-line **shimmer skeletons** (bg `surface-variant #DEE3EB`, 1.2s pulse). Keep the bottom nav.

---

## Screen: Empty

Design the **empty** ("no matches") state. Keep the search + chips. Center an empty block: a 48dp muted people icon (`on-surface-variant`), headline **"No clients found"** in `title-medium`, sub-line "Try a different search or filter." in `body-medium`. If CREATE_CLIENT is held, show a text button **"New client"** and keep the FAB.

---

## Screen: Error

Design the **error** state (first page failed, no cache). Keep the app bar. Center: 48dp `[!]` icon in `error #BA1A1A`, body copy in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (`cl_error_retry`, bg `primary #0091EA`, `on-primary`, "Retry loading the client list"). Retry → Loading → Content.

---

## Prototype Interactions

- Search typing → debounced in-VM filter; escalates to `GET /v1/search` only when local pages are exhausted.
- Status chip tap → filter in place (no refetch).
- Row tap → navigate to client-detail-360.
- FAB tap → navigate to the dynamic client-create form (dynamic-template-forms).
- Retry → Error → Loading → Content.
