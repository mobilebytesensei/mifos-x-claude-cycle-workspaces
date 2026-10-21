# mifos-x-open-banking — Requirements

Functional requirements mirror `idea-layer/idea-plan.yaml` §requirements, which is the approved
source. Each FR is the coverage key the idea-layer FR-coverage check reads.

> **Regenerated 2026-08-06.** This file had drifted onto a completely different numbering scheme
> from the plan it claims to mirror — its FR-001 was "authenticates via OBP DirectLogin", while
> the plan's FR-001 is Dynamic Client Registration. It also carried requirements for an
> authentication model this app cannot have (password reset, password change, an in-app SCA
> code) and a payment model it does not use (payment rails, a live funds check before
> continuing). The IDs below now match the plan exactly.

---

## Onboarding & Consent

| ID | Description |
|---|---|
| FR-001 | Perform Dynamic Client Registration once per brand using the signed SSA to obtain client credentials. |
| FR-002 | Run the FAPI consent journey: client_credentials token → create account-access-consent → app-to-app authorize (auth code + PKCE + signed request object) → token exchange. |
| FR-008 | Provide a consent dashboard: active consents, granted permissions, expiry, revoke, and 90-day reconfirmation. |

> **There is no authentication requirement beyond FR-002.** The PSU authenticates at HSBC; this
> app never receives a credential. The old FR-001/002/003 (DirectLogin, password reset, password
> change) described an OBP model and were withdrawn with the `forgot-password` and
> `change-password` screens on 2026-08-06.

## Account Information (AISP)

| ID | Description |
|---|---|
| FR-003 | List authorised accounts and show account detail. |
| FR-004 | Show balances per account. |
| FR-005 | Show transactions with date and credit/debit filtering, plus transaction detail. |
| FR-006 | Show beneficiaries, standing orders, direct debits and scheduled payments — **read-only**. |
| FR-007 | Show statements (list + detail), account product information, and party (account holder) details. |
| FR-011 | Client-side transaction categorization. **Scoped down** — the per-transaction category tag only; the PFM dashboard, budgets and drill-down surfaces are out of scope. |

## Payment Initiation (PISP)

| ID | Description |
|---|---|
| FR-012 | Initiate a consumer payment on **any of the seven** HSBC UK Personal payment types, gathering the debtor, creditor, amount and whatever timing dimension that type carries. |
| FR-012a | Present the seven types as a grid of square tiles on a Payments hub, each opening that type's own screen. |
| FR-013 | Complete the PISP app-to-app authorisation round trip on `scope=payments`: validate state and nonce, exchange the code, and poll the originating family's consent to `AUTH`. |
| FR-014 | Track a submitted payment to settlement, mapping OBIE status onto an in-progress / terminal-success / terminal-failure disposition. |

## Payment correctness — the rules the research established

Every requirement below is an **observed** sandbox result. Where HSBC's Implementation Guide and
the observation disagree, the observation is what is encoded, and the divergence is named in
`idea-plan.yaml`.

| ID | Description |
|---|---|
| FR-015 | Restrict every payment to a **consumer** payment context — `TransferToThirdParty` or `TransferToSelf`. The merchant contexts and the merchant `Risk` fields must never be sent, on any of the seven types. |
| FR-016 | Sign every PISP write with a detached JWS (`PS256`, `b64:false` + crit claims). Omission returns `400 U019`. |
| FR-017 | Attach an `x-idempotency-key` (max 40 chars) to every PISP write, generated once per staged payment and reused across the consent stage, the submit, and every retry. |
| FR-018 | Offer only **eligible** debtor accounts per type. Eligibility is enforced by the account **scheme**, not the product: `UK.OBIE.SortCodeAccountNumber` is payable, `UK.OBIE.PAN` is not, and Global Money may not be TPP-named except on the international same-account conversion. |
| FR-019 | Apply the correct **per-rail field contract**. Domestic standing orders send `FirstPaymentAmount`; international standing orders send `InstructedAmount` — each rail refuses the other's field with `U005`. International shapes must send `CurrencyOfTransfer` and `ChargeBearer` and must never send `RemittanceInformation`. |
| FR-020 | Constrain recurrence and dates to the observed limits: exactly five frequency values (`WEEK`, `FRTN`, `MNTH`, `QURT`, `YEAR`); a scheduled date strictly after today and no more than 365 days ahead; a standing order's final date after the first and within 12 months. |
| FR-021 | Track **both** the consent-status GET and the resource-status GET on all seven families, mapping the four observed status ladders. Accept both the v4.0 short codes and the v3.1 long forms. Never key on `StatusUpdateDateTime`. Fail open to in-progress on an unrecognised status. Never claim a mandate has *paid* — OBIE exposes no per-execution status. |

## Variable Recurring Payments

| ID | Description |
|---|---|
| FR-022 | Create a VRP mandate **once** and reuse it. The consent carries `ControlParameters` (GBP only), requires `UK.OBIE.SortCodeAccountNumber` on both sides, and accepts only `UK.OBIE.SCANotRequired`. Each payment does a `POST` funds-confirmation on the PSU token, then `POST /domestic-vrps` — with no re-authentication. |
| FR-023 | Revoke a VRP mandate via `DELETE`, and treat the resulting `400 U011` on any later consent GET as *"you revoked this"* rather than an error. The app persists its own revoked record because the API can no longer report one. |
| FR-024 | Subscribe to and poll OBIE events for `UK.OBIE.Consent-Authorization-Revoked` so an out-of-band revocation surfaces, and detect the trusted-beneficiary failure mode where the consent stays `Authorised` while payments silently fail with `UK.OBIE.ExemptionNotApplied`. |

---

## Withdrawn

| ID | Was | Withdrawn |
|---|---|---|
| FR-009 | Display multi-currency accounts (Global Money / Global Wallet) | 2026-07-30 — orphaned. Global accounts render in the accounts list; there is no dedicated surface and `AccountFilter` deliberately offers no Global chip, because a Global Money wallet reports `CACC` and is indistinguishable from a current account. |
| FR-010 | ATM locator via HSBC Open Data | 2026-07-30 as a requirement, **not** as behaviour. Back in scope 2026-08-02 as planned work; the spec, exports and DTOs are retained. |
| — | Password reset / password change / in-app SCA code | 2026-08-06 — impossible under FAPI. The PSU authenticates at HSBC and there is no in-app password or challenge step. |
| — | Payment rail selection, pre-submit live funds check on every payment | 2026-08-06 — OBP-era. Every domestic Initiation declares `UK.OBIE.FPS`; there is no rail to choose. Funds-confirmation exists on only three of the seven families and runs after authorisation, not before continuing. |
| — | Add / edit / delete saved recipients | 2026-08-06 — OBIE `beneficiaries` is read-only; there is no write side. |
| — | Cancel a direct debit; amend or cancel a standing order | 2026-08-06 — **regulatory, not technical.** OBIE provides no direct-debit cancellation, and OBL's Customer Experience Guidelines make it a mandatory obligation to redirect the PSU to their bank for standing-order and scheduled-payment changes. |
| — | Freeze / unfreeze a card | 2026-08-06 — no OBIE endpoint. The card appears only as an account. |
| FR-024 (old) | Spending insights, budget progress, category breakdowns | 2026-08-02 with the PFM screens. |
| — | Tag and categorize transactions | 2026-08-06 — the `transaction-tags` screen used an OBP v1.2.1 metadata API with no OBIE counterpart. The client-side category tag under FR-011 survives. |
