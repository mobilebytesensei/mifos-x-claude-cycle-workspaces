# Meeting Summary — Mockup Specification

**Feature**: meeting-summary | **Route**: `/meetings/{meetingId}/summary` | **Type**: read-only summary
**Feature group**: meeting-lifecycle | **Flow**: meeting-lifecycle-flow
**Generated from**: `screens/meeting-summary/ui.yaml`, `screens/meeting-summary/demo-data.yaml`, `screens/meeting-summary/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature meeting-summary`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar background, hero card, Done CTA, corpus net-change value
**Primary variant**: `#1B5E20` (`--primary-900`) — pressed / long-press state on Done CTA and share icon
**Primary container**: `#C8E6C9` (`--primary-100`) — hero corpus chip, attendance + group-savings metric card backgrounds
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund chip emphasis, secondary highlight (not used as CTA)
**Secondary container**: `#FFE0B2` — individual-savings metric card, avatar backgrounds
**Tertiary container**: `#B2DFDB` — loan-repayments metric card, corpus reconciliation section background
**Warning container**: `#FFF9C4` — fines-collected metric card background
**Warning text**: `#E65100` — fines label + value color
**Error container**: `#FFCDD2` — loans-disbursed metric card background, error state icon tint
**Error text**: `#B71C1C` — LoadFailed banner text
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (skeleton shimmer, dividers)
**On-primary**: `#FFFFFF` — text + iconography on the green hero + Done CTA
**On-surface**: `#212121` — body text on canvas
**On-surface-variant**: `#757575` — labels, subtitles, section headers
**Corner radius**: `24dp xl` hero card · `12dp md` corpus reconciliation card · `12dp lg` skeleton items · `16px` metric cards · `12dp` chip
**Elevation**: 0dp TopAppBar (surface-colored) · 4dp hero_card · 1dp metric cards · 0dp corpus reconciliation card (color-only) · 3dp Done CTA on press
**Min touch target**: 56dp Done button · 48dp TopAppBar share icon · 48dp TopAppBar back icon · 56dp per savings-breakdown row

---

## Screen: Meeting Summary

### Entry
- From **meeting-conduct** (`condition: wizard_submitted_successfully`) — Save-Collection-Sheet flow lands here after the COMP-CAL server call closes the meeting record.
- From **meeting-calendar** (`condition: user_taps_completed_meeting_summary_deep_link`) — deep link from a completed calendar row.
- Nav params: `meeting_id: String`, `meeting_number: Int`, `group_id: Int`.
- Back navigation (TopAppBar arrow OR Done button) pops the route and returns to `meeting-calendar`.

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Meeting #5 Summary        [ ⇪ ]    │  TopAppBar — surface bg, onSurface text
│      12 May 2026                        │  subtitle · bodySmall, onSurfaceVariant
├─────────────────────────────────────────┤  16dp gap
│  ┌────────────────────────────────────┐ │
│  │                                    │ │  hero_card · primary #2E7D32, corner 24dp
│  │  Total Collected                   │ │  labelLarge, onPrimary
│  │  KES 1,750                         │ │  displaySmall, onPrimary, bold, mono
│  │  Meeting #5 · 12 May 2026          │ │  bodyMedium, onPrimary
│  │                                    │ │
│  │  ┌──────────────────────────────┐  │ │  corpus_hero_chip · primaryContainer #C8E6C9
│  │  │ Corpus: KES 64,100           │  │ │  labelMedium, onPrimaryContainer
│  │  └──────────────────────────────┘  │ │
│  └────────────────────────────────────┘ │  24dp padding, 16dp margin, 4dp elevation
├─────────────────────────────────────────┤  12dp gap
│  ┌─────────────────┐  ┌───────────────┐ │
│  │ 👥  Attendance  │  │ 👥 Grp Savings│ │  metric_grid · 2 cols, gap 12dp
│  │ 5 / 5           │  │ KES 1,500     │ │  primaryContainer bg, corner 16px
│  └─────────────────┘  └───────────────┘ │
│  ┌─────────────────┐  ┌───────────────┐ │
│  │ 👤  Ind. Savings│  │ ⭳  Repayments │ │
│  │ KES 250         │  │ KES 2,500     │ │  secondary / tertiary container bgs
│  └─────────────────┘  └───────────────┘ │
│  ┌─────────────────┐  ┌───────────────┐ │
│  │ ⚠  Fines        │  │ ⭱  Disbursed  │ │
│  │ KES 100         │  │ KES 8,000     │ │  warning / error container bgs
│  └─────────────────┘  └───────────────┘ │
├─────────────────────────────────────────┤  16dp gap
│  Savings Breakdown                       │  section header · titleSmall, onSurfaceVariant
│  ┌────────────────────────────────────┐ │
│  │ (AW) Amina Wangari       KES 350   │ │  list-item · 56dp, avatar 36dp, initials
│  │      Group: KES 300 · Ind: KES 50  │ │  bodySmall, onSurfaceVariant · divider
│  ├────────────────────────────────────┤ │
│  │ (JO) Joseph Otieno       KES 300   │ │  trailing labelLarge, primary color
│  │      Group: KES 300 · Ind: KES 0   │ │
│  ├────────────────────────────────────┤ │
│  │ (GW) Grace Wanjiku       KES 400   │ │
│  │      Group: KES 300 · Ind: KES 100 │ │
│  ├────────────────────────────────────┤ │
│  │ (PK) Peter Kamau         KES 350   │ │
│  │      Group: KES 300 · Ind: KES 50  │ │
│  ├────────────────────────────────────┤ │
│  │ (MA) Mary Achieng        KES 350   │ │
│  │      Group: KES 300 · Ind: KES 50  │ │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤  16dp gap
│  ┌────────────────────────────────────┐ │
│  │  Corpus Reconciliation              │ │  card · tertiaryContainer, corner 12dp
│  │                                     │ │  titleSmall, onTertiaryContainer
│  │  Opening              KES 51,750    │ │  info_row · bodyMedium
│  │  Closing              KES 64,100    │ │  info_row · titleMedium (emphasized)
│  │  Net Change           +KES 12,350   │ │  info_row · primary color
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤  24dp gap
│  ┌────────────────────────────────────┐ │
│  │              Done                  │ │  done_button · primary #2E7D32, 56dp
│  └────────────────────────────────────┘ │  full-width, onPrimary label, 16dp margin
└─────────────────────────────────────────┘  24dp bottom padding
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Meeting #5 of Mwangaza Women's Group (12 May 2026, all 5 members present):

**Header totals**
| Field | Value | Source |
|-------|-------|--------|
| meetingNumber | 5 | `MeetingSummaryData.meetingNumber` |
| actualDate | 12 May 2026 | `MeetingSummaryData.actualDate` |
| totalSavingsCollected | KES 1,750 | hero displaySmall |
| closingCorpus | KES 64,100 | hero chip + reconciliation |
| openingCorpus | KES 51,750 | reconciliation opening row |
| attendanceCount / totalMemberCount | 5 / 5 | attendance metric |

**Metric grid values**
| Metric | Value | Container color |
|--------|-------|-----------------|
| Attendance | 5 / 5 | primaryContainer `#C8E6C9` |
| Group Savings | KES 1,500 | primaryContainer `#C8E6C9` |
| Individual Savings | KES 250 | secondaryContainer `#FFE0B2` |
| Loan Repayments | KES 2,500 | tertiaryContainer `#B2DFDB` |
| Fines Collected | KES 100 | warningContainer `#FFF9C4` |
| Loans Disbursed | KES 8,000 | errorContainer `#FFCDD2` |

**Savings Breakdown (5 rows from `SavingsBreakdownItem`)**
| # | Member | Group | Individual | Total (trailing) |
|---|--------|-------|-----------:|-----------------:|
| 1 | Amina Wangari | 300 | 50 | KES 350 |
| 2 | Joseph Otieno | 300 | 0 | KES 300 |
| 3 | Grace Wanjiku | 300 | 100 | KES 400 |
| 4 | Peter Kamau | 300 | 50 | KES 350 |
| 5 | Mary Achieng | 300 | 50 | KES 350 |

**Corpus reconciliation check**
`opening 51,750 + savings 1,750 + repayments 2,500 + fines 100 − disbursed 8,000 = closing 64,100` ✓ (matches the demo dataset — no arithmetic drift).

**Note on loan activity** (from `LoanSummaryItem` — surfaced in the metric grid, not currently listed as a section; consumed by feature-group `loan-management` mockup):
- Peter Kamau received KES 8,000 disbursement (drives the "Loans Disbursed" tile).
- Joseph Otieno repaid KES 1,200 (overdue + standard), others KES 600–700 each (sum = KES 2,500).

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Fetching `MeetingRecordDetail` from Store5 stream (SQLDelight cache warm-start + Fineract `GET /groups/{groupId}/meetings/{meetingId}` fresh fetch gated by `cmp-network-monitor`) OR reading from in-memory meeting-conduct wizard state on same-session entry.

```
┌─────────────────────────────────────────┐
│ [‹] Meeting #{n} Summary       [ ⇪ ]    │  top_app_bar retained (title + share)
├─────────────────────────────────────────┤
│                                          │  16dp gap
│  ┌──────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │   │  loading_skeleton · count 5, height 80dp
│  └──────────────────────────────────┘   │  corner 12dp lg, surfaceVariant #F5F5F5
│  ┌──────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │   │  shimmer 1.4s ease-in-out infinite
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

- 5 skeleton rows at 80dp × full width, corner 12dp lg, surfaceVariant `#F5F5F5` shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled → static surfaceVariant blocks).
- TopAppBar keeps title placeholder "Meeting #{meetingNumber} Summary" but subtitle empty until data arrives.
- Share icon renders inert (no ripple, `pointer-events: none`) while `isSharing == false` AND `meetingSummary == null`.
- Cache hit (warm-start via Store5 SoT) collapses this state to a sub-100ms flash — most re-entries render `content` immediately.

### `content` (see layout above)
Full summary rendered. TopAppBar title `Meeting #{{meetingNumber}} Summary` + subtitle actualDate. Hero card, metric grid, savings breakdown list, corpus reconciliation card, Done button. Share icon in AppBar becomes active — tap dispatches `ShareMeetingReport` (effect: `share_external`) which composes a text/PDF via kmpToolkit + FileKit and opens the OS share-sheet. `isSharing` toggles a circular progress indicator inside the share icon slot while the report composes; the whole screen stays interactive (Done still tappable).

### `error`
Fineract API failed AND cache is empty for this meeting — retry surface.

```
┌─────────────────────────────────────────┐
│ [‹] Meeting Summary            [ ⇪ ]    │  top_app_bar retained (icons inert)
├─────────────────────────────────────────┤
│                                          │
│                                          │
│               ☁                          │  error_banner · cloud_off icon 64dp
│                                          │  errorContainer #FFCDD2 tint
│      Could not load meeting              │  title · titleLarge, onSurface
│              summary                     │
│                                          │
│    No cached copy for Meeting #{n}       │  body · bodyMedium, onSurfaceVariant
│    on this device. Reconnect and         │
│    tap Retry.                            │
│                                          │
│  ┌────────── Retry ────────────────┐    │  cta · primary #2E7D32, 48dp min
│  └─────────────────────────────────┘    │  → dispatches LoadSummary action_contract
│                                          │     effect: call_api, external Store5, fresh
└─────────────────────────────────────────┘
```

- Error copy: `LoadFailed` = "Could not load meeting summary. Showing cached data." When cache is truly empty the copy substitutes to the harder "No cached copy for Meeting #{n} on this device."
- Retry tap re-dispatches `LoadSummary` (effect: `call_api`) via Store5 stream with `fresh=true`.
- Share icon is inert in `error` state (no summary to share).
- Back button still active — returns to `meeting-calendar`.

---

## Interaction Patterns

1. **Screen enters composition** → `LoadSummary` (effect: `call_api`, external: `Store5`) — Store5 stream from SQLDelight SoT + Fineract fetcher `GET /groups/{groupId}/meetings/{meetingId}` gated by `cmp-network-monitor`. On same-session entry from meeting-conduct, in-memory wizard state is projected onto `MeetingSummaryData` and the Store5 stream backfills the SoT.
2. **Share icon tap** → `ShareMeetingReport` (effect: `share_external`, external: `kmpToolkit`, `FileKit`). Composes a text/PDF meeting report from the loaded `MeetingRecordDetail` (totals, savings breakdown, opening/closing corpus) and opens the OS share-sheet via kmpToolkit ShareSheet. Toggles `isSharing = true` while composing (icon → circular progress); auto-resets on share-sheet dismissal. No cash-in/cash-out and no copy retained after dismissal.
3. **Done button tap** → `NavigateDone` (effect: `navigate`, target: `meeting-calendar`). NavController pops the summary route; read-only screen so no persistence or corpus reconciliation runs on the Done tap.
4. **TopAppBar back arrow tap** → same `NavigateDone` action, same effect. UI-level convenience: two affordances → identical VM action.
5. **Retry tap (error state)** → `LoadSummary` re-dispatched with `fresh=true`. Skeletons return until Store5 emits the next snapshot.
6. **System back gesture** → NavController pop (framework default). VM receives no explicit event; equivalent to `NavigateDone`.

---

## Accessibility

- TopAppBar back arrow + share icon each expose distinct `content_description` — `"Back to meeting calendar"` and `"Share meeting report"` (i18n key `share_btn_description`).
- Hero card is a single semantic group: "Total collected KES 1,750, Meeting 5 on 12 May 2026, closing corpus KES 64,100."
- Metric grid tiles each read as "{label}: {value}" with icon marked `aria-hidden` (label carries the meaning). Amount + label are always co-present — never icon-only.
- Savings breakdown row semantic: "{memberName}: group savings KES {group}, individual savings KES {individual}, total KES {sum}".
- Corpus reconciliation rows: "Opening KES 51,750. Closing KES 64,100. Net change positive KES 12,350." Sign (positive/negative) is spoken, not left color-only.
- Done button min touch target 56dp; share + back icons 48dp.
- Currency amounts rendered with Roboto Mono / SF Mono for glanceable tabular alignment; screen reader speaks the numeric value with locale currency ("Kenyan shillings 1,750").
- Locales covered (`i18n:`): English (`Meeting Summary`), Swahili (`Muhtasari wa Mkutano` / `Iliyokusanywa`), French (`Résumé de la réunion`), Hindi (`बैठक सारांश`) — dialect resolution follows the app-shell locale picker.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS; large-text mode reflows the metric grid to a single column below ~360dp width equivalent.

---

## Motion & Feedback

- Skeleton shimmer: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Hero card entry: 200ms fade + 8dp upward slide when transitioning `loading → content`.
- Metric grid: staggered 40ms per tile fade-in on first render (max 240ms total across the 6 tiles) — disabled under `prefers-reduced-motion`.
- Done button press: MD3 elevation 0dp → 3dp + ripple (`--primary-900` `#1B5E20` tint).
- Share icon while `isSharing`: rotating circular progress indicator inside the icon slot, MD3 default 1.4s per revolution.
- Snackbar (`ShowSnackbar`-driven, if share fails): standard MD3 slide-up + auto-dismiss 4s.
- No confetti, no full-screen success animation — matches variance 3/10 · motion 3/10 aesthetic.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`
**Internal lib**: `cmp-network-monitor`
**DI**: `MeetingRepository`, `ShareManager`, `NavigationManager`

Read paths (offline-first, single write happens off-screen at meeting-conduct save):
- `meetingSummary` ← `MeetingRepository.getMeetingSummary(groupId, meetingId)` via Store5 stream
  - Source of truth: SQLDelight `meeting_records` cache
  - Fetcher: Fineract `GET /groups/{groupId}/meetings/{meetingId}` (single-row, gated by `cmp-network-monitor`)
  - Same-session hand-off: meeting-conduct passes the in-memory wizard state directly; Store5 backfill runs in parallel to warm SoT for future re-entries
  - `Retry` re-triggers the stream with `fresh=true`
- Derived: `netCorpusChange = closingCorpus - openingCorpus` (client-side, rendered in reconciliation card).

Write path: **none from this screen.** Persisted totals and opening/closing corpus were reconciled at close by the COMP-CAL `save-collection-sheet` companion RPC during meeting-conduct — this screen is strictly a read-only projection. `ShareMeetingReport` composes an ephemeral text/PDF but does not write back to the SoT or the Fineract server.

Offline behavior: cache-first render always attempts; if the cache is empty and the network is offline, the `error` state surfaces with the "No cached copy on this device" body copy. If the cache is populated but the fresh fetch fails, the `content` state remains rendered with a non-blocking snackbar `LoadFailed` ("Could not load meeting summary. Showing cached data.").

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/meeting-summary/ui.yaml` |
| API contract | `idea-layer/screens/meeting-summary/api.yaml` |
| Data flow | `idea-layer/screens/meeting-summary/data-flow.yaml` |
| Demo data | `idea-layer/screens/meeting-summary/demo-data.yaml` |
| Flow | `idea-layer/screens/meeting-summary/flow.yaml` |
| Tests | `idea-layer/screens/meeting-summary/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/meeting-summary/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/meeting-summary/preview/content.html` |
| Preview HTML (error) | `idea-layer/screens/meeting-summary/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/meeting-summary/prompts/{loading,content,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/meeting-summary/stitch/` (empty until STITCH_API_KEY available) |
| Feature-group mockup | `idea-layer/mockups/meeting-lifecycle/MOCKUP.md` (Screen: Summary section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (3/3 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The empty state described in `demo-data.yaml`'s alternate hint ("no members present" edge) is NOT declared in the ui.yaml `states:` block; the closest surface is `error` when Fineract returns 404 for a nonexistent meeting record. Adding an explicit `empty` state would require a ui.yaml amendment routed through `/idea-feature-enrich`.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features meeting-summary
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml` components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
