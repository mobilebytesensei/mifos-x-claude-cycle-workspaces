# Feature Spec — pay-vrp-mandate

**Feature ID:** pay-vrp-mandate  
**Cluster:** payment-initiation  
**Contract version:** 2.0.0  
**Status:** enriched (score 92)  
**Last updated:** 2026-08-07

---

## Feature Overview

Variable Recurring Payments (VRP) is the seventh and structurally distinct payment rail. Where the other six rails each produce one payment per consent, a VRP consent is created once, authorised once, and then funds as many individual payments as the PSU chooses without any re-authentication — until the PSU revokes it. One authorisation, many payments, no expiry.

This means the feature is not a payment form. It is a **mandate lifecycle manager**: three surfaces in one feature, a persistent local ledger, and a health model that is independent of consent status. It is the only payment type with a DELETE, the only one whose consent never reaches Consumed, and the only one whose resource status is returned in the v3.1 long-name encoding.

**What this rail is not:** there is no international VRP, no scheduled or standing-order analogue, and no forward-dating within a mandate. Payments are single and immediate. Recurrence lives in the PSU tapping Pay now again, not in an instruction the bank holds.

---

## Screens

| Screen ID | Name | Archetype | Entry point |
|---|---|---|---|
| `pay-vrp-mandate` | Variable payments | index_list | Tap "Variable payments" tile on the payments hub |
| `pay-vrp-mandate-create` | New variable payment | form (4 steps) | Tap add in top bar or empty-state CTA |
| `pay-vrp-mandate-detail` | Variable payment | detail_screen | Tap a mandate row, or arrive after consent reaches AUTH |

The payments hub tile opens the **list**, not a form. For every other rail, the common action is creating a payment; for VRP, the common action is paying under an existing mandate. Making the form the landing surface would put the rare action first.

---

## State Model

| State | Triggered by | Visible components |
|---|---|---|
| `Loading` | Screen mount | Skeleton placeholders |
| `Content(mandates)` | Local mandates loaded and status refreshed | `mandate_list`, `mandate_row`, `mandate_health_chip` |
| `Empty` | No local mandate records | `no_mandates` empty state |
| `Creating(step)` | User taps add / empty-state CTA | `create_step_indicator`, step-specific fields |
| `Detail(mandate)` | User taps a mandate row or arrives after AUTH | `mandate_detail_card`, `headroom_list`, health banners |
| `Paying` | User taps Pay now | `payment_amount_field`, `payment_reference_field` |
| `Settling` | POST /domestic-vrps returns 201 | `settling_indicator` (30-second countdown) |
| `Revoking` | User taps Revoke | `revoke_confirm_dialog` |
| `Error(type)` | API error or local validation failure | `error_panel` with type-specific copy |

### ViewModel: VrpMandateViewModel

```
ui_state_type: VrpMandateUiState
actions: LoadMandates · OpenMandate · StartCreate · SelectDebtorAccount ·
         EnterCreditor · EnterMaxIndividualAmount · SelectPeriodType ·
         EnterPeriodLimit · ToggleSecondLimit · ReviewMandate · CreateMandate ·
         StartPaymentUnderMandate · EnterPaymentAmount · EnterPaymentReference ·
         ConfirmFundsAndPay · RecordPaymentInLedger · MarkMandateUnpayable ·
         ConfirmRevoke · Revoke · BackStep
events: NavigateToPaymentConsent · NavigateToPaymentStatus
di: AccountsOverviewRepository · VrpMandateRepository · PaymentInitiationRepository
```

`VrpMandateRepository` is unique to this feature. It owns two local stores no other payment type has: the **mandate roster** (because after DELETE the bank can no longer report that a mandate ever existed) and the **payment spend ledger** (because the API exposes no consumed or remaining amount against any periodic limit).

### Mandate health states

Health is derived from payment outcomes, never from consent status. Three of the four states coexist with `Data.Status == AUTH`.

| Health | Chip label | Role | Icon | Trigger |
|---|---|---|---|---|
| `active` | Active | `primary` (mandate_health_chip) | `autorenew` | Consent AUTH; no recent ExemptionNotApplied |
| `failing` | Payments failing | `tertiary` | `schedule` | Consent AUTH; recent payments carry StatusReason `UK.OBIE.ExemptionNotApplied` |
| `unpayable` | Cannot pay | `error` | `error` | Consent AUTH; local record shows `unpayableAt != null` (every payment failed U021) |
| `revoked` | Cancelled | `onSurfaceVariant` | `block` | Local `revokedAt != null`, or consent GET returns 400 U011 |

**Critical design invariant:** A mandate can be simultaneously past SCA, fully authorised, and structurally incapable of paying — consent 45224 proved this. Funds confirmation returned `"Available"`, yet every payment failed 400 U021. Health must never be read from the consent ladder.

---

## Navigation

```
payments hub
  └─ pay-vrp-mandate (list)
       ├─ [add / empty-state CTA]
       │    └─ pay-vrp-mandate-create (4-step form)
       │         └─ payment-consent (authorise — fires ONCE in mandate lifetime)
       │               └─ pay-vrp-mandate-detail
       └─ [tap mandate row]
             └─ pay-vrp-mandate-detail
                  ├─ [Pay now, health == active]
                  │    └─ payment-status (no re-authorise leg)
                  └─ [Revoke confirmed]
                        └─ pay-vrp-mandate (list, mandate now revoked)
```

**Authorisation asymmetry:** `payment-consent` appears exactly once per mandate — on the create path. The payment path never touches it. An already-authorised VRP consent cannot be re-authorised. There is no re-consent transition, no expiry countdown, and no renewal job: VRP tokens live as long as the consent.

**Out-of-band transitions (no user action):**
- PSU revokes in the HSBC app → detected via event poll (`UK.OBIE.Consent-Authorization-Revoked`) or next consent GET returning 400 U011 → mandate health becomes `revoked`
- PSU deletes payee from their beneficiary list → detected when recent payments carry StatusReason `UK.OBIE.ExemptionNotApplied` → mandate health becomes `failing`

---

## API Endpoints

| # | Method | Path | Auth | Purpose |
|---|---|---|---|---|
| 1 | POST | `/obie/open-banking/v4.0/pisp/domestic-vrp-consents` | client_credentials | Create mandate — runs once |
| 2 | GET | `/obie/open-banking/v4.0/pisp/domestic-vrp-consents/{ConsentId}` | client_credentials | Poll consent status; maps 400 U011 to revoked |
| 3 | DELETE | `/obie/open-banking/v4.0/pisp/domestic-vrp-consents/{ConsentId}` | client_credentials | Revoke — the only DELETE in the payment surface; returns 204 |
| 4 | POST | `/obie/open-banking/v4.0/pisp/domestic-vrp-consents/{ConsentId}/funds-confirmation` | **PSU token** | Check funds before each payment; POST not GET (amount is per-payment); 401 on client_credentials |
| 5 | POST | `/obie/open-banking/v4.0/pisp/domestic-vrps` | **PSU token** | Execute payment under mandate; no re-authentication |
| 6 | GET | `/obie/open-banking/v4.0/pisp/domestic-vrps/{DomesticVRPId}` | client_credentials | Read payment status |

Resource host: `https://secure.sandbox.ob.hsbc.co.uk`  
Authorise host: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`  
Auth: mTLS + `private_key_jwt` (PS256) + OAuth authorization-code, FAPI 1.0 Advanced

---

## Design Tokens

All tokens resolve from `design-tokens.yaml`. No inline hex literals.

| Purpose | Token |
|---|---|
| Primary action, active-tab, mandate active health | `colors.primary` (#266489) |
| Mandate health chip — active state background | `colors.primaryContainer` |
| Mandate health chip — active state foreground | `colors.onPrimaryContainer` |
| Warning / payments-failing health chip | `colors.tertiary` (#64597B) |
| Payments-failing chip background | `colors.tertiaryContainer` |
| Payments-failing chip foreground | `colors.onTertiaryContainer` |
| Error / cannot-pay health chip | `colors.error` (#BA1A1A) |
| Cannot-pay chip background | `colors.errorContainer` |
| Cannot-pay chip foreground | `colors.onErrorContainer` |
| Revoked / cancelled chip | `colors.onSurfaceVariant` (#41474D) |
| Revoked chip background | `colors.surfaceVariant` |
| Card surfaces | `colors.surfaceContainer` |
| Monetary amounts | `typography.mono` (Roboto Mono) |
| Card radius | `rounded.medium` (12dp) |
| Button radius | `rounded.full` (pill) |
| Screen padding | `spacing.screen_padding` (16dp) |
| Screen titles | `typography.headlineSmall` (24sp) |
| List primary text | `typography.bodyLarge` (16sp) |
| List supporting text | `typography.bodyMedium` (14sp) on `colors.onSurfaceVariant` |

**Mandate health chip is a separate component** from `status_chip`. It must never be wired to the consent status ladder. Its icon distinguishes it from payment-disposition chips: `autorenew` (active), `schedule` (failing), `error` (unpayable), `block` (revoked) — never `check_circle`, which belongs to the settled-payment disposition.

---

## Referenced Journeys

**None. No journey in `idea-layer/journeys/` walks any of this feature's three screens.**

All five journeys were checked against their `screen_sequence`: `consumer-authentication`,
`consumer-accounts-payments`, `consumer-cards-financing`, `consumer-insights-utilities`,
`consumer-profile-settings`. Three of them reach the `payments` hub, and each then taps a different
tile — Domestic single, Domestic standing order, International single. None taps Variable payments.

`journeys/INDEX.md` names this **the most valuable of the uncovered features**, and the reasoning
holds against this spec: VRP is the only rail with a lifecycle rather than a transaction — create
once, pay many times with no re-authentication, revoke — and it owns three states no other journey
can reach, all of which coexist with `Data.Status == AUTH`:

| Uncovered state | Why no other journey can exercise it |
|---|---|
| Authorised but silently failing | Payments carry StatusReason `UK.OBIE.ExemptionNotApplied` after the PSU deletes the payee at the bank — health becomes `failing` while consent stays AUTH |
| Revoked out-of-band | PSU revokes in the HSBC app; detected only by event poll or the next consent GET — no in-app action triggers it |
| `400 U011` rendered as "you revoked this" | Must read as a deliberate cancellation from the local record, never as a generic error |

A journey covering this rail would also be the only one to exercise the `unpayable` state — the
consent-45224 case where funds confirmation returns `"Available"` yet every payment fails `U021`,
which is the empirical basis for the design invariant that health is never read from the consent
ladder.

To close the gap: `/idea journey new --cover pay-vrp-mandate`.
