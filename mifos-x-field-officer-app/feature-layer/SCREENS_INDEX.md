# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/feature-layer/SCREENS_INDEX.md"
# last_modified: "2026-03-20"

# Screens Index - O(1) Lookup

> **Purpose**: Instant lookup for all screens in the feature-layer.

---

## Quick Reference

| # | Screen | Feature | Route | ViewModel | Keywords | Path |
|:-:|--------|---------|-------|-----------|----------|------|
| 1 | {{SCREEN_NAME}} | {{FEATURE}} | {{ROUTE}} | {{VIEWMODEL}} | {{KEYWORDS}} | feature/{{FEATURE}}/{{SCREEN_NAME}}.kt |

---

## Category Index

### Authentication Screens
| Screen | Feature | Path |
|--------|---------|------|

### Dashboard Screens
| Screen | Feature | Path |
|--------|---------|------|

### Account Screens
| Screen | Feature | Path |
|--------|---------|------|

### Settings Screens
| Screen | Feature | Path |
|--------|---------|------|

---

## Keyword -> Screen Mapping

```yaml
# Auth
login: LoginScreen
register: RegisterScreen
forgot password: ForgotPasswordScreen

# Dashboard
home: HomeScreen
overview: DashboardScreen

# Accounts
accounts: AccountsScreen
account details: AccountDetailScreen
```

---

## Screen Types

| Type | Description | Example |
|------|-------------|---------|
| List | Shows collection of items | AccountsScreen |
| Detail | Shows single item | AccountDetailScreen |
| Form | User input | CreateBeneficiaryScreen |
| Dialog | Modal interaction | ConfirmationDialog |

---

## File Structure Per Screen

```
feature/{feature}/
├── {Name}Screen.kt        # Composable UI
├── {Name}ScreenContent.kt # Stateless preview-able content (optional)
├── {Name}ViewModel.kt     # State management
├── {Name}UiState.kt       # UI state sealed class
└── navigation/
    └── {Name}Navigation.kt
```

---

## Commands

```bash
/enforce-index screens     # Validate this index
/feature [name]            # Create feature (auto-indexes screens)
/gap-analysis feature      # Check feature layer gaps
```
