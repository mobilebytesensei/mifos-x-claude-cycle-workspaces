# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/server-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Server Layer Guide - mifos-mobile

> Conventions and patterns for API documentation.

---

## Purpose

The server layer documents all backend APIs, endpoints, and integration patterns used by the application.

---

## Directory Structure

```
server-layer/
├── API_INDEX.md        # O(1) endpoint lookup
├── API_REFERENCE.md    # Complete API documentation
├── CLIENT_PATTERNS.md  # Service/Repository patterns
├── ERROR_HANDLING.md   # Error handling conventions
├── TESTING_STATUS.md   # API test coverage
├── LAYER_GUIDE.md      # This file
├── endpoints/          # Per-endpoint documentation
│   ├── AUTH.md
│   ├── CLIENT.md
│   ├── SAVINGS.md
│   └── {CATEGORY}.md
└── api-versions/       # API version history
    ├── README.md
    └── v1/
```

---

## Source of Truth

```
┌─────────────────────────────────────────────────────────────┐
│  Design Layer: features/*/API.md                            │
│  └─→ ULTIMATE SOURCE OF TRUTH                               │
│  └─→ Where APIs are first designed/documented               │
├─────────────────────────────────────────────────────────────┤
│  Server Layer: (This directory)                             │
│  └─→ DERIVED but COMPLETE for client layer                  │
│  ├─→ API_INDEX.md - Quick lookup                           │
│  ├─→ API_REFERENCE.md - Complete endpoint details          │
│  └─→ endpoints/ - Category-specific docs                   │
├─────────────────────────────────────────────────────────────┤
│  Client Layer: core/network/, core/data/                    │
│  └─→ IMPLEMENTATION based on server layer docs             │
└─────────────────────────────────────────────────────────────┘
```

---

## Endpoint Documentation Pattern

Each endpoint file should document:

```markdown
### METHOD /endpoint

**Purpose**: Description

**Service**: `ServiceName.methodName()`

**Request**:
```json
{ "field": "value" }
```

**Response**:
```json
{ "field": "value" }
```

**DTO**: `DtoName`

**Errors**:
| Code | Message | Handling |
|------|---------|----------|
```

---

## Authentication

Document authentication requirements:

| Method | Header | Example |
|--------|--------|---------|
| Basic | `Authorization` | `Basic {base64}` |
| JWT | `Authorization` | `Bearer {token}` |
| API Key | `X-API-Key` | `{key}` |

---

## Workflow

1. Design API in `design-spec-layer/features/{feature}/API.md`
2. Add to `API_INDEX.md` for quick lookup
3. Document details in `endpoints/{category}.md`
4. Update `API_REFERENCE.md` if needed
5. Implement in client layer

---

## Commands

| Command | Purpose |
|---------|---------|
| `/gap-analysis server` | Check API documentation gaps |
| `/client [feature]` | Generate client from API docs |
| `/enforce-index api` | Validate API_INDEX |
