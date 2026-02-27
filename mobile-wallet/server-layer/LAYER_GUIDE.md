# Server Layer Guide - mobile-wallet

> API documentation for Fineract Self-Service backend

---

## Layer Purpose

The server layer documents the backend API:
- Fineract Self-Service API endpoints
- Request/Response models
- Authentication flows
- Error handling patterns

---

## Backend Architecture

```
┌─────────────────────────────────────────────────────┐
│                   mobile-wallet                      │
├─────────────────────────────────────────────────────┤
│                  Ktorfit Client                      │
├─────────────────────────────────────────────────────┤
│              FineractApiManager                      │
│   ┌─────────────┬─────────────┬─────────────┐       │
│   │ AuthService │ ClientSvc   │ AccountSvc  │       │
│   └─────────────┴─────────────┴─────────────┘       │
├─────────────────────────────────────────────────────┤
│          Fineract Self-Service API                   │
│         /fineract-provider/api/v1/self/             │
└─────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
server-layer/
├── API_INDEX.md           # Service registry
├── LAYER_GUIDE.md         # This file
├── endpoints/             # Per-endpoint documentation
│   └── {service}.md
└── api-versions/          # Version-specific docs
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/server [service]` | Document API service |
| `/gap-analysis server` | Check documentation gaps |

---

## API Documentation Template

Each service should document:
1. Base path
2. Endpoints (method, path, params)
3. Request/Response models
4. Error codes
5. Example usage
