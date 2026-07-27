<!--
  generated_from_feature: meeting-summary
  contract_version: "2.0.0"
  source: idea-layer/screens/meeting-summary/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Meeting Summary — API Contract

## Endpoints (1)

| ID | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|
| `get_meeting_record` | GET | `/fineract-provider/api/v1/datatables/dt_meeting_record/{centerId}` | BasicAuth | no |

Read-only. Totals + corpus were reconciled at close by the collection-sheet companion; this screen
never moves money.

## Request / Response Details

### GET /datatables/dt_meeting_record/{centerId}

**Path params:** `centerId: Int`. **Query params:** `meetingNumber: Int`.
**Response:** `MeetingRecordDetail`.
**Errors:** 404 → show cached data or error state · 5xx → show error banner.

**Cache:** Store5 stale-while-revalidate over SQLDelight, keyed by center/meeting.

## DTOs

### MeetingRecordDetail
```
meetingId: String
meetingNumber: Int
actualDate: String (dd MMMM yyyy)
attendanceCount: Int
totalMemberCount: Int
groupSavingsCollected: Long
individualSavingsCollected: Long
totalSavingsCollected: Long
loansDisbursed: Long
loansRepaid: Long
finesCollected: Long
openingCorpus: Long
closingCorpus: Long
savingsBreakdown: List<SavingsBreakdownItem>
loanItems: List<LoanSummaryItem>
```

### SavingsBreakdownItem
```
memberId: String
memberName: String
groupSavings: Long
individualSavings: Long
```

### LoanSummaryItem
```
memberId: String
memberName: String
amountDisbursed: Long
amountRepaid: Long
outstandingAfter: Long
```

## Dependencies

- Services: `MeetingRepository`, `ShareManager`, `NavigationManager`, `LocalMeetingDao`
- Features: `meeting-conduct` (entry), `meeting-calendar` (exit)

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `404 NotFound` | Show cached data or Error state |
| `5xx Server` | Error banner (`LoadFailed` — "Showing cached data") |

## Share Behaviour

The share action generates a text/PDF report from the loaded `MeetingRecordDetail` (totals,
savings breakdown, opening/closing corpus) and opens the OS share sheet via kmpToolkit/FileKit;
`isSharing` toggles while composing. No copy is retained after dismissal.
