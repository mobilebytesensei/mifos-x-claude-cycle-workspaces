# Mockup — pay-vrp-mandate

Design system: Open Banking — Trust Blue v1.4.0  
Token source: `idea-layer/design-system/design-tokens.yaml`  
Component reference: `idea-layer/design-system/DESIGN.md`

> COPY SOURCE — every user-facing string in this document is now the verbatim
> `_strings/strings.yaml` value for the key `screens/pay-vrp-mandate/ui.yaml` binds. The `vrp.*`
> (36 keys) and `payment.*` namespaces were authored 2026-08-07; the keys cited inline resolve.
> The four defects the previous pass recorded are resolved as follows:
> 1. Screen 1 empty-state body now carries the FULL `vrp.empty_body` — no ellipsis, and both
>    facts present: only ones set up in THIS app are listed, and a dated or repeating
>    instruction belongs to Pay on a date / Standing order.
> 2. The Step-3 pro-rating banner is now `vrp.pro_rating_notice` verbatim. The developer
>    instruction ("probe before assuming") is gone; the caution it carried survives.
> 3. Headroom rows no longer state a remainder as the bank's arithmetic. Every figure is
>    labelled as counted by this app, with `vrp.pro_rating_notice` alongside — `ui.yaml#headroom_list`
>    records that the API exposes no consumed, remaining or period-boundary value.
> 4. NOT a defect — premise corrected. `design-tokens.yaml#semantic.status.warning_container`
>    maps `warning` onto tertiaryContainer / onTertiaryContainer, and
>    `semantic.mandate_health.failing` declares exactly that pair (#EADDFF / #4C4162, icon
>    `schedule`). The table's `tertiaryContainer` fill IS `color: warning`. The mapping is now
>    cited in the table so it does not read as drift again.
> ⚠ STILL UNSOURCED (no catalogue key AND no component in `ui.yaml`): the pay-sheet CTA
> ("Pay £5.00"), the revoke dialog's dismiss label, the create CTA ("Authorise mandate"), the
> per-payment charge note, and Screen 1's "Choose a funding account" heading.

---

## Screen 1 — Variable payments (mandate list)

**Screen ID:** `pay-vrp-mandate`  
**Archetype:** index_list  
**Shell:** `top_app_bar` + `bottom_nav`

### Component Hierarchy

```
Scaffold
├── TopAppBar
│    ├── navigationIcon: back (arrow_back)
│    ├── title: "Variable payments"   [titleLarge · onSurface]   {vrp.title}
│    └── actions:
│         └── IconButton(icon=add, contentDescription="Set up a variable payment")
│              {vrp.create_action} · container: transparent · tint: onSurface
├── BottomNavigationBar
│    └── active tab: Pay   [primary]
└── ContentArea  [background: surface · padding: 16dp]
     ├── STATE: loading
     │    └── LazyColumn
     │         └── MandateRowSkeleton × 3
     │              ├── ShimmerBox(width=160dp, height=14dp)   [surfaceContainerHigh]
     │              ├── ShimmerBox(width=120dp, height=12dp)   [surfaceContainerHighest]
     │              └── ShimmerBox(width=80dp, height=24dp, radius=full)   [surfaceContainerHigh]
     │
     ├── STATE: content
     │    └── LazyColumn  [contentDescription: "Your variable payments"  {vrp.list_label}]
     │         └── MandateRow (per mandate)  [testTag: vrp:mandateRow]
     │              ElevatedCard(radius=medium · container=surfaceContainer · elevation=1)
     │              ├── Row (leading)
     │              │    └── Icon(autorenew · size=40dp)  [primary]  ← always autorenew; not a payment icon
     │              ├── Column (body)
     │              │    ├── Text(creditorName · titleMedium · onSurface)
     │              │    └── Text(limitsSummary · bodySmall · onSurfaceVariant)
     │              │         e.g. "Up to £10.00 per payment · £50.00 / week"
     │              └── MandateHealthChip  [testTag: vrp:healthChip]
     │                   ── see Mandate Health Chip spec below ──
     │
     └── STATE: empty  [testTag: vrp:noMandates]
          EmptyStateLayout(padding=32dp)
          ├── Icon(account_balance · size=64dp · onSurfaceVariant)
          ├── Text("No variable payments" · headlineSmall · onSurface · textAlign=center)
          │    {vrp.empty_title}
          ├── Text(bodyMedium · onSurfaceVariant · textAlign=center)  {vrp.empty_body}
          │    "A variable payment lets you set spending limits once, then pay any amount
          │     within them without approving each payment. You have not set one up yet. Only
          │     the ones you set up in this app appear here, so one set up on another device
          │     will not show. If you want a payment on a set date, or one that repeats on a
          │     schedule, use Pay on a date or Standing order instead."
          │    RENDER IN FULL. No ellipsis, no truncation — the last two sentences are the
          │    device-scope fact and the redirect, and neither exists anywhere else.
          └── FilledButton("Set up a variable payment" · radius=full · container=primary · label=onPrimary)
               {vrp.create_action} · action: StartCreate  [testTag: vrp:noMandates]
```

### Mandate Health Chip

The `mandate_health_chip` is a **separate component** from `status_chip`. It must never read its colour from consent status. Icon is always present — colour is never the only signal (WCAG 1.4.1).

| State | `ui.yaml` color | Icon | Container | On-container | Label (key) |
|---|---|---|---|---|---|
| `active` | success | `autorenew` | `primaryContainer` (#C9E6FF) | `onPrimaryContainer` (#004B6F) | Active `{vrp.health.active}` |
| `failing` | warning | `schedule` | `tertiaryContainer` (#EADDFF) | `onTertiaryContainer` (#4C4162) | Payments failing `{vrp.health.failing}` |
| `unpayable` | error | `error` | `errorContainer` (#FFDAD6) | `onErrorContainer` (#93000A) | Cannot make payments `{vrp.health.unpayable}` |
| `revoked` | onSurfaceVariant | `block` | `surfaceVariant` (#DDE3EA) | `onSurfaceVariant` (#41474D) | Cancelled `{vrp.health.revoked}` |

**Token mapping — `warning` IS tertiaryContainer here.** `design-tokens.yaml#semantic.status.warning_container` maps the `warning` family onto tertiary rather than minting an amber hue, and `semantic.mandate_health.failing` declares that exact pair with the `schedule` glyph. `success` likewise maps onto primary. The container columns above therefore match `ui.yaml`'s `color:` values; they are not drift.

**Contrast:** active 7.27:1 (W-02/W-05) · failing 7.27:1 (W-16/W-17) · unpayable 7.24:1 (W-03/W-06) · revoked 7.28:1 (W-30). All pairs measured in prior releases; no new pair introduced.

**Never use `check_circle` here.** That icon belongs to the settled-payment disposition. The `active` mandate chip uses `autorenew` precisely to prevent the visual confusion between "mandate is active" and "payment settled".

---

## Screen 2 — New variable payment (create form — 4 steps)

**Screen ID:** `pay-vrp-mandate-create`  
**Archetype:** form  
**Shell:** `top_app_bar` (back only, no bottom nav)

```
Scaffold
├── TopAppBar
│    ├── navigationIcon: back
│    └── title: "New variable payment"  [titleLarge · onSurface]   {vrp.create_title}
└── ContentArea  [padding: 16dp]
     ├── StepIndicator  [testTag: vrpCreate:stepIndicator]
     │    Four captions: "Account" {payment.step.account} · "Payee" {payment.step.payee} ·
     │    "Limits" {vrp.step.limits} · "Review" {payment.step.review}
     │    [bodyMedium · onSurfaceVariant]
     │    NO "Step N of M" string. The former step_indicator key was deleted with the send-money
     │    screen and deliberately not carried into the payment.* namespace.
     │
     ├── STEP 1: Account
     │    ├── Text("Choose the account to pay from" · titleMedium · onSurface)
     │    │    {payment.debtor_list_label} — NOTE: ui.yaml#debtor_account_list declares no
     │    │    `label:`, so this heading is currently unbound. Add the binding.
     │    └── LazyColumn  [testTag: vrpCreate:debtorList]
     │         └── AccountRow per eligible account (scheme == SortCodeAccountNumber)
     │              ElevatedCard(radius=medium · container=surfaceContainer)
     │              ├── Text(accountName · bodyLarge · onSurface)
     │              ├── Text(maskedIdentification · bodySmall · onSurfaceVariant)
     │              └── trailing: RadioButton  [primary]
     │    Note: credit card is never offered. Global Money TPP-named excluded (U002).
     │    Savings IS offered (scheme eligible; contradicts Guide §28.8).
     │
     ├── STEP 2: Payee
     │    ├── OutlinedTextField(label="Sort code" {payment.sort_code_label} · testTag=vrpCreate:creditorSortCodeField)
     │    │    radius=small(8dp) · outline=outline · focus=primary · error=error
     │    ├── OutlinedTextField(label="Account number" {payment.account_number_label} · testTag=vrpCreate:creditorAccountNumberField)
     │    └── OutlinedTextField(label="Recipient's name" {payment.payee_name_label} · testTag=vrpCreate:creditorNameField)
     │    Validation on-change after first blur.
     │    Creditor must be SortCodeAccountNumber — IBAN returns U021.
     │
     ├── STEP 3: Limits
     │    ├── OutlinedTextField(label="Most you can pay at once" {vrp.max_individual_label}
     │    │    · keyboard=number · testTag=vrpCreate:maxIndividualField)
     │    │    helperText {vrp.max_individual_helper}: "The largest single payment allowed under
     │    │    this variable payment. Payments can only be made in pounds."
     │    ├── DropdownMenu(label="Limit period" {vrp.period_type_label} · testTag=vrpCreate:periodTypePicker)
     │    │    options: Day / Week / Month (observed 201) · Fortnight / Half-year / Year (OBIE enum, untested)
     │    ├── OutlinedTextField(label="Most you can pay in that period" {vrp.period_limit_label}
     │    │    · keyboard=number · testTag=vrpCreate:periodLimitField)
     │    ├── Switch("Add a second limit" {vrp.add_second_limit_label} · default=false · testTag=vrpCreate:addSecondLimitSwitch)
     │    │    When on: second period-type picker + period-limit field appear.
     │    │    Max OBSERVED is two limits. Do not build an unbounded list.
     │    └── InfoBanner(testTag=vrpCreate:proRatingNotice)
     │         visibility: periodLimitAmount set AND periodAlignment == Calendar
     │         content {vrp.pro_rating_notice}: "Your first period may allow less than this,
     │                   because it starts partway through. HSBC works that out and does not
     │                   share the figure, so this app cannot show how much is left in it."
     │         severity: info  [tertiaryContainer / onTertiaryContainer]
     │         No computed figure — pro-rating was documented but never observed in any response.
     │         PSU-facing register only: no "probe", no developer instruction.
     │
     └── STEP 4: Review
          ├── InfoBanner(testTag=vrpCreate:singleAuthorisationNotice)
          │    content {vrp.single_authorisation_notice}: "You approve this once. After that,
          │              every payment within these limits goes through without HSBC asking you
          │              again. It does not expire — it runs until you cancel it here, or in the
          │              HSBC app."
          │    severity: info  [tertiaryContainer / onTertiaryContainer]
          ├── ReviewCard  [testTag=vrpCreate:reviewCard · ElevatedCard(radius=medium · surfaceContainer)]
          │    ├── Row("From" {payment.review.from} / accountLabel)
          │    ├── Row("To" {vrp.review.to} / "test user · 401800 00133787")
          │    ├── Row("Most per payment" {vrp.review.max_per_payment} / "£10.00")
          │    └── Row("Period limits" {vrp.review.period_limits} / "£50.00 a week")
          │    No first-period row. No reference row. Charges appear per payment, not on the consent.
          └── FilledButton("Authorise mandate" · radius=full · container=primary · label=onPrimary)
               UNSOURCED — no key, and ui.yaml declares no CTA on this step. Note the consumer
               wording rule: the shipped label must not say "mandate".
               action: CreateMandate → POST /domestic-vrp-consents → navigate to payment-consent
```

---

## Screen 3 — Variable payment (mandate detail)

**Screen ID:** `pay-vrp-mandate-detail`  
**Shell:** `top_app_bar` (back only, no bottom nav)

```
Scaffold
├── TopAppBar
│    ├── navigationIcon: back
│    └── title: "Variable payment"  [titleLarge · onSurface]   {vrp.detail_title}
└── ContentScrollArea  [padding: 16dp]
     │
     ├── MandateDetailCard  [testTag: vrpDetail:card · ElevatedCard(radius=medium · surfaceContainer)]
     │    ├── Row("To" {vrp.review.to} / "test user · 401800 00133787")
     │    ├── Row("Most per payment" {vrp.review.max_per_payment} / "£10.00")
     │    └── Row("Status" {vrp.detail.status} / MandateHealthChip)
     │
     ├── HeadroomSection (label: "Limits and spending"  {vrp.detail.headroom})
     │    [testTag: vrpDetail:headroomList]
     │    The key is deliberately NOT "What's left": the local ledger restarts at zero after a
     │    reinstall while the bank's does not, so the section may not promise a remainder.
     │    For EACH periodic limit:
     │    ElevatedCard(radius=medium · surfaceContainer)
     │    ├── Text("Weekly limit" · bodyMedium · onSurface)
     │    ├── Text("£50.00 limit · £10.00 counted from payments made in this app"
     │    │        · bodySmall · onSurfaceVariant)
     │    │   NEVER "£10.00 of £50.00 used this week" — that states the bank's arithmetic. The
     │    │   API exposes no consumed amount, no remaining amount and no period boundary.
     │    └── LinearProgressIndicator(progress=0.20 · color=primary · trackColor=primaryContainer)
     │    Below the section, as an info note: {vrp.pro_rating_notice} — "Your first period may
     │    allow less than this, because it starts partway through. HSBC works that out and does
     │    not share the figure, so this app cannot show how much is left in it."
     │    Every limit always shown — U014 breach does not name which limit was hit.
     │    On fresh install with no ledger: show limits without a spent figure ("—/£50.00").
     │
     ├── CONDITIONAL: health == failing
     │    WarningBanner  [testTag: vrpDetail:failingBanner · warning = tertiaryContainer / onTertiaryContainer]
     │    Icon(schedule · size=24dp) + {vrp.failing_banner}: "Payments under this variable payment
     │    are being turned down. This usually means the payee has been removed in the HSBC app.
     │    Add them back there, then try again."
     │
     ├── CONDITIONAL: health == unpayable
     │    ErrorBanner  [testTag: vrpDetail:unpayableBanner · errorContainer / onErrorContainer]
     │    Icon(error · size=24dp) + ONE text run {vrp.unpayable_banner}: "This variable payment
     │    cannot make any payments. The account you chose at HSBC cannot be used for them, and
     │    that cannot be changed now. The funds check said the money was there, but every payment
     │    has been turned down. Cancel this one and set up a new one against an account with a
     │    sort code and account number."
     │    ONE key, ONE run — ui.yaml declares a single `content`. No retry is offered.
     │
     ├── CONDITIONAL: health == revoked
     │    InfoBanner  [testTag: vrpDetail:revokedBanner · surfaceContainerHigh / onSurface]
     │    {vrp.revoked_banner}: "This variable payment has been cancelled. It cannot be restarted
     │    — set up a new one if you still need it."
     │    Neutral, never error-coloured: U011 after DELETE is a normal terminal state.
     │
     ├── CONDITIONAL: uiState is Paying
     │    PaymentSheet  (shown inline or as BottomSheet · radius top=extra_large)
     │    ├── Text("Amount" {vrp.payment_amount_label} · titleMedium · onSurface)
     │    ├── AmountField  [testTag: vrpDetail:paymentAmountField]
     │    │    font=mono · scale=headlineSmall · prefix="£" · keyboard=number
     │    │    validation: amount <= MaximumIndividualAmount AND <= the headroom this app has
     │    │    counted on EVERY limit; the error names the limit that blocks it AND says the
     │    │    count is this app's own, never the bank's.
     │    ├── OutlinedTextField(label="Reference (optional)" {vrp.payment_reference_label}
     │    │    · testTag=vrpDetail:paymentReferenceField)
     │    │    Each payment carries its own reference → Data.Instruction.RemittanceInformation.
     │    └── FilledButton("Pay £5.00" · radius=full · container=primary · label=onPrimary)
     │         UNSOURCED — no key, and ui.yaml declares no sheet CTA component.
     │         action: ConfirmFundsAndPay
     │         Funds-confirmation (PSU token, POST) runs first; the Available result is a
     │         transient step before POST /domestic-vrps. Never rendered as a promise.
     │
     ├── CONDITIONAL: uiState is Paying(Settling)  [testTag: vrpDetail:settlingIndicator]
     │    SettlingCard  [ElevatedCard(radius=medium · surfaceContainer)]
     │    ├── CircularProgressIndicator  [color=secondary]
     │    ├── Text("Sending your payment" {vrp.settling} · titleMedium · onSurface)
     │    └── Text("Expected by 15:19:48" · bodyMedium · onSurfaceVariant)
     │    Duration driven from the RETURNED ExpectedSettlementDateTime (CreationDateTime + 30
     │    seconds), never a hardcoded 30. This is the only rail where that field is honest.
     │
     ├── CONDITIONAL: uiState is Error(FraudCheckRejected)  [testTag: vrpDetail:eveningWindowNotice]
     │    InfoBanner {vrp.evening_window_notice}: "HSBC turned this payment down for extra fraud
     │    checks. Payments made between 6pm and 11:45pm are more likely to be checked this way.
     │    Nothing has been sent — try again outside those hours."
     │    No auto-retry, health unchanged.
     │
     ├── CONDITIONAL: health == active (Pay now button)
     │    FilledButton("Pay now" {vrp.pay_now} · radius=full · container=primary · label=onPrimary)
     │    [testTag: vrpDetail:payNowButton]
     │    Hidden on failing / unpayable / revoked — payment would be refused.
     │    No re-authentication — taps go straight to funds-confirmation then the payment endpoint.
     │
     └── CONDITIONAL: health in {active, failing, unpayable} (Revoke button)
          TextButton("Cancel this variable payment" {vrp.revoke} · color=error)
          [testTag: vrpDetail:revokeButton]
          action: ConfirmRevoke → opens revoke_confirm_dialog
          Also offered on `unpayable` — that is the one the PSU most wants gone.

     REVOKE DIALOG  [testTag: vrpDetail:revokeConfirmDialog · visible when uiState is Revoking]
     AlertDialog(radius=extra_large · surfaceContainerHigh)
     ├── title {vrp.revoke_confirm_title}: "Cancel this variable payment?"
     ├── body {vrp.revoke_confirm_body}: "The limits you set will be removed and no more payments
     │          can be made under this variable payment. This cannot be undone — you would need
     │          to set up a new one and approve it with HSBC again."
     ├── confirm: FilledButton("Yes, cancel it" {vrp.revoke_confirm_cta} · color=error)
     └── dismiss: TextButton("Cancel")
          UNSOURCED — ui.yaml declares title, body and confirm only, so no key exists. It also
          now collides with the confirm ("Yes, cancel it"): two adjacent buttons reading
          "Cancel". Declare the dismiss in ui.yaml and author a key before render.
```

---

## Component ↔ API Binding Table

| Component | Trigger | API call | Auth token | Notes |
|---|---|---|---|---|
| `mandate_list` mount | LoadMandates | GET /domestic-vrp-consents/{id} per local record | client_credentials | 400 U011 → mark revoked, not error |
| `mandate_list` mount | LoadMandates | POST /v4.0/events (poll) | client_credentials | Detect out-of-band revoke |
| `create_review_card` CTA | CreateMandate | POST /domestic-vrp-consents | client_credentials | Validate client-side first; no redirect in response |
| After consent AUTH | — | — | — | Navigate to detail; one-time authorise leg complete |
| `pay_now_button` | StartPaymentUnderMandate | POST .../funds-confirmation | **PSU token** | client_credentials → 401; "Available" ≠ promise |
| `pay_now_button` | ConfirmFundsAndPay (1) | GET /domestic-vrp-consents/{id} | client_credentials | Re-read authorised Initiation before payment |
| `pay_now_button` | ConfirmFundsAndPay (2) | POST /domestic-vrps | **PSU token** | Echo Initiation from GET; append to local ledger on 201 |
| `revoke_button` | ConfirmRevoke → Revoke | DELETE /domestic-vrp-consents/{id} | client_credentials | Write local revoked record before next GET fires |

---

## Partial-Failure Taxonomy

| Scenario | API signal | UX treatment | Health change |
|---|---|---|---|
| **AUTH-but-unpayable** (consent 45224) | Consent AUTH; funds-confirmation "Available"; POST /domestic-vrps 400 U021 on bank-written PAN debtor | `unpayable_mandate_banner`, Pay now hidden, Revoke offered. Never show funds-confirmation result as reassurance. No retry. | `active → unpayable` (local record) |
| **Trusted-beneficiary failure** | Consent AUTH; payment StatusReason `UK.OBIE.ExemptionNotApplied` | `failing_mandate_banner`, Pay now hidden. Instruct PSU to re-add payee in HSBC app. | `active → failing` (derived from payment outcomes) |
| **Evening fraud-window rejection** | 400 at 18:00–23:45 | `evening_window_notice` banner, state the window, no auto-retry. | **None** — health unchanged |
| **Limit breach** | 400 U014 @ Data.Instruction.InstructedAmount.Amount | Show all limits (bank does not name which was hit). Prevented by local validation before the call. | None |
| **Out-of-band revoke** (PSU in HSBC app) | Event `UK.OBIE.Consent-Authorization-Revoked` or consent GET 400 U011 | Mandate renders revoked without PSU opening it. | `any → revoked` |
| **Bank writes bad debtor** | Consent AUTH with `SchemeName: UK.OBIE.PAN` in Initiation | U021 at payment time. Mark unpayable, show banner, offer Revoke. | `active → unpayable` |
| **Revoked mandate re-opened** | GET consent 400 U011 | Map to revoked (local record). Never render as generic error. | Drives `revoked` display |
| **Post-revoke GET** | 400 U011 with Path `/domestic-vrp-consents/45205` | Special-case before path mapper — URL path, not a field pointer. | — |
