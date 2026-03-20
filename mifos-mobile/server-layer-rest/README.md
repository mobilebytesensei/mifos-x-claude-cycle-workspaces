# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/server-layer-rest/README.md"
# last_modified: "2026-03-20"

# Server Layer - REST API

**Project:** mifos-mobile
**Server Type:** Custom REST API
**Last Updated:** 2026-03-19

---

## Overview

This server layer documents a custom REST API backend. Unlike Supabase projects, REST API projects require separate backend implementation.

---

## Directory Structure

```
server-layer/
├── README.md                 # This file
├── API_INDEX.md              # O(1) endpoint lookup
├── API_REFERENCE.md          # OpenAPI-style reference
└── endpoints/                # Per-feature endpoint docs
    ├── authentication.md
    ├── users.md
    └── {feature}.md
```

---

## Base Configuration

```yaml
base_url: {{BASE_URL}}
api_version: v1
content_type: application/json
authentication: Bearer token
```

---

## Quick Reference

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Authentication | /api/v1/auth | POST |
| Users | /api/v1/users | GET, POST, PUT, DELETE |
| {Resource} | /api/v1/{resource} | GET, POST, PUT, DELETE |

---

## Authentication

### Bearer Token

```http
Authorization: Bearer <access_token>
```

### Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "<refresh_token>"
}
```

---

## Common Response Formats

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

---

## Pagination

All list endpoints support pagination:

```
GET /api/v1/items?page=1&limit=20
```

Response includes meta:

```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

## Integration with Framework

### Design Layer Sync

The `/server check` command compares:
- `design-spec-layer/features/{feature}/API.md` (required endpoints)
- `server-layer/endpoints/{feature}.md` (documented endpoints)

### Client Layer Integration

When `/gap-implement-project` runs:
1. Reads API.md from design layer
2. Checks if endpoint is documented in server layer
3. Generates client service with correct endpoint paths

---

## Documentation Commands

```bash
# Check API documentation coverage
/server check

# Verify endpoints match design layer
/server status
```

---

## Adding New Endpoints

1. Add endpoint to `design-spec-layer/features/{feature}/API.md`
2. Create/update `server-layer/endpoints/{feature}.md`
3. Update `API_INDEX.md`
4. Run `/server check` to verify
