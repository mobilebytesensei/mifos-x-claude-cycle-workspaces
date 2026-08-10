# Fines Tracking — API Reference
**Feature**: fines-tracking | **Requirements**: FR-012, FR-020
**Backend**: Mifos Fineract REST API (custom datatables)

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /fineract-provider/api/v1/datatables/dt_meeting_record | Create meeting record including totalFinesCollected | BasicAuth |
| POST | /fineract-provider/api/v1/datatables/dt_meeting_attendance | Record per-member attendance with fineAmount | BasicAuth |

Fines are not posted as standalone Fineract transactions. They are embedded in meeting-record and attendance-record datatables and contribute to corpus tracking. The Fineract batch API (`POST /batches`) is used when submitting the full meeting online.

---

## Request / Response Details

### POST /datatables/dt_meeting_record

**Purpose**: Create the meeting record after wizard completes. `totalFinesCollected` includes attendance fines + loan penalty fines from meeting #4.

**Request Body (CreateMeetingRecordRequest)**:
```json
{
  "groupId": 7,
  "meetingNumber": 4,
  "actualDate": "06 May 2026",
  "openingCorpus": 12400,
  "closingCorpus": 13500,
  "totalSavingsCollected": 1000,
  "totalRepaymentsReceived": 0,
  "totalLoansDisbursed": 0,
  "totalFinesCollected": 150,
  "attendanceCount": 4,
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```

**totalFinesCollected breakdown (demo meeting #4)**:
- Mary Akinyi absent fine: KES 100
- Grace Mwangi late fine: KES 50
- Attendance fines total: KES 150
- Loan penalty fines: KES 0 (no overdue loans this meeting)
- **Total: KES 150**

**Response (DataTableEntryResponse)**:
```json
{
  "resourceId": 4,
  "resourceIdentifier": "dt_meeting_record_4"
}
```

**Errors**:
- 400: Validation error (e.g. closingCorpus < 0, missing required fields)
- 403: Forbidden — treasurer or chairperson role required
- 500: Queue entire meeting to SyncQueue

---

### POST /datatables/dt_meeting_attendance

**Purpose**: Record individual member attendance with fine amount. One call per member, posted sequentially (or as part of batch).

**Request Body (CreateAttendanceRequest) — per member**:

**Present member (no fine)**:
```json
{
  "meetingId": "meeting-7-4",
  "memberId": "101",
  "status": "PRESENT",
  "fineAmount": 0,
  "locale": "en"
}
```

**Late member (KES 50 fine)**:
```json
{
  "meetingId": "meeting-7-4",
  "memberId": "103",
  "status": "LATE",
  "fineAmount": 50,
  "locale": "en"
}
```

**Absent member (KES 100 fine)**:
```json
{
  "meetingId": "meeting-7-4",
  "memberId": "105",
  "status": "ABSENT",
  "fineAmount": 100,
  "locale": "en"
}
```

**Response (DataTableEntryResponse)**:
```json
{
  "resourceId": 201,
  "resourceIdentifier": "dt_meeting_attendance_201"
}
```

**Errors**:
- 400: Invalid status value or missing memberId
- 500: Queue this member's attendance to SyncQueue

---

## Corpus Impact of Fines

Fines increase the closing corpus balance. The closing corpus formula:

```
closingCorpus = openingCorpus
              + totalSavingsCollected
              + totalRepaymentsReceived
              + totalFinesCollected        ← fines boost corpus
              - totalLoansDisbursed
```

**Demo meeting #4**:
```
closingCorpus = 12,400 (opening)
              + 1,000  (savings: 4 members × ~KES 250 avg)
              + 0      (no repayments)
              + 150    (fines: 1 absent KES 100 + 1 late KES 50)
              - 0      (no disbursals)
              = 13,550
```

---

## DTOs

### CreateMeetingRecordRequest
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| groupId | Int | Yes | Fineract group ID |
| meetingNumber | Int | Yes | Sequential meeting number (1-indexed) |
| actualDate | String | Yes | "dd MMMM yyyy" format |
| openingCorpus | Long | Yes | KES at start of meeting (from dt_group_corpus) |
| closingCorpus | Long | Yes | KES at end: openingCorpus + collected - disbursed |
| totalSavingsCollected | Long | Yes | Sum of all mandatory savings deposits |
| totalRepaymentsReceived | Long | Yes | Sum of all loan repayments |
| totalLoansDisbursed | Long | Yes | Sum of approved + disbursed loan amounts |
| totalFinesCollected | Long | Yes | Sum of attendance fines + loan penalty fines |
| attendanceCount | Int | Yes | Number of PRESENT members |
| locale | String | Yes | "en" |
| dateFormat | String | Yes | "dd MMMM yyyy" |

### CreateAttendanceRequest
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| meetingId | String | Yes | "{groupId}-{meetingNumber}" composite key |
| memberId | String | Yes | Fineract client ID |
| status | String | Yes | "PRESENT", "LATE", or "ABSENT" |
| fineAmount | Long | Yes | 0 for PRESENT, 50 for LATE, 100 for ABSENT |
| locale | String | Yes | "en" |

### DataTableEntryResponse
| Field | Type | Description |
|-------|------|-------------|
| resourceId | Long | Auto-generated datatable row ID |
| resourceIdentifier | String | "{tableName}_{rowId}" |

### AttendanceStatus (enum)
| Value | Fine | Icon | Description |
|-------|------|------|-------------|
| PRESENT | 0 | checkmark (green) | Member arrived on time |
| LATE | 50 | clock (amber) | Member arrived late — fine applied |
| ABSENT | 100 | dismiss (red) | Member absent — fine applied |

### FineBreakdown (computed in ViewModel — not sent to API)
| Field | Type | Description |
|-------|------|-------------|
| attendanceFinesTotal | Long | Sum of all LATE (50) + ABSENT (100) fines |
| loanPenaltyFinesTotal | Long | Sum of treasurer-entered loan fines |
| totalFinesCollected | Long | attendanceFinesTotal + loanPenaltyFinesTotal |

---

## Demo Data — Meeting #4 Fines

**Group**: Mwangaza Women's Group (groupId=7, meeting #4, 06 May 2026)

### Attendance Records

| Member | memberId | Status | Fine |
|--------|----------|--------|------|
| Amara Diallo | 101 | PRESENT | KES 0 |
| Peter Otieno | 102 | PRESENT | KES 0 |
| Grace Mwangi | 103 | LATE | KES 50 |
| John Mwangi | 104 | PRESENT | KES 0 |
| Mary Akinyi | 105 | ABSENT | KES 100 |

**Attendance fines total: KES 150**
**Attendance count (PRESENT): 3**

### Loan Penalty Fines

| Loan | Member | Status | Penalty Fine |
|------|--------|--------|-------------|
| — | — | No overdue loans in demo | KES 0 |

**Loan penalty fines total: KES 0**

### totalFinesCollected: KES 150

### SyncQueue Entries (offline scenario)

When meeting #4 conducted offline, attendance records are queued:

| id | entity_type | payload_summary |
|----|------------|----------------|
| 4 | ATTENDANCE | memberId=103, status=LATE, fineAmount=50 |
| 5 | ATTENDANCE | memberId=105, status=ABSENT, fineAmount=100 |
| 6 | MEETING | totalFinesCollected=150, closingCorpus=13550 |
