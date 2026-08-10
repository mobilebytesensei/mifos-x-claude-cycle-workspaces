<!--
  generated_from_feature: meeting-conduct
  contract_version: "2.0.0"
  source: idea-layer/screens/meeting-conduct/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Meeting Conduct — API Contract

## Endpoints (11 — 5 read, 6 write)

Base path: `/fineract-provider/api/v1` · Auth BasicAuth · Tenant `X-Fineract-Platform-TenantId: default`.

### Read (screen_init parallel load)

| ID | Method | Endpoint | Errors |
|---|---|---|---|
| `get_previous_meeting_record` | GET | `/datatables/dt_meeting_record/{groupId}` | 404 first-meeting placeholder · 401 login · 5xx continue empty |
| `get_group_members` | GET | `/groups/{groupId}` | 404 block advance (members required) · 401 login |
| `get_group_corpus` | GET | `/datatables/dt_group_corpus/{groupId}` | 404 default 0 · 5xx warning chip |
| `get_active_loans` | GET | `/loans?loanStatus=active` | 404 empty step 4 · 5xx error chip |
| `get_loan_votes` | GET | `/datatables/dt_loan_vote/{loanId}` | 404 no votes (0/0) |

`get_previous_meeting_record` params: `groupId` (nav_params), `meetingNumber` (computed = current − 1).
`get_active_loans` param: `groupId` (nav_params).

### Write (ordered submit sequence — sync_queue priority in parentheses)

| ID | Method | Endpoint | Body DTO | Offline op (priority) |
|---|---|---|---|---|
| `post_meeting_record` | POST | `/datatables/dt_meeting_record` | CreateMeetingRecordRequest | CREATE_MEETING_RECORD (1) |
| `post_meeting_attendance` | POST | `/datatables/dt_meeting_attendance` | CreateAttendanceRequest | CREATE_MEETING_ATTENDANCE (2) |
| `post_savings_transaction` | POST | `/savingsaccounts/{savingsId}/transactions` | SavingsTransactionRequest | POST_SAVINGS_TRANSACTION (3) |
| `post_loan_repayment` | POST | `/loans/{loanId}/transactions?command=repayment` | LoanRepaymentRequest | POST_LOAN_REPAYMENT (4) |
| `post_loan_disbursal` | POST | `/loans/{loanId}/transactions?command=disburse` | LoanDisbursalRequest | POST_LOAN_DISBURSAL (5) |
| `patch_corpus` | PUT | `/datatables/dt_group_corpus/{groupId}` | UpdateCorpusRequest | UPDATE_CORPUS (6) |

Write errors: 400 validation snackbar · 5xx → queue that item to `sync_queue`. Disbursal 400 means
the corpus gate should have blocked it (log + error).

## DTOs

### Read models
```
MeetingRecordDetail { meetingNumber, actualDate, totalSavings, totalRepayments,
  totalLoansDisbursed, totalFinesCollected, closingCorpus, attendanceCount }
GroupDetail { id, name, groups: List<GroupSummary>, activeClientMembers: List<ClientMember> }
CorpusRecord { groupId, corpusBalance, cashOnHand, lastUpdatedMeeting, lastUpdatedDate }
LoanListResponse { totalFilteredRecords, pageItems: List<LoanDetail> }
LoanDetail { loanId, clientId, clientName, principal, outstandingBalance, isOverdue,
  weekNumber, numberOfRepayments, expectedWeeklyRepayment }
LoanVoteRecord { loanId, votesFor, votesAgainst, votesAbstain }
```

### Submit request DTOs
```
CreateMeetingRecordRequest { groupId, meetingNumber, actualDate, openingCorpus, closingCorpus,
  totalSavingsCollected, totalRepaymentsReceived, totalLoansDisbursed, totalFinesCollected,
  attendanceCount, locale="en", dateFormat="dd MMMM yyyy" }
CreateAttendanceRequest { meetingId, memberId, status ∈ {PRESENT,LATE,ABSENT}, fineAmount, locale="en" }
SavingsTransactionRequest { transactionDate, transactionAmount, paymentTypeId (1=Cash), locale, dateFormat }
LoanRepaymentRequest { transactionDate, transactionAmount, paymentTypeId, locale, dateFormat }
LoanDisbursalRequest { actualDisbursementDate, note, locale, dateFormat }
UpdateCorpusRequest { corpusBalance, lastUpdatedMeeting, lastUpdatedDate, locale, dateFormat }
DataTableEntryResponse { resourceId, resourceIdentifier }
```

### View-state models
```
GroupMember { memberId, name, initials, role }
AttendanceStatus = PRESENT | LATE | ABSENT
SavingsEntry { memberId, groupAmount, individualAmount }
SavingsType = GROUP_LINKED | INDIVIDUAL
LoanSummary { loanId, memberId, memberName, memberInitials, principal, outstandingBalance,
  isOverdue, weekNumber, expectedWeeklyRepayment }
LoanApplication { id, memberId, memberName, requestedAmount, purpose }
LoanVote = FOR | AGAINST | ABSTAIN
PreviousMeetingSummary { meetingNumber, date, totalCollected, corpusAtClose, attendanceCount }
```

## Repository Contract

- `MeetingRepository`: getPreviousMeetingRecord, createMeetingRecord, recordAttendance
- `SavingsRepository`: postSavingsTransaction
- `LoanRepository`: getActiveLoans, getLoanVotes, postRepayment, disburse
- `CorpusRepository`: getCorpus, updateCorpus
- `SyncQueueRepository`: enqueue

## Offline Behaviour

When `ConnectivityObserver` / `cmp-network-monitor` reports offline (or any submit call returns
5xx), the full ordered payload is enqueued to the SQLDelight `sync_queue` with the priorities
above (keyed by `meeting_id`); the UI shows an optimistic success and navigates to meeting-summary
from cached data. Store5 drains the queue in priority order on reconnect. Wizard progress is
persisted to `meeting_wizard_state` on each step advance so an interrupted meeting resumes.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `AttendanceIncomplete` | Step 1 gate — block advance |
| `MinContributionNotMet` | Step 3 gate — block advance |
| `RepaymentExceedsBalance` | Step 4 gate — block advance |
| `CorpusInsufficient` | Step 5 corpus gate — block disbursal |
| `400 Validation` | Validation snackbar |
| `401 Unauthorized` | Redirect to login |
| `5xx Server` / offline | Enqueue to sync_queue; optimistic success + offline toast |
