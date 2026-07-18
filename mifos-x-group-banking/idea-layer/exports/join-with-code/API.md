# Join With Code — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool |
|---|---|---|---|---|---|
| `validate_invite_token` | GET | `/companion/datatables/invitations/{entityId}` | Bearer | no | COMP-DT-002 (datatable read) |
| `get_group_preview` | GET | `/companion/groups/{groupId}` | Bearer | no | COMP-GRP-001 |
| `associate_client_to_group` | POST | `/companion/groups/{groupId}/associate-clients` | Bearer | yes | COMP-GRP-003 |
| `mark_invitation_accepted` | PUT | `/companion/datatables/invitations/{entityId}/{rowId}` | Bearer | yes | COMP-DT-004 |

## Request / Response Details

### GET /companion/datatables/invitations/{entityId} (COMP-DT-002 read)

entityId = invite token string (URL-encoded).

**Request:** no body.

**Response**

| Field | Type | Description |
|---|---|---|
| rowId | Long | Datatable row identifier |
| token | String | Invite code |
| groupId | String | Group this invite belongs to |
| invitedEmailPhone | String? | Intended recipient (may be null for generic codes) |
| expiresAt | String | ISO-8601 expiry |
| acceptedAt | String? | Set if already accepted |

**Errors**

| Code | Meaning |
|---|---|
| 404 | Token not found → `ERROR_INVALID_CODE` |
| 410 | Token expired → `ERROR_EXPIRED` |
| 409 | Token already accepted by this user → `ERROR_ALREADY_MEMBER` |

---

### GET /companion/groups/{groupId} (COMP-GRP-001 — read for preview)

**Response**

| Field | Type | Description |
|---|---|---|
| groupId | String | Companion group ID |
| groupName | String | Display name |
| groupType | String | e.g. VSLA, ROSCA |
| memberCount | Int | Current member count |

---

### POST /companion/groups/{groupId}/associate-clients (COMP-GRP-003)

**Request**

| Field | Type | Required |
|---|---|---|
| clientIds | List<String> | yes |

**Response**

| Field | Type | Description |
|---|---|---|
| groupId | String | Group ID |
| associatedClientId | String | The newly associated client |
| role | String | Assigned role (default MEMBER) |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Missing clientIds |
| 401 | Unauthorized |
| 404 | Group not found |
| 409 | Client already associated |

---

### PUT /companion/datatables/invitations/{entityId}/{rowId} (COMP-DT-004)

**Request**

| Field | Type | Required |
|---|---|---|
| acceptedAt | String | yes (ISO-8601) |

**Response**

| Field | Type | Description |
|---|---|---|
| rowId | Long | Updated row ID |
| status | String | "accepted" |

**Note:** Failure of this call is **non-fatal**. Navigation to group-dashboard proceeds
regardless of the outcome of this mark-accepted call.

---

## DTOs

### InvitationRow
```
rowId: Long
token: String
groupId: String
invitedEmailPhone: String?
expiresAt: String
acceptedAt: String?
```

### GroupPreview
```
groupId: String
groupName: String
groupType: String
memberCount: Int
```

### AssociateClientsRequest
```
clientIds: List<String>
```

### AssociateClientsResponse
```
groupId: String
associatedClientId: String
role: String
```

### MarkAcceptedRequest
```
acceptedAt: String
```

## Offline Behaviour

Joining a group requires active connectivity. No offline fallback. The `pending_invite_cache`
is session-only and cleared on success or unrecoverable error.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `404 validate_invite_token` | `ERROR_INVALID_CODE` state |
| `410 validate_invite_token` | `ERROR_EXPIRED` state |
| `409 validate_invite_token` | `ERROR_ALREADY_MEMBER` state |
| `404 associate_client_to_group` | Show error banner |
| `409 associate_client_to_group` | `ERROR_ALREADY_MEMBER` state |
| `mark_invitation_accepted any` | Log + ignore — non-fatal |
| `network.offline` | `ERROR_NETWORK` state |
| `401` | Redirect to `login-signup` with `pendingInviteCode` |
