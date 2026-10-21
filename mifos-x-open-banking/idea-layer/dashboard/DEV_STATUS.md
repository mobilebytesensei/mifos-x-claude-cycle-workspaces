# Development Status — mifos-x-open-banking

> Regenerated 2026-08-07 against the live roster. Every row below is derived this run from
> `screens/_list.json` (42 entries, the canonical enumeration) and each feature's own
> `screens/{f}/docs.yaml`. The previous body was a 2026-08-03 snapshot describing a 46-screen
> app that no longer exists.

## Summary

| Metric | Value |
|--------|-------|
| Screens on disk | 42 |
| Screens in `_list.json` | 42 / 42 (roster and disk agree) |
| Features with `docs.yaml` | 42 / 42 |
| Mean quality score | 92.4 (min 83 `about` · max 98 `profile`) |
| Rendered preview state files | 124 across 33 features (9 features have none) |
| Features with a MOCKUP.md | 16 / 42 |
| Features registered in an API group | 30 / 42 |
| API groups | 15 (`server/api_manifest.yaml`) |
| Flows | 2 (app-main, consumer-banking) |
| Journeys | 5 |
| DTOs registered | 69 |
| Bottom-nav tabs | 4 (Home · Accounts · Pay · More — `design-system/app-shell.yaml`) |

**What moved since 2026-08-03.** The roster fell 46 → 42 in two steps. On 2026-08-06 the
seven-type payments rewrite deleted eleven screens (`send-money`, `send-money-amount`,
`send-money-confirm`, `payment-result`, `sca-challenge`, `fx-rates`, `transaction-tags`,
`standing-order-edit`, `standing-order-create`, `change-password`, `forgot-password`) and added
the `payments` hub plus seven per-type rails. On 2026-08-07 `cards` and `card-detail` were
deleted — OBIE has no card resource, so both screens were describing an API surface that does
not exist. The old Summary block counted all thirteen deleted screens and none of the eight
added ones; every number in it was wrong, not just the two card rows corrected by hand.

## Feature Status Table

Every column is DERIVED this run, not carried forward. `Status` and `Quality` are
`docs.yaml#status` and `docs.yaml#quality_score`; `Export` is the presence of
`mockups/{f}/MOCKUP.md`; `Preview` is the count of rendered `screens/{f}/preview/*.html`
state files; `API` is whether the feature appears in `server/api_manifest.yaml`.

The `#` column is `_list.json#display_order`, so ordinals are stable across regenerations and
skip the numbers vacated by deleted screens (16, 17, 20).

| # | Feature | Status | Quality | Export | Preview | API |
|---|---------|--------|---------|--------|---------|-----|
| 1 | splash | approved | 85 | yes | 2 | yes |
| 2 | login | approved | 95 | yes | 5 | yes |
| 3 | home | approved | 95 | yes | 4 | yes |
| 4 | consent-callback | approved | 95 | no | 6 | yes |
| 5 | licences | implemented | 90 | no | 1 | no |
| 6 | privacy-policy | enriched | 92 | no | 1 | no |
| 7 | profile | approved | 98 | yes | 3 | no |
| 8 | settings | approved | 95 | yes | 3 | no |
| 9 | terms-of-service | enriched | 92 | no | 1 | no |
| 10 | user-onboarding | enriched | 95 | no | 1 | no |
| 11 | accounts | approved | 95 | yes | 4 | yes |
| 12 | account-detail | approved | 95 | yes | 4 | yes |
| 13 | transactions | approved | 95 | yes | 4 | yes |
| 14 | transaction-detail | approved | 95 | yes | 4 | yes |
| 15 | beneficiaries | approved | 95 | yes | 4 | yes |
| 18 | standing-orders | approved | 95 | yes | 5 | yes |
| 19 | standing-order-detail | approved | 93 | no | 4 | yes |
| 21 | scheduled-payments | approved | 96 | no | 5 | yes |
| 22 | direct-debits | approved | 95 | yes | 5 | yes |
| 23 | direct-debit-detail | approved | 91 | no | 4 | yes |
| 24 | statements | approved | 97 | no | 4 | yes |
| 25 | statement-detail | approved | 95 | no | 4 | yes |
| 26 | product | approved | 95 | no | 4 | yes |
| 27 | products | enriched | 88 | yes | 4 | no |
| 28 | account-holder | approved | 96 | no | 4 | no |
| 29 | consent-list | approved | 95 | no | 5 | yes |
| 30 | consent-detail | approved | 95 | no | 6 | yes |
| 31 | consent-manager | approved | 92 | yes | 6 | yes |
| 32 | atm-locator | approved | 84 | yes | 4 | yes |
| 33 | branch-locator | enriched | 88 | no | — | no |
| 34 | notifications | approved | 91 | yes | 4 | no |
| 35 | about | enriched | 83 | no | 1 | no |
| 36 | payments | enriched | 86 | no | — | yes |
| 37 | pay-domestic-single | enriched | 94 | no | — | yes |
| 38 | pay-domestic-scheduled | enriched | 91 | no | — | yes |
| 39 | pay-domestic-standing-order | enriched | 88 | no | — | yes |
| 40 | pay-international-single | enriched | 93 | no | — | yes |
| 41 | pay-international-scheduled | enriched | 91 | no | — | yes |
| 42 | pay-international-standing-order | enriched | 89 | no | — | yes |
| 43 | pay-vrp-mandate | enriched | 92 | no | — | yes |
| 44 | payment-consent | enriched | 90 | no | 5 | yes |
| 45 | payment-status | enriched | 91 | no | 3 | no |

**Tallies** — Status: 25 approved · 16 enriched · 1 implemented.
Quality: mean 92.4, all 42 features scored, none below 83.
Export: 16 have a MOCKUP.md, 26 do not. Preview: 33 have rendered states, 9 have none.
API: 30 registered, 12 have no endpoint surface.

### Where the roster is thin

The table no longer splits along the old "two generations" axis — that framing described a
`send-money` family and a `consent-manager`-vs-`consent-list` rivalry, and the payments half of
it was resolved by deletion on 2026-08-06. What replaces it is narrower and easier to act on:

- **The eight new payments screens are specified but unrendered.** `payments` and the seven
  `pay-*` rails are all `enriched`, all API-registered, and all carry zero preview HTML. They
  are the newest features in the roster and the only cluster where the idea-layer is complete
  but nothing has been drawn. `branch-locator` is in the same position for a different reason —
  it was added as an Open Data surface and never rendered.
- **`enriched` is now the second-largest status.** 16 of 42, up from 3. That is a direct
  consequence of the rewrite: eight new screens entered at `enriched` and none has passed
  `/idea-approve` yet. It is expected, not drift, but it means only 25 features are eligible
  for `/implement`.
- **MOCKUP.md coverage fell to 16/42** because the 2026-08-03 export set included six screens
  that have since been deleted. No mockup was lost; the denominator changed.

## Flow Distribution

| Flow | Screens |
|------|---------|
| app-main | splash, login, profile, settings + legal screens |
| consumer-banking | accounts, transactions, statements, standing orders, direct debits, consents, locators |

The third flow, `send-money-payment`, was removed with the screens it described. The seven
payment rails are reached from the `payments` hub rather than from a dedicated flow file.

## This Regeneration (2026-08-07)

| Area | Outcome |
|------|---------|
| Roster | Re-derived from `screens/_list.json` (42). The prior table listed 46 features, of which 13 no longer exist and 8 current ones were missing entirely. |
| Status + Quality | Read per-feature from `screens/{f}/docs.yaml`. `Quality` is a new column; the prior table had no quality signal at all despite every `docs.yaml` carrying one. |
| Summary block | Every metric recomputed. The prior block was stale on all eleven rows — screen count, nav edges, flows, DTOs, API groups and tag counts all predated both deletions. |
| Bottom nav | Recorded as 4 tabs. The fifth "Cards" tab traced to a single wrong line in PROJECT_CONFIG.yaml and is gone; `design-system/app-shell.yaml` is the authority. |
| Preview HTML | Counted, not assumed: 124 files across 33 features. |

## Carry-Forward Issues

| ID | Severity | Issue | Fix |
|----|----------|-------|-----|
| PAY-RENDER | WARN | 8 payments-family screens + `branch-locator` have zero rendered preview states | `/idea-feature-render` on each |
| PAY-APPROVE | WARN | 16 features sit at `enriched`; none of the 8 new payment screens has passed the human gate | `/idea-approve` |
| NAV-STALE-HTML | WARN | Rendered preview HTML across the roster still carried bottom-nav targets for deleted screens; corrected by hand 2026-08-07 and stamped, but the pages were not re-derived | full `/idea-feature-render` sweep |
| SIB-TESTS | WARN | `tests.yaml` absent on a majority of features | `/idea-feature-test-export` |
| SH-1 | WARN | Sibling YAMLs diverge in body shape from the v4.0 schemas | user declined the restructure 2026-08-02 |
| FW-1 | WARN | Defect in shipped `framework-verify-action-contract.sh` | not fixable from this project |
| DST3/DST4 | FAIL | `design-tokens.yaml` uses `color:` not M3 `colors:` schema | `/design-system` |
| V1-TABLES-DIR | FAIL | `server/tables/` missing | `/server init` — may be N/A; this project owns no backend |
| STALE-COUNTS | WARN | `DESIGN_VALIDATION` findings predate both deletions | `/design-validate` |

## Next Steps

- **Render the payments family** — `payments` plus the seven `pay-*` rails plus
  `branch-locator`. Nine features, zero preview states between them; they are the only
  substantial gap left in the roster.
- **Re-render the corrected previews** — the 2026-08-07 nav fixes were hand-applied to what was
  visibly wrong. A full `/idea-feature-render` is still owed so the pages are derived rather
  than patched.
- `/idea-approve` on the payments family once rendered — nothing there can reach `/implement`
  while it sits at `enriched`.
- `/design-validate` — refresh `DESIGN_VALIDATION.yaml` against 42 screens.
- `/implement atm-locator` — the spec is retained and in scope; the source route is still a placeholder.
