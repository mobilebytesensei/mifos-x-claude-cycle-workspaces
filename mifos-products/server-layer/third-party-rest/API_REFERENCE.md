# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/third-party-rest/API_REFERENCE.md"
# last_modified: "2026-03-19"

# API Reference

**Project:** mifos-products
**Base URL:** {{BASE_URL}}
**Version:** 1.0.0

---

## Overview

This document provides OpenAPI-style reference for all API endpoints.

---

## Servers

| Environment | URL |
|-------------|-----|
| Development | http://localhost:8080/api/v1 |
| Staging | https://staging.mifos-products.com/api/v1 |
| Production | https://api.mifos-products.com/api/v1 |

---

## Authentication

### Bearer Token

All authenticated endpoints require:

```http
Authorization: Bearer <access_token>
```

### Token Lifecycle

1. Login → Receive access_token + refresh_token
2. Use access_token for API calls
3. When access_token expires → Use refresh_token to get new tokens
4. When refresh_token expires → Re-login required

---

## Common Headers

| Header | Required | Description |
|--------|:--------:|-------------|
| Content-Type | Yes | `application/json` |
| Authorization | Auth | `Bearer <token>` |
| Accept | No | `application/json` |
| X-Request-ID | No | Client-generated request ID |

---

## Common Response Codes

| Code | Meaning |
|:----:|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (success, no body) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (duplicate resource) |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |

---

## Data Types

### UUID

```
format: uuid
pattern: ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
example: "123e4567-e89b-12d3-a456-426614174000"
```

### DateTime

```
format: ISO 8601
pattern: YYYY-MM-DDTHH:mm:ss.sssZ
example: "2026-01-13T10:30:00.000Z"
```

### Pagination

```json
{
  "page": 1,
  "limit": 20,
  "total": 100,
  "total_pages": 5,
  "has_next": true,
  "has_prev": false
}
```

---

## Error Format

### Standard Error

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": []
  }
}
```

### Validation Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Invalid email format"
      }
    ]
  }
}
```

---

## Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| Authentication | 10 req/min |
| Read (GET) | 100 req/min |
| Write (POST/PUT/DELETE) | 30 req/min |

Headers returned:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1673612345
```

---

## Schemas

### User

```yaml
User:
  type: object
  properties:
    id:
      type: string
      format: uuid
    email:
      type: string
      format: email
    name:
      type: string
    avatar_url:
      type: string
      format: uri
      nullable: true
    created_at:
      type: string
      format: date-time
    updated_at:
      type: string
      format: date-time
```

### AuthTokens

```yaml
AuthTokens:
  type: object
  properties:
    access_token:
      type: string
    refresh_token:
      type: string
    expires_in:
      type: integer
      description: Seconds until access_token expires
    token_type:
      type: string
      enum: [Bearer]
```

---

## Endpoint Documentation Template

Use this template for documenting endpoints in `endpoints/*.md`:

```markdown
## Endpoint Name

**Method:** GET/POST/PUT/DELETE
**Path:** /api/v1/resource
**Auth:** Required / Optional / None

### Description

Brief description of what this endpoint does.

### Request

#### Headers

| Header | Required | Description |
|--------|:--------:|-------------|
| Authorization | Yes | Bearer token |

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | uuid | Resource ID |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| limit | integer | 20 | Items per page |

#### Request Body

\`\`\`json
{
  "field": "value"
}
\`\`\`

### Response

#### Success (200)

\`\`\`json
{
  "success": true,
  "data": { ... }
}
\`\`\`

#### Error (400)

\`\`\`json
{
  "success": false,
  "error": { ... }
}
\`\`\`
```
