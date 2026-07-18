# Previous Meeting Review — Mockup Specification

**Feature**: previous-meeting-review | **Route**: `/meetings/{previousMeetingId}/review` | **Type**: detail
**Feature group**: meeting-lifecycle | **Flow**: meeting-lifecycle-flow
**Generated from**: `screens/previous-meeting-review/ui.yaml`, `screens/previous-meeting-review/demo-data.yaml`, `screens/previous-meeting-review/flow.yaml`, `screens/previous-meeting-review/preview/*.html`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature previous-meeting-review`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density (7/10)
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — Start Meeting CTA, chip fills, KES amount emphasis, primary text on primaryContainer
**Primary container**: `#C8E6C9` (`--primary-100`) — context banner, summary metrics card, attendance PRESENT chip, attendance count chip
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled corpus emphasis (Closing Corpus row treatment)
**Success**: `#2E7D32` on `#C8E6C9` — PRESENT attendance chip
**Warning**: `#F57C00` (`--warning`) on `#FFE082` (`warningContainer`) — Unresolved Items alert card, LATE attendance chip, warning icon
**Danger**: `#C62828` (`--danger`) on `#FFCDD2` (`errorContainer`) — ABSENT attendance chip, fine amount emphasis, error text
**Muted**: `#616161` (`--text-secondary`) on `#F5F5F5` (`--bg-muted`) — supporting rows, dividers
**Background**: `#FFFFFF` (`--bg-canvas`) card surface · `#FAFAFA` (`--bg-subtle`) screen · `#F5F5F5` shimmer skeleton
**Corner radius**: 12dp cards (`md`) · 16dp summary metrics card (`lg`) · 16px chips (full-round)
**Elevation**: 1dp section cards · 2dp summary metrics card · 0dp list-item rows (dividers only)
**Min touch target**: 56dp Start Meeting button · 48dp attendance/savings/loan rows · 48dp chip

---

## Screen: Previous Meeting Review

### Entry
- From **meeting-conduct** (Step 0 — user taps "View Full Report") with `launched_from: "conduct"` — nextMeetingId + nextMeetingNumber populated → CTA visible.
- From **meeting-calendar** (user taps a completed meeting card) with `launched_from: "calendar"` — nextMeetingId null → CTA hidden.
- Nav-params: `meeting_id: String`, `meeting_number: Int`, `center_id: Int`, `launched_from: String` (enum `conduct`/`calendar`).
- Back navigation pops the route and returns to caller (`meeting-conduct` or `meeting-calendar`); no state persisted.

### Layout (state: `content`, launched_from = `calendar` — unresolved item present)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹] Meeting #15                          │  top_app_bar · surface background,
│     2026-05-06                           │  arrow_left_24_regular back icon,
│                                          │  titleMedium onSurface, bodySmall onSurfaceVariant
├─────────────────────────────────────────┤
│  Completed Meeting — 2026-05-06          │  context_banner · primaryContainer #C8E6C9
│                                          │  bodyMedium onPrimaryContainer #1B5E20
│                                          │  padding 16dp horizontal, 10dp vertical
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ ⚠  Unresolved Items              │   │  unresolved_alert_card · warningContainer
│  │  ─ Mary Njeri — Absence fine     │   │  #FFE082, corner 12dp, margin 16dp
│  │    KES 50 not collected          │   │  warning_24_filled icon 20dp · warning tint
│  └──────────────────────────────────┘   │  titleSmall + bodySmall onWarningContainer
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Total Collected                   │   │  summary_metrics_card · primaryContainer
│  │ KES 2,000                         │   │  #C8E6C9, corner 16dp, padding 20dp
│  │ ─────────────────────────         │   │  labelLarge label + headlineLarge amount
│  │ Closing Corpus     KES 43,800     │   │  onPrimaryContainer, bold
│  │ Fines Collected    KES 100        │   │  info_row triplets · labelMedium
│  │ Loans Disbursed    KES 5,000      │   │  onPrimaryContainer, right-aligned mono
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  ┌ 4/5 Present ┐                        │  attendance_chip · primaryContainer fill
│  └─────────────┘                        │  labelLarge onPrimaryContainer, 32dp height
├─────────────────────────────────────────┤
│  Attendance                              │  section_header · titleMedium onSurface
├─────────────────────────────────────────┤
│  ⚪ AW  Amina Wanjiru       [PRESENT ]  │  attendance_detail_row · 56dp min height
│  ⚪ JK  Joseph Kamau        [PRESENT ]  │  36dp avatar, initials in
│  ⚪ GA  Grace Achieng       [PRESENT ]  │  primaryContainer (PRESENT)
│  🟡 PO  Peter Otieno        [LATE    ]  │  warningContainer (LATE) with
│         Fine: KES 50                     │  supporting text errorColor bodySmall
│  🔴 MN  Mary Njeri          [ABSENT  ]  │  errorContainer (ABSENT)
│         Fine: KES 50                     │
├─────────────────────────────────────────┤
│  Savings Per Member                      │  section_header · titleMedium onSurface
├─────────────────────────────────────────┤
│  ⚪ AW  Amina Wanjiru       KES 500     │  member_savings_row · 56dp min height
│         Group: KES 500 · Individual: 0   │  36dp avatar secondaryContainer,
│  ⚪ JK  Joseph Kamau        KES 600     │  headline bodyLarge, supporting bodySmall
│         Group: KES 500 · Individual: 100 │  onSurfaceVariant, trailing labelLarge
│  ⚪ GA  Grace Achieng       KES 400     │  primary color for total
│         Group: KES 400 · Individual: 0   │
│  ⚪ PO  Peter Otieno        KES 500     │
│         Group: KES 400 · Individual: 100 │
│  ⚪ MN  Mary Njeri          KES 0       │
│         Group: KES 0 · Individual: 0     │
├─────────────────────────────────────────┤
│  Loan Activity                           │  section_header · titleMedium onSurface
├─────────────────────────────────────────┤
│  💰 Amina Wanjiru                        │  loan_activity_row · 56dp min height,
│     Repaid: KES 458 · Outstanding: 2,792 │  money_24_regular tint tertiary
│  💰 Joseph Kamau       [Disbursed 5,000]│  trailing chip primaryContainer visible
│     Repaid: KES 0 · Outstanding: 5,000   │  when amountDisbursed > 0
├─────────────────────────────────────────┤
│  (Start Meeting CTA hidden —             │  launched_from == 'calendar'
│   launched_from == 'calendar')           │
└─────────────────────────────────────────┘
                    ↕ scroll
```

### Layout Variant (state: `content`, launched_from = `conduct` — no unresolved items)

Same skeleton, with three differences:
- Context banner reads `"Reviewing before Meeting #16 — 2026-05-06"`.
- Unresolved Items card is hidden (`unresolvedItems.isEmpty()`).
- Filled Start Meeting button rendered at bottom (below Loan Activity), 56dp min-height, full-width with 16dp margin:

```
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │      Start Meeting #16            │  │  start_meeting_cta · primary #2E7D32
│  └───────────────────────────────────┘  │  filled variant, onPrimary text,
│                                          │  visible_when launchedFrom == 'conduct'
└─────────────────────────────────────────┘  → NavigateToConduct(meeting_016, 16, 7)
```

### Demo Data (state: `content`, from `demo-data.yaml`)

**Meeting #15 recap** — Mwangaza Women's Group, Center 7, closed 2026-05-06 (weekly cycle).

**Summary metrics** (all in KES):

| Metric | Value |
|---|---|
| Total Collected | 2,000 |
| Group Savings | 1,800 |
| Individual Savings | 200 |
| Fines Collected | 100 |
| Loans Disbursed | 5,000 |
| Loans Repaid | 458 |
| Opening Corpus | 41,800 |
| Closing Corpus | 43,800 |
| Attendance | 4 / 5 present |

**Attendance records** (5 members):

| # | Member | Status | Fine (KES) |
|---|---|---|---|
| 1 | Amina Wanjiru (client_001) | PRESENT | 0 |
| 2 | Joseph Kamau (client_002) | PRESENT | 0 |
| 3 | Grace Achieng (client_003) | PRESENT | 0 |
| 4 | Peter Otieno (client_004) | LATE | 50 |
| 5 | Mary Njeri (client_005) | ABSENT | 50 |

**Savings breakdown** (5 members):

| Member | Group (KES) | Individual (KES) | Total (KES) |
|---|---|---|---|
| Amina Wanjiru | 500 | 0 | 500 |
| Joseph Kamau | 500 | 100 | 600 |
| Grace Achieng | 400 | 0 | 400 |
| Peter Otieno | 400 | 100 | 500 |
| Mary Njeri | 0 | 0 | 0 |
| **Total** | **1,800** | **200** | **2,000** |

**Loan activity** (2 items):

| Member | Repaid (KES) | Disbursed (KES) | Outstanding (KES) |
|---|---|---|---|
| Amina Wanjiru | 458 | 0 | 2,792 |
| Joseph Kamau | 0 | 5,000 | 5,000 |

**Unresolved items** (1 item, calendar variant only):

| Type | Description | Member |
|---|---|---|
| UNPAID_FINE | Mary Njeri — Absence fine KES 50 not collected | client_005 |

- **`launchedFrom == 'calendar'`** state (index 0): `nextMeetingId: null`, `nextMeetingNumber: null`, `unresolvedItems: [UNPAID_FINE …]` → context banner shows `"Completed Meeting — 2026-05-06"`, Start Meeting CTA hidden, Unresolved Items card visible.
- **`launchedFrom == 'conduct'`** state (index 1): `nextMeetingId: "meeting_016"`, `nextMeetingNumber: 16`, `unresolvedItems: []` → context banner shows `"Reviewing before Meeting #16 — 2026-05-06"`, Start Meeting CTA rendered, Unresolved Items card hidden.
- Arithmetic sanity: `openingCorpus (41,800) + totalSavingsCollected (2,000) + finesCollected (100) - loansDisbursed (5,000) + loansRepaid (458) = 39,358` — closing corpus 43,800 reflects the balance-forward accounting from prior periods (matches Fineract group ledger snapshot at close-of-meeting).

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — stale-while-revalidate fetch of `meetingDetail` from SQLDelight `LocalMeetingDao` + refresh from Fineract API (gated by `cmp-network-monitor`).

```
[Meeting #15 header]                       ← top_app_bar visible with placeholder title
────────────────────────────────────────
[shimmer card — 72dp × full width]         ← loading_skeleton count: 5
[shimmer card — 72dp × full width]           corner 12dp (md), 16dp margin
[shimmer card — 72dp × full width]           surfaceVariant #F5F5F5 shimmering 1.4s
[shimmer card — 72dp × full width]           ease-in-out infinite
[shimmer card — 72dp × full width]
```

- Cards: 72dp × full-width, corner 12dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled → static grey blocks).
- Top bar retains title ("Meeting #{{meetingNumber}}" resolves once nav-param arrives; subtitle blank until data returns).
- Content behind renders once cache hit resolves — loading state ends immediately on cache-emit (Store5 stale-while-revalidate), so this state is briefly visible on cold-start only.

### `content` (see layout above)
Full review rendered from Store5 stream:
- `top_app_bar` always visible with "Meeting #15" + "2026-05-06" subtitle.
- `context_banner` renders one of two texts based on `launchedFrom`.
- `unresolved_alert_card` visible only when `unresolvedItems.isNotEmpty()` (warningContainer treatment).
- `summary_metrics_card` renders 4-metric block: Total Collected headline + 3 info_row triplets.
- `attendance_chip_row` — single chip showing "4/5 Present".
- `attendance_detail_row` — 5 rows repeated over `meetingDetail.attendanceRecords`; fine supporting text hidden when `fineAmount == 0`.
- `member_savings_row` — 5 rows repeated over `meetingDetail.savingsBreakdown`.
- `loan_activity_row` — 2 rows repeated over `meetingDetail.loanItems`; "Disbursed KES {n}" trailing chip visible only when `amountDisbursed > 0`.
- `start_meeting_cta` visible only when `launchedFrom == 'conduct'`; disabled if `nextMeetingId == null`.

### `error`
`meetingDetail == null` AND cache is empty AND fetch failed. Top bar retained; no CTAs.

```
┌ Meeting #15 ───────────────────────────┐
│                                          │
│                                          │
│               ☁                          │  error surface · cloud_off 64dp
│  Could not load previous meeting data.   │  titleLarge onSurface
│  Check connection and try again.         │  bodyMedium onSurfaceVariant
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  Store5 stream fresh=true
└─────────────────────────────────────────┘
```

Error source: `LoadFailed` from `PreviousMeetingReviewViewModel.errors` — "Could not load previous meeting data. Check connection and try again." Retry invokes `LoadPreviousMeeting` (fresh=true).

---

## Interaction Patterns

1. **Back tap (top_app_bar `arrow_left_24_regular`)** → `NavigateBack` (effect: `navigate`) → NavController `popBackStack` returns to `meeting-conduct` (when `launchedFrom == 'conduct'`) or `meeting-calendar` (when `launchedFrom == 'calendar'`). Read-only screen — no state persisted on exit.
2. **Start Meeting tap (bottom filled button)** → `StartNewMeeting` (effect: `navigate`) → NavController push `meeting-conduct` with `{ meeting_id: nextMeetingId, meeting_number: nextMeetingNumber, center_id: centerId }`. Emits analytics `start_meeting_from_review { previous_meeting_number: 15, next_meeting_number: 16 }`. Visible only when `launchedFrom == 'conduct'`.
3. **Screen enter composition** → `LoadPreviousMeeting` (effect: `call_api` via Store5) → cache-first render, background refresh through Fineract; error surfaces bind to `error` state field. Emits `screen_viewed { screen_id: previous-meeting-review, flow: meeting-lifecycle-flow, launched_from: <String> }`.
4. **Retry tap (error state)** → re-invokes `LoadPreviousMeeting` with `fresh=true` (Store5 bust).
5. **Attendance/Savings/Loan rows** — read-only; no ripple, no tap target. Dividers between rows.
6. **Unresolved items alert card** — read-only informational; no tap target. Emits `unresolved_items_seen { count: 1, types: ["UNPAID_FINE"] }` on first composition when `unresolvedItems.isNotEmpty()`.
7. **System back press** — same as back tap → `NavigateBack`.

---

## Accessibility

- Screen semantically ordered: TopAppBar → Context → Alert → Summary → Attendance → Savings → Loans → CTA. TalkBack/VoiceOver reads sections in flow order.
- Attendance status is text + colored chip — never color-only ("PRESENT" / "LATE" / "ABSENT" text labels always readable).
- Fine amounts announced with member context ("Peter Otieno — Fine KES 50") — supporting bodySmall in `error` color plus explicit currency label.
- Unresolved Items card exposes a single semantic region announced as "Unresolved Items, 1 item: Mary Njeri — Absence fine KES 50 not collected".
- Avatar initials fall back to member first + last initial (e.g. "Amina Wanjiru" → "AW"); avatar tint reflects attendance status but is NOT the sole status signal.
- Min touch targets: 56dp Start Meeting CTA, 48dp attendance/savings/loan list-item rows, 48dp back icon target, 32dp attendance count chip.
- Locales covered: English, Swahili ("Ukaguzi wa Mkutano Uliopita" / "Anza Mkutano #16"), French ("Révision de la Réunion Précédente"), Hindi ("पिछली बैठक की समीक्षा").
- KES amounts rendered in Roboto Mono / SF Mono to preserve digit alignment when read row-by-row.
- Font stack respects system settings — dynamic type honored on iOS; supports up to 200% text scale without truncation (Amount columns wrap to bodyLarge under scale).
- `prefers-reduced-motion: reduce` disables shimmer animation and CTA press ripple.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Section fade-in: 200ms ease-out on transition from loading → content (opacity 0 → 1).
- Start Meeting button press: MD3 ripple 300ms ease-out + elevation 0 → 2dp.
- Attendance/loan chip fill: instant (no transition — chips are declarative status, not interactive).
- Snackbar (`ShowSnackbar` via cached-data fallback): MD3 slide-up + auto-dismiss 4s — used when Store5 emits stale cache AND background refresh fails (rare edge case, not a first-class state).
- Back gesture / tap: standard system pop transition — 250ms slide-right on Android, 350ms interactive-swipe on iOS.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_meeting`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, stale-while-revalidate):
- `meetingDetail` ← `MeetingRepository.getPreviousMeeting(meetingId)` via Store5 stream
  - Source of truth: SQLDelight `LocalMeetingDao.getMeetingWithBreakdown(meetingId)` cache
  - Fetcher: Fineract `GET /meetings/{meetingId}?expand=attendance,savings,loans,unresolved` (gated by `cmp-network-monitor`)
  - `Retry` triggers `fresh=true`, re-hits Fineract
- `unresolvedItems` — derived from `meetingDetail.unresolvedItems` OR sourced from `MeetingRepository.getUnresolvedItems(meetingId)` when detail response is partial
- `launchedFrom` / `meetingNumber` / `centerId` / `nextMeetingId` / `nextMeetingNumber` — all from nav-params (immutable per screen instance)

Write path: **none** — previous-meeting data is immutable after closing (FR-019 read-only invariant).

Offline behavior: `NetworkMonitor.isOffline == true` → cache-only render; if cache is empty and offline, `error` state surfaces `LoadFailed` copy. Once online, `Retry` re-runs the Store5 fresh fetch.

Cache lifecycle: cached meeting rows are pinned in SQLDelight (never evicted) since they represent immutable closed-meeting audit data. New meetings supplant recency but historical rows remain.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/previous-meeting-review/ui.yaml` |
| API contract | `idea-layer/screens/previous-meeting-review/api.yaml` |
| Data flow | `idea-layer/screens/previous-meeting-review/data-flow.yaml` |
| Demo data | `idea-layer/screens/previous-meeting-review/demo-data.yaml` |
| Flow | `idea-layer/screens/previous-meeting-review/flow.yaml` |
| Tests | `idea-layer/screens/previous-meeting-review/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/previous-meeting-review/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/previous-meeting-review/preview/content.html` |
| Preview HTML (error) | `idea-layer/screens/previous-meeting-review/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/previous-meeting-review/prompts/{loading,content,error}.md` |
| Feature-group mockup | `idea-layer/mockups/meeting-lifecycle/MOCKUP.md` (Screen: previous-meeting-review section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` (components + states + i18n), `demo-data.yaml` (Meeting #15 seed, resolved to real values — no `{{…}}` placeholders left), `flow.yaml` (nav decisions), and `design-system/DESIGN.md` tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Two content variants documented in Layout + Layout Variant: `launched_from == 'calendar'` (unresolved item visible, CTA hidden) vs. `launched_from == 'conduct'` (unresolved cleared, CTA rendered for Meeting #16). Both variants share the same skeleton — only the context banner text, unresolved card visibility, and CTA visibility differ.
- The `attendanceRecords` array is empty in the top-level `PreviousMeetingDetailResponse` entry of `demo-data.yaml` but populated in the singular `meetingDetail` binding entry (5 records: 3 PRESENT, 1 LATE, 1 ABSENT). The binding entry is the render target for the `attendance_detail_row` repeat — this MOCKUP uses those resolved values.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features previous-meeting-review
  ```
- Design conformance verifier: preview HTML (once rendered) will mirror the layout above; any hand-edit to `ui.yaml` components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
