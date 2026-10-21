# TEST SPEC — Accounts

| Field      | Value                          |
|------------|--------------------------------|
| Feature    | accounts                       |
| Source     | `screens/accounts/tests.yaml`  |
| Scenarios  | 9                              |
| Priorities | not declared (see note)        |
| States     | content 6 · loading 1 · error 1 · empty 1 |
| Module     | `feature/accounts`             |

---

## Coverage

All four declared states covered. Ids are non-contiguous by design: TC-ACCTS-007 was **deleted**
on 2026-08-01, and 008–010 were deliberately not renumbered so external references to those ids
keep resolving.

**No scenario on this screen declares a `priority`.** That is not a transcription gap — the field
is absent in `tests.yaml`. Nine of the project's 41 priority-less scenarios are here, the largest
single concentration. Surfaced rather than defaulted: guessing `high` for all nine would make an
authoring gap look like a decision.

---

## Deleted scenario — TC-ACCTS-007

Recorded because a spec that silently skips an id invites someone to re-add it.

TC-ACCTS-007 asserted `state: consent_expiring`, a "Consent expiring soon" warning banner and a
"Reconfirm access" button. **None of the three exist.** `ui.yaml:109` declares
`[loading, content, empty, error]`, and `_strings/strings.yaml:58` records the matching prune
("Pruned 2026-07-28: consent_expiring.* (no such state)").

This was a half-applied sweep: the 07-28 reverse sync removed the state and its strings in one
edit but left the test that exercised them. The scenario was *unsatisfiable*, not merely
mislabelled — there was no surviving surface to retarget it at — so it was deleted rather than
repointed. Consent expiry is covered where it is actually implemented: the consent-list reconfirm
banner (TC-CLIST-006) and the consent-detail expiry warning.

---

## TC-ACCTS-001 — Accounts list loads and renders a balance preview per account

**State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 5 accounts and their balances
- **When** Screen mounts
- **Then**
  - Five account cards render (Everyday Current, ISA Saver, Platinum Mastercard, Global Money, Global Wallet — USD)
  - Each card shows account subtype, masked/formatted account identifier, and `InterimAvailable` balance
  - Total balance `stat_block` shows £15,797.63 (GBP accounts only)
  - Balance amounts match demo-data values

---

## TC-ACCTS-002 — Loading state shows shimmer skeleton cards during fetch

**State:** loading

- **Given** Slow network; API calls in flight
- **When** Screen mounts
- **Then**
  - Three shimmer skeleton card placeholders visible with pulsing animation
  - Account list, filter chips and total balance stat NOT rendered

---

## TC-ACCTS-003 — Error state with Retry on 401 token expired

**State:** error

- **Given** Access token is expired; accounts-list returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with error icon and "Your session has expired. Please sign in again."
  - Retry button visible with accessibility label "Retry loading accounts"
  - Tapping Retry re-triggers `accounts_and_balances_load`

---

## TC-ACCTS-004 — Empty state when no accounts are returned

**State:** empty

- **Given** HSBC returns `OBReadAccount6` with an empty `Data.Account[]` (PSU selected no accounts during consent)
- **When** Screen mounts
- **Then**
  - Empty state renders with `account_balance_wallet` icon
  - Title "No accounts found" and body directing the PSU to revoke and re-authorise

The body text is the substantive assertion. An empty account set here is almost never a bank-side
condition — it means the PSU consented to nothing, and the only route out is re-authorisation.

---

## TC-ACCTS-005 — Tapping an account card navigates to account-detail

**State:** content

- **Given** Accounts list rendered in content state with the "Everyday Current" card (`accountId=40051512345678`) visible
- **When** User taps the "Everyday Current" card
- **Then** Navigates to account-detail with `accountId=40051512345678`

---

## TC-ACCTS-006 — GlobalMoney and GlobalWallet multi-currency cards render correctly

**State:** content

- **Given** HSBC sandbox returns 5 accounts including GlobalMoney (GBP) and GlobalWallet (USD)
- **When** Screen mounts and content state renders
- **Then**
  - GlobalMoney card shows "Global Money", `public` icon, £500.00 balance
  - GlobalWallet card shows "Global Wallet — USD", `currency_exchange` icon, "USD 250.00"
  - GlobalWallet balance displays its native currency code (USD), not GBP
  - Both cards are excluded from the GBP total (`totalBalanceFormatted` stays £15,797.63)

The last two assertions are the same defect approached from both ends: rendering a USD balance
with a £ sign, and summing it into a GBP total, are one mistake. Catching only the display half
would leave a total that is quietly wrong.

---

## TC-ACCTS-008 — CreditCard account displays a "Balance owed" badge in the error colour

**State:** content

- **Given** Platinum Mastercard in content state (`CreditDebitIndicator=Debit`, £342.18)
- **When** Accounts list renders
- **Then**
  - £342.18 renders in the `error` colour, not default `onSurface`
  - "Balance owed" tonal badge visible on the card
  - Other accounts (CurrentAccount, Savings) show no badge and use the default colour

The control assertion on the last line is what makes this a real test — colouring *every* balance
`error` would satisfy the first two.

---

## TC-ACCTS-009 — Account-type filter chip narrows the visible cards

**State:** content

- **Given** All 5 accounts loaded (CurrentAccount, Savings, CreditCard, GlobalMoney, GlobalWallet)
- **When** User taps the "Savings" chip filter
- **Then**
  - Only the "ISA Saver" card is visible
  - CurrentAccount, CreditCard, GlobalMoney and GlobalWallet cards not rendered
  - "All" chip is deselected; "Savings" chip is selected

---

## TC-ACCTS-010 — Partial balance failure renders the card without its balance

**State:** content

- **Given** accounts-list returns 5 accounts; the balances call for ISA Saver returns 403 (`ReadBalances` not in consent)
- **When** Screen mounts
- **Then**
  - ISA Saver card renders with account details but no balance row
  - Other accounts with successful balance calls show balances normally
  - Screen does NOT enter the error state

This is the most valuable scenario on the screen. OBIE grants `ReadAccountsDetail` and
`ReadBalances` independently, so a per-account balance 403 is a normal consent shape, not a
failure. Collapsing the whole list into an error state because one balance was refused would hide
four accounts the PSU is fully authorised to see.

---

_Generated by /idea-feature-test-export | 2026-08-03_
