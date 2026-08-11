# MifosSave - Mifos X Group Banking

> Offline-first KMP community banking app digitizing VSLA/ROSCA group savings, lending & share-out via Mifos Fineract

| Field | Value |
|-------|-------|
| Project | mifos-x-group-banking |
| Workspace | mifos-x |
| Type | kmp |
| Package | org.mifos.groupbanking |
| Domain | fintech (community-banking, microfinance, savings-groups) |
| Status | planning |

---

## Elevator Pitch

MifosSave digitizes the full lifecycle of self-funded community banking groups — meetings, savings, lending, and share-out — with offline-first KMP and Mifos Fineract backend.

## Problem Statement

Millions of people in emerging markets organize into community savings groups (VSLA, ROSCA, ASCA, SHG) to pool savings, issue loans, and distribute profits. These groups operate with paper ledgers, leading to record-keeping errors, fraud, limited transparency, and inability to scale. Existing digital solutions are either online-only, lack Fineract integration, or don't support the full group lifecycle.

## Solution

MifosSave provides a Kotlin Multiplatform mobile app that digitizes every step of the community banking lifecycle — from group creation and member onboarding, through meeting-driven savings collection and loan disbursement, to periodic share-out — all working offline-first with automatic sync to Mifos Fineract when connectivity is available.

## Core Value Propositions

1. **Offline-first**: full functionality without internet — sync when connected
2. **Meeting-centric workflow**: mirrors how real groups operate (attendance -> savings -> loans -> decisions)
3. **Fineract-backed**: enterprise-grade financial record-keeping via proven open-source core banking
4. **Low-literacy UX**: icon-heavy, minimal text, voice prompts, large touch targets
5. **Transparent**: every member can see group balances, loan status, and share-out projections in real-time

## Target Users

> **One unified identity — anyone can self-sign-up.** No up-front "admin vs member" choice. After login, capabilities are **auto-resolved per group** from the roles the user holds. The same person can organize one group and be a plain member of another. (Global self-signup pivot, 2026-07-17.)

### Roles (resolved per group, after login)
| Role | Scope | Key Capabilities |
|---|---|---|
| **Organizer** | creates & owns a group; acts as its loan officer | create/approve loans, schedule + run meetings, record savings, execute share-out, invite members |
| Treasurer | delegated by organizer | record savings, repayments, fines, attendance |
| Chairperson | delegated | approve/reject loans, run meetings, initiate share-out |
| Secretary | delegated | meeting notes, action items |
| **Member** | any group participant | view own savings/loans, group summary, request loans, participate in votes |

> A user with **zero groups** lands on "create your first group / join with an invite code" — never rejected.

### Optional supervisory tier (opt-in, NOT the default identity)
| Persona | Role | Key Capabilities |
|---------|------|-----------------|
| David | MFI Field Officer | Read-only cross-group monitoring, reports |
| Sarah | NGO Program Manager | Read-only analytics, donor reports, program metrics |

## Success Metrics

- 50+ active groups onboarded within 6 months of launch
- 90% reduction in meeting duration vs paper-based workflow
- Zero record-keeping disputes in digitized groups
- 95% sync success rate on 2G/3G connections
- < 5 minute onboarding time for new group treasurer
- 100% data parity between local cache and Fineract backend after sync

## Scope

### In Scope (v1.0.0)
- **Global self-signup**: anyone downloads → self-registers → creates or joins a group (no back-office provisioning)
- **Single login/signup** screen with post-login capability auto-resolution (organizer vs member, per group)
- **Config-driven group types** — VSLA · ASCA · ROSCA · SILC · SHG · SACCO/Credit-Union · CBO/Village-Banking · Burial/Welfare-Society · JLG — extensible to ANY type via config (see `ARCHITECTURE.md`)
- **Pluggable distribution** — pro-rata share-out (VSLA/ASCA/SILC) · rotation payout (ROSCA) · auction/bid (chit/hui)
- **Invite members** via link/code
- Group creation, member onboarding, role assignment
- Meeting lifecycle (schedule, attendance, agenda) with enhanced step-by-step flow
- Dual savings: Group-Linked (mandatory, min/max enforced) + Individual (voluntary)
- Real-time corpus/fund balance tracking with excess outflow blocking
- Loan application, approval (with voting), disbursement, repayment
- Share-out calculation and distribution
- End-user personal dashboard with loan request capability
- Previous meeting review before starting new meeting
- Offline-first with SQLDelight local cache
- Sync engine for Mifos Fineract (batch API)
- Multi-language support (Swahili, French, Hindi, English)

### Out of Scope
- Mobile money integration (v2.0.0)
- Inter-group lending (v2.0.0)
- Credit scoring / ML risk assessment (v2.0.0)
- Web admin dashboard (v2.0.0)
- SMS notifications (v2.0.0)

## Platform & Technology

| Decision | Choice |
|----------|--------|
| Architecture | Clean Architecture + MVI/UDF |
| DI Framework | Koin |
| State Management | Compose State |
| Navigation | Voyager |
| Backend | Mifos Fineract |
| Local DB | SQLDelight |
| Platform Targets | Android, iOS, Desktop |

## Backend — Companion API (mcp-mifosx)

The app consumes a **Companion API** layer that sits between the KMP client and Apache Fineract Core.
This layer is implemented as an **extension of the existing `mcp-mifosx` Go server** — no Supabase, no
standalone DDD service.

**Why a companion layer?** Fineract's self-service scope grants only one privilege class. The companion
API bridges self-signed-up users into Fineract's office-scoped model (COMP-AUTH-001..003), orchestrates
group back-office operations with a service credential (COMP-GRP-001..005, COMP-CAL-001..003), and
provides generic datatable CRUD for all group-type state (COMP-DT-001..005, COMP-DIST-001/002).

### Build tiers (mcp-mifosx Go extension)

| Tier | Tools | What to build |
|---|---|---|
| **TIER-1** | COMP-AUTH-001..003, COMP-GRP-001..005, COMP-CAL-001..003 (9 tools) | Thin `BaseToolDef` wraps over existing Fineract endpoints in `go/tools/companion_*.go` |
| **TIER-2** | COMP-DT-001..005, COMP-DIST-001/002 (7 tools) | Generic datatable-CRUD + distribution-execute in `go/tools/datatables.go` |
| **P0 auth-model** | — | Per-call user credential + service-credential group orchestration (the one structural lift) |

### Companion datatables to provision (once at deploy)

`dt_group_type_config` · `dt_companion_invitations` · `dt_rosca_rotation` · `dt_rosca_auction` · `dt_vsla_cycle` · `dt_welfare_fund` (all attached to `m_group`)

### Deploy gate (external, blocks device-verify)

Until the companion API is built and deployed:
- Implemented features **compile + build-green**
- `/device-test` returns **`pending-device-verify`** (not a failure — the honest external gate)
- `matrix-green` is gated on this spec being executed

**Full spec**: `server-layer/COMPANION_API_BUILD_DEPLOY.md` · **Contracts**: `server-layer/API_CONTRACT.yaml` (companion section)

## Branding

| Element | Value |
|---------|-------|
| Display Name | MifosSave |
| Primary Color | #2E7D32 (Forest Green) |
| Accent Color | #FF8F00 (Amber) |
| Typography | Noto Sans (large scale) |
| Icon Style | Rounded |

---

> Generated from idea-plan.yaml | Last updated: 2026-05-03
