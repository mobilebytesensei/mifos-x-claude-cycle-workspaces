# TEST SPEC — Privacy Policy

| Field      | Value                                     |
|------------|-------------------------------------------|
| Feature    | privacy-policy                            |
| Source     | `screens/privacy-policy/tests.yaml`       |
| Scenarios  | 15                                        |
| Priorities | high 9 · medium 6                         |
| States     | content 15                                |
| Module     | _none yet — spec-only feature_            |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| content | 15 | TC-PP-001 … -015 |

Single-state, and TC-PP-013 gives the reason: `static_content`, nine sections from the compile-time
constant `privacyPolicySections`, no ViewModel, no network. There is no load to fail.

---

## This spec tests copy, not code

Eleven of the fifteen scenarios (TC-PP-002 … -012) assert what the **policy text says**. That is
unusual for a test spec and it is right here: on a privacy screen the copy *is* the feature, and a
false claim in it is a compliance defect rather than a typo.

The scenarios are structured as claims that must hold:

| Section | Scenario | The claim under test |
|---------|----------|----------------------|
| GDPR banner | TC-PP-002 | sandbox scope, never a live bank |
| Data touched | TC-PP-003 | three categories; no contacts/location/camera/mic/photos |
| Lawful basis | TC-PP-004 | contract · legitimate interests · consent |
| Purpose | TC-PP-005 | password never stored; no profiling, sale or advertising |
| Local storage | TC-PP-006 | app-private; no maintainer backend |
| Diagnostics | TC-PP-007 | no credentials or account data in reports |
| Sharing | TC-PP-008 | exactly one outbound destination; no tracking SDKs |
| Retention | TC-PP-009 | operator's schedule; clears on sign-out and uninstall |
| Rights | TC-PP-010 | six GDPR rights named; sandbox requests routed onward |
| Contact | TC-PP-011 | community route + supervisory-authority right |

---

## TC-PP-012 is the guard on all of them

TC-PP-012 scans the rendered policy for claims a sandbox demo must **not** make — FCA reporting,
AML/KYC obligations, seven-year retention, Firebase or Crashlytics, identity-document collection.

That is the scenario doing the real work. Privacy policies are routinely assembled from templates
written for regulated live banks, and every item on that list is standard boilerplate. Each one
would be a false statement in this app: it collects no identity documents, has no AML duty, and
ships no Crashlytics. A policy that claims otherwise misleads in the direction of *sounding more
careful than it is*, which is the harder kind to notice in review.

---

## TC-PP-001 — Content state renders the banner, all nine sections and the stamp

**Priority:** high · **State:** content

- **Given** `PrivacyPolicyScreen` composed at route `/legal/privacy`
- **When** Screen renders
- **Then**
  - Top app bar shows "Privacy Policy" with an `arrow_back` navigation icon; no bottom nav
  - `pp_gdpr_banner` visible above every policy card
  - All nine section cards visible in order: `data_collection`, `lawful_basis`, `purpose`, `local_storage`, `diagnostics`, `third_party`, `retention`, `user_rights`, `dpo`
  - `pp_last_updated_text` visible at the foot
  - Content is the only declared state

---

## TC-PP-002 — Sandbox scope is declared before any policy section

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_gdpr_banner` renders
- **Then**
  - Banner text states the app is an open-source UK Open Banking reference client connected to the HSBC UK Open Banking sandbox
  - It states every account, balance and transaction shown is sandbox test data
  - It states the app never connects to a live bank
  - It appears **above** `pp_data_collection_card`, so scope is set before any claim is made

Ordering is asserted, not just presence. Every statement below the banner is scoped by it — "we
never share your banking data" means something different once the reader knows the data is
fictional.

---

## TC-PP-003 — Data-touched section scopes collection to three categories and denies device access

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_data_collection_body` renders
- **Then**
  - Sandbox credentials, sandbox banking data and app preferences are the three named categories
  - The copy explicitly denies requesting contacts, location, camera, microphone and photos

The denial list needs maintaining alongside the app. `atm-locator` (TC-ATM-006) requests coarse
location via `rememberDeviceLocationRequester` — a spec-only feature today, but if it ships this
sentence becomes false. Flagged, not resolved: the fix is a copy change at that point, not now.

---

## TC-PP-004 — Lawful basis enumerates contract, legitimate interests and consent

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `pp_lawful_basis_body` renders
- **Then**
  - Contract performance is cited for the credential-for-token exchange
  - Legitimate interests is cited for non-identifying crash diagnostics
  - Consent is cited for optional diagnostics, with withdrawal available from Settings

Withdrawal "available from Settings" is a promise about another screen. The `settings` feature
ships; whether it carries a diagnostics toggle is not asserted by any scenario in either spec.

---

## TC-PP-005 — Purpose section states the password is never stored

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_purpose_body` renders
- **Then**
  - Credentials are described as sent once and exchanged for a short-lived session token
  - The copy states the password itself is never stored
  - It states nothing is profiled, scored, sold or used for advertising

"Never stored" is a claim about implementation that only the login and change-password paths can
honour. `change-password` TC-CHPW-013 preserves three plaintext passwords **on state** across a
failure — in memory, not on disk, so the claim survives, but the two specs are close enough
together that the distinction should stay deliberate.

---

## TC-PP-006 — Storage section discloses app-private storage and no maintainer backend

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_local_storage_body` renders
- **Then**
  - Session token and preferences are described as app-private, protected by the OS sandbox
  - The copy states the app has no backend of its own
  - It states nothing is uploaded to servers run by the maintainers

---

## TC-PP-007 — Diagnostics section excludes credentials and account data from reports

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `pp_diagnostics_body` renders
- **Then**
  - Diagnostic records are stated never to contain credentials, session token, account numbers or transaction details
  - A Settings toggle is described for builds that ship with diagnostics enabled

---

## TC-PP-008 — Sharing section names exactly one outbound destination

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_third_party_body` renders
- **Then**
  - The only outbound flow named is API requests to the bank's Open Banking endpoint over mutual TLS, processed by HSBC under its own privacy notice
  - The copy states nothing is shared with advertisers, data brokers or social networks
  - It states the app embeds no third-party tracking SDKs

"Exactly one" is the strongest claim in the policy and the easiest to break — a single analytics
dependency added to a build file falsifies it without anyone editing this screen. Worth a build-time
check rather than only a rendering assertion.

---

## TC-PP-009 — Retention section places custody with the sandbox operator

**Priority:** high · **State:** content

- **Given** Content state
- **When** `pp_retention_body` renders
- **Then**
  - Sandbox data is described as following the operator's retention schedule, with the app a window rather than custodian
  - Local cache and session token are stated to clear on sign-out
  - Uninstall is stated to remove everything stored on the device
  - No fixed multi-year retention period is claimed

"A window rather than custodian" is the honest framing for a client that stores nothing of its
own, and the final assertion stops the usual template sentence — a seven-year period this app has
no basis to promise — from creeping back in.

---

## TC-PP-010 — Rights section lists the GDPR rights and routes sandbox requests onward

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `pp_user_rights_body` renders
- **Then**
  - Access, rectification, erasure, restriction, portability and objection are all named
  - Self-service paths (Settings, sign out, uninstall) are described first
  - Requests for data held by the bank itself are directed to HSBC

Self-service first is the right ordering. For most of these rights the customer can act
immediately — signing out and uninstalling *is* erasure for everything the app holds.

---

## TC-PP-011 — Contact section offers a community path and the supervisory-authority right

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `pp_dpo_body` renders
- **Then**
  - A GitHub issue and `privacy@mifos.org` are given as the routes for policy questions
  - Concerns about how the bank processes account and payment data are directed to HSBC as controller
  - The right to complain to a local supervisory authority is stated
  - No named DPO or postal address is claimed

The component is called `dpo` and the last assertion says there is no DPO. Naming an officer this
project has not appointed would be the false-comfort failure again; the id is a leftover from the
section's conventional title.

---

## TC-PP-012 — Policy copy stays truthful to a sandbox demo

**Priority:** high · **State:** content

- **Given** The full rendered policy text
- **When** It is scanned for live-bank obligations
- **Then**
  - No FCA reporting obligation is claimed
  - No AML or KYC obligation is claimed
  - No seven-year retention period is claimed
  - No Firebase, Crashlytics or named KYC provider is claimed
  - No identity-document collection is claimed

---

## TC-PP-013 — Screen is static and cannot fail to load

**Priority:** high · **State:** content

- **Given** `PrivacyPolicyScreen(onBack, modifier)` is composed
- **When** Its contract is inspected
- **Then**
  - `state_model` type is `static_content` — no ViewModel, no DI, no repository, no events, no network
  - The nine sections come from the compile-time constant `privacyPolicySections`
  - No loading skeleton, error state or retry affordance exists

Compile-time constants rather than a fetched document. That is the correct call for a legal
notice: the policy the customer reads is the one that shipped with the build they are running, and
it cannot be swapped underneath them or fail to arrive.

---

## TC-PP-014 — Long policy text is reachable by scrolling

**Priority:** medium · **State:** content

- **Given** Content exceeds one viewport at `baseline_width: 390`
- **When** User scrolls to the bottom
- **Then**
  - All nine cards and `pp_last_updated_text` are reachable inside the vertical scroll
  - `pp_last_updated_text` reads "Last updated: 28 May 2026 · Version 1.0"

The date is asserted as a literal, so this scenario fails the moment the policy is revised — which
is the intended behaviour. A policy edit that leaves the stamp untouched is the defect.

---

## TC-PP-015 — Back returns to the Settings entry point

**Priority:** medium · **State:** content

- **Given** Screen entered from Settings → Privacy Policy
- **When** User taps the top app bar back icon
- **Then**
  - The `onBack` lambda is invoked
  - The user returns to the entry point (`nav_back`)

Note `about` TC-ABOUT-010 asserts its legal rows open **external** URLs and do not navigate here.
Both are consistent: this screen is reached from Settings, not from About.

---

## Traceability

| Section card | Scenario |
|--------------|----------|
| `pp_gdpr_banner` | TC-PP-002 |
| `data_collection` | TC-PP-003 |
| `lawful_basis` | TC-PP-004 |
| `purpose` | TC-PP-005 |
| `local_storage` | TC-PP-006 |
| `diagnostics` | TC-PP-007 |
| `third_party` | TC-PP-008 |
| `retention` | TC-PP-009 |
| `user_rights` | TC-PP-010 |
| `dpo` | TC-PP-011 |

All nine sections plus the banner have exactly one covering scenario, and TC-PP-012 scans the whole.

---

_Generated by /idea-feature-test-export | 2026-08-04_
