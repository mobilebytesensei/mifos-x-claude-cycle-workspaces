# Personal Savings — Mockup Specification

**Feature**: personal-savings | **Route**: `/savings` | **Type**: list (tabbed detail)
**Feature group**: end-user-dashboard | **Flow**: end-user-dashboard-flow
**Generated from**: `screens/personal-savings/ui.yaml`, `screens/personal-savings/demo-data.yaml`, `screens/personal-savings/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature personal-savings`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts + running balances
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, balance-hero card fill, progress indicator, selected chip, error CTA, deposit-transaction accent
**Primary-pressed**: `#1B5E20` (`--primary-900`) — pressed state on primary surfaces
**Primary-container**: `#C8E6C9` (`--primary-100`) — progress-track fill, unselected tab-chip surface
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled-fund / share-out contexts (not surfaced on this screen)
**Danger**: `#C62828` (`--danger`) — withdrawal-transaction amount + icon tint
**Info**: `#1565C0` (`--info`) — reserved for system notices
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer skeleton, transaction icon container)
**On-primary text/opacity**: white body on primary green · balance label at 0.8 opacity · account-number line at 0.7 opacity
**Corner radius**: `lg` 24dp balance-hero + contribution-progress + empty-individual promo · `md` 12dp shimmer rows + transaction icon container · `full` 9999 for chip pills and progress bar cap
**Elevation**: 0dp balance-hero (fills primary — flat by design) · 2dp contribution-progress card · 0dp top bar
**Min touch target**: 48dp transaction list rows · 48dp tab chips · 48dp Retry CTA

---

## Screen: My Savings

### Entry
- From **personal-dashboard** ("Savings" card / summary tap); nav-params `clientId: Long`, `groupLinkedSavingsId: Long`, `individualSavingsId: Long?`
- Deep-link fallback: opens on GROUP_LINKED tab; individual tab is hidden until `individualSavingsId != null`
- Back navigation (`arrow_left_24_regular`) pops the route and returns to `personal-dashboard`

### Layout (state: `content`, tab: `GROUP_LINKED`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  My Savings              [#2E7D32]  │  top_bar — primary green, onPrimary text
├─────────────────────────────────────────┤
│    ( Group-linked* )  ( Individual )    │  savings_tab_row — chip-group, single-select
│                                          │  selected = primary fill / onPrimary text
│                                          │  unselected = primaryContainer / onPrimaryContainer
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Group-Linked Savings              │   │  balance_hero_card · primary fill
│  │                                    │   │  corner_radius lg, padding 24dp,
│  │ KES 3,500                          │   │  margin_horizontal 16dp, elevation 0dp
│  │                                    │   │  balance_label · labelLarge, onPrimary 0.8
│  │ Acc: 2001                          │   │  balance_amount · displaySmall bold onPrimary
│  └──────────────────────────────────┘   │  account_number_text · labelMedium onPrimary 0.7
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [✓] Contribution Progress         │   │  contribution_progress_card (visible_when GROUP_LINKED)
│  │                                    │   │  surface fill, corner_radius lg, elevation 2dp,
│  │ 14 / 16 meetings                   │   │  padding 16dp, margin_horizontal 16dp, mb 12dp
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  ← 8dp bar        │   │  meetings_progress_bar · primary indicator
│  │                                    │   │  primaryContainer track, full-round, height 8dp
│  │ This cycle: KES 3,500              │   │  contribution_range_text · bodySmall onSurfaceVariant
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  Transaction History                     │  transactions_header · titleMedium semibold onSurface
├─────────────────────────────────────────┤
│  (↗) Deposit             +KES 500       │  transaction_list_item · 48dp min-touch, divider on
│      2026-05-06          Balance: 3,500 │  leading icon-container 40dp circle, surfaceVariant
├─────────────────────────────────────────┤    · deposit uses arrow_trending_up_24_filled,
│  (↗) Deposit             +KES 500       │      tint primary
│      2026-04-29          Balance: 3,000 │    · withdrawal uses arrow_trending_down_24_filled,
├─────────────────────────────────────────┤      tint error (#C62828) — none in the seed data
│  (↗) Interest Posting    +KES 12.50     │  headline · bodyLarge onSurface (txn description)
│      2026-04-30          Balance: 2,512.50 │  supporting · bodySmall onSurfaceVariant (date)
├─────────────────────────────────────────┤    trailing column:
│  (↗) Deposit             +KES 500       │      txn_amount · bodyLarge semibold, colored by kind
│      2026-04-22          Balance: 2,500 │      running_balance · labelSmall outline
├─────────────────────────────────────────┤
│  (↗) Deposit             +KES 500       │
│      2026-04-08          Balance: 2,000 │
├─────────────────────────────────────────┤
│  (↗) Deposit             +KES 500       │
│      2026-03-25          Balance: 1,500 │
├─────────────────────────────────────────┤
│  (↗) Deposit             +KES 500       │
│      2026-03-11          Balance: 1,000 │
├─────────────────────────────────────────┤
│  (↗) Deposit             +KES 500       │  page fits demo seed (8 rows); scroll extends
│      2026-02-25          Balance: 500   │  via paginated get_group_linked_transactions
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

**Session state** (clientId 101, member role, Mwangaza Women's Group, KES):

| Field | Value |
|-------|-------|
| selectedTab | `GROUP_LINKED` (initial) |
| groupLinkedSavingsId | 2001 |
| individualSavingsId | 2050 |
| groupLinkedBalance | KES 3,500.00 |
| individualBalance | KES 800.00 |
| contributionTarget | KES 500.00 (per meeting) |
| meetingsAttended / totalMeetings | 14 / 16 (87.5% cycle progress) |
| isLoading / isRefreshing | false / false |
| error | null |

**Group-linked transactions** (8 rows — 6 weekly deposits + 1 interest posting + 1 seed deposit):

| id   | Kind             | Date        | Amount     | Running Balance |
|------|------------------|-------------|------------|-----------------|
| 4001 | Deposit          | 2026-05-06  | +KES 500   | KES 3,500.00    |
| 4002 | Deposit          | 2026-04-29  | +KES 500   | KES 3,000.00    |
| 4003 | Interest Posting | 2026-04-30  | +KES 12.50 | KES 2,512.50    |
| 4004 | Deposit          | 2026-04-22  | +KES 500   | KES 2,500.00    |
| 4005 | Deposit          | 2026-04-08  | +KES 500   | KES 2,000.00    |
| 4006 | Deposit          | 2026-03-25  | +KES 500   | KES 1,500.00    |
| 4007 | Deposit          | 2026-03-11  | +KES 500   | KES 1,000.00    |
| 4008 | Deposit          | 2026-02-25  | +KES 500   | KES 500.00      |

**Individual transactions** (3 rows — voluntary savings, revealed on tab switch):

| id   | Kind    | Date       | Amount    | Running Balance |
|------|---------|------------|-----------|-----------------|
| 5001 | Deposit | 2026-04-15 | +KES 400  | KES 800.00      |
| 5002 | Deposit | 2026-03-01 | +KES 300  | KES 400.00      |
| 5003 | Deposit | 2026-02-10 | +KES 100  | KES 100.00      |

- **Currency**: KES (Kenyan Shilling, `displaySymbol: "KES"`). Roboto Mono / SF Mono renders every amount and running balance for column alignment.
- **Transaction shape**: `id`, `transactionType.{value,code,description}`, `date: [YYYY, M, D]`, `amount: Double`, `runningBalance: Double`, `currency`.
- **Progress**: 14/16 = 87.5% of the current 16-meeting cycle — primaryContainer track fully painted primary green up to that fraction (~14 of the 16 tick zones on the bar).
- **Empty individual promo**: only surfaces when the user taps the Individual chip AND the seeded `individualSavingsId` is null (not in the default demo, but wired via `visible_when` — see states below).

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton while `SavingsRepository.getSavingsTransactions()` fires a parallel fetch of the group-linked and (if present) individual accounts through Store5.

```
┌ [‹] My Savings ────────────────────────┐  top_bar visible with title
│    ( Group-linked* )  ( Individual )    │  savings_tab_row skeleton — chips are inert
├─────────────────────────────────────────┤
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← 56dp, md      │  shimmer_loading · count 6, height 56dp,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  │  corner_radius md (12dp),
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  │  margin_horizontal 16dp,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  │  surfaceVariant (#F5F5F5) fill,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  │  1.4s ease-in-out shimmer sweep
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  │
└─────────────────────────────────────────┘
```

- Six 56dp rows mirror the transaction-list rhythm (5–6 rows visible above the fold on a Pixel-class device).
- Respects `prefers-reduced-motion: reduce` (animation disabled, static gray rows retained).
- Top bar retains "My Savings" title. The tab chips render but are non-interactive (`pointer-events: none`) until `isLoading == false`.
- Balance-hero card and contribution-progress card are omitted during load — the skeleton stands in for both.

### `content` (see layout above)
Data streamed from Store5 (SQLDelight source-of-truth + Fineract `/self/savingsaccounts/{savingsId}/transactions` fetcher, 300s stale-while-revalidate). Tab-switch triggers a client-side state transition; individual transactions are lazy-loaded on first switch to the INDIVIDUAL tab. Cache rows serve immediately when `NetworkMonitor.isOffline == true`.

Two tab-scoped content variants share this layout:

- **Group-linked** (default): balance-hero label "Group-Linked Savings", `groupLinkedBalance`, `Acc: {groupLinkedSavingsId}` (2001), contribution-progress card visible, transactions from `groupLinkedTransactions` (8 rows).
- **Individual**: label swaps to "Individual Savings", `individualBalance`, `Acc: {individualSavingsId}` (2050), contribution-progress card hidden (`visible_when: selectedTab == GROUP_LINKED`), transactions from `individualTransactions` (3 rows).

**Empty individual sub-state** (`selectedTab == INDIVIDUAL && individualSavingsId == null`):

```
┌ [‹] My Savings ────────────────────────┐
│    ( Group-linked )  ( Individual* )    │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │              🐷                   │   │  empty_individual_promo — secondaryContainer bg,
│  │                                    │   │  corner_radius lg, padding 24dp,
│  │      No individual savings yet     │   │  margin_horizontal 16dp
│  │                                    │   │  icon piggy_bank_24_filled
│  │  Speak to your group treasurer     │   │  title · titleLarge onSecondaryContainer
│  │  to open an individual savings     │   │  body · bodyMedium onSecondaryContainer
│  │  account.                          │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### `error`
Fineract API failed AND SQLDelight cache is empty (or offline with no prior sync) — retry surface. When cache HAS rows, the toast fallback keeps the content visible per `error_network`.

```
┌ [‹] My Savings ────────────────────────┐
│    ( Group-linked* )  ( Individual )    │  tabs remain interactive (state is per-account)
├─────────────────────────────────────────┤
│                                          │
│                                          │
│               (📶⃠)                       │  error_state · wifi_off_24_filled icon,
│                                          │  onSurfaceVariant tint
│      Could not load savings              │  title · titleLarge onSurface
│                                          │
│    Check your internet connection        │  body · bodyMedium onSurfaceVariant
│    and try again.                        │
│                                          │
│  ┌───────── Try Again ─────────────┐    │  cta_label · primary #2E7D32, 48dp,
│  └────────────────────────────────┘    │  full-round corner
│                                          │  → OnRetry action_contract effect: call_api
└─────────────────────────────────────────┘  (gated by cmp-network-monitor)
```

Error types (from `SavingsError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data." (falls back to snackbar when cache non-empty)
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Unauthorized` — retry:false, `error_session_expired` "Session expired. Please log in again." → redirect to `login`

---

## Interaction Patterns

1. **Tab tap** → `OnTabSelected(tab)` (effect: `transform_state`) → sets `selectedTab` in `PersonalSavingsState` and re-binds balance / progress / transaction list to the tab-scoped fields. Pure ViewModel transition — no network unless the individual tab has never loaded, in which case Store5 lazily fetches `get_individual_transactions`.
2. **Back tap** → `NavigateBack` (effect: `navigate`) → NavController pops back to `personal-dashboard`; savings view state is transient and discarded (no persistence needed).
3. **Pull to refresh** → `OnRefresh` (flow: `reload_both_accounts` with `invalidate_cache: true`) → Store5 `fresh=true` re-fires both `get_group_linked_transactions` and `get_individual_transactions` (when applicable), sets `isRefreshing = true` while in flight.
4. **Retry tap (error state)** → `OnRetry` (effect: `call_api`, external: Store5 + ktor, internal: `cmp-network-monitor`) → re-hits Fineract for the currently active tab with cache bypass; offline tap gracefully falls back to the last cached SQLDelight rows without erroring.
5. **Transaction list row tap** — non-navigating in this pass (no on_click declared on `transaction_list_item`); tap emits standard MD3 ripple for visual feedback only. Future receipts / voucher deep-link is a separate feature.

---

## Accessibility

- Tab chips carry role `tab`; selected chip communicates state via ARIA `aria-selected="true"` and reads e.g. "Group-linked, tab 1 of 2, selected".
- Balance-hero card is a semantic group ("Group-Linked Savings, KES 3,500, account 2001").
- Contribution progress bar exposes `role="progressbar"` with `aria-valuemin=0`, `aria-valuemax=totalMeetings`, `aria-valuenow=meetingsAttended`, and reads "14 of 16 meetings, 87 percent".
- Transaction rows announce as a single semantic action ("Deposit, 6 May 2026, plus 500 Kenyan shillings, balance 3,500").
- Withdrawal amounts are red + prefixed with `-` — never color-only; deposit amounts are green + prefixed with `+`.
- Min touch target 48dp on rows, tabs, and the Retry CTA (WCAG 2.1 SC 2.5.5).
- Focus ring: 2dp solid `--primary-700` with 2dp offset per DESIGN.md Accessibility section.
- Font stack respects system settings (Roboto / SF Pro system) — text scales up to 200% without layout breakage.
- Locales covered: English (`en`) declared in ui.yaml `i18n`; Swahili / French / Hindi strings inherit the project-wide `_strings/strings.yaml` roll-up on the next `/idea-sync` pass.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Tab chip selection: fill transition 150ms (`--fast`, DESIGN.md motion preset) — cubic-bezier(0.4, 0, 0.2, 1).
- Row ripple: MD3 standard 300ms ease-out on tap (visual only — no navigation yet).
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Snackbar (cached-data fallback): standard MD3 slide-up + auto-dismiss 4s ("No internet connection. Showing cached data.").
- Retry CTA press: MD3 ripple + 150ms ease-out state change; disabled while re-fetch is in flight (`isRefreshing == true`).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `ktor`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, cache-first — Store5 with 300s stale-while-revalidate):
- `groupLinkedTransactions[]` ← `SavingsRepository.getSavingsTransactions(groupLinkedSavingsId, limit=50, offset=0)`
  - Source of truth: SQLDelight `savings_transactions` cache (keyed by savingsId)
  - Fetcher: Fineract `GET /self/savingsaccounts/{savingsId}/transactions?limit=50&offset=…` (gated by `cmp-network-monitor`)
- `individualTransactions[]` ← `SavingsRepository.getSavingsTransactions(individualSavingsId, limit=50, offset=0)`
  - Same shape and cache table, keyed on `individualSavingsId`
  - Fires lazily on first switch to the INDIVIDUAL tab
- `groupLinkedBalance` / `individualBalance` ← derived from the most-recent row's `runningBalance` per tab
- `meetingsAttended` / `totalMeetings` ← session-scoped (populated on entry by `personal-dashboard`, refreshed via `OnRefresh`)
- `SessionManager` — resolves current member's `clientId` + role gating (member role only; treasurer / chairperson use different flows)

Write path: **none**. This screen is strictly read-only. Deposits happen through `meeting-conduct` (per-meeting group contribution) and future receipt flows; withdrawals happen through group-linked-savings share-out / redemption (separate features).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar ("No internet connection. Showing cached data.") — the list itself stays in `content` state. If cache is empty AND offline, the `error` state renders with `wifi_off_24_filled` and the `error_network` copy.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/personal-savings/ui.yaml` |
| API contract | `idea-layer/screens/personal-savings/api.yaml` |
| Data flow | `idea-layer/screens/personal-savings/data-flow.yaml` |
| Demo data | `idea-layer/screens/personal-savings/demo-data.yaml` |
| Flow | `idea-layer/screens/personal-savings/flow.yaml` |
| Tests | `idea-layer/screens/personal-savings/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/personal-savings/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/personal-savings/preview/content.html` |
| Preview HTML (error) | `idea-layer/screens/personal-savings/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/personal-savings/prompts/{loading,content,error}.md` |
| Stitch mockup (legacy 2026-05-09) | `idea-layer/mockups/personal-savings/stitch/01-personal-savings-content/{code.html,screen.png}` |
| Feature-group mockup | `idea-layer/mockups/end-user-dashboard/MOCKUP.md` (Screen — Personal Savings section) |
| Design system SoT | `idea-layer/design-system/DESIGN.md` (CommonPurse-v3) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (3/3 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + api.yaml + flow.yaml + DESIGN.md per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy stitch artifact under `stitch/01-personal-savings-content/` (Stitch screen `87bb047540864f5e927ec9cd4b27ba28`, generated 2026-05-09) is stale relative to the current `screen_state` split (`Loading | Content | Error` — 3 states) and the 87.5% cycle-progress balance-hero surfacing; it will be regenerated on the next Stitch-enabled `/idea-feature-stitch --features personal-savings` pass.
- The **Individual** tab is data-driven visibility: `visible_when: individualSavingsId != null`. When the current member has no individual account, the tab renders but tapping it surfaces the `empty_individual_promo` card (piggy_bank_24_filled, secondaryContainer background) with a treasurer-hint CTA — no error, no dead click.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features personal-savings
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml` `components` or `states` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
