# API — User Profile

Client contracts for `profile`. This project owns no backend: these are Ktorfit contracts against
the OBP sandbox, not owned schema.

---

## obp_get_user_profile

| | |
|---|---|
| Endpoint | `GET /obp/v4.0.0/users/current` |
| Trigger | `on_screen_load` |
| Consumer | `ProfileRepository` → `ProfileViewModel.load()` |
| Wired | yes |

**Response fields**

| Field      | Type   | Maps to                                                        |
|------------|--------|-----------------------------------------------------------------|
| `user_id`  | String | Not rendered — identity only                                    |
| `username` | String | `displayName` (falls back to the email local-part when blank), and `initials` derived from it |
| `email`    | String | `email` → `profile_email_field`                                 |

**Not returned by this endpoint**

`phone` has no source field. `ProfileContent.phone` is hardcoded `""`, so `profile_phone_field`
renders permanently empty. This is an OBP UserProfile limitation, not a mapping gap — recorded so
it is not "fixed" by inventing a source.

`fullName` is not a distinct field either: shipped binds it to the same value as `displayName`.

**Errors**

| Code | Name          | UI message                     | State |
|------|---------------|--------------------------------|-------|
| 401  | AUTH_ERROR    | "Could not load your profile"  | error |
| 500  | NETWORK_ERROR | "Could not load your profile"  | error |

Both resolve to the same `error` state — icon `error_outline`, title "Could not load your profile",
body "Check your connection and try again.", Retry → `onRetry()`. `ScreenState.Error` carries
`isNetworkError`, so the two are distinguishable in state even though the copy is shared.

---

## obp_update_user_profile — DECLARED, DEFERRED

| | |
|---|---|
| Endpoint | `PUT /obp/v4.0.0/users/current` |
| Trigger | `deferred` |
| Wired | **no** |

No request or response shape is declared, and nothing calls it. This is the endpoint an editable
profile would require; its deferred state is why the screen is specified read-only — no editing, no
save, no avatar upload — rather than treated as an unfinished form.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/profile/api.yaml. -->
