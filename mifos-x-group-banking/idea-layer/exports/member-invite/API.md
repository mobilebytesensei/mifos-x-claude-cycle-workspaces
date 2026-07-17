# Member Invite — API Contract

> **Backend build gate:** These endpoints use **COMP-DT-002/003/005** — generic datatable-CRUD tools
> in mcp-mifosx (`go/tools/datatables.go`) operating on the `dt_companion_invitations` datatable
> (attached to `m_group`). The datatable must be **provisioned once at deploy** (via COMP-DT-001) and
> the companion API must be built and deployed before this flow is reachable on device.
> Build spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md §1b (TIER-2) + §2 + §3`

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool |
|---|---|---|---|---|---|
| `create_invite` | POST | `/companion/datatables/invitations/{groupId}` | Bearer | yes | COMP-DT-002 |
| `list_pending_invites` | GET | `/companion/datatables/invitations/{groupId}` | Bearer | no | COMP-DT-003 |
| `revoke_invite` | DELETE | `/companion/datatables/invitations/{groupId}/{rowId}` | Bearer | yes | COMP-DT-005 |

## Request / Response Details

### POST /companion/datatables/invitations/{groupId} (COMP-DT-002 — create)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| emailPhone | String? | no | Intended recipient email/phone (null = generic code) |
| roleToAssign | String | yes | MEMBER \| TREASURER \| SECRETARY |

**Response**

| Field | Type | Description |
|---|---|---|
| rowId | Long | New datatable row ID |
| token | String | Invite code (alphanumeric, 8–12 chars) |
| inviteLink | String | Deep-link URL: `mifos://join?code={token}` |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Invalid roleToAssign |
| 401 | Unauthorized |
| 403 | Not an organizer/treasurer of this group |
| 500 | Server error |

---

### GET /companion/datatables/invitations/{groupId} (COMP-DT-003 — list)

**Query Params**

| Param | Type | Default |
|---|---|---|
| limit | Int | 20 |
| offset | Int | 0 |
| status | String? | "pending" (not yet accepted) |

**Response**

| Field | Type | Description |
|---|---|---|
| items | List<PendingInvite> | Page of pending invites |
| totalCount | Int | Total pending count |
| hasMore | Boolean | Whether more pages exist |

**Cache:** TTL 60 s, stale-while-revalidate.

---

### DELETE /companion/datatables/invitations/{groupId}/{rowId} (COMP-DT-005 — revoke)

**Request:** no body.

**Response:** 204 No Content on success.

**Errors**

| Code | Meaning |
|---|---|
| 404 | Invite row not found (already revoked) |
| 403 | Not authorised to revoke this invite |

**Optimistic update:** Row removed from `pending_invites_cache` immediately before the
DELETE completes. If the call fails, the row is restored and a snackbar shows the error.

---

## DTOs

### CreateInviteRequest
```
emailPhone: String?
roleToAssign: String   // MEMBER | TREASURER | SECRETARY
```

### GeneratedInvite
```
rowId: Long
token: String
inviteLink: String
```

### PendingInvite
```
rowId: Long
token: String
invitedEmailPhone: String?
roleToAssign: String
expiresAt: String      // ISO-8601
acceptedAt: String?    // null if pending
```

## Offline Behaviour

Invite generation requires active connectivity. The pending invites list serves the
`pending_invites_cache` (60 s stale) when offline, with a "Last synced" banner.
Revoke is attempted live; if offline, the optimistic delete is rolled back.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `403 Forbidden` | "Only organisers can generate invites" snackbar |
| `401 Unauthorized` | Navigate to `login-signup` |
| `network.offline (generate)` | Block generate — show "Requires internet" |
| `network.offline (list)` | Serve cached pending list + banner |
| `network.offline (revoke)` | Roll back optimistic delete + snackbar |
| `500 Server` | Show retry snackbar |
