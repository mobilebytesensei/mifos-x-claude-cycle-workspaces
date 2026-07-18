# Login Signup — Feature Spec

## Overview

Authentication entry-point for the Mifos X Group Banking companion app. Provides unified
self-registration + password login + PIN login in a single screen, with biometric unlock
for returning users. Post-auth routing is group-context-aware: members with ≥1 group go
directly to `GroupListScreen`; zero-group members see a dual CTA to create or join a group.

**Acceptance Criteria:**

- AC1: Toggling between Login and Sign Up mode swaps form fields without navigation.
- AC2: `OnLoginTap` calls COMP-AUTH-002; `OnSignupTap` calls COMP-AUTH-001.
- AC3: After auth success, `groupMemberships` from COMP-AUTH-003 determines routing.
- AC4: Biometric unlock invokes `BiometricManager.authenticate()` — calls COMP-AUTH-003
       on success to refresh the session token.
- AC5: `zero_groups` state shows `OnCreateGroupTap` → `group-type-picker` and
       `OnJoinWithCodeTap` → `join-with-code`.
- AC6: `SessionStore` stores `sessionToken` encrypted in local preferences.
- AC7: Network is required — no offline fallback (auth must be live).

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| login-signup | `LoginSignupScreen` | Single column, center-card | Auth entry-point — mode-toggle header, credential fields, submit button, biometric unlock |

## State Model

### LoginSignupViewModel

**State — `LoginSignupState`**

| Field | Type | Default | Description |
|---|---|---|---|
| mode | AuthMode | `AuthMode.LOGIN` | LOGIN or SIGNUP — drives visible field set |
| name | String | `""` | Display name field (SIGNUP only) |
| emailPhone | String | `""` | Email or phone for both modes |
| password | String | `""` | Password input (obscured) |
| pin | String | `""` | 4-digit PIN for returning users (LOGIN only) |
| isSubmitting | Boolean | `false` | In-flight API call |
| validationErrors | Map<String,String> | `emptyMap()` | Field-level validation messages |
| error | String? | `null` | Top-level error banner message |
| isBiometricAvailable | Boolean | `false` | Controls biometric CTA visibility |
| sessionToken | String? | `null` | Set on successful auth — triggers routing |
| groupMemberships | List<GroupMembership> | `emptyList()` | From COMP-AUTH-003; drives post-login nav |

**Screen States — `LoginSignupScreenState`**

| State | Components |
|---|---|
| `content` | auth_mode_toggle, name_field (SIGNUP), email_phone_field, password_field, pin_field (LOGIN), submit_button, biometric_cta |
| `loading` | shimmer skeleton over fields |
| `error` | error_banner + form fields (non-blocking) |
| `zero_groups` | success_banner, create_group_cta, join_with_code_cta |

**Actions — `LoginSignupAction`**

| Action | Trigger |
|---|---|
| `OnModeToggle` | Tap Sign Up / Log In toggle |
| `OnNameChange(name)` | Text input change |
| `OnEmailPhoneChange(emailPhone)` | Text input change |
| `OnPasswordChange(password)` | Text input change |
| `OnPinChange(pin)` | PIN pad tap |
| `OnLoginTap` | Tap Log In button |
| `OnSignupTap` | Tap Sign Up button |
| `OnBiometricUnlock` | Tap biometric icon |
| `OnCreateGroupTap` | Tap Create Group CTA (zero_groups state) |
| `OnJoinWithCodeTap` | Tap Join with Code CTA (zero_groups state) |
| `OnForgotPassword` | Tap Forgot Password link |

**Events — `LoginSignupEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToPersonalDashboard` | — | `groupMemberships` not empty, no organizer role |
| `NavigateToGroupList` | — | `groupMemberships` not empty, any organizer role |
| `NavigateToGroupTypePicker` | — | `OnCreateGroupTap` in zero_groups state |
| `NavigateToJoinWithCode` | — | `OnJoinWithCodeTap` in zero_groups state |
| `ShowSnackbar` | message: String | Error / success notifications |
| `PromptBiometric` | — | `OnBiometricUnlock` dispatched |

**DI Dependencies**

- `AuthRepository` — wraps COMP-AUTH-001/002/003
- `BiometricManager` — platform expect/actual for biometric prompt
- `SessionStore` — encrypted local preferences for sessionToken
- `NetworkMonitor` — connectivity gate (auth requires online)

## Navigation

| Action | Destination | Params |
|---|---|---|
| Login success + has groups + organizer role | `group-list` | — |
| Login success + has groups + member only | `personal-dashboard` | — |
| Login success + no groups | zero_groups state | — |
| `OnCreateGroupTap` | `group-type-picker` | — |
| `OnJoinWithCodeTap` | `join-with-code` | — |
| Biometric unlock → re-auth | `PersonalDashboard` or `GroupList` | resolved from refreshed groupMemberships |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `companion_self_register` | POST | `/companion/auth/self-register` | COMP-AUTH-001 | yes |
| `companion_login` | POST | `/companion/auth/login` | COMP-AUTH-002 | yes |
| `companion_me` | GET | `/companion/auth/me` | COMP-AUTH-003 | no (cache 300s) |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `session_store` | userId | upsert | local_encrypted_prefs — serve_stale offline |
| `group_memberships_cache` | groupId | upsert | sqldelight_entity — serve_stale 300s |

**Sync Queue:** none (auth requires connectivity; no offline mutation supported).

## DTOs

See `exports/login-signup/API.md` for full DTO schemas.

Key types: `SelfRegisterRequest`, `LoginRequest`, `AuthResponse` (userId, sessionToken,
tokenExpiresAt, groupMemberships), `GroupMembership` (groupId, groupName, role, joinedAt),
`UserProfile`.

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/login-signup/prompts/` (per-state prompt files)
- **Preview HTML:** `idea-layer/screens/login-signup/preview/` (rendered HTML previews)
- **Design conformance:** header card with mode-toggle chip row; email/phone + password field;
  PIN row visible in LOGIN mode only; biometric icon in top-right of submit button row;
  zero_groups state renders two full-width outlined buttons (Create Group / Join with Code).
