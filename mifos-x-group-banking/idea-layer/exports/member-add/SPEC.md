<!--
  generated_from_feature: member-add
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 87)
-->

# Member Add — Feature Spec

## Overview

Single-page form to onboard a new member into a savings group. Fields: first/last name
(required), Kenyan phone number (required, E.164-validated), a photo (camera or gallery picker),
and a role dropdown (chairperson/treasurer/secretary/member). On submit it chains three Fineract
REST calls — `create_client` (POST /clients) → `assign_member_role` (dt_member_role datatable) →
optional `upload_photo` (multipart). Reachability comes from `cmp-network-monitor`; when offline
the operations are enqueued to the SQLDelight `sync_queue` for Store5-backed drain. Photo capture
uses filekit-core. Covers FR-002.

**Route:** `/groups/{groupId}/members/add` · **Entry:** `member-list` (FAB tap)
**Nav params:** `groupId: String (required)`

**Acceptance Criteria:**

- AC1: Form initialises empty; `groupId` captured from nav_params.
- AC2: Required-field + Kenyan-phone (`^(\+254|0)[7][0-9]{8}$`) validation runs inline; invalid
       blocks submit.
- AC3: Photo picker offers camera (filekit-core capture) or gallery; selection stored to photoUri;
       removable.
- AC4: Role dropdown defaults MEMBER; selection sets selectedRole.
- AC5: Online submit chains create_client → assign_member_role → (photoUri != null) upload_photo,
       then `NavigateToMemberProfile`.
- AC6: Offline submit enqueues to sync_queue and emits `ShowOfflineSyncDialog`; duplicate phone →
       `PhoneAlreadyExists` inline on the phone field.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| member-add-screen | `MemberAddScreen` | Form, vertical scroll | Single-page create-member form with photo capture |

## State Model

### MemberAddViewModel

**State — `MemberAddState`**

| Field | Type | Default | Description |
|---|---|---|---|
| firstName | String | `""` | First name (required, ≤50) |
| lastName | String | `""` | Last name (required, ≤50) |
| phone | String | `""` | Kenyan phone (+254 prefix) |
| photoUri | String? | `null` | Selected/captured photo path |
| selectedRole | MemberRole | `MemberRole.MEMBER` | Assigned role |
| validationErrors | Map<String,String> | `emptyMap()` | Per-field errors |
| isSubmitting | Boolean | `false` | Submit chain in flight |
| isSubmitSuccess | Boolean | `false` | Navigate trigger |
| isOffline | Boolean | `false` | Drives offline banner |
| error | MemberAddError? | `null` | Top-level error |
| showPhotoPicker | Boolean | `false` | Photo source bottom sheet |
| groupId | String | `""` | From nav_params |

**Screen States — `MemberAddScreenState`**: `Content`, `Submitting`, `Success`, `Error`

| State | Components |
|---|---|
| `Content` | top_bar, photo_picker_area, first_name_field, last_name_field, phone_field, role_dropdown, offline_banner, save_button |
| `Submitting` | same as Content (save_button loading, fields disabled) |
| `Success` | navigated to member-profile |
| `Error` | Content components + inline error below save button |

**Errors — `MemberAddError`**

| Type | Retry | Message Key | Notes |
|---|---|---|---|
| Validation | no | error_validation | Field-level errors |
| Network | yes | error_network | Offline → fallback queue_offline |
| Server | yes | error_server | 5xx |
| Auth | no | error_auth | 401 → redirect login |
| PhoneAlreadyExists | no | error_phone_exists | Duplicate phone |

**Actions — `MemberAddAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnFirstNameChange` | value | Type first name | transform_state — update + clear error |
| `OnLastNameChange` | value | Type last name | transform_state — update + clear error |
| `OnPhoneChange` | value | Type phone number | transform_state — update + E.164 check |
| `OnPhotoPickerOpen` | — | Tap photo area / camera icon | transform_state — show bottom sheet |
| `OnPhotoCaptured` | uri | Camera capture complete | record_media — filekit-core, store photoUri |
| `OnPhotoSelected` | uri | Gallery image selected | persist_file — filekit-core, store photoUri |
| `OnPhotoRemoved` | — | Tap remove photo | transform_state — photoUri = null |
| `OnRoleSelected` | role | Select role from dropdown | transform_state — set selectedRole |
| `OnSubmit` | — | Tap Save Member | call_api — create_client → role → photo (offline → queue) |
| `OnBack` | — | Tap back / close | navigate — pop to member-list, discard form |

**Events — `MemberAddEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToMemberProfile` | memberId: String, groupId: String | Submit success |
| `NavigateBack` | — | `OnBack` |
| `ShowPhotoPicker` | — | Photo picker open |
| `ShowOfflineSyncDialog` | — | Offline submit queued |
| `ShowSnackbar` | message: String | Errors |

**DI Dependencies**

- `MemberRepository` — createMember, assignRole, uploadPhoto
- `SyncQueueRepository` — offline enqueue
- `ImagePickerHelper` (filekit-core)
- `NetworkMonitor` (cmp-network-monitor)
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Submit success | `member-profile` | memberId, groupId |
| `OnBack` | `member-list` | — |

**navigates_to:** `member-list`, `member-profile`

## API Endpoints (3)

| ID | Method | Endpoint | Writable | Offline op |
|---|---|---|---|---|
| `create_client` | POST | `/clients` | yes | CREATE_MEMBER |
| `assign_member_role` | POST | `/datatables/dt_member_role/{clientId}` | yes | ASSIGN_MEMBER_ROLE |
| `upload_photo` | POST | `/clients/{clientId}/images` (multipart) | yes | UPLOAD_MEMBER_PHOTO |

See `exports/member-add/API.md`.

## Flow Logic

**on_submit:** validate_all (firstName min 2, lastName min 2, phone E164_KE, selectedRole required) →
- on_valid → check network_available:
  - online → create_client → on_success assign_member_role → on_success (photoUri != null) upload_photo → emit NavigateToMemberProfile
  - offline → queue_to_sync_queue → emit ShowOfflineSyncDialog
- on_invalid → show_validation_errors

**on_photo_picker_open:** show bottom_sheet_photo_source.
**phone_validation:** rule `^(\+254|0)[7][0-9]{8}$`, error `error_phone_format`.

## Dependencies

- **Features:** `member-list` (entry/back), `member-profile` (post-create)
- **Libraries:** `cmp-network-monitor`, `cmp-network-monitor-compose`; external: filekit-core,
  SQLDelight, Store5, Fineract REST /clients
- **Required modules:** core/network, core/database, core/store

## DTOs

See `exports/member-add/API.md`. Key types: `CreateMemberRequest`,
`MemberRole` (CHAIRPERSON, TREASURER, SECRETARY, MEMBER).

## Testing (8 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-MAD-001 | P0 | On mount, form empty; groupId captured from nav_params |
| TC-MAD-002 | P0 | Empty required field shows inline error on submit; blocked |
| TC-MAD-003 | P0 | Invalid phone format shows phoneError inline |
| TC-MAD-004 | P0 | Online submit POSTs; emits MemberAdded on success |
| TC-MAD-005 | P1 | PhoneAlreadyExists shown inline on phone field |
| TC-MAD-006 | P0 | Offline submit queues to sync_queue + offline confirmation |
| TC-MAD-007 | P2 | Photo capture opens camera and sets photoUri |
| TC-MAD-008 | P0 | Auth 401 redirects to login-signup |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

> Source note: TC-MAD-004 references a single companion `POST /companion/groups/1/members` call;
> `api.yaml`/`flow.yaml` define the 3-call Fineract chain (create_client → assign_member_role →
> upload_photo). This spec follows `api.yaml` (endpoint SoT); reconcile the test wording.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/member-add/prompts/`
- **Preview HTML:** `idea-layer/screens/member-add/preview/`
- **Design conformance:** circular 120dp `photo_picker_area` (surfaceVariant) shows an add-a-photo
  placeholder or the selected photo with a top-end error-colored remove button; tapping opens the
  `photo_source_bottom_sheet` (camera / gallery). First/last name and phone (+254 prefix, helper
  text) fields surface inline `validationErrors`; the role dropdown defaults MEMBER. A
  tertiaryContainer `offline_banner` (wifi_off) appears when `isOffline`. Full-width primary Save
  button (56dp) shows a loading indicator and disables fields while submitting.
