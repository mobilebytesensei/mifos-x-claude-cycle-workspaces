# Plan: Design Flow - Authentication

**Plan ID:** design-flow-authentication-260119-001
**Created:** 2026-01-19
**Status:** Complete
**Type:** User Flow Creation

---

## Summary

| Attribute | Value |
|-----------|-------|
| Project | mifos-mobile |
| Flow Name | authentication |
| Screens | 12 |
| Related Features | auth, passcode |
| Based On | features/auth/SPEC.md |

---

## What Was Done

### 1. User Flows Directory Created
- Created `design-spec-layer/user-flows/` directory
- Created `design-spec-layer/user-flows/flows/` for flow files
- Created `FLOWS_INDEX.md` for O(1) lookup

### 2. Authentication Flow Created
- File: `flows/authentication.mmd`
- Format: Mermaid flowchart
- Screens covered:
  - Splash Screen
  - Login Screen
  - Registration Screen
  - Upload ID Screen
  - OTP Verification Screen
  - Password Recovery Screen
  - Set Password Screen
  - Passcode Setup Screen
  - Passcode Verify Screen
  - Status Screen
  - Home Screen (exit point)

### 3. Flow Structure

```
Authentication Flow Structure:
├── Splash (entry)
│   └── Auth Check
│       ├── Has Session → Passcode Verify → Home
│       └── No Session → Login
├── Login
│   ├── → Passcode Setup → Home
│   ├── → Sign Up (Registration)
│   └── → Forgot Password (Recovery)
├── Registration
│   └── → Upload ID → OTP Verify → Success → Login
└── Password Recovery
    └── → Set New Password → Login
```

---

## Files Created

| # | File | Purpose |
|:-:|------|---------|
| 1 | `user-flows/FLOWS_INDEX.md` | O(1) flow lookup index |
| 2 | `user-flows/flows/authentication.mmd` | Authentication flow diagram |

---

## Flow Coverage Analysis

| Feature | Status | Notes |
|---------|:------:|-------|
| auth | ✅ Covered | Full login/registration flow |
| passcode | ✅ Covered | Setup and verify flows |
| home | ⚠️ Entry only | Exit point from auth flow |
| accounts | ❌ Not covered | Needs separate flow |
| savings-account | ❌ Not covered | Needs separate flow |
| loan-account | ❌ Not covered | Needs separate flow |
| beneficiary | ❌ Not covered | Needs separate flow |
| transfer | ❌ Not covered | Needs separate flow |

---

## Next Steps

### Recommended Flow Generation

| Priority | Flow | Command | Description |
|:--------:|------|---------|-------------|
| P1 | core-navigation | `/flow-generate core-navigation` | Tab bar navigation |
| P1 | accounts | `/flow-generate accounts` | Account list & details |
| P2 | transfer | `/flow-generate transfer` | Money transfer flow |
| P2 | beneficiary | `/flow-generate beneficiary` | Beneficiary management |

### Validate Flow

```bash
/flow-validate authentication    # Check flow coverage
/flow authentication             # Visualize flow
```

---

## Mermaid Live Preview

View the authentication flow diagram:
[Mermaid Live Editor](https://mermaid.live/edit)

Paste the content from `flows/authentication.mmd` to visualize.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-19 | Created authentication flow from auth SPEC.md |
