<!--
  generated_from_feature: loan-apply
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 85)
-->

# Loan Apply — Feature Spec

## Overview

Loan application form filled by a chairperson or treasurer on behalf of a group member.
Validates that the requested amount does not exceed `memberSavingsBalance × loanMultiplier`
(from `dt_group_config`) and runs a client-side corpus buffer check that warns if the
disbursement would push the group fund below a 10% buffer. Caches members, products, and
config offline via SQLDelight through Store5, then POSTs a `LoanApplicationRequest` to
Fineract `m_loan` (status "submitted and pending approval") via `LoanRepository`.
`cmp-network-monitor` blocks offline submits and serves cached data for eligibility recompute.
On success, navigates to `meeting-conduct` for a democratic vote.

**Route:** `/groups/{groupId}/loans/apply` · **Entry:** `loan-list` (Apply for Loan FAB)
**Nav params:** `groupId: Long (required)`

**Acceptance Criteria:**

- AC1: On mount, load members, loan products, group corpus, and group config in parallel
       before showing the form (Loading → Content).
- AC2: On member selection, fetch member savings + loan template via Store5; compute
       `eligibleAmount = memberSavingsBalance × loanMultiplier`; show `eligibility_banner`.
- AC3: `OnAmountChanged` is a pure transform — validates `requestedAmount <= eligibleAmount`
       (sets `amountError`) and runs corpus check `corpusBalance - requestedAmount >=
       corpusBalance × 0.10` (sets `corpusWarning`). No I/O.
- AC4: Submit enabled only when `selectedMember != null && requestedAmount.isNotBlank() &&
       amountError == null && selectedProduct != null`.
- AC5: `OnSubmit` builds a `LoanApplicationRequest` and POSTs to Fineract `/loans`; on success
       emit `NavigateToMeetingConduct(loanId)`.
- AC6: Offline submit is blocked by `cmp-network-monitor` → `LoanApplyError.Network` +
       `ShowSnackbar(error_network)`; no `post_loan` call.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan-apply-screen | `LoanApplyScreen` | Form, vertical scroll | Multi-field application form with real-time eligibility and corpus checks |

## State Model

### LoanApplyViewModel

**State — `LoanApplyState`**

| Field | Type | Default | Description |
|---|---|---|---|
| selectedMember | GroupMember? | `null` | Member the loan is applied for |
| requestedAmount | String | `""` | Raw amount input (KES) |
| durationWeeks | Int | `12` | Loan duration in weeks |
| purpose | LoanPurpose | `LoanPurpose.BUSINESS` | Selected loan purpose |
| selectedProduct | LoanProduct? | `null` | Chosen Fineract loan product |
| members | List<GroupMember> | `emptyList()` | Group members for selector |
| loanProducts | List<LoanProduct> | `emptyList()` | Available loan products |
| memberSavingsBalance | Double | `0.0` | Selected member's savings balance |
| loanMultiplier | Double | `3.0` | Eligibility multiplier from group config |
| eligibleAmount | Double | `0.0` | `savings × loanMultiplier` ceiling |
| corpusBalance | Double | `0.0` | Current group corpus balance |
| corpusWarning | Boolean | `false` | True when disbursement breaches 10% buffer |
| isSubmitting | Boolean | `false` | In-flight submission |
| isLoadingTemplate | Boolean | `false` | Loan template fetch in flight |
| amountError | String? | `null` | Inline amount validation error |
| error | LoanApplyError? | `null` | Top-level error |
| submitSuccess | Boolean | `false` | Navigate trigger |

**Screen States — `LoanApplyScreenState`**: `Loading`, `Content`, `Submitting`, `Error`, `Success`

| State | Components |
|---|---|
| `Loading` | top_bar (fetch members/products/corpus/config in parallel) |
| `Content` | top_bar, member_selector, eligibility_banner, amount_input, corpus_warning_banner, duration_dropdown, purpose_dropdown, product_dropdown, submit_button |
| `Submitting` | same as Content (inputs disabled, submit_button shows loading) |
| `Error` | top_bar, error_state |

**Errors — `LoanApplyError`**

| Type | Retry | Message Key | Notes |
|---|---|---|---|
| Network | yes | error_network | Offline — application queued/blocked |
| Server | yes | error_server | 5xx |
| AmountExceedsEligibility | no | error_amount_exceeds | Amount > ceiling |
| CorpusInsufficient | no | error_corpus | Corpus too low (422) |
| Auth | no | error_auth | Session expired → redirect login |

**Actions — `LoanApplyAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnMemberSelected` | member: GroupMember | Select from member dropdown | call_api — get_member_savings + get_loan_template via Store5 |
| `OnAmountChanged` | amount: String | Type loan amount | transform_state — validate ceiling + corpus buffer |
| `OnDurationChanged` | weeks: Int | Select duration | transform_state — writes durationWeeks |
| `OnPurposeChanged` | purpose: LoanPurpose | Select purpose | transform_state — stores LoanPurpose enum |
| `OnProductSelected` | product: LoanProduct | Select loan product | call_api — get_loan_template via Store5 |
| `OnSubmit` | — | Tap Submit button | call_api — post_loan (m_loan create) |
| `OnBack` | — | Tap back / nav icon | navigate — pop to loan-list, no persist |

**Events — `LoanApplyEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToMeetingConduct` | loanId: Long | Submit success |
| `NavigateBack` | — | `OnBack` |
| `ShowSnackbar` | message: String | Errors |

**DI Dependencies**

- `LoanRepository` — submitLoanApplication, getLoanProducts, getLoanTemplate
- `MemberRepository` — getGroupMembers, getMemberSavingsBalance
- `GroupRepository` — getGroupCorpus, getGroupConfig
- `NetworkMonitor` (cmp-network-monitor)
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Submit success | `meeting-conduct` | `loanId` |
| `OnBack` from form | `loan-list` | — |

**navigates_to:** `meeting-conduct`, `loan-list`

## API Endpoints (7)

| ID | Method | Endpoint | Cache | Writable |
|---|---|---|---|---|
| `get_group_members` | GET | `/groups/{groupId}?associations=clientMembers` | 3600 s cache-first | no |
| `get_loan_products` | GET | `/loanproducts` | 3600 s cache-first | no |
| `get_loan_template` | GET | `/loans/template` | — | no |
| `get_member_savings` | GET | `/clients/{clientId}/accounts` | — | no |
| `get_group_corpus` | GET | `/datatables/dt_group_corpus/{groupId}` | — | no |
| `get_group_config` | GET | `/datatables/dt_group_config/{groupId}` | — | no |
| `post_loan` | POST | `/loans` | — | yes |

See `exports/loan-apply/API.md` for full contracts.

## Flow Logic

| Trigger | Steps |
|---|---|
| `on_load` | load_members (get_group_members) · load_loan_products (get_loan_products) · load_corpus (get_group_corpus) · load_group_config (get_group_config) |
| `on_member_selected` | fetch_member_savings (get_member_savings) · compute_eligible_amount (`memberSavingsBalance × loanMultiplier`) · load_loan_template (get_loan_template) |
| `on_amount_changed` | validate_amount (`requestedAmount <= eligibleAmount`, on_fail set_amount_error) · check_corpus (`corpusBalance - requestedAmount >= corpusBalance × 0.10`, on_fail set_corpus_warning) |
| `on_submit` | validate_form · submit_loan_application (post_loan) → on_success navigate_to_meeting_conduct / on_error show_error |

## Dependencies

- **Features:** `loan-list` (entry), `meeting-conduct` (post-submit vote)
- **Libraries:** `cmp-network-monitor`; external: Store5, SQLDelight, Fineract m_loan
- **Local DB tables:** group_members, loan_products, dt_group_config

## DTOs

See `exports/loan-apply/API.md`. Key types: `GroupMember`, `LoanProduct`,
`LoanPurpose` (MEDICAL, EDUCATION, BUSINESS, EMERGENCY, OTHER), `LoanApplicationRequest`,
`GroupConfig`.

## Testing (21 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LA-001 | P0 | Loading fetches members/products/corpus/config in parallel → Content |
| TC-LA-002 | P0 | eligibleAmount computed from savings × loanMultiplier |
| TC-LA-003 | P1 | Submitting disables inputs + shows submit loading |
| TC-LA-004 | P1 | Error state renders error_state with retry CTA |
| TC-LA-005 | P0 | OnMemberSelected fetches savings + template, recomputes eligibility |
| TC-LA-006 | P0 | OnAmountChanged over ceiling sets amountError, disables submit |
| TC-LA-007 | P0 | OnAmountChanged within ceiling clears amountError, enables submit |
| TC-LA-008 | P1 | corpus_warning_banner shows when disbursement breaches 10% buffer |
| TC-LA-009 | P1 | OnProductSelected loads loan template to pre-fill |
| TC-LA-010 | P1 | OnDurationChanged updates durationWeeks |
| TC-LA-011 | P1 | OnPurposeChanged stores LoanPurpose; BUSINESS default |
| TC-LA-012 | P1 | OnBack pops without persisting |
| TC-LA-013 | P0 | OnSubmit online POSTs /loans → navigates to meeting-conduct |
| TC-LA-014 | P1 | OnSubmit 400 shows per-field validation errors |
| TC-LA-015 | P1 | OnSubmit 403 shows insufficient-role error |
| TC-LA-016 | P0 | OnSubmit offline blocked by cmp-network-monitor (Network error) |
| TC-LA-017 | P1 | OnSubmit 422 corpus-insufficient error |
| TC-LA-018 | P1 | OnSubmit 500 retry-able Server error |
| TC-LA-019 | P0 | Auth 401 redirects to login |
| TC-LA-020 | P1 | Offline mount serves cached members/products/config |
| TC-LA-021 | P0 | Eligibility ceiling enforced (amount capped at savings × multiplier) |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-apply/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-apply/preview/`
- **Design conformance:** `eligibility_banner` (primaryContainer) shows savings balance +
  max-eligible line only when a member is selected. `corpus_warning_banner` (amber `#FFF9C4` /
  `#E65100`) appears above submit when the 10% buffer would be breached. `amount_input` surfaces
  `amountError` inline. Submit button (primary, 24dp radius, 56dp min-touch, fill width) shows a
  loading indicator while submitting and is disabled until all required fields validate.
