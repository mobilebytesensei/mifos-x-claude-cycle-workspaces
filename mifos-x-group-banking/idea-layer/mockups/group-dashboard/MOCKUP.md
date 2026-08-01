# Group Dashboard — Mockup Spec

## Design Language

CommonPurse uses Material Design 3 with a VSLA-inspired brand palette designed for low-literacy rural users in East Africa. All touch targets are minimum 48dp (primary CTAs pushed to 56dp). Typography uses the system stack (Roboto on Android / SF Pro on iOS) at comfortable density with an emphasis on clarity for outdoor viewing. Group Dashboard follows the app's `minimalist-ui` family (variance 3/10, motion 3/10, density 7/10) — grid-aligned, predictable, subtle transitions. Amounts (KES values) render in Roboto Mono / SF Mono for column alignment across corpus stats and activity feed.

**Brand colours (from `design-system/DESIGN.md`)**:
- Primary 700: #2E7D32 (base VSLA-green — app bar, primary CTAs, corpus balance emphasis)
- Primary 900: #1B5E20 (pressed CTA states)
- Primary 500: #43A047 (hover / focus highlight)
- Primary 100: #C8E6C9 (primary-container — group_header_card background)
- Accent 700: #FF8F00 (pooled-fund emphasis)
- Accent 100: #FFE082 (subtle amber accent)
- Success: #2E7D32 (approved / on-track)
- Warning: #F57C00 (validation warnings)
- Danger: #C62828 (error banner, corpus-insufficient border, error state icon)
- Info: #1565C0 (informational hints)
- Secondary 700: #00695C (shareout projection text, share-out CTA border)
- Tertiary 700: #1565C0 (savings-summary total emphasis, ROSCA pool text)
- Bg canvas: #FFFFFF (cards, sheets)
- Bg subtle: #FAFAFA (screen background)
- Bg muted: #F5F5F5 (shimmer placeholder tint)
- Border subtle: #EEEEEE (dividers)
- Border default: #E0E0E0 (outlined field borders, outlined-CTA borders when disabled)
- Text primary: #212121 (body, headline)
- Text secondary: #616161 (metadata, labels, quick-action heading)
- Text disabled: #9E9E9E (disabled state)

**Typography**: Roboto / SF Pro. displaySmall=36sp (corpus balance, rotation position), headlineSmall=24sp (group name), titleLarge=22sp, titleMedium=18sp (card labels, savings total), titleSmall=14sp semibold (Quick Actions heading), bodyLarge=16sp, bodyMedium=14sp, labelLarge=14sp semibold, labelSmall=12sp. Currency values (KES) rendered Roboto Mono / SF Mono for column alignment on corpus stats + activity feed.

**Shapes**: cornerRadius sm=8dp (chips), md=12dp (buttons, banners), lg=16dp (metric cards, quick-actions card, savings-summary card, activity-feed card), full=9999dp (chips, filled CTA).

**Elevation**: TopBar 0dp (flat over primary); group_header_card 0dp (tonal-container, sits flush under top bar); corpus_card & rotation_card 4dp (hero metric surface); quick_actions_section 2dp; savings_summary_card 2dp; activity_feed_section 2dp; shimmer 0dp; error_state 0dp (full-bleed).

---

## Screen-by-Screen

### GroupDashboardScreen (single scrollable dashboard, per-group)

**Layout**: Scaffold with primary-tinted top bar + scrollable Column body. Background: `#FAFAFA`. Content sections are stacked as full-width cards with 16dp horizontal margins + 12dp vertical spacing between cards. The dashboard is **group-type-aware** — the second card swaps between `corpus_card` (ACCUMULATING types: VSLA/SILC/ASCA/SHG/CBO/SACCO/Burial) and `rotation_card` (ROTATING_PAYOUT types: ROSCA and variants), driven by `typeConfig.pool_model`. The quick-actions grid is **role-gated** — ORGANIZER/CHAIRPERSON/TREASURER see the 2×2 management grid (Start Meeting, Members, Loans, Share-Out); MEMBER sees the 2×2 read-only grid (My Savings, My Loans, Meetings, Members). Demo tenant = VSLA (`Mwangaza Women's Group`, ORGANIZER viewer, corpus KES 47,500 across 20 members, cycle 1 of 12 months, weekly meetings) alongside the ROSCA variant (`Jiunge ROSCA Circle`, MEMBER viewer, position #7 of 10, next payout to Amina Hassan at position #4).

**States**:
- `loading` (initial_state) — parallel companion API calls in flight (get_group + get_viewer_role + get_group_corpus + get_group_accounts + get_group_type_config); top_bar rendered without title; shimmer_dashboard shows 4 stacked 120dp-height rounded-16dp surfaceVariant placeholders below it
- `content_accumulating` — VSLA/SILC/ASCA/SHG group; group_header_card + corpus_card + quick_actions_section (management grid for ORGANIZER demo) + savings_summary_card + activity_feed_section; shareout_projection_text visible below the corpus balance; corpus_blocked_banner hidden (isCorpusInsufficient=false)
- `content_rotating` — ROSCA group; group_header_card + rotation_card + quick_actions_section (member grid for MEMBER demo) + savings_summary_card + activity_feed_section; rotation_card replaces corpus_card in slot 2
- `error` — top_bar + error_state (full-bleed centered illustration + Retry CTA); Retry re-fires the parallel API fan-out through `cmp-network-monitor` connectivity check

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| top_bar | TopBar | Background primary (#2E7D32), text onPrimary (#FFFFFF), elevation 0dp, height 56dp. Navigation icon `arrow_back` 24dp onPrimary at start. Title: `{{group.name}}` (e.g. "Mwangaza Women's Group" / "Jiunge ROSCA Circle") — titleLarge (22sp), onPrimary, single-line ellipsis-end. Trailing overflow icon `more_vert` 24dp onPrimary with content_description "More options". Loading state hides title until group resolves. | Tap `arrow_back` → OnBack → NavigateBack (pops to group-list or group-create). Tap `more_vert` → OnMoreOptions → toggles `isMoreMenuExpanded` to reveal the **`group-dashboard-more-menu`** DropdownMenu (Compose-DropdownMenu; local UI state only, no network) — see "Overflow menu" below. |
| group-dashboard-more-menu | DropdownMenu | **NEW (G13).** Anchored to the `more_vert` icon, top-end aligned, surface (#FFFFFF) fill, elevation 3dp, cornerRadius sm (8dp), min_width 200dp; visible when `isMoreMenuExpanded == true` (scrim-free, dismiss-on-outside-tap). Two `DropdownMenuItem` rows, each 48dp min-height with a 24dp leading icon (onSurfaceVariant) + labelLarge (14sp) onSurface text: **`menu_group_settings`** — leading `settings` icon, label "Settings"; **`menu_sync_status`** — leading `sync` icon, label "Sync Status". | Tap `menu_group_settings` → OnGroupSettings → navigate to `settings` (param-less shared screen); closes menu. Tap `menu_sync_status` → OnSyncStatus → navigate to `sync-status` (param-less shared offline-sync dashboard); closes menu. Both close the menu on select (`isMoreMenuExpanded = false`). |
| group_header_card | Card (tonal) | Background primaryContainer (#C8E6C9), elevation 0dp, cornerRadius 0dp, padding 16dp, full-width, flush under top bar. Contains: `group_name_large` — `{{group.name}}` headlineSmall (24sp) onPrimaryContainer semibold; `cycle_info_text` — "Cycle 1 of 12 months • Weekly meetings" (VSLA demo) / "Cycle 3 of 10 months • Monthly meetings" (ROSCA demo) — bodyMedium (14sp) onPrimaryContainer; `header_badges_row` — wrapping horizontal row of chips: `group_type_chip` (icon `category_24_regular` 18dp + label "VSLA"/"ROSCA" — tertiaryContainer bg #BBDEFB, onTertiaryContainer text, corner_radius full, height 32dp, padding 12dp/6dp), `viewer_role_chip` (icon `person_24_regular` + label "organizer"/"member" lowercase — secondaryContainer bg #CCE8E1, onSecondaryContainer text), `member_count_chip` ("20 members" / "10 members" — surfaceVariant bg #E7E0EC, onSurfaceVariant text), `overdue_loans_chip` (only visible when `group.overdueLoansCount > 0` — errorContainer bg #FFDAD6, onErrorContainer text, e.g. "1 overdue"). Chip spacing 8dp horizontal, wraps to a second row on narrow devices. | Non-interactive |
| corpus_card | Card | Background surface (#FFFFFF), elevation 4dp, cornerRadius lg (16dp), padding 20dp, margin_horizontal 16dp, margin_top 12dp. Border switches on `isCorpusInsufficient`: 2dp danger (#C62828) when true, transparent 0dp when false. Visible when `typeConfig.pool_model != 'ROTATING_PAYOUT'`. Contains: `corpus_label` — "Corpus Fund" titleMedium (18sp) onSurface semibold; `corpus_balance_large` — `KES {{corpus.currentBalance \| number}}` displaySmall (36sp) primary700 (#2E7D32) in Roboto Mono; `shareout_projection_text` — "Projected share-out: KES 2,750" bodyMedium (14sp) secondary700 (#00695C), visible when `shareOutProjection != null`; `corpus_blocked_banner` (only when isCorpusInsufficient) — errorContainer #FFDAD6 bg, onErrorContainer text, leading `warning` 20dp icon, message "Loan disbursement is blocked — corpus balance is below minimum threshold.", cornerRadius md, padding 12dp, live_region assertive; `corpus_details_row` — 3-column horizontal row of stat pills at the card foot, evenly spaced with 1dp borderSubtle vertical dividers: `opening_balance_stat` ("Opening Balance" labelSmall textSecondary / "KES 0" bodyLarge onSurface Roboto Mono), `contributions_stat` ("Contributions" / "KES 52,500"), `loans_outstanding_stat` ("Loans Out" / "KES 5,000"). | Non-interactive dashboard surface |
| rotation_card | Card | Background surface (#FFFFFF), elevation 4dp, cornerRadius lg (16dp), padding 20dp, margin_horizontal 16dp, margin_top 12dp. Visible when `typeConfig.pool_model == 'ROTATING_PAYOUT'`. Contains: `rotation_label` — "Rotation Status" titleMedium (18sp) onSurface semibold; `viewer_position_text` — "Your position: #7" (ROSCA demo) displaySmall (36sp) primary700 (#2E7D32) semibold; `next_recipient_row` — horizontal row: `next_recipient_label` "Next payout →" bodyMedium onSurfaceVariant + `next_recipient_chip` "Amina Hassan (#4)" (secondaryContainer bg, onSecondaryContainer text, corner_radius full, padding 12dp/6dp, leading avatar-placeholder circle 20dp secondary700 tint); `corpus_balance_small` — "Pool: KES 20,000" bodyLarge (16sp) tertiary700 (#1565C0) Roboto Mono. | Non-interactive |
| quick_actions_section | Card | Background surface (#FFFFFF), elevation 2dp, cornerRadius lg (16dp), padding 16dp, margin_horizontal 16dp, margin_top 12dp. Header row: `quick_actions_label` "Quick Actions" titleSmall (14sp) semibold onSurfaceVariant (#616161), letter-spaced 0.5. Below the header, exactly ONE of the two grids renders. **management_actions_grid** (2 columns, 12dp column-gap + 12dp row-gap, visible when `viewerRole ∈ {ORGANIZER, CHAIRPERSON, TREASURER}`): `start_meeting_button` (filled — primary #2E7D32 bg, onPrimary text, cornerRadius full, min_height 56dp, leading `meeting_room` 20dp onPrimary, label "Start Meeting" labelLarge semibold), `view_members_button` (outlined — 1dp primary border, primary text, cornerRadius full, min_height 56dp, leading `group` 20dp primary, label "Members"), `view_loans_button` (outlined, leading `account_balance`, label "Loans"), `share_out_button` (outlined — border/text secondary700 #00695C when enabled, outline #79747E border + onSurfaceVariant text when disabled, min_height 56dp, leading `share`, label "Share-Out"; `enabled = isCycleEnd && viewerRole ∈ {ORGANIZER, TREASURER}` → for the VSLA demo the button is DISABLED because isCycleEnd=false). **member_actions_grid** (2 columns, same spacing, visible when `viewerRole == 'MEMBER'`): `view_savings_button` ("My Savings" outlined, leading `savings_24_regular`), `view_loans_member_button` ("My Loans" outlined, leading `account_balance`), `view_meetings_button` ("Meetings" outlined, leading `calendar_month_24_regular`), `view_members_member_button` ("Members" outlined — outline border + onSurfaceVariant text, styled as tertiary/secondary CTA). Each button has 12dp inset padding, full-width within its column cell. | Tap `start_meeting_button` → OnStartMeeting → if `isCorpusInsufficient` emit ShowCorpusBlockedDialog; else NavigateToMeetingCalendar(groupId). Tap `view_members_button` / `view_members_member_button` → OnViewMembers → NavigateToMemberList(groupId). Tap `view_loans_button` / `view_loans_member_button` → OnViewLoans → NavigateToLoanList(groupId). Tap `share_out_button` when enabled → OnShareOut → NavigateToShareOut(groupId, `typeConfig.shareout_formula`); tap when disabled → ShowSnackbar(message_key=`share_out_not_available` "Share-Out is only available at the end of the cycle."). Tap `view_savings_button` → OnViewSavings → NavigateToSavingsDashboard(groupId, typeConfig). Tap `view_meetings_button` → OnStartMeeting → NavigateToMeetingCalendar(groupId) (member read-only variant, corpus-sufficiency check skipped). |
| savings_summary_card | Card | Background surface (#FFFFFF), elevation 2dp, cornerRadius lg (16dp), padding 16dp, margin_horizontal 16dp, margin_top 12dp. Contains: `savings_label` "Savings Summary" titleMedium (18sp) onSurface semibold; `contribution_model_text` bodyMedium (14sp) onSurfaceVariant (#616161) — text adapts on `config.contribution_model`: SHARE_BASED_VARIABLE → "Share-based: KES 200 / share · 1–5 shares / meeting" (VSLA demo); FIXED_AMOUNT → "Fixed: KES 2,000 per meeting" (ROSCA demo); FIXED_NEGOTIATED → "Negotiated fixed: KES {amount} per meeting"; `total_savings_text` — "KES 52,500 total" (VSLA demo) / "KES 60,000 total" (ROSCA demo) titleLarge (22sp) tertiary700 (#1565C0) Roboto Mono, right-aligned at the card foot. | Non-interactive (savings ledger deep-link is via member_actions_grid `view_savings_button`) |
| activity_feed_section | Card | Background surface (#FFFFFF), elevation 2dp, cornerRadius lg (16dp), padding 16dp, margin_horizontal 16dp, margin_top 12dp, margin_bottom 24dp. Contains: `activity_label` "Recent Activity" titleMedium (18sp) onSurface semibold; then a vertical list of `activity_list_item` rows sourced from `recentActivity[]` (VSLA demo = 5 items). Each row: leading `activity_type_icon` 40dp circular chip tinted by activity.type — MEETING `calendar_month_24_regular` primaryContainer, DEPOSIT `arrow_downward_24_regular` on secondaryContainer, LOAN `account_balance_24_regular` on tertiaryContainer, SHARE_OUT `share_24_regular` on accent100, NEW_MEMBER `person_add_24_regular` on primaryContainer; headline `{{activity.description}}` bodyLarge (16sp) onSurface (e.g. "Weekly contribution", "Loan disbursed", "New member joined"); supporting `{{activity.date}} • {{activity.memberName}}` bodyMedium (14sp) textSecondary (e.g. "2026-05-05 • Amina Wanjiru") — memberName omitted for MEETING type; trailing `{{activity.amount \| currency: KES}}` bodyLarge (16sp) Roboto Mono, primary700 for DEPOSIT / danger for LOAN outflow / hidden when amount == null (MEETING, NEW_MEMBER). Row height min 56dp, 1dp borderSubtle divider between rows. | Row tap is a **future affordance** — currently non-interactive (no `on_click` in ui.yaml); reserved for future OnActivityTap navigating to per-transaction detail. |
| shimmer_dashboard | ShimmerPlaceholder | Rendered ONLY in the `loading` state, replacing every card below `top_bar`. 4 stacked placeholders, each height 120dp, cornerRadius lg (16dp), background surfaceVariant (#E7E0EC), margin_horizontal 16dp, margin_top 12dp, animated left-to-right shimmer sweep (motion 3/10 — 1200ms duration, opacity 0.4→1.0→0.4). Represents group_header_card + corpus_card + quick_actions_section + savings_summary_card respectively. | Non-interactive |
| error_state | Empty/Error state | Full-bleed centered layout, background canvas #FAFAFA, padding 24dp horizontal. Contains: leading `cloud_off` 64dp illustration textSecondary (#616161); title "Could not load group" titleLarge (22sp) onSurface semibold, centered, margin_top 16dp; body `{{error.message}}` (resolved per errors enum — "No internet. Showing cached data." / "Server error. Please retry." / "Group not found." / "Session expired.") bodyMedium (14sp) textSecondary, centered, margin_top 8dp, max_width 320dp; `Retry` CTA — FilledButton, primary bg, onPrimary text, cornerRadius full, min_height 48dp, min_width 160dp, margin_top 24dp. Only rendered when `errors.retry == true` (Network, Server); NotFound/Auth hide the CTA (Auth redirects to login instead). | Tap `Retry` → Retry → re-triggers the parallel companion fetch (get_group + get_viewer_role + get_group_corpus + get_group_accounts) with cache invalidation, checks connectivity via `cmp-network-monitor` before dispatching. |

**Component composition per state**:

| State | Rendered composition (top → bottom) |
|-------|-------------------------------------|
| `loading` | top_bar + shimmer_dashboard (×4 placeholders) |
| `content_accumulating` (VSLA demo — ORGANIZER) | top_bar + group_header_card + corpus_card + quick_actions_section (management_actions_grid) + savings_summary_card + activity_feed_section |
| `content_rotating` (ROSCA demo — MEMBER) | top_bar + group_header_card + rotation_card + quick_actions_section (member_actions_grid) + savings_summary_card + activity_feed_section |
| `error` | top_bar + error_state |

---

## Overflow menu (top-bar `more_vert` → `group-dashboard-more-menu`) — NEW (G13)

Tapping the top-bar overflow icon toggles `isMoreMenuExpanded` and reveals a Compose `DropdownMenu` anchored at the top-end of the bar. It carries two items — both navigate to real, param-less shared screens (this replaces a previously-undefined menu reference). Available in every content state and across all roles.

```
┌ Mwangaza Women's Group        [⋮] ┐   top_bar (primary #2E7D32)
│                              ┌──────────────────────┐
│                              │ ⚙  Settings          │  menu_group_settings → settings
│                              │ ⟳  Sync Status       │  menu_sync_status → sync-status
│                              └──────────────────────┘
│                                surface #FFFFFF, elev 3dp, corner 8dp, min_width 200dp
│                                each item 48dp, leading 24dp icon onSurfaceVariant + labelLarge onSurface
└──────────────────────────────────────────────────────┘
  Dismiss: tap outside / select an item → isMoreMenuExpanded = false
```

- **Settings** (`menu_group_settings`, leading `settings` icon) → `OnGroupSettings` → navigate to the shared `settings` screen; no params, no data mutation.
- **Sync Status** (`menu_sync_status`, leading `sync` icon) → `OnSyncStatus` → navigate to the shared `sync-status` offline-sync dashboard; no params, no data mutation.
- Selecting either item closes the menu (`isMoreMenuExpanded = false`) before navigating.

---

## Demo data resolution

Rendered against `demo-data.yaml` seed entries:

**`content_accumulating` state — VSLA (Mwangaza Women's Group), ORGANIZER viewer**:
- `group.name` = "Mwangaza Women's Group", `group.cycleNumber` = 1, `group.cycleLengthMonths` = 12, `group.meetingFrequency` = "Weekly", `group.memberCount` = 20, `group.overdueLoansCount` = 0 (overdue chip hidden)
- `groupTypeName` = "VSLA", `viewerRole` = "ORGANIZER" → management_actions_grid renders
- `typeConfig.pool_model` = "ACCUMULATING" → corpus_card renders (rotation_card hidden)
- `typeConfig.contribution_model` = "SHARE_BASED_VARIABLE" → savings-summary contribution_model_text shows "Share-based: KES 200 / share · 1–5 shares / meeting"
- `corpus.currentBalance` = 47,500 → displaySmall "KES 47,500"; `openingBalance` = 0; `totalContributionsThisCycle` = 52,500; `totalLoansOutstanding` = 5,000
- `shareOutProjection` = 2,750 → shareout_projection_text visible
- `isCorpusInsufficient` = false → corpus_card border transparent, corpus_blocked_banner hidden
- `isCycleEnd` = false → share_out_button DISABLED
- `accounts.savingsBalance` = 52,500 → savings-summary total_savings_text "KES 52,500 total"
- `recentActivity` (5 items from ActivityItem DTO): MEETING "Weekly meeting — week 4 recorded" (2026-05-05, no amount) · DEPOSIT "Weekly contribution" KES 300 (Amina Wanjiru) · DEPOSIT "Weekly contribution" KES 500 (Joseph Kamau) · LOAN "Loan disbursed" KES 8,000 (Grace Akinyi) · NEW_MEMBER "New member joined" (Peter Mwangi, 2026-04-28, no amount)

**`content_rotating` state — ROSCA (Jiunge ROSCA Circle), MEMBER viewer**:
- `group.name` = "Jiunge ROSCA Circle", `group.cycleNumber` = 3 of 10 months, `group.meetingFrequency` = "Monthly", `group.memberCount` = 10, `group.overdueLoansCount` = 0
- `groupTypeName` = "ROSCA", `viewerRole` = "MEMBER" → member_actions_grid renders
- `typeConfig.pool_model` = "ROTATING_PAYOUT" → rotation_card renders (corpus_card hidden)
- `typeConfig.contribution_model` = "FIXED_AMOUNT", `contribution_amount` = 2,000 → savings-summary contribution_model_text "Fixed: KES 2,000 per meeting"
- `rotationPosition` = 7 → viewer_position_text "Your position: #7"
- `nextRecipientName` = "Amina Hassan", `nextRecipientPosition` = 4 → next_recipient_chip "Amina Hassan (#4)"
- `corpus.currentBalance` = 20,000 → corpus_balance_small "Pool: KES 20,000"
- `accounts.savingsBalance` = 60,000 → savings-summary total_savings_text "KES 60,000 total"; `activeLoanCount` = 0

**`loading` state**: shimmer only, no bound demo data.

**`error` state**: `error.type = Network`, `error.message` = "No internet. Showing cached data." → Retry CTA rendered.

---

## Role & type variant matrix (visibility contract)

| viewerRole | typeConfig.pool_model | Metric card shown | Quick-actions grid | share_out_button enabled iff |
|---|---|---|---|---|
| ORGANIZER | ACCUMULATING | corpus_card | management_actions_grid | isCycleEnd == true |
| ORGANIZER | ROTATING_PAYOUT | rotation_card | management_actions_grid | *(share_out_button hidden — ROSCA has no share-out phase; enabled=false via missing shareout_formula)* |
| CHAIRPERSON | ACCUMULATING | corpus_card | management_actions_grid | never (chairperson not in {ORGANIZER, TREASURER}) |
| CHAIRPERSON | ROTATING_PAYOUT | rotation_card | management_actions_grid | never |
| TREASURER | ACCUMULATING | corpus_card | management_actions_grid | isCycleEnd == true |
| TREASURER | ROTATING_PAYOUT | rotation_card | management_actions_grid | never |
| MEMBER | ACCUMULATING | corpus_card | member_actions_grid | n/a (share_out_button not present in member grid) |
| MEMBER | ROTATING_PAYOUT | rotation_card | member_actions_grid | n/a |

**Corpus-insufficient overlay** (`isCorpusInsufficient == true`, VSLA/ACCUMULATING only):
- corpus_card border switches to 2dp #C62828 danger
- corpus_blocked_banner renders inside the card (errorContainer background, warning icon, live_region assertive)
- start_meeting_button remains visually enabled but its OnStartMeeting handler emits `ShowCorpusBlockedDialog` instead of navigating

---

## Interaction contract (action → effect → target)

| Component | Action | Effect | Target / notes |
|---|---|---|---|
| top_bar `arrow_back` | OnBack | navigate | Pops backstack to group-list (or group-create if entry_point `group_created`) |
| top_bar `more_vert` | OnMoreOptions | transform_state | Toggles `isMoreMenuExpanded` to reveal `group-dashboard-more-menu` Compose-DropdownMenu; local UI state only |
| menu_group_settings (overflow item) | OnGroupSettings | navigate | NavigateToSettings → shared `settings` screen; param-less; closes menu |
| menu_sync_status (overflow item) | OnSyncStatus | navigate | NavigateToSyncStatus → shared `sync-status` offline-sync dashboard; param-less; closes menu |
| start_meeting_button | OnStartMeeting | navigate | Corpus-sufficiency check → NavigateToMeetingCalendar(groupId); ORGANIZER/CHAIRPERSON only; if isCorpusInsufficient → ShowCorpusBlockedDialog |
| view_members_button / view_members_member_button | OnViewMembers | navigate | NavigateToMemberList(groupId); management roles = full mgmt, MEMBER = read-only directory |
| view_loans_button / view_loans_member_button | OnViewLoans | navigate | NavigateToLoanList(groupId); read-only for MEMBER |
| share_out_button (enabled) | OnShareOut | navigate | NavigateToShareOut(groupId, `typeConfig.shareout_formula`); ORGANIZER/TREASURER only; applies shareout_formula for ACCUMULATING types |
| share_out_button (disabled) | OnShareOut | transform_state | ShowSnackbar(share_out_not_available) — "Share-Out is only available at the end of the cycle." |
| view_savings_button | OnViewSavings | navigate | NavigateToSavingsDashboard(groupId, typeConfig); MEMBER only — self-scoped to the group's savings dashboard (forwards the groupId + typeConfig this dashboard already holds; replaces the prior member-savings-detail target that required a memberId this screen does not carry) |
| view_meetings_button | OnStartMeeting | navigate | NavigateToMeetingCalendar(groupId); MEMBER read-only variant; corpus-sufficiency check bypassed |
| error_state Retry CTA | Retry | call_api | Re-triggers parallel companion fetch (get_group + get_viewer_role + get_group_corpus + get_group_accounts) with cache invalidation via cmp-network-monitor |
| Pull-to-refresh (top-level Column) | OnRefresh | call_api | Re-runs the parallel fan-out without a full loading state — shows a top spinner; on success updates state fields in place |

---

## API bindings

Sourced from `screens/group-dashboard/api.yaml` (COMP-GRP-001 companion contract). Loads run **in parallel** on entry — the screen enters `Content` only once all four calls resolve (or `Error` on any failure that lacks a cached fallback):

- `get_group(groupId)` → Group + GroupTypeConfig (fills `group`, `typeConfig`, `groupTypeName`, `config`)
- `get_viewer_role(groupId, userId)` → ViewerRole (fills `viewerRole` from dt_member_role datatable)
- `get_group_corpus(groupId)` → GroupCorpus (fills `corpus`, `shareOutProjection`, `rotationPosition`, `nextRecipientName`, `nextRecipientPosition`)
- `get_group_accounts(groupId)` → GroupAccounts (fills `accounts.savingsBalance`, `accounts.loansOutstanding`, `accounts.activeLoanCount`)
- `get_group_activity(groupId, limit=5)` → List<ActivityItem> (fills `recentActivity`)

Client-side derivations after data arrives:
- `isCorpusInsufficient = corpus.currentBalance < config.minimumDisbursementThreshold` (ACCUMULATING only)
- `isCycleEnd = group.cycleNumber == config.cycleLengthMonths` (drives share_out_button enabled state)

Offline behaviour (via `cmp-network-monitor`): on network unavailability the ViewModel returns the last-cached Group + corpus snapshot and surfaces a warning banner in the group_header_card row; the Retry CTA on error_state re-checks connectivity before re-issuing calls.

---

## Accessibility

- All interactive components meet 48dp min touch target (primary CTAs 56dp)
- `top_bar` overflow icon carries content_description "More options"
- `corpus_blocked_banner` uses `live_region=assertive` — screen readers announce the disbursement block immediately when it appears
- `error_state` announces title + body when the state becomes active
- Chip labels in `header_badges_row` are lower-cased for display but carry the canonical uppercase role in their accessibility label (e.g. displayed "organizer" → announced "Organizer role")
- The role-gated grids swap declaratively, so screen-reader focus lands correctly on the first button of whichever grid is active (no hidden phantom buttons)
- Currency values use `contentDescription` overrides to speak "forty-seven thousand five hundred Kenyan shillings" instead of raw digits where the platform supports it

## i18n

All user-facing strings resolve via `strings.xml` keys defined in ui.yaml `i18n.en`:
- `corpus_label`, `corpus_blocked`, `quick_actions_label`, `start_meeting`, `view_members`, `view_loans`, `share_out`, `savings_label`, `contribution_range`, `activity_label`, `share_out_not_available`
- Error strings: `error_network`, `error_server`, `error_not_found`, `error_auth`

Group name, group type name, currency code, and member names are **data-driven** (not localised) — they arrive verbatim from the companion API and demo data.
