# CommonPurse - Mifos X Group Banking

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

CommonPurse digitizes the full lifecycle of self-funded community banking groups — meetings, savings, lending, and share-out — with offline-first KMP and Mifos Fineract backend.

## Problem Statement

Millions of people in emerging markets organize into community savings groups (VSLA, ROSCA, ASCA, SHG) to pool savings, issue loans, and distribute profits. These groups operate with paper ledgers, leading to record-keeping errors, fraud, limited transparency, and inability to scale. Existing digital solutions are either online-only, lack Fineract integration, or don't support the full group lifecycle.

## Solution

CommonPurse provides a Kotlin Multiplatform mobile app that digitizes every step of the community banking lifecycle — from group creation and member onboarding, through meeting-driven savings collection and loan disbursement, to periodic share-out — all working offline-first with automatic sync to Mifos Fineract when connectivity is available.

## Core Value Propositions

1. **Offline-first**: full functionality without internet — sync when connected
2. **Meeting-centric workflow**: mirrors how real groups operate (attendance -> savings -> loans -> decisions)
3. **Fineract-backed**: enterprise-grade financial record-keeping via proven open-source core banking
4. **Low-literacy UX**: icon-heavy, minimal text, voice prompts, large touch targets
5. **Transparent**: every member can see group balances, loan status, and share-out projections in real-time

## Target Users

### Admin Client (Staff Auth)
| Persona | Role | Key Capabilities |
|---------|------|-----------------|
| Amina | Group Treasurer / Secretary | Record savings (group-linked + individual), track loans, calculate share-out, mark attendance |
| Joseph | Group Chairperson | Conduct meetings, approve/reject loans, initiate share-out, manage group parameters |
| David | MFI Field Officer | Read-only cross-group monitoring, force sync, reports |
| Sarah | NGO Program Manager | Read-only analytics, donor reports, program metrics |

### End User Client (Self-Service Auth)
| Persona | Role | Key Capabilities |
|---------|------|-----------------|
| Grace | Regular Group Member | View own savings/loans (group-linked + individual), group summary, request loans, see share-out projection |

> **Two client types**: Admin (manages groups via staff auth) vs End User (sees own data via self-service auth). Different navigation graphs, different screens, different permissions.

## Success Metrics

- 50+ active groups onboarded within 6 months of launch
- 90% reduction in meeting duration vs paper-based workflow
- Zero record-keeping disputes in digitized groups
- 95% sync success rate on 2G/3G connections
- < 5 minute onboarding time for new group treasurer
- 100% data parity between local cache and Fineract backend after sync

## Scope

### In Scope (v1.0.0)
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

## Branding

| Element | Value |
|---------|-------|
| Display Name | CommonPurse |
| Primary Color | #2E7D32 (Forest Green) |
| Accent Color | #FF8F00 (Amber) |
| Typography | Noto Sans (large scale) |
| Icon Style | Rounded |

---

> Generated from idea-plan.yaml | Last updated: 2026-05-03
