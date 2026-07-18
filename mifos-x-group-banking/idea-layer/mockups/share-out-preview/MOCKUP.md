# Share-Out Preview — Mockup Specification

**Feature**: share-out-preview | **Route**: `/groups/{groupId}/share-out/preview` | **Type**: detail
**Feature group**: share-out | **Flow**: share-out-flow
**Generated from**: `screens/share-out-preview/ui.yaml`, `screens/share-out-preview/demo-data.yaml`, `design-system/DESIGN.md`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature share-out-preview`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, Confirm CTA, refresh icon, pool amount emphasis
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled-fund visual metaphor (subtle, in cycle banner accents)
**Success**: `#1B5E20` on `#C8E6C9` — highlight-max row on payout table (top-earning member)
**Warning**: `#F57C00` on `#FFE082` — inline advisory banner (unused on happy path)
**Danger**: `#C62828` on `#FFCDD2` — error state icon + retry emphasis
**Muted**: `#616161` on `#F5F5F5` — labels, secondary metadata, table zebra rows
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, filled inputs)
**Corner radius**: 12dp cards + banners + rotation card · 16dp formula chip · 24dp Confirm button (full-width pill)
**Elevation**: 2dp fund summary + rotation preview cards · 0dp banners (primaryContainer fill)
**Min touch target**: 56dp Confirm button · 48dp refresh action · 44dp table rows

---

## Screen: Share-Out Preview

### Entry
- From **group-dashboard** → "Share Out (cycle-end action)" tile; nav-params `groupId: String`, `typeConfig: GroupTypeConfig`
- Guarded by `entry_points[0].condition: viewerRole in [ORGANIZER, TREASURER, CHAIRPERSON]` — non-privileged members never see the entry point
- Back navigation (top-left arrow or system back) pops the route and returns to `group-dashboard` without mutating any corpus / payout data

### Layout (state: `content_accumulating` — VSLA / ASCA / SHG / SILC)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Share-Out Preview        [↻]       │  TopAppBar — primary #2E7D32, onPrimary
│                                          │  nav_icon: arrow_back → OnBack (NavigateBack)
│                                          │  action: refresh → OnRefresh (call_api, fresh=true)
├─────────────────────────────────────────┤
│  ╭──────────────────────────────────╮   │
│  │  Cycle 1 — Distribution Preview  │   │  cycle_info_banner · primaryContainer
│  │  All calculations are             │   │  corner 12dp, padding 16dp
│  │  preliminary. Confirm to proceed. │   │  onPrimaryContainer text, titleMedium + bodySmall
│  ╰──────────────────────────────────╯   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │  Total Corpus (Fund)             │   │  fund_summary_card · surface, elev 2dp
│  │                    KES 20,000    │   │  corner 12dp, padding 16dp
│  │                                   │   │  labeled-value rows · bodyLarge
│  │  Total Profit (Interest Earned)  │   │
│  │                     KES 4,000    │   │  profit value tinted primary #2E7D32
│  │  ─────────────────────────────    │   │  divider · 8dp margin
│  │  Total Distribution Pool          │   │  titleLarge, primary, bold
│  │                    KES 24,000    │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  [ Pro-rata by savings ]                 │  distribution_formula_chip · tertiaryContainer
│                                          │  corner 16dp, padding 6dp 12dp
│                                          │  label adapts to shareoutFormula token
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │ Member         Savings  Share%  KES ││  member_payout_table · surface, onSurface
│  ├─────────────────────────────────────┤│  headers · labelSmall, --text-secondary
│  │ Amina Wanjiru    6,000   28.3  6,792││  ← highlight_max row (#E8F5E9 fill, #1B5E20)
│  │ Joseph Kamau     4,800   21.7  5,208││  bodyMedium, mono for amounts, right-aligned
│  │ Grace Wanjiku    3,850   20.0  4,800││
│  │ Peter Otieno     3,000   18.3  4,392││
│  │ Mary Akinyi      2,250   11.7  2,808││
│  └─────────────────────────────────────┘│  rows_source: memberPayouts (5 rows)
├─────────────────────────────────────────┤
│                                          │
│  ┌──────────────────────────────────┐   │
│  │   Confirm & Proceed to Execute    │   │  confirm_button · filled, primary #2E7D32
│  └──────────────────────────────────┘   │  corner 24dp, min_touch 56dp, full_width
│                                          │  enabled_when memberPayouts.isNotEmpty()
│                                          │  → on_click OnConfirm → share-out-execute
└─────────────────────────────────────────┘
```

### Layout (state: `content_rotating` — ROSCA / chit)

```
┌─────────────────────────────────────────┐
│ [‹]  Share-Out Preview        [↻]       │  TopAppBar unchanged
├─────────────────────────────────────────┤
│  ╭──────────────────────────────────╮   │
│  │  Cycle 3 — Distribution Preview  │   │  cycle_info_banner
│  │  All calculations are             │   │
│  │  preliminary. Confirm to proceed. │   │
│  ╰──────────────────────────────────╯   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │  Total Corpus (Fund)             │   │  fund_summary_card
│  │                    KES 30,000    │   │
│  │  Total Profit (Interest Earned)  │   │
│  │                        KES 0     │   │  ROSCA carries no interest
│  │  ─────────────────────────────    │   │
│  │  Total Distribution Pool          │   │
│  │                    KES 30,000    │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  [ Fixed rotation order ]                │  distribution_formula_chip
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │  Next Recipient                   │   │  rotation_preview_card · secondaryContainer
│  │  Grace Wairimu                    │   │  corner 12dp, elev 2dp, padding 16dp
│  │                                    │   │  label: labelLarge, onSecondaryContainer
│  │  Payout Amount        KES 30,000  │   │  name: headlineMedium, bold
│  │  ─────────────────────────────    │   │  labeled-value · titleLarge amount
│  │  Your position: 3                 │   │  divider · 8dp margin
│  └──────────────────────────────────┘   │  bodyMedium footer
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │   Confirm & Proceed to Execute    │   │  confirm_button
│  └──────────────────────────────────┘   │  enabled_when poolModel == 'ROTATING_PAYOUT'
└─────────────────────────────────────────┘
```

### Demo Data — Variant A: `content_accumulating` (from `demo-data.yaml`)

Mwangaza Women's Group (Kisumu West Branch, KES, weekly contributions, VSLA / ASCA style):

| Cycle | Pool Model     | Formula          | Corpus | Profit | Pool   |
|-------|----------------|------------------|--------|--------|--------|
| 1     | ACCUMULATING   | PRORATA_SAVINGS  | 20,000 | 4,000  | 24,000 |

| Member (id)          | Savings (KES) | Share % | Payout (KES) |
|----------------------|---------------|---------|--------------|
| Amina Wanjiru (101)  | 6,000         | 28.3    | **6,792**  ← highlight_max |
| Joseph Kamau (102)   | 4,800         | 21.7    | 5,208        |
| Grace Wanjiku (103)  | 3,850         | 20.0    | 4,800        |
| Peter Otieno (104)   | 3,000         | 18.3    | 4,392        |
| Mary Akinyi (105)    | 2,250         | 11.7    | 2,808        |
| **Total**            | **19,900**    | 100.0   | **24,000**   |

- Rounding: `sharePercent` and `payoutAmount` are backend-computed with cent-level residual folded into the top-earning row so the sum matches `totalPool` exactly.
- `sharesHeld` is `null` on this variant (PRORATA_SAVINGS group — the group is FIXED_AMOUNT, savings drive %).

### Demo Data — Variant B: `content_rotating` (from `demo-data.yaml`)

Tumaini ROSCA (Nairobi, KES, monthly contributions, fixed rotation):

| Cycle | Pool Model      | Formula      | Corpus | Profit | Pool   | Next Recipient   | Amount    | Your Slot |
|-------|-----------------|--------------|--------|--------|--------|------------------|-----------|-----------|
| 3     | ROTATING_PAYOUT | FIXED_ORDER  | 30,000 | 0      | 30,000 | Grace Wairimu    | 30,000    | 3         |

- `memberPayouts` is `null` on this variant — the member table is not rendered; the rotation preview card takes its place.
- `totalProfit == 0` is the ROSCA norm (no interest earned; the whole pot rotates to the next recipient).
- `Your position: 3` communicates to the viewer that they are 3rd in the fixed rotation queue this cycle.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `ContentAccumulating`, `ContentRotating`, `Error`) — each renders as a distinct preview surface.

### `loading`
Shimmer skeleton mirroring the detail scaffold — parallel fetch of `ShareOutPreview` from SQLDelight `shareout_preview_cache` + companion `COMP-DIST-001` API.

```
[Share-Out Preview header]                 ← top_bar visible with title
────────────────────────────────────────
[shimmer card ]  ← 80dp × full width, corner 12dp, surfaceVariant
[shimmer card ]
[shimmer card ]   ← shimmer_detail count: 4
[shimmer card ]
```

- Cards: 80dp × full width, corner 12dp, `surfaceVariant` `#F5F5F5` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation replaced by static tint).
- Top bar retains "Share-Out Preview" title; refresh icon inert during load.
- Confirm button not rendered in loading state.

### `content_accumulating` (see Variant A layout above)
Populated from Store5 stream. Table `highlight_max` row (`#E8F5E9` on `#1B5E20`) marks the top-earning member. Formula chip label swaps deterministically between {Pro-rata by shares held, Pro-rata by savings, Equal split} based on `shareoutFormula`. Confirm button enabled iff `memberPayouts.isNotEmpty()`.

### `content_rotating` (see Variant B layout above)
Populated from Store5 stream. `rotation_preview_card` replaces the member table; `Your position: {rotationPosition}` is derived from the viewer's `memberId` in the rotation queue. Formula chip label swaps between {Fixed rotation order, Rotation by lottery, Chit auction} based on `shareoutFormula`. Confirm button enabled iff `poolModel == 'ROTATING_PAYOUT'`.

### `error`
Companion API `get_shareout_preview` failed AND cache is empty — retry surface. When cache HAS a fresh row (≤60s TTL), the toast fallback keeps the previous content visible.

```
┌ Share-Out Preview ──────────────────────┐
│                                          │
│                                          │
│               ☁                          │  error_state · cloud_off icon
│    Could not compute distribution        │  title · titleLarge
│                                          │
│    {error.message}                       │  body · bodyMedium, --text-secondary
│    e.g. "Server error. Please try        │
│    again."                                │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  Re-invokes get_shareout_preview,
│                                          │  clears ShareOutPreviewError,
│                                          │  returns to Loading state
└─────────────────────────────────────────┘
```

Error types (from `ShareOutPreviewError`):
- `Network` — retry:true, `error_network` "No internet. Showing cached data." (renders as snackbar when cache is warm)
- `Server` — retry:true, `error_server` "Server error. Please try again." (renders full error state on cold cache)
- `InsufficientData` — retry:false, `error_insufficient_data` "Insufficient data to compute distribution." (advises the user to complete missing member records first)
- `Auth` — retry:false, `error_auth` "Session expired. Please log in again." → redirect to `login`

---

## Interaction Patterns

1. **Back tap** → `OnBack` (effect: `navigate`) → NavController pops back to `group-dashboard`; no corpus / payout data mutated.
2. **Refresh icon tap** → `OnRefresh` (effect: `call_api`, external: `ktor-client`) → re-fetches the strategy-aware preview from companion COMP-DIST-001, bypassing the 60s SQLDelight cache; replaces `shareout_preview_cache` row on success.
3. **Confirm & Proceed tap** → `OnConfirm` (effect: `navigate`) → NavController push `share-out-execute` with `groupId`, `typeConfig`, `cycleNumber`, `totalPool`, and the pool-model-appropriate payload (`memberPayouts[]` for ACCUMULATING; `nextRecipientName` + `nextRecipientAmount` + `rotationPosition` for ROTATING_PAYOUT). **No API call and no persistence happen here** — execution happens on the next screen after double-confirmation.
4. **Pull to refresh** → `OnRefresh` (same contract as icon tap) → Store5 fresh=true reload; header + banner remain sticky; shimmer replaces card content briefly.
5. **Retry tap (error state)** → `Retry` (effect: `call_api`, external: `ktor-client`) → clears `ShareOutPreviewError`, transitions to `loading`, then re-renders the appropriate content variant.
6. **Formula chip tap** — INERT on this preview screen (informational only; strategy is fixed by `typeConfig` nav-arg and cannot be swapped without leaving to group-settings).

---

## Accessibility

- Confirm CTA exposes a single semantic action ("Confirm and proceed to share-out execution, pool {{totalPool}} Kenyan shillings").
- Highlight-max row uses fill + text-color contrast — never color-only; the payout amount remains readable at 4.5:1 minimum on `#E8F5E9` / `#1B5E20`.
- Formula chip carries `role="status"` with `aria-live="polite"` so screen readers announce the strategy label change on refresh.
- Payout table cells use `Roboto Mono` / `SF Mono` right-aligned for KES amounts — reduces visual scanning fatigue.
- Rotation preview card announces "Next recipient {{name}}, {{amount}} Kenyan shillings, your position {{rotationPosition}}" as a single semantic block.
- Min touch target 56dp on Confirm, 48dp on refresh icon, 44dp on table rows (rows are non-interactive; touch-target requirement is relaxed).
- Locales covered: English, Swahili (`Muhtasari wa Mgawanyo` / `Thibitisha na Endelea`), French (`Aperçu du Partage` / `Confirmer et Procéder`), Hindi (`शेयर-आउट पूर्वावलोकन` / `पुष्टि करें और आगे बढ़ें`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS; table remains legible up to `xxLarge`.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- State swap `content_accumulating` ↔ `content_rotating`: cross-fade 200ms (no slide, no reflow flicker).
- Confirm button press: MD3 elevation change 0dp → 2dp + ripple; button briefly disabled 300ms after tap to prevent double-nav.
- Refresh icon: single 360° rotation over 800ms while `OnRefresh` in flight, then eases back to 0°.
- Pull-to-refresh spinner: MD3 refresh indicator tinted primary `#2E7D32`.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for the cached-data fallback banner when `Network` error surfaces with warm cache).
- Highlight-max row fade-in: 250ms on first render only — subsequent refreshes swap without re-animating.

---

## Data Flow (ui.yaml `business_logic.kind: api-driven detail`)

**External libs**: `Store5`, `SQLDelight`, `ktor-client`, `Fineract COMP-DIST-001`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, 60s cache TTL):
- `ShareOutPreview` ← `ShareOutRepository.getPreview(groupId, typeConfig)` via Store5 stream
  - Source of truth: SQLDelight `shareout_preview_cache` keyed by `(groupId, cycleNumber)`
  - Fetcher: companion `POST /companion/groups/{groupId}/shareout/preview` with `typeConfig` body (COMP-DIST-001) — auth gated by session role check
  - `OnRefresh` triggers `fresh=true` bypass; `Retry` re-triggers the fetcher after error clear
- `poolModel`, `shareoutFormula` derive from `typeConfig` (nav-arg) — never fetched; used to fork the render branch
- `memberPayouts[]` OR (`nextRecipientName`, `nextRecipientAmount`, `rotationPosition`) — mutually exclusive; determined by `poolModel`
- `canProceed` ← derived state: `poolModel == 'ROTATING_PAYOUT' || memberPayouts.isNotEmpty()` — gates Confirm button

Write path: **none** on this screen. `share-out-preview` is strictly a preview surface; `share-out-execute` performs the actual COMP-DIST-001/002 execution after double-confirmation.

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows (if warm ≤60s) still render and `Network` error surfaces as a non-blocking snackbar ("No internet. Showing cached data.") — the summary card and table stay in their content state. Cold cache + offline surfaces the full `error` state.

---

## Strategy Adaptation Matrix

The screen has ONE ui.yaml but THREE effective rendered surfaces driven by `typeConfig.shareout_formula`:

| Formula          | poolModel         | Rendered Body                              | Formula Chip Label             |
|------------------|-------------------|--------------------------------------------|--------------------------------|
| PRORATA_SHARES   | ACCUMULATING      | `member_payout_table` w/ Shares column     | "Pro-rata by shares held"      |
| PRORATA_SAVINGS  | ACCUMULATING      | `member_payout_table` w/ Savings column    | "Pro-rata by savings"          |
| EQUAL            | ACCUMULATING      | `member_payout_table` w/ equal Payout col  | "Equal split"                  |
| FIXED_ORDER      | ROTATING_PAYOUT   | `rotation_preview_card` w/ next recipient  | "Fixed rotation order"         |
| LOTTERY          | ROTATING_PAYOUT   | `rotation_preview_card` (drawn recipient)  | "Rotation by lottery"          |
| AUCTION          | ROTATING_PAYOUT   | `rotation_preview_card` w/ winning bid     | "Chit auction"                 |

- The `member_payout_table` column headers adapt: `"Shares / Savings"` label swaps its underlying binding between `sharesHeld` and `totalSavings` based on formula — the visual column width stays 104dp.
- The `rotation_preview_card` copy is identical across FIXED_ORDER / LOTTERY / AUCTION; only the chip label changes and, for AUCTION, `nextRecipientAmount` reflects the winning bid rather than the full pot.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/share-out-preview/ui.yaml` |
| API contract | `idea-layer/screens/share-out-preview/api.yaml` |
| Data flow | `idea-layer/screens/share-out-preview/data-flow.yaml` |
| Demo data | `idea-layer/screens/share-out-preview/demo-data.yaml` |
| Flow | `idea-layer/screens/share-out-preview/flow.yaml` |
| Tests | `idea-layer/screens/share-out-preview/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/share-out-preview/preview/loading.html` |
| Preview HTML (content_accumulating) | `idea-layer/screens/share-out-preview/preview/content_accumulating.html` |
| Preview HTML (content_rotating) | `idea-layer/screens/share-out-preview/preview/content_rotating.html` |
| Preview HTML (error) | `idea-layer/screens/share-out-preview/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/share-out-preview/prompts/{loading,content_accumulating,content_rotating,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/share-out-preview/stitch/` (empty — external dep pending) |
| Feature-group mockup | `idea-layer/mockups/share-out/MOCKUP.md` (Preview screen section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001 despite `ui.yaml#requires_stitch: true`). This MOCKUP.md is the LLM-driven analog synthesized from ui.yaml + demo-data.yaml + `design-system/DESIGN.md` per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The strategy adaptation logic (ACCUMULATING vs ROTATING_PAYOUT branching) is encoded in `visible:` guards on `member_payout_table` and `rotation_preview_card` — a single ui.yaml serves both surfaces without state-model duplication.
- Confirm CTA does NOT perform the distribution — it navigates to `share-out-execute` where a second confirmation gate + COMP-DIST-001/002 mutation call live. This preview screen is strictly read-only.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features share-out-preview
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml` `components` / `states` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
