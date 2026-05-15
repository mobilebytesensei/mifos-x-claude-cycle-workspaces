# User Flows — mifos-x-group-banking

## Critical Flows

### 1. Admin Auth → Dashboard
login → client-type-selector → admin-dashboard
- Biometric / PIN shortcut skips username/password
- Client type persisted — next launch skips selector

### 2. Meeting Conduct (Full)
meeting-calendar → meeting-conduct → meeting-summary
- Record attendance first (gate: all members marked before savings)
- Collect savings per member (amount input)
- Review agenda items
- Submit → creates Fineract meeting record + attendance records + savings transactions

### 3. Loan Apply → Approval
loan-list → loan-apply → (chairperson approval) → loan-detail
- End user loan request goes through dt_loan_request custom datatable
- Admin sees pending requests on admin-dashboard
- Chairperson approves via loan-detail → loan-apply confirmation

### 4. Share-Out Cycle
group-dashboard → share-out-preview → share-out-execute
- Preview shows per-member pro-rata calculations
- Execute is irreversible — biometric confirmation required
- Withdraws from group savings account, records in dt_share_out

### 5. Member Onboarding
member-list → member-add → (optional) member-profile
- POST /clients → assign to group → set role in dt_member_role
- Photo capture optional
- Offline: queued in SyncQueue, synced on next connectivity

## Medium Priority Flows

### 6. Loan Repayment
loan-list → loan-detail → loan-repayment-dialog
- Cash payment recorded by treasurer
- Updates loan outstanding balance
- Offline: queued

### 7. Offline Sync
sync-status → (retry / resolve conflict)
- Shows pending items from SyncQueue
- Retry individual failed items
- Conflict resolution: server wins by default, flag for user review
