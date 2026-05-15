# _deferred — Planned Future Screens

This directory holds candidate screens that are planned for CommonPurse but have not yet been enriched or scaffolded into `screens/`. They represent the product roadmap beyond the current MVP cycle.

## How to Promote a Deferred Screen

1. Run `/idea add` to scaffold `screens/{id}/ui.yaml` from this backlog.
2. Run `/idea-enrich {id}` to enrich the new screen.
3. Move it from this list to `FEATURES.md` and the appropriate `flow.yaml`.
4. Delete the entry from this file.

---

## Candidate Future Screens

### 1. `loan-calculator`
**Purpose**: Interactive amortization calculator that lets members simulate weekly repayment amounts for a given principal, interest rate, and loan term before applying.
**Role**: End User + Admin
**Priority**: P1 — reduces incorrect loan applications at the meeting table.

### 2. `group-analytics-dashboard`
**Purpose**: Charts showing group savings growth over time, loan repayment performance, member retention, and cycle-over-cycle trends. Exports a PDF summary.
**Role**: Admin (field officer, chairperson)
**Priority**: P1 — critical for group health reviews and donor reporting.

### 3. `member-profile-edit`
**Purpose**: Edit a member's personal details (name, phone, national ID, next-of-kin) without removing and re-adding them to the group.
**Role**: Admin (field officer, secretary)
**Priority**: P1 — member data changes frequently; currently requires Fineract web UI.

### 4. `push-notification-settings`
**Purpose**: Granular notification preferences per event type (meeting reminder, loan due, sync complete, share-out ready). Respects Android notification channels.
**Role**: All
**Priority**: P2 — current settings screen only has a single toggle; fine-grained control improves retention.

### 5. `group-audit-log`
**Purpose**: Chronological activity log of all actions taken in a group (deposits, withdrawals, loan approvals, share-out, member additions). Filterable by actor and date range.
**Role**: Admin (chairperson, field officer)
**Priority**: P2 — transparency requirement for formal VSLA groups; supports dispute resolution.

### 6. `bulk-loan-approval`
**Purpose**: Batch screen listing all pending loan requests for a group meeting, allowing the chairperson to approve or reject multiple requests in a single confirmation flow.
**Role**: Admin (chairperson)
**Priority**: P2 — speeds up loan vote recording during meetings with multiple requests.

### 7. `repayment-schedule-export`
**Purpose**: View and export (PDF/CSV) the full repayment schedule for an active loan, including past payments, upcoming due dates, and outstanding balance.
**Role**: End User + Admin
**Priority**: P2 — frequently requested by members for personal budgeting.

### 8. `center-overview`
**Purpose**: Field officer view showing all groups in a center with aggregate KPIs: total corpus, overdue loans, attendance rate, last meeting date.
**Role**: Admin (field officer)
**Priority**: P1 — field officers manage 5-20 groups; the current admin-dashboard shows only one group at a time.
