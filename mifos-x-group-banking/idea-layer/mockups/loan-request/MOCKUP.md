# Loan Request — Mockup Specification

**Feature**: loan-request | **Route**: `/loan-request` | **Type**: form
**Feature group**: end-user-dashboard | **Flow**: end-user-dashboard-flow
**Generated from**: `screens/loan-request/ui.yaml`, `screens/loan-request/demo-data.yaml`, `screens/loan-request/preview/*.html` (5 states)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-request`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, submit button, active slider track, success dialog icon, retry chip
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (savings-limit-card halo — not the base fill)
**Success**: `#1B5E20` on `#C8E6C9` — success dialog check icon, submitted confirmation
**Warning**: `#F57C00` on `#FFE082` — offline banner tint, retryable-error emphasis
**Danger**: `#C62828` on `#FFCDD2` — validation error text, error snackbar background
**Muted**: `#616161` on `#F5F5F5` — supporting text, disabled submit button
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (repayment summary card)
**Corner radius**: `sm` 8dp offline banner · `md` 12dp duration/repayment cards · `lg` 16dp savings-limit-card · full-round submit button + FAB press states
**Elevation**: 0dp savings-limit-card (tertiaryContainer flat) · 1dp duration-selector · 2dp success dialog · 3dp error snackbar
**Min touch target**: 48dp text-field, dropdown, slider thumb, dialog confirm button · 56dp submit button

---

## Screen: Request a Loan

### Entry
- From **personal-dashboard** ("Request a Loan" CTA card); nav-params `clientId: Long`, `savingsBalance: Double`, `loanMultiplier: Double = 3.0`
- From **personal-loans** (FAB `+ Request` on the member's own loan list); same nav-params
- Back navigation pops the route and returns to `personal-loans` (discarding unsaved form per `NavigateBack` action_contract)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Request a Loan          [#2E7D32]  │  top_bar — primary green, onPrimary text, elevation 0dp
├─────────────────────────────────────────┤     back → NavigateBack → personal-loans
│                                          │
│  ┌── SAVINGS LIMIT ─────────────────┐   │  savings_limit_card
│  │ 💰 Your savings balance          │   │    tertiaryContainer · corner 16dp · padding 16dp
│  │    KES 1,200                     │   │    row 1 · bodyLarge, icon `savings`
│  │                                   │   │
│  │ 💵 Maximum you can borrow        │   │    row 2 · titleMedium bold, icon `money`
│  │    KES 3,600  (3× your savings)  │   │    hint: labelSmall onSurfaceVariant
│  └──────────────────────────────────┘   │
│                                          │
│  ┌── Loan Amount (KES) ─────────────┐   │  amount_field · Outlined text-field
│  │  💱  KES  [ 5,000       ]        │   │    leading_icon currency_exchange, prefix "KES"
│  │  Enter amount between KES 500    │   │    keyboard_type number, ime_action next
│  │  and your maximum                │   │    supporting_text · bodySmall onSurfaceVariant
│  └──────────────────────────────────┘   │    error_text renders when requestedAmountError != null
│                                          │    on_change → OnAmountChange(value) → transform_state
│                                          │
│  ┌── Loan Purpose ──────────────────┐   │  purpose_dropdown · Outlined ExposedDropdownMenu
│  │  📝  [ Farming / Agriculture  ▾ ]│   │    leading_icon `notepad` (feature_list)
│  └──────────────────────────────────┘   │    options: SCHOOL_FEES, MEDICAL, BUSINESS,
│                                          │             FARMING, HOME_IMPROVEMENT,
│                                          │             EMERGENCY, OTHER
│                                          │    on_change → OnPurposeSelected(purpose)
│                                          │
│  ┌── Repayment Duration ────────────┐   │  duration_selector · Card surface · corner 12dp
│  │  Repayment Duration              │   │    elevation 1dp · padding 16dp
│  │  ────●────────────────────────   │   │    Slider: min 4 · max 52 · steps 12
│  │  4 wk           12 wk        52wk│   │    active #2E7D32 · inactive primaryContainer
│  │                                   │   │    on_change → OnDurationChanged(weeks)
│  └──────────────────────────────────┘   │
│                                          │
│  ┌── REPAYMENT SUMMARY ─────────────┐   │  repayment_summary_card · surfaceVariant
│  │  Principal            KES 5,000  │   │    corner 12dp · padding 16dp
│  │  Interest (group rate)  KES 415  │   │    visible_when: requestedAmount not blank
│  │  ────────────────────────────    │   │                    && requestedAmountError == null
│  │  Total to repay      KES 5,415   │   │    total row: titleMedium bold, divider above
│  └──────────────────────────────────┘   │    Roboto Mono / SF Mono for amounts
│                                          │
│  ┌────── Submit Application ────────┐   │  submit_button · filled, full-round, min 56dp
│  └──────────────────────────────────┘   │    primary #2E7D32 · onPrimary text
│                                          │    enabled_when: isFormValid && !isSubmitting
│                                          │    on_click → OnSubmitClick → api.submit_loan_request
│                                          │      effect call_api · lib cmp-network-monitor
│                                          │      ext-libs Ktor, SQLDelight
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Four member loan request submissions across a Kisumu VSLA group (KWB-001, KES, PENDING at time of capture):

| clientId | Requested | Purpose (enum: narrative)                                             | Duration | Savings @ req | Submitted            |
|---------:|----------:|-----------------------------------------------------------------------|---------:|--------------:|----------------------|
| 1003     | 5,000     | FARMING: Purchase maize seeds and fertilizer for planting season      | 10 wk    | 1,200         | 2026-07-11 08:30 UTC |
| 1004     | 8,000     | BUSINESS: Buy stock for small grocery kiosk                           | 16 wk    |   950         | 2026-07-11 09:15 UTC |
| 1005     | 3,000     | SCHOOL_FEES: Term-2 school fees for secondary school daughter         |  6 wk    |   750         | 2026-07-11 10:00 UTC |
| 1006     | 2,500     | MEDICAL: Antenatal clinic visit and prescribed supplements            |  8 wk    |   640         | 2026-07-11 10:42 UTC |

- **Purpose column**: on-device the user picks one of the 7 canonical enum values; the concatenated `"ENUM: narrative"` string is what the datatable stores so the organizer sees both category + context at the next meeting.
- **savings × loanMultiplier**: with default `loanMultiplier = 3.0`, `maxLoanAmount` per row = 3,600 · 2,850 · 2,250 · 1,920 — rows 1 and 2 EXCEED the max (would render `requestedAmountError`); rows 3 and 4 are valid. Rendering the layout above uses clientId 1003's amount adjusted-to-max (KES 3,600 shown in savings-limit-card; layout mock uses KES 5,000 as illustrative pre-validation input to demonstrate the summary card).
- **LoanRequestResponse (2 items)** — successful datatable creates: `resourceId 3301 / clientId 1003 / resourceExternalId LR-2026-0711-001` and `resourceId 3302 / clientId 1004 / LR-2026-0711-002`. Rendered in the success dialog post-submit.
- **SyncQueueEntry (2 items)** — offline queue rows: `id 9001` (retryCount 0) and `id 9002` (retryCount 1) both `entityType: LOAN_REQUEST`, `status: PENDING`. Payload is the JSON-serialised `LoanRequestPayload` verbatim; drained by the background sync worker on reconnect.
- **Status default** — Fineract `POST /datatables/dt_loan_request` sets `status = "PENDING"` per `api.yaml`; organizer approves at the next group meeting.

---

## States

The ui.yaml declares 5 `screen_state` members (`Content`, `Submitting`, `SubmitSuccess`, `SubmitError`, `OfflineQueued`) — each renders as a distinct HTML preview surface under `preview/`.

### `content` (see layout above)
Form ready — savings-limit-card populated from nav_params, all fields enabled, `submit_button` disabled until `isFormValid == true`. `repayment_summary_card` appears only after a valid amount is typed.

Validation contract (from `flow.yaml#flow_logic`):
- `requestedAmount.toDouble() > maxLoanAmount` → `requestedAmountError = "Amount exceeds your maximum of KES {{maxLoanAmount}}"`
- `requestedAmount.toDouble() <= 0` → `requestedAmountError = "Amount must be greater than zero"`
- Valid → clear error, recompute `repaymentEstimate` (weekly ≈ `principal * (1 + groupRate) / durationWeeks`).
- `isFormValid = requestedAmount.isValid && purpose != null && durationWeeks in 4..52`.

### `submitting`

```
┌ Request a Loan ────────────────────────┐
│  [savings-limit-card — dimmed]          │  fields disabled (alpha 0.6, pointer-events none)
│  [amount_field — disabled]              │
│  [purpose_dropdown — disabled]          │
│  [duration_selector — disabled]         │
│  [repayment_summary_card]               │
│                                          │
│                ⟳                        │  submitting_indicator · CircularProgress
│           (spinning)                     │    32dp · primary #2E7D32 · center · marginTop 24dp
│                                          │    visible_when: isSubmitting == true
└─────────────────────────────────────────┘
```

- Ktor POST is in flight; `submit_button` swapped out for the circular indicator.
- IME dismissed on `OnSubmitClick`; back-press is soft-blocked (system nav still available; no data loss because the payload is already in flight).

### `submit_success` (online)

```
┌ Request a Loan ────────────────────────┐
│  [savings-limit-card]                   │
│  [amount_field]                          │
│  [purpose_dropdown]                      │
│  [duration_selector]                     │
│  [repayment_summary_card]                │
│  [submit_button]                         │
│                                          │
│      ╔════════════════════════════╗     │  success_dialog · MD3 AlertDialog
│      ║          ✓                 ║     │    icon check_circle · tint primary #2E7D32
│      ║   Request Submitted!       ║     │    icon size 48dp
│      ║                            ║     │    title · titleLarge
│      ║  Your loan request has     ║     │    body · bodyMedium onSurfaceVariant
│      ║  been submitted. It will   ║     │
│      ║  be reviewed by the group  ║     │
│      ║  at the next meeting.      ║     │
│      ║                            ║     │
│      ║        ┌────────┐          ║     │  confirm_button · filled primary
│      ║        │   OK   │          ║     │    min_touch_target 48dp
│      ║        └────────┘          ║     │    on_click → OnSuccessDialogDismiss
│      ╚════════════════════════════╝     │      → navigate personal-dashboard
└─────────────────────────────────────────┘
```

- Fineract returns `LoanRequestResponse { resourceId, officeId, clientId, resourceExternalId }`; the `resourceExternalId` (LR-YYYY-MMDD-NNN) becomes the admin's audit reference.
- OK tap → NavController pops to `personal-dashboard`; the new PENDING row appears in the organizer's queue at the next meeting.

### `submit_error`

```
┌ Request a Loan ────────────────────────┐
│  [savings-limit-card]                   │
│  [amount_field]                          │
│  [purpose_dropdown]                      │
│  [duration_selector]                     │
│  [repayment_summary_card]                │
│  [submit_button — re-enabled]            │
│                                          │
│  ┌─ error_snackbar ─────────────────┐   │  errorContainer #FFCDD2
│  │ ⚠ {{error.message}}      Retry → │   │  onErrorContainer text
│  │   e.g. "Server error. Please      │   │  duration 5000ms · slide-up MD3
│  │   try again."                     │   │  action_label "Retry"
│  └──────────────────────────────────┘   │    on_click → OnRetry → api.submit_loan_request
└─────────────────────────────────────────┘        (call_api, re-uses same LoanRequestPayload)
```

Error types (from `SubmitError`):
- `Network` — `retry: true` · `error_network_queued` "No internet. Your request has been saved for later." (falls through to `offline_queued` instead — see below)
- `Server` — `retry: true` · `error_server` "Server error. Please try again." (5xx path — Retry re-hits Fineract)
- `Validation` — `retry: false` · `error_validation` "Please check all fields and try again." (400 field-level errors mapped back onto `requestedAmountError` / `purposeError`)
- `Unauthorized` — `retry: false` · `error_session_expired` "Session expired. Please login again." → redirect to `login`

### `offline_queued`

```
┌ Request a Loan ────────────────────────┐
│ ┌ 📶⃠ You are offline. Your request will─┐│  offline_mode_banner · secondaryContainer
│ │  be saved and submitted when you       ││    corner 8dp · padding 8dp 16dp
│ │  reconnect.                             ││    icon wifi_off · visible_when isOfflineMode
│ └────────────────────────────────────────┘│
│  [savings-limit-card]                   │
│  [amount_field]                          │  fields still ENABLED — user may still edit
│  [purpose_dropdown]                      │  before re-tapping submit (idempotent enqueue)
│  [duration_selector]                     │
│  [repayment_summary_card]                │
│  [submit_button]                         │
│                                          │
│      ╔════════════════════════════╗     │  success_dialog · offline copy variant
│      ║        📥 (queued)         ║     │    title · "Request Saved!"
│      ║   Request Saved!           ║     │    body · "You are offline. Your loan request
│      ║                            ║     │           has been saved and will be submitted
│      ║  You are offline. Your     ║     │           automatically when you reconnect."
│      ║  loan request has been     ║     │
│      ║  saved and will be         ║     │
│      ║  submitted automatically   ║     │
│      ║  when you reconnect.       ║     │
│      ║                            ║     │
│      ║        ┌────────┐          ║     │
│      ║        │   OK   │          ║     │
│      ╚════════════════════════════╝     │
└─────────────────────────────────────────┘
```

- Trigger: `cmp-network-monitor` reports offline at `OnSubmitClick` OR Ktor returns 503.
- `SyncQueueEntry` written to SQLDelight `sync_queue` via `SyncQueueRepository`: `{ entityType: "LOAN_REQUEST", payload: <json>, status: "PENDING", retryCount: 0 }`.
- Background worker drains on reconnect with exponential backoff; on 200 → row flips to `SYNCED`; on repeated 5xx → `retryCount++` up to a cap.
- `ShowOfflineQueuedConfirmation` event fired to also flash a snackbar in case the dialog is dismissed quickly.

---

## Interaction Patterns

1. **Amount input** → `OnAmountChange(value)` (effect: `transform_state`) → recomputes `repaymentEstimate` and `requestedAmountError` in-memory; pure `StateFlow` re-emit, no I/O.
2. **Purpose selection** → `OnPurposeSelected(purpose)` (effect: `transform_state`) → sets `state.purpose`, clears `purposeError`, re-evaluates `isFormValid`.
3. **Duration slider** → `OnDurationChanged(weeks)` (effect: `transform_state`) → updates `state.durationWeeks`, recomputes `repaymentEstimate = principal * (1 + rate) / weeks`.
4. **Submit tap** → `OnSubmitClick` (effect: `call_api`, libs `cmp-network-monitor` + `Ktor` + `SQLDelight`) → dispatches through `LoanRequestRepository`:
   - Online path: Ktor `POST /datatables/dt_loan_request` with body from `LoanRequestPayload`; on 200 → `submit_success`; on 4xx/5xx → `submit_error`.
   - Offline path: `SyncQueueRepository.enqueue(LOAN_REQUEST, json)` via SQLDelight → `offline_queued` state + `ShowOfflineQueuedConfirmation` event.
5. **Success OK** → `OnSuccessDialogDismiss` (effect: `navigate`) → NavController push `personal-dashboard`; loan appears PENDING in organizer queue.
6. **Retry tap (error snackbar)** → `OnRetry` (effect: `call_api`) → re-posts the same `LoanRequestPayload`; on repeated offline → re-queues to SyncQueue rather than surfacing duplicate errors.
7. **Back tap** → `NavigateBack` (effect: `navigate`) → pops to `personal-loans`; the unsaved form is discarded per action_contract description.

---

## Accessibility

- All labels + values are exposed to the semantics tree; amount/duration render both a colored control and a plain-text summary in the repayment card.
- `requestedAmountError` is announced via `LiveRegion(assertive)` on error transition; supporting_text stays visible on focus.
- Amount field: `keyboard_type: number` + `ime_action: next` — keyboard advances to purpose dropdown without dismissing.
- Purpose dropdown carries role `combobox`; the 7 options render with `role: option` inside a bottom sheet on mobile.
- Slider thumb has 48dp min hit area with left/right key/arrow-swipe increment (step = 4 weeks per `steps: 12` over range `4..52`).
- Submit button state (`enabled_when`) is mirrored on `Semantics { disabled = !isFormValid || isSubmitting }`; screen readers read "Submit Application, disabled" until validity flips.
- Offline banner announces on state transition (`aria-live: polite`).
- Success dialog captures focus + returns focus to submit button on dismiss.
- Locales covered: English (canonical), Swahili ("Omba Mkopo"), French ("Demander un prêt"), Hindi ("ऋण के लिए आवेदन करें") — `i18n.en` block in ui.yaml is the source; other locales derive from `_strings/strings.yaml` per RULE-IDEA-I18N-COMPLETENESS-001.
- Font stack: Roboto / SF Pro system — dynamic type honored on iOS; amounts render Roboto Mono / SF Mono for aligned columns.

---

## Motion & Feedback

- Duration slider thumb: 150ms ease-out translate; active-track fill grows in sync.
- Amount field error: `requestedAmountError` fades in over 120ms (motion 3/10 — no aggressive shake).
- Repayment summary card: enters via 200ms ease-out fade + 4dp vertical translate when `requestedAmount` first becomes valid.
- Submit press: MD3 filled-button state layer + ripple 300ms ease-out.
- Submitting spinner: MD3 CircularProgress 1.4s rotation ease-in-out infinite; obeys `prefers-reduced-motion: reduce` (halts + shows indeterminate bar instead).
- Success dialog: 250ms scale-and-fade MD3 dialog enter; icon `check_circle` renders with static fill (no bounce — motion 3/10).
- Error snackbar: MD3 slide-up 200ms; auto-dismiss 5000ms; Retry tap dispatches immediately, snackbar dismisses in 100ms.
- Offline banner: fade in on `isOfflineMode` flip (no slide — banner is persistent, not transient).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Ktor` (HTTP client), `SQLDelight` (SyncQueue persistence), `StateFlow` (VM state)
**Internal libs**: `cmp-network-monitor` (connectivity check)

Read paths (form initialization from nav_params):
- `savingsBalance` ← `nav_params.savingsBalance` (passed from `personal-dashboard`/`personal-loans`)
- `loanMultiplier` ← `nav_params.loanMultiplier` (default 3.0)
- `maxLoanAmount` ← derived: `savingsBalance * loanMultiplier` (recomputed in VM `init`)
- `clientId` ← `nav_params.clientId`

Write path (submit):
- Online: `LoanRequestRepository.submit(LoanRequestPayload)` → Ktor `POST /datatables/dt_loan_request` → returns `LoanRequestResponse`.
- Offline: `LoanRequestRepository.submit(...)` internally routes through `cmp-network-monitor.isOffline` → `SyncQueueRepository.enqueue(SyncQueueEntry)` → SQLDelight `sync_queue` table.

Connectivity contract (`flow.yaml#connectivity_on_submit`):
- Online + 200 → `submit_success` → navigate to `personal-dashboard`.
- Online + 4xx/5xx → `submit_error` (mapped to `SubmitError.{Server, Validation, Unauthorized}`).
- Offline → `offline_queued` (SyncQueueEntry created) → navigate to `personal-dashboard` after OK.

Idempotency: `submitted_at` (ISO-8601) + `clientId` compose a soft-dedupe key checked by the Fineract admin dashboard; the server returns 409 on exact duplicate (mapped back to a snackbar "Duplicate loan request pending").

Offline behavior: `SyncQueueEntry.payload` is the JSON-serialised `LoanRequestPayload` verbatim (see demo-data row `id 9001`); the drain worker rehydrates it on reconnect with exponential backoff; `status` transitions `PENDING → SYNCED` (or `FAILED` after cap).

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/loan-request/ui.yaml` |
| API contract | `idea-layer/screens/loan-request/api.yaml` |
| Data flow | `idea-layer/screens/loan-request/data-flow.yaml` |
| Demo data | `idea-layer/screens/loan-request/demo-data.yaml` |
| Flow | `idea-layer/screens/loan-request/flow.yaml` |
| Tests | `idea-layer/screens/loan-request/tests.yaml` |
| Docs | `idea-layer/screens/loan-request/docs.yaml` |
| Preview HTML (content) | `idea-layer/screens/loan-request/preview/content.html` |
| Preview HTML (submitting) | `idea-layer/screens/loan-request/preview/submitting.html` |
| Preview HTML (submit_success) | `idea-layer/screens/loan-request/preview/submit_success.html` |
| Preview HTML (submit_error) | `idea-layer/screens/loan-request/preview/submit_error.html` |
| Preview HTML (offline_queued) | `idea-layer/screens/loan-request/preview/offline_queued.html` |
| Stitch prompts (per state) | `idea-layer/screens/loan-request/prompts/{content,submitting,submit_success,submit_error,offline_queued}.md` |
| Design system | `idea-layer/design-system/DESIGN.md` |
| Feature-group mockup | `idea-layer/mockups/loan-management/MOCKUP.md` (member-side Request section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001 + RULE-STITCH-VAULT-DIRECT-001 SPE-1..SPE-3). This MOCKUP.md is the LLM-driven analog synthesized from ui.yaml (5-state canonical), demo-data.yaml (LoanRequestPayload + LoanRequestResponse + SyncQueueEntry entries), api.yaml (`POST /datatables/dt_loan_request` + DTOs), flow.yaml (validation + connectivity branches), and design-system/DESIGN.md tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  # Stitch key resolves through the vault (never hand-write .env.stitch — RULE-STITCH-VAULT-DIRECT-001)
  deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-request
  ```
- Design conformance verifier: preview HTML mirrors the layout above per state; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade, which will re-materialise this file via `/idea-render-mockup --feature loan-request`.
- Amount validation happens ENTIRELY client-side against `savingsBalance * loanMultiplier` before Ktor is called — no server round-trip for typos.
- The `LoanRequestPayload.purpose` string persisted to `dt_loan_request` is `"{ENUM_VALUE}: {narrative}"` — the enum is source-of-truth for filters/analytics, the narrative is the organizer's context. Any downstream analytics `screen_viewed` event (see `docs.yaml#legacy_metadata.analytics`) is emitted on `content` render.
