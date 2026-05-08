# Member Onboarding — API Contract

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /groups/{groupId}/clients | Fetch paginated list of members belonging to the group | Bearer token |
| GET | /clients/{clientId} | Fetch full client (member) profile from Fineract | Bearer token |
| GET | /clients/{clientId}/accounts | Fetch savings and loan accounts for the member | Bearer token |
| GET | /datatables/dt_member_role/{clientId} | Fetch member's assigned role from custom datatable | Bearer token |
| PUT | /datatables/dt_member_role/{clientId} | Update member's role in the dt_member_role datatable | Bearer token (chairperson only) |
| POST | /clients | Create a new Fineract client (group member) | Bearer token |
| POST | /datatables/dt_member_role/{clientId} | Write member's role to custom datatable | Bearer token |
| POST | /clients/{clientId}/images | Upload member profile photo (multipart/form-data) | Bearer token |

---

## Request / Response Details

### get_group_members

**Request**
```
GET /groups/{groupId}/clients
Path params:
  groupId: Long (required, from nav params)
Query params:
  limit: Int = 20
  offset: Int = 0 (increments by 20 per page)
```

**Response**
```json
{
  "totalFilteredRecords": 5,
  "pageItems": [
    {
      "id": 1001,
      "displayName": "Amina Wanjiru",
      "status": { "id": 300, "value": "Active" },
      "mobileNo": "+254712345678",
      "imagePresent": false,
      "savingsAccountBalance": 3500.00,
      "loanStatus": "NONE"
    },
    {
      "id": 1002,
      "displayName": "Joseph Kamau",
      "status": { "id": 300, "value": "Active" },
      "mobileNo": "+254798765432",
      "imagePresent": false,
      "savingsAccountBalance": 4200.00,
      "loanStatus": "ACTIVE"
    }
  ]
}
```

**Errors**
- 401: Unauthorized — redirect to login
- 403: Forbidden — insufficient permissions
- 404: Group not found — navigate back with snackbar
- 500: Server error — show retry

**Pagination**: offset-based, 20 per page. `hasMorePages = offset + pageItems.size < totalFilteredRecords`

**Cache**: TTL 120s, stale-while-revalidate. Offline: show cached member list.

---

### get_client

**Request**
```
GET /clients/{clientId}
Path params:
  clientId: Long (required, from nav params)
```

**Response**
```json
{
  "id": 1001,
  "displayName": "Amina Wanjiru",
  "firstname": "Amina",
  "lastname": "Wanjiru",
  "mobileNo": "+254712345678",
  "emailAddress": null,
  "activationDate": [2026, 1, 15],
  "imagePresent": false,
  "officeId": 1,
  "status": { "id": 300, "value": "Active" }
}
```

**Errors**: 401, 404 (member not found), 500

**Cache**: TTL 300s, stale-while-revalidate

---

### get_client_accounts

**Request**
```
GET /clients/{clientId}/accounts
Path params:
  clientId: Long (required)
```

**Response**
```json
{
  "savingsAccounts": [
    {
      "id": 2001,
      "productName": "Group Savings",
      "accountBalance": 3500.00,
      "accountNo": "GS-0001",
      "status": { "id": 300, "value": "Active" }
    }
  ],
  "loanAccounts": []
}
```

**Active loan with arrears example**:
```json
{
  "loanAccounts": [
    {
      "id": 3001,
      "productName": "Group Loan",
      "loanBalance": 2000.00,
      "accountNo": "GL-0001",
      "status": { "id": 300, "value": "Active" },
      "inArrears": true
    }
  ]
}
```

**Errors**: 401, 404, 500

**Cache**: TTL 120s, stale-while-revalidate

---

### get_member_role

**Request**
```
GET /datatables/dt_member_role/{clientId}
Path params:
  clientId: Long (required)
```

**Response**
```json
{
  "role": "TREASURER",
  "assignedDate": "2026-01-15"
}
```

**Errors**
- 401: Unauthorized
- 404: Role not set — default app to MEMBER role (not an error in UI)
- 500: Server error

**Cache**: TTL 300s, stale-while-revalidate

---

### update_member_role

**Request**
```
PUT /datatables/dt_member_role/{clientId}
Path params:
  clientId: Long (required, from nav params)
Body (application/json):
{
  "role": "CHAIRPERSON"
}
```

**Valid role values**: CHAIRPERSON, TREASURER, SECRETARY, MEMBER

**Response**
```json
{ "resourceId": 1001 }
```

**Errors**
- 400: Invalid role value — inline error in sheet
- 401: Unauthorized
- 403: Forbidden — current user is not chairperson of this group
- 500: Server error — snackbar with retry option

**No offline queue** — role updates are online-only (requires chairperson auth check server-side)

---

### create_client

**Request**
```
POST /clients
Body (application/json):
{
  "firstname": "Grace",
  "lastname": "Achieng",
  "mobileNo": "+254723456789",
  "active": true,
  "activationDate": "06 May 2026",
  "officeId": 1,
  "groupId": 50,
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```

**Field notes**:
- `mobileNo`: Must match regex `^(\+254|0)[7][0-9]{8}$` (Kenyan E.164 or local format)
- `officeId`: Derived from the group's office (fetched from group details)
- `groupId`: Fineract Group ID (NOT Center ID — Fineract Groups are the sub-entity of Centers for client membership)
- `activationDate`: Current date at time of submission

**Response**
```json
{
  "resourceId": 1006,
  "clientId": 1006
}
```

**Errors**
- 400: Validation error (invalid fields or duplicate phone number)
  - Duplicate phone: surfaced as `PhoneAlreadyExists` error with inline field error
- 401: Unauthorized
- 403: Forbidden — only admin can create clients
- 500: Server error

**Offline Queue**: table `sync_queue`, operation `CREATE_MEMBER`.
Payload JSON includes all body fields + groupId. Retried with exponential backoff.

---

### assign_member_role

**Request**
```
POST /datatables/dt_member_role/{clientId}
Path params:
  clientId: Long (from create_client response.resourceId)
Body (application/json):
{
  "role": "SECRETARY",
  "groupId": 50,
  "assignedDate": "2026-05-06"
}
```

**Response**
```json
{ "resourceId": 1006 }
```

**Errors**: 400, 401, 500

**Offline Queue**: operation `ASSIGN_MEMBER_ROLE`. Chained after CREATE_MEMBER completes.

---

### upload_photo

**Request**
```
POST /clients/{clientId}/images
Path params:
  clientId: Long (from create_client response)
Content-Type: multipart/form-data
Body:
  file: <binary JPEG/PNG, max 2MB>
```

**Response**
```json
{ "resourceId": 1006 }
```

**Errors**
- 400: File too large (max 2MB) — show inline error "Photo must be smaller than 2 MB"
- 401: Unauthorized
- 500: Server error

**Offline Queue**: operation `UPLOAD_MEMBER_PHOTO`. Chained after ASSIGN_MEMBER_ROLE completes.
Photo URI stored locally until sync.

**Condition**: Only called when `photoUri != null`. If no photo is selected, this step is skipped entirely.

---

## DTOs

### Member
| Field | Type | Notes |
|-------|------|-------|
| id | String | Internal app ID |
| fineractClientId | Long | Maps to Fineract Client.id |
| displayName | String | Full display name (e.g. "Amina Wanjiru") |
| photoUri | String? | Local URI or Fineract image URL; null if no photo |
| role | MemberRole | CHAIRPERSON, TREASURER, SECRETARY, or MEMBER |
| savingsBalance | Double | KES current savings account balance |
| loanStatus | LoanStatus | ACTIVE, NONE, or OVERDUE |

### MemberRole
| Value | Display | Color (list chip) | Color (profile chip) |
|-------|---------|-------------------|---------------------|
| CHAIRPERSON | Chairperson | bg=#A6F1A6, text=#002106 | bg=#2E7D32, text=#FFFFFF |
| TREASURER | Treasurer | bg=#FFDDB3, text=#2A1700 | bg=#FF8F00, text=#FFFFFF |
| SECRETARY | Secretary | bg=#D2E4FF, text=#001C39 | bg=#1565C0, text=#FFFFFF |
| MEMBER | Member | bg=#DEE5DA, text=#424942 | bg=#DEE5DA, text=#424942 |

### LoanStatus
| Value | Badge Color |
|-------|------------|
| ACTIVE | bg=#C8E6C9, text=#1B5E20 |
| NONE | bg=#DEE5DA, text=#424942 |
| OVERDUE | bg=#FFCDD2, text=#B71C1C |

### MemberAccounts
| Field | Type | Notes |
|-------|------|-------|
| savingsBalance | Double | KES total savings balance |
| savingsAccountNo | String | Account number |
| savingsHistory | List\<SavingsDataPoint\> | List of date+balance for sparkline |
| activeLoan | ActiveLoanSummary? | null if no active loan |

### ActiveLoanSummary
| Field | Type | Notes |
|-------|------|-------|
| loanId | Long | Fineract loan ID |
| productName | String | e.g. "Group Loan" |
| principalAmount | Double | KES original principal |
| outstandingBalance | Double | KES remaining balance |
| inArrears | Boolean | true if loan is overdue |
| dueDate | String | ISO date of next payment |

### SavingsDataPoint
| Field | Type | Notes |
|-------|------|-------|
| date | String | ISO date string (YYYY-MM-DD) |
| balance | Double | KES cumulative balance at that date |

### AttendanceSummary
| Field | Type | Notes |
|-------|------|-------|
| meetingsAttended | Int | Count of meetings attended by this member |
| totalMeetings | Int | Total meetings held by the group |
| attendanceRate | Float | 0.0–1.0 (meetingsAttended / max(totalMeetings, 1)) |

### CreateMemberRequest
| Field | Type | Notes |
|-------|------|-------|
| firstName | String | min 2 chars |
| lastName | String | min 2 chars |
| phone | String | Kenya E.164 format, unique |
| photoUri | String? | Local file URI; null if none |
| role | MemberRole | Selected from dropdown |
| groupId | String | Parent group's app ID |
| officeId | Long | From parent group |
| activationDate | String | Current date (dd MMMM yyyy) |

### Phone Validation Rule
- Regex: `^(\+254|0)[7][0-9]{8}$`
- Valid examples: `+254712345678`, `0712345678`
- Invalid: `+1555123456`, `0812345678`, `254712345678` (missing +)
- Error message: "Enter a valid Kenyan phone number."
- Duplicate check: HTTP 400 from create_client → surfaced as error_phone_exists: "A member with this phone number already exists."
