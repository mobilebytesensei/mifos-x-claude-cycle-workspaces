# API — Product Terms

Client contract for `product`. This project owns no backend: this is a Ktorfit contract against the
HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `ProductRepository`.

---

## product

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/product` |
| Permission | **ReadProducts** |
| Domain type | `OBProduct2?` — **nullable** |

Returns the product associated with the account — a Personal Current Account (PCA) or Business
Current Account (BCA) — including fee tiers, credit-interest bands and overdraft terms.

`AccountId` arrives via `SavedStateHandle` from the navigation argument.

### The response is tiered, not flat

Credit interest and overdraft charges are **banded**: a band contains tiers, and each tier carries
its own threshold and rate. That is why the SPEC renders nested lists rather than key/value rows —
collapsing a band to one number would state a rate the customer does not actually pay at their
balance.

`ReadProducts` is its own consent scope. A consent that reads accounts and balances does not
necessarily read products, which is what `ConsentScopeError` distinguishes.

---

## Errors

| Type                   | Cause                                    | Recoverable by retry |
|------------------------|------------------------------------------|----------------------|
| `TokenExpiredError`    | PSU token expired                        | after re-auth        |
| `ConsentScopeError`    | Consent lacks `ReadProducts`             | **no**               |
| `ProductNotFoundError` | No product associated with the account   | **no** — renders `empty` |
| `NetworkError`         | Offline / transport                      | yes                  |

`ProductNotFoundError` is the reason `product` is nullable and `empty` exists as a state. A
successful call can legitimately return no product — for an account type the bank does not publish
terms for — and that is not a failure to retry.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/product/api.yaml. -->
