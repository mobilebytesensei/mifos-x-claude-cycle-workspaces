# API — meeting-lifecycle
# MifosSave (mifos-x-group-banking) | Feature FR-003 / FR-019
# Generated: 2026-05-06

---

## Endpoints Table

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/centers/{centerId}/meetings | Fetch scheduled meetings for center | BasicAuth + Fineract-Platform-TenantId header |
| GET | /fineract-provider/api/v1/datatables/dt_meeting_record/{centerId} | Fetch completed meeting records from custom datatable | BasicAuth |
| GET | /fineract-provider/api/v1/centers/{centerId} | Fetch center detail including group members list | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Fetch opening corpus balance | BasicAuth |
| GET | /fineract-provider/api/v1/loans?groupId={groupId}&loanStatus=active | Fetch active loans for group members | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_loan_vote/{loanId} | Fetch vote tally for a pending loan application | BasicAuth |
| POST | /fineract-provider/api/v1/datatables/dt_meeting_record | Create meeting record (submit step 1 of 6) | BasicAuth |
| POST | /fineract-provider/api/v1/datatables/dt_meeting_attendance | Record per-member attendance (submit step 2 of 6) | BasicAuth |
| POST | /fineract-provider/api/v1/savingsaccounts/{savingsId}/transactions | Post savings deposit per member per type (submit step 3 of 6) | BasicAuth |
| POST | /fineract-provider/api/v1/loans/{loanId}/transactions?command=repayment | Record loan repayment (submit step 4 of 6) | BasicAuth |
| POST | /fineract-provider/api/v1/loans/{loanId}/transactions?command=disburse | Disburse approved loan (submit step 5 of 6) | BasicAuth |
| PUT | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Update corpus to closingCorpus (submit step 6 of 6) | BasicAuth |

---

## Request/Response Details

### GET /centers/{centerId}/meetings
**Path params:** centerId (Int)
**Query params:** fromDate (YYYY-MM-DD, optional), toDate (YYYY-MM-DD, optional)
**Response:** Array of MeetingListResponse objects
**Error handling:** 401 → redirect login; 404 → empty state; 5xx → cached data + error banner

### GET /datatables/dt_meeting_record/{centerId}
**Path params:** centerId (Int)
**Query params:** meetingNumber (Int, optional — used to fetch single previous meeting)
**Response:** MeetingRecordList or MeetingRecordDetail (single)
**Error handling:** 404 → no records yet, empty list; 5xx → error banner

### POST /datatables/dt_meeting_record
**Body:** CreateMeetingRecordRequest
**Response:** DataTableEntryResponse {resourceId: Long, resourceIdentifier: String}
**Error handling:** 400 → validation error snackbar; 5xx → queue entire meeting payload to SyncQueue

### POST /datatables/dt_meeting_attendance
**Body:** CreateAttendanceRequest
**Response:** DataTableEntryResponse
**Error handling:** 5xx → queue this member's attendance to SyncQueue

### POST /savingsaccounts/{savingsId}/transactions
**Path params:** savingsId (String)
**Body:** SavingsTransactionRequest
**Response:** SavingsTransactionResponse {officeId, savingsId, resourceId}
**Error handling:** 5xx → queue to SyncQueue

### POST /loans/{loanId}/transactions?command=repayment
**Path params:** loanId (String)
**Body:** LoanRepaymentRequest
**Response:** LoanTransactionResponse {officeId, loanId, resourceId}
**Error handling:** 5xx → queue to SyncQueue

### PUT /datatables/dt_group_corpus/{centerId}
**Path params:** centerId (Int)
**Body:** UpdateCorpusRequest
**Response:** DataTableEntryResponse
**Error handling:** 5xx → queue corpus update (highest priority in SyncQueue)

---

## DTOs

### MeetingListResponse
| Field | Type | Notes |
|-------|------|-------|
| meetingId | String | Unique meeting identifier |
| meetingNumber | Int | Sequential meeting number within group |
| meetingDate | String | Format: YYYY-MM-DD |
| status | MeetingStatus | Enum: UPCOMING, COMPLETED, MISSED |
| attendanceCount | Int? | Nullable — null for upcoming |
| totalCollectedKES | Long? | Nullable — null for upcoming |

### MeetingRecordDetail (dt_meeting_record row)
| Field | Type | Notes |
|-------|------|-------|
| meetingNumber | Int | |
| actualDate | String | dd MMMM yyyy |
| totalSavings | Long | Sum of group + individual savings |
| totalRepayments | Long | Sum of all loan repayments |
| totalLoansDisbursed | Long | Sum of approved loan disbursements |
| totalFinesCollected | Long | Late + absent fines total |
| closingCorpus | Long | Computed closing corpus balance |
| attendanceCount | Int | Number present (including late) |

### CreateMeetingRecordRequest
| Field | Type | Default |
|-------|------|---------|
| centerId | Int | from nav params |
| meetingNumber | Int | from nav params |
| actualDate | String | today |
| openingCorpus | Long | from dt_group_corpus |
| closingCorpus | Long | computed |
| totalSavingsCollected | Long | runningSavingsTotal |
| totalRepaymentsReceived | Long | totalRepayments |
| totalLoansDisbursed | Long | totalLoansDisbursed |
| totalFinesCollected | Long | totalFinesCollected |
| attendanceCount | Int | present + late count |
| locale | String | "en" |
| dateFormat | String | "dd MMMM yyyy" |

### CreateAttendanceRequest
| Field | Type | Values |
|-------|------|--------|
| meetingId | String | |
| memberId | String | |
| status | String | PRESENT, LATE, ABSENT |
| fineAmount | Long | 0 / 50 / 100 |
| locale | String | "en" |

### SavingsTransactionRequest
| Field | Type | Notes |
|-------|------|-------|
| transactionDate | String | dd MMMM yyyy |
| transactionAmount | Long | groupAmount or individualAmount |
| paymentTypeId | Int | 1 = Cash |
| locale | String | "en" |
| dateFormat | String | "dd MMMM yyyy" |

### UpdateCorpusRequest
| Field | Type | Notes |
|-------|------|-------|
| corpusBalance | Long | closingCorpus value |
| lastUpdatedMeeting | Int | meetingNumber |
| lastUpdatedDate | String | today |
| locale | String | "en" |
| dateFormat | String | "dd MMMM yyyy" |

### CorpusRecord (GET response)
| Field | Type | Notes |
|-------|------|-------|
| centerId | Int | |
| corpusBalance | Long | Current corpus = openingCorpus for new meeting |
| cashOnHand | Long | Physical cash held by treasurer |
| lastUpdatedMeeting | Int | Last meeting number that updated corpus |
| lastUpdatedDate | String | |
