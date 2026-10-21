# DTO Registry — mifos-x-open-banking

Wire and domain types for the HSBC UK Open Banking (OBIE v4.0) surface.

> **Migrated 2026-08-06 by /idea-sync** — the OBP eviction. This registry previously carried 55
> Open Bank Project types with `/obp/vX` API paths, snake_case `bank_id` / `account_id` /
> `view_id` path parameters, and a `counterparty` model OBIE does not have. `INDEX.md` had
> flagged this as an open `PARTIAL` since 2026-08-02 (`D5-USED-BY-FRESH`,
> `D6-ORIGIN-MATCHES-SERVER`). It is now closed.

---

## Deleted — no OBIE equivalent exists

These were not retargeted because there is nothing to retarget them to.

| DTO | Why |
|---|---|
| `SepaTransactionRequest` | OBP SEPA transaction-request. There is no SEPA rail — every domestic Initiation declares `UK.OBIE.FPS`. |
| `Challenge` | OBP SCA challenge object. HSBC performs SCA in its own browser; there is no in-app challenge. |
| `Counterparty`, `TransactionCounterparty`, `DirectDebitCounterparty` | **OBIE has no counterparty concept.** The read-side analogue is `beneficiaries`, and it is read-only. A transaction's other party is `CreditorAccount` / `DebtorAccount` with a `Name`. |
| `IbanCheckResult` | OBP IBAN pre-check endpoint. IBANs are validated locally by mod-97 checksum instead. |
| `MandateDetail`, `CancelMandateResponse` | OBP direct-debit cancellation. **OBIE provides none.** |
| `CreateStandingOrderRequest`, `CreateStandingOrderResponse`, `StandingOrderUpdateRequest`, `StandingOrderStatusResponse` | OBP standing-order write model. Creation is now the PISP `domestic-standing-order` family; **amendment is prohibited outright** by OBL Customer Experience Guidelines. |
| `StandingOrderExecution` | Modelled a per-execution status. **OBIE exposes no per-execution status for any deferred family** — the resource describes the mandate's setup, never the Nth payment. Keeping this type would have implied data that cannot be obtained. |
| `StandingOrder`, `StandingOrderSchedule` | OBP write shapes, superseded by the PISP mandate contract. |
| `Payment` | Backed `obp_get_mandate_detail`. |
| `ChangePasswordRequest/Response`, `PasswordResetRequest/ConfirmRequest/Response` | **There is no in-app password under FAPI.** The PSU authenticates at HSBC. |
| `UserProfile` | OBP user account with a DirectLogin username and `obp_consumer_key`. OBIE's analogue is `account-holder`, read from the `party` resource. |
| `OidcToken` | `obp-oidc` at `apisandbox-oidc.openbankproject.com`. |
| `Tag`, `TransactionTag`, `TagAuthorUser`, `Comment`, `TransactionComment` | OBP v1.2.1 transaction-metadata API. No OBIE counterpart; the `transaction-tags` screen went with them. |
| `CardReplacement` | OBP card operations. OBIE has no cards endpoint at all. |
| `AmountOfMoney` | Self-described as "structurally identical to `MoneyAmount`" — an OBP PFM v6 duplicate. |

**31 deleted.**

### Deleted 2026-08-07 — one more, with the cards screens

| DTO | Why |
|---|---|
| `CardDetail` | An inline entry in `_index.yaml` with no `dtos/CardDetail.yaml` behind it, and `card-detail` was its **only** `used_by` — orphaned the moment that screen was deleted. Its fields (`maskedNumber`, `cardType`, `status`, `expiryDate`, `creditLimit`) are an OBP shape; OBIE returns none of them. `creditLimit` has no OBIE source at all, which is the same absence that made card-detail's Spending Limits sections unbuildable. `Account.yaml#used_by` also lost its `{ feature: cards, api_id: get_accounts_for_cards }` row — never a distinct operation, only a card-framed alias for the accounts list. |

**32 deleted in total.**

## Added — the PISP surface

| DTO | Purpose |
|---|---|
| `ObAccountIdentification` | `SchemeName` + `Identification` + `Name`. Carries the **eligibility matrix**: eligibility is scheme-based, not product-based, and this is where that rule lives. |
| `ObMandateRelatedInformation` | The recurrence block on both standing-order rails. Holds the five-value frequency enum and the `PointInTime` write/read asymmetry. |
| `ObPaymentStatus` | **The single source of truth for status.** Four ladders, two encodings, the `StatusUpdateDateTime` trap, the fail-open rule, and the no-per-execution-status finding. |
| `VrpControlParameters` | The VRP spending envelope. Pro-rating, the GBP-only rule, the `UK.OBIE.SCA` refusal, and `VRPType`. |

**4 added.** Per-family request/response types are owed — the per-type wire contracts currently
live in each screen's `api.yaml`, where the evidence that justifies them sits alongside.

## Retargeted — same concept, OBIE path

`Account`, `AccountRouting`, `Transaction`, `TransactionAccount`, `TransactionDetails`,
`TransactionMetadata`, `DirectDebit`, `StandingOrderDetail`, `Consent`, `ConsentRedirect`,
`Product`, `ProductDetails`, `ProductMeta`, `MoneyAmount`, `Charge`, `Card`, `CardAccountRef`,
`AtmLocation`, `Branch`, `BranchRouting`, `LobbyHours`, `DriveUpHours`, `PostalAddress`,
`GeoLocation`.

Several carry an inline note where the OBIE behaviour is counter-intuitive — the unmasked PAN on
`Transaction`, the absent `StandingOrderId` on `StandingOrderDetail`, the per-family charge
timing on `Charge`, and the fact that `Card` is not a card resource at all.

## Flagged — orphaned, pending a decision

| DTO | Position |
|---|---|
| `FxRate`, `Currency` | **OBIE has no FX rate or currency endpoint.** No observed response on any international family carries a rate. All three international payment screens therefore display no rate and consume neither type. The `fx-rates` screen and its `server/apis/fx-rates.yaml` group file were both deleted 2026-08-06 (see Known open items below); these two DTOs are what outlived them. |

---

## Known open items

| Item | State |
|---|---|
| ~~`used_by[].api_id` back-references~~ | **CLOSED 2026-08-06.** All 26 retargeted once the screen `api.yaml` files were migrated. Zero `obp_*` api_ids remain. Four could not be repointed and were **removed** rather than redirected, because the operation has no OBIE successor: `obp_update_standing_order` (a PISP may not amend a standing order), `obp_transaction_tags_get` (no transaction-metadata resource), `obp_create_sepa_transfer` / `obp_confirm_sepa_transfer` (no SEPA rail). |
| ~~Stale `used_by[].feature` entries~~ | **CLOSED 2026-08-06.** 11 DTOs named deleted features — `send-money`, `send-money-amount`, `standing-order-edit`, `transaction-tags`. All repointed or removed. |
| ~~v3.1 api_paths~~ | **CLOSED 2026-08-06.** **26 DTOs** declared `v3.1` — the 7 shipped PISP types plus 19 AIS types. Every observed call in the corpus is `v4.0`. The generations differ materially: v4.0 re-coded every `UK.OBIE.*` error string to a short code, **and HSBC serves both generations at once** (v4.0 short codes on PISP consents, v3.1 long forms on the AIS consent header check and the VRP status field). A client assuming one encoding per version will be wrong on at least one endpoint — see `ObPaymentStatus.yaml#dual_encoding_trap`. |
| ~~Card / CardAccountRef~~ | **DELETED 2026-08-06.** OBIE has no card resource; a card is an `Account` with `SchemeName == UK.OBIE.PAN`. Both DTOs duplicated `Account.yaml` while describing OBP fields that do not exist. ~~The `cards` / `card-detail` screens survive with `Account` as their response type.~~ **CLOSED 2026-08-07 — the screens were deleted too**, by the repository owner. The 08-06 reprieve rested on the screens being a legitimate filtered projection of the accounts list; that argument is overruled, the feature came from the OLD OBP PLANNING and goes with it. Nothing now consumes `Account` under a card framing. Not to be confused with `CccProduct.yaml` — **commercial credit cards** in the Open Data Product Finder, a different resource on a different host, live and unaffected. |
| ~~ATM / branch **host**~~ | **CLOSED 2026-08-07.** Resolved to `api.hsbc.com` from the HSBC-published `open-atm-locator-swagger.json#host`, reached via develop.hsbc.com — the resolution route the open item prescribed. Open Data v2.2, unauthenticated, live-only, vendor media type `application/prs.openbanking.opendata.v2.2+json`. It is a **different host from the AIS/PIS surface** (`secure.sandbox.ob.hsbc.co.uk`) and takes no mTLS certificate. Endpoints in `server/apis/atm-locator.yaml`; per-endpoint evidence in `screens/atm-locator/api.yaml` and `screens/branch-locator/api.yaml`. |
| **Branch DTOs still on the OBP shape** | ⚠ `AtmLocation` was retargeted to the Open Data v2.2 PascalCase shape, but `Branch`, `BranchRouting`, `LobbyHours` and `DriveUpHours` were **not** — they still carry snake_case fields, a `bank_id`, and an `UNRESOLVED` `api_path`. The host is no longer the blocker; the DTOs are. Retarget them against the published open-branch-locator swagger, then fill in the six `response_dto: unresolved` markers on the branch endpoints in `server/apis/atm-locator.yaml`. Do **not** infer the shape from the ATM sibling — a branch record carries `Availability` and `ServiceAndFacility` members the ATM record has none of. |
| Per-family PISP request/response DTOs | **Still owed.** Only the domestic-single family has typed DTOs. The other six families' contracts currently live in each screen's `api.yaml`, where the evidence sits alongside them. |
| `profile` | OBP-era user profile with no OBIE data source; `account-holder` already covers the party resource. **Deletion candidate** — same class as `fx-rates`, which was deleted 2026-08-06. |

## Charge — a note worth keeping

`Charge.yaml`'s `used_by` deliberately **omits `pay-international-single`**. That is the only
shape in the entire payment surface returning no `Charges` at any stage, through to `ACCC` —
verified across 33 consents and 4 authorised resources. Listing it would imply a fee row that
never populates, and the international *scheduled* and *standing-order* rails DO charge (0.50 at
resource creation, in the **instructed** currency), so "international is free" is a tempting and
wrong generalisation.
