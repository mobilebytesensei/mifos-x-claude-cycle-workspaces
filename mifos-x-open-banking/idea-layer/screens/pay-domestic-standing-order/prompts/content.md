---
feature: pay-domestic-standing-order
state: content
generated_by: idea-feature-export
design_system: Open Banking — Trust Blue v1.4.0
---

# pay-domestic-standing-order — content state

<!-- COPY PROVENANCE: quoted copy is VERBATIM strings.payment.* / pay_domestic_standing_order.*
     catalogue text. Four slots have no key at all and stay marked COPY GAP = render EMPTY,
     never invented. -->

↓↓↓ MOCKUP PROMPT

Render FOUR sub-frames (one per step). All share: top app bar (`arrow_back`, "Standing order"
`titleLarge`), step indicator (Payee / Schedule / Amount / Review), bottom nav (Home · Accounts
· Pay active · More). Tokens by NAME only — no hex, no inline sizes.

## STEP 1 — Payee

**[no_debtor_note]** MANDATORY — `color/surfaceContainerLow`, `radius/md`, icon `info`, text
`bodyMedium` `color/onSurfaceVariant`: "You choose the account this comes from when you approve
the standing order with HSBC, not here."

Beneficiary list, section label "Choose who to pay" (`labelLarge`, `color/onSurfaceVariant`).
Rows Fill×72dp: `account_balance` (`icon/md`, `color/primary`) · name (`bodyLarge`) / sort code
+ account (`bodyMedium`, mono) · `chevron_right`. "Mr Mark" / "80-20-01  10203349" ·
"Greenways Ltd" / "20-45-67  87654321"
"Enter account details instead" text button (`labelLarge`, `color/primary`).

## STEP 2 — Schedule

**[frequency_picker]** "How often"; value "Monthly", `expand_more`. Menu open: EXACTLY 5 items —
Weekly · Every 2 weeks · Monthly (selected, `color/primaryContainer`) · Every 3 months · Yearly.

**[first_payment_date_picker]** "First payment date"; value "13 Aug 2026", `calendar_today`.
**[has_end_date_switch]** "Set an end date" · Switch ON.
**[final_payment_date_picker]** (ON only): "Final payment date"; value "4 Dec 2026".
<!-- COPY GAP: no key for a 12-month bound helper; ui.yaml declares no helper_text here. -->

## STEP 3 — Amount

**[amount_field]** "Amount of each payment"; prefix "£"; input "25.00" (`headlineSmall`).
**[varying_amounts_switch]** "Use different amounts for later payments" · Switch OFF.
**[reference_field]** "Reference (optional)"; value "Monthly rent"; helper (`bodySmall`,
`color/onSurfaceVariant`) "Shown on the recipient's statement. Up to 35 characters."; count
"12/35" (`labelSmall`).
<!-- COPY GAP ×2: no key for the amount-field helper or the equal-amounts sub-label. -->

## STEP 4 — Review

**[review_card]** `color/surfaceContainerLow`, `radius/md`, level1, divider
`color/outlineVariant`. Rows Fill×56dp, in this order:
- To | Mr Mark · 80-20-01 10203349
- How often | Monthly · First payment | 13 Aug 2026 · Final payment | 4 Dec 2026
- Amount | £25.00 · Reference | Monthly rent
- HSBC's charge | £0.05 — amount + currency ONLY, NEVER the Type
<!-- COPY GAP: no key for the review card title. -->

**[amend_notice]** MANDATORY — `color/tertiaryContainer`, `radius/md`, icon `warning`
(`color/tertiary`), text `bodyMedium` `color/onTertiaryContainer`: "Once this standing order is
set up, this app cannot change it or cancel it. To change the amount or the schedule, or to
stop it altogether, use the HSBC app or online banking."

**[confirm_button]** "Set up this standing order" — `color/primary`, `radius/full`,
`labelLarge` `color/onPrimary`. Must NOT read "Send £25.00" — nothing is sent today.

## Self-Validation Checklist

- [ ] 4 sub-frames; frequency picker has exactly 5 options; no_debtor_note on Step 1
- [ ] Fee row: amount + currency only (no Type)
- [ ] amend_notice on Step 4: `color/tertiaryContainer`, catalogue copy verbatim
- [ ] No text rendered into any slot marked COPY GAP

↑↑↑ MOCKUP PROMPT
