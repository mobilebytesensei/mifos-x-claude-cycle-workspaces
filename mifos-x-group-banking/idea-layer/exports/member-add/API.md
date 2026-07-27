<!--
  generated_from_feature: member-add
  contract_version: "2.0.0"
  source: idea-layer/screens/member-add/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Member Add — API Contract

## Endpoints (3 — ordered submit chain)

Base path: `/fineract-provider/api/v1` · Auth BasicAuth · Tenant `X-Fineract-Platform-TenantId: default`.

| ID | Function | Method | Endpoint | Writable | Offline op |
|---|---|---|---|---|---|
| `create_client` | create_client | POST | `/clients` | yes | CREATE_MEMBER |
| `assign_member_role` | assign_member_role | POST | `/datatables/dt_member_role/{clientId}` | yes | ASSIGN_MEMBER_ROLE |
| `upload_photo` | upload_photo | POST | `/clients/{clientId}/images` | yes | UPLOAD_MEMBER_PHOTO |

`assign_member_role` and `upload_photo` take `clientId` from the `create_client` response.

## Request / Response Details

### POST /clients (create_client)

**Body**

| Field | Type |
|---|---|
| firstname | String |
| lastname | String |
| mobileNo | String |
| active | Boolean |
| activationDate | String |
| officeId | Long |
| groupId | Long |
| locale | String |
| dateFormat | String |

**Response:** `{ resourceId: Long, clientId: Long }`.
**Errors:** 400 validation / duplicate phone · 401 Unauthorized · 403 Forbidden · 500 Server error.

### POST /datatables/dt_member_role/{clientId} (assign_member_role)

**Params:** `clientId: Long` (from create_client response).
**Body:** `{ role: String, groupId: Long, assignedDate: String }`.
**Response:** `{ resourceId: Long }`. **Errors:** 400 invalid role · 401 · 500.

### POST /clients/{clientId}/images (upload_photo)

**Params:** `clientId: Long`. **Body type:** `multipart/form-data`, `{ file: File }`.
**Response:** `{ resourceId: Long }`. **Errors:** 400 file too large (max 2MB) · 401 · 500.
Called only when `photoUri != null`.

## DTOs

### CreateMemberRequest
```
firstName: String
lastName: String
phone: String
photoUri: String?
role: MemberRole
groupId: String
officeId: Long
activationDate: String
```

### MemberRole (enum)
```
CHAIRPERSON | TREASURER | SECRETARY | MEMBER
```

## Repository Contract

- `MemberRepository`: createMember, assignRole, uploadPhoto
- `SyncQueueRepository`: enqueue
- Services: `NetworkMonitor`, `SessionManager`, `ImagePickerHelper`

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `Validation` | Inline `validationErrors` (error_validation) |
| `PhoneAlreadyExists` (400 dup) | Inline error on phone field (error_phone_exists) |
| `network.offline` | Enqueue chain to sync_queue; ShowOfflineSyncDialog (error_network) |
| `401 Unauthorized` | `MemberAddError.Auth` → redirect login |
| `403 Forbidden` | Forbidden error |
| `500 Server` | `MemberAddError.Server` (retry) |

## Offline Behaviour

When `cmp-network-monitor` reports offline, the create → assign-role → upload-photo operations are
enqueued to the SQLDelight `sync_queue` (CREATE_MEMBER / ASSIGN_MEMBER_ROLE / UPLOAD_MEMBER_PHOTO)
and drained via Store5 on reconnect; the UI shows the offline banner + `ShowOfflineSyncDialog`
instead of navigating to member-profile.
