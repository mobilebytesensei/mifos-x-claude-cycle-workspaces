# API Versions - Mifos Mobile

> Version-specific API documentation for Fineract Self-Service API

---

## Current Versions

| Version | Status | Introduced | Deprecated | Sunset |
|:-------:|:------:|:----------:|:----------:|:------:|
| v1 | Current | v0.3.0 | - | - |

---

## Backend: Fineract

| Setting | Value |
|---------|-------|
| Type | Fineract Self-Service API |
| Base URL | `https://[server]/fineract-provider/api/v1/self/` |
| Auth | Basic Auth (Base64 encoded) |
| Documentation | [Fineract API Docs](https://demo.mifos.io/api-docs/apiLive.htm) |

---

## Version Policy

| Policy | Value |
|--------|-------|
| Deprecation Notice | 2 minor versions before removal |
| Sunset Period | 6 months after deprecation |
| Breaking Changes | Major version bump required |

---

## Directory Structure

```
api-versions/
├── README.md              # This file
└── v1/
    ├── README.md          # v1 API overview
    └── endpoints/
        ├── auth.md
        ├── clients.md
        ├── accounts.md
        └── ...
```

---

## Fineract API Categories

| Category | Endpoint Prefix | Count |
|----------|-----------------|:-----:|
| Authentication | `/authentication` | 1 |
| Clients | `/clients` | 5 |
| Savings | `/savingsaccounts` | 8 |
| Loans | `/loans` | 10 |
| Beneficiaries | `/beneficiaries` | 4 |
| Transfers | `/accounttransfers` | 3 |
| Charges | `/charges` | 2 |
| Notifications | `/notifications` | 2 |
