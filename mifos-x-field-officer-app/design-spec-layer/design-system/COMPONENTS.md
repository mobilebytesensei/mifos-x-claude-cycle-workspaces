# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/design-system/COMPONENTS.md"
# last_modified: "2026-03-20"

# Component Specifications - Mifos X Field Officer App

> **Design System**: Material Design 3
> **Version**: 1.0.0
> **Updated**: 2026-03-13
> **Pattern**: Trust + Clarity (Banking/Finance)

All components follow M3 specifications adapted for the field officer banking context. Touch targets are minimum 48dp. All interactive states (default, hovered, pressed, focused, disabled) are specified.

---

## 1. Top App Bar

### Standard Top App Bar
Used on most screens (Client List, Loan List, Collections).

**Structure**:
```
[Navigation Icon] [Title] [Action Icons...]
```

| Property | Value |
|----------|-------|
| Height | 64dp |
| Background | `surface` (default), `surfaceContainer` (on scroll) |
| Title style | `titleLarge` (22sp, weight 500) |
| Title color | `onSurface` |
| Navigation icon | 24dp, `onSurface` color, 48dp touch target |
| Action icons | 24dp each, `onSurfaceVariant`, 48dp touch target |
| Elevation | 0dp (default), 3dp (on scroll) |
| Padding | 4dp leading, 4dp trailing (icons sit at 8dp from edge with padding) |

**Sync Status Indicator** (Banking-specific):
- Position: Trailing action area, before other icons
- States: `ArrowSync24Regular` (syncing, animated), `CloudCheckmark24Regular` (synced, tertiary color), `CloudOff24Regular` (offline, error color)
- Badge: Numeric badge on sync icon shows pending-upload count

**Scrolled State**:
- Background transitions to `surfaceContainer` with 200ms ease
- Elevation appears (3dp)
- Title remains visible

### Medium Top App Bar
Used on detail screens (Client Details, Loan Details).

| Property | Value |
|----------|-------|
| Collapsed height | 64dp |
| Expanded height | 112dp |
| Expanded title style | `headlineMedium` (28sp) |
| Collapsed title style | `titleLarge` (22sp) |
| Title position | Bottom-left when expanded, center when collapsed |

### Large Top App Bar
Used on Dashboard screen.

| Property | Value |
|----------|-------|
| Collapsed height | 64dp |
| Expanded height | 152dp |
| Expanded title style | `headlineLarge` (32sp) |
| Subtitle | Officer name + last sync time in `bodySmall` |

---

## 2. Bottom Navigation Bar

The primary navigation for the field officer app. 4 tabs.

**Structure**:
```
[Clients Tab] [Loans Tab] [Collections Tab] [More Tab]
```

| Property | Value |
|----------|-------|
| Height | 80dp total (56dp bar + 24dp bottom safe area) |
| Background | `surfaceContainer` |
| Indicator color | `secondaryContainer` |
| Active icon color | `onSecondaryContainer` |
| Active label color | `onSurface` |
| Inactive icon color | `onSurfaceVariant` |
| Inactive label color | `onSurfaceVariant` |
| Label style | `labelMedium` (12sp, weight 500) |
| Indicator shape | `full` (pill shape, 64dp wide x 32dp tall) |
| Touch target per item | Full tab width x 56dp height |
| Elevation | 3dp |

**Tab Definitions**:

| Tab | Icon | Label | Badge |
|-----|------|-------|-------|
| Clients | `Person24Regular` | "Clients" | None |
| Loans | `Money24Regular` | "Loans" | Overdue count (error badge) |
| Collections | `WalletCreditCard24Regular` | "Collections" | Today's pending (primary badge) |
| More | `Navigation24Regular` | "More" | None |

**Active State**: Shows filled icon variant + indicator pill behind icon.

**Badge Specifications**:
- Small dot (no number): 6dp diameter, `error` color
- Count badge (1-99): 16dp height, min 16dp width, `error` color, `labelSmall` white text
- Large count (99+): Shows "99+" text

---

## 3. Buttons

### Primary Button (Filled)
Used for primary actions: "Submit Payment", "Save Client", "Approve Loan".

| Property | Value |
|----------|-------|
| Height | 40dp minimum (touch area 48dp via padding) |
| Horizontal padding | 24dp |
| Background | `primary` (#1B5EA6) |
| Text color | `onPrimary` (#FFFFFF) |
| Text style | `labelLarge` (14sp, weight 500) |
| Corner radius | 9999dp (fully rounded) |
| Elevation | 0dp (flat, M3 standard for filled button) |
| Ripple color | `onPrimary` at 12% |
| Disabled background | `onSurface` at 12% |
| Disabled text | `onSurface` at 38% |
| Min width | 64dp |
| Icon (optional) | 18dp leading icon with 8dp gap |

**States**:
- Default: `primary` background
- Hovered: `primary` + `onPrimary` 8% overlay
- Pressed: `primary` + `onPrimary` 12% overlay (ripple)
- Focused: `primary` + focus ring (3dp `primary` outline, 3dp offset)
- Disabled: `onSurface` at 12% background, `onSurface` at 38% text

### Secondary Button (Filled Tonal)
Used for secondary actions: "View Details", "Add Document", "Schedule Visit".

| Property | Value |
|----------|-------|
| Height | 40dp |
| Background | `secondaryContainer` (#BDE9F9) |
| Text color | `onSecondaryContainer` (#001F28) |
| Text style | `labelLarge` |
| Corner radius | 9999dp |
| Ripple color | `onSecondaryContainer` at 12% |

### Outlined Button
Used for tertiary/cancel actions: "Cancel", "Reset Filters", "Back".

| Property | Value |
|----------|-------|
| Height | 40dp |
| Border | 1dp `outline` (#74777F) |
| Background | Transparent |
| Text color | `primary` (#1B5EA6) |
| Text style | `labelLarge` |
| Corner radius | 9999dp |

### Text Button
Used for low-priority actions: "Learn More", "Skip", inline links.

| Property | Value |
|----------|-------|
| Height | 40dp |
| Background | Transparent |
| Text color | `primary` (#1B5EA6) |
| Text style | `labelLarge` |
| Horizontal padding | 12dp |

### Destructive Button
Used for dangerous actions: "Delete Client", "Write Off Loan". Always shows confirmation dialog.

| Property | Value |
|----------|-------|
| Style | Filled button variant |
| Background | `error` (#BA1A1A) |
| Text color | `onError` (#FFFFFF) |
| Prefix icon | `Warning24Regular` |
| Usage | Must always be preceded by confirmation dialog |

---

## 4. Cards

### Client Card
Displays a client summary in the client list.

**Structure**:
```
[Avatar/Initials] [Client Name - titleMedium]    [Status Chip]
                  [Client ID - bodySmall]
                  [Active Loans: N - bodyMedium]  [Amount Due - titleSmall]
```

| Property | Value |
|----------|-------|
| Background | `surfaceContainerLow` |
| Corner radius | 12dp |
| Elevation | 1dp (elevated card) |
| Padding | 16dp |
| Min height | 88dp |
| Width | Full column width - 32dp (16dp screen padding each side) |

**Avatar**:
- Size: 40x40dp
- Shape: Circle (full corner radius)
- Background: `primaryContainer` (#D6E3FF)
- Text: Client initials in `titleMedium`, `onPrimaryContainer` color
- If photo available: Show photo with circular crop

**Status Chip** (trailing, top-right):
- Height: 24dp (display only, not interactive)
- Corner radius: 8dp (small chip)
- See Status Chips section for color mapping

### Loan Card
Displays a loan summary.

**Structure**:
```
[Loan ID - labelSmall/overline]                  [Status Chip]
[Client Name - titleMedium]
[Loan Amount - headlineSmall/weight 500]         [Due Date - bodySmall]
[EMI: $XX.XX - bodyMedium]                       [Remaining: N payments]
```

| Property | Value |
|----------|-------|
| Background | `surfaceContainerLow` |
| Corner radius | 12dp |
| Elevation | 1dp |
| Padding | 16dp |
| Min height | 96dp |

**Amount Display**:
- Loan Amount: `headlineSmall`, `onSurface`, weight 500
- Overdue amounts: `headlineSmall`, `error` color
- Currency symbol: Same style as amount, slightly smaller (use `titleMedium`)

### Collection Card
Displays a scheduled collection for a client visit.

**Structure**:
```
[Visit Time - labelMedium]     [Priority Indicator dot]
[Client Name - titleMedium]
[Collection Amount - titleLarge, weight 500]
[Center Name - bodySmall]      [Distance - bodySmall]
[Collect Button (48dp)]
```

| Property | Value |
|----------|-------|
| Background | `surface` |
| Corner radius | 12dp |
| Border | 1dp `outlineVariant` (not elevated, uses border) |
| Padding | 16dp |
| Min height | 120dp |

### Summary/Stats Card
Used on Dashboard for KPI overview (total collections, pending loans, etc).

**Structure**:
```
[Icon - 24dp, primaryContainer background circle]
[Metric Value - headlineMedium, weight 500]
[Metric Label - bodySmall, onSurfaceVariant]
[Trend indicator (optional) - labelSmall + arrow icon]
```

| Property | Value |
|----------|-------|
| Background | `surfaceContainer` |
| Corner radius | 16dp |
| Elevation | 0dp |
| Padding | 16dp |
| Width | 160dp (2-column grid on compact screen) |

---

## 5. Search Bar

Used on Client List and Loan List screens.

**Docked Search Bar** (within content area):

| Property | Value |
|----------|-------|
| Height | 56dp |
| Background | `surfaceContainerHigh` |
| Corner radius | 9999dp (pill shape) |
| Leading icon | `Search24Regular`, `onSurfaceVariant` |
| Placeholder | "Search clients..." in `bodyLarge`, `onSurfaceVariant` |
| Input text style | `bodyLarge`, `onSurface` |
| Trailing icons | `Filter24Regular` (filter), `Dismiss24Regular` (clear when active) |
| Padding | 16dp horizontal |
| Active border | None (background color change indicates focus) |
| Focused background | `surfaceContainerHighest` |

**Search Suggestions Dropdown**:
- Background: `surfaceContainerHighest`
- Corner radius: 4dp
- Max height: 312dp (5-6 items)
- Item height: 56dp
- Item text: `bodyLarge`
- Divider: 1dp `outlineVariant`

---

## 6. Text Fields

Used for all data entry: client forms, loan entry, payment amounts.

### Outlined Text Field (Standard)

| Property | Value |
|----------|-------|
| Height | 56dp |
| Border | 1dp `outline` (#74777F) |
| Focused border | 2dp `primary` (#1B5EA6) |
| Error border | 2dp `error` (#BA1A1A) |
| Label style | `bodySmall` (12sp) when active, `bodyLarge` (16sp) when empty |
| Label color | `onSurfaceVariant` (default), `primary` (focused) |
| Input text style | `bodyLarge` (16sp) |
| Corner radius | 4dp (xs) |
| Background | Transparent |
| Helper text | `bodySmall`, `onSurfaceVariant`, 4dp below field |
| Error text | `bodySmall`, `error`, 4dp below field |
| Leading icon (optional) | 20dp, `onSurfaceVariant` |
| Trailing icon (optional) | 20dp, `onSurfaceVariant` |

**States**:
- Default: `outline` border, floating label
- Focused: `primary` border (2dp), label moves up and changes to `primary`
- Error: `error` border (2dp), label/helper text turn `error`
- Disabled: `onSurface` at 38% text, `onSurface` at 12% border

### Financial Amount Field
Specialized for currency input.

| Property | Value |
|----------|-------|
| Base style | Outlined Text Field |
| Leading element | Currency symbol ("$", "MKK", etc.) in `titleMedium` |
| Keyboard type | Numeric decimal |
| Input alignment | Right-aligned for amounts |
| Format on blur | Apply comma formatting: "1250.00" → "1,250.00" |
| Validation | Must be > 0, within loan disbursement range |

### Date Field
For loan due dates, visit scheduling.

| Property | Value |
|----------|-------|
| Base style | Outlined Text Field |
| Trailing icon | `Calendar24Regular` opens date picker |
| Format | DD/MM/YYYY or locale-specific |
| Keyboard type | Numeric (for manual entry) |

---

## 7. Dialogs

### Confirmation Dialog
Used for all financial and destructive actions.

**Structure**:
```
[Icon (optional, 24dp)]
[Title - headlineSmall]
[Supporting text - bodyMedium, onSurfaceVariant]
[Divider]
[Cancel Button (text)] [Confirm Button (filled)]
```

| Property | Value |
|----------|-------|
| Background | `surfaceContainerHigh` |
| Corner radius | 28dp |
| Width | Min 280dp, max 560dp |
| Padding | 24dp |
| Title style | `headlineSmall` (24sp) |
| Body style | `bodyMedium` (14sp), `onSurfaceVariant` |
| Elevation | 6dp (level3) |
| Scrim | `scrim` at 32% |
| Button row | Right-aligned, 8dp gap between buttons |

**Financial Confirmation Pattern**:
For payment submission, loan approval - show amount in dialog:
```
"Confirm Payment Collection"
"You are collecting USD 1,250.00 from John Banda.
 This action will be synced when online."
[Cancel]  [Collect Payment]
```

**Destructive Confirmation Pattern**:
```
[Warning icon - error color]
"Delete Client Record?"
"This will permanently delete John Banda and all
 associated loan history. This cannot be undone."
[Cancel]  [Delete - error filled button]
```

### Alert Dialog
For errors, network failures, sync conflicts.

| Property | Value |
|----------|-------|
| Icon | `ErrorCircle24Regular`, `error` color, 24dp |
| Title | `headlineSmall` |
| One button | "OK" or "Retry" (filled primary button) |

---

## 8. Bottom Sheet

### Modal Bottom Sheet
Used for: filter options, quick actions, detail previews.

| Property | Value |
|----------|-------|
| Background | `surfaceContainerLow` |
| Corner radius | 28dp (top corners only) |
| Drag handle | 4dp x 32dp, `onSurfaceVariant` at 40%, centered, 22dp from top |
| Header padding | 16dp horizontal, 16dp top |
| Content padding | 0-16dp horizontal (varies) |
| Max height | 70% of screen height |
| Scrim | `scrim` at 32% |
| Elevation | 1dp |

**Filter Bottom Sheet** (Client/Loan filters):
- Title: "Filter" in `titleLarge`
- Filter groups with dividers
- Apply button: Full-width filled primary button at bottom
- Clear All: Text button above Apply button

**Quick Actions Bottom Sheet** (Long-press on list item):
```
[Client Name - titleMedium]
[Divider]
[View Details - bodyLarge + icon]
[Collect Payment - bodyLarge + icon]
[Add Note - bodyLarge + icon]
[Schedule Visit - bodyLarge + icon]
[Divider]
[Delete - bodyLarge + error color + warning icon]
```

---

## 9. Loading States

### Skeleton Screen
Used for initial content load. Matches the shape of the actual content.

| Property | Value |
|----------|-------|
| Color | `surfaceVariant` (#E0E2EC) |
| Animation | Shimmer left-to-right, 1500ms loop |
| Corner radius | Matches content component corners |

**Client List Skeleton**:
- 5 skeleton client cards
- Each card: avatar circle + 3 text lines of varying widths
- Full-width, 88dp height per card

**Loan Card Skeleton**:
- Loan amount line (60% width, headlineSmall height)
- Client name line (40% width)
- Details row (3 short lines side by side)

### Linear Progress Indicator
Used for determinate operations: sync progress, batch upload.

| Property | Value |
|----------|-------|
| Color | `primary` |
| Track color | `surfaceVariant` |
| Height | 4dp |
| Position | Below top app bar (full width) |

### Circular Progress Indicator
Used for button loading states, inline operations.

| Property | Value |
|----------|-------|
| Size | 24dp (small), 40dp (standard) |
| Color | `primary` (on surface), `onPrimary` (on filled button) |
| Stroke width | 3dp |
| Animation | Continuous rotation |

**Button Loading State**:
- Replace button text with 24dp circular progress (`onPrimary` color)
- Disable button interaction
- Maintain button width (prevent layout shift)

---

## 10. Empty and Error States

### Empty State
Shown when a list has no items.

**Structure**:
```
[Illustration / Large Icon - 80dp]
[Title - headlineSmall]
[Description - bodyMedium, onSurfaceVariant]
[Primary Action Button (optional)]
```

| Property | Value |
|----------|-------|
| Icon size | 80dp |
| Icon color | `onSurfaceVariant` at 60% |
| Title style | `headlineSmall` |
| Description style | `bodyMedium`, `onSurfaceVariant` |
| Max width | 280dp (centered) |
| Vertical position | Center of available space |

**Banking-specific empty states**:

| Screen | Icon | Title | Description |
|--------|------|-------|-------------|
| Client List (no results) | `Person24Regular` | "No clients found" | "Try adjusting your search or filters" |
| Loan List (all clear) | `Money24Regular` | "No active loans" | "All loans are up to date" |
| Collections (done) | `WalletCreditCard24Regular` | "All collected!" | "Great work! No pending collections for today." |
| Offline clients | `CloudOff24Regular` | "No offline data" | "Connect to internet to sync client data" |

### Error State
Shown when a network request fails.

**Structure**:
```
[ErrorCircle icon - 48dp, error color]
[Title - headlineSmall]
[Description - bodyMedium]
[Retry Button - filled primary]
```

| Property | Value |
|----------|-------|
| Icon color | `error` |
| Background | `errorContainer` (subtle) |
| Corner radius | 12dp (if within a card) |

**Error Types**:

| Type | Icon | Title | Action |
|------|------|-------|--------|
| Network error | `CloudOff24Regular` | "Connection failed" | "Retry" button |
| Server error | `ErrorCircle24Regular` | "Something went wrong" | "Try Again" + "Contact Support" |
| Auth expired | `SignOut24Regular` | "Session expired" | "Sign In Again" button |
| Sync conflict | `Warning24Regular` | "Sync conflict detected" | "Resolve Conflicts" button |
| Permission denied | `Warning24Regular` | "Access denied" | "Contact Administrator" |

---

## 11. List Items

### Standard List Item (Client/Loan list rows)

**Single-line**:
```
[Leading (avatar/icon)] [Primary text - titleMedium] [Trailing (metadata)]
```
Height: 56dp

**Two-line**:
```
[Leading] [Primary text - titleMedium]        [Trailing]
          [Secondary text - bodyMedium, onSurfaceVariant]
```
Height: 72dp

**Three-line**:
```
[Leading] [Primary text - titleMedium]        [Trailing]
          [Secondary text line 1 - bodyMedium]
          [Secondary text line 2 - bodySmall, onSurfaceVariant]
```
Height: 88dp

| Property | Value |
|----------|-------|
| Leading element | 40dp avatar, 24dp icon, or 16dp text |
| Leading padding | 16dp from edge |
| Content padding | 16dp from leading |
| Trailing padding | 16dp from edge |
| Divider | 1dp `outlineVariant`, inset 16dp from leading content |
| Ripple | Full width, `primary` at 8% |

### Client List Item (Three-line, banking-specific)
```
[40dp Avatar]  [Client Name - titleMedium]              [Status Chip]
               [ID: #CF-001234 - bodySmall]
               [Loans: 2 | Due: USD 450.00 - bodySmall]  [Due: Mar 20]
```
Height: 88dp

### Loan List Item (Two-line)
```
[Loan icon]  [Client Name - titleMedium]               [Amount - titleMedium]
             [Loan #LN-054321 | Due: Mar 15 - bodySmall] [Status Chip]
```
Height: 72dp

---

## 12. Status Chips

Used throughout the app to convey loan/client status. Display-only (not interactive unless specified).

**Structure**:
```
[Status icon (optional, 16dp)] [Status label - labelSmall, UPPERCASE]
```

| Property | Value |
|----------|-------|
| Height | 24dp (display), 32dp (filter chip) |
| Corner radius | 8dp |
| Horizontal padding | 8dp |
| Label style | `labelSmall` (11sp, weight 500, uppercase) |
| Icon size | 16dp |

**Status Definitions**:

| Status | Background | Text Color | Icon |
|--------|------------|------------|------|
| Active | `primaryContainer` (#D6E3FF) | `onPrimaryContainer` (#001A41) | Filled circle dot |
| Approved | `tertiaryContainer` (#89F8CF) | `onTertiaryContainer` (#002116) | `Checkmark16Regular` |
| Pending | `#FFF8E1` (amber-50) | `#5D4037` (brown) | `Clock16Regular` |
| Overdue | `errorContainer` (#FFDAD6) | `onErrorContainer` (#410002) | `Warning16Regular` |
| Closed | `surfaceVariant` (#E0E2EC) | `onSurfaceVariant` (#44474F) | `Subtract16Regular` |
| Disbursed | `secondaryContainer` (#BDE9F9) | `onSecondaryContainer` (#001F28) | `Money16Regular` |
| Written Off | `errorContainer` (#FFDAD6) | `onErrorContainer` (#410002) | `DismissCircle16Regular` |
| Rejected | `surfaceVariant` (#E0E2EC) | `error` (#BA1A1A) | `Dismiss16Regular` |

**Dark Mode**: All container colors shift to dark M3 equivalents automatically.

---

## 13. Amount Display

A specialized component for displaying financial amounts prominently.

### Large Amount Display
Used for: Total collection target, loan principal, outstanding balance.

```
[Currency Code - labelMedium, onSurfaceVariant]
[Amount - headlineLarge or headlineMedium, weight 700]
[Label - bodySmall, onSurfaceVariant]
```

| Property | Value |
|----------|-------|
| Amount style | `headlineMedium` (28sp) or `headlineLarge` (32sp) |
| Font weight | 700 (bold for financial prominence) |
| Currency code | Left-aligned, `labelMedium`, `onSurfaceVariant` |
| Positive amount | `onSurface` |
| Negative amount | `error` (#BA1A1A) |
| Zero amount | `onSurfaceVariant` |
| Alignment | Right-aligned in list context, Center in card context |

### Inline Amount Display
Used within list items, secondary to client name.

```
[Currency symbol][Amount - titleMedium/titleSmall, weight 500]
```

| Property | Value |
|----------|-------|
| Style | `titleMedium` (16sp) |
| Font weight | 500 |
| Overdue color | `error` |

### Amount Formatting Rules

| Value Range | Format Example |
|-------------|----------------|
| Whole numbers | 1,250 |
| With decimals | 1,250.00 (always 2 decimal places) |
| Large amounts | 1,250,000.00 |
| With currency | USD 1,250.00 or $1,250.00 |
| Negative | -USD 125.00 (red color) |
| Range | USD 500.00 - 1,500.00 |

---

## 14. Offline/Sync Banner

Persistent status notification at the top of the content area (below top app bar).

### Offline Banner

| Property | Value |
|----------|-------|
| Background | `errorContainer` (#FFDAD6) |
| Text color | `onErrorContainer` (#410002) |
| Height | 40dp |
| Icon | `CloudOff20Regular`, leading |
| Text | "You're offline. Changes will sync when connected." |
| Text style | `labelMedium` |
| Dismissible | No (auto-dismisses when back online) |

### Pending Sync Banner

| Property | Value |
|----------|-------|
| Background | `primaryContainer` (#D6E3FF) |
| Text color | `onPrimaryContainer` (#001A41) |
| Height | 40dp |
| Icon | `ArrowSync20Regular` (animated spin) |
| Text | "Syncing 5 changes..." |
| Action | "View" text button (opens sync queue) |

### Sync Success Snackbar
Appears briefly (3 seconds) when sync completes.

| Property | Value |
|----------|-------|
| Background | `inverseSurface` (#2E3036) |
| Text color | `inverseOnSurface` (#EFF0F7) |
| Text | "All changes synced" |
| Icon | `CloudCheckmark20Regular`, `inversePrimary` color |
| Duration | 3000ms |
| Position | Bottom, 8dp above bottom navigation |

---

## Component Usage Summary

| Component | Primary Screen | Key Consideration |
|-----------|---------------|-------------------|
| Top App Bar | All screens | Sync status icon always visible |
| Bottom Navigation | All main screens | Badge on Collections for daily count |
| Client Card | Client List | 3-line for info density |
| Loan Card | Loan List | Highlight overdue in error color |
| Collection Card | Collections | CTA button must be 48dp+ |
| Status Chip | Everywhere | Never use color alone |
| Amount Display | Loans, Collections | Always 2 decimal places |
| Skeleton Screen | All data loads | Match exact content shape |
| Empty State | All list screens | Banking-specific copy and icons |
| Confirmation Dialog | All financial actions | Required before submit |
| Offline Banner | All screens | Auto-managed via connectivity |
