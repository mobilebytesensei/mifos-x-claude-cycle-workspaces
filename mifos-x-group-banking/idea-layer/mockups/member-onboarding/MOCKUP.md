# Member Onboarding — Mockup Spec

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans — scaled up for low-vision rural users
**Palette**:
- Primary: #2E7D32 (VSLA-green) — trust, growth
- Secondary: #FF8F00 (amber) — TREASURER role color
- Tertiary: #1565C0 (trust-blue) — SECRETARY role color, attendance
- Surface: #FAFAFA — card backgrounds
- Background: #FFFFFF

**Shape**: full=9999dp (avatars), large=16dp (cards), medium=12dp (list items), small=8dp (chips)
**Elevation**: level_2 (3dp) for cards, level_3 (6dp) for sheets
**Min touch target**: 48dp (list items), 56dp (FAB, Save Member button)
**Motion**: Standard easing 250–400ms for screens, 150ms for chips/badges

---

## Screen-by-Screen

### MemberListScreen (`/groups/{groupId}/members`)

**Layout**: `Scaffold` + `TopAppBar` (with subtitle) + `LazyColumn` + `FloatingActionButton`

```
┌─────────────────────────────────────────┐
│ [←] Members                             │  bg=#2E7D32, text=#FFFFFF
│     Mwangaza Women's Group              │  subtitle bodySmall 12sp, #FFFFFF 80% alpha
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │  List item — h=72dp min
│ │ [AW]  Amina Wanjiru                 │ │  avatar 48dp, circle, bg=#FFDDB3, initials
│ │       Savings: KES 3,500            │ │  bodySmall 12sp, #424942
│ │                   [Treasurer][No Loan│  chips: trailing column
│ └─────────────────────────────────────┘ │  divider 0.5dp #C2C9BD
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ [JK]  Joseph Kamau                  │ │  avatar bg=#A6F1A6 (CHAIRPERSON green)
│ │       Savings: KES 4,200            │ │
│ │                [Chairperson][Active] │ │  loan badge bg=#C8E6C9 text=#1B5E20
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ [GA]  Grace Achieng                 │ │  avatar bg=#D2E4FF (SECRETARY blue)
│ │       Savings: KES 2,800            │ │
│ │                  [Secretary][No Loan]│ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ [PO]  Peter Otieno                  │ │  avatar bg=#DEE5DA (MEMBER grey)
│ │       Savings: KES 1,500            │ │
│ │                     [Member][Overdue]│ │  overdue badge bg=#FFCDD2 text=#B71C1C
│ └─────────────────────────────────────┘ │
│                                         │
│                          [+ Add Member] │  FAB bottom_end, bg=#2E7D32, 56dp
└─────────────────────────────────────────┘
```

**Swipe-to-reveal** (start-to-end direction):
```
← [person icon] View Profile [primaryContainer bg #A6F1A6]
```
- Swipe threshold: 80dp
- Reveal width: 120dp
- Background: #A6F1A6, icon=person tint=#002106, label bodyMedium 14sp #002106
- On full swipe: same as tap → NavigateToMemberProfile

**States**:

_Loading_: TopAppBar + 6× shimmer rows (h=72dp, cornerRadius=4dp, bg=#DEE5DA, animated)

_Empty_: TopAppBar + centered EmptyState: group_add icon 80dp + "No members yet" + "Add the first member to this group." + "Add Member" OutlinedButton + FAB

_Error_: TopAppBar + ErrorState: cloud_off + "Could not load members" + error.message + "Retry" FilledButton

_Loading more_ (pagination): linear progress indicator at bottom of list, height=4dp, color=#2E7D32, visible when isLoadingMore=true

---

### MemberProfileScreen (`/groups/{groupId}/members/{memberId}`)

**Layout**: `Scaffold` + `TopAppBar` + `LazyColumn` (scrollable sections)

```
┌─────────────────────────────────────────┐
│ [←] Member Profile                      │  bg=#2E7D32, text=#FFFFFF
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │  Header — bg=#A6F1A6, pad=20dp, no border
│ │         [AW]                        │ │  avatar 80dp circle, center-aligned
│ │      Amina Wanjiru                  │ │  headlineSmall 24sp, #002106
│ │       [Treasurer]                   │ │  chip bg=#FF8F00 text=#FFFFFF
│ │   📞 +254712345678                  │ │  bodyMedium 14sp, #002106, phone icon
│ │   Member since 15 Jan 2026          │ │  bodySmall 12sp, #002106
│ │                     [Edit Role]     │ │  OutlinedButton (visible to chairperson only)
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │  Savings History card — elev=2dp
│ │ Savings History                     │ │  titleMedium 16sp/500, #1A1C19
│ │ KES 3,500                           │ │  headlineMedium 28sp, #2E7D32
│ │                                     │ │
│ │ ╭──╮╭───╮╭────╮╭─────╮╭──────╮     │ │  sparkline chart h=80dp
│ │ ╰──╯╰───╯╰────╯╰─────╯╰──────╯     │ │  line=#2E7D32, fill=#A6F1A6 20% opacity
│ └─────────────────────────────────────┘ │
│                                         │
│ [Active Loan card — shown only if loan  │
│  exists; hidden for Amina (no loan)]    │
│                                         │
│ ┌─────────────────────────────────────┐ │  Attendance card — elev=2dp
│ │ Meeting Attendance                  │ │
│ │ 14 / 15                             │ │  headlineMedium 28sp, #1565C0
│ │ 93% attendance rate                 │ │  bodyMedium 14sp, #424942
│ │ ██████████████████████░░ 93%        │ │  LinearProgressIndicator h=8dp
│ └─────────────────────────────────────┘ │  indicator=#1565C0 (≥80%), track=#DEE5DA
└─────────────────────────────────────────┘
```

**Active Loan Card** (visible when activeLoan != null):
```
┌─────────────────────────────────────────┐
│ Active Loan                             │  titleMedium 16sp/500
│ Group Loan                              │  bodyMedium 14sp, #424942
│ KES 2,000 outstanding                   │  titleLarge 22sp, #1A1C19
│                                         │
│ [⚠ This loan is in arrears.            │  errorContainer banner (conditional)
│    Due: 2026-04-15]                     │  bg=#FFDAD6, text=#410002
└─────────────────────────────────────────┘  border 2dp #D32F2F when inArrears=true
```

**Savings Sparkline** (h=80dp, w=fullWidth − 32dp, inside card):
- Type: LineChart (sparkline, no axes, no legend)
- Data: 7 points from savingsHistory list (Jan–Mar 2026)
- Line: 2dp stroke, color=#2E7D32
- Area fill: gradient #A6F1A6 to transparent (top to bottom, 40% opacity)
- Points: 4dp filled circles at each data point, color=#2E7D32
- Animated: line draws from left to right on appear (600ms, decelerated easing)

**Role Edit Bottom Sheet** (shown when isEditingRole=true):
```
╔═════════════════════════════════════════╗
║ ▬▬▬ (drag handle)                       ║  handle 4dp × 32dp, rounded
║                                         ║  bg=#FAFAFA
║ Change Member Role                      ║  titleMedium 16sp/500, #1A1C19
║─────────────────────────────────────────║
║ ○ Chairperson                           ║  RadioButton + labelLarge 14sp
║ ● Treasurer    (current)                ║  selected: primary #2E7D32 radio
║ ○ Secretary                             ║
║ ○ Member                                ║
║─────────────────────────────────────────║
║ [        Confirm         ]              ║  FilledButton, bg=#2E7D32, h=56dp, fullWidth
╚═════════════════════════════════════════╝
```
- Sheet background: #FAFAFA
- Corner radius: 28dp top-only
- Elevation: level_3 (6dp)
- Scrim: #000000 at 32% opacity
- List items: min h=56dp, RadioButton leading, labelLarge trailing text
- Confirm button: shows CircularProgressIndicator 16dp when isUpdatingRole=true

---

### MemberAddScreen (`/groups/{groupId}/members/add`)

**Layout**: `Scaffold` + close `TopAppBar` + scrollable `Column` + sticky save button

```
┌─────────────────────────────────────────┐
│ [✕] Add Member                          │  bg=#2E7D32, text=#FFFFFF
├─────────────────────────────────────────┤
│                                         │
│         ┌────────────────┐              │
│         │                │              │  120dp × 120dp circle
│         │   add_a_photo  │              │  bg=#DEE5DA, cornerRadius=9999dp
│         │   (40dp icon)  │              │  tap whole area = open photo picker
│         └────────────────┘              │  [✕] remove button top-right when photo set
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ First Name *                     │   │  OutlinedTextField, h=56dp
│  │ e.g. Amina                       │   │  placeholder bodyMedium 14sp #727971
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ Last Name *                      │   │  OutlinedTextField, h=56dp
│  │ e.g. Wanjiru                     │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ Phone Number *                   │   │  OutlinedTextField, keyboard=phone
│  │ +254712345678                    │   │  prefix="+254", h=56dp
│  │ Kenyan number: +254 or 07XXXXXXXX│   │  helper bodySmall 12sp #424942
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │ Role *                       [▼] │   │  ExposedDropdownMenu, h=56dp
│  │ Member (default)                 │   │
│  └──────────────────────────────────┘   │
│                                         │
│  [wifi_off] You are offline. This...   │  tertiaryContainer, visible when isOffline
│                                         │
│  ┌──────────────────────────────────┐   │
│  │          Save Member             │   │  FilledButton, bg=#2E7D32, h=56dp, fullWidth
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Photo picker area**:
- Default state (no photo): circular container 120dp, bg=#DEE5DA, add_a_photo icon 40dp tint=#424942, centered
- Photo selected: circular container 120dp, image fills container with circular clip (cornerRadius=9999dp). Cancel icon (✕) appears top-right as 32dp icon-button, bg=#D32F2F, tint=#FFFFFF.
- Tap anywhere on circle: opens PhotoSourceBottomSheet

**PhotoSourceBottomSheet**:
```
╔════════════════════════════╗
║ Add Photo                  ║  titleMedium
║────────────────────────────║
║ [camera_alt]  Take Photo   ║  list item, h=56dp
║ [photo_lib]  Choose from   ║
║              Gallery       ║
╚════════════════════════════╝
```
- Sheet corner radius: 28dp top only
- Each option: ListItem with leading icon (24dp), headlineLarge 16sp, min h=56dp

**Photo validation**: file size check before upload (max 2MB). If oversized: snackbar "Photo must be smaller than 2 MB."

**Role Dropdown options**:
- Chairperson (value=CHAIRPERSON)
- Treasurer (value=TREASURER)
- Secretary (value=SECRETARY)
- Member (value=MEMBER) — default selected

**Offline banner** (visible when isOffline=true):
- bg=#D2E4FF, icon=wifi_off tint=#1565C0, text=#001C39
- Text: "You are offline. This member will be added when you reconnect."
- bodySmall 12sp, padding=12dp, cornerRadius=8dp

---

## Interaction Patterns

**Member list item tap**: bounded ripple 200ms → NavigateToMemberProfile
**Swipe start-to-end**: reveals green "View Profile" action. On swipe completion (>80% width): immediate navigation. On partial swipe release: snaps back.

**FAB (Add Member)**: collapses on scroll down (threshold 200dp), extends on scroll up. Person_add icon + "Add Member" label.

**Profile load**: three parallel API calls (get_client, get_client_accounts, get_member_role). Shimmer (4×100dp cards) shown during load. On success: cards fade in staggered 50ms each. Sparkline animates draw-on-entry.

**Edit Role flow**:
1. "Edit Role" button visible only when isCurrentUserChairperson=true
2. Tap: ModalBottomSheet expands from bottom (450ms long_1, decelerated easing). Scrim fades in.
3. Current role pre-selected in radio group
4. User taps different role: radio animates to selected (#2E7D32, 150ms)
5. Tap "Confirm": isUpdatingRole=true, button shows spinner 16dp white
6. API PUT /datatables/dt_member_role/{clientId} succeeds: sheet dismisses (400ms, accelerated), role chip on header updates with crossfade (200ms), snackbar "Role updated successfully."
7. API fails: sheet stays open, snackbar "Could not update role. Please retry."

**Member-add form submit**:
1. Tap "Save Member": validate all fields synchronously
2. Invalid: error borders animate in (#D32F2F, 150ms), error helper text slides down (150ms)
3. Valid, online: isSubmitting=true, button shows spinner. API chain: create_client → assign_member_role → upload_photo (if photoUri set) → NavigateToMemberProfile
4. Valid, offline: enqueue all three sync operations → ShowOfflineSyncDialog → navigate back to member-list on dismiss

**Back/discard** (member-add): if any field has content → DiscardDialog "Discard new member?" [Cancel] [Discard]

---

## Accessibility

**Member list items**: contentDescription: "${member.displayName}, ${member.role}, KES ${member.savingsBalance}, loan status ${member.loanStatus}"
**Avatars**: alt text = "${member.displayName} profile photo" or "${initials} avatar"
**Chips**: contentDescription includes role name and context (e.g., "Treasurer role badge")
**Swipe action**: also accessible as a button via accessibility services
**FAB**: contentDescription "Add new member to group"
**Attendance progress bar**: accessibilityDescription "${meetingsAttended} of ${totalMeetings} meetings attended, ${attendanceRate}%"
**Sparkline**: accessibilityDescription "Savings history chart: KES 500 in January to KES 3,500 in March 2026"
**Focus ring**: 3dp primaryContainer (#A6F1A6) on all interactive elements
**Touch targets**: all list rows minimum 72dp; FAB 56dp; "Edit Role" button 48dp; all form fields 56dp
