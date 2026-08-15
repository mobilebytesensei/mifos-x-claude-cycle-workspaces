# ${BACKEND_NAME} API Index

> **Purpose**: Fast API lookup with service method references
> **Pattern**: Static table first → endpoints/ for details → Design layer for source

---

## Source of Truth Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  Design Layer: features/*/API.md                                │
│  └─→ ULTIMATE SOURCE OF TRUTH                                   │
│  └─→ Where APIs are first designed/documented                   │
├─────────────────────────────────────────────────────────────────┤
│  Server Layer: (This directory)                                 │
│  └─→ DERIVED but COMPLETE for client layer                      │
│  ├─→ API_INDEX.md (this file) - Quick lookup                   │
│  ├─→ API_REFERENCE.md - Complete endpoint details              │
│  ├─→ CLIENT_PATTERNS.md - Service/Repository patterns          │
│  └─→ ERROR_HANDLING.md - Exception handling                    │
├─────────────────────────────────────────────────────────────────┤
│  Client Layer: services/, repository/, models/                  │
│  └─→ IMPLEMENTATION based on server layer docs                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

1. [Quick Lookup](#quick-lookup)
2. [By Category](#by-category)
3. [Keyword Mapping](#keyword--endpoint-mapping-o1-lookup)
4. [Backend Configuration](#backend-configuration)
5. [External References](#external-references)

---

## Quick Lookup

| Endpoint | Method | Purpose | Service Method | Docs |
|----------|--------|---------|----------------|------|
| `/authentication` | POST | Login user | `authenticate()` | [AUTH](endpoints/AUTH.md) |
| `/clients` | GET | List clients | `getClients()` | [CLIENT](endpoints/CLIENT.md) |
| `/clients/{id}` | GET | Get client details | `getClientDetails()` | [CLIENT](endpoints/CLIENT.md) |

> **Note**: This table is auto-populated during `/project-add` or `/project-verify`.
> Add new endpoints using the format: `| /path | METHOD | Purpose | methodName() | [CATEGORY](endpoints/CATEGORY.md) |`

---

## By Category

### Authentication (${AUTH_ENDPOINT_COUNT} endpoints)

| Endpoint | Method | Service Method | Purpose |
|----------|--------|----------------|---------|
| `/authentication` | POST | `authenticate()` | Login with credentials |
| `/registration` | POST | `register()` | Register new user |

**Service**: `AuthenticationService`
**Docs**: [auth/API.md](../idea-layer/exports/auth/API.md)

---

### Client (${CLIENT_ENDPOINT_COUNT} endpoints)

| Endpoint | Method | Service Method | Purpose |
|----------|--------|----------------|---------|
| `/clients` | GET | `getClients()` | List all clients |
| `/clients/{id}` | GET | `getClientDetails()` | Get client by ID |
| `/clients/{id}/accounts` | GET | `getClientAccounts()` | Get client accounts |

**Service**: `ClientService`
**Docs**: [client/API.md](../idea-layer/exports/client/API.md)

---

## Keyword → Endpoint Mapping (O(1) Lookup)

```yaml
# Authentication
login: /authentication
authenticate: /authentication
register: /registration
signup: /registration

# Client
client: /clients
clients: /clients
client details: /clients/{id}
accounts: /clients/{id}/accounts

# Add more keyword mappings as endpoints are documented
```

---

## Backend Configuration

| Setting | Value |
|---------|-------|
| Provider | ${BACKEND_PROVIDER} |
| Base URL | ${BASE_URL} |
| Auth Method | ${AUTH_METHOD} |
| Content-Type | application/json |

---

## External References

| Resource | URL |
|----------|-----|
| API Documentation | ${API_DOCS_URL} |
| Swagger UI | ${SWAGGER_URL} |

---

## Endpoint Files (O(1) Lookup)

| File | Category | Endpoints |
|------|----------|:---------:|
| [AUTH.md](endpoints/AUTH.md) | Authentication | TBD |
| [CLIENT.md](endpoints/CLIENT.md) | Client | TBD |

---

## Related Files

| File | Purpose |
|------|---------|
| `endpoints/*.md` | Per-category endpoint documentation |
| `API_REFERENCE.md` | Complete endpoint overview |
| `CLIENT_PATTERNS.md` | Service/Repository implementation patterns |
| `ERROR_HANDLING.md` | Exception handling reference |
| `LAYER_GUIDE.md` | Server layer conventions |

---

## Commands

```bash
/enforce-index api         # Validate this index
/server [endpoint]         # Document endpoint (auto-indexes)
/gap-analysis server       # Check server layer gaps
```
