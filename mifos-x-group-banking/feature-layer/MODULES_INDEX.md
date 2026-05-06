# Modules Index - O(1) Lookup

> **Purpose**: Instant lookup for all feature modules in the feature-layer.

---

## Quick Reference

| # | Module | Screens | ViewModels | Status | Keywords | Path |
|:-:|--------|:-------:|:----------:|:------:|----------|------|
| 1 | {{MODULE_NAME}} | {{SCREEN_COUNT}} | {{VM_COUNT}} | {{STATUS}} | {{KEYWORDS}} | feature/{{MODULE_NAME}}/ |

---

## Category Index

### Core Modules
| Module | Path |
|--------|------|
| auth | feature/auth/ |
| home | feature/home/ |

### Account Modules
| Module | Path |
|--------|------|
| accounts | feature/accounts/ |
| savings-account | feature/savings-account/ |
| loan-account | feature/loan-account/ |

### Transaction Modules
| Module | Path |
|--------|------|
| transfer | feature/transfer-process/ |
| recent-transaction | feature/recent-transaction/ |

### Settings Modules
| Module | Path |
|--------|------|
| settings | feature/settings/ |
| notification | feature/notification/ |

---

## Keyword → Module Mapping

```yaml
# Core
login: auth
home: home
dashboard: home

# Accounts
accounts: accounts
savings: savings-account
loan: loan-account

# Transactions
transfer: transfer-process
transactions: recent-transaction
```

---

## Module Structure

```
feature/{module}/
├── src/
│   └── commonMain/
│       └── kotlin/
│           ├── {Module}Screen.kt
│           ├── {Module}ViewModel.kt
│           ├── {Module}UiState.kt
│           ├── navigation/
│           │   └── {Module}Navigation.kt
│           └── di/
│               └── {Module}Module.kt
└── build.gradle.kts
```

---

## Status Legend

| Status | Meaning |
|:------:|---------|
| ✅ | Complete (Screen + ViewModel + Navigation + DI) |
| ⚠️ | Partial (missing components) |
| ❌ | Not started |
| 🔄 | In progress |

---

## Commands

```bash
/enforce-index modules     # Validate this index
/feature [module]          # Create module (auto-indexes)
/gap-analysis feature      # Check feature layer gaps
```
