# API — Payments Hub

Feature: `payments` · Schema: 4.0 · Contract: 2.0.0

---

## This screen makes no backend calls

`operations: []` — the payments hub is a pure navigation surface. Its tile list is a compile-time
constant; nothing is fetched before it can render, and nothing can fail. `has_api` is deliberately
absent from this feature's capability declaration (`capabilities: [has_ui, has_flow]`).

### Why — the rationale from `api.yaml#no_api_rationale`

> Pure navigation surface — static tile list known at compile time.

Declaring operations here would be wrong in two ways:

1. It would imply the hub fetches something before it can render. The hub has no loading state and
   no error state by contract — nothing here can fail. Adding an endpoint would immediately require
   adding loading and error states to a screen designed precisely to not need them.

2. It would duplicate contracts that belong exclusively to the seven type features. Each type screen
   owns its own wire contract against a distinct endpoint family. Those contracts are not shared
   resources: they cannot be factored out because the forms that drive them are mutually exclusive
   in their field shapes (see `docs.yaml#seven_tiles_not_one_form`).

This file exists so the sibling set is complete and so a reader looking for the hub's network
behaviour finds an explicit "none" rather than an absent file.

---

## Downstream endpoint map — where each family lives

The hub routes seven tiles to seven features. Each feature owns its own endpoint family under the
HSBC UK OBIE Read/Write v4.0 PISP base URL:

```
https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp
```

| Tile                  | Feature                        | Endpoint family                                                                    |
|-----------------------|--------------------------------|------------------------------------------------------------------------------------|
| Pay someone           | `pay-domestic-single`          | `POST /domestic-payment-consents` → `POST /domestic-payments`                      |
| Pay on a date         | `pay-domestic-scheduled`       | `POST /domestic-scheduled-payment-consents` → `POST /domestic-scheduled-payments`  |
| Standing order        | `pay-domestic-standing-order`  | `POST /domestic-standing-order-consents` → `POST /domestic-standing-orders`        |
| Pay abroad            | `pay-international-single`     | `POST /international-payment-consents` → `POST /international-payments`            |
| Pay abroad on a date  | `pay-international-scheduled`  | `POST /international-scheduled-payment-consents` → `POST /international-scheduled-payments` |
| Overseas standing order | `pay-international-standing-order` | `POST /international-standing-order-consents` → `POST /international-standing-orders` |
| Variable payments     | `pay-vrp-mandate`              | `POST /domestic-vrp-consents` → `POST /domestic-vrps` · `DELETE /domestic-vrp-consents/{id}` · `POST /domestic-vrps/funds-confirmation` |

Two additional screens are shared across all seven rails; the hub does not hold their contracts:

| Screen            | Role                                                              |
|-------------------|-------------------------------------------------------------------|
| `payment-consent` | Authorise return leg — polls the originating family's consent-status GET |
| `payment-status`  | Settlement tracker — reads the originating family's resource-status GET  |

---

## Rail-level constraints relevant to the hub's design

These constraints are the reason the hub exists rather than a parameterised single form. They are
documented here so that a future proposal to add network calls to this screen has the context to
assess whether the trade-off is worth the statelessness cost.

**Only VRP supports revocation via DELETE.** The six non-VRP rails have no DELETE endpoint. A PSU
who wants to cancel a standing order or scheduled payment must do so through HSBC's own channel
(OBL Customer Experience Guidelines — the `amend_notice` component surfaces this at the point the
PSU is thinking about recurring payments).

**Only the two single-payment rails (`pay-domestic-single` and `pay-international-single`) have a
funds-confirmation step.** The four deferred rails have no such endpoint. VRP has a distinct
funds-confirmation verb (`POST /domestic-vrps/funds-confirmation`) rather than the `GET` the singles
use. A hub that exposed this detail would need to know the rail before it can show anything — which
is exactly the problem the hub's statelessness avoids.

**Standing orders and scheduled payments cannot be amended or cancelled through a TPP.** This is an
OBL CX Guideline constraint, not a sandbox limitation. The hub's `amend_notice` component is the
mandated touchpoint: it must appear at the Pay landing tab, not only inside the type screen.

---

## Statelessness invariant (from `docs.yaml`)

> The hub makes NO network call and holds NO state beyond the static seven-item tile list.
> The ViewModel injects nothing and exists only to keep navigation events off the composable.

No future modification should break this invariant without a new feature record. The two obvious
requests that would break it:

- A recent-payees strip would require a `GET /beneficiaries` call and a new loading state.
- A per-tile eligibility badge would require a `GET /accounts` call, making the hub network-bound
  and importing the full auth / consent / eligibility failure surface.

Either feature belongs in a new component with its own feature record.
