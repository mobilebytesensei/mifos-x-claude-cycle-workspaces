# Loan Apply — Mockup Specification

**Feature**: loan-apply | **Route**: `/groups/{groupId}/loans/apply` | **Type**: form
**Feature group**: loan-management | **Flow**: loan-management-flow
**Generated from**: `screens/loan-apply/ui.yaml`, `screens/loan-apply/demo-data.yaml`, `screens/loan-apply/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-apply`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — all CTAs, back button, active states
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (not used on this screen)
**Success**: `#2E7D32` — eligibility "Max eligible" value
**Warning**: `#F57C00` — corpus buffer banner text
**Danger**: `#C62828` — amount-exceeds validation error
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` filled inputs
**Corner radius**: 16px cards · 12px form fields & buttons · 8dp per ui.yaml component styles
**Min touch target**: 48dp (form fields, dropdowns) · 56dp (primary Submit)

---

## Screen: Apply for Loan

### Entry
- FAB from **loan-list** ("Apply for Loan"); nav-param `groupId: Long`
- Back navigation returns to loan-list (no draft persistence — form data discarded)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Apply for loan          [#2E7D32]  │  TopAppBar — primary green, onPrimary text
├─────────────────────────────────────────┤
│  Select member                          │  Dropdown label
│  ┌─────────────────────────────────┐    │
│  │ [👤] Grace Akinyi          [▼]  │    │  member_selector · 48dp min, person icon
│  └─────────────────────────────────┘    │  binds → members[] (5 GroupMember DTOs)
├─────────────────────────────────────────┤
│  ┌ ─ Eligibility ─────────────────┐     │  eligibility_banner — primaryContainer bg
│  │ Savings balance      KES 3,200  │    │  visible_when: selectedMember != null
│  │ Max eligible         KES 9,600  │    │  "Max" value in --success green
│  │ Multiplier           3.0× savings│    │  loanMultiplier from GroupConfig
│  └────────────────────────────────┘     │
├─────────────────────────────────────────┤
│  Requested amount (KES)                 │
│  ┌─────────────────────────────────┐    │
│  │ [₵] 8,000                        │    │  amount_input · decimal keyboard,
│  └─────────────────────────────────┘    │  currency_exchange leading icon
│  Within your eligible limit of KES 9,600│  help text · bodySmall, --text-secondary
├─────────────────────────────────────────┤
│  ┌ ⚠ Corpus warning ─────────────┐      │  corpus_warning_banner — #FFF9C4 bg,
│  │ Disbursing this amount will    │     │  #E65100 text · visible_when: corpusWarning
│  │ reduce group corpus below 10%. │     │  (hidden on content default demo)
│  └───────────────────────────────┘      │
├─────────────────────────────────────────┤
│  Loan duration                          │
│  ┌─────────────────────────────────┐    │
│  │ 8 weeks                    [▼]  │    │  duration_dropdown · 4 / 8 / 12 / 24 / 52
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│  Loan purpose                           │
│  ┌─────────────────────────────────┐    │
│  │ Business                   [▼]  │    │  purpose_dropdown · MEDICAL / EDUCATION /
│  └─────────────────────────────────┘    │  BUSINESS / EMERGENCY / OTHER
├─────────────────────────────────────────┤
│  Loan product                           │
│  ┌─────────────────────────────────┐    │
│  │ Group Solidarity Loan      [▼]  │    │  product_dropdown · loads from LoanProduct[]
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │       Submit Application         │    │  submit_button · primary #2E7D32,
│  └─────────────────────────────────┘    │  56dp height, 24dp radius, full width
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`)

- **Selected member**: Grace Akinyi (id 303) — Mwangaza Women's Group
- **Savings balance**: KES 3,200 (from `MemberRepository.getMemberSavingsBalance` via Store5)
- **Loan multiplier**: 3.0 (from `GroupConfig.loanMultiplier`)
- **Eligible amount**: KES 9,600 (savings × multiplier — computed in ViewModel)
- **Requested amount**: 8,000 (within eligibility limit, no `amountError`)
- **Duration**: 8 weeks
- **Purpose**: BUSINESS
- **Product**: Group Solidarity Loan (id 1, KES 1,000–15,000, 0.83% / period)
- **Corpus balance**: 24,000 → `corpusWarning=false` (8,000 does not breach 10% buffer)

---

## States

The ui.yaml declares 5 `screen_state` members (`Loading`, `Content`, `Submitting`, `Error`, `Success`) — 4 render as distinct HTML preview surfaces; `Success` is transient (fires `NavigateToMeetingConduct` + `ShowSnackbar`, no dedicated preview).

### `loading`
Shimmer skeleton mirroring content layout — parallel fetch of `members`, `loanProducts`, `GroupConfig`.

```
[shimmer field] ← member_selector placeholder
[shimmer card ] ← eligibility_banner (title + 2 meta lines)
[shimmer field] ← amount_input
[shimmer field] ← duration_dropdown
[shimmer field] ← purpose_dropdown
[shimmer field] ← product_dropdown
[shimmer btn  ] ← submit_button
```

- Fields: 48dp × full width, corner 12px, `--bg-muted` shimmer gradient (1.4s ease-in-out infinite)
- Respects `prefers-reduced-motion: reduce` (animation disabled)
- Top bar retains title "Apply for loan" (no back navigation while loading)

### `content` (see layout above)
Form ready for input. Eligibility + corpus banners render conditionally per `visible_when` bindings. Submit button `enabled_when: selectedMember != null && requestedAmount.isNotBlank() && amountError == null && selectedProduct != null`.

### `submitting`
Form frozen; overlay spinner over 55% dimmed / desaturated form.

```
┌ Apply for loan ────────────────────────┐
│  [form components rendered disabled]    │  ← main[data-inert] · opacity 0.55
│  [Grace Akinyi · KES 3,200 · KES 9,600] │     saturate(0.85), pointer-events:none
│  [8,000 · 8 weeks · Business · GSL]     │
│  [ Submitting… ]                        │  ← submit_button label swap, disabled
└────────────────────────────────────────┘
      ┌─────────────────────────┐
      │        [spinner]         │  ← Full-screen overlay, rgba(255,255,255,0.92)
      │  Submitting your        │      z-index 100, gap 16px
      │  application…            │
      │  Sending to the group    │
      │  ledger…                 │
      └─────────────────────────┘
```

- Back button hidden (`visibility:hidden`) — no navigation during POST
- `LoanRepository.submitLoanApplication` → Fineract `post_loan` (creates `m_loan` pending)
- `cmp-network-monitor` blocks the submit while offline

### `error`
API failure — retry CTA + secondary "Back to loans".

```
┌ Apply for loan ────────────────────────┐
│  ┌ ☁ Could not submit ──────────────┐   │  Alert — --danger red border/heading
│  │ No internet. Your application    │   │
│  │ for KES 8,000 will be queued     │   │  Error message body reads from
│  │ offline and sent when you        │   │  error.message (interpolated)
│  │ reconnect.                       │   │
│  └─────────────────────────────────┘    │
│                                          │
│               ☁                          │  empty_state illustration
│         Submission failed                │  titleLarge
│    Check your connection and             │  bodyMedium, --text-secondary
│    try again, or head back to            │
│    your loans.                           │
│                                          │
│  ┌────── Try Again ────────────────┐    │  primary #2E7D32, 56dp full width
│  └─────────────────────────────────┘    │  → OnSubmit (retries with same payload)
│  ┌────── Back to loans ────────────┐    │  secondary outlined
│  └─────────────────────────────────┘    │  → nav loan-list
└────────────────────────────────────────┘
```

Error types (from `LoanApplyError`):
- `Network` — retry:true, `error_network` "No internet. Application will be queued offline."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `AmountExceedsEligibility` — retry:false, `error_amount_exceeds`
- `CorpusInsufficient` — retry:false, `error_corpus`
- `Auth` — retry:false, `error_auth` → redirect to `login`

---

## Validation Rules

1. **Amount vs eligibility**: `requestedAmount > eligibleAmount` → inline error text under amount_input (`--danger` red, labelSmall) blocking Submit.
2. **Corpus buffer check**: `corpusBalance - requestedAmount < corpusBalance × 0.10` → warning banner surfaces (non-blocking; user may still Submit).
3. **Submit enablement**: all four conditions must hold — `selectedMember != null && requestedAmount.isNotBlank() && amountError == null && selectedProduct != null`. Below-threshold shows outline / disabled style.
4. **Offline gate**: `cmp-network-monitor` blocks Submit while offline; surfaces the queued-offline error toast.

---

## Interaction Patterns

1. **Member selection** → `OnMemberSelected` (effect: `call_api`) → `MemberRepository.getMemberSavingsBalance` + `get_loan_template` via Store5. Recomputes `eligibleAmount` reactively.
2. **Amount typing** → `OnAmountChanged` (effect: `transform_state`, no I/O) → validates + updates `amountError` and `corpusWarning`.
3. **Duration / purpose change** → `OnDurationChanged` / `OnPurposeChanged` (both `transform_state`) → pure ViewModel writes.
4. **Product selection** → `OnProductSelected` (effect: `call_api`) → `LoanRepository.getLoanTemplate` via Store5, pre-fills principal / repayments / interest.
5. **Submit tap** → `OnSubmit` (effect: `call_api`) → `LoanRepository.submitLoanApplication` → Fineract `post_loan` → creates `m_loan` pending approval → emits `NavigateToMeetingConduct(loanId)`.
6. **Back tap** → `OnBack` (effect: `navigate`) → pops the loan-apply route off NavController; form state discarded (no draft persist).

---

## Accessibility

- All form fields carry explicit labels + placeholders (see i18n block in ui.yaml — `en`, `sw`, `fr`, `hi` locales).
- Min touch target 48dp on all dropdowns and inputs; 56dp on primary Submit.
- Error surfaces are text + icon (☁ cloud_off) — never color-only.
- Corpus warning banner uses `#E65100` on `#FFF9C4` — passes WCAG AA contrast.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.
- Locales covered: English, Swahili (`Omba Mkopo` / `Wasilisha Ombi`), French (`Demande de Prêt`), Hindi (`ऋण आवेदन`).

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Submit overlay: fade-in ~200ms on state transition Content → Submitting.
- Dropdown menus: MD3 standard easing 200ms.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s.

---

## Data Flow (ui.yaml `business_logic.kind: composite`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_loan`
**Internal lib**: `cmp-network-monitor`

Read paths:
- `members[]` ← `MemberRepository.getGroupMembers(groupId)` via Store5 (SQLDelight cache)
- `loanProducts[]` ← `LoanRepository.getLoanProducts()` via Store5
- `GroupConfig` ← `GroupRepository.getGroupConfig(groupId)` (loanMultiplier, maxLoanAmount)
- `memberSavingsBalance` ← `MemberRepository.getMemberSavingsBalance(memberId)` on selection
- `corpusBalance` ← `GroupRepository.getGroupCorpus(groupId)` (10% buffer check)

Write path:
- `LoanApplicationRequest` → `LoanRepository.submitLoanApplication` → `POST /loans` (Fineract) → creates `m_loan` row (submitted, pending approval) → returns `loanId` → navigate to `meeting-conduct` for democratic vote.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/loan-apply/ui.yaml` |
| API contract | `idea-layer/screens/loan-apply/api.yaml` |
| Data flow | `idea-layer/screens/loan-apply/data-flow.yaml` |
| Demo data | `idea-layer/screens/loan-apply/demo-data.yaml` |
| Flow | `idea-layer/screens/loan-apply/flow.yaml` |
| Tests | `idea-layer/screens/loan-apply/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/loan-apply/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/loan-apply/preview/content.html` |
| Preview HTML (submitting) | `idea-layer/screens/loan-apply/preview/submitting.html` |
| Preview HTML (error) | `idea-layer/screens/loan-apply/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/loan-apply/prompts/{loading,content,submitting,error}.md` |
| Feature-group mockup | `idea-layer/mockups/loan-management/MOCKUP.md` (Screen 2 section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-apply
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
