# Login Signup — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool |
|---|---|---|---|---|---|
| `companion_self_register` | POST | `/companion/auth/self-register` | no | yes | COMP-AUTH-001 |
| `companion_login` | POST | `/companion/auth/login` | no | yes | COMP-AUTH-002 |
| `companion_me` | GET | `/companion/auth/me` | Bearer | no | COMP-AUTH-003 |

## Request / Response Details

### POST /companion/auth/self-register (COMP-AUTH-001)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| name | String | yes | Display name |
| emailPhone | String | yes | Email or phone (server normalises) |
| password | String | yes | Min 8 chars |

**Response**

| Field | Type | Description |
|---|---|---|
| userId | String | Companion user ID |
| sessionToken | String | Bearer token |
| tokenExpiresAt | String | ISO-8601 expiry |
| groupMemberships | List<GroupMembership> | Empty for new registrations |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Validation error (email/phone format, password length) |
| 409 | emailPhone already registered |
| 500 | Server error |

**Cache:** none — write endpoint.

---

### POST /companion/auth/login (COMP-AUTH-002)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| emailPhone | String | yes | Registered email or phone |
| password | String | yes (if no pin) | Password |
| pin | String | yes (if no password) | 4-digit PIN (alternative to password) |

**Response** — same shape as COMP-AUTH-001 response.

**Errors**

| Code | Meaning |
|---|---|
| 400 | Missing credentials |
| 401 | Wrong emailPhone or password/pin |
| 429 | Too many failed attempts — rate-limited |
| 500 | Server error |

---

### GET /companion/auth/me (COMP-AUTH-003)

**Request** — no body; Bearer token in header.

**Response**

| Field | Type | Description |
|---|---|---|
| userId | String | Companion user ID |
| displayName | String | Stored display name |
| emailPhone | String | Registered credential |
| groupMemberships | List<GroupMembership> | All groups user belongs to |

**Errors**

| Code | Meaning |
|---|---|
| 401 | Expired or invalid session token |

**Cache:** TTL 300 s, stale-while-revalidate. Invalidated on logout.

---

## DTOs

### SelfRegisterRequest
```
name: String
emailPhone: String
password: String
```

### LoginRequest
```
emailPhone: String
password: String?
pin: String?
```

### AuthResponse
```
userId: String
sessionToken: String
tokenExpiresAt: String
groupMemberships: List<GroupMembership>
```

### GroupMembership
```
groupId: String
groupName: String
role: String        // ORGANIZER | MEMBER | TREASURER | CHAIRPERSON | SECRETARY
joinedAt: String    // ISO-8601
```

### UserProfile
```
userId: String
displayName: String
emailPhone: String
groupMemberships: List<GroupMembership>
```

## Offline Behaviour

Auth endpoints require active connectivity. No offline mutation or token refresh is
supported. `SessionStore` serves the cached `sessionToken` for subsequent in-session API
calls while online; on expiry the user is redirected to login-signup.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `400 Bad Request` | Show field-level `validationErrors` map |
| `401 Unauthorized` | Show top-level error banner |
| `409 Conflict` | Show "Already registered" inline error |
| `429 Rate Limited` | Show "Too many attempts, try again later" banner |
| `network.offline` | Block submit — show "Requires internet connection" |
| `500 Server` | Show retry banner |
