# MifosX BackOffice — Generic Fineract Back-Office Platform (Master Spec)

> **Project:** `mifos-x-backoffice-next-gen` · KMP (Compose Multiplatform, Android + iOS + Desktop) · offline-first · permission-driven.
> Grounded in four audits (this idea-layer's `research/`): [FINERACT_API_SURFACE.md](research/FINERACT_API_SURFACE.md) (live spec: 600 paths / 965 ops), [PERMISSION_SCOPE_MODEL.md](research/PERMISSION_SCOPE_MODEL.md) (source-verified capability model), [OFFLINE_FIRST_BLUEPRINT.md](research/OFFLINE_FIRST_BLUEPRINT.md) (openMF/kmp-project-template Store5 patterns), [REFERENCE_FIELD_OFFICER_APP.md](research/REFERENCE_FIELD_OFFICER_APP.md) (openMF/mifos-x-field-officer-app — reference only, fresh build).

## 1. What we're building (the concept)

A **single back-office platform** — one KMP binary — that exposes the **entire Apache Fineract API surface** (965 operations) as real, end-to-end features, and shows each user **exactly and only** the features their server-returned permissions allow (**View / Create / Edit / Delete / workflow-action** per feature). This is **not a field-officer app**. It is the generic back office for **every role**: system admin, branch manager, accountant, teller/cashier, product admin, loan officer, collections field officer, branch supervisor (checker), CSR, auditor. A "role" is just a permission bundle — the same binary is every one of them. It works **offline-first** throughout, so any role can work in low/no connectivity.

Backend is Apache Fineract (Mifos), consumed as-is — **zero server forks**. Sandbox: `https://sandbox.mifos.community/fineract-provider/api/v1`. The existing `openMF/mifos-x-field-officer-app` is a **reference** for feature ideas only — we build fresh with a generic, permission-gated architecture (its field-officer-centric assumptions are exactly what we generalize away from).

## 2. Three architectural pillars

### Pillar A — Permission-driven capability model (the core concept)
`POST /v1/authentication` returns `permissions: Collection<String>` — flat opaque codes (`READ_CLIENT`, `DISBURSE_LOAN`, `CREATE_JOURNALENTRY`, `ALL_FUNCTIONS`…). We normalize these into a `PermissionSet` (O(1) lookup + fingerprint, encrypted) and resolve a **Capability Map** (data, not code — `capability-map.json`, remote-updatable) via a `PermissionEvaluator`: the ONLY authorization authority the UI talks to. **Each of the 17 modules is a nav root gated by its permission group**; actions are `Gated{}`; the domain layer double-enforces; a `403` refreshes the map and prunes the UI (never crashes). Grammar mirrors the server exactly (`canView`, `canDo` (write-umbrella never grants), `canCheck`, backdated `*INPAST_LOAN`). Full model + capability tables: `research/PERMISSION_SCOPE_MODEL.md`.

### Pillar B — Complete Fineract API surface (every endpoint is a feature)
965 operations across identity/access, clients (KYC/360°), groups & centers, loans (incl. Working-Capital), savings/deposits/shares, collections, accounting/GL, products & charges, organization, users/roles/permissions, tellers/cash, datatables/config, scheduler/jobs, reports/search/audit, maker-checker, communications, and cross-cutting (batches, documents, notifications). Universal contracts: tenant header, template pattern (`GET /{entity}/template`), command pattern, maker-checker (queued 2xx), external-ID mirrors (~180 ops), `POST /batches` (transactional — the offline-sync keystone). Full map: `research/FINERACT_API_SURFACE.md`.

### Pillar C — Offline-first on openMF/kmp-project-template
The template's `core-base/store` + `core/store` seam **is** an offline-first REST-client skeleton: reads via `StoreFactory.createStore` + Room `SourceOfTruth` + `asScreenStream` (`CACHE_FIRST_SWR`) + `ScreenContent` (6 states free); queued writes via `DraftSubmitHandler` + `RoomSubmitOutbox` + `OfflineSubmitSyncer`; batch replay via `BatchSubmitHandler.AllOrNothing` (≙ `POST /batches`); delta sync via `Synchronizer.changeListSync` (KDoc names Fineract). Each feature spans A–L slot layers. Full blueprint + recipe: `research/OFFLINE_FIRST_BLUEPRINT.md`.

## 3. The 5 NEW infrastructure pieces
The template gives reads/writes/sync/batch free. We build:
1. **`core/permissions`** — `PermissionSet` + `PermissionEvaluator` + `CapabilityMap` + Compose `Gated{}` + build-time nav filter (Pillar A).
2. **Dynamic template-driven forms** — schema model + renderer from Fineract `GET /{entity}/template` + `/datatables`; `JsonObject` payloads through the outbox; templates cached offline.
3. **Durable idempotency** — persist `idempotency_key` on `DraftEntity` (Room v11); zero double-post on retries.
4. **Needs-Attention conflict inbox** — `DraftDao.observeAllFailed()` + Retry/Edit/Discard + explicit `ConflictStrategy`.
5. **Per-entity Fineract delta adapters** — `lastModifiedSince`/audit feeds onto `changeListSync`; per-adapter isolation.

## 4. Personas = permission bundles (same binary is all of them)
- **System admin** (`ALL_FUNCTIONS`) — the entire platform.
- **Branch manager** — portfolio + approvals + reports + staff oversight.
- **Accountant** — Accounting (GL, journals, closures, provisioning); portfolio read-only.
- **Teller/cashier** — money movement + teller/cash management.
- **Product admin** — products & charges + data-tables/config.
- **Loan officer (maker)** — client onboarding + loan origination; Approve/Disburse shown-but-disabled.
- **Collections field officer** — field-ops dashboard + collection sheets + attendance; read-only elsewhere.
- **Branch supervisor (checker)** — Maker-Checker inbox + audit.
- **CSR** — client profile view/update + notes + account lookup.
- **Auditor** (`ALL_FUNCTIONS_READ`) — everything readable, every report runnable, zero mutating controls.

## 5. The 17 back-office modules (each API-complete + permission-gated + offline-first)
`M01 Dashboard` (role-adaptive tiles) · `M02 Clients & KYC` · `M03 Groups & Centers` · `M04 Loan Portfolio` (origination/servicing/delinquency/reschedule/working-capital) · `M05 Savings, Deposits & Shares` · `M06 Collections` (field ops) · `M07 Accounting & GL` · `M08 Products & Charges` · `M09 Organization` (offices/staff/holidays/funds/codes) · `M10 Users, Roles & Permissions` · `M11 Tellers & Cash` · `M12 Data Tables & Configuration` · `M13 Scheduler & Jobs` · `M14 Reports, Search & Audit` · `M15 Approvals (Maker-Checker)` · `M16 Communications` (SMS/email/templates) · `M17 Sync & Settings`. A field officer sees ~3 of these; a system admin sees all 17 — same binary, decided by permissions.

## 6. Non-functional + security
Offline-first (100% of capture workflows offline; outbox survives crash + reinstall-restore; **zero duplicate/lost transactions** via durable idempotency + batch). TLS 1.2+ + cert pinning; Keystore/Keychain + biometric; SQLCipher DB + encrypted media; PII-scrubbed logs; server authorization is the only real gate; screenshot-block PII; DPDP/GDPR; OWASP MASVS L2 + pen test. Android 8.0+ / iOS 15+ / Desktop; server-version handshake at login; multi-tenant + multi-server switch.

## 7. Delivery roadmap
- **P0 Foundations** — Fineract OpenAPI client, tenant/auth + `core/permissions` bootstrap, encrypted storage, dynamic-forms engine, CI. *Exit: login flips the 17 module roots + actions by permissions.*
- **P1 Read platform** — Dashboard + Clients + Loans + Savings read/detail (gated, offline), search, reports (read), audit. *Exit: any role gets a complete read-only back-office offline.*
- **P2 Money movement + collections** — repayments/deposits/withdrawals/charges, collection sheets, outbox + batch + durable idempotency, Needs-Attention, tellers/cash. *Exit: field + teller staff transact offline with zero double-post.*
- **P3 Origination** — template-driven onboarding + loan/savings/FD/RD/share wizards, guarantors/collateral, maker-checker. *Exit: full origination without paper.*
- **P4 Supervision + accounting** — checker inbox, approve/disburse/reschedule/transfers; accounting (GL/journal/closure/provisioning). *Exit: supervisors approve; accountants close books in-app.*
- **P5 Full admin + hardening** — users/roles/permissions, products/charges, organization, datatables/config, scheduler, campaigns; i18n, MASVS L2, pen test. *Exit: every Fineract endpoint live, gated by login permissions.*
- **P6 Rollout & ops** — staged rollout per role, training, telemetry, Fineract-upgrade regression (contract tests vs the live spec).

## 8. Definition of done
A user of ANY role logs in against the institution's production Fineract tenant, sees exactly and only the modules + features their permissions allow, performs their full job — from a collections officer's day of sheets to a system admin's product + user + accounting administration — offline where needed, syncs with **zero duplicate or lost transactions**, and Fineract reflects every action with full audit and maker-checker integrity, at ≥99.5% crash-free sessions.
