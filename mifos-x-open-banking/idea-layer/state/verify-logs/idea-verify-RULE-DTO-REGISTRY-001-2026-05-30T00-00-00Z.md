# /idea verify --rule RULE-DTO-REGISTRY-001

| Field | Value |
|-------|-------|
| Run at | 2026-05-30T00:00:00Z |
| Project | mifos-x/mifos-x-open-banking |
| Rule | RULE-DTO-REGISTRY-001 v1.0.0 |
| Scope | project-wide (all features) |
| Cache mode | cold |
| Overall | **PASS (with warnings)** |

---

## Summary

| Sub-check | Scope | Status | Count |
|-----------|-------|--------|-------|
| D1-REGISTRY-PRESENT | project | ✓ PASS | 66 DTOs |
| D2-EVERY-CONSUMER-REF-RESOLVES | feature | ✓ PASS | 0 unresolved refs (40 features) |
| D3-NO-DUPLICATE-NAMES | project | ✓ PASS | 0 duplicates |
| D4-NO-SHADOW-OF-SHARED | project | ✓ PASS | 0 shadows |
| D5-USED-BY-FRESH | feature | ⚠ WARN | 43 DTOs with empty used_by[] |
| D6-ORIGIN-MATCHES-SERVER | feature | ✓ PASS | all origin: project (REST) |
| D7-REPLACED-BY-RESOLVES | feature | — SKIP | no replaced_by declared |

**Blocking errors: 0.** Non-blocking: D5 (43 DTO_USED_BY_DRIFT warns).

---

## D1 — Registry Present

```
idea-layer/dtos/: 66 files
has_api features: 40 (all screens with api.yaml)
Result: PASS
```

---

## D2 — Every Consumer Ref Resolves

Checked 40 features × api.yaml. Scanned `type: X`, `type: List<X>`, `dto: X` locations.

All PascalCase DTO refs resolve to `idea-layer/dtos/{Name}.yaml` or `templates/shared/common-dtos.yaml`.

**No D2 violations. PASS.**

---

## D3 — No Duplicate Names

```
66 registry entries scanned. 0 duplicate name: declarations found.
Result: PASS
```

---

## D4 — No Shadow of Shared

```
Shared baselines: ErrorEnvelope, PaginationCursor, PaginatedEnvelope, AuthSession
Project registry intersection: (none)
Result: PASS
```

---

## D5 — used_by[] Freshness (WARN — non-blocking)

All 66 project DTOs have `used_by: []`. Actual consumer map (from api.yaml refs) shows 43 DTOs are
actively referenced but have no back-refs recorded.

| DTO | Referenced by |
|-----|--------------|
| Account | consumer-home, customer-detail, send-money |
| AccountApplication | fo-dashboard |
| AccountInfo | pfm-dashboard |
| AccountRouting | account-detail, accounts, customer-detail, home, transaction-detail |
| AmountOfMoney | pfm-dashboard |
| BranchRouting | atm-locator |
| Card | cards |
| CardReplacement | card-detail |
| Challenge | send-money, send-money-confirm |
| Charge | send-money, send-money-confirm |
| Comment | transaction-detail |
| Consent | consent-manager |
| ConsentRedirect | consent-manager |
| Counterparty | beneficiaries, send-money, standing-orders |
| CreditRating | customer-detail |
| Customer | customer-search, fo-dashboard |
| CustomerAccountLink | customer-detail |
| CustomerMessage | customer-messages |
| DirectDebit | direct-debits |
| DirectDebitCounterparty | direct-debits |
| DriveUpHours | atm-locator |
| FaceImage | customer-detail |
| GeoLocation | atm-locator |
| LobbyHours | atm-locator |
| MoneyAmount | customer-detail, fo-dashboard, send-money |
| Payment | direct-debit-detail |
| PersonalDataField | pfm-dashboard |
| PostalAddress | atm-locator |
| Product | products |
| ProductDetails | products |
| ProductMeta | products |
| SignalChannel | notifications |
| StandingOrder | standing-orders |
| StandingOrderDetail | standing-order-detail, standing-order-edit |
| StandingOrderExecution | standing-order-detail |
| StandingOrderSchedule | standing-orders |
| StandingOrderStatusResponse | standing-order-detail |
| StandingOrderUpdateRequest | standing-order-edit |
| Tag | transaction-detail |
| TagAuthorUser | transaction-tags |
| Transaction | consumer-home, pfm-dashboard |
| TransactionDetails | pfm-dashboard |
| TransactionTag | transaction-tags |

Severity: WARN (non-blocking). Error code: `DTO_USED_BY_DRIFT`
Fix: `/idea generate-dtos --refresh-back-refs`

---

## D6 — Origin Matches Server

```
All 66 DTOs: source.origin = project (REST api_path)
No DTOs declare origin: rpc or origin: table
Result: PASS
```

---

## D7 — Replaced-By Resolves

```
0 DTOs declare replaced_by:
Result: SKIP
```

---

## Remediation

### D5 (warn — non-blocking, auto-fix available)

```bash
/idea generate-dtos --refresh-back-refs
```

Populates `used_by[]` back-refs for all 43 DTOs from authoritative api.yaml consumer refs.
