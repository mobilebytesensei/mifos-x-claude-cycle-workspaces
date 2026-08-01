# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/idea-layer/FEATURES.md"

# Feature Registry — mifos-x-backoffice-next-gen

> **Total**: 30 | **Designed**: 0 | **Implemented**: 0
> **Last Updated**: 2026-08-01 (evolve: role-based-app-assembly — +6 features: nav-shell-assembler, network-config, passcode-lock, biometric-setup, path-tracking, search-record)
> Managed by `/idea`. Read by `/design`, `/implement`, `/gap-planning-project`.
> Derived from `idea-layer/idea-plan.yaml` §features (4 foundation + 17 back-office modules). Every module is permission-gated + offline-first.

---

## Features

| # | Feature | Module | Priority | Permission gate | Screens | API groups | Phase | Designed | Impl | Status |
|:-:|---------|--------|:--------:|-----------------|:-------:|-----------|:-----:|:--------:|:----:|--------|
| F01 | permission-capability-engine | foundation | must_have | (engine — gates everything) | login-tenant | /v1/authentication, /v1/permissions | P0 | ❌ | ❌ | planned |
| F02 | offline-sync-engine | foundation | must_have | (infra) | sync-console | POST /v1/batches, changeListSync | P0/P2 | ❌ | ❌ | planned |
| F03 | dynamic-template-forms | foundation | must_have | (infra) | (all create/edit forms) | GET /{entity}/template, /v1/datatables | P0 | ❌ | ❌ | planned |
| F04 | needs-attention-inbox | foundation | must_have | (infra) | needs-attention-inbox | (outbox DraftDao.observeAllFailed) | P2 | ❌ | ❌ | planned |
| M01 | Role-adaptive Dashboard | m01-dashboard | must_have | view-tiles intersect permissions | dashboard | /v1/runreports, /v1/notifications, /v1/makercheckers, /v1/collectionsheet | P1 | ❌ | ❌ | planned |
| M02 | Clients & KYC | m02-clients | must_have | READ_/CREATE_/UPDATE_/DELETE_CLIENT + sub-resources + lifecycle | client-list, client-detail-360 | /v1/clients (+template,+external-id), sub-resources | P1/P3 | ❌ | ❌ | planned |
| M03 | Groups & Centers | m03-groups-centers | should_have | *_GROUP, *_CENTER, *_MEETING, SAVEORUPDATEATTENDANCE_MEETING | — | /v1/groups, /v1/centers, /v1/calendars, /v1/meetings | P2 | ❌ | ❌ | planned |
| M04 | Loan Portfolio | m04-loan-portfolio | must_have | *_LOAN + APPROVE_/DISBURSE_/REPAYMENT_/WRITEOFF_ + charges/guarantor/collateral/reschedule; *INPAST_LOAN | loan-detail, loan-application-wizard | /v1/loans (+template, calculateLoanSchedule), transactions, rescheduleloans, working-capital-loans | P1/P3/P4 | ❌ | ❌ | planned |
| M05 | Savings, Deposits & Shares | m05-savings-deposits-shares | must_have | *_SAVINGSACCOUNT (+DEPOSIT_/WITHDRAWAL_/HOLDAMOUNT_/POSTINTEREST_), *_FIXEDDEPOSIT/_RECURRINGDEPOSIT/_SHAREACCOUNT, *_ACCOUNTTRANSFER, *_STANDINGINSTRUCTION | — | /v1/savingsaccounts, /v1/fixeddepositaccounts, /v1/recurringdepositaccounts, /v1/accounttransfers, /v1/standinginstructions | P1/P2 | ❌ | ❌ | planned |
| M06 | Collections (field ops) | m06-collections | must_have | READ_COLLECTIONSHEET, SAVE_/SAVECOLLECTIONSHEET_CENTER/_GROUP, REPAYMENT_LOAN, DEPOSIT_SAVINGSACCOUNT | collection-sheet | POST /v1/collectionsheet, /v1/centers/{id}?command=saveCollectionSheet, POST /v1/batches | P2 | ❌ | ❌ | planned |
| M07 | Accounting & GL | m07-accounting | should_have | READ_/CREATE_GLACCOUNT, *_JOURNALENTRY (+REVERSE_), *_GLCLOSURE, *_ACCOUNTINGRULE, provisioning | journal-entry | /v1/glaccounts, /v1/journalentries, /v1/glclosures, /v1/provisioningentries, /v1/runaccruals | P4 | ❌ | ❌ | planned |
| M08 | Products & Charges | m08-products-charges | should_have | *_LOANPRODUCT/_SAVINGSPRODUCT/_FIXEDDEPOSITPRODUCT/_SHAREPRODUCT, *_CHARGE, floating rates, delinquency, tax | product-editor | /v1/loanproducts, /v1/savingsproducts, /v1/charges, /v1/floatingrates, /v1/delinquency/*, /v1/taxes/* | P5 | ❌ | ❌ | planned |
| M09 | Organization | m09-organization | should_have | *_OFFICE, *_STAFF, *_HOLIDAY, *_FUND, *_PAYMENTTYPE, *_CODE/_CODEVALUE, *_CURRENCY | — | /v1/offices, /v1/staff, /v1/holidays, /v1/funds, /v1/paymenttypes, /v1/codes+codevalues, /v1/currencies | P5 | ❌ | ❌ | planned |
| M10 | Users, Roles & Permissions | m10-users-roles-permissions | should_have | *_USER, *_ROLE (+ENABLE_/DISABLE_), READ_PERMISSION, PERMISSIONS_ROLE, UPDATE_PERMISSION | user-role-matrix | /v1/users, /v1/roles, /v1/roles/{id}/permissions, /v1/permissions | P5 | ❌ | ❌ | planned |
| M11 | Tellers & Cash | m11-tellers-cash | could_have | *_TELLER, ALLOCATECASHIER_/ALLOCATECASHTOCASHIER_/SETTLECASHFROMCASHIER_TELLER | teller-cash | /v1/tellers, /v1/tellers/{id}/cashiers, /v1/cashiersjournal | P2 | ❌ | ❌ | planned |
| M12 | Data Tables & Configuration | m12-datatables-config | could_have | *_DATATABLE (+REGISTER_/DEREGISTER_), dynamic {ACTION}_{table}, *_CONFIGURATION | — | /v1/datatables, /v1/entityDatatableChecks, /v1/fieldconfiguration/{entity}, /v1/configurations | P5 | ❌ | ❌ | planned |
| M13 | Scheduler & Jobs (COB) | m13-scheduler-jobs | could_have | READ_/UPDATE_/EXECUTEJOB_SCHEDULER | — | /v1/jobs (+executeJob, runhistory, steps), /v1/scheduler, /v1/businessdate | P5 | ❌ | ❌ | planned |
| M14 | Reports, Search & Audit | m14-reports-search-audit | should_have | READ_{report}∨REPORTING_SUPER_USER, *_REPORT, READ_AUDIT, search | report-runner | /v1/runreports/{name}, /v1/reports, /v1/search+advance, /v1/audits | P1 | ❌ | ❌ | planned |
| M15 | Approvals (Maker-Checker) | m15-approvals-makerchecker | should_have | any *_CHECKER ∨ CHECKER_SUPER_USER; per-entry {ACTION}_{ENTITY}_CHECKER | checker-inbox | /v1/makercheckers (+approve/reject, DELETE, searchtemplate) | P4 | ❌ | ❌ | planned |
| M16 | Communications | m16-communications | could_have | *_SMSCAMPAIGN, email campaign codes, *_REPORTMAILINGJOB, template | — | /v1/smscampaigns, /v1/email/campaign, /v1/reportmailingjobs, /v1/templates | P5 | ❌ | ❌ | planned |
| M17 | Sync & Settings | m17-sync-settings | must_have | (settings) | sync-console | /v1/instance-mode, DynamicBaseUrlPlugin | P0/P2 | ❌ | ❌ | planned |
| F22 | Role-adaptive Nav Shell | nav-shell-assembler | must_have | assembler — renders the permitted module roster | nav-shell-assembler | (permission-capability-engine roster) | P0/R0 | ❌ | ❌ | scaffold |
| F23 | Network Config — product onboarding (powered by Mifos Initiative) | network-config | must_have | (foundation — pre-auth) | network-config | /v1/authentication, DynamicBaseUrlPlugin | P0/R0 | ❌ | ❌ | scaffold |
| F24 | App Lock — passcode | passcode-lock | must_have | (post-auth lock) | passcode-lock | (local) | P0/R0 | ❌ | ❌ | scaffold |
| F25 | Biometric Enrollment | biometric-setup | should_have | (post-auth lock) | biometric-setup | (local, encrypted) | P0/R0 | ❌ | ❌ | scaffold |
| F26 | GPS Field-Visit Route | path-tracking | should_have | loan-officer / collections personas | path-tracking | (core/platform location) | P2/R1 | ❌ | ❌ | scaffold |
| F27 | Offline / Recent Search History | search-record | should_have | field-officer personas | search-record | (local cache) | P1/R1 | ❌ | ❌ | scaffold |
| F28 | Fineract Auth Session — login + persisted session + authenticated client | fineract-auth-session | must_have | (foundation — pre-auth) | fineract-auth-session | /v1/authentication | P0 | ❌ | ❌ | scaffold |
| F29 | Permission Set Detail (resolved codes · umbrellas · fingerprint) | foundation | should_have | (read-only) | permission-set-detail | /v1/permissions | P1 | ❌ | ❌ | scaffold |
| F30 | Capability Map Detail (version · checksum · requirement tree) | foundation | should_have | (read-only) | capability-map-detail | /v1/permissions | P1 | ❌ | ❌ | scaffold |

---

## Feature Dependencies

```
permission-capability-engine (F01)  ──gates──►  ALL 17 modules (M01–M17)
offline-sync-engine (F02)           ──enables──► money-movement in M02/M04/M05/M06/M11
dynamic-template-forms (F03)        ──renders──► create/edit forms in M02/M04/M05/M08/M12
needs-attention-inbox (F04)         ──consumes─► failed replays from F02 outbox
M02 Clients ──precedes──► M04 Loan origination (client-onboarding-to-loan flow)
M10 Users/Roles ──authors──► the permissions[] that F01 consumes
```

---

## Feature-Flow Mapping

> From `idea-layer/idea-plan.yaml` §flows.

| Flow | Screens | Entry point |
|------|:-------:|-------------|
| login-permission-bootstrap | login-tenant → dashboard | app launch |
| client-onboarding-to-loan | client-list → client-detail-360 → loan-application-wizard → checker-inbox → loan-detail | Clients module |
| daily-collections | dashboard → collection-sheet → sync-console | Dashboard tile |
| accounting-close | journal-entry → report-runner | Accounting module |
| admin-setup | user-role-matrix → product-editor | Admin control plane |
| offline-recovery | sync-console → needs-attention-inbox | Sync & Settings |

---

## Feature Acceptance Criteria

> Per-feature acceptance criteria from idea-plan.yaml §features[].acceptance_criteria. Used by `/implement` for TDD test generation.

### permission-capability-engine (F01)
- [ ] AC-001: Login permissions[] normalized to a PermissionSet with umbrella short-circuits; each of the 17 module roots gates on its permission group.
- [ ] AC-002: Nav filtered at build time; `Gated{}` hides/disables per onDenied; unmapped id = HIDDEN (fail closed); domain double-enforces.
- [ ] AC-003: Same binary renders admin vs teller vs field-officer surface purely from permissions (CapabilityMatrixTest golden file green).

### offline-sync-engine (F02)
- [ ] AC-004: Every offline mutation queued with a DURABLE idempotency_key (Room v11) + (action,entity); replay exactly-once (zero double-post).
- [ ] AC-005: Delta-pull hydrates the user's office/portfolio working set via changeListSync adapters; rejected replay → Needs-Attention.

### dynamic-template-forms (F03)
- [ ] AC-006: Create/edit forms rendered from GET /{entity}/template + /datatables; a back-office config change appears next sync, no release.

### needs-attention-inbox (F04)
- [ ] AC-007: Rejected offline commands land here with the server error; Retry/Edit/Discard; ConflictStrategy resolved explicitly; never silently dropped.

### M01 · Role-adaptive Dashboard
- [ ] AC-008: Home tiles = the intersection of the dashboard tile set and the user's permissions; one failing tile never blanks the rest.

### M02 · Clients & KYC
- [ ] AC-009: Client 360 offline; onboarding queues with client-generated externalId; every sub-resource + lifecycle command gated.

### M04 · Loan Portfolio
- [ ] AC-010: Full loan lifecycle template→submit→approve→disburse→service→close; live schedule preview; every command gated; offline-queued.

### M05 · Savings, Deposits & Shares
- [ ] AC-011: Full deposit lifecycle + transactions + holds/blocks + transfers + SI, gated + offline.

### M06 · Collections
- [ ] AC-012: Center/group/individual sheets with dues; bulk atomic batch submit; 30-member sheet <1s cache; receipts.

### M07 · Accounting & GL
- [ ] AC-013: Chart of accounts, balanced manual journal entries, closures, provisioning — gated by the accounting group (online-only + maker-checker).

### M10 · Users, Roles & Permissions
- [ ] AC-014: Create users, assign roles, edit the role→permission matrix, toggle maker-checker per action — the admin control plane.

### M15 · Approvals (Maker-Checker)
- [ ] AC-015: Self-scoped checker inbox; approve/reject queued commands; pre-flight badges via ?makerCheckerable=true.

### M17 · Sync & Settings
- [ ] AC-016: Sync console + Needs-Attention inbox; tenant/server switch (dev/sandbox/prod); i18n; diagnostics; biometric lock.

> Remaining modules (M03, M08, M09, M11–M14, M16) carry their acceptance criteria in idea-plan.yaml §features; enrich per-feature via `/idea-feature-enrich`.

---

*Managed by `/idea`. Bridge between requirements and implementation.*
*Each feature maps to: requirements (FR/SFR/DR) → flow → SPEC.md → source code → tests.*
