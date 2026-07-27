<!--
  generated_from_feature: meeting-calendar
  contract_version: "2.0.0"
  source: idea-layer/screens/meeting-calendar/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Meeting Calendar — API Contract

## Endpoints (2)

| ID | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|
| `get_center_meetings` | GET | `/fineract-provider/api/v1/centers/{centerId}/meetings` | BasicAuth | no |
| `get_meeting_records_datatable` | GET | `/fineract-provider/api/v1/datatables/dt_meeting_record/{centerId}` | BasicAuth | no |

Read-only. No money moves — Fineract is the system of record.

## Request / Response Details

### GET /centers/{centerId}/meetings

**Path params:** `centerId: Int`. **Query params:** `fromDate: YYYY-MM-DD`, `toDate: YYYY-MM-DD`.
**Response:** `MeetingListResponse`.
**Errors:** 401 → redirect login · 404 → show empty state · 5xx → show error banner, use cached data.

### GET /datatables/dt_meeting_record/{centerId}

**Path params:** `centerId: Int`. **Response:** `MeetingRecordList` (completed meeting records with
collected amounts). **Errors:** 404 → no records yet, continue with empty list.

## DTOs

### MeetingListResponse
```
meetingId: String
meetingNumber: Int
meetingDate: String (YYYY-MM-DD)
status: MeetingStatus
attendanceCount: Int?
totalCollectedKES: Long?
```

### MeetingRecordList
```
centerId: Int
records: List<MeetingRecordItem>
```

### MeetingRecordItem
```
meetingNumber: Int
actualDate: String
totalSavings: Long
totalRepayments: Long
attendanceCount: Int
closingCorpus: Long
```

### MeetingListItem
```
meetingId: String
meetingNumber: Int
meetingDate: String
status: MeetingStatus
attendanceCount: Int?
totalCollectedKES: Long?
```

### MeetingStatus (enum)
```
UPCOMING | COMPLETED | MISSED
```

### ViewMode (enum)
```
LIST | CALENDAR
```

## Dependencies

- Services: `MeetingRepository`, `NavigationManager`, `ConnectivityObserver`, `LocalMeetingDao`
- Features: `meeting-conduct`, `previous-meeting-review`

## Cache Strategy

`stale-while-revalidate`; offline `show_cached_data`. Cached via SQLDelight, gated by
`cmp-network-monitor` for live refresh.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `401 Unauthorized` | Redirect to login |
| `404 NotFound` (meetings) | Empty state |
| `404 NotFound` (records) | Continue with empty records list |
| `5xx Server` / offline | Error banner over cached data; Retry re-fetches network-first |
