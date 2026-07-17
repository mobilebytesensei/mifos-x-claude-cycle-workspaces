# Group Type Picker — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|
| `get_group_type_configs` | GET | `/companion/datatables/group_type_config/{entityId}` | Bearer | no |

entityId = 0 (global catalog; not per-group).

## Request / Response Details

### GET /companion/datatables/group_type_config/0

**Request:** no body. Bearer token in header.

**Response**

| Field | Type | Description |
|---|---|---|
| data | List<GroupTypeConfig> | All available group types |

**Errors**

| Code | Meaning |
|---|---|
| 401 | Unauthorized |
| 404 | Datatable entity not found |
| 500 | Server error |

**Cache:** TTL 86400 s, stale-while-revalidate. Config rarely changes.

---

## DTOs

### GroupTypeConfig
```
typeSlug: String                        // e.g. "vsla", "rosca", "asca"
displayName: String                     // e.g. "VSLA", "ROSCA", "SHG"
tagline: String                         // Short description shown on card
savingsMechanism: String                // e.g. "Share-based", "Fixed contributions"
contributionMode: String                // SHARE_BASED_VARIABLE | FIXED_AMOUNT | FIXED_NEGOTIATED
lendingEnabled: Boolean
hasSocialFund: Boolean
hasBankLinkage: Boolean
welfareOnlyMode: Boolean
formallyRegistered: Boolean
defaultLoanMultiplier: Double?
defaultInterestRatePct: Double?
defaultCycleLengthMonths: Int
maxMembers: Int
minMembers: Int
```

**Supported typeSlug values (9 types):**
`vsla`, `rosca`, `asca`, `silc`, `shg`, `sacco`, `cbo_village_bank`, `burial_welfare`, `jlg`

**pool_model derivation (client-side):**
- `ACCUMULATING`: vsla, silc, asca, shg, sacco, cbo_village_bank, burial_welfare, jlg
- `ROTATING_PAYOUT`: rosca

## Offline Behaviour

`group_type_config_cache` serves stale data with a "last synced" indicator. The 86400 s
TTL means configs are refreshed at most daily. No mutation operations — read-only screen.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `401 Unauthorized` | Navigate to `login-signup` |
| `404 Not Found` | Show error banner — datatable not provisioned |
| `network.offline` | Serve cached configs with sync banner |
| `500 Server` | Show retry banner |
