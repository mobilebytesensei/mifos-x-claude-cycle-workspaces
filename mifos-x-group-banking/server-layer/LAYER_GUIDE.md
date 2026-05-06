---
_blueprint:
  version: "2.88.0"
  date: "2026-05-05"
  layer: "server-layer"
  project: "mifos-x-group-banking"
  scaffolded_at: "2026-05-05"
---

# Server Layer Guide — mifos-x-group-banking

> Backend: Mifos Fineract REST API. No custom server — all operations via MCP + REST.

## Structure

```
server-layer/
├── API.md                 # Endpoint documentation per feature
├── API_CONTRACT.yaml      # Machine-readable endpoint contracts
├── API_INDEX.md           # O(1) endpoint lookup by feature
└── BRIDGE_AUDIT_LOG.yaml  # Mifos bridge audit trail
```

## Backend Pattern

This project uses **third-party-rest** backend (Fineract), not Supabase.
All data operations go through the Mifos MCP Server (65 tools) or direct Fineract REST.

| Layer | Responsibility |
|-------|---------------|
| server-layer | Documents which Fineract endpoints each feature uses |
| client-layer | Implements KtorFit services + repositories wrapping those endpoints |
| feature-layer | ViewModels call repositories, never Fineract directly |

## Commands

| Command | Purpose |
|---------|---------|
| `/server` | Server layer operations |
| `/mifos-bridge` | Re-run bridge to update API_CONTRACT |
| `/client [feature]` | Generate client code from API_CONTRACT |
