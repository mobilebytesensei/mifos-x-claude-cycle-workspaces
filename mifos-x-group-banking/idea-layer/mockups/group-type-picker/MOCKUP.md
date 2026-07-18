# Group Type Picker — Mockup Specification
**Feature**: group-type-picker | **Screen**: group-type-picker-screen | **Route**: `/groups/create/type`

Step 1a of the group-create wizard. Presents the 9 seeded `GroupTypeConfig` rows (VSLA, ROSCA, ASCA, SILC, SHG, SACCO / Credit Union, CBO / Village Bank, Burial / Welfare Society, JLG) as tappable Material 3 cards. Tapping a card resolves the `typeSlug` to its full `GroupTypeConfig` and navigates to `group-create`, which reads `savingsMechanism`, `contributionMode`, `lendingEnabled`, `hasSocialFund`, `hasBankLinkage`, and `welfareOnlyMode` to conditionally show / hide downstream wizard sections. Covers **FR-022**. Entry points: `group-list` (FAB tap) and `group-dashboard` (change-type tap).

---

## Design Language

**System**: Material Design 3 (MD3) — comfortable density
**Font**: Noto Sans (multilingual rural users)
**Primary**: #2E7D32 (VSLA green) — TopAppBar bg, card leading icons, chip container
**On-primary**: #FFFFFF — TopAppBar title, back icon
**Surface**: #FFFFFF — card background
**On-surface**: #1B1B1B — card title text (`titleMedium`)
**On-surface-variant**: #49454F — card tagline (`bodySmall`)
**Primary container**: #C8E6C9 — feature chip background
**On-primary container**: #1B5E20 — feature chip text
**Error**: #D32F2F — error banner text + icon
**Error container**: #FDECEA — error banner bg
**Min touch target**: 48dp (full card is tappable; ≥88dp tall so easily satisfied)
**Corner radius**: 12dp (cards), 8dp (chips), 4dp (top-bar)
**Card elevation**: 1dp (rest) → 3dp (pressed ripple)
**Card padding**: 16dp all sides; 12dp vertical rhythm between siblings

---

## Screen: Group Type Picker (`/groups/create/type`)

### Layout — Content state (9-card scrollable list)
```
┌─────────────────────────────────────────┐
│ [←] Choose Group Type         [#2E7D32] │  TopAppBar — primary bg, white text + back
├─────────────────────────────────────────┤ ▲
│ ┌─────────────────────────────────────┐ │ │
│ │ [$] VSLA                            │ │ │  Card 1 — savings icon (32dp, primary)
│ │     Save in shares each meeting;    │ │ │  title = titleMedium
│ │     borrow up to 3× your shares;    │ │ │  tagline = bodySmall onSurfaceVariant
│ │     share-out at year end           │ │ │
│ │     [Share-based saving]            │ │ │  chip row — primaryContainer bg
│ │     [Internal lending]              │ │ │  chips wrap; 8dp gap
│ │     [Annual share-out]              │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [↻] ROSCA                           │ │ │  Card 2 — rotate_right icon
│ │     Fixed pot rotates — one member  │ │ │
│ │     takes all each period (susu,    │ │ │
│ │     tanda, hui, committee)          │ │ │
│ │     [Rotating payout]               │ │ │  2 feature chips only
│ │     [Fixed contribution]            │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [🏛] ASCA                           │ │ │  Card 3 — account_balance icon
│ │     Fixed contributions build a     │ │ │
│ │     fund; members borrow and pay    │ │ │
│ │     interest; bookkeeping required  │ │ │
│ │     [Accumulating fund]             │ │ │
│ │     [Internal lending]              │ │ │
│ │     [Fixed contributions]           │ │ │
│ └─────────────────────────────────────┘ │ │  Scrollable
│ ┌─────────────────────────────────────┐ │ │
│ │ [👥] SILC                           │ │ │  Card 4 — people_alt icon
│ │     CRS-promoted VSLA variant with  │ │ │
│ │     share-based saving and internal │ │ │
│ │     lending                         │ │ │
│ │     [Share-based saving]            │ │ │
│ │     [CRS-promoted]                  │ │ │
│ │     [Internal lending]              │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [👥] SHG                            │ │ │  Card 5 — groups icon
│ │     Save regularly; borrow from     │ │ │
│ │     internal fund; qualify for bank │ │ │
│ │     linkage loan (1:1–4:1)          │ │ │
│ │     [Bank linkage]                  │ │ │
│ │     [Internal fund]                 │ │ │
│ │     [India-origin model]            │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [🏢] SACCO / Credit Union           │ │ │  Card 6 — corporate_fare icon
│ │     Registered co-operative; share  │ │ │
│ │     capital; elected board;         │ │ │
│ │     regulated by authority          │ │ │
│ │     [Share capital]                 │ │ │
│ │     [Formal governance]             │ │ │
│ │     [Regulated]                     │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [🏙] CBO / Village Bank             │ │ │  Card 7 — location_city icon
│ │     External MFI loan on-lent to    │ │ │
│ │     members alongside internal      │ │ │
│ │     savings (FINCA model)           │ │ │
│ │     [MFI on-lending]                │ │ │
│ │     [Internal savings]              │ │ │
│ │     [FINCA model]                   │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [♥] Burial / Welfare Society        │ │ │  Card 8 — favorite icon
│ │     Welfare fund IS the purpose;    │ │ │
│ │     member benefits on life events; │ │ │
│ │     can nest inside other groups    │ │ │
│ │     [Welfare-only mode]             │ │ │  2 chips only
│ │     [Nestable]                      │ │ │
│ └─────────────────────────────────────┘ │ │
│ ┌─────────────────────────────────────┐ │ │
│ │ [🤝] JLG                            │ │ │  Card 9 — handshake icon
│ │     4–10 members take an external   │ │ │
│ │     MFI loan jointly with mutual    │ │ │
│ │     guarantee; no internal savings  │ │ │
│ │     pot                             │ │ │
│ │     [Joint guarantee]               │ │ │
│ │     [External MFI loan]             │ │ │
│ │     [No savings pool]               │ │ │
│ └─────────────────────────────────────┘ │ ▼
└─────────────────────────────────────────┘
```

### States

- **Loading** (`initial_state`): full-screen centered `CircularProgressIndicator` — color=primary, size 48dp, accessibility label "Loading group types…". TopAppBar visible; no cards rendered. Shown while COMP-DT-003 (`GET /companion/datatables/group_type_config/0`) fetches the 9 seeded rows on `on_mount`.
- **Content**: TopAppBar + vertically scrolling column of 9 cards in canonical registry order (VSLA → ROSCA → ASCA → SILC → SHG → SACCO → CBO → Burial → JLG). Each card is a single tappable surface (`onClick = OnTypeCardTap(typeSlug)`) with `Modifier.semantics { onClick(label = "Select {type_name}") }`. Ripple = primary at 12% alpha.
- **Error**: TopAppBar + centered error banner — `error_outline` icon (32dp, error color) above `{error.message}` (`bodyMedium`, `onSurface`) above a filled tonal "Retry" button (48dp, primary container). Cards are NOT rendered. On Retry tap → transitions to Loading, re-dispatches COMP-DT-003; on success upserts rows into `group_type_config_cache` SQLDelight table and emits Content. Error message copy is keyed by `GroupTypePickerError.type` (Network / Server / Auth) → `error_network` / `error_server` / `error_auth`. Auth error additionally redirects to login route.

### Card Component Contract (all 9 cards share this shape)

| Slot | Value | Style |
|---|---|---|
| Leading icon (32dp, primary tint) | Per-type Material icon (see table below) | Vertically centered against title row |
| Title (`titleMedium`) | Type display name (see i18n table) | `onSurface`, 20sp/28sp line-height |
| Tagline (`bodySmall`) | One-line description of the model | `onSurfaceVariant`, wraps to 2–3 lines on narrow screens |
| Feature chip row (`FlowRow`, 8dp gap) | 2 or 3 distinguishing feature chips | `primaryContainer` bg, `onPrimaryContainer` text, 8dp corner radius, 12dp horizontal padding, 6dp vertical padding |
| Whole-card `on_click` | `OnTypeCardTap { typeSlug }` → `navigate → group-create` | Ripple over entire card surface |

### Group-type mapping (icon + savings/contribution axes → downstream wizard branches)

| # | typeSlug | Icon (Material) | savingsMechanism | contributionMode | lendingEnabled | hasSocialFund | hasBankLinkage | Downstream wizard sections revealed by group-create |
|---|---|---|---|---|---|---|---|---|
| 1 | `VSLA` | `savings` | ACCUMULATING | SHARE_BASED_VARIABLE | ✓ | ✓ | — | share-based contribution, social-fund setup, annual share-out |
| 2 | `ROSCA` | `rotate_right` | ROTATING_PAYOUT | FIXED | — | — | — | payout-order roster; hides internal-lending + social-fund |
| 3 | `ASCA` | `account_balance` | ACCUMULATING | FIXED | ✓ | — | — | fixed-contribution entry, internal-loan config; hides payout-order + social-fund |
| 4 | `SILC` | `people_alt` | ACCUMULATING | SHARE_BASED_VARIABLE | ✓ | ✓ | — | identical to VSLA + CRS programme-affiliation field |
| 5 | `SHG` | `groups` | ACCUMULATING | FIXED | ✓ | — | ✓ | bank-linkage section (linking bank, credit grade, leverage 1:1–4:1) alongside standard fixed-contribution + internal-loan |
| 6 | `SACCO` | `corporate_fare` | ACCUMULATING | FIXED | ✓ | — | — (formally registered) | formal-governance section: registration number, regulator, elected officers, share-capital ledger; officer-election workflow required |
| 7 | `CBO_VILLAGE_BANK` | `location_city` | ACCUMULATING | FIXED | ✓ | — | ✓ | MFI on-lending section (partner, external loan amount, margin), internal savings, 4-month cycle default |
| 8 | `BURIAL_WELFARE` | `favorite` | ACCUMULATING | FIXED | — | ✓ (welfareOnlyMode) | — | welfare-only mode: benefit-trigger config (event types, payout amounts), optional nested-group selector; hides internal-lending |
| 9 | `JLG` | `handshake` | NONE | MINIMAL | — | — | ✓ | MFI-loan details section + joint-liability agreement workflow; suppresses corpus / share-out / social-fund steps |

### Interaction Rules

- Whole card is the click target (title, tagline, chips, and icon all propagate `on_click` to the parent card). Consistent across all 9 cards.
- On tap:
  1. VM emits `OnTypeCardTap { typeSlug }` action.
  2. Reducer resolves `typeSlug` → `GroupTypeConfig` from `typeConfigs` state (`reads_from: [typeConfigs]`; no writes).
  3. VM emits `NavigateToGroupCreate { typeConfig }` event.
  4. Screen's `LaunchedEffect` on the event calls `onNavigateToGroupCreate(typeConfig)` — a Compose callback that Route wires to `NavController.navigate("group-create?config=...")`.
- On system back gesture OR top-bar back icon tap: emit `OnBack` → `NavigateBack` event → pop route. Any partial wizard state is discarded (no persistence).
- On Retry tap (Error state only): emit `OnRetry` → re-run `on_mount` fetch; screen transitions Loading → Content or Loading → Error.

### Accessibility

- Every card carries `accessibility_label = "{strings.type_{slug}_name}"` (e.g. `"VSLA"`, `"Burial / Welfare Society"`). Icon `accessibility_label = ""` (decorative — the card label already announces the type).
- Feature chips are non-focusable summary chips (`Modifier.clearAndSetSemantics { }`) — TalkBack announces them as part of the card's aggregated content description; they are not individually tappable.
- Loading state announces `"Loading group types…"` via `accessibility_label`.
- Error banner announces its message first, then the "Retry" CTA.
- Contrast: primary green #2E7D32 on white ≥ 4.5:1 (WCAG AA). Feature chip #1B5E20 on #C8E6C9 ≥ 4.5:1.

### Analytics

- `screen_view: group_type_picker_viewed` — on first Content composition.
- `group_type_selected` — trigger `type card tap`, params `{ type_slug: String }` (one of the 9 canonical slugs above).
- `group_type_picker_dismissed` — trigger `back tap` (either system back or top-bar back icon).

### Copy (English, from `ui.yaml#i18n.en`)

| Key | Copy |
|---|---|
| `screen_title` | "Choose Group Type" |
| `loading_label` | "Loading group types…" |
| `btn_retry` | "Retry" |
| `error_network` | "Could not load group types. Check your connection and retry." |
| `error_server` | "Server error loading group types. Please retry." |
| `error_auth` | "Session expired. Please log in again." |
| `type_vsla_name` / `_tagline` | "VSLA" / "Save in shares each meeting; borrow up to 3× your shares; share-out at year end" |
| `type_rosca_name` / `_tagline` | "ROSCA" / "Fixed pot rotates — one member takes all each period (susu, tanda, hui, committee)" |
| `type_asca_name` / `_tagline` | "ASCA" / "Fixed contributions build a fund; members borrow and pay interest; bookkeeping required" |
| `type_silc_name` / `_tagline` | "SILC" / "CRS-promoted VSLA variant with share-based saving and internal lending" |
| `type_shg_name` / `_tagline` | "SHG" / "Save regularly; borrow from internal fund; qualify for bank linkage loan (1:1–4:1)" |
| `type_sacco_name` / `_tagline` | "SACCO / Credit Union" / "Registered co-operative; share capital; elected board; regulated by authority" |
| `type_cbo_name` / `_tagline` | "CBO / Village Bank" / "External MFI loan on-lent to members alongside internal savings (FINCA model)" |
| `type_burial_name` / `_tagline` | "Burial / Welfare Society" / "Welfare fund IS the purpose; member benefits on life events; can nest inside other groups" |
| `type_jlg_name` / `_tagline` | "JLG" / "4–10 members take an external MFI loan jointly with mutual guarantee; no internal savings pot" |

Per-card feature chip labels (`type_{slug}_feature_1..3`) mirror the "Feature chip row" values shown in each card in the layout diagram above.

---

## Data Contract

- **API**: `COMP-DT-003 GET /companion/datatables/group_type_config/0` — returns array of 9 `GroupTypeConfig` rows. `entityId = 0` because this is a catalogue query, not per-instance.
- **Cache**: SQLDelight table `group_type_config_cache` (columns mirror `GroupTypeConfig` DTO). Read-through: on `on_mount`, ViewModel queries cache first; if fresh (< 24h) emits Content immediately, else fires COMP-DT-003 and upserts on success.
- **Nav argument**: whole `GroupTypeConfig` passed to `group-create` (typically JSON-serialised through the nav-args bundle) so downstream steps have the two axes + boolean flags without a second fetch.
- **No local mutation**: `GroupTypeConfig` rows are read-only catalogue seeds; nothing on this screen writes back to server or cache except the fetch upsert path.

---

## Companion Screens / Cross-references

- Referenced by `group-list` (FAB → this screen) and `group-dashboard` ("Change group type" → this screen).
- Forwards to `group-create` (`nav_params: { config: GroupTypeConfig }`) which is where the config's fields drive the rest of the wizard.
- Upstream design authority: `idea-layer/screens/group-type-picker/ui.yaml` (schema v4.0, approved 2026-07-17). Stitch mockup PNGs / HTMLs live in this directory under `stitch/` (loading / content / error).
