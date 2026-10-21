# E2E Remediation Plan — mifos-x-open-banking

Derived from `/idea-verify-e2e` on **2026-08-03T07:58Z** (mean health **54**, range 20–92;
1 feature ≥ 90, 19 at 50–89, 26 below 50).

Run the phases **in order** — each phase depends on the artifacts the previous one writes.
Within a phase, the numbered commands are also ordered.

Checkpoint commands (`/idea-verify-e2e`) are cheap and worth running between phases so you
can see the mean move and catch a phase that did not land.

**Before anything:** confirm the session is bound to this project.

```
/context-start mifos-x/mifos-x-open-banking
```

---

## Phase 0 — State hygiene + schema normalization

The 23 stale features are at `contract_version: 1.1.0`; 18 `ui.yaml` declare no
`schema_version` at all and 3 sit at `3.1`. Everything downstream reads the schema, so this
goes first.

```
1.  /state-repair
2.  /idea-migrate-schema                      # dry-run, review the per-feature transform list
3.  /idea-migrate-schema --confirm            # apply
4.  /idea-migrate-schema --verbose            # confirm 46/46 land at 4.0 + sibling: ui
```

**Closes:** N-4 (21 of 46 screens not in v4.0 sibling form) · Schema column (5 pts × 21 features).

---

## Phase 1 — Roster sync (the single largest lever)

23 features never received the 2026-08-02 source-truth pass. None declares `flow_ref`,
none carries `test_tag`, none is in `TRAINING_MASTER.yaml`. One sync pass closes all three.

The 23: `about` `atm-locator` `card-detail` `cards` `change-password` `consent-manager`
`direct-debit-detail` `forgot-password` `fx-rates` `notifications` `payment-result`
`privacy-policy` `products` `profile` `sca-challenge` `send-money-amount`
`send-money-confirm` `splash` `standing-order-create` `standing-order-detail`
`standing-order-edit` `terms-of-service` `transaction-tags`

```
5.  /idea-sync                                # enrich → cascade → docset roll-up; regenerates TRAINING_MASTER
6.  /idea-feature-enrich-loop --auto          # bulk-enrich whatever sync left pending
7.  /idea-heal                                # drain any coherence gaps sync surfaced
8.  /idea-verify-e2e                          # CHECKPOINT — expect the mean to move ~54 → ~68
```

**Closes:** flow_ref (5 pts × 23) · training (5 pts × 23) · test_tag binding, which unblocks
full drift credit later · `TRAINING_MASTER.yaml roster_size: 23` → 46.

---

## Phase 2 — Missing exports (18-pt roundtrip check, 16 features)

No `exports/` dir at all: `account-holder` `consent-callback` `consent-detail`
`consent-list` `licences` `payment-consent` `payment-result` `payment-status` `product`
`sca-challenge` `scheduled-payments` `send-money-amount` `standing-order-create`
`statement-detail` `statements` `user-onboarding`

8 of these have **shipped source modules** — the spec artifacts are behind the code.

```
9.  /idea-feature-export --all --triage       # groups by readiness, exports only what is ready
10. /idea-feature-export account-holder
11. /idea-feature-export consent-callback
12. /idea-feature-export consent-detail
13. /idea-feature-export consent-list
14. /idea-feature-export product
15. /idea-feature-export statements
16. /idea-feature-export statement-detail
17. /idea-feature-export scheduled-payments
18. /idea-feature-export licences
19. /idea-feature-export user-onboarding
20. /idea-feature-export send-money-amount
21. /idea-feature-export standing-order-create
22. /idea-feature-export sca-challenge
23. /idea-feature-export payment-result
24. /idea-feature-export payment-consent
25. /idea-feature-export payment-status
```

> `/idea export …` is the same command if you prefer the short alias.
> Steps 10–25 are only needed for whatever step 9's triage reports as blocked.

Also fix the 8 features whose exports exist but carry no `tests/` subdir
(`about` `change-password` `direct-debit-detail` `forgot-password` `privacy-policy`
`standing-order-detail` `standing-order-edit` `terms-of-service`):

```
26. /idea-feature-test-export --all
```

---

## Phase 3 — Renders (15-pt check, 11 missing + 3 partial)

No `preview/` at all: `account-holder` `consent-callback` `consent-detail` `consent-list`
`licences` `payment-consent` `payment-status` `product` `scheduled-payments`
`statement-detail` `statements`

Partial: `payment-result` 1/4 states · `sca-challenge` 2/4 · `standing-order-create` 3/4

```
27. /idea-render-mockup --status              # matrix first — see missing/stale/failed classes
28. /idea-render-mockup --filter missing
29. /idea-feature-render payment-result
30. /idea-feature-render sca-challenge
31. /idea-feature-render standing-order-create
32. /idea-feature-render --recompose-shared   # re-apply current chrome partials across all previews
33. /idea-feature-validate --strict           # RV-001..028 per-file
34. /idea-verify-e2e                          # CHECKPOINT — expect ~68 → ~82
```

**Known ceiling:** the render check caps at **11/15** for every feature until
`V1-RENDER-CACHE-FRESH` becomes measurable. `.render-cache.json` is keyed `stitch.{state}`
— it is the stitch-prompt build cache, not a preview-render ledger. **This is a framework
fix, not a project fix**, and no command in this file will move it. Track it separately.

---

## Phase 4 — Stitch (8-pt check, 33 uncovered + 6 unclean)

Only 13 of 46 carry a `STITCH_STATUS.yaml` entry. Of those, `accounts` `forgot-password`
`home` `direct-debits` are `failed` and `cards` `change-password` are `partial`. The other
33 have `prompts/` built but were never run.

```
35. /idea-feature-stitch-preflight            # env + .stitch/ infra + design-system id check
36. /idea-feature-stitch-reconcile            # reconcile STITCH_STATUS against what is on disk
37. /idea-feature-stitch accounts
38. /idea-feature-stitch home
39. /idea-feature-stitch direct-debits
40. /idea-feature-stitch forgot-password
41. /idea-feature-stitch cards
42. /idea-feature-stitch change-password
43. /idea-feature-stitch-loop                 # the remaining 33; --resume if it stops midway
44. /idea-feature-stitch-verify
45. /idea-feature-stitch-ledger               # confirm 46/46 have an entry
```

> The 2026-08-02 all-features run failed `consent-manager` (6 states) on `STN gate failure`.
> Expect step 43 to surface it again — fix the gate input, do not force past it.

---

## Phase 5 — Design conformance (3-pt DS check + Layer 4.5)

Three criticals are open in `state/DESIGN_VALIDATION.yaml`. **R-1 is corpus-wide**, which is
why no feature currently scores full DS.

- **D-2** — 167 of 262 `on_click` blocks declare no `action_contract` (20 screens).
  Worst: `consent-manager` 28, `notifications` 24, `transaction-tags` 17, `card-detail` 13.
- **D-4** — 15 declared states render zero components.
- **R-1** — 81 `text` sites use `value` where the registry requires `content`;
  `list_item` satisfies the required `headline` slot at 5 of 39.

```
46. /design-validate                          # re-measure, get the current site list
47. /rule-check RULE-IDEA-ACTION-CONTRACT-001 # D-2: the action_contract authoring pass
48. /idea-feature-enrich consent-manager
49. /idea-feature-enrich notifications
50. /idea-feature-enrich transaction-tags
51. /idea-feature-enrich card-detail
52. /design-validate                          # confirm D-2 site count falls
```

R-1 (`value` → `content`, `list_item.headline`) is a mechanical corpus rewrite across
`screens/*/ui.yaml`. It has **no shipped command** — it needs a Claude editing pass under
RULE-CI-001 (Read/Edit only, no scripts on idea-layer). Its framework half is tracked as FW-3.

---

## Phase 6 — Drift closure (18-pt check)

Three distinct problems:

**(a) `licences` + `user-onboarding`** — contract 2.0.0 with `flow_ref` + `tests.yaml`, but
no source module *and* no `spec_ahead_of_source` declaration, so drift scores 0 rather than
N/A. Either declare the gap or build the module. Pick one:

```
53a. # declare: add docs.yaml#spec_ahead_of_source to both (Edit, per RULE-CI-001)
53b. /idea-approve licences && /kmp-implement licences
53c. /idea-approve user-onboarding && /kmp-implement user-onboarding
```

**(b) `scheduled-payments`** — the `unsupported` state declared in `ui.yaml` is absent in
source (`CAPABILITY_GAPS` resolution_log step 3, OPEN since the prior run).

```
54. /kmp-implement scheduled-payments
```

**(c) The 3 PISP features** (`send-money` `payment-consent` `payment-status`) — correctly
N/A today because `spec_ahead_of_source` declares the module absence as queued work. Build
them only when the PISP epic is scheduled; until then they are honestly scored.

```
55. /idea-verify-source-drift --all
56. /idea-verify-source-drift --fix           # D6 test stubs + D7 hash re-stamp only
```

---

## Phase 7 — Matrix + approval refresh

`IDEA_MATRIX.yaml` is stale — 26 rows against 46 screens, and it lists none of
`account-holder` `consent-list` `consent-detail` `consent-callback` `product` `statements`
`statement-detail` `scheduled-payments` `licences` `user-onboarding`, **all of which have
shipped source modules**.

```
57. /idea-matrix
58. /idea-approve --dry-run --all-ready       # review the predicate result per feature
59. /idea-approve --all-ready
60. /idea-matrix                              # confirm 46 rows
```

---

## Phase 8 — Final verification

```
61. /idea-verify-e2e                          # full grid
62. /idea-verify-e2e --min 50                 # must exit 0 (26 features fail this today)
63. /idea-verify-e2e --min 75                 # the real target once Phases 0–6 land
64. /project-verify
```

---

## Expected trajectory

| After phase | Mean | What moved |
|---|---:|---|
| baseline | 54 | — |
| 0 (schema) | ~57 | Schema 5 pts × 21 |
| 1 (roster sync) | ~68 | flow_ref + training + test_tag across 23 |
| 2 (exports) | ~74 | roundtrip 18 pts × 16 |
| 3 (renders) | ~82 | render 15 pts × 11, partial × 3 |
| 4 (stitch) | ~87 | stitch 8 pts × 33 |
| 5 (design) | ~88 | DS 1–2 pts × 46 |
| 6 (drift) | ~90 | drift 18 pts × 2–3 |

**Hard ceiling: ~92 per feature** until `V1-RENDER-CACHE-FRESH` becomes measurable
framework-side. Do not read a sub-95 mean as project debt after Phase 6 — 3 of the 15
render points are structurally unscoreable today.

---

## Not in this plan

- The framework-side render-cache ledger (blocks 3 render pts for every feature, forever,
  until fixed). Needs a framework change — file it against the render pipeline, not here.
- `FW-8` / `FW-9` in `DESIGN_VALIDATION.yaml` (`blocking-for-automation`): the runtime names
  two token files that exist nowhere in the framework, and the shipped validator cannot
  consume this corpus. Both are framework defects surfaced by this project.
