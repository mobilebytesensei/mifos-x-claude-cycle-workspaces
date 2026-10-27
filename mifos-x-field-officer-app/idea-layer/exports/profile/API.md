<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: profile
sources:
  - screens/profile/api.yaml
  - screens/profile/data-flow.yaml
  - dtos/AppUser.yaml
  - dtos/ChangePasswordRequest.yaml
  - dtos/PostAuthenticationRequest.yaml
  - dtos/PostAuthenticationResponse.yaml
-->

# API — Profile

Over the existing authenticated Ktor client. Probed live on the gateway 2026-10-27 (fieldofficer @
apis.mifos.community, tenant mifos-bank-1). Password probes sent MISMATCHED pairs only; the password never
changed (re-sign-in with the old password: 200).

## Reads

| id | Method · path | Permission | Notes |
|---|---|---|---|
| session | local — `ProjectPreferencesRepository.fineractUser` | — | userId, username, officeId, officeName, roles, permissions; offline-safe |
| get_user | `GET users/{userId}` | READ_USER | **same store + key as Home** (`DashboardRepository.userStream`). fields: firstname, lastname, email, officeName, staff{id, displayName}, selectedRoles. fieldofficer → IRVING ZEPEDA, staff null |
| get_staff | `GET staff/{staffId}` | READ_STAFF | only when staff present; `isLoanOfficer` for the chip; 403 → "Staff" |
| server | local — `ServerConfigRepository` + `ServerInstancesStore` | — | instance name, live flag, URL, tenant |

## Writes

| id | Method · path | Body | Result |
|---|---|---|---|
| change_password | `POST users/{userId}/pwd` | `{password, repeatPassword}` (`dtos/ChangePasswordRequest.yaml`) | 2xx → success (body unmeasured). 400 → `errors[].defaultUserMessage[]` shown one per line. 403 → `defaultUserMessage` |
| change_password (fallback) | `PUT users/{userId}` | same | needs UPDATE_USER; admin edit path — fallback only |
| reauthenticate | `POST authentication` | `{username, password: new}` | replaces the stored key; failure → sign out keeping data |

## Server validation (measured)

- policy: "Password must be 12 to 50 characters long, containing at least one uppercase letter, one lowercase
  letter, one numeric digit, and one special character, with no spaces or consecutive repeating characters"
- `repeatPassword`: "The parameter `repeatPassword` is not equal to password."
- envelope `defaultUserMessage: "Validation errors exist."` is NOT shown — the per-error messages are.

## Never

The password is never logged, cached, put in a Store, or kept after the sheet closes; only the re-sign-in
writes it to the session store, exactly as sign-in already does.
