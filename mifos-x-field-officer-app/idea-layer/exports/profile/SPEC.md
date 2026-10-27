<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: profile
generated_from_feature_version: "1.2"
sources:
  - screens/profile/docs.yaml
  - screens/profile/ui.yaml
  - screens/profile/api.yaml
  - screens/profile/flow.yaml
  - screens/profile/data-flow.yaml
  - screens/profile/tests.yaml
  - flows/account.yaml
  - journeys/field-officer-checks-account.yaml
  - design-system/design-tokens.yaml
  - REQUIREMENTS.md (FR-PRO-01..06, NFR-PRO-01)
design_tier_consumed: stitch          # RULE-UI-SOURCE-001 US9: all 5 states — mockups/profile/stitch/0{1..5}-profile-*
-->

# SPEC — Profile

The signed-in officer's own account, opened from the Home avatar (the navigation drawer whose header used to
open it was removed 2026-10-27). Who am I signed in as, which office do my Home figures cover, which server
am I on — plus Change password and Sign out. Offline it shows the identity saved at sign-in.

| | |
|---|---|
| Feature id | `profile` |
| Module | `feature/profile` (template backbone) — the fork body lives in `identity/` behind `BackboneRegistry.profileBody` |
| Route | `ProfileRoute` (no params) — registered on the OUTER authenticated graph; opened by `HomeNavigation.Profile` |
| Bottom nav | **no** — detail shell: back arrow + "Profile" (`ui.yaml#shell`) |
| Business logic | `composite` — `content_input_submit`, `NETWORK_WITH_CACHE` read + one SubmitHandler write |
| Version | 1.2 |

## Decisions (docs.yaml)

| id | decision |
|---|---|
| opened-from-home-avatar | the Home avatar is the only entry; no tab, no drawer |
| identity-from-two-sources | session (username, userId, office, roles) renders at once + offline; `GET users/{id}` adds name, email, staff link |
| scope-is-home-scope | "My portfolio" with a staff link, else `Office: <name>` — Home's rule, not recomputed |
| change-password-re-signs-in | after a 200, sign in again with the new password and store the new key; on failure sign out keeping data |
| password-path | `POST users/{id}/pwd`; `PUT users/{id}` only as fallback; each server message shown, the app never enforces its own policy copy |
| sign-out-shared-with-settings | the Settings `SignOutDialog` + `SignOutViewModel`; Settings keeps its row |
| detail-shell | back arrow + title; today's screen has no app bar |

## Screens

| Screen | ViewModel | States (ui.yaml) |
|---|---|---|
| `ProfileScreen` (template shell) → `ProfileBody` (fork, `identity/`) | `ProfileViewModel` | loading · content · error · offline · change_password (sheet) |

The template `ProfileScreen` is a bare `KptScaffold` with no top bar. The fork body draws its own app bar with
the back arrow, so the template shell stays untouched.

## Components (ui.yaml → testTag)

| Component | testTag | States | Contents |
|---|---|---|---|
| back | `profile_back` | all | pops to Home |
| offline_banner | `profile_offline_banner` | offline | "You're offline. This is the account saved when you signed in." |
| identity_card | `profile_identity` | all | 72dp initials disc (same initials + tint as the Home avatar) · full name · username · email (if present) · Loan officer / Staff chip (only with a staff link) |
| name_error_banner | `profile_name_error` + Retry `profile_retry` | error | "Couldn't load your name from the server." + server reason |
| office row | — | all | Office · value |
| scope_row | `profile_scope` | all | "What Home shows" · `Office: CENTRAL` or `My portfolio` · supporting note |
| roles_section | `profile_roles` | all | one outlined chip per `session.roles[].name` |
| session_card | `profile_session` + `profile_server_settings` | all | instance + Live badge (online) · Server URL · Tenant · Server settings → ServerConfig |
| account_actions | `profile_change_password` · `profile_sign_out` | all | Change password (disabled offline, with reason) · Sign out (error colour) |
| change_password_sheet | `profile_password_sheet` · `profile_new_password` · `profile_repeat_password` · `profile_password_cancel` · `profile_password_save` | change_password | lead line · new (with policy hint) · repeat (mismatch error) · server errors · Cancel / Save password (disabled until both filled + equal + not submitting) |

## State Model

```
ProfileState(
  username: String, initials: String,          // session — never empty while signed in
  officeName: String, roles: List<String>,     // session
  fullName: String?, email: String?,           // users/{id}; null while loading / on error
  staffName: String?, isLoanOfficer: Boolean?, // users/{id}.staff + staff/{id}
  scopeLabel: ScopeLabel,                      // MyPortfolio | Office(name)
  nameState: ScreenState<Unit>,                // loading / error(reason) / content for the name read only
  online: Boolean,
  server: ServerSession(instanceName, isLive, url, tenant),
  password: PasswordForm?,                     // null = sheet closed
)
PasswordForm(new: String, repeat: String, submitting: Boolean, serverErrors: List<String>)
  mismatch = repeat.isNotEmpty() && repeat != new
  canSave  = new.isNotEmpty() && repeat.isNotEmpty() && !mismatch && !submitting
```

Screen state is derived: `loading` while the name read has nothing cached, `error` when it failed with
nothing cached, `offline` overlay when the device is offline, `change_password` while the sheet is open.
The identity block never blanks (NFR-PRO-01).

## Data (layers)

| Layer | Adds |
|---|---|
| `core/network` | `UserApi.changePassword(userId, ChangePasswordRequest)` → `POST users/{id}/pwd`; `StaffApi.getStaff(id)` if not already present |
| `core/data` | `ProfileRepository.changePassword(userId, new, repeat): Result<Unit>` mapping 400 `errors[].defaultUserMessage` to a list; reuses `DashboardRepository.userStream(userId)` for the name and `AuthCommandRepository` for the re-sign-in |
| `feature/profile/identity` | `ProfileViewModel` (actions per docs.yaml#vm_actions), `ProfileBody` with app bar + sheet, strings ×20 |
| `cmp-navigation` | already done: `HomeNavigation.Profile` → `navigateToProfile()`, `profileDestination` on the outer graph |

## Navigation (flow.yaml)

| Trigger | Target |
|---|---|
| back | Home |
| Server settings | `serverConfig` |
| Sign out confirmed / re-sign-in failed | sign-in (session cleared → RootNavViewModel) |

## Design (Stitch, consumed per state)

Left-aligned identity block: 72dp `primaryContainer` disc with indigo initials and a white ring, the name in
headline-small; everything below is a quiet grouped list on white 16dp-radius bordered cards (56dp rows, icon
+ label + value). Section headings small and muted. The Live pill is the only green; Sign out the only red.
Error: one rose inline strip under the identity, rest unchanged. Offline: amber banner on top, Change password
greyed with its reason. Sheet: 28dp top corners over a 42% scrim, outlined fields, policy hint, mismatch in
error colour, Save disabled.

## Testing

`tests.yaml` — 10 scenarios (6 high · 3 medium · 1 low). Journey `field-officer-checks-account` (5 steps).
Implement as `ProfileViewModelTest` (state derivation, scope rule, mismatch/canSave, submit success → reauth,
400 → server errors, reauth failure → sign out), `ProfileBodyUiTest` (testTags, sheet), previews + Roborazzi
goldens per state.

## Known Gaps

| Gap | Why | Rendered as |
|---|---|---|
| Fork body in a template-synced module | `feature/profile` is in `SYNC_DIRS` (backbone); `identity/` is fork code inside it, as it already is today | recorded; a template sync must keep `identity/` (verify on the next `/kmp-project-template-sync`) |
| Success body of the password change unmeasured | probes used mismatched pairs on purpose | treat any 2xx as success |
| Gateway demo user has no staff link | measured | the Loan officer chip + "My portfolio" are tested with a fake staff-linked user |
| Stitch renders section headings in capitals | Stitch style | code uses the sentence-case strings |
