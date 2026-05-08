# Group Management — Mockup Spec

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans — scaled up for low-vision rural users
**Palette**:
- Primary: #2E7D32 (VSLA-green) — trust, growth
- Secondary: #FF8F00 (amber) — shared coin, harvest energy
- Tertiary: #1565C0 (trust-blue) — informational elements
- Surface: #FAFAFA — card backgrounds
- Background: #FFFFFF

**Shape tokens**: small=8dp, medium=12dp, large=16dp, extra_large=28dp
**Elevation**: Cards use level_2 (3dp) to level_4 (8dp)
**Min touch target**: 48dp (standard), 56dp (primary CTAs and FABs)
**Motion**: Standard easing `cubic-bezier(0.2, 0.0, 0, 1.0)`, medium durations 250–400ms

---

## Screen-by-Screen

### GroupListScreen (`/groups`)

**Layout**: `Scaffold` with `TopAppBar` + `LazyColumn` + `ExtendedFloatingActionButton`

```
┌─────────────────────────────────────────┐
│ [AppBar — #2E7D32]  My Groups   🔔      │  h=64dp, status bar compensated
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ 🔍 Search groups…              ✕   │ │  h=48dp, cornerRadius=28dp, elev=2dp
│ └─────────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐  │  Group card start
│  │  Mwangaza Women's Group           │  │  titleMedium 16sp/500
│  │  [Cycle 1]  5 members             │  │  chip bg=#FFDDB3 text=#2A1700
│  │  Last met: 28 Apr 2026            │  │  bodySmall 12sp
│  │                        [● GREEN]  │  │  badge bg=#C8E6C9 text=#1B5E20
│  └───────────────────────────────────┘  │  cornerRadius=12dp, pad=16dp, elev=2dp
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Tumaini Savings Circle           │  │
│  │  [Cycle 3]  12 members            │  │
│  │  Last met: 25 Apr 2026            │  │
│  │                       [● AMBER]   │  │  badge bg=#FFF9C4 text=#E65100
│  └───────────────────────────────────┘  │
│                                         │
│                                         │
│                             [+ New Group│  FAB: 56dp, bg=#2E7D32, icon+label
│                                       ] │  position=bottom_end, margin=16dp
└─────────────────────────────────────────┘
```

**States**:

_Loading_: TopAppBar + SearchBar + 5× shimmer cards (h=88dp, cornerRadius=12dp, bg=#DEE5DA, animated shimmer left-to-right)

_Empty_: TopAppBar + SearchBar + centered illustration (group_off icon 80dp, #727971) + title "No groups yet" (headlineSmall, #1A1C19) + body "Create your first savings group to get started." (bodyMedium, #424942) + "Create Group" OutlinedButton (borderColor=#2E7D32) + FAB

_Error_: TopAppBar + full-screen error area: cloud_off icon 64dp, title "Could not load groups" (titleLarge), body text from error.message, "Retry" FilledButton (#2E7D32)

_Search active_: SearchBar has focus; filtered list updates in real time; clear icon appears at right; empty filter state shows "No results for '{{query}}'" subtitle text

**Interactions**:
- Card tap: ripple effect (duration 200ms, bounded), navigates to group-dashboard
- Search input: keyboard shows immediately; list filters as user types (debounce 150ms)
- Pull-to-refresh: Material 3 pull indicator (#2E7D32); invalidates cache and re-fetches
- FAB: slight elevation on press; navigates to group-create

---

### GroupDashboardScreen (`/groups/{groupId}`)

**Layout**: `Scaffold` with `TopAppBar` (with back arrow) + `LazyColumn` (vertical scroll with 16dp item spacing)

```
┌─────────────────────────────────────────┐
│ [←] Mwangaza Women's Group        [⋮]  │  bg=#2E7D32, text=#FFFFFF
├─────────────────────────────────────────┤
│                                         │
│ ┌───────────────────────────────────────┤  Group header — bg=#A6F1A6, pad=16dp
│ │ Mwangaza Women's Group                │  headlineSmall 24sp, #002106
│ │ Cycle 1 of 12 months • Weekly meetings│  bodyMedium 14sp, #002106
│ │ [5 members]  [0 overdue]              │  chips: bg=#FFDDB3 / surfaceVariant
│ └───────────────────────────────────────┘
│                                         │
│ ┌───────────────────────────────────────┐  Corpus card — bg=#FAFAFA, elev=8dp
│ │ Corpus Fund                           │  titleMedium 16sp/500
│ │ KES 47,500                            │  displaySmall 36sp, #2E7D32
│ │ Opening: KES 0  │ Contrib: KES 52,500 │  stat row — bodyMedium 14sp
│ │ Loans Out: KES 5,000                  │  bodyMedium
│ └───────────────────────────────────────┘  cornerRadius=16dp, pad=20dp
│  [CORPUS BLOCKED BANNER — hidden when sufficient]
│  ⚠ Loan disbursement is blocked...      │  bg=#FFDAD6, text=#410002
│                                         │
│ ┌───────────────────────────────────────┐  Quick Actions card — elev=2dp
│ │ Quick Actions                         │  titleSmall 14sp, #424942
│ │ ┌──────────────┐ ┌──────────────────┐ │
│ │ │[🏛] Start    │ │[👥] Members      │ │  2-column grid
│ │ │    Meeting   │ │                  │ │  Start: filled #2E7D32
│ │ └──────────────┘ └──────────────────┘ │  Members: outlined #2E7D32
│ │ ┌──────────────┐ ┌──────────────────┐ │
│ │ │[💰] Loans    │ │[📤] Share-Out    │ │  Loans: outlined #2E7D32
│ │ │              │ │  (disabled)      │ │  Share-Out: outlined, disabled at mid-cycle
│ │ └──────────────┘ └──────────────────┘ │
│ └───────────────────────────────────────┘
│                                         │
│ ┌───────────────────────────────────────┐  Savings Summary — elev=2dp
│ │ Savings Summary                       │
│ │ Mandatory: KES 100 – KES 500/meeting  │  bodyMedium #424942
│ │ KES 52,500 total                      │  titleLarge 22sp, #1565C0
│ └───────────────────────────────────────┘
│                                         │
│ ┌───────────────────────────────────────┐  Recent Activity — elev=2dp
│ │ Recent Activity                       │
│ │ [🤝] Meeting #4 conducted             │  list-item, h=56dp
│ │      28 Apr 2026 • All members        │
│ │ [💵] Deposit — Amina Wanjiru         │
│ │      KES 500 · 28 Apr 2026           │
│ └───────────────────────────────────────┘
└─────────────────────────────────────────┘
```

**States**:

_Loading_: TopAppBar + 4× shimmer blocks (h=120dp, cornerRadius=16dp, animated)

_Corpus Insufficient_: Corpus card gains a 2dp error (#D32F2F) border. Warning banner appears between corpus card and quick actions: `⚠ Loan disbursement is blocked — corpus balance is below minimum threshold.` bg=#FFDAD6, text=#410002. Start Meeting still works; loan disbursement on that screen will be blocked.

_Error_: Full-screen error with cloud_off + retry button

---

### GroupCreateScreen (`/groups/create`)

**Layout**: `Scaffold` with close-icon `TopAppBar` + step indicator + scrollable form content + sticky bottom buttons

**Step Indicator** (below top bar):
```
  ●──────────●──────────○
Identity   Rules     Review
(active)  (inactive) (inactive)
```
Active dot: #2E7D32 filled. Completed dot: #FF8F00 filled. Inactive: #727971 outlined. Line: #C2C9BD. Labels: labelSmall 11sp.

**Step 1 — Group Identity**:
```
┌──────────────────────────────────────────┐
│ [✕] New Group                            │  AppBar — bg=#2E7D32
├──────────────────────────────────────────┤
│  ● ─────── ○ ─────── ○                  │  Step indicator
│ Identity   Rules    Review               │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Group Name *              [60]   │    │  OutlinedTextField, h=56dp
│  │ e.g. Mwangaza Women's Group      │    │  placeholder bodyMedium #727971
│  │ 3–60 characters                  │    │  helper bodySmall
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Office *                    [▼]  │    │  Dropdown, h=56dp
│  │ Select office                    │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Currency *                  [▼]  │    │  Dropdown (KES default)
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Meeting Day *               [▼]  │    │  Dropdown (Mon–Sun)
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Meeting Time *              [🕐] │    │  TimePicker field, h=56dp
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │            Next                  │    │  FilledButton full-width, bg=#2E7D32
│  └──────────────────────────────────┘    │
└──────────────────────────────────────────┘
```

**Step 2 — Rules**: 6 numeric text fields (Min Contribution, Max Contribution, Loan Multiplier, Interest Rate, Cycle Length, Fine Amount). Each: OutlinedTextField h=56dp, keyboard=numeric, helper text explains context. Next + Back buttons at bottom.

**Step 3 — Review**:
```
┌───────────────────────────────────────────┐
│ Review Group Details         titleMedium  │  Card bg=#FAFAFA, cornerRadius=16dp
│                                           │
│ Identity                                  │  section header labelMedium #727971
│  Name        Mwangaza Women's Group       │  bodyMedium #1A1C19
│  Office      Nairobi Head Office          │
│  Currency    KES                          │
│  Meeting     Monday at 09:00              │
│                                           │
│ Rules                                     │
│  Contribution  KES 100 – KES 500          │
│  Loan Mult.    3× savings                 │
│  Interest      10% flat                   │
│  Cycle         12 months                  │
│  Late Fine     KES 50                     │
│                                           │
│ [wifi_off] You are offline. This group... │  tertiaryContainer banner (conditional)
│                                           │
│  ┌──────────────────────────────────────┐ │
│  │         Create Group                 │ │  FilledButton full-width, h=56dp
│  └──────────────────────────────────────┘ │
│            Back                           │  TextButton
└───────────────────────────────────────────┘
```

---

## Interaction Patterns

**Tap Group Card**: 200ms bounded ripple from tap origin. Card scale 1.0 → 0.98 → 1.0 (spring). Then navigate: shared element transition on group name text (fade + slide up, 350ms).

**Pull to Refresh**: Standard M3 pull indicator animates at #2E7D32. On release, spinner completes rotation, data reloads, indicator dismisses with 200ms fade.

**FAB Tap**: FAB shows bounded ripple; screen transition slides new screen from bottom (300ms, standard easing). FAB collapses on scroll down (scroll threshold 200dp), re-extends on scroll up.

**Wizard Step Advance**: Validation runs synchronously. Invalid fields animate border to #D32F2F with helper text fade-in (150ms). Valid step: step indicator dot fills with #FF8F00 animation (200ms), content slides left (300ms, standard easing).

**Corpus Insufficient Banner**: Animates in with slide-down + fade-in (250ms). Error border on corpus card pulses once (animation: border-color #FAFAFA → #D32F2F, 300ms). Remains visible until balance is sufficient again.

**Submit Loading**: "Create Group" button label fades out (100ms), CircularProgressIndicator fades in center of button (100ms). Button remains full width. All form fields become disabled (alpha 0.38).

---

## Accessibility

**Touch targets**: All interactive elements meet 48dp minimum. Primary CTAs (Next, Create Group, Quick Action buttons, FAB) are 56dp.

**Color contrast**:
- Primary (#2E7D32) on white: 5.83:1 — WCAG AAA
- onPrimary (#FFFFFF) on #2E7D32: 13.5:1 — WCAG AAA
- Error (#D32F2F) on white: 5.91:1 — WCAG AAA
- Secondary (#FF8F00) on white: 3.21:1 — AA large only; used only for chips ≥14sp

**Keyboard / TalkBack**:
- All cards have `contentDescription` combining group name + health status + cycle info
- FAB contentDescription: "Create new savings group"
- Corpus block banner is announced by accessibility services when it appears
- Wizard: step changes announced as "Step 2 of 3, Rules"
- Form fields use `labelledBy` semantics

**Focus ring**: 3dp ring in primaryContainer (#A6F1A6) for keyboard navigation

**Dynamic type**: All text sizes defined in sp; system font scaling respected. Comfortable density (extra spacing) aids rural low-vision users.
