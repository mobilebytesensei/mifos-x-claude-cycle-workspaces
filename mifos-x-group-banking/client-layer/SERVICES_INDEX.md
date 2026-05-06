# Services Index - O(1) Lookup

> **Purpose**: Instant lookup for all network services in the client-layer.

---

## Quick Reference

| # | Service | Methods | Repository | Keywords | Path |
|:-:|---------|:-------:|------------|----------|------|
| 1 | {{SERVICE_NAME}} | {{METHOD_COUNT}} | {{REPOSITORY}} | {{KEYWORDS}} | services/{{SERVICE_NAME}}.kt |

---

## Category Index

### Authentication Services
| Service | Repository | Path |
|---------|------------|------|
| AuthenticationService | AuthRepository | services/AuthenticationService.kt |

### Account Services
| Service | Repository | Path |
|---------|------------|------|

### Transaction Services
| Service | Repository | Path |
|---------|------------|------|

---

## Keyword → Service Mapping

```yaml
# Authentication
login service: AuthenticationService
auth api: AuthenticationService

# Accounts
account service: AccountService
balance api: AccountService
```

---

## Service → Repository Mapping

| Service | Repository |
|---------|------------|
| AuthenticationService | AuthRepository |
| AccountService | AccountRepository |

---

## Service Interface Pattern

```kotlin
interface {ServiceName} {
    suspend fun method1(): Response<Type>
    suspend fun method2(param: Type): Response<Type>
}
```

---

## Commands

```bash
/enforce-index services    # Validate this index
/client [service]          # Create service (auto-indexes)
/gap-analysis client       # Check client layer gaps
```
