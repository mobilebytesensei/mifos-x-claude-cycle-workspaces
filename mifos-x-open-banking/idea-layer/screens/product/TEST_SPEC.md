# TEST SPEC — Product

| Field      | Value                          |
|------------|--------------------------------|
| Feature    | product                        |
| Source     | `screens/product/tests.yaml`   |
| Scenarios  | 9                              |
| Priorities | critical 3 · normal 6          |
| States     | content 3 · error 3 · empty 2 · loading 1 |
| Module     | `feature/product`              |

---

## Coverage

Contiguous ids; all four declared states covered.

**Priority vocabulary is unique to this screen.** It uses `critical` / `normal`; account-detail
uses `critical/high/medium/low`, consent-detail `high/medium/low`, direct-debits `P0/P1/P2`,
beneficiaries and payment-consent `p0/p1/p2`. Five vocabularies across the corpus. Transcribed as
declared.

---

## The 404-is-not-an-error decision (TC-PROD-006)

Worth stating because it was a three-way contradiction that got resolved rather than papered over.

TC-PROD-006 originally asserted `state: error` on 404. Meanwhile `data-flow.yaml:29-33` mapped
404 → `empty` and cited `api.yaml` as its authority, while `api.yaml` itself said `error`. So the
scenario, the data-flow map, and the API contract disagreed, and the data-flow map was citing an
authority that contradicted it.

Resolved to **`empty`** on 2026-07-30: a bank holding no product record for an account is not a
failure the customer can act on. `api.yaml` was corrected in the same pass, so all three now agree.

TC-PROD-006's closing assertion states the reasoning directly — a `Success` response with no
PCA/BCA block and a 404 are *the same thing to the customer*. Rendering one as an error and the
other as empty would be a distinction that exists only in the transport layer.

---

## TC-PROD-001 — Product terms load and render all sections (tiered credit interest)

**Priority:** critical · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns `OBReadProduct2` for account 40051512345678 with two credit interest tiers
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Product header card shows "HSBC Advance Account" and type label "PCA"
  - Product ID caption rendered
  - **Fees:** Monthly Maximum Charge shows £0.00
  - **Credit Interest:** first tier shows "Up to £1,000 · paid Monthly" with "0.00% AER"
  - **Credit Interest:** second tier shows "Up to £10,000 · paid Monthly" with "0.15% AER"
  - **Overdraft:** Arranged overdraft row shows 39.9% EAR
  - **Overdraft:** Unarranged overdraft row shows 49.9% EAR
  - **Features:** 6 feature rows, each with a `check_circle` icon
  - All section headers and labels render in i18n-resolved text

Two tiers rather than one is the fixture choice that matters — a tiered rate structure collapsed
to a single figure is the classic product-terms bug, and it only shows up with more than one tier.
The AER/EAR distinction is likewise asserted as declared: they are different regulated measures
(credit vs overdraft) and are not interchangeable.

---

## TC-PROD-002 — Loading state while the product endpoint is in flight

**Priority:** critical · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible with accessibility label "Loading product terms"
  - Product sections not rendered
  - Error and empty states not visible

---

## TC-PROD-003 — Error with Retry on 403 ReadProducts permission missing

**Priority:** critical · **State:** error

- **Given** Consent does not include `ReadProducts`; `GET /accounts/{id}/product` returns 403
- **When** Screen mounts
- **Then**
  - Error `empty_state` renders with `error_outline` icon
  - Title "Could not load product terms"
  - Body shows the ViewModel error message: "Consent does not include ReadProducts."
  - Retry button visible with label "Retry"
  - Tapping Retry dispatches `retry_load` → re-triggers `product_load`

Note this screen offers **Retry on 403**, where direct-debits (TC-DD-006) and home (TC-HOME-011)
hide it for the same status. The two treatments are defensible for different reasons — a missing
`ReadProducts` scope is narrower than a revoked consent — but they are inconsistent across the
corpus, and a customer meeting both will not see why one offers a second attempt and the other
does not. Recorded as an observation, not transcribed away.

---

## TC-PROD-004 — Error on 401, access token expired

**Priority:** normal · **State:** error

- **Given** PSU access token has expired; endpoint returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with "Session expired. Please re-authenticate."
  - Retry button visible

---

## TC-PROD-005 — Empty state for an account type with no OBProduct2 entry

**Priority:** normal · **State:** empty

- **Given** Valid PSU access token; account is GlobalMoney type; `OBReadProduct2` `Data` array is empty
- **When** Screen mounts
- **Then**
  - Empty state renders with `info_outline` icon — the **informational** variant, not the error one
  - Title "No product information"
  - Body "No product data is available for this account."
  - **No Retry button** — this is not a retriable error
  - Product sections (Fees, Credit Interest, Overdraft, Features) not rendered

The icon assertion is doing the work. `info_outline` against `error_outline` is the entire visual
difference between "this account has no published terms" and "we could not reach the bank", and
they call for opposite reactions from the customer.

---

## TC-PROD-006 — Empty state on 404, no product record for the AccountId

**Priority:** normal · **State:** empty

- **Given** `AccountId` has no associated `OBProduct2` record; endpoint returns 404
- **When** Screen mounts
- **Then**
  - Empty state renders with the no-product-data message
  - No error icon and no Retry CTA
  - Outcome matches TC-PROD-005 — a Success with no PCA/BCA block and a 404 are the same thing to the customer

---

## TC-PROD-007 — Back navigation returns to account-detail

**Priority:** normal · **State:** content

- **Given** Product terms rendered for account 40051512345678, reached from the account-detail Product chip
- **When** User taps the back arrow in the top app bar
- **Then** Navigates back to account-detail; `accountId` preserved in the back-stack

---

## TC-PROD-008 — BCA account type renders terms from the product.BCA path

**Priority:** normal · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns `OBReadProduct2` for a Business Current Account with `product.BCA` non-null, `product.PCA` null
- **When** Screen mounts with an `accountId` referencing a BCA
- **Then**
  - Product header card shows the BCA `ProductName` and type label "BCA"
  - `ProductType` overline reads "BCA" (dynamic data, `i18n:skip`)
  - Fee, Credit Interest, Overdraft and Features sections render from `product.BCA.*` paths
  - Empty state is **NOT** shown (BCA product data present)
  - Error state is **NOT** shown

The pair to TC-PROD-001, and the reason both exist: `OBReadProduct2` puts personal and business
current account terms under **different top-level keys**, so a reader hardcoded to `product.PCA`
renders a business account as empty. The two negative assertions are what catch that — the screen
would look plausible, just blank.

`i18n:skip` on the overline is correct and worth noting: "BCA" is an OBIE product-type code
returned by the API, not display copy to translate.

---

## TC-PROD-009 — Error state on network failure

**Priority:** normal · **State:** error

- **Given** Device is offline; `GET /accounts/{id}/product` throws `IOException` or similar
- **When** Screen mounts
- **Then**
  - Error `empty_state` renders with `error_outline` icon
  - Title "Could not load product terms"
  - Body shows the localised network error message from the ViewModel
  - Retry button visible with label "Retry"
  - Tapping Retry re-dispatches `product_load`; if the connection is restored, transitions to **content or empty**

"Content or empty" is the right assertion rather than "content" — a successful retry against an
account with no published terms lands in empty, and demanding content would make TC-PROD-005's
account fail this scenario.

---

_Generated by /idea-feature-test-export | 2026-08-03_
