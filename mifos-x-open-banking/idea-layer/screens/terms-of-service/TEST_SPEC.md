# TEST SPEC — Terms of Service

| Field      | Value                                       |
|------------|---------------------------------------------|
| Feature    | terms-of-service                            |
| Source     | `screens/terms-of-service/tests.yaml`       |
| Scenarios  | 15                                          |
| Priorities | high 6 · medium 8 · low 1                   |
| States     | content 15                                  |
| Module     | _none yet — spec-only feature_              |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| content | 15 | TC-TOS-001 … -015 |

Single-state, for the same reason as `privacy-policy`: TC-TOS-013 pins `static_content`, clauses
from the compile-time constant `tosSections`, no ViewModel and no network. Nothing can fail to
load, so there is no other state to reach.

---

## Twelve of fifteen scenarios test the wording of a legal document

Like its `privacy-policy` sibling, this spec asserts *what the copy says*, clause by clause. That
is the correct treatment: the terms are the feature, and a wrong sentence here is a
misrepresentation rather than a rendering bug.

| # | Clause | Scenario | The claim under test |
|---|--------|----------|----------------------|
| — | Agreement Overview | TC-TOS-001, -002 | un-numbered, renders first |
| 1 | Acceptance | TC-TOS-003 | install / sign-in / use are the binding acts |
| 2 | Demo service | TC-TOS-004 | not a bank; no real money; no deposit guarantee |
| 3 | Account usage | TC-TOS-005 | **never reuse a real banking password** |
| 4 | Prohibited use | TC-TOS-006 | five named prohibitions |
| 5 | Licensing | TC-TOS-007 | code rights come from MPL-2.0, not these terms |
| 6 | Data handling | TC-TOS-008 | no real personal or payment details |
| 7 | Warranty | TC-TOS-009 | mirrors MPL-2.0 §6 |
| 8 | Liability | TC-TOS-010 | carve-out justified by holding no real funds |
| 9 | Changes | TC-TOS-011 | tied to the visible version stamp |
| 10 | Contact | TC-TOS-012 | three routes, ten working days |

---

## The two clauses that protect a real person

Most of this document protects the project. Two clauses protect the customer, and both are
`priority: high`:

**TC-TOS-005** — the copy explicitly warns never to reuse a password from a real banking service.
This is the single most consequential sentence in the app. A sandbox demo that invites credential
entry will receive real banking passwords unless it says otherwise, plainly, at the point of use.
Worth noting the warning lives *here* — in terms most people will not open — and not on the
`login` screen where the password is typed.

**TC-TOS-008** — entering real personal details, real account numbers or real payment credentials
is forbidden, and periodic resets remove data permanently and irrecoverably. The second half is
what makes the first half credible: it explains *why* the prohibition exists rather than merely
asserting it.

---

## TC-TOS-001 — Content state renders the overview plus all ten numbered clauses

**Priority:** high · **State:** content

- **Given** `TermsOfServiceScreen` composed at route `/legal/terms`
- **When** Screen renders
- **Then**
  - Top app bar shows "Terms of Service" with an `arrow_back` navigation icon; no bottom nav
  - `tos_intro_card` renders first as the un-numbered Agreement Overview
  - Cards 1 through 10 render in order: `acceptance`, `demo_service`, `account_usage`, `prohibited`, `licensing`, `data_handling`, `warranty`, `liability`, `changes`, `contact`
  - `tos_last_updated_text` closes the screen
  - Content is the only declared state

---

## TC-TOS-002 — Clause numbering is contiguous and starts after the overview

**Priority:** medium · **State:** content

- **Given** Content state
- **When** The section headers are read in order
- **Then**
  - `tos_intro_header` "Agreement Overview" carries no number
  - Headers read "1. Acceptance of Terms" through "10. Contact" with no gaps or repeats
  - Each header renders as a heading for assistive tech

Numbering is not cosmetic in a legal document — clauses get cited by number, and a gap or repeat
makes a citation ambiguous. Asserting contiguity catches the usual failure: a clause removed
without renumbering the rest.

---

## TC-TOS-003 — Acceptance clause names the binding actions

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `tos_acceptance_body` renders
- **Then**
  - Installing the app, granting it an Open Banking consent at your bank, or otherwise using the app are named as acceptance
  - The copy tells a non-agreeing user not to use the app
  - Organisational use requires confirmed authority to accept

Acceptance by installation means the customer is bound before they ever open this screen. Standard
practice, and it makes the placement of TC-TOS-005's never-asks-for-credentials statement matter
more, not less.

---

## TC-TOS-004 — Clause 2 disclaims regulated-institution status

**Priority:** high · **State:** content

- **Given** Content state
- **When** `tos_demo_service_body` renders
- **Then**
  - The app is stated not to be a bank, e-money institution or other regulated financial service
  - It is stated never to hold, move or safeguard real money
  - All data is described as synthetic sandbox data that may be reset without notice
  - No balance is stated to be covered by any deposit guarantee scheme

The deposit-guarantee sentence is the one that would matter in a dispute. An app that renders
balances, statements and payment confirmations looks like a bank; saying it is not one is a
different claim from saying no deposit protection applies to what it shows.

---

## TC-TOS-005 — Credentials clause states the app never asks for banking credentials

**Priority:** high · **State:** content

- **Given** Content state
- **When** `tos_account_usage_body` renders
- **Then**
  - Access is described as granted by the Open Banking consent the user approves at their bank
  - The copy **explicitly states the app has no account and no password field and will never ask for banking credentials**
  - Suspected compromise of banking credentials is to be reported to the bank
  - Access is stated to be revocable at any time, from the app or from the bank

Under FAPI the customer authenticates on HSBC's own domain via redirect, so the app never sees a
username or password — there is no PSU credential for it to hold or for these terms to protect.
The assertion is therefore a negative one: the strongest thing the clause can say is that the
credential field does not exist. It doubles as an anti-phishing statement, which is why the
"if any app claiming to be an Open Banking provider asks, that is not how the standard works"
sentence is load-bearing rather than decorative.

---

## TC-TOS-006 — Acceptable-use clause enumerates all five prohibitions

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `tos_prohibited_body` renders
- **Then**
  - Attacking, overloading or circumventing sandbox security and rate limits is prohibited
  - Harvesting or scraping other sandbox users' data is prohibited
  - Presenting the app or its synthetic data as a real banking service to mislead is prohibited
  - Introducing malicious code is prohibited
  - Any unlawful purpose is prohibited

The third prohibition is the interesting one — it forbids the customer doing to others exactly
what TC-TOS-004 commits the app itself not to do.

---

## TC-TOS-007 — Licensing clause defers code rights to the MPL, not to the terms

**Priority:** high · **State:** content

- **Given** Content state
- **When** `tos_licensing_body` renders
- **Then**
  - The source is stated to be licensed under Mozilla Public License v2.0 with the URL given
  - Rights to use, modify and redistribute are stated to come from **that licence** rather than these terms
  - Mifos marks and bundled third-party licences are reserved, and use of the bank's Open Banking APIs is stated to be additionally subject to HSBC's developer terms

The deferral matters legally: terms of service that appeared to grant or restrict code rights would
conflict with the MPL the project actually ships under. Consistent with `about` TC-ABOUT-009 (the
MPL text is reachable) and `licences` TC-LICENCES-001 (it is bundled in the build).

---

## TC-TOS-008 — Sandbox-data clause forbids entering real personal or payment details

**Priority:** high · **State:** content

- **Given** Content state
- **When** `tos_data_handling_body` renders
- **Then**
  - Entered data is described as non-confidential test data stored on the sandbox
  - Entering real personal details, real account numbers or real payment credentials is forbidden
  - Periodic resets are stated to remove data permanently and irrecoverably
  - The clause cross-references the Privacy Policy

---

## TC-TOS-009 — Warranty disclaimer mirrors MPL-2.0 Section 6

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `tos_warranty_body` renders
- **Then**
  - The app and sandbox are provided "as is" and "as available"
  - Merchantability, fitness for a particular purpose, availability and data accuracy are all disclaimed
  - The clause states it mirrors the warranty disclaimer in Section 6 of the MPL-2.0

Naming the source section is a good habit — it makes the clause auditable against the licence
instead of standing as boilerplate that happens to resemble it.

---

## TC-TOS-010 — Liability clause ties the monetary carve-out to the no-real-funds fact

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `tos_liability_body` renders
- **Then**
  - Indirect, incidental, special, consequential and punitive damages plus data loss are excluded to the extent permitted by law
  - The Mifos Initiative, contributors and the sandbox operators are the named beneficiaries
  - The no-monetary-claim statement is justified by the app never holding real funds

Justifying the exclusion rather than merely asserting it is unusual and better. A blanket
liability waiver reads as self-serving; one grounded in a verifiable fact — no real money passes
through — is a claim the reader can check against TC-TOS-004.

---

## TC-TOS-011 — Changes clause ties revisions to the visible version stamp

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `tos_changes_body` renders
- **Then**
  - Material changes are stated to be announced in the app and in the project repository
  - The version stamp at the bottom of the screen is stated to update with each revision
  - `tos_last_updated_text` reads "Last updated: 28 May 2026 — Version 1.0"

The clause makes a promise the assertion then enforces: a terms edit that leaves the stamp
unchanged breaks this test. Same mechanism as `privacy-policy` TC-PP-014, and both stamps
currently read 28 May 2026 · Version 1.0 — note this one uses an em dash where the privacy policy
uses a middot.

---

## TC-TOS-012 — Contact clause gives three routes and a response expectation

**Priority:** low · **State:** content

- **Given** Content state
- **When** `tos_contact_body` renders
- **Then**
  - mifos.org community, a GitHub issue and `legal@mifos.org` are all named
  - A ten-working-day response aim is stated

A stated response time is a commitment worth keeping deliberate — it is the sort of line that is
easy to write and easy to miss when the project's capacity changes.

---

## TC-TOS-013 — Screen is static and cannot fail to load

**Priority:** high · **State:** content

- **Given** `TermsOfServiceScreen(onBack, modifier)` is composed
- **When** Its contract is inspected
- **Then**
  - `state_model` type is `static_content` — no ViewModel, no DI, no repository, no events, no network
  - Clauses come from the compile-time constant `tosSections`
  - No loading skeleton, error state or retry affordance exists

Terms shipped with the build rather than fetched. The right call for a document the customer is
bound by: the version they can read is the version they agreed to, and it cannot be changed under
them or fail to arrive.

---

## TC-TOS-014 — Full terms are reachable by scrolling

**Priority:** medium · **State:** content

- **Given** Content greatly exceeds one viewport at `baseline_width: 390`
- **When** User scrolls to the bottom
- **Then**
  - All eleven cards and the last-updated stamp are reachable inside the vertical scroll
  - No clause is clipped or unreachable

An unreachable clause in a document the customer is bound by is worse than a layout bug. This is
the assertion that makes "you agreed to these terms" defensible.

---

## TC-TOS-015 — Back returns to the Settings entry point

**Priority:** medium · **State:** content

- **Given** Screen entered from Settings → Terms of Service
- **When** User taps the top app bar back icon
- **Then**
  - The `onBack` lambda is invoked
  - The user returns to the entry point (`nav_back`)

---

## Traceability

| Clause card | Scenario |
|-------------|----------|
| `tos_intro_card` | TC-TOS-001, -002 |
| 1 `acceptance` | TC-TOS-003 |
| 2 `demo_service` | TC-TOS-004 |
| 3 `account_usage` | TC-TOS-005 |
| 4 `prohibited` | TC-TOS-006 |
| 5 `licensing` | TC-TOS-007 |
| 6 `data_handling` | TC-TOS-008 |
| 7 `warranty` | TC-TOS-009 |
| 8 `liability` | TC-TOS-010 |
| 9 `changes` | TC-TOS-011 |
| 10 `contact` | TC-TOS-012 |

All eleven cards have exactly one covering scenario.

---

_Generated by /idea-feature-test-export | 2026-08-04_
