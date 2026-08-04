# Group Create — Mockup Spec

## Design Language

MifosSave uses Material Design 3 with a VSLA-inspired brand palette designed for low-literacy rural users in East Africa. All touch targets are minimum 48dp. Typography uses the system stack (Roboto on Android / SF Pro on iOS) at comfortable density with an emphasis on clarity for outdoor viewing. Group Create follows the app's `minimalist-ui` family (variance 3/10, motion 3/10, density 7/10) — grid-aligned, predictable, subtle transitions.

**Brand colours (from `design-system/DESIGN.md`)**:
- Primary 700: #2E7D32 (base VSLA-green — app bar, primary CTAs)
- Primary 900: #1B5E20 (pressed CTA states)
- Primary 500: #43A047 (hover / focus highlight)
- Primary 100: #C8E6C9 (chip backgrounds — group type banner)
- Accent 700: #FF8F00 (pooled-fund emphasis — social fund block)
- Accent 100: #FFE082 (subtle amber accent — social fund toggle background)
- Success: #2E7D32 (approved / on-track)
- Warning: #F57C00 (validation warnings, offline banner border)
- Danger: #C62828 (error banner, validation errors)
- Info: #1565C0 (informational hints, tertiary container)
- Bg canvas: #FFFFFF (cards, sheets)
- Bg subtle: #FAFAFA (screen background)
- Bg muted: #F5F5F5 (filled input backgrounds)
- Border subtle: #EEEEEE (dividers)
- Border default: #E0E0E0 (outlined field borders)
- Text primary: #212121 (body)
- Text secondary: #616161 (metadata, labels)
- Text disabled: #9E9E9E (disabled state)

**Typography**: Roboto / SF Pro. displaySmall=36sp, headlineMedium=28sp, titleLarge=22sp, titleMedium=18sp, bodyLarge=16sp, bodyMedium=14sp, labelSmall=12sp. Amounts (KES values) rendered in Roboto Mono / SF Mono for column alignment on the review card.

**Shapes**: cornerRadius sm=8dp (chips, small buttons), md=12dp (cards, step indicator), lg=16dp (review card, sheets), full=9999dp (pill CTAs).

**Elevation**: TopBar 0dp (flat); step indicator 0dp; input fields 0dp (outlined); review card 2dp tonal; primary CTA 0dp (filled tonal); loading sheet 3dp.

---

## Screen-by-Screen

### GroupCreateScreen (4-step wizard, single screen host)

**Layout**: Scaffold with primary-tinted top bar + scrollable Column body. Background: `#FAFAFA`. Wizard fields adapt to `typeConfig.contribution_model` and `typeConfig.pool_model` forwarded from group-type-picker. Demo tenant = VSLA (share_value KES 200, 1–5 shares, social fund 5%), showcased against ROSCA variant (fixed contribution KES 500, LOTTERY payout).

**States**:
- `content` (initial_state) — active wizard step visible; Next / Back CTA row pinned at bottom; step indicator at top
- `step_2` — Type-adaptive Rules step; visible fields depend on `typeConfig.contribution_model`
- `step_3` — Members step; simple maxMembers field
- `step_4` — Review + submit; ReviewCard renders full config; Submit CTA replaces Next
- `submitting` — Submit button in loading state (spinner replaces label, button disabled); ReviewCard and step indicator remain visible; back button disabled
- `success` — Very brief; immediately navigates to `group-dashboard` with the returned `groupId` + `inviteCode`
- `error` — Inline error banner rendered above the review card; Submit re-enabled; fields editable

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| top_bar | TopBar | Background primary (#2E7D32), text onPrimary (#FFFFFF), elevation 0dp, height 56dp. Navigation icon `close` 24dp onPrimary at start. Title: "New {{groupTypeName}} Group" — titleLarge (22sp), onPrimary. Fallback title "New Group" when typeConfig is null. | Tap close icon → OnBack → NavigateBack (pops to group-type-picker; discards partial wizard state) |
| group_type_banner | Chip | Background primaryContainer (#C8E6C9), text color onPrimaryContainer (#1B5E20), corner_radius full (9999dp), padding_horizontal 12dp, padding_vertical 6dp, height 32dp, margin_horizontal 16dp, margin_top 8dp. Leading icon: `category_24_regular` 18dp. Label: "{{groupTypeName}}" — labelLarge (14sp). Renders "VSLA" / "ROSCA" / "SHG" from nav_arg. | Non-interactive |
| step_indicator | StepIndicator | 4 pills laid horizontally, margin_horizontal 16dp, margin_top 16dp, margin_bottom 24dp. Each pill: 8dp height, corner_radius 4dp. Active pill fills primary (#2E7D32), 32dp wide. Completed pills fill primary at 60% (#43A047), 24dp wide. Upcoming pills fill borderSubtle (#EEEEEE), 24dp wide. Below pills: 4 labels row — "Identity" / "Rules" / "Members" / "Review" — labelSmall (12sp), active label onSurface (#212121) semibold, inactive textDisabled (#9E9E9E). | Non-interactive (progress indicator only) |
| group_name_field | OutlinedTextField (Step 1) | label "Group Name", placeholder "e.g. Mwangaza Women's Group", leading icon `people_24_regular` 24dp, keyboard text, IME next, max length 60, margin_horizontal 16dp, margin_bottom 12dp, min_height 56dp, corner_radius md (12dp). Character counter "{{groupName.length}}/60" trailing at labelSmall. Error state: border 2dp danger (#C62828), helper text "{{validationErrors.group_name}}" bodyMedium danger. | Type → OnNameChange |
| office_dropdown | OutlinedDropdown (Step 1) | label "Office", placeholder "Select office", leading icon `location_24_regular` 24dp, trailing chevron_down_24_regular, margin_horizontal 16dp, margin_bottom 12dp, min_height 56dp. Bottom sheet on tap listing officeList (Kisumu West Branch / Kisumu East Branch / Kisumu Central Branch from demo). Selected: text primary onSurface, chevron rotates 180°. | Tap → shows sheet → select item → OnOfficeSelect(officeId, officeName) |
| currency_dropdown | OutlinedDropdown (Step 1) | label "Currency", default "KES", leading icon `money_24_regular` 24dp, options [KES, USD, UGX, TZS]. Same shape as office_dropdown. | Tap → sheet → OnCurrencyChange(value) |
| meeting_day_dropdown | OutlinedDropdown (Step 1) | label "Meeting Day", leading icon `calendar_24_regular` 24dp, options [Monday..Sunday]. Same shape. Demo default: "Monday". | Tap → sheet → OnMeetingDaySelect(day) |
| meeting_time_picker | OutlinedTextField+TimePicker (Step 1) | label "Meeting Time", leading icon `clock_24_regular` 24dp, tap opens Material TimePicker dialog. Demo default: "09:00". Required. | Tap → OS TimePicker → OnMeetingTimeSelect(time) |
| share_value_field | OutlinedTextField (Step 2, VSLA) | label "Share Value (KES per share)", leading icon `money_24_regular` 24dp, keyboard numeric, prefix "KES" grouping semibold onSurfaceVariant. Visible when `typeConfig.contribution_model == 'SHARE_BASED_VARIABLE'`. Required. Demo: "200". | Type → OnShareValueChange |
| share_min_field | OutlinedTextField (Step 2, VSLA) | label "Min Shares per Meeting", keyboard numeric, min_height 56dp. Visible when SHARE_BASED_VARIABLE. Demo: "1". | Type → OnShareMinChange |
| share_max_field | OutlinedTextField (Step 2, VSLA) | label "Max Shares per Meeting", keyboard numeric. Visible when SHARE_BASED_VARIABLE. Demo: "5". Validation: shareMax >= shareMin. | Type → OnShareMaxChange |
| contribution_amount_field | OutlinedTextField (Step 2, ROSCA/SHG) | label "Fixed Contribution per Meeting (KES)", leading icon `money_24_regular`, keyboard numeric, prefix "KES". Visible when `typeConfig.contribution_model != 'SHARE_BASED_VARIABLE'`. Required. Demo (ROSCA): "500". | Type → OnContributionAmountChange |
| payout_order_dropdown | OutlinedDropdown (Step 2, ROSCA only) | label "Payout Order Method", leading icon `arrow_sort_24_regular`, options [FIXED_ORDER, LOTTERY, AUCTION, NEED_BASED]. Visible when `typeConfig.pool_model == 'ROTATING_PAYOUT'`. Demo (ROSCA): "LOTTERY". | Tap → sheet → OnPayoutOrderChange(method) |
| loan_multiplier_field | OutlinedTextField (Step 2, shared) | label "Loan Multiplier (×savings)", keyboard numeric, helper text "Members can borrow up to {{value}}× their savings" bodyMedium textSecondary. Demo: "3". | Type → OnLoanMultiplierChange |
| interest_rate_field | OutlinedTextField (Step 2, shared) | label "Interest Rate (%)", keyboard numeric, suffix "%" onSurfaceVariant, helper "Flat rate per cycle". Demo: "10". | Type → OnInterestRateChange |
| cycle_length_field | OutlinedTextField (Step 2, shared) | label "Cycle Length (months)", keyboard numeric, helper "Share-out at end of cycle". Demo: "12". | Type → OnCycleLengthChange |
| fine_amount_field | OutlinedTextField (Step 2, shared) | label "Late Penalty / Fine (KES)", keyboard numeric, prefix "KES", helper "Charged for missed meetings". Demo: "50". | Type → OnFineAmountChange |
| social_fund_toggle | ListTileWithSwitch (Step 2) | Row: leading icon `heart_24_regular` 24dp accent (#FF8F00), title "Enable Social / Welfare Fund" titleMedium onSurface, subtitle "Portion of corpus for emergencies (funerals, health)" bodyMedium textSecondary, trailing Material 3 Switch. Track colour when on: accent100 (#FFE082); thumb accent700 (#FF8F00). Card wrapper: background surface, cornerRadius md (12dp), margin_horizontal 16dp, margin_bottom 12dp, padding 16dp. | Toggle → OnSocialFundToggle(enabled) |
| social_fund_percent_field | OutlinedTextField (Step 2) | label "Social Fund % of Corpus", keyboard numeric, suffix "%", default "5", helper "Deducted from shareout". Visible when `socialFundEnabled == true`. Renders indented (margin_left 32dp) as child of the toggle card visually. | Type → OnSocialFundPercentChange |
| max_members_field | OutlinedTextField (Step 3) | label "Max Members", leading icon `people_24_regular`, keyboard numeric, default "30", helper "Recommended: 15–30 members". Required. Validation: value ≥ 2. Demo (VSLA): "20". | Type → OnMaxMembersChange |
| review_card | Card (Step 4) | Background surface (#FFFFFF), elevation 2dp, cornerRadius lg (16dp), padding 20dp, margin_horizontal 16dp, margin_bottom 16dp. Contains 3 sections (Identity, Rules, Members) with sub-headers labelLarge (14sp) primary700, followed by 2-column key/value rows: label textSecondary bodyMedium at left, value onSurface bodyLarge at right, monospace for amounts. Section dividers: 1dp borderSubtle (#EEEEEE) height, margin_vertical 12dp. VSLA demo renders: Identity {Type: VSLA, Name: Mwangaza Women's Group, Office: Nairobi Head Office, Currency: KES, Meeting: Monday at 09:00}; Rules {Share Value: KES 200/share, Shares per Meeting: 1–5 shares, Loan Multiplier: 3× savings, Interest Rate: 10% flat, Cycle Length: 12 months, Late Fine: KES 50, Social Fund: 5% of corpus}; Members {Max Members: 20}. ROSCA variant hides share rows, shows Contribution + Payout Order rows. | Non-interactive (informational summary). Fields are edited by tapping Back and returning to earlier steps. |
| offline_notice_banner | Banner (inside review_card, Step 4 only) | Background tertiaryContainer (#BBDEFB — info 100-ish), cornerRadius md (12dp), padding 12dp, margin_top 12dp inside review_card. Leading icon `wifi_off_24_filled` 20dp info (#1565C0). Text "You are offline. This group will be created when you reconnect." bodyMedium onTertiaryContainer (#0D47A1). live_region polite for screen reader. Visible only when `isOffline == true`. | Non-interactive |
| back_step_button | TextButton | label "Back", leading icon `arrow_left_24_regular` 20dp primary, text primary (#2E7D32) labelLarge semibold. Visible when `currentStep > 1`. min_touch_target 48dp. Positioned as leading button in pinned bottom action row. Padding 12dp horizontal, corner_radius 8dp. | Tap → OnPreviousStep |
| next_button | FilledButton | label "Next", trailing icon `arrow_right_24_regular` 20dp onPrimary. Background primary (#2E7D32), text onPrimary (#FFFFFF), cornerRadius full (9999dp), min_height 56dp, full_width (minus 16dp horizontal margin when no back_step_button; flex-1 sharing row otherwise). Visible when `currentStep < 4`. Disabled state (pressed but validationErrors non-empty): background primary at 40% opacity. | Tap → OnNextStep |
| submit_button | FilledButton | label "Create Group", leading icon `checkmark_24_regular` 20dp onPrimary. Background primary (#2E7D32), text onPrimary, cornerRadius full (9999dp), min_height 56dp, full_width. Visible when `currentStep == 4`. Loading state: spinner (CircularProgressIndicator size=24dp onPrimary) replaces both icon + label; button disabled. | Tap → OnSubmit → COMP-GRP-001 POST /companion/groups |
| error_banner | Card (Step 4 error state) | Background errorContainer (#FFDAD6), cornerRadius md (12dp), padding 12dp, margin_horizontal 16dp, margin_top 8dp. Leading icon `warning_24_filled` 20dp onErrorContainer (#410002). Text bodyMedium onErrorContainer (dynamic from GroupCreateError.message_key: error_validation / error_network / error_server / error_auth). Trailing "Retry" TextButton labelLarge onErrorContainer bold — only visible when `error.retry == true`. live_region assertive. | "Retry" tap → OnSubmit (re-fires COMP-GRP-001) |

**Layout structure (Step 4 / review + submit)**:
```
[TopBar — primary tint, 56dp, close icon + "New VSLA Group"]
[8dp gap]
[GroupTypeBanner chip — "VSLA" — 32dp, primaryContainer]
[16dp gap]
[StepIndicator — 4 pills row, Identity=✓ Rules=✓ Members=✓ Review=active]
[24dp gap]
[ReviewCard — 16dp side margins, 2dp elevation]
  ├─ "Review Group Details" titleMedium onSurface
  ├─ 20dp gap
  ├─ "Identity" section header
  ├─ Group Type    ·   VSLA
  ├─ Name          ·   Mwangaza Women's Group
  ├─ Office        ·   Nairobi Head Office
  ├─ Currency      ·   KES
  ├─ Meeting       ·   Monday at 09:00
  ├─ [divider]
  ├─ "Rules" section header
  ├─ Share Value          ·   KES 200 / share      (VSLA row)
  ├─ Shares per Meeting   ·   1–5 shares            (VSLA row)
  ├─ Loan Multiplier      ·   3× savings
  ├─ Interest Rate        ·   10% flat
  ├─ Cycle Length         ·   12 months
  ├─ Late Fine            ·   KES 50
  ├─ Social Fund          ·   5% of corpus
  ├─ [divider]
  ├─ "Members" section header
  ├─ Max Members   ·   20
  └─ [offline_notice_banner if isOffline]
[24dp gap]
[BottomActionRow — 16dp side padding, 12dp vertical padding]
  ├─ [Back] TextButton     (24dp gap)     [Create Group] FilledButton flex-1
```

---

## Interaction Patterns

**Step advance (all steps)**:
1. User taps `next_button`
2. OnNextStep dispatched — client validates current step's required fields against `typeConfig`
3. On pass: `currentStep` increments; visible components swap via Compose `AnimatedContent` with slide-horizontal transition (duration medium_1 = 250ms, standard easing)
4. On fail: `validationErrors` map populated per-field; each field renders 2dp danger border + helper text; wizard remains on current step; scroll animates to first error

**Step back**:
1. User taps `back_step_button`
2. OnPreviousStep dispatched — no validation, no field clearing
3. `currentStep` decrements; components swap via slide-horizontal reverse (250ms)
4. All previously entered values retained so user can review/edit

**Adaptive Step 2 rendering (drives from typeConfig)**:
- VSLA (SHARE_BASED_VARIABLE + ACCUMULATING): shows share_value_field, share_min_field, share_max_field, hides contribution_amount_field, hides payout_order_dropdown
- ROSCA (FIXED_AMOUNT + ROTATING_PAYOUT): hides share_* fields, shows contribution_amount_field, shows payout_order_dropdown
- SHG / JLG (FIXED_AMOUNT + ACCUMULATING): hides share_* fields, shows contribution_amount_field, hides payout_order_dropdown
- Shared rules (loan_multiplier, interest_rate, cycle_length, fine_amount, social_fund) always visible
- Fields animate in/out with fade+height transition (short_3 = 150ms) when the wizard first mounts Step 2

**Social fund toggle**:
1. User taps the switch on `social_fund_toggle`
2. Haptic light impact; switch thumb slides accent700 direction (short_3 = 150ms)
3. `socialFundEnabled` set to true
4. `social_fund_percent_field` animates in below the toggle (fade+height, 150ms)

**Submit**:
1. User taps `submit_button` on Step 4
2. Button transitions to loading state — icon+label replaced by CircularProgressIndicator (150ms cross-fade); button disabled
3. `isSubmitting = true` → screen state = `submitting`; back_step_button disabled
4. COMP-GRP-001 POST /companion/groups called with CreateGroupOrchestrationRequest assembled from state
5. On success (2xx): response {groupId, fineractCenterId, inviteCode} written to groups_cache + group_type_config_cache; NavigateToGroupDashboard(groupId) emitted; screen navigates
6. On 400 (validation): validationErrors populated; screen state = `error`; error_banner shows "error_validation"
7. On 409 (group-name-taken): screen state = `error`; ShowSnackbar("This group name is already taken.") emitted
8. On 5xx: screen state = `error`; error_banner shows "error_server" with Retry button (retry=true)
9. On offline (NetworkMonitor reports no connectivity): request serialised to sync_queue via Bookkeeper; snackbar "Queued for sync when you reconnect" via ShowSnackbar; offline_notice_banner remains; screen still navigates to group-dashboard with a locally-generated temp groupId

**Close/Back exit**:
1. User taps close icon on top_bar OR system back
2. OnBack dispatched → NavigateBack event
3. Wizard state discarded (currentStep, all form fields, validationErrors cleared on ViewModel disposal)
4. Nav pops to group-type-picker (or group-list depending on entry path)
5. No confirmation dialog — the wizard is client-only until Step 4 Submit; discarding is safe

---

## Accessibility

**WCAG AA compliance**:
- Primary (#2E7D32) on white: 5.83:1 — passes AA normal text
- onPrimary (#FFFFFF) on primary (#2E7D32): 13.5:1 — passes AAA
- onPrimaryContainer (#1B5E20) on primaryContainer (#C8E6C9): 8.6:1 — passes AAA
- Danger (#C62828) on errorContainer (#FFDAD6): 6.9:1 — passes AA
- Text primary (#212121) on background (#FAFAFA): 15.4:1 — passes AAA
- Text secondary (#616161) on background (#FAFAFA): 5.9:1 — passes AA

**Touch targets**: All interactive elements minimum 48dp. Primary CTAs (next_button, submit_button) are 56dp for confidence. TextButtons include 12dp side padding so labelled tap area meets 48dp.

**Content descriptions**:
- top_bar close icon: "Close and discard new {{groupTypeName}} group"
- group_type_banner: "Group type: {{groupTypeName}}"
- step_indicator: live_region polite; announces "Step {{currentStep}} of 4: {{step_label}}" on step change
- Each form field: label read as accessibility label; validationErrors read as live_region assertive on populate
- social_fund_toggle: "Social welfare fund {{'enabled' if socialFundEnabled else 'disabled'}}. Portion of corpus for emergencies."
- submit_button: "Create Group. Sends form to companion API."
- submit_button loading state: "Creating group, please wait." announced once when isSubmitting becomes true
- offline_notice_banner: live_region polite; announced once when appears
- error_banner: live_region assertive; announced immediately on error

**Focus order (Step 1 = Identity)**: TopBar close → step_indicator (informational skip) → group_name_field → office_dropdown → currency_dropdown → meeting_day_dropdown → meeting_time_picker → next_button

**Focus order (Step 2 = Rules, VSLA variant)**: back_step_button → step_indicator (skip) → share_value_field → share_min_field → share_max_field → loan_multiplier_field → interest_rate_field → cycle_length_field → fine_amount_field → social_fund_toggle → social_fund_percent_field (if visible) → next_button

**Focus order (Step 2 = Rules, ROSCA variant)**: back_step_button → step_indicator (skip) → contribution_amount_field → payout_order_dropdown → loan_multiplier_field → interest_rate_field → cycle_length_field → fine_amount_field → social_fund_toggle → next_button

**Focus order (Step 4 = Review)**: back_step_button → review_card (traversed heading-by-heading + row-by-row via TalkBack heading nav) → submit_button. On error state, error_banner injected before submit_button.

**Keyboard / IME behaviour**: All text fields opt into IME action `next` except the final visible field on each step (uses `done`). meeting_time_picker opens the OS TimePicker dialog rather than accepting text input to avoid IME confusion.

**Screen reader mode**: When TalkBack / VoiceOver active, the wizard NEVER auto-advances on the last-field IME action — the user must explicitly tap `next_button`. The step transition animation is replaced by an instant swap. The submitting state announces "Creating group" once (not repeatedly). The offline banner announces once on visibility change; not on every re-render.

---

## Empty / Error / Loading States

**Empty (Step 1 first mount)**: All form fields render at their `default` values from `state_model` (currency = "KES", meeting_day empty, etc.). The `next_button` is enabled at all times — validation runs on tap; empty required fields produce inline errors rather than a globally-disabled CTA. This mirrors MifosSave's "trust the user, guide with errors" pattern used in Login (see mockups/authentication/MOCKUP.md).

**Loading (submitting state)**: submit_button transitions to spinner-only; back button disabled; all fields disabled (opacity 40%); step indicator remains active state but pill labels dimmed. No overlaid scrim — the wizard body stays visible so the user can see what's being sent. Duration expectation: <2s for online, <500ms for offline queue.

**Error (post-submit)**: error_banner appears above the review_card with contextual message. For `error_validation` (400): banner reads "Please fix the highlighted fields." and the wizard silently rewinds to the earliest step with a populated `validationErrors` entry (Step 1 if group_name blank, Step 2 if rules invalid, etc.). For `error_network`: banner shows offline queue message + "Retry" button; if user taps Retry, the request is re-queued (idempotent on name+officeId+userId). For `error_server`: banner shows "Server error. Please retry." with Retry button. For `error_auth`: banner briefly displays "Session expired." then redirects to login (500ms delay).

**Offline (isOffline == true)**: offline_notice_banner appears inside the review_card at the bottom of Step 4. The submit_button label changes to "Queue for Sync" (bodyLarge onPrimary). On Submit tap, the request is serialised into `sync_queue` via Bookkeeper with `entity_type=CREATE_GROUP_ORCHESTRATE`, `idempotency_key=name+officeId+userId`. Screen still navigates to group-dashboard with the temp groupId; a persistent chip on the group-dashboard header reads "Pending sync — will complete when online". The offline banner is styled with the info palette (tertiaryContainer + onTertiaryContainer) rather than warning/danger because offline queuing is a first-class expected behaviour, not an error.

**Success**: No visible success surface on the wizard itself — the transition to group-dashboard is immediate. If offline, the group-dashboard renders with a "sync pending" chip; if online, the dashboard shows the new inviteCode (from CreateGroupOrchestrationResponse) prominently in a share-ready card.

---

## Notes for Implementation

- **Adaptive fields (Step 2)** — driven by `typeConfig.contribution_model` and `typeConfig.pool_model`; ViewModel exposes `visibleStep2Fields: List<String>` computed once when typeConfig is set to keep the Composable declarative.
- **Companion API atomicity** — Submit calls a SINGLE COMP-GRP-001 endpoint; that endpoint orchestrates createCenter + activate + associateClients + assignRole ORGANIZER + dt_group_type_config provisioning in one backend transaction. The client MUST NOT hand-roll these Fineract calls; the presence of a `GroupRepository` DI-bound method `createGroupOrchestrated(request): Response` is the contract.
- **Offline** — SyncQueueRepository serialises the raw CreateGroupOrchestrationRequest; NetworkMonitor observes connectivity; Bookkeeper writes+drains via Store5 (`core/store/GroupCreationStore`).
- **Session** — SessionManager provides `userId` which is embedded in the request as `userId` (creator becomes ORGANIZER automatically).
- **Icon set** — FluentIcons throughout (people_24, location_24, money_24, calendar_24, clock_24, arrow_sort_24, arrow_left_24, arrow_right_24, checkmark_24, warning_24, wifi_off_24, heart_24, category_24, close_24, chevron_down_24). Rendered via `androidx.compose.material.icons` on Android + shared Compose Multiplatform Icons on iOS/desktop for parity.
- **Analytics** (legacy_metadata.analytics — see docs.yaml):
  - screen_view: `group_create_viewed`
  - step advance: `group_create_step_advanced { step: Int }`
  - submit tap: `group_create_submitted { is_offline: Boolean }`
  - offline queue: `group_create_queued_offline`
  - success: `group_created { group_id: String, cycle_months: Int }`
- **Route** — `/groups/create` — mounted under the group-management nav graph. Nav args: `typeConfig: GroupTypeConfig` (required, JSON-serialisable). No deep-link support (opens only via in-app group-type-picker flow).

---

## Related Screens

- **group-type-picker** — Entry point. Forwards `typeConfig` as a nav_arg.
- **group-list** — Legacy entry point (`fab_tap`) — now routes via group-type-picker first for consistency.
- **group-dashboard** — Success destination. Receives `{groupId}` and (if applicable) `{inviteCode}`.
- **join-with-code** — Consumes the `inviteCode` field returned from CreateGroupOrchestrationResponse for member self-signup.
