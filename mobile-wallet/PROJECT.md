# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/PROJECT.md"
# last_modified: "2026-03-20"

# mobile-wallet - Project Configuration

> Mobile Wallet - Digital wallet app for payments, transfers, and financial services

---

## Project Info

| Field | Value |
|-------|-------|
| **Project Name** | mobile-wallet |
| **Workspace** | mifos-x |
| **Type** | kmp |
| **Subtype** | kmp-app |
| **Created** | 2026-02-25 |

---

## Project Idea

Mobile wallet for financial transactions - Digital wallet app for payments, transfers, and financial services including P2P transfers, bill payments, KYC verification, and account management.

---

## Targets

| Platform | Status |
|----------|:------:|
| Android | ✅ |
| iOS | ✅ |
| Desktop | ✅ |
| Web | ✅ |

---

## Backend Configuration

```yaml
backend:
  provider: fineract
  type: rest
  client: ktorfit
  secondary: supabase  # For config/instance management
```

---

## Source Repository

| Field | Value |
|-------|-------|
| URL | https://github.com/openMF/mobile-wallet |
| Path | source/mobile-wallet |
| Type | Git Submodule |

---

## Layer Status

| Layer | Status | Features/Items |
|-------|:------:|----------------|
| Plan | 🟢 Created | - |
| Design | 🟢 Created | 23 features |
| Server | 🟢 Created | 19 services |
| Client | 🟢 Created | 23 repositories |
| Feature | 🟢 Created | 55 screens, 41 ViewModels |
| Platform | 🟢 Created | 4 platforms |
| Testing | 🟢 Created | - |

---

## Quick Links

- [Design Specs](design-spec-layer/FEATURES_INDEX.md)
- [API Reference](server-layer/API_INDEX.md)
- [Client Services](client-layer/SERVICES_INDEX.md)
- [Feature Modules](feature-layer/MODULES_INDEX.md)
- [Current Work](CURRENT_WORK.md)

---

## Commands

```bash
# Session management
/session-start mobile-wallet
/session-end

# Gap analysis
/gap-analysis
/gap-planning design

# Implementation
/design [feature]
/implement [feature]
/verify
```
