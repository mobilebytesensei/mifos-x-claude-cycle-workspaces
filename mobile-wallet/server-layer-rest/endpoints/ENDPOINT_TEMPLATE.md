# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/server-layer-rest/endpoints/ENDPOINT_TEMPLATE.md"
# last_modified: "2026-03-19"

# {{FEATURE_NAME}} Endpoints

**Feature:** {{feature_name}}
**Base Path:** /api/v1/{{resource}}
**Last Updated:** 2026-03-19

---

## Endpoints Summary

| Method | Endpoint | Description | Auth |
|:------:|----------|-------------|:----:|
| GET | /api/v1/{{resource}} | List all {{resource}} | Yes |
| GET | /api/v1/{{resource}}/:id | Get {{resource}} by ID | Yes |
| POST | /api/v1/{{resource}} | Create {{resource}} | Yes |
| PUT | /api/v1/{{resource}}/:id | Update {{resource}} | Yes |
| DELETE | /api/v1/{{resource}}/:id | Delete {{resource}} | Yes |

---

## List {{RESOURCE}}

**Method:** GET
**Path:** `/api/v1/{{resource}}`
**Auth:** Required

### Description

Retrieves a paginated list of {{resource}}.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| limit | integer | 20 | Items per page (max: 100) |
| sort | string | created_at | Sort field |
| order | string | desc | Sort order (asc/desc) |
| search | string | - | Search query |

### Response (200 OK)

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "string",
      "created_at": "2026-01-13T10:00:00Z",
      "updated_at": "2026-01-13T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

---

## Get {{RESOURCE}} by ID

**Method:** GET
**Path:** `/api/v1/{{resource}}/:id`
**Auth:** Required

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | uuid | {{RESOURCE}} ID |

### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_at": "2026-01-13T10:00:00Z",
    "updated_at": "2026-01-13T10:00:00Z"
  }
}
```

### Response (404 Not Found)

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "{{RESOURCE}} not found"
  }
}
```

---

## Create {{RESOURCE}}

**Method:** POST
**Path:** `/api/v1/{{resource}}`
**Auth:** Required

### Request Body

```json
{
  "name": "string (required)",
  "description": "string (optional)"
}
```

### Response (201 Created)

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_at": "2026-01-13T10:00:00Z",
    "updated_at": "2026-01-13T10:00:00Z"
  }
}
```

### Response (400 Bad Request)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "code": "REQUIRED",
        "message": "Name is required"
      }
    ]
  }
}
```

---

## Update {{RESOURCE}}

**Method:** PUT
**Path:** `/api/v1/{{resource}}/:id`
**Auth:** Required

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | uuid | {{RESOURCE}} ID |

### Request Body

```json
{
  "name": "string (optional)",
  "description": "string (optional)"
}
```

### Response (200 OK)

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_at": "2026-01-13T10:00:00Z",
    "updated_at": "2026-01-13T10:00:00Z"
  }
}
```

---

## Delete {{RESOURCE}}

**Method:** DELETE
**Path:** `/api/v1/{{resource}}/:id`
**Auth:** Required

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | uuid | {{RESOURCE}} ID |

### Response (204 No Content)

No response body.

### Response (404 Not Found)

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "{{RESOURCE}} not found"
  }
}
```

---

## DTOs

### {{RESOURCE}}Request

```typescript
interface {{RESOURCE}}Request {
  name: string;          // Required
  description?: string;  // Optional
}
```

### {{RESOURCE}}Response

```typescript
interface {{RESOURCE}}Response {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}
```

### {{RESOURCE}}ListResponse

```typescript
interface {{RESOURCE}}ListResponse {
  success: boolean;
  data: {{RESOURCE}}Response[];
  meta: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}
```
