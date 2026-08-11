# Authentication — Feature Spec

## Overview

Authentication is the entry point for all MifosSave users. It presents a client-type selection screen (admin/staff or end-user/member), then routes to a contextual login form supporting Fineract username+password credentials, a 4-digit offline PIN, and optional biometric unlock.

**Acceptance Criteria**
- FR-013: Authenticate users via Fineract credentials with local PIN and optional biometric for offline access
- FR-014: Two client types — Admin (staff) and End User (self-service) — each with a distinct UI surface
- FR-015: Admin role-based permissions: treasurer, chairperson, field officer, program manager
- Staff login calls `POST /authentication`; end-user login calls `POST /self/authentication`
- On success, admin navigates to admin-dashboard; end user navigates to personal-dashboard
- PIN mode replaces username/password fields with a 4-digit numpad
- Biometric button visible only when device biometrics are enrolled and available
- On offline state, PIN login must function without network connectivity
- App version displayed at bottom of client-type selector for support reference
- Error states shown inline with localised message for each error type
- Analytics events fired: `client_type_selected`, `login_attempted`, `login_success`, `login_failed`, `biometric_triggered`

## Screens

| Screen | Composable | Layout | Description |
|--------|-----------|--------|-------------|
| Client Type Selector | `ClientTypeSelectorScreen` | Column (centered, full-screen) | First screen on app launch. Two large icon-driven tiles for admin vs member path. No API call. |
| Login | `LoginScreen` | Column (scrollable, centered) | Contextual auth form. Switches between password and PIN mode. Biometric unlock optional. |

## State Model

### ClientTypeSelectorViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| selectedClientType | ClientType? | null |
| isNavigating | Boolean | false |

**Actions**:
- `OnAdminSelected` — triggered by tap on "I manage a group" tile; emits `NavigateToAdminLogin` and passes `client_type=admin` to login screen
- `OnMemberSelected` — triggered by tap on "I'm a group member" tile; emits `NavigateToEndUserLogin` and passes `client_type=end_user` to login screen

**Events**:
- `NavigateToAdminLogin` — routes to `/login` with `client_type=admin`
- `NavigateToEndUserLogin` — routes to `/login` with `client_type=end_user`

**DI**: NavigationManager, SessionPreferences

### LoginViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| clientType | ClientType | ClientType.END_USER |
| username | String | "" |
| password | String | "" |
| pin | String | "" |
| isPasswordVisible | Boolean | false |
| isPinMode | Boolean | false |
| isBiometricAvailable | Boolean | false |
| isLoading | Boolean | false |
| error | LoginError? | null |

**Actions**:
- `OnUsernameChange(value: String)` — triggered by typing in username field
- `OnPasswordChange(value: String)` — triggered by typing in password field
- `OnTogglePasswordVisibility` — triggered by tapping eye icon
- `OnLoginClick` — triggered by tapping Login button; calls appropriate API based on clientType
- `OnPinChange(digit: String)` — triggered by tapping PIN digit; auto-submits on 4th digit
- `OnTogglePinMode` — switches between password and PIN entry modes
- `OnBiometricClick` — triggered by tapping fingerprint icon; emits `ShowBiometricPrompt`
- `OnPinSubmit` — auto-triggered when PIN reaches 4 characters

**Events**:
- `NavigateToAdminDashboard(userId: Long, roles: List<String>)` — on admin login success
- `NavigateToEndUserDashboard(clientId: Long, token: String)` — on end-user login success
- `ShowBiometricPrompt` — triggers OS biometric dialog

**DI**: AuthRepository, SessionManager, BiometricManager, PinManager, SyncQueueRepository

## Navigation

| From | To | Condition | Params |
|------|----|-----------|--------|
| app_launch (no session) | client-type-selector | no_saved_session | — |
| logout | client-type-selector | user_logged_out | — |
| client-type-selector | login | user_selects_admin | client_type: admin |
| client-type-selector | login | user_selects_end_user | client_type: end_user |
| login | admin-dashboard | admin_login_success | userId: Long, roles: List\<String\> |
| login | personal-dashboard | end_user_login_success | clientId: Long, selfServiceToken: String |
| login | client-type-selector | user_taps_back | — |

## API Endpoints

| ID | Method | Path | Auth | Cache |
|----|--------|------|------|-------|
| authenticate_admin | POST | /authentication | None (pre-auth) | no-cache |
| authenticate_end_user | POST | /self/authentication | None (pre-auth) | no-cache |

## Design Tokens Used

- `primaryContainer` — admin tile background (#A6F1A6 light)
- `onPrimaryContainer` — admin tile icon + label tint (#002106 light)
- `secondaryContainer` — member tile background (#FFDDB3 light)
- `onSecondaryContainer` — member tile icon + label tint (#2A1700 light)
- `primary` — login button fill, biometric border, PIN filled dots (#2E7D32 light)
- `onPrimary` — top bar title, login button text (#FFFFFF)
- `onSurface` — login title, username/password text (#1A1C19 light)
- `onSurfaceVariant` — subtitle text, back icon (#424942 light)
- `errorContainer` — error banner background (#FFDAD6 light)
- `onErrorContainer` — error banner text (#410002 light)
- `surface` — login screen background (#FAFAFA light)
- `outline` — app version label (#727971 light)
- `outlineVariant` — PIN empty dots (#C2C9BD light)
- Shape token `lg` (16dp) — tile corner radius
- Shape token `md` (12dp) — PIN pad corner radius
- Shape token `full` (9999dp) — login button corner radius
- Elevation level_2 (3dp) — client type tile cards
