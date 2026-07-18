# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/idea-layer/ROADMAP.md"

# Product Roadmap — mifos-x-backoffice-next-gen

> **Last Updated**: 2026-07-17
> Managed by `/idea roadmap`. Read by `/gap-planning-project`.
> Strategy: **phased** (P0–P6). Derived from `idea-layer/idea-plan.yaml` §release_plan.
> Every phase ships modules that are permission-gated + offline-first.

---

## P0 — Foundations

**Status**: ❌ Not started | **Target**: —

**Scope**: OpenAPI/Fineract client, tenant/auth + `core/permissions` capability bootstrap, encrypted storage, FineractAuthProvider, dynamic-forms engine, CI.
**Exit**: Login flips the 17 module roots + actions by permissions vs the sandbox.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| permission-capability-engine (F01) | ❌ | ❌ | ❌ |
| offline-sync-engine (F02, infra) | ❌ | ❌ | ❌ |
| dynamic-template-forms (F03) | ❌ | ❌ | ❌ |
| M17 Sync & Settings (tenant/server switch) | ❌ | ❌ | ❌ |

### Release Checklist
- [ ] Fineract OpenAPI client wired (openMF SDK preferred; contract-test CI vs live spec)
- [ ] `core/permissions` PermissionSet + CapabilityMap + PermissionEvaluator
- [ ] Encrypted storage (Keystore/Keychain + SQLCipher)
- [ ] Dynamic-forms engine renders from `GET /{entity}/template`
- [ ] CapabilityMatrixTest golden file green

---

## P1 — Read platform

**Status**: ❌ Planned | **Target**: —

**Scope**: Dashboard + Clients + Loans + Savings read/detail (gated, offline CACHE_FIRST_SWR), search, reports (read), audit.
**Exit**: Any role gets a complete read-only back-office offline.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| M01 Dashboard | ❌ | ❌ | ❌ |
| M02 Clients & KYC (read/360°) | ❌ | ❌ | ❌ |
| M04 Loan Portfolio (read/detail) | ❌ | ❌ | ❌ |
| M05 Savings/Deposits/Shares (read) | ❌ | ❌ | ❌ |
| M14 Reports, Search & Audit (read) | ❌ | ❌ | ❌ |

---

## P2 — Money movement + collections

**Status**: ❌ Planned | **Target**: —

**Scope**: repayments/deposits/withdrawals/charges, collection sheets, outbox + batch + durable idempotency, Needs-Attention, tellers/cash.
**Exit**: Field + teller staff transact offline with zero double-post.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| offline-sync-engine (F02, write path) | ❌ | ❌ | ❌ |
| needs-attention-inbox (F04) | ❌ | ❌ | ❌ |
| M06 Collections | ❌ | ❌ | ❌ |
| M11 Tellers & Cash | ❌ | ❌ | ❌ |
| M05 money movement (deposit/withdrawal) | ❌ | ❌ | ❌ |

---

## P3 — Origination

**Status**: ❌ Planned | **Target**: —

**Scope**: template-driven client onboarding + loan/savings/FD/RD/share application wizards, guarantors/collateral, maker-checker submit.
**Exit**: Full origination without paper.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| M02 Clients (onboarding + externalId queue) | ❌ | ❌ | ❌ |
| M04 Loan origination wizard | ❌ | ❌ | ❌ |
| M03 Groups & Centers | ❌ | ❌ | ❌ |

---

## P4 — Supervision + accounting

**Status**: ❌ Planned | **Target**: —

**Scope**: checker inbox, approve/disburse/reschedule/transfers; accounting (GL/journal/closure/provisioning).
**Exit**: Supervisors approve; accountants close books in-app.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| M15 Approvals (Maker-Checker) | ❌ | ❌ | ❌ |
| M07 Accounting & GL | ❌ | ❌ | ❌ |
| M04 supervision (approve/disburse/reschedule) | ❌ | ❌ | ❌ |

---

## P5 — Full admin + hardening

**Status**: ❌ Planned | **Target**: —

**Scope**: users/roles/permissions, products/charges, organization, datatables/config, scheduler, campaigns; i18n, MASVS L2, pen test, perf.
**Exit**: Every Fineract endpoint live as a feature, gated by login permissions.

### Features

| Feature | Designed | Impl | Tests |
|---------|:--------:|:----:|:-----:|
| M10 Users, Roles & Permissions | ❌ | ❌ | ❌ |
| M08 Products & Charges | ❌ | ❌ | ❌ |
| M09 Organization | ❌ | ❌ | ❌ |
| M12 Data Tables & Configuration | ❌ | ❌ | ❌ |
| M13 Scheduler & Jobs | ❌ | ❌ | ❌ |
| M16 Communications | ❌ | ❌ | ❌ |

### Release Checklist
- [ ] i18n (English + N locales)
- [ ] OWASP MASVS L2 + pen test
- [ ] Performance meets NFR targets (cold start <2.5s, crash-free ≥99.5%)

---

## P6 — Rollout & ops

**Status**: ❌ Planned | **Target**: —

**Scope**: staged rollout per role, training, telemetry, Fineract-upgrade regression (contract tests vs live spec).
**Exit**: Org-wide adoption across all roles.

---

*Managed by `/idea roadmap`. Phases map to FEATURES.md `Phase` column + idea-plan.yaml §release_plan.*
