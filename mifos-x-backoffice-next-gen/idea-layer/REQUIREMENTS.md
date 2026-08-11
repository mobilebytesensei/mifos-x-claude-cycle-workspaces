# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/idea-layer/REQUIREMENTS.md"

# Requirements Registry — mifos-x-backoffice-next-gen

> **Last Updated**: 2026-07-17
> **Single source of truth** for ALL product requirements.
> Managed by `/idea`. Read by `/design`, `/server`, `/implement`, `/test`.
> Derived from `idea-layer/idea-plan.yaml` §requirements, §technical_decisions, §permission_scope.

---

## Technical Context

| Attribute | Value |
|-----------|-------|
| Architecture | MVI (Compose Multiplatform + Store5 offline-first) |
| Backend Type | none (Apache Fineract consumed as-is — zero server forks) |
| Base URL | `{host}/fineract-provider/api/v1/…` · sandbox `https://sandbox.mifos.community/fineract-provider/api/v1` |
| Auth Method | basicAuth `base64EncodedAuthenticationKey` after `POST /v1/authentication`; OAuth2/OIDC optional; `Fineract-Platform-TenantId` header on every op |
| Database | Room-KMP (SQLCipher) — per-entity cache + `framework_submit_drafts` outbox (v11) |
| API Docs | `research/FINERACT_API_SURFACE.md` (OpenAPI 3.0.3, 600 paths / 965 ops, Fineract 1.16.0-SNAPSHOT) |

### Key Entities / Data Model

| Entity | Description | Storage | CRUD | Feature |
|--------|-------------|---------|:----:|---------|
| Client | KYC/360° customer | Room cache + Fineract | CRUD | M02 |
| Loan | Full lifecycle incl. Working-Capital | Room cache + Fineract | CRUD | M04 |
| SavingsAccount/FD/RD/Share | Deposits & shares | Room cache + Fineract | CRUD | M05 |
| CollectionSheet | Center/group/individual dues | Room cache + Fineract | RU | M06 |
| JournalEntry/GLAccount | Accounting & GL | Fineract (online-only) | CR | M07 |
| User/Role/Permission | Admin control plane | Fineract (online-only) | CRUD | M10 |
| DraftEntity (outbox) | Queued offline mutation + durable idempotency_key | Room v11 (local) | CRUD | F02/F04 |
| PermissionSet/CapabilityMap | Normalized login permissions[] + data-driven map | encrypted local + core/permissions | derived | F01 |

### Third-Party Services

| Service | Purpose | SDK/Library | Required |
|---------|---------|-------------|:--------:|
| Apache Fineract REST API | Entire back-office capability set (965 ops) | openMF Fineract Client KMP SDK (+ generated-from-OpenAPI/Ktorfit for gaps) | ✅ |
| Store5 (`org.mobilenativefoundation.store`) | Offline-first read/write/batch/delta | kmp-project-template `core-base/store` | ✅ |

---

## Functional Requirements (FR)

| ID | Requirement | Priority | Feature | Acceptance Criteria | Status |
|----|-------------|:--------:|---------|---------------------|:------:|
| FR-1 | Login `POST /authentication` + tenant header; persist permissions[]+fingerprint (encrypted); build CapabilityMap | must | F01 | Login flips the 17 module roots + actions by permissions vs sandbox | planned |
| FR-2 | Permission-gated **3-tier** assembly across ALL 17 modules — Tier1 nav root HIDDEN when zero family codes (fail-closed); Tier2 feature opens on ≥1 family code; Tier3 lacked actions GRAYED-OUT + on-tap "You don't have permission, contact your manager" dialog; every control `action_contract{required_permission, denied_behavior:gray-out-info-dialog}`; effective set = union of roles' codes (ALL_FUNCTIONS=all); domain double-enforce | must | F01, F22, M01–M17 | Same binary renders admin vs teller vs field-officer from permissions alone; lacked actions grayed with a reason | planned |
| FR-3 | Offline outbox — every mutating command persisted w/ durable idempotency key + (action,entity); replay via `POST /batches` | must | F02 | Exactly-once replay; zero double-post; outbox survives crash + reinstall-restore | planned |
| FR-4 | Delta-pull sync scoped to the user's office/portfolio; CACHE_FIRST_SWR reads everywhere | must | F02, M01–M17 | Any role gets a complete read-only back-office offline | planned |
| FR-5 | Dynamic forms rendered from `GET /{entity}/template` + `/datatables` (cached offline) | must | F03 | A back-office config change appears next sync, no release | planned |
| FR-6 | Maker-checker aware; checker inbox for authorized users | should | M15 | Self-scoped checker inbox; approve/reject queued commands | planned |
| FR-7 | 403 drift protocol — refresh permissions, re-resolve, prune, notify once; replay revalidates permission | must | F01 | 403 never crashes; UI pruned + notified once | planned |
| FR-8 | Multi-platform (Android/iOS/Desktop) single codebase; tenant + server switch | must | M17 | Tenant/server switch (dev/sandbox/prod) works on all platforms | planned |
| FR-9 | Role-adaptive **nav shell** — bottom-bar (phone) + NavigationRail/drawer (desktop) roots data-bound to the resolved permission module roster; roots with zero family permission hidden | must | F22 | A super-user, admin and loan-officer open the same binary and see different nav rosters | planned |
| FR-10 | **Network-config product onboarding** (powered by Mifos Initiative) — sign-in has professional username+password + [Scan config]/[Configure]; config page offers Mifos community demo OR own-org Fineract (base-URL/tenant/user/pass) + Scan-QR + Reset-to-demo; save re-points + forces re-auth; demo default seeded in core/network | must | F23 | Any MFI points the app at their own instance (scan or type) or uses the demo; usable out-of-box | planned |
| FR-11 | **Per-role dashboard assembly** + first-run role walkthrough — the home assembles My Field Day / Operations / Platform Admin from the resolved permission set | must | M01, F22 | Loan-officer, admin and super-user each get a distinct assembled home | planned |
| FR-12 | **App lock** — numeric passcode (set/enter) + biometric enrollment + 15s background re-lock | should | F24, F25 | App re-locks after background timeout; biometric unlock with passcode fallback | planned |

---

## Server / API Requirements (SFR)

> Backend provider is `none`. The app CALLS Apache Fineract's existing REST API — the server layer is API contract documentation (no server built). Full endpoint map in `research/FINERACT_API_SURFACE.md`.

| ID | Endpoint group | Method | Purpose | Feature | Auth | Status |
|----|----------------|:------:|---------|---------|:----:|:------:|
| SFR-1 | `/v1/authentication`, `/v1/userdetails` | POST/GET | Session + permissions[] | F01 | basicAuth + tenant | planned |
| SFR-2 | `/v1/clients` (+template, +external-id, sub-resources) | GET/POST/PUT/DELETE | Client 360° + lifecycle | M02 | basicAuth | planned |
| SFR-3 | `/v1/loans` (+template, calculateLoanSchedule), `/transactions`, `/rescheduleloans` | GET/POST/PUT | Loan lifecycle + servicing | M04 | basicAuth | planned |
| SFR-4 | `/v1/savingsaccounts`, `/fixeddepositaccounts`, `/recurringdepositaccounts`, `/accounttransfers` | GET/POST/PUT | Deposit & share lifecycle | M05 | basicAuth | planned |
| SFR-5 | `POST /v1/collectionsheet`, `/v1/centers/{id}?command=saveCollectionSheet` | POST | Collection sheets | M06 | basicAuth | planned |
| SFR-6 | `/v1/glaccounts`, `/v1/journalentries`, `/v1/glclosures` | GET/POST | Accounting & GL | M07 | basicAuth | planned |
| SFR-7 | `/v1/users`, `/v1/roles`, `/v1/roles/{id}/permissions`, `/v1/permissions` | GET/POST/PUT | Admin control plane | M10 | basicAuth | planned |
| SFR-8 | `/v1/makercheckers` (+approve/reject) | GET/POST/DELETE | Checker inbox | M15 | basicAuth | planned |
| SFR-9 | `/v1/runreports/{name}`, `/v1/search`, `/v1/audits` | GET | Reports, search, audit | M14 | basicAuth | planned |
| SFR-10 | `POST /v1/batches?enclosingTransaction=` | POST | Transactional offline-outbox replay (keystone) | F02 | basicAuth | planned |

---

## Data Requirements (DR)

| ID | Entity | Storage | Cache TTL | Sync Strategy | Feature | Status |
|----|--------|---------|-----------|---------------|---------|:------:|
| DR-1 | Cached Fineract reads (Client/Loan/Savings/…) | Room (SQLCipher) | per-entity FreshnessBands | offline-first (CACHE_FIRST_SWR) + delta changeListSync | M01–M17 | planned |
| DR-2 | DraftEntity outbox (`framework_submit_drafts`) | Room v11 (SQLCipher) | PENDING never pruned; 30d for terminal | write-through via `POST /batches` on reconnect | F02/F04 | planned |
| DR-3 | Reference data (offices, codes, paymenttypes, currencies, templates) | Room | boot-hydrated | polling/on-boot; feeds offline dropdown vocabularies | M09/F03 | planned |
| DR-4 | PermissionSet + fingerprint + CapabilityMap | encrypted local store | per-session; refresh on 403 | manual (re-login) + 403-drift refresh | F01 | planned |

Storage: room-kmp (SQLCipher) · Sync: offline-first, write-through, delta

---

## Integration Requirements (IR)

| ID | Service | Purpose | SDK/Library | Required | Status |
|----|---------|---------|-------------|:--------:|:------:|
| IR-1 | Apache Fineract REST API | Entire back-office capability set (965 ops) | openMF Fineract Client KMP SDK + generated-from-OpenAPI/Ktorfit | ✅ | planned |
| IR-2 | Store5 offline-first stack | Reads/writes/batch/delta | kmp-project-template `core-base/store` + `core/store` | ✅ | planned |
| IR-3 | Secure storage + biometrics | Keystore/Keychain, SQLCipher, biometric lock | platform expect/actual | ✅ | planned |

---

## Non-Functional Requirements (NFR)

| ID | Requirement | Category | Target | Status |
|----|-------------|----------|--------|:------:|
| NFR-1 | Cold start <2.5s; large lists paginated <1s from cache; day's ops sync <60s/3G | performance | as stated | planned |
| NFR-2 | Zero duplicate/lost transactions; outbox survives crash + reinstall-restore | reliability | 0 dup/lost | planned |
| NFR-3 | English + N locales; a11y; Android 8.0+ / iOS 15+ / Desktop | usability/accessibility | as stated | planned |
| NFR-4 | Crash-free sessions | reliability | ≥99.5% | planned |
| NFR-5 | Reversal rate | reliability | <0.5% | planned |

---

## Security Requirements (SEC)

| ID | Requirement | Category | Verification | Status |
|----|-------------|----------|--------------|:------:|
| SEC-1 | TLS 1.2+ + cert pinning; Keystore/Keychain + biometric; SQLCipher DB + encrypted media; PII-scrub logs | security | pen test + MASVS L2 | planned |
| SEC-2 | Idempotency keys on all mutations; screenshot-block PII; maker-checker end-to-end | security | integration tests | planned |
| SEC-3 | DPDP/GDPR consent/retention/erasure; root/jailbreak detection; OWASP MASVS L2 + pen test | security/compliance | audit | planned |

---

## Platform Requirements

| Platform | Min Version | Required Capabilities | Features Available |
|----------|-------------|----------------------|-------------------|
| Android | 8.0+ | Keystore, biometric, SQLCipher, offline storage | all (adaptive BottomBar) |
| iOS | 15+ | Keychain, biometric, SQLCipher | all (adaptive) |
| Desktop | KMP desktop (JVM) | secure storage, NavigationRail/drawer | all — first-class (back-office users at desks) |

---

## User Workflows

> Personas are permission bundles — the same binary is all of them (§personas).

| # | Workflow | Persona | Flows Involved | Priority |
|:-:|----------|---------|----------------|:--------:|
| 1 | Login → permission-gated home | any role | login-permission-bootstrap | must |
| 2 | Client onboarding → loan origination | loan-officer (maker) | client-onboarding-to-loan | must |
| 3 | Daily collections + sync | collections field officer | daily-collections | must |
| 4 | Accounting close | accountant | accounting-close | should |
| 5 | Admin setup (users/roles + products) | system admin / product admin | admin-setup | should |
| 6 | Offline recovery / needs-attention | teller / field officer | offline-recovery | must |
| 7 | Checker inbox approvals | branch supervisor (checker) | (M15 checker-inbox) | should |
| 8 | Read-only audit | auditor (ALL_FUNCTIONS_READ) | (M14 report-runner) | should |

---

## Requirement Coverage Summary

| Type | Total | Implemented | Coverage |
|------|:-----:|:-----------:|:--------:|
| FR | 8 | 0 | 0% |
| SFR | 10 | 0 | 0% |
| DR | 4 | 0 | 0% |
| IR | 3 | 0 | 0% |
| NFR | 5 | 0 | 0% |
| SEC | 3 | 0 | 0% |

---

*Managed by `/idea`. Read by downstream commands for validation.*
*`/design` validates FR coverage. `/server` validates SFR. `/implement` uses acceptance criteria for TDD.*
