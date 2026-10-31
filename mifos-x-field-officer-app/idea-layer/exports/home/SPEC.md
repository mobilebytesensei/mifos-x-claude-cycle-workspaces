<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: home
generated_from_feature_version: "1.0"
sources:
  - screens/home/docs.yaml
  - screens/home/ui.yaml
  - screens/home/api.yaml
  - screens/home/flow.yaml
  - screens/home/data-flow.yaml
  - screens/home/tests.yaml
  - design-system/design-tokens.yaml
  - design-system/app-shell.yaml
  - REQUIREMENTS.md (FR-DASH-01..07, NFR-PERM-01)
design_tier_consumed: stitch          # RULE-UI-SOURCE-001 US9: all 5 states — mockups/home/stitch/0{1..5}-home-*
-->

# SPEC — Home

The field officer's daily work surface and the Home tab. It answers "what needs me today": the day's
collections, the work queue, meetings due today, a portfolio summary, and quick actions. Every card and
action is driven by the signed-in user's Fineract permissions — **absent, never disabled**, when the
user lacks the right.

| | |
|---|---|
| Feature id | `home` |
| Module | `feature/home` (flat; pinned) |
| Route | `HomeRoute` (no params) — Home tab start destination |
| Entry point | yes — first tab after sign-in |
| Bottom nav | yes — Home · Clients · Centers · Groups (`app-shell.yaml`) |
| Business logic | `composite` — `read_dashboard`, `NETWORK_WITH_CACHE` |
| Version | 1.0 |

## Decisions (docs.yaml)

| id | decision |
|---|---|
| portfolio-scope | "My portfolio" when the user has a staff link (`GET /users/{id}.staff`); office-wide otherwise |
| own-loan-queues | approval/disbursal queues count only the officer's own loans (`loanOfficerId == staffId`, else `submittedByUsername == username`) |
| dashboard-is-home | the dashboard IS the Home tab; search stays on the top-bar magnifier |
| no-account-creates-on-home | quick actions: client · group · centre · collection sheet · run reports · search only — loan/savings/share/collateral start from the client profile |

## Permission model

`has(code) = code ∈ permissions || ALL_FUNCTIONS || (READ_* && ALL_FUNCTIONS_READ) || (*_CHECKER && CHECKER_SUPER_USER) || (READ_<report> && REPORTING_SUPER_USER)`.
Source: `POST /authentication → permissions[]`, persisted with the session. A card the user cannot read is
never subscribed and never rendered.

## Screens

| Screen | ViewModel | States (ui.yaml) |
|---|---|---|
| `HomeDashboardScreen` (Home tab body, via `BackboneRegistry.homeBody`) | `HomeViewModel` | loading · content · partial_failure · error · offline |
| `LoanQueueScreen` (`LoanQueueRoute(status)`) | `LoanQueueViewModel` | loading · content · empty · error |

## Components (ui.yaml → testTag)

| Component | testTag | Permission | Contents |
|---|---|---|---|
| header | `home_header` | — | greeting (morning/afternoon/evening) + office · business date · instance; scope chip `home_scope_chip` when staff-linked |
| card_skeletons | `home_skeleton` | — | per-card shimmer (loading) |
| collections_card | `home_collections` | READ_COLLECTIONSHEET | clients due · amount due (per currency); "Open collection sheet" `home_open_collection_sheet` |
| work_queue_card | `home_work_queue` | per row | checker `home_queue_checker` (*_CHECKER) · approval `home_queue_approval` / disbursal `home_queue_disbursal` (READ_LOAN) · pending clients `home_queue_pending_clients` (READ_CLIENT) · reschedules `home_queue_reschedules` (READ_RESCHEDULELOAN) · drafts `home_queue_drafts` (local, hidden at 0) |
| meetings_card | `home_meetings` / row `home_meeting_row` | READ_CALENDAR + READ_CENTER | centres whose collection meeting falls on the business date |
| portfolio_card | `home_portfolio` | per tile | active clients · active loans · outstanding · overdue · in arrears · PAR · savings · groups · centres — figures, **not tappable** |
| quick_actions | `home_quick_actions` / `home_qa_*` | per action | 6 tiles, 3 per row |
| card_error_retry | `home_card_error` | — | partial_failure: the failed card's body only; retries that card |
| screen_error_retry | `home_screen_error` | — | error/offline: every remote card failed; retries all |
| recent_card | `home_recent` | — | hidden — no recently-opened source exists yet (see Known Gaps) |

## State Model

### HomeViewModel — `BaseViewModel<HomeUiState, Nothing, HomeAction>`

```
HomeUiState(
  header: HomeHeader(name, officeName, businessDate?, instanceName?, ownPortfolio),
  cards: List<HomeCardSlot(id: COLLECTIONS|WORK_QUEUE|MEETINGS|PORTFOLIO, state: ScreenState<HomeCard>)>,
  quickActions: List<QuickAction>,
  draftCount: Int,            // local, never a loading slot
)
HomeAction = Retry(card) | Refresh
```

One `ScreenState` slot per card, each from its own repository stream — one slow or failed source never
blanks the others (FEATURE_LAYER "Dashboard fan-out shape"). Multi-source cards fuse with
`combineScreenStates`; scope-dependent cards use `combineContent`.

### LoanQueueViewModel

`state: StateFlow<ScreenState<List<DashboardLoan>>>` — the same "own" rule as the dashboard count, so the
list always matches the number tapped. Empty → "No loans in this queue".

## API

See `API.md`. Substrate: `kpt.core.data.dashboard.DashboardRepository` (new) over five `@StoreProvider`
stores (`dashboardUser`, `dashboardBusinessDate`, `dashboardLoans`, `dashboardClientCount`,
`dashboardSavings`), plus the existing Checker inbox, Collection sheet, Center, Group, FormDraft and
ServerConfig repositories.

## Navigation (flow.yaml)

| Trigger | Target |
|---|---|
| Open collection sheet / Collection sheet tile | `individualCollectionSheet` |
| Checker inbox tasks | `checkerInbox` |
| Loans awaiting approval / disbursal | `loanAccountList` → `LoanQueueRoute(100 \| 200)` → loan profile |
| Clients pending activation | `clientList` |
| Pending reschedule requests | `loanReschedules` (checker inbox reschedules tab) |
| My unsynced drafts | `syncAndDrafts` |
| Meeting row | `centerDetail` |
| New client / group / centre | `createNewClient` / `createGroup` / `createCenter` |
| Run reports | `runReports` |
| Search | `search` |

## Design (Stitch, consumed per state)

Sections are titled groups of raised surface tiles (`surfaceContainerLowest`, `shapes.medium`, elevation
level 1) with tinted icon badges. Work queue: 2-column grid, count top-right, drafts tile amber
(`tertiaryContainer`). Portfolio: "Total outstanding portfolio" highlight + 2-column figure grid; money
via `MoneyText` (overdue `moneyNegative`, savings `moneyPositive`), PAR in `tertiary`. Quick actions:
3-column grid, circular `primaryContainer` badges. Partial failure: red banner (`moneyNegativeContainer`)
with a Retry button under the card's title. Error/offline: one centred card — "Couldn't load your day" +
Retry, quick actions below.

## Testing

`tests.yaml` — 21 scenarios (15 high · 5 medium · 1 low). Implemented: `HomeViewModelTest` (permission
gating, own-loan scoping, unlinked fallback, per-card failure isolation, quick-action set) and
`HomeDashboardScreenUiTest` (surfaces, nav targets, drafts visibility, per-card retry, all-failed screen
error). Maestro: `maestro/happy_path.yaml`.

## Known Gaps

| Gap | Why | Rendered as |
|---|---|---|
| Collected today / goal / progress hero; Overdue clients tile | `IndividualCollectionSheet` carries `totalDue` only — no collected amount, no overdue count | omitted; clients due + amount due shown |
| Meeting time + On schedule / Upcoming status | centre calendars give the date only | omitted; name + groups count |
| Group meetings | `GroupWithAssociations` twin has no meeting calendar | centres only |
| Recently opened | no recently-opened history source in the app | card hidden (`hidden_when: no recent records`) |
| Work queue "View all" | no declared destination in flow.yaml | omitted — a dead control otherwise |
| Clients pending activation filter | the client list has no status filter | opens the full client list |
| Header date names | app-wide dates are English-only (DateHelper) | "Mon 26 Oct 2026" in English |
| Top-bar status chip / avatar menu | app chrome is template-owned (shell) | avatar initials in the header only |
