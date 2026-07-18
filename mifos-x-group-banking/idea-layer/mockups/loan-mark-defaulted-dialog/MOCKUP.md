# Mark Loan Defaulted Dialog — Mockup Specification

**Feature**: loan-mark-defaulted-dialog | **Route**: `/groups/{groupId}/loans/{loanId}/mark-defaulted` (modal overlay on `loan-detail`) | **Type**: dialog
**Feature group**: loan-management | **Parent screen**: loan-detail
**Generated from**: `screens/loan-mark-defaulted-dialog/ui.yaml`, `screens/loan-mark-defaulted-dialog/demo-data.yaml`, `screens/loan-mark-defaulted-dialog/api.yaml`, `screens/loan-mark-defaulted-dialog/flow.yaml`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-mark-defaulted-dialog`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density, elevated dialog surface
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — NOT used on this destructive surface
**Danger**: `#B71C1C` on `#FFCDD2` — Mark Defaulted CTA, warning icon tint, error copy
**On-danger**: `#FFFFFF` — CTA label
**Outline**: `#79747E` — Cancel button border
**Surface**: `#FFFFFF` dialog · `#FAFAFA` app-behind (scrim `rgba(0,0,0,0.32)`)
**On-surface**: `#1C1B1F` title + body copy · `#49454F` outline-button label
**Corner radius**: 28dp dialog container (MD3 default) · 24dp filled CTA · 20dp outlined Cancel
**Elevation**: 6dp modal dialog above scrim
**Min touch target**: 48dp on both action buttons
**Dialog width**: 312dp (mobile) / 400dp (tablet), auto-height
**Scrim**: `rgba(0,0,0,0.32)` covers `loan-detail` behind (tap outside → OnDismiss)

---

## Screen: Mark Loan as Defaulted (dialog overlay)

### Entry
- Modal opened from **loan-detail** when the chairperson taps the "Mark Defaulted" action row on an ACTIVE / OVERDUE loan (`condition: session.role == chairperson AND loan.status in [ACTIVE, OVERDUE]`).
- Nav params (required): `loanId: Long`, `memberName: String`, `loanAmountKes: Double` — all resolved from the parent screen selection.
- Dismiss returns focus to `loan-detail` with no state change (or with a refresh event on success — see Interaction 3).

### Layout (state: `idle`)

```
╔══════════════════════════════════════════════════╗
║   loan-detail dimmed behind scrim rgba(0,0,0,.32) ║
║                                                    ║
║     ┌────────────────────────────────────────┐    ║
║     │                                          │    ║
║     │        Mark Loan as Defaulted           │    ║  dialog_title · titleLarge, onSurface #1C1B1F
║     │                                          │    ║  centered, 24sp, medium weight
║     │                                          │    ║
║     │                  ⚠                       │    ║  warning_icon · warning_amber
║     │              (48dp, error)               │    ║  48dp · tint #B71C1C · centered
║     │                                          │    ║
║     │                                          │    ║
║     │   This action cannot be undone.          │    ║  warning_body_text · bodyMedium
║     │   Member Peter Otieno's loan of          │    ║  onSurface #1C1B1F · center-aligned
║     │   KES 1,500 will be marked as            │    ║  16dp horizontal padding
║     │   defaulted.                             │    ║  {{memberName}} + {{loanAmountKes | number}}
║     │                                          │    ║
║     │                                          │    ║
║     │                                          │    ║  dialog_actions_row · gap 12dp, arrangement end
║     │             ┌────────┐ ┌──────────────┐  │    ║  padding 16dp 0dp 0dp 0dp
║     │             │ Cancel │ │Mark Defaulted│  │    ║  Cancel — outlined, outline border, onSurface label
║     │             └────────┘ └──────────────┘  │    ║  Mark Defaulted — filled #B71C1C,
║     │                                          │    ║  onError #FFFFFF, corner 24dp
║     └────────────────────────────────────────┘    ║  dialog surface #FFFFFF, corner 28dp, elevation 6dp
║                                                    ║
╚══════════════════════════════════════════════════╝
```

### Demo Data (state: `idle`, from `demo-data.yaml` + ui.yaml)

Bound from the parent `loan-detail` selection — Peter Otieno (loanId `5002`) has an overdue 1,500 KES loan after 3 consecutive missed weekly payments, matching the Mwangaza Women's Group (Kisumu West Branch, KES, weekly repayment) fixture also used by `loan-list`.

| Field           | Value                                                                                 |
|-----------------|---------------------------------------------------------------------------------------|
| `memberName`    | `Peter Otieno`                                                                        |
| `loanAmountKes` | `1500` → rendered as `KES 1,500` via `{{loanAmountKes \| number}}` NumberFormat locale filter |
| `isSubmitting`  | `false`                                                                               |
| `submitError`   | `null`                                                                                |
| `loanId`        | `5002` (nav_param — not rendered, used only for the API call)                          |

Fineract write-off request body (bound at `OnConfirm`; see `demo-data.yaml#WriteOffTransactionRequest`):

| Field             | Value              | Notes                                       |
|-------------------|--------------------|---------------------------------------------|
| `transactionDate` | `09 May 2026`      | `dd MMMM yyyy` — today, computed at submit  |
| `locale`          | `en`               | Project convention                          |
| `dateFormat`      | `dd MMMM yyyy`     | Matches Fineract server expectation         |

Fineract write-off response (bound on success; see `demo-data.yaml#WriteOffResponse`):

| Field        | Value  |
|--------------|--------|
| `officeId`   | `1`    |
| `clientId`   | `1002` |
| `loanId`     | `5002` |
| `resourceId` | `5002` |

---

## States

The ui.yaml declares 3 `states` blocks (`idle`, `submitting`, `error`) — each renders as a distinct dialog surface variant. There is no `loading` or `empty` state (dialog opens instantly with nav-param data; there is nothing to fetch).

### `idle` (see layout above)
Dialog opens with warning icon, body copy referencing `memberName` + `loanAmountKes`, and both action buttons enabled. This is the default surface when the chairperson taps "Mark Defaulted" on `loan-detail`.

- Both buttons enabled and interactive.
- Focus lands on the outlined **Cancel** button (a11y safe default for destructive dialogs — avoids one-tap catastrophic confirm).
- `Enter` key on hardware keyboards triggers Cancel (not Confirm) for the same reason.

### `submitting`
Chairperson tapped **Mark Defaulted**; `LoanRepository.markDefaulted(loanId)` is in flight against `POST /loans/{loanId}/transactions?command=writeoff`.

```
     ┌────────────────────────────────────────┐
     │                                          │
     │        Mark Loan as Defaulted           │
     │                                          │
     │                  ⚠                       │
     │              (48dp, error)               │
     │                                          │
     │   This action cannot be undone.          │
     │   Member Peter Otieno's loan of          │
     │   KES 1,500 will be marked as            │
     │   defaulted.                             │
     │                                          │
     │             ┌────────┐ ┌──────────────┐  │
     │             │ Cancel │ │ ◐  Marking…  │  │  Mark Defaulted → loading_when: isSubmitting
     │             │(disabled)│ │(disabled)   │  │  Cancel disabled to prevent double-tap /
     │             └────────┘ └──────────────┘  │  race with an in-flight write-off
     └────────────────────────────────────────┘
```

- **Mark Defaulted** shows a 20dp indeterminate MD3 circular progress spinner (color `onError` #FFFFFF) in place of the label; button width fixed to prevent layout shift.
- Both buttons are disabled (`aria-disabled="true"`, `pointer-events: none`, 38% alpha) — the destructive network call cannot be cancelled once dispatched.
- Scrim tap is inert during submit — dialog cannot be dismissed until API resolves.
- `cmp-network-monitor.isOnline` guard was already checked BEFORE entering this state; if offline, submit is blocked at the `OnConfirm` handler and no request goes on the wire.

### `error`
API returned a non-2xx response (401/403/404/409/500 per `api.yaml#errors`) OR the network call failed. `submitError` is set on the ViewModel state and rendered inline between the body copy and the action row.

```
     ┌────────────────────────────────────────┐
     │                                          │
     │        Mark Loan as Defaulted           │
     │                                          │
     │                  ⚠                       │
     │                                          │
     │   This action cannot be undone.          │
     │   Member Peter Otieno's loan of          │
     │   KES 1,500 will be marked as            │
     │   defaulted.                             │
     │                                          │
     │   Could not mark loan as defaulted.      │  submit_error_text · bodySmall
     │   Please try again.                      │  error color #B71C1C · center-aligned
     │                                          │  visible_when: submitError != null
     │             ┌────────┐ ┌──────────────┐  │
     │             │ Cancel │ │Mark Defaulted│  │  Both buttons re-enabled;
     │             └────────┘ └──────────────┘  │  Cancel keeps focus per a11y default
     └────────────────────────────────────────┘
```

Error copy (from `ui.yaml#i18n.en`):
- `409` / server rejection → `error_server`: "Could not mark loan as defaulted. Please try again."
- `403` → `error_forbidden`: "You do not have permission to perform this action." (chairperson role check failed server-side)
- `409` state-conflict → `error_ineligible`: "This loan cannot be defaulted in its current state." (loan already CLOSED / already written off)
- `401` → dialog dismisses and app navigates to `login` (session expired — handled at the AuthInterceptor layer, not on this dialog).

---

## Interaction Patterns

1. **Cancel tap** → `OnDismiss` (effect: `none`) → emits `LoanMarkDefaultedDialogEvent.Dismiss` to `loan-detail`. Pure UI state transition — no persistence, no API call, no side effect on the m_loan record. Dialog animates out with MD3 fade+scale (200ms).
2. **Scrim tap (outside dialog)** → `OnDismiss` (same handler as Cancel). Only reachable in the `idle` and `error` states; disabled during `submitting`.
3. **Mark Defaulted tap** → `OnConfirm` (effect: `call_api`, external lib: Fineract via `LoanRepository`, guarded by `cmp-network-monitor`) →
   - Preflight: if `NetworkMonitor.isOffline == true`, do NOT dispatch; set `submitError = "No internet connection. Reconnect and try again."` and remain on the dialog (no offline queue — this action is destructive and must round-trip to the server).
   - Otherwise: `state.isSubmitting = true`, then call `LoanRepository.markDefaulted(loanId)` which POSTs to `/loans/{loanId}/transactions?command=writeoff` with today's date in `dd MMMM yyyy`.
   - **Success**: emit `LoanMarkedDefaulted(loanId)` event to `loan-detail`, invalidate the Store5/SQLDelight `loans` cache (`fresh=true` reload upstream), dismiss the dialog.
   - **Error**: `state.isSubmitting = false`, `state.submitError = <mapped copy>` → dialog transitions to the `error` surface (see above). Chairperson may retry (idempotent per Fineract `command=writeoff` semantics for the same loanId) or Cancel.
4. **Back gesture / hardware back** → same as `OnDismiss` in `idle` / `error`; consumed and ignored in `submitting`.
5. **Enter key on hardware keyboard** → activates Cancel (destructive-safe default), not Confirm.

---

## Accessibility

- Dialog is announced as `role="alertdialog"` with `aria-labelledby=dialog_title` and `aria-describedby=warning_body_text` — screen readers hear the destructive nature immediately.
- Warning icon is decorative — `contentDescription: null` (Compose) / `aria-hidden="true"` (HTML). The destructive intent is carried by the copy, not by color alone (WCAG 1.4.1).
- Both action buttons meet 48dp min touch target and have `contentDescription` — Cancel: "Cancel — do not mark loan as defaulted"; Mark Defaulted: "Mark {{memberName}}'s KES {{loanAmountKes}} loan as defaulted — this cannot be undone".
- Focus trap: `Tab` cycles Cancel → Mark Defaulted → Cancel (both directions); focus cannot leave the dialog while it is open.
- Focus restore: when the dialog closes (success or dismiss), focus returns to the "Mark Defaulted" trigger on `loan-detail`.
- Destructive-safe default: initial focus is on Cancel, and `Enter` maps to Cancel (see Interaction 5). The confirm button is deliberately positioned to the right, away from the reading path start.
- Locales covered: English, Swahili (`Weka Mkopo Kama Mbaya` / `Ghairi`), French (`Marquer comme Défaut` / `Annuler`), Hindi (`ऋण डिफ़ॉल्ट के रूप में चिह्नित करें` / `रद्द करें`) — see `ui.yaml#i18n`.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS; body copy wraps rather than truncates.
- Color contrast: `#B71C1C` on `#FFFFFF` = 6.4:1 (AA large + AA normal); `#1C1B1F` on `#FFFFFF` = 16.7:1.

---

## Motion & Feedback

- Dialog enter: MD3 modal show — scrim fade-in 100ms + dialog scale 0.95 → 1.0 + fade-in 200ms ease-out.
- Dialog exit: MD3 modal hide — dialog scale 1.0 → 0.95 + fade-out 150ms ease-in, scrim fade-out 100ms.
- **Mark Defaulted** press: MD3 ripple (300ms ease-out) then swap label → spinner (opacity crossfade 100ms).
- Cancel press: MD3 outlined ripple, no elevation change.
- `submitting` spinner: MD3 indeterminate 20dp circular, 1400ms rotation, color `onError` #FFFFFF — disabled under `prefers-reduced-motion` (spinner replaced by "Marking…" static label).
- `error` transition: `submit_error_text` fades in 150ms + dialog height animates 200ms ease-out to accommodate the extra row (no layout jump).
- No auto-dismiss on success — parent screen handles the transition (the dialog fades out and `loan-detail` refreshes its loan status badge from ACTIVE/OVERDUE to CLOSED-DEFAULTED).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_loan` (via `LoanRepository`)
**Internal lib**: `cmp-network-monitor`

Read paths: **none** — all three nav_params (`loanId`, `memberName`, `loanAmountKes`) are supplied by the parent `loan-detail` screen at dialog construction; there is no fetch on open.

Write path (irreversible):
- `LoanRepository.markDefaulted(loanId): Flow<Unit>` → `POST /loans/{loanId}/transactions?command=writeoff` with body `{ transactionDate, locale, dateFormat }`.
- On success: repository invalidates the Store5 `loans` cache row for the affected loan (fresh=true stream), which propagates to `loan-list` and the parent `loan-detail` so both re-render with the new CLOSED-DEFAULTED status.
- No offline queue — destructive actions require an online round-trip (Interaction 3 preflight).

Guard: `cmp-network-monitor.isOnline` MUST be `true` before dispatching the POST. Offline attempts short-circuit into the `error` state without touching the wire.

Analytics events emitted (per `docs.yaml#legacy_metadata.analytics.events`):
- `loan_default_dialog_opened { loan_id, member_name }` — fired on entry.
- `loan_default_confirmed { loan_id }` — fired on `OnConfirm` before the POST.
- `loan_default_success { loan_id }` — fired on 2xx response.
- `loan_default_error { loan_id, error }` — fired on non-2xx or network error.
- `loan_default_dialog_dismissed { loan_id }` — fired on `OnDismiss` (Cancel or scrim tap).

---

## Related Artifacts

| Type                        | Path                                                                                       |
|-----------------------------|--------------------------------------------------------------------------------------------|
| Screen YAML                 | `idea-layer/screens/loan-mark-defaulted-dialog/ui.yaml`                                    |
| API contract                | `idea-layer/screens/loan-mark-defaulted-dialog/api.yaml`                                   |
| Data flow                   | `idea-layer/screens/loan-mark-defaulted-dialog/data-flow.yaml`                             |
| Demo data                   | `idea-layer/screens/loan-mark-defaulted-dialog/demo-data.yaml`                             |
| Flow                        | `idea-layer/screens/loan-mark-defaulted-dialog/flow.yaml`                                  |
| Tests                       | `idea-layer/screens/loan-mark-defaulted-dialog/tests.yaml`                                 |
| Preview HTML                | `idea-layer/screens/loan-mark-defaulted-dialog/preview/*.html`                             |
| Stitch prompts (per state)  | `idea-layer/screens/loan-mark-defaulted-dialog/prompts/{idle,submitting,error}.md`         |
| Stitch mockup (deferred)    | `idea-layer/mockups/loan-mark-defaulted-dialog/stitch/…` (regenerate on next Stitch pass)  |
| Feature-group mockup        | `idea-layer/mockups/loan-management/MOCKUP.md`                                             |
| Parent screen mockup        | `idea-layer/mockups/loan-detail/MOCKUP.md`                                                 |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` (3 states, 5 components, i18n × 4 locales) + `demo-data.yaml` (Peter Otieno / 1500 KES / loanId 5002) + `api.yaml` (`POST /loans/{loanId}/transactions?command=writeoff`) + `flow.yaml` (`on_confirm` / `on_dismiss` handlers) + `design-system/DESIGN.md` tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- This is a **destructive irreversible** confirmation dialog — the UX contract deliberately weights against accidental confirm: focus lands on Cancel, `Enter` maps to Cancel, and the red CTA sits to the right (away from the reading path start).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-mark-defaulted-dialog
  ```
- Design conformance verifier: any hand-edit to `ui.yaml` components / states / i18n triggers `needs_generate_mockup` on the next `/idea-sync` cascade; MOCKUP.md is regenerated (not hand-edited).
