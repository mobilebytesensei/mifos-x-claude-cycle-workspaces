# Journeys Index — mifos-x-open-banking

Schema: `core/schemas/journeys/journey.schema.json` (x-contract-version: 1.0.0)
Regenerated: 2026-08-06 by `/idea-sync` — seven-type payments rewrite + OBP eviction.
Flow linkage: run `/idea journey link` to wire `flows[]` bidirectional refs to `idea-layer/flows/*.yaml`.

**This app is consumer-only.** The field-officer persona and its journeys were removed on
2026-08-02; see the "Removed" section below.

---

## Journey Inventory

| id | archetype | # screens | tier | success metric kind |
|----|-----------|-----------|------|---------------------|
| [consumer-authentication](consumer-authentication.yaml) | first-time consumer | 3 | maximum | task_completion |
| [consumer-accounts-payments](consumer-accounts-payments.yaml) | returning consumer | 11 | maximum | task_completion |
| [consumer-cards-financing](consumer-cards-financing.yaml) | returning consumer | 6 | maximum | task_completion |
| [consumer-insights-utilities](consumer-insights-utilities.yaml) | returning consumer | 6 | medium | activation |
| [consumer-profile-settings](consumer-profile-settings.yaml) | returning consumer | 7 | maximum | task_completion |

Total: 5 journeys.

> **`consumer-cards-financing` is no longer about cards** (2026-08-07). Its two opening steps,
> `cards` and `card-detail`, were removed with those screens; it is now
> **"Consumer Recurring Payments Review"**, 8 → 6 steps, entering on `transactions`. The `id` was
> deliberately **not** renamed — `screens/standing-order-detail/flow.yaml` and
> `screens/direct-debit-detail/flow.yaml` both reference it, and renaming would break those refs
> to buy a better label. Read the `name`, not the `id`. See "Removed 2026-08-07" below.

---

## Removed 2026-08-06 (`/idea-sync` — seven-type payments rewrite + OBP eviction)

| Journey | Why |
|---|---|
| `consumer-forgot-password` | **There is no in-app password under FAPI.** The PSU authenticates on HSBC's own site; this app never receives a credential, so there is nothing to recover. The whole journey described a capability the architecture cannot have. |
| `send-money-payment` | Superseded. It walked the linear `send-money → amount → confirm → result` form, which no longer exists. Its coverage now lives inside `consumer-accounts-payments`, extended with the app-to-app authorisation step. |

Edits to surviving journeys, all for the same reason — they walked screens that were deleted:

- **`consumer-accounts-payments`** — the `transaction-tags` and `send-money*` steps were replaced
  by `payments → pay-domestic-single → beneficiaries → payment-consent → payment-status`. The
  **`payment-consent` step is new and load-bearing**: the PSU leaves the app entirely to
  authorise at HSBC, which is the single largest drop-off risk in the flow and did not exist in
  the old journey at all. `has_payments` was also dropped from `capabilities_used` — that
  capability means in-app-purchase / store-billing compliance, not bank payment initiation.
- **`consumer-cards-financing`** — the `standing-order-edit` step was removed (a PISP may not
  amend or cancel a standing order) and replaced with a hop to the payments hub to create a new
  one. The `standing-order-detail` success signal no longer asks for "recent executions": OBIE
  exposes **no per-execution status**, so that signal asked for data that cannot be obtained.
- **`consumer-insights-utilities`** — the `fx-rates → send-money` pair was replaced by
  `payments → pay-international-single`, and the success metric retargeted. OBIE has no FX rate
  endpoint, so "live FX rates visible" was never a producible signal.
- **`consumer-profile-settings`** — the `change-password` step and its failure mode were removed.
  Its failure modes now cover the consent lifecycle instead: revoked-at-the-bank, and the
  90-day reconfirmation lapse (which is the designed default, not a failure).
- **`consumer-authentication`** — preconditions and failure modes rewritten off DirectLogin.
  "Wrong credentials" is gone (the app has no credential fields); added state/nonce mismatch,
  PSU-denies-at-bank, and mTLS handshake failure.

---

## Removed 2026-08-07 (repository owner — cards deleted)

No journey was deleted. One was retargeted:

- **`consumer-cards-financing`** — the opening `cards` → `card-detail` pair was removed with
  those two screens. **OBIE has no card resource**: a card is an `Account` whose
  `Account[].SchemeName` is `UK.OBIE.PAN`, which is why the `Card` and `CardAccountRef` DTOs were
  already deleted on 2026-08-06. The screens were spared then on the argument that filtering the
  accounts list to PAN entries is a legitimate surface; the repository owner has overruled it —
  the feature came from the OLD OBP PLANNING and goes with it.

  The journey survives because its remaining six steps were never card-scoped: `transactions`,
  `standing-orders`, `direct-debits`, `direct-debit-detail`, `standing-order-detail`, `payments`.
  What did not survive is the success metric, which was card-only
  (`cards_opened → card_detail_viewed`); it is retargeted onto the direct-debit drill-down, the
  same list→detail shape on a surface that still exists. The `card data load failure` mode is
  replaced by the **403-with-empty-body on stale SCA**, which is the real load failure here:
  `standing-orders` and `direct-debits` both sit behind the PSD2 RTS Article 10 boundary while
  `transactions` keeps working, and there is no error code to key on.

  `name` and `description` now read "Consumer Recurring Payments Review". The `id` is unchanged
  and is the only thing still saying "cards".

---

## Coverage gaps owed

The seven payment types now have one journey between them (`consumer-accounts-payments`, which
walks domestic single only). Six type screens are journey-uncovered:

`pay-domestic-scheduled` · `pay-domestic-standing-order` · `pay-international-scheduled` ·
`pay-international-standing-order` · `pay-vrp-mandate`

**`pay-vrp-mandate` is the most valuable gap.** It is the only feature with a lifecycle —
create once, pay many times with no re-authentication, revoke — and three states that no other
journey can exercise: the mandate that is *authorised but silently failing*
(`UK.OBIE.ExemptionNotApplied` after the PSU deletes the payee at the bank), the mandate revoked
*out-of-band*, and the `400 U011` that must render as "you revoked this" rather than as an error.

Also still uncovered: `account-holder` · `consent-callback` · `consent-detail` · `consent-list` ·
`product` · `scheduled-payments` · `statement-detail` · `statements` · `user-onboarding`.

---

## Removed 2026-08-02 (`/idea-sync` — consumer-only scope)

The field-officer persona was dropped. Deleted journeys: `fo-authentication-registration`,
`fo-customer-lifecycle`, `fo-operations-management`.

`consumer-insights-utilities` was edited, not deleted: its opening `pfm-dashboard` step and the
`pfm_engagement_rate` metric were removed (PFM was dropped in the same pass and never built).

Earlier removal, recorded 2026-07-28: `pfm-review` — its four screens were spec-only.

---

## RULE-JOURNEY-001 Compliance

| check | status | notes |
|-------|--------|-------|
| J1 — required top-level fields present | PASS | id, version, persona, goal, success_metric, screen_sequence, expected_outcome present in all 5 |
| J2 — id matches filename stem | PASS | all 5 stems match their `id:` value |
| J3 — screen_sequence minItems=1 | PASS | minimum 3; maximum 11 (consumer-accounts-payments) |
| J4 — success_metric.kind ∈ enum | PASS | task_completion (4), activation (1) |
| J5 — tier ∈ enum | PASS | maximum (4), medium (1) |
| J6 — preconditions + failure_modes on high-risk journeys | PASS | present on all maximum-tier journeys |
| J7 — INDEX.md covers all journey ids | PASS | all 5 on-disk journeys listed above |

---

## Known Schema Conflict (report-only, not a RULE-JOURNEY-001 failure)

The schema pattern for `screen_id`, `feature_id`, `recovery_screen` and `fallback_screen_id` is
`^[a-z][a-zA-Z0-9]*$` (camelCase only, no hyphens). This project uses kebab-case screen IDs
matching the `screens/` directory structure. Per the standing directive ("screen_id is a free
string, kebab is fine"), kebab IDs are used throughout. **Action required**: update the
project's local `journey.schema.json` pattern to `^[a-z][a-z0-9-]*$`, or add an
`x-allow-kebab: true` annotation.
