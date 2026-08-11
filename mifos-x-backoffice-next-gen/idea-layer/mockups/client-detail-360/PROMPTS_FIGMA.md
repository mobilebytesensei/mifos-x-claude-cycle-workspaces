# Client 360 — Figma Design Hand-off Prompts

> Generated from `screens/client-detail-360/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=6e48a28eed9d · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for account nos + balances).

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` · **on-primary** `#FFFFFF` · **secondary** `#00796B` (Assign-staff) · **secondary-container** `#B8F2E6` (Active chip) · **on-secondary-container** `#00201A`
- **surface** `#FCFCFF` · **on-surface** `#1A1C1E` · **on-surface-variant** `#42474E` · **surface-variant** `#DEE3EB` (shimmer) · **outline** `#72777F` · **error** `#BA1A1A`
- **Type**: title-large 22/28 (client name) · title-medium 16/24 · label-large 14/20 · body-medium 14/20 · body-small 12/16 · mono = Roboto Mono for account nos + KES balances
- **Radius**: card lg 16 · chip sm 8 · button 28 · **Spacing**: 8pt grid, 16dp margins, 12dp row padding

---

## Screen: Content (Success state)

Design the **content** state of the Client 360 profile for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (56dp, `surface`, 1px bottom `outline`): back arrow + title = the client display name **"Grace Wanjiru Mwangi"** in title-large `on-surface`.

**Identity card** (`cd_header`, full width minus 16dp margins, radius 16dp, bg `surface`, 1px `outline`, 16dp padding): the display name in title-medium; a trailing **status chip** ("Active", chip bg `secondary-container #B8F2E6`, `on-secondary-container` label, radius 8). Below: account no **`000010241`** and external id **`KE-CLT-2024-10241`** in Roboto Mono `body-small`; then office **"Nairobi CBD"** · officer **"Peter Kariuki"** in `body-small` `on-surface-variant`; legal form PERSON.

**Tab row** (`cd_tabs`, M3 primary tabs, `primary #0091EA` indicator): **General · Accounts · Notes**. Default selection Accounts for this hand-off.

**Accounts tab body**: a list of account rows (`cd_account_row`, 48dp+ each, 1px separators). Each row: product name (`body-medium` `on-surface`), account no + status, and a right-aligned balance in Roboto Mono. Seed with real data — *Group Business Loan* `000055231` Active **KES 42,500**; *Emergency Loan* `000055890` Closed **KES 0**; *Mandatory Savings* `000078012` Active **KES 8,340.50**; *Voluntary Savings* `000078455` Active **KES 22,100**. Tapping a loan row navigates to loan-detail (savings/shares open their own detail).

**Permission-gated action bar** (bottom): a filled primary button **"Activate"** (`cd_activate`, bg `primary #0091EA`, `on-primary` label) shown only for a *pending* client with ACTIVATE_CLIENT; a **"Assign Staff"** secondary/outlined button (`cd_assign_staff`, `secondary #00796B` accent) shown when ASSIGNSTAFF_CLIENT is held. For this Active client, Activate is absent and Assign Staff is present.

---

## Screen: Loading

Design the **loading** state. Keep the app bar. Render the identity card, tab strip, and ~4 account rows as **shimmer skeletons** (bg `surface-variant #DEE3EB`, 1.2s pulse). No real text, no action bar.

---

## Screen: Empty

Design the **empty** ("client not found") state. Keep a back arrow in the app bar. Center a not-found block: a 48dp muted person-off icon (`on-surface-variant`), headline **"Client not found"** in `title-medium`, sub-line "This client may have been deleted or the id is wrong." in `body-medium`, and a text button **"Go back"**.

---

## Screen: Error

Design the **error** state (client load failed, no cache). Keep the app bar. Center: 48dp `[!]` icon in `error #BA1A1A`, body copy in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (`cd_error_retry`, bg `primary #0091EA`, `on-primary`, "Retry loading the client profile"). Retry → Loading → Content. Note: an accounts-only failure does NOT show this whole-screen error — instead the Accounts tab shows an inline retry strip while the identity header stays rendered.

---

## Prototype Interactions

- Tab tap → switch body in place (no refetch).
- Account row tap (loan) → navigate to loan-detail.
- Activate / Assign Staff → confirmation, then enqueue to outbox; status chip / staff field update in place with a queued badge until sync.
- Retry → Error → Loading → Content.
- System back → return to the M02 clients list.
