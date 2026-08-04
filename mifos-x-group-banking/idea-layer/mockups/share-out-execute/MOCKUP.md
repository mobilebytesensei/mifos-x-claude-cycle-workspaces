# Share-Out Execute — Mockup Specification

**Feature**: share-out-execute | **Route**: `/groups/{groupId}/share-out/execute` | **Type**: detail
**Feature group**: share-out | **Flow**: share-out-flow
**Generated from**: `screens/share-out-execute/ui.yaml`, `screens/share-out-execute/demo-data.yaml`, `screens/share-out-execute/preview/*.html` (5 states rendered 2026-07-18)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature share-out-execute`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, Done CTA, progress bar, DONE badges
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis on summary card highlights
**Danger**: `#C62828` (`--danger`) — Execute CTA fill (irreversible action), FAILED badges, ConfirmationRequired copy
**Warning**: `#F57C00` (`--warning`) — offline banner, PartialFailure banner
**Success**: `#2E7D32` on `#C8E6C9` (`--primary-100`) — completion banner background + DONE icon tint
**Muted**: `#616161` on `#F5F5F5` — PENDING status pips, disabled back button
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` filled inputs · `#C8E6C9` primaryContainer summary card
**Corner radius**: 12dp cards + banners · 8dp confirmation text field · 24dp buttons (biometric, execute, done) · full-round icon badges
**Elevation**: 0dp summary card (`primaryContainer` fill on `--bg-canvas`) · 2dp confirmation card · 2dp rotation card
**Min touch target**: 56dp Execute/Done · 48dp Retry/Biometric · 56dp per-member row

---

## Screen: Execute Share-Out / Execute Rotation Payout

The title and Execute button label are STRATEGY-ADAPTIVE — driven by `typeConfig.shareoutFormula`:
- `PRORATA_SHARES | PRORATA_SAVINGS | EQUAL` → **"Execute Share-Out"** (ACCUMULATING · VSLA/ASCA/SHG/SILC · COMP-DIST-001)
- `FIXED_ORDER | LOTTERY | AUCTION` → **"Execute Rotation Payout"** (ROTATING_PAYOUT · ROSCA/chit · COMP-DIST-002)

For `ROTATING_PAYOUT` the `member_payout_row` list is replaced by a single `rotation_execute_card` naming the next recipient.

### Entry

- From **share-out-preview** — the operator (viewer role ∈ {ORGANIZER, TREASURER, CHAIRPERSON}) taps "Confirm & Execute"; nav-params: `{ groupId, typeConfig, totalPool, memberPayouts }`. For `ROTATING_PAYOUT` the `memberPayouts` list is empty and the recipient is derived from the group's current rotation slot.
- Back navigation (`OnBack` → `NavigateBack`) is **enabled only while `!isExecuting && !isCompleted`**; once the operator taps Execute the back icon greys out to prevent abandonment mid-execution.
- On completion (or offline queue) Done (`OnDone` → `NavigateToGroupDashboard(groupId)`) pops the entire share-out subgraph and lands on the group dashboard, which re-reads the advanced cycle / rotation state.

### Layout (state: `content` — ACCUMULATING · double-confirmation gate)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Execute Share-Out       [#2E7D32]  │  top_bar — primary green, onPrimary text
│                                          │  nav_enabled_when: !isExecuting && !isCompleted
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Total Distribution Pool            │ │  summary_card · primaryContainer fill
│  │                                    │ │  labelMedium onPrimaryContainer
│  │ KES 24,000                         │ │  headlineSmall, bold, onPrimaryContainer
│  │ 5 members to receive payouts       │ │  bodyMedium onPrimaryContainer, +4dp
│  └────────────────────────────────────┘ │  corner 12dp, elevation 0dp, m: 16 16 0
├─────────────────────────────────────────┤
│  Member Payouts                          │  payout_list_header · titleSmall,
│                                          │  onSurfaceVariant, p: 16 16 4
├─────────────────────────────────────────┤
│  ( AW )  Amina Wanjiru         ○ pend    │  member_payout_row · list-item · 56dp min
│         KES 6,792 (28%)                  │  supporting: bodyMedium, primary color
├─────────────────────────────────────────┤  divider: true
│  ( JK )  Joseph Kamau          ○ pend    │  avatar 40dp secondaryContainer,
│         KES 5,208 (22%)                  │  initials from memberInitials
├─────────────────────────────────────────┤
│  ( GW )  Grace Wanjiku         ○ pend    │  trailing icon_badge hidden while
│         KES 4,800 (20%)                  │  !isExecuting && !isCompleted && !queuedOffline
├─────────────────────────────────────────┤
│  ( PO )  Peter Otieno          ○ pend    │
│         KES 4,392 (18%)                  │
├─────────────────────────────────────────┤
│  ( MA )  Mary Akinyi           ○ pend    │
│         KES 2,808 (12%)                  │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Confirm Share-Out                  │ │  double_confirmation_section · card
│  │ This action is irreversible.       │ │  bodySmall onSurfaceVariant
│  │ Type "SHARE OUT" below or use      │ │
│  │ biometric authentication.          │ │
│  │                                    │ │
│  │ ┌────────────────────────────────┐ │ │
│  │ │ Confirmation                   │ │ │  confirmation_text_field · 48dp min
│  │ │ Type "SHARE OUT"               │ │ │  corner 8dp; error_text shown when
│  │ └────────────────────────────────┘ │ │  confirmationText.isNotBlank && !isConfirmed
│  │                                    │ │  → OnConfirmationTextChanged (transform_state)
│  │ ┌───── 🔒 Use Biometric ────────┐ │ │  biometric_button · outlined, 24dp round,
│  │ └────────────────────────────────┘ │ │  full-width, +12dp margin_top
│  │                                    │ │  → OnBiometricSelected (transform_state)
│  └────────────────────────────────────┘ │  → ShowBiometricPrompt event
├─────────────────────────────────────────┤
│  ┌──────── Execute Share-Out ────────┐  │  execute_button · filled DANGER (#C62828)
│  └────────────────────────────────────┘ │  onError text, 24dp round, 56dp min
│                                          │  enabled_when: isConfirmed && !isExecuting
│                                          │  loading_when: isExecuting
│                                          │  → OnExecute (call_api COMP-DIST-001)
└─────────────────────────────────────────┘
```

### Layout (state: `content` — ROTATING_PAYOUT variant)

```
┌─────────────────────────────────────────┐
│ [‹]  Execute Rotation Payout [#2E7D32]  │  top_bar title flips to "Rotation Payout"
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │  summary_card
│  │ Total Distribution Pool            │ │
│  │ KES 30,000                         │ │
│  │ 1 recipient (rotation)             │ │  poolModel == ROTATING_PAYOUT copy
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Rotation Payout                         │  payout_list_header (rotation variant)
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Paying out to                      │ │  rotation_execute_card · secondaryContainer
│  │ Grace Wairimu                      │ │  headlineMedium bold onSecondaryContainer
│  │ Amount     KES 30,000              │ │  labeled-value titleLarge
│  └────────────────────────────────────┘ │  member_payout_row list HIDDEN
├─────────────────────────────────────────┤
│  ┌ Confirm — Type "SHARE OUT" or 🔒 ─┐ │  double_confirmation_section — same as above
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌─── Execute Rotation Payout ───────┐  │  execute_button label flips
│  └────────────────────────────────────┘ │  → OnExecute (call_api COMP-DIST-002)
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Five payouts for Mwangaza Women's Group cycle 1 (`PRORATA_SAVINGS`, KES total pool `24,000.00`):

| memberId | Member          | Initials | Total Savings | Share % | Payout (KES) |
|----------|-----------------|----------|---------------|---------|--------------|
| MBR-101  | Amina Wanjiru   | AW       | 6,000         | 28.3%   | 6,792.00     |
| MBR-102  | Joseph Kamau    | JK       | 4,800         | 21.7%   | 5,208.00     |
| MBR-103  | Grace Wanjiku   | GW       | 3,850         | 20.0%   | 4,800.00     |
| MBR-104  | Peter Otieno    | PO       | 3,000         | 18.3%   | 4,392.00     |
| MBR-105  | Mary Akinyi     | MA       | 2,250         | 11.7%   | 2,808.00     |

- **Sum of payouts** = 24,000.00 KES · **totalPool** = 24,000.00 · **totalCount** = 5.
- **`shareoutFormula`** = `PRORATA_SAVINGS` → ACCUMULATING branch → COMP-DIST-001 (`POST /companion/groups/{groupId}/shareout/execute`).
- **ROTATING_PAYOUT** counter-example (from `RotationPayoutExecuteResponse` fixture): Tumaini ROSCA cycle 3 pays `KES 30,000` to `MBR-201` and advances `newRotationPosition: 4` — used to seed the ROTATING_PAYOUT layout snapshot above.
- **`isConfirmed`** starts `false`; the Execute button is DISABLED until the operator either types "SHARE OUT" exactly OR completes the biometric prompt.
- **`isOnline`** default `true` in the seed; the offline banner is dormant unless `NetworkMonitor.isOffline == true`.

---

## States

The ui.yaml declares 5 `screen_state` members (`Content`, `Executing`, `Success`, `PartialFailure`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `content`
Awaiting double-confirmation. Layout as shown above. Chairperson/treasurer/organizer scans the payout list, types the confirmation phrase (or authenticates via biometric), then taps Execute. Back navigation is enabled. Offline banner shows if `!isOnline`.

### `executing`

```
┌ Execute Share-Out ──────────────────────┐
│ [‹]  Execute Share-Out                   │  back icon DISABLED (nav_enabled_when false)
├─────────────────────────────────────────┤
│  ┌ Total Distribution Pool ──────────┐  │  summary_card unchanged
│  │ KES 24,000 · 5 members            │  │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Member Payouts                          │
├─────────────────────────────────────────┤
│  ( AW )  Amina Wanjiru       ✔ done     │  trailing icon_badge NOW visible:
│         KES 6,792 (28%)                  │  DONE → checkmark_circle_24_filled, primary
├─────────────────────────────────────────┤
│  ( JK )  Joseph Kamau        ✔ done     │
│         KES 5,208 (22%)                  │
├─────────────────────────────────────────┤
│  ( GW )  Grace Wanjiku       ↻ in-prog  │  IN_PROGRESS → spinner_ios_20_filled,
│         KES 4,800 (20%)                  │  secondary color, animated: true
├─────────────────────────────────────────┤
│  ( PO )  Peter Otieno        ○ pending  │  PENDING → circle_24_regular, onSurfaceVariant
│         KES 4,392 (18%)                  │
├─────────────────────────────────────────┤
│  ( MA )  Mary Akinyi         ○ pending  │
│         KES 2,808 (12%)                  │
├─────────────────────────────────────────┤
│  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░  2 of 5        │  progress_indicator · linear, height 8dp,
│                                          │  color primary, corner 4dp
└─────────────────────────────────────────┘
```

- `progress_indicator.value = executedCount.toFloat() / totalCount.toFloat()` — advances as each `MemberExecutionStatus` flips PENDING → IN_PROGRESS → DONE (or FAILED).
- Double-confirmation section + Execute button are hidden (`visible_when: !isExecuting && !isCompleted`).
- Per-member row `trailing` uses the icon palette from `member_payout_row.style`: PENDING = neutral, IN_PROGRESS = animated secondary spinner, DONE = primary checkmark, FAILED = red error circle, QUEUED = secondary cloud-arrow-up.

### `success`

```
┌ Execute Share-Out ──────────────────────┐
│ [ ]  Execute Share-Out                   │  back icon disabled (nav_enabled_when false)
├─────────────────────────────────────────┤
│  ┌ Total Distribution Pool ──────────┐  │  summary_card retained
│  │ KES 24,000 · 5 members            │  │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Member Payouts                          │
├─────────────────────────────────────────┤
│  ( AW ) Amina Wanjiru         ✔ done    │  all 5 rows DONE badges (primary #2E7D32)
│  ( JK ) Joseph Kamau          ✔ done    │
│  ( GW ) Grace Wanjiku         ✔ done    │
│  ( PO ) Peter Otieno          ✔ done    │
│  ( MA ) Mary Akinyi           ✔ done    │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │           ✔  (48dp primary)         │ │  completion_banner · primaryContainer
│  │      Share-Out Complete!            │ │  titleLarge, onPrimaryContainer
│  │  KES 24,000 distributed to 5        │ │  bodyMedium, onPrimaryContainer
│  │  members successfully.              │ │
│  └────────────────────────────────────┘ │  corner 12dp, padding 20dp, m: 16 16 0
├─────────────────────────────────────────┤
│  ┌─────────────── Done ───────────────┐ │  done_button · primary fill, 56dp min,
│  └────────────────────────────────────┘ │  24dp round, full-width
│                                          │  → OnDone → NavigateToGroupDashboard(groupId)
└─────────────────────────────────────────┘
```

- ROSCA/rotation success flips the completion banner headline to "Rotation Payout Complete!" (i18n `success_title_rotation`) and the body to "KES {totalPool} paid to {memberPayouts[0].memberName}."
- Response fixture `SOR-20260509-001` (`succeededCount: 5, failedCount: 0, failedMemberIds: []`) drives this preview.

### `partial_failure`

```
┌ Execute Share-Out ──────────────────────┐
│ [ ]  Execute Share-Out                   │
├─────────────────────────────────────────┤
│  ┌ KES 24,000 · 5 members ───────────┐  │  summary_card retained
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Member Payouts                          │
│  ( AW ) Amina Wanjiru       ✔ done      │
│  ( JK ) Joseph Kamau        ✔ done      │
│  ( GW ) Grace Wanjiku       ✔ done      │
│  ( PO ) Peter Otieno        ✔ done      │
│  ( MA ) Mary Akinyi         ✕ FAILED    │  FAILED badge red (#C62828) error_circle
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │  ⚠  Partial Completion              │ │  partial_failure_banner · warningContainer
│  │  4 of 5 payouts succeeded.          │ │  titleMedium onWarningContainer
│  │  1 failed. Tap Retry to re-attempt.│ │  bodySmall onWarningContainer
│  └────────────────────────────────────┘ │  corner 12dp, padding 16dp
├─────────────────────────────────────────┤
│  ┌───── Retry Failed Payouts ────────┐  │  retry_failed_button · secondary fill
│  └────────────────────────────────────┘ │  48dp min, full-width
│                                          │  → OnRetryFailed (call_api COMP-DIST-001)
└─────────────────────────────────────────┘
```

- Driven by fixture `SOR-20260509-002` (`succeededCount: 4, failedCount: 1, failedMemberIds: ["MBR-105"]`).
- Retry re-submits ONLY `failedPayouts[]` — the sync_queue idempotency key prevents double-paying the members that already landed DONE.
- Retry success moves the FAILED row to DONE and demotes the partial banner to the success completion banner (state flips to `success`).

### `error`

```
┌ Execute Share-Out ──────────────────────┐
│ [‹]  Execute Share-Out                   │  back re-enabled
├─────────────────────────────────────────┤
│  ┌ KES 24,000 · 5 members ───────────┐  │  summary_card retained
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Member Payouts (all PENDING pips)       │
│  ( AW ) Amina Wanjiru         ○         │
│  ( JK ) Joseph Kamau          ○         │
│  ( GW ) Grace Wanjiku         ○         │
│  ( PO ) Peter Otieno          ○         │
│  ( MA ) Mary Akinyi           ○         │
├─────────────────────────────────────────┤
│  ⚠  Server error. Please try again.      │  snackbar (ShowSnackbar event) · MD3 4s
├─────────────────────────────────────────┤
│  ┌────── Execute Share-Out ──────────┐  │  execute_button re-enabled for retry
│  └────────────────────────────────────┘ │  → OnExecute
└─────────────────────────────────────────┘
```

Error surfaces mapped to `ShareOutError` types:
- `Network` retry:false, `error_queued_offline` — "You are offline. Payout will execute automatically when you reconnect." → the entire request serializes to `sync_queue` (priority 100, HIGH) and the screen flips to the `queued_offline_banner` variant (see below).
- `Server` retry:true, `error_server` — "Server error. Please try again." Execute button re-enabled.
- `Auth` retry:false, `error_auth` — "Session expired. Please log in again." → redirect to `login`.
- `PartialFailure` retry:true, `error_partial` — handled as its own `partial_failure` state.
- `ConfirmationRequired` retry:false, `error_confirmation_required` — 'Please type "CONFIRM" or use biometric to confirm.'

### Offline queue variant (composed on top of `content` when `queuedOffline == true`)

```
┌ Execute Share-Out ──────────────────────┐
│  ⚠  You are offline. Share-out will be   │  offline_info_banner · warningContainer
│     queued and executed automatically    │
│     when you reconnect.                  │
├─────────────────────────────────────────┤
│  ( AW ) Amina Wanjiru       ⛅ queued    │  trailing icon_badge QUEUED →
│         KES 6,792 (28%)                  │  cloud_arrow_up_24_regular, secondary
│  … (all 5 rows QUEUED)                   │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Queued for Sync                    │ │  queued_offline_banner · secondaryContainer
│  │ 5 payouts queued. They will be     │ │  titleSmall + bodySmall
│  │ processed automatically when you   │ │
│  │ reconnect.                         │ │
│  └────────────────────────────────────┘ │  corner 12dp, padding 16dp
├─────────────────────────────────────────┤
│  ┌─────────────── Done ───────────────┐ │  done_button visible (queuedOffline branch)
│  └────────────────────────────────────┘ │  → OnDone → NavigateToGroupDashboard(groupId)
└─────────────────────────────────────────┘
```

- Backing sync_queue rows (`SyncQueueItem` fixtures): `entityType: SHARE_OUT_EXECUTE` for ACCUMULATING, `entityType: ROTATION_PAYOUT_EXECUTE` for ROSCA — both `priority: 100`, `status: PENDING`, drained by the background sync worker on connectivity restoration.

---

## Interaction Patterns

1. **Confirmation text edit** → `OnConfirmationTextChanged(text)` (effect: `transform_state`) — updates `confirmationText` per keystroke; flips `isConfirmed = true` only when the entry matches `"SHARE OUT"` verbatim. Error text renders inline once the field is non-blank AND not yet confirmed.
2. **Biometric tap** → `OnBiometricSelected` (effect: `transform_state`) — emits `ShowBiometricPrompt`; the platform prompt via `BiometricManager` returns success → `isConfirmed = true`. No network, no persistence — only the local confirmation flag flips.
3. **Execute tap** → `OnExecute` (effect: `call_api`, external: `ktor-client`) — branch on `poolModel`:
   - `ACCUMULATING` → `POST /companion/groups/{groupId}/shareout/execute` (COMP-DIST-001) with `memberPayouts[]` body. Server records `dt_share_out` and drains each member's `savingsaccounts/{id}/transactions` withdrawal via Fineract.
   - `ROTATING_PAYOUT` → `POST /rotation/execute` (COMP-DIST-002) with the single recipient. Server advances the `rosca_rotation` slot.
   - Per-member `MemberExecutionStatus` streams PENDING → IN_PROGRESS → DONE/FAILED for the progress indicator.
   - Offline: entire request serialized to HIGH-priority `sync_queue`, screen flips to `queued_offline_banner` variant, Done becomes the sole CTA.
   - `writes_to`: `share_out_record`, `member_savings_accounts`, `sync_queue`, `shareout_execution_log`.
4. **Retry failed tap** → `OnRetryFailed` (effect: `call_api`, external: `ktor-client`) — re-submits `failedPayouts` subset to COMP-DIST-001; idempotency key blocks double-payment. Rows flip FAILED → DONE, `succeededCount` increases, banner demotes to `completion_banner` on full recovery.
5. **Back tap** → `OnBack` (effect: `navigate`) — emits `NavigateBack` to `share-out-preview`. Enabled ONLY while `!isExecuting && !isCompleted`; abandons the un-executed distribution WITHOUT touching corpus / payouts / sync_queue.
6. **Done tap** → `OnDone(groupId)` (effect: `navigate`) — emits `NavigateToGroupDashboard(groupId)`; leaves the completed (or offline-queued) execute screen and re-lands on the group dashboard, which re-reads the advanced cycle / rotation state. Pure navigation — the distribution is already executed or queued.

---

## Accessibility

- Execute button uses `danger` semantic colour (`--danger` `#C62828`) — supplemented by explicit copy ("This action is irreversible") and the double-confirmation gate; colour alone never signals destructiveness.
- Confirmation text field enforces `48dp` min touch target and 8dp corner; error copy is a labelSmall row anchored beneath the field with role `alert` so screen readers announce the mismatch.
- Biometric button uses the outlined variant with `fingerprint_24_regular` icon + label — screen readers announce "Use Biometric Instead, button" not the icon glyph.
- Per-member `trailing` icon_badge carries both an icon AND a status word semantic (PENDING / IN PROGRESS / DONE / FAILED / QUEUED) — never colour-only.
- Progress indicator label ("2 of 5 payouts completed") is a live region so assistive tech announces execution advancement.
- Locales covered: English, Swahili (`Fanya Mgawanyo` / `Maliza`), French (`Exécuter le Partage` / `Terminer`), Hindi (`शेयर-आउट निष्पादित करें` / `समाप्त`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.

---

## Motion & Feedback

- Execute button loading spinner (`loading_when: isExecuting`) replaces the label with a 300ms MD3 circular indicator; button colour stays `danger`.
- Progress indicator advance: 200ms ease-in-out per tick as `executedCount` increments.
- IN_PROGRESS row spinner: `spinner_ios_20_filled` at 1.2s rotation loop; disabled under `prefers-reduced-motion`.
- DONE row transition: 150ms fade-in on the primary checkmark.
- Completion banner entry: 200ms slide-up + fade under `motion: gentle` preset (`fast:150ms · base:200ms · slow:300ms`, `cubic-bezier(0.4, 0, 0.2, 1)`).
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s — used for `error_server`, `error_queued_offline`, and biometric failure.
- Biometric prompt: platform-native (Android `BiometricPrompt`, iOS Face/Touch ID) — MifosSave does not intercept animation.

---

## Data Flow (ui.yaml `business_logic.kind: crud` · strategy-adaptive)

**External libs**: `ktor-client`, `Fineract m_loan/m_savings`, `Fineract Companion (COMP-DIST-001, COMP-DIST-002)`
**Internal libs**: `cmp-network-monitor`, `cmp-biometric`, `cmp-sync-queue`, `SessionManager`

Read paths (parameters supplied at nav-time):
- `typeConfig` → drives BOTH `shareoutFormula` (branches title + Execute label + COMP-DIST endpoint) AND `poolModel` (drives layout: `member_payout_row` list vs. `rotation_execute_card`).
- `memberPayouts[]` → nav param for ACCUMULATING; empty for `ROTATING_PAYOUT` (single recipient derived from group rotation slot).
- `totalPool` → nav param; also serialized into every sync_queue payload.
- `isOnline` ← `NetworkMonitor.observeConnectivity()` (offline-first primary flag).
- `viewerRole` ← `SessionManager` — screen inaccessible unless role ∈ `{ORGANIZER, TREASURER, CHAIRPERSON}` (enforced upstream in `share-out-preview` navigation guard).

Write paths (all irreversible; gated by `isConfirmed`):
- ACCUMULATING (`PRORATA_SHARES | PRORATA_SAVINGS | EQUAL`) → COMP-DIST-001 `POST /companion/groups/{groupId}/shareout/execute` with `memberPayouts[]` → server writes `share_out_record`, executes per-member `m_savings` withdrawals, appends `shareout_execution_log`.
- ROTATING_PAYOUT (`FIXED_ORDER | LOTTERY | AUCTION`) → COMP-DIST-002 `POST /rotation/execute` with single recipient → server advances `rosca_rotation` slot, writes single withdrawal.
- Offline path (either branch): serialize request → `sync_queue` (`priority: 100`, `status: PENDING`) → drained by background worker on `NetworkMonitor` reconnect; idempotency key prevents double-payment.
- Retry path (partial failure): re-submit ONLY `failedPayouts[]` subset to COMP-DIST-001; idempotency key blocks members already DONE.

Legacy raw-Fineract equivalent (replaced by companion endpoints):
```
POST /datatables/dt_share_out/{centerId}
  → for each member: POST /savingsaccounts/{savingsAccountId}/transactions {transactionType: WITHDRAWAL, amount: payoutAmount}
```
The companion endpoint collapses this into a single-call orchestration + `share_out_record` audit row.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/share-out-execute/ui.yaml` |
| API contract | `idea-layer/screens/share-out-execute/api.yaml` |
| Data flow | `idea-layer/screens/share-out-execute/data-flow.yaml` |
| Demo data | `idea-layer/screens/share-out-execute/demo-data.yaml` |
| Flow | `idea-layer/screens/share-out-execute/flow.yaml` |
| Docs | `idea-layer/screens/share-out-execute/docs.yaml` |
| Tests | `idea-layer/screens/share-out-execute/tests.yaml` |
| Preview HTML (content) | `idea-layer/screens/share-out-execute/preview/content.html` |
| Preview HTML (executing) | `idea-layer/screens/share-out-execute/preview/executing.html` |
| Preview HTML (success) | `idea-layer/screens/share-out-execute/preview/success.html` |
| Preview HTML (partial_failure) | `idea-layer/screens/share-out-execute/preview/partial_failure.html` |
| Preview HTML (error) | `idea-layer/screens/share-out-execute/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/share-out-execute/prompts/{content,executing,success,partial_failure,error}.md` |
| Feature-group mockup | `idea-layer/mockups/share-out/MOCKUP.md` (Execute-screen section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (5/5 states rendered 2026-07-18) + ui.yaml + demo-data.yaml + `design-system/DESIGN.md` per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Strategy adaptation is DATA-DRIVEN — the ViewModel reads `typeConfig.shareoutFormula` + `poolModel` from nav-params; the same composable renders both the VSLA/ASCA/SHG/SILC (member list) branch and the ROSCA/chit (single-recipient) branch without conditional route split.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features share-out-execute
  ```
- Design conformance verifier: preview HTML mirrors the layouts above; any hand-edit to `ui.yaml` components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
