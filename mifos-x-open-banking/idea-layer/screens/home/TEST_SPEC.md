# TEST SPEC — Home

| Field      | Value                       |
|------------|-----------------------------|
| Feature    | home                        |
| Source     | `screens/home/tests.yaml`   |
| Scenarios  | 13                          |
| Priorities | medium 2 · not declared 11  |
| States     | content 8 · error 3 · loading 1 · empty 1 |
| Module     | `feature/home`              |

---

## Coverage

All four declared states covered. Ids are non-contiguous in two different ways, and only one of
them is a deletion:

- **TC-HOME-016 was removed** on 2026-07-30 (`/idea-feature-export` stale-artifact fix) — see below.
- **TC-HOME-004, -005, -008, -009 never existed in this file.** No deletion record accompanies
  them, so they are gaps in the numbering rather than removals. Recorded so a later pass does not
  read the absence as a second deletion, and does not "restore" scenarios that were never written.

**11 of 13 scenarios declare no `priority`.** Only TC-HOME-017 and TC-HOME-018 do (both `medium`),
and both declare it *after* `then:` rather than before — the two most recently appended scenarios.
Surfaced, not defaulted.

---

## Deleted scenario — TC-HOME-016

TC-HOME-016 asserted "Statements quick action navigates to statements screen". The quick-actions
row was removed from source and its 119-line `ui.yaml` card deleted in the same pass. `homeGraph`
exposes only `onNavigateToTransactions` and `onNavigateToTransactionDetail`, so there is no
statements callback for the test to exercise.

**Contradiction resolved 2026-08-03** (`/idea-sync`). TC-HOME-001 still asserted "Quick actions row
shows Pay (disabled), Transactions, Statements, Manage consents", and TC-HOME-002 listed an
"actions row" shimmer — both describing the same removed surface, in direct conflict with the
deletion note above. Settled against **source**, not by picking a record: `rg -i 'quickaction|quick_action'`
over `feature/home/src` returns 0 matches across 18 files, and `HomeDestination.kt:30-31` exposes
only the two callbacks. `ui.yaml` carries a tombstone comment where `quick_actions_card` was,
`docs.yaml:34` records the removal, `_strings/strings.yaml:503` records the 9 orphaned string keys
it swept. Every artifact agreed except these two assertions; both are now removed.

---

## Authoring-format note

This file is the only `tests.yaml` in the corpus written in a **dumper-normalised** style: `£`
appears as the escape `\xA3`, long `given:` values use quoted line-continuations, and list
indentation alternates between two- and four-space within one document. It parses correctly and
the content is intact — recorded only because a hand-edit here will not round-trip to the same
shape as its siblings.

---

## TC-HOME-001 — Content state loads for the default selected account

**State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 3 accounts; `selectedAccountId = '40051512345678'` (Everyday Current); `/accounts/{id}/balances` returns InterimAvailable £2,847.63; `/accounts/{id}/transactions` returns 5 booked entries
- **When** Screen mounts
- **Then**
  - Account switcher strip renders 3 chips: "Everyday Current" (selected), "ISA Saver", "Platinum Mastercard"
  - Hero balance card shows Nickname "Everyday Current", balance "£2,847.63", identifier "40-05-15 12345678"
  - Recent transactions section shows 5 rows, most recent first: AMAZON UK, PRET A MANGER, TESCO, TFL, SALARY
  - Spending snapshot card shows "£167.41" and top category "Groceries"

---

## TC-HOME-002 — Loading state shows shimmer skeletons during initial fetch

**State:** loading

- **Given** Slow network; API calls in flight
- **When** Screen mounts
- **Then**
  - Hero card and 3 transaction-row shimmers visible with pulsing animation
  - No balance amount, account chip, or transaction rows rendered
  - Accessibility label "Loading your account" present

The "actions row" shimmer was dropped from this list on 2026-08-03 for the same reason as
TC-HOME-001's assertion — a skeleton cannot mirror a component that no longer composes.

The shimmer *shape* mirrors the content layout rather than replacing it with a spinner, and the
negative assertion is what keeps that honest — a skeleton that renders alongside a real balance is
a flash of wrong data, not a loading state.

---

## TC-HOME-003 — Account switcher re-loads content for a different account

**State:** content

- **Given** Content state with Everyday Current selected
- **When** User taps the "ISA Saver" chip
- **Then**
  - Loading state briefly shown
  - Hero balance card updates to ISA Saver nickname and balance (£12,450.00)
  - Recent transactions update to ISA Saver transactions
  - "ISA Saver" chip now selected; "Everyday Current" unselected

The transactions assertion is the one that catches the real bug: updating the hero balance while
leaving the previous account's transactions below it produces a screen that is coherent-looking
and wrong.

---

## TC-HOME-006 — "View all" link navigates to transactions

**State:** content

- **Given** Home rendered in content state for account 40051512345678 with the recent transactions section populated
- **When** User taps the "View all" text button in the recent transactions header
- **Then** `onNavigateToTransactions(accountId)` fires → `TransactionsRoute(accountId=40051512345678)`

This scenario's component (`home#view_all_transactions_link`, a `text_button`) was one of the two
that `action-contract-walk.ts` could not evaluate until its INTERACTIVE set widened on 2026-07-31.
It now evaluates and passes.

---

## TC-HOME-007 — Account selector sheet opens, selects and dismisses without navigating

**State:** content

- **Given** Home rendered in content state; the PSU holds more than one authorised account so the switcher offers a choice
- **When** User taps the hero card account switcher, picks a different account chip, then dismisses
- **Then**
  - `OpenAccountSelector` sets `isAccountSelectorVisible = true`; `home_account_selector_sheet` displayed
  - Tapping an account chip dispatches `SelectAccount` and persists `selectedAccountId` via `UserDataRepository`
  - `DismissAccountSelector` sets `isAccountSelectorVisible = false`
  - **No navigation occurs at any point**

The final assertion is the whole scenario. Account switching is a state change on one screen, not
a route — and the persistence step is what TC-HOME-018 later depends on across a cold restart.

---

## TC-HOME-010 — Error state with retry CTA on 401 token expired

**State:** error

- **Given** Access token expired; `/accounts` returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Title renders from `{strings.home.error.title}`
  - Body shows "Your session has expired. Please sign in again."
  - Retry button visible (`error.recoverable = true`)
  - Tapping Retry re-triggers `home_load`

---

## TC-HOME-011 — Non-recoverable 403 hides the Retry button

**State:** error

- **Given** `ReadAccountsDetail` permission absent; `/accounts` returns 403
- **When** Screen mounts
- **Then**
  - Error state renders with "Account access permission denied" body
  - Retry button **NOT** visible (`error.recoverable = false`)

---

## TC-HOME-012 — Empty state with CTA when no accounts are returned

**State:** empty

- **Given** HSBC returns `OBReadAccount6` with an empty `Data.Account[]`
- **When** Screen mounts
- **Then**
  - Empty state renders with `account_balance_wallet` icon
  - Title and body from `{strings.home.empty.*}` visible
  - CTA button "Connect your bank" navigates to login

Home's empty state offers a route out (re-connect) where accounts' equivalent (TC-ACCTS-004) only
explains. Both are defensible for their position in the app — home is where a first-run customer
lands — but they are different treatments of the same server condition.

---

## TC-HOME-013 — Tapping a recent transaction row navigates to transaction-detail

**State:** content

- **Given** Home rendered in content state; recent transactions include "AMAZON UK MARKETPLACE" (TX-20260627-0002)
- **When** User taps the "AMAZON UK MARKETPLACE" row
- **Then** Navigates to transaction-detail with `transactionId=TX-20260627-0002` and `accountId=40051512345678`

Both params are asserted. `accountId` is not redundant — transaction detail needs the owning
account to render its header, and OBIE transaction ids are only unique within an account.

---

## TC-HOME-014 — CreditCard account shows balance-owed styling in the hero card

**State:** content

- **Given** User selects "Platinum Mastercard" (`CreditDebitIndicator=Debit`) via the account switcher
- **When** Hero card renders for Platinum Mastercard
- **Then**
  - Balance text renders in `error` colour
  - Account subtype shown as "CreditCard"
  - Identification shows "xxxx xxxx xxxx 7654"

Same rule as TC-ACCTS-008 on the accounts list, asserted again here because the hero card is a
separate composable — a fix applied to the list card would not reach it.

---

## TC-HOME-015 — Debit amounts render in error colour, credits in primary

**State:** content

- **Given** Home rendered in content state; recent transactions contain at least one debit and one credit
- **When** Recent transactions list renders
- **Then**
  - AMAZON UK, PRET A MANGER, TESCO, TFL rows show amount in `error` colour prefixed "- £"
  - SALARY ACME LTD row shows amount in `primary` colour prefixed "+ £"

Colour and sign are asserted together deliberately — either alone is a single point of failure for
a colour-blind customer or a monochrome screenshot.

---

## TC-HOME-017 — 503 from the sandbox surfaces a recoverable error state

**Priority:** medium · **State:** error

- **Given** HSBC sandbox returns 503 Service Unavailable on `GET /accounts`
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Body shows "Unable to load your account. Please retry."
  - Retry button visible (`error.recoverable = true`)
  - Tapping Retry re-triggers `home_load` **from the beginning**

"From the beginning" matters on this screen more than elsewhere: home fans out into three parallel
AIS calls plus two derivations (`business_logic.kind: composite`), so a partial retry would leave
the hero card fresh and the spending snapshot stale.

---

## TC-HOME-018 — selectedAccountId persists across app restarts via DataStore

**Priority:** medium · **State:** content

- **Given** User previously selected "ISA Saver" (`AccountId=40051589012345`); app is restarted
- **When** Home screen mounts after a cold restart
- **Then**
  - Loading state shown briefly
  - Hero balance card renders ISA Saver, **not** the default first account
  - "ISA Saver" chip is selected in the account switcher strip
  - No prompt or account-selection step required

The pair to TC-HOME-007: that scenario asserts the write, this one asserts the read survives
process death. Neither is meaningful without the other.

---

_Generated by /idea-feature-test-export | 2026-08-03_
