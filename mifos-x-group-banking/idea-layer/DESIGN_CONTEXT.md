# Design Context — MifosSave (mifos-x-group-banking)

> Authoritative design brief for all MifosSave screens, enrichment, and mockup generation.
> Source of truth: `idea-layer/design-tokens.yaml` + `idea-layer/training/TRAINING_MASTER.yaml`

---

## App Identity

**MifosSave** is a community savings group management app built on Apache Fineract (Mifos X).
Its tagline — *"Your community savings group"* — reflects the mission: bring transparent,
trustworthy financial tooling to VSLA (Village Savings and Loan Association) groups, rotating
savings groups, and field-officer-managed microfinance clusters in emerging markets.

Primary users are rural communities in East Africa, South Asia, and West Africa who operate
savings groups with 10–30 members. Meetings happen weekly or bi-weekly. Cash is physical.
Connectivity is intermittent. Trust is everything.

---

## Two Client Types

### Admin Client (Group Treasurer / Chairperson / Field Officer)
- Authenticates via Fineract staff endpoint (`POST /authentication`)
- Full group management: create groups, onboard members, conduct meetings, manage loans
- Home screen: `admin-dashboard` — corpus balance, meeting countdown, pending loans
- Elevated trust: can disburse loans, execute share-out, mark defaults

### End User Client (Group Member — Self-Service)
- Authenticates via Fineract self-service endpoint (`POST /self/authentication`)
- Read-only group view: personal savings, personal loans, loan requests
- Home screen: `personal-dashboard` — individual balance, loan status, next meeting
- Limited scope: can submit loan requests, view attendance, check share-out allocation

---

## Design Principles

### 1. Offline-First
Network is unreliable in the field. Every screen must render from local Room cache. Mutations
queue in `dt_sync_metadata` and sync when connectivity resumes. The `sync-status` screen is
always reachable. Sync state indicators appear on admin-dashboard and field-officer-dashboard.

### 2. Data Density — Purposeful
Meetings collect data from 10–30 members in a single session. Forms must be compact and
fast to scan without sacrificing legibility. Use table-style list tiles, not card-heavy layouts,
for multi-member data entry (attendance rows, savings collection inputs).

### 3. Rural UX — Large Targets, Simple Flows
- Minimum 48dp touch targets; 56dp preferred for primary actions
- Maximum 3 steps to complete any primary user task
- No swipe-to-delete, no multi-select, no drag-and-drop — motor imprecision in field conditions
- Confirmation dialogs for destructive actions (defaults, share-out execution, logout)

### 4. Trust Through Transparency
- Every financial transaction shows amount + member name + timestamp
- Corpus balance is always visible in admin context (group_cycle_header)
- Loan disbursement is blocked when corpus is insufficient — never silently fails
- Share-out flow is 2-step: preview (read) → execute (confirm) — no accidental distribution

---

## Color System

| Role | Hex | Usage |
|------|-----|-------|
| Primary / Green | `#2E7D32` | Savings, deposits, success states, CTAs, top bars |
| Primary Container | `#A6F1A6` | Success chips, positive balance backgrounds |
| Secondary / Amber | `#FF8F00` | Warnings, loan overdue indicators, pending states |
| Tertiary / Blue | `#1565C0` | Navigation, informational banners, field-officer accents |
| Error / Red | `#BA1A1A` | Defaults, errors, destructive action confirmation |
| Surface | `#FFFBFE` | Card backgrounds, list backgrounds |
| On-Surface-Variant | `#49454F` | Sublabels, secondary text |

**Contrast Rule**: All text on primary (#2E7D32) background must use `#FFFFFF` (onPrimary).
Outdoor use — WCAG AAA (7:1) preferred, WCAG AA (4.5:1) minimum for all body text.

---

## Typography — Noto Sans

Noto Sans is chosen for broad language coverage: English, Swahili (sw), French (fr), Hindi (hi).
All four are supported at runtime via composable-tree restart on language change.

| Token | Size | Weight | Use |
|-------|------|--------|-----|
| displaySmall | 36sp | 400 | Corpus balance hero |
| headlineMedium | 28sp | 400 | Screen titles |
| titleLarge | 22sp | 500 | Section headers |
| titleMedium | 16sp | 500 | Card titles, member names |
| bodyLarge | 16sp | 400 | List item primary text |
| bodyMedium | 14sp | 400 | List item secondary text |
| labelLarge | 14sp | 500 | Button labels, tab labels |
| labelSmall | 11sp | 500 | Chips, badges, status indicators |

---

## Key Interaction Patterns

### Corpus Card Blocking Pattern
`group-dashboard` shows corpus balance as a `corpus_balance_card`. If corpus < requested loan
amount, the "Disburse Loan" FAB is disabled with tooltip: "Insufficient corpus fund". This
prevents over-disbursement. Corpus is updated in real-time from `dt_group_corpus`.

### Meeting Conduct Multi-Step Form
`meeting-conduct` is the most complex screen: attendance → savings collection → loan votes →
loan repayments → meeting close. Progress is tracked by step index. Each step auto-saves to
local DB before advancing. Meeting can be paused and resumed (offline-safe).

### Share-Out Two-Step Preview + Execute
`share-out-preview` renders the distribution matrix (member → share amount) read-only.
`share-out-execute` requires explicit "Execute Share-Out" confirmation with amount summary.
Cannot be undone after execution — confirmation dialog emphasizes finality.

### Loan Approval Voting
Loans require democratic approval: `dt_loan_vote` records each member's for/against vote.
Chairperson approval is a separate gate. `loan-apply` shows live vote tally. Admin can only
disburse when quorum is met and chairperson has approved.

### Offline Sync Queue
All mutations (deposits, attendance, loan votes) are written to local Room first, then enqueued
in `dt_sync_metadata`. `sync-status` screen shows pending operations count, last sync time,
and conflict resolution status. Background sync runs on WiFi or mobile data availability.

---

## Accessibility — Outdoor Use Profile

- **Touch targets**: 48dp minimum, 56dp for financial transaction inputs
- **Contrast**: WCAG AAA (7:1) for primary text on all backgrounds
- **Font scaling**: All text in sp (scales with system font size)
- **Screen reader**: All interactive elements have `contentDescription` mapped to `label_source`
- **Color-blind safe**: Never rely on color alone — always pair with icon + label
- **Glare resistance**: Avoid pure white (#FFFFFF) large surfaces — use `surface` token (#FFFBFE)
  or `surface_container` for card backgrounds

---

> Generated by /idea-migration reference | 2026-05-08
> Applies to: all 30 screens across 15 features
