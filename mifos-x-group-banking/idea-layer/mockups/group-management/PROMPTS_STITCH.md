# Group Management — Stitch Prompts

---

## 1. Design System Context

### Project Identity
App name: CommonPurse
Platform: Android (Kotlin Multiplatform Mobile — Compose UI)
Design system: Material Design 3
Font family: Noto Sans (all weights)
Scale style: Large — scaled up for low-vision rural users in East Africa
Color mode: Light (primary surfaces) with full dark-mode token set available
Density: Comfortable — extra breathing room between elements

### Color Tokens — Light Mode (complete hex set)

**Primary role**
- primary: #2E7D32 (deep VSLA-green — growth, trust)
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6 (pale green — header backgrounds)
- onPrimaryContainer: #002106 (near-black green — text on pale green)
- inversePrimary: #8BD68F (for dark surfaces)

**Secondary role**
- secondary: #FF8F00 (warm amber — shared coin, harvest)
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3 (pale amber — cycle chips, member chips)
- onSecondaryContainer: #2A1700 (dark brown — text on amber chips)

**Tertiary role**
- tertiary: #1565C0 (trust-blue — informational chips, savings totals)
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF (pale blue — offline notice banners)
- onTertiaryContainer: #001C39 (deep navy — text on offline banners)

**Error role**
- error: #D32F2F (material red — corpus block, arrears indicators)
- onError: #FFFFFF
- errorContainer: #FFDAD6 (pale red — corpus block banner background)
- onErrorContainer: #410002 (deep red — corpus block banner text)

**Surface role**
- background: #FFFFFF
- onBackground: #1A1C19 (near-black — primary body text)
- surface: #FAFAFA (near-white — card backgrounds)
- onSurface: #1A1C19
- surfaceVariant: #DEE5DA (grey-green — shimmer backgrounds, dividers)
- onSurfaceVariant: #424942 (medium grey — supporting text, subtitles)
- outline: #727971 (grey — borders, inactive indicators)
- outlineVariant: #C2C9BD (pale grey — dividers)
- scrim: #000000 (bottom sheet scrim)
- inverseSurface: #2F312D
- inverseOnSurface: #F0F1EB

**Health indicator colors (semantic, not M3 roles)**
- GREEN badge background: #C8E6C9 — text: #1B5E20
- AMBER badge background: #FFF9C4 — text: #E65100
- RED badge background: #FFCDD2 — text: #B71C1C

**Role chip colors**
- CHAIRPERSON chip: background #A6F1A6 (primaryContainer) — text #002106 (onPrimaryContainer)
- TREASURER chip: background #FFDDB3 (secondaryContainer) — text #2A1700 (onSecondaryContainer)
- SECRETARY chip: background #D2E4FF (tertiaryContainer) — text #001C39 (onTertiaryContainer)
- MEMBER chip: background #DEE5DA (surfaceVariant) — text #424942 (onSurfaceVariant)

### Color Tokens — Dark Mode (complete hex set)
- primary: #8BD68F — onPrimary: #003910 — primaryContainer: #00531A — onPrimaryContainer: #A6F1A6
- secondary: #FFB95C — onSecondary: #472A00 — secondaryContainer: #653E00 — onSecondaryContainer: #FFDDB3
- tertiary: #9FCAFF — onTertiary: #00325B — tertiaryContainer: #004A82 — onTertiaryContainer: #D2E4FF
- error: #FFB4AB — onError: #690005 — errorContainer: #93000A — onErrorContainer: #FFDAD6
- background: #1A1C19 — onBackground: #E2E3DD
- surface: #121412 — onSurface: #E2E3DD
- surfaceVariant: #424942 — onSurfaceVariant: #C2C9BD
- outline: #8C9388 — outlineVariant: #424942

### Typography Scale (Noto Sans, all sizes in sp)

| Role | Size (sp) | Line Height (sp) | Tracking (sp) | Weight |
|------|-----------|-----------------|---------------|--------|
| displayLarge | 57 | 64 | -0.25 | 400 |
| displayMedium | 45 | 52 | 0 | 400 |
| displaySmall | 36 | 44 | 0 | 400 |
| headlineLarge | 32 | 40 | 0 | 400 |
| headlineMedium | 28 | 36 | 0 | 400 |
| headlineSmall | 24 | 32 | 0 | 400 |
| titleLarge | 22 | 28 | 0 | 500 |
| titleMedium | 16 | 24 | 0.15 | 500 |
| titleSmall | 14 | 20 | 0.1 | 500 |
| bodyLarge | 16 | 24 | 0.5 | 400 |
| bodyMedium | 14 | 20 | 0.25 | 400 |
| bodySmall | 12 | 16 | 0.4 | 400 |
| labelLarge | 14 | 20 | 0.1 | 500 |
| labelMedium | 12 | 16 | 0.5 | 500 |
| labelSmall | 11 | 16 | 0.5 | 500 |

### Spacing Scale (dp values)
- xxs: 2dp
- xs: 4dp
- sm: 8dp
- md: 12dp
- lg: 16dp (default card padding, standard spacing unit)
- xl: 24dp (large section gaps)
- xxl: 32dp (screen-edge margins on medium breakpoint)
- 3xl: 48dp
- 4xl: 64dp

### Shape Tokens (cornerRadius)
- none: 0dp
- extra_small: 4dp (chips, badges)
- small: 8dp (search bar suggestion rows)
- medium: 12dp (group list cards, shimmer, chips in list)
- large: 16dp (dashboard section cards, wizard review card)
- extra_large: 28dp (FAB, extended FAB)
- full: 9999dp (circular avatars, circular photo pickers)

### Elevation (shadow + tonal overlay)
- level_0: 0dp shadow, 0.00 tonal alpha (flat: headers)
- level_1: 1dp shadow, 0.05 tonal alpha (subtle raised)
- level_2: 3dp shadow, 0.08 tonal alpha (group list cards)
- level_3: 6dp shadow, 0.11 tonal alpha (dropdowns, sheets)
- level_4: 8dp shadow, 0.12 tonal alpha (corpus card — elevated emphasis)
- level_5: 12dp shadow, 0.14 tonal alpha (navigation bars)

### Motion Tokens
Durations (ms):
- short_1: 50ms (micro feedback — ripple start)
- short_2: 100ms (button label crossfade)
- short_3: 150ms (chip appear, validation error fade-in)
- short_4: 200ms (card press scale, ripple complete)
- medium_1: 250ms (banner slide-in)
- medium_2: 300ms (wizard step slide, list item enter)
- medium_3: 350ms (screen enter shared element)
- medium_4: 400ms (screen exit)
- long_1: 450ms (bottom sheet expand)
- long_2: 500ms (full-screen transitions)

Easing curves:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0) — for most transitions
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0) — emphasis transforms
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0) — elements entering screen
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0) — elements exiting screen

### Accessibility Constraints
- Minimum touch target: 48dp (standard interactive elements)
- Primary CTA touch target: 56dp (filled buttons, FAB, quick action buttons)
- Contrast normal text: 4.5:1 minimum (WCAG AA)
- Contrast large text (≥18sp): 3.0:1 minimum
- Focus ring: 3dp, color primaryContainer (#A6F1A6)
- TalkBack: all cards, buttons, and interactive elements require contentDescription

---

## 2. Screen Layouts

### Screen: GroupListScreen

**Route**: `/groups`
**Composable**: `GroupListScreen(viewModel: GroupListViewModel)`
**Full layout tree** (Compose pseudo-hierarchy):

```
Scaffold(
  topBar = TopAppBar(
    title = "My Groups",                          // titleMedium 16sp not — actually CenterAlignedTopAppBar uses headlineSmall
    backgroundColor = #2E7D32,
    contentColor = #FFFFFF,
    actions = [
      IconButton(icon = notifications, contentDescription = "Notifications", size = 48dp)
    ],
    modifier = windowInsetsPadding(top)
  ),
  floatingActionButton = ExtendedFloatingActionButton(
    text = "New Group",
    icon = Icons.Add,
    containerColor = #2E7D32,
    contentColor = #FFFFFF,
    shape = RoundedCornerShape(28dp),             // extra_large
    modifier = size(min=56dp),
    onClick = { OnCreateGroup }
  )
) {
  Column(
    modifier = fillMaxSize + padding(horizontal=0dp, vertical=0dp)
  ) {
    // Search bar — always visible
    SearchBar(
      query = searchQuery,
      placeholder = "Search groups…",
      modifier = fillMaxWidth + padding(horizontal=16dp, vertical=8dp),
      shape = RoundedCornerShape(28dp),
      elevation = 2dp,
      backgroundColor = #FAFAFA,
      trailingIcon = if (searchQuery.isNotEmpty) X_icon else null,
      onQueryChange = { OnSearch(it) },
      onClearSearch = { OnClearSearch }
    )

    // Content area switches on screenState
    when (screenState) {
      Loading -> LazyColumn(modifier = fillMaxWidth + padding(horizontal=16dp)) {
        items(5) { ShimmerGroupCard(height=88dp, cornerRadius=12dp, color=#DEE5DA) }
      }

      Content -> LazyColumn(
        modifier = fillMaxWidth,
        contentPadding = PaddingValues(horizontal=16dp, vertical=8dp),
        verticalArrangement = spacedBy(12dp)
      ) {
        items(filteredGroups, key = { it.id }) { group ->
          GroupCard(
            group = group,
            modifier = fillMaxWidth + clickable { OnGroupClick(group.id) }
          )
        }
      }

      Empty -> Box(modifier = fillMaxSize, contentAlignment = Center) {
        EmptyState(icon = group_off, title = "No groups yet",
          body = "Create your first savings group to get started.",
          cta = "Create Group", onCta = { OnCreateGroup })
      }

      Error -> Box(modifier = fillMaxSize, contentAlignment = Center) {
        ErrorState(icon = cloud_off, title = "Could not load groups",
          body = error.message, cta = "Retry", onCta = { Retry })
      }
    }
  }
}
```

**GroupCard internal layout** (Card, cornerRadius=12dp, elevation=2dp, bg=#FAFAFA, padding=16dp, minTouchTarget=72dp):

```
Column(modifier = fillMaxWidth + padding(16dp)) {
  Row(horizontalArrangement = SpaceBetween, verticalAlignment = CenterVertically) {
    Text(group.name, style=titleMedium, color=#1A1C19, modifier = weight(1f))
    HealthBadge(status=group.healthIndicator)   // chip, cornerRadius=4dp
  }
  Spacer(height=4dp)
  Row(horizontalArrangement = spacedBy(8dp)) {
    Chip("Cycle ${group.cycleNumber}", bg=#FFDDB3, text=#2A1700, cornerRadius=4dp)
    Text("${group.memberCount} members", style=bodySmall, color=#424942)
  }
  Spacer(height=4dp)
  Text("Last met: ${group.lastMeetingDate}", style=bodySmall, color=#424942)
}
```

Health badge colors:
- GREEN: bg=#C8E6C9, text=#1B5E20, dot circle ●
- AMBER: bg=#FFF9C4, text=#E65100, dot circle ●
- RED: bg=#FFCDD2, text=#B71C1C, dot circle ●

---

### Screen: GroupDashboardScreen

**Route**: `/groups/{groupId}`
**Composable**: `GroupDashboardScreen(groupId: String, viewModel: GroupDashboardViewModel)`

**Full layout tree**:

```
Scaffold(
  topBar = TopAppBar(
    title = group.name,                           // headlineSmall 24sp truncated
    navigationIcon = IconButton(arrow_back, "Back", { OnBack }),
    actions = [IconButton(more_vert, "More options", { OnMoreOptions })],
    backgroundColor = #2E7D32, contentColor = #FFFFFF
  )
) {
  when (screenState) {
    Loading -> LazyColumn(padding=16dp, verticalArrangement=spacedBy(16dp)) {
      items(4) { ShimmerCard(height=120dp, cornerRadius=16dp, color=#DEE5DA) }
    }

    Content -> LazyColumn(
      modifier = fillMaxSize,
      contentPadding = PaddingValues(bottom=24dp),
      verticalArrangement = spacedBy(0dp)          // sections are flush then spaced inside
    ) {
      // 1. Group Header — no card border, flush with app bar
      item {
        GroupHeaderSection(group=group, modifier=fillMaxWidth)
      }
      // 2. Corpus Card — elevated card
      item {
        CorpusCard(
          corpus=corpus, isInsufficient=isCorpusInsufficient,
          modifier=fillMaxWidth + padding(16dp)
        )
      }
      // 3. Corpus Blocked Banner (conditional)
      if (isCorpusInsufficient) {
        item { CorpusBlockedBanner(modifier=fillMaxWidth + padding(horizontal=16dp)) }
      }
      // 4. Quick Actions
      item { QuickActionsSection(isCycleEnd=isCycleEnd, modifier=fillMaxWidth + padding(16dp)) }
      // 5. Savings Summary
      item { SavingsSummaryCard(config=config, accounts=accounts, modifier=fillMaxWidth + padding(horizontal=16dp)) }
      // 6. Activity Feed
      item { ActivityFeedSection(activities=recentActivity, modifier=fillMaxWidth + padding(16dp)) }
    }

    Error -> Box(fillMaxSize, Center) {
      ErrorState(icon=cloud_off, title="Could not load group",
        body=error.message, cta="Retry", onCta={ Retry })
    }
  }
}
```

**GroupHeaderSection** (bg=#A6F1A6, padding=16dp, elevation=0dp):
```
Column(padding = 16dp, bg = #A6F1A6) {
  Text(group.name, style=headlineSmall 24sp, color=#002106, maxLines=2)
  Spacer(4dp)
  Text("Cycle ${group.cycleNumber} of ${group.cycleLengthMonths} months • ${group.meetingFrequency} meetings",
    style=bodyMedium 14sp, color=#002106)
  Spacer(8dp)
  Row(spacedBy=8dp) {
    Chip("${group.memberCount} members", bg=#FFDDB3, text=#2A1700)
    Chip(
      "${group.overdueLoansCount} overdue",
      bg = if (overdueLoansCount > 0) #FFDAD6 else #DEE5DA,
      text = if (overdueLoansCount > 0) #410002 else #424942
    )
  }
}
```

**CorpusCard** (bg=#FAFAFA, cornerRadius=16dp, elevation=8dp, padding=20dp):
```
Card(cornerRadius=16dp, elevation=8dp, modifier=fillMaxWidth + padding(horizontal=16dp)) {
  Column(padding=20dp) {
    Text("Corpus Fund", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(8dp)
    Text("KES ${corpus.currentBalance.formatted}",
      style=displaySmall 36sp/400, color=#2E7D32)
    Spacer(16dp)
    Row(arrangement=SpaceEvenly) {
      StatColumn(label="Opening Balance", value="KES ${corpus.openingBalance.formatted}")
      StatColumn(label="Contributions", value="KES ${corpus.totalContributionsThisCycle.formatted}")
      StatColumn(label="Loans Out", value="KES ${corpus.totalLoansOutstanding.formatted}")
    }
  }
}
```
When insufficient: card border = 2dp #D32F2F.

**QuickActionsSection** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
Card(cornerRadius=16dp, elevation=2dp) {
  Column(padding=16dp) {
    Text("Quick Actions", style=titleSmall 14sp, color=#424942)
    Spacer(12dp)
    Row(arrangement=spacedBy(12dp)) {
      Column(weight=1f) {
        FilledButton("Start Meeting", icon=meeting_room, bg=#2E7D32, text=#FFFFFF,
          modifier=fillMaxWidth + height(56dp), onClick={ OnStartMeeting })
        Spacer(12dp)
        OutlinedButton("Loans", icon=account_balance, borderColor=#2E7D32, text=#2E7D32,
          modifier=fillMaxWidth + height(56dp), onClick={ OnViewLoans })
      }
      Column(weight=1f) {
        OutlinedButton("Members", icon=group, borderColor=#2E7D32, text=#2E7D32,
          modifier=fillMaxWidth + height(56dp), onClick={ OnViewMembers })
        Spacer(12dp)
        OutlinedButton("Share-Out", icon=share,
          borderColor = if (isCycleEnd) #FF8F00 else #727971,
          text = if (isCycleEnd) #FF8F00 else #424942,
          enabled = isCycleEnd,
          modifier=fillMaxWidth + height(56dp), onClick={ OnShareOut })
      }
    }
  }
}
```

**SavingsSummaryCard** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
Card {
  Column(padding=16dp) {
    Text("Savings Summary", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(8dp)
    Text("Mandatory contribution: KES ${config.contributionMin.toInt()} – KES ${config.contributionMax.toInt()} per meeting",
      style=bodyMedium 14sp, color=#424942)
    Spacer(8dp)
    Text("KES ${accounts.savingsBalance.formatted} total",
      style=titleLarge 22sp/500, color=#1565C0)
  }
}
```

**ActivityFeedSection** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
Card {
  Column(padding=16dp) {
    Text("Recent Activity", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(8dp)
    activities.forEach { activity ->
      ListItem(
        leadingContent = { ActivityIcon(type=activity.type) },
        headlineContent = { Text(activity.description, style=bodyMedium 14sp, color=#1A1C19) },
        supportingContent = { Text("${activity.date} • ${activity.memberName ?: ""}", style=bodySmall 12sp, color=#424942) },
        trailingContent = if (activity.amount != null) {
          Text("KES ${activity.amount.formatted}", style=labelLarge 14sp, color=#2E7D32)
        },
        modifier = fillMaxWidth + minHeight(56dp)
      )
    }
  }
}
```

---

### Screen: GroupCreateScreen (3-step wizard)

**Route**: `/groups/create`
**Composable**: `GroupCreateScreen(viewModel: GroupCreateViewModel)`

**Full scaffold**:
```
Scaffold(
  topBar = TopAppBar(
    title = "New Group", titleStyle=titleMedium,
    navigationIcon = IconButton(close, "Discard and close", { OnBack }),
    backgroundColor = #2E7D32, contentColor = #FFFFFF
  )
) {
  Column(fillMaxSize) {
    StepIndicator(currentStep=currentStep, totalSteps=3, labels=["Identity", "Rules", "Review"],
      activeColor=#2E7D32, completedColor=#FF8F00, inactiveColor=#727971,
      modifier=fillMaxWidth + padding(horizontal=16dp, vertical=12dp))

    // Scrollable content area
    Box(modifier=fillMaxSize.weight(1f)) {
      when (currentStep) {
        1 -> GroupIdentityStep(state=state, errors=validationErrors)
        2 -> GroupRulesStep(state=state, errors=validationErrors)
        3 -> GroupReviewStep(state=state, isOffline=isOffline)
      }
    }

    // Sticky bottom navigation row
    Column(modifier=fillMaxWidth + padding(horizontal=16dp, vertical=12dp)) {
      if (currentStep == 3) {
        FilledButton("Create Group", loading=isSubmitting,
          bg=#2E7D32, text=#FFFFFF, modifier=fillMaxWidth + height(56dp), onClick={ OnSubmit })
      } else {
        FilledButton("Next", bg=#2E7D32, text=#FFFFFF,
          modifier=fillMaxWidth + height(56dp), onClick={ OnNextStep })
      }
      if (currentStep > 1) {
        TextButton("Back", color=#2E7D32, modifier=fillMaxWidth + height(48dp), onClick={ OnPreviousStep })
      }
    }
  }
}
```

**Step 1 content** (GroupIdentityStep):
```
LazyColumn(contentPadding = PaddingValues(horizontal=16dp), verticalArrangement=spacedBy(12dp)) {
  item { OutlinedTextField(label="Group Name *", placeholder="e.g. Mwangaza Women's Group",
    helper="3–60 characters", maxLength=60, minHeight=56dp,
    isError=validationErrors["groupName"] != null,
    errorText=validationErrors["groupName"]) }
  item { ExposedDropdownMenuBox(label="Office *", placeholder="Select office",
    options=officeList.map{it.name}, minHeight=56dp,
    isError=validationErrors["officeId"] != null) }
  item { ExposedDropdownMenuBox(label="Currency *", options=["KES","USD","UGX","TZS"],
    selected="KES", minHeight=56dp) }
  item { ExposedDropdownMenuBox(label="Meeting Day *",
    options=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    minHeight=56dp, isError=validationErrors["meetingDay"] != null) }
  item { TimePickerField(label="Meeting Time *", minHeight=56dp,
    isError=validationErrors["meetingTime"] != null) }
}
```

**Step 2 content** (GroupRulesStep):
```
LazyColumn(contentPadding=PaddingValues(horizontal=16dp), verticalArrangement=spacedBy(12dp)) {
  item { OutlinedTextField(label="Min Contribution (KES) *", placeholder="e.g. 100",
    keyboard=numeric, minHeight=56dp, isError=validationErrors["contributionMin"] != null) }
  item { OutlinedTextField(label="Max Contribution (KES) *", placeholder="e.g. 500",
    keyboard=numeric, minHeight=56dp) }
  item { OutlinedTextField(label="Loan Multiplier (×savings) *", placeholder="e.g. 3",
    helper="Member can borrow up to X times their total savings",
    keyboard=numeric, minHeight=56dp) }
  item { OutlinedTextField(label="Interest Rate (%) *", placeholder="e.g. 10",
    helper="Flat interest rate per loan cycle",
    keyboard=numeric, minHeight=56dp) }
  item { OutlinedTextField(label="Cycle Length (months) *", placeholder="e.g. 12",
    keyboard=numeric, minHeight=56dp) }
  item { OutlinedTextField(label="Late Penalty / Fine (KES) *", placeholder="e.g. 50",
    helper="Fine charged for missing minimum contribution — FR-020",
    keyboard=numeric, minHeight=56dp) }
}
```

**Step 3 content** (GroupReviewStep):
```
LazyColumn(contentPadding=PaddingValues(horizontal=16dp, vertical=8dp)) {
  item {
    Card(bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=20dp) {
      Column {
        Text("Review Group Details", style=titleMedium 16sp/500, color=#1A1C19)
        Spacer(16dp)
        SectionLabel("Identity")
        ReviewRow("Name", groupName)
        ReviewRow("Office", officeName)
        ReviewRow("Currency", currency)
        ReviewRow("Meeting", "$meetingDay at $meetingTime")
        Spacer(12dp)
        SectionLabel("Rules")
        ReviewRow("Contribution", "KES $contributionMin – KES $contributionMax")
        ReviewRow("Loan Multiplier", "${loanMultiplier}× savings")
        ReviewRow("Interest Rate", "$interestRate% flat")
        ReviewRow("Cycle Length", "$cycleLengthMonths months")
        ReviewRow("Late Fine", "KES $fineAmount")
        if (isOffline) {
          Spacer(12dp)
          OfflineBanner("You are offline. This group will be created when you reconnect.",
            bg=#D2E4FF, text=#001C39, icon=wifi_off)
        }
      }
    }
  }
}
```

---

## 3. Component Specifications

### TopAppBar (GroupListScreen)
- Type: CenterAlignedTopAppBar
- Height: 64dp (plus window inset top)
- Background: #2E7D32
- Title: "My Groups", style=titleLarge 22sp/500, color=#FFFFFF, centered
- Action: IconButton, icon=notifications, tint=#FFFFFF, touchTarget=48dp
- Elevation: 0dp (flat against screen edge), surface tint disabled
- Scroll behavior: enterAlways (collapses on scroll down, re-enters on scroll up)

### TopAppBar (GroupDashboard + GroupCreate)
- Type: SmallTopAppBar
- Height: 56dp
- Background: #2E7D32
- Navigation icon: arrow_back (dashboard) / close (create), tint=#FFFFFF, touchTarget=48dp
- Title: group.name (dashboard) / "New Group" (create), truncated with ellipsis at 1 line
- Actions: more_vert (dashboard), none (create)

### SearchBar
- Type: DockedSearchBar (Material 3)
- Height: 48dp, width: fillMaxWidth − 32dp horizontal padding
- Corner radius: 28dp (pill shape)
- Background: #FAFAFA, elevation: 2dp
- Placeholder: "Search groups…", style=bodyMedium 14sp, color=#727971
- Leading icon: search, tint=#727971, size=24dp
- Trailing icon: cancel (shown only when query.isNotEmpty), tint=#424942
- Active state: border 1dp #2E7D32 on focus
- Input text: bodyMedium 14sp, color=#1A1C19

### GroupCard
- Type: ElevatedCard
- Width: fillMaxWidth
- Min height: 88dp (72dp content + 16dp padding each side)
- Corner radius: 12dp
- Elevation: 2dp (level_2: shadow 3dp)
- Background: #FAFAFA
- Padding: 16dp all sides
- Ripple: bounded, color=#2E7D32 at 12% opacity, duration=200ms
- Press state: scale 1.0 → 0.98 → 1.0 (spring stiffness=400)
- Content:
  - Row 1: group.name (titleMedium 16sp/500, #1A1C19) + HealthBadge (right-aligned)
  - Row 2: Cycle chip + member count text
  - Row 3: Last meeting date text
  - Spacing between rows: 4dp

### HealthBadge
- Type: AssistChip (non-interactive, label only)
- Corner radius: 4dp (extra_small)
- Height: 24dp
- Padding: horizontal 8dp, vertical 4dp
- Typography: labelMedium 12sp/500
- GREEN: bg=#C8E6C9, text=#1B5E20
- AMBER: bg=#FFF9C4, text=#E65100
- RED: bg=#FFCDD2, text=#B71C1C

### ExtendedFAB (Group List)
- Type: ExtendedFloatingActionButton
- Height: 56dp, min width: 80dp
- Corner radius: 28dp (extra_large)
- Background: #2E7D32
- Icon: add, tint=#FFFFFF, size=24dp
- Label: "New Group", style=labelLarge 14sp/500, color=#FFFFFF
- Position: Alignment.BottomEnd, margin=16dp from screen edges
- Expanded: shows icon + label. Collapsed (on scroll down): shows icon only
- Scroll threshold to collapse: 200dp scrolled
- Expand animation: 300ms standard easing, icon stays, label fades in
- Shadow: elevation level_3 (6dp)

### ShimmerGroupCard
- Width: fillMaxWidth
- Height: 88dp
- Corner radius: 12dp
- Background: animated gradient #DEE5DA → #C2C9BD → #DEE5DA, animates left-to-right
- Animation: cycle duration 1200ms, infinitely repeating
- Spacing between shimmer items: 12dp

### CorpusCard
- Type: ElevatedCard
- Corner radius: 16dp (large)
- Elevation: 8dp (level_4)
- Background: #FAFAFA
- Padding: 20dp
- Border: normally 0dp. When isCorpusInsufficient=true: 2dp solid #D32F2F
- Title: "Corpus Fund", titleMedium 16sp/500, #1A1C19
- Balance: "KES X,XXX", displaySmall 36sp/400, #2E7D32. Formatted with thousand separators.
- Stat row: 3 equal-width StatColumn items, bodyMedium 14sp
  - Labels: "Opening Balance", "Contributions", "Loans Out" — labelSmall 11sp, #424942
  - Values: KES amounts — bodyMedium 14sp, #1A1C19

### CorpusBlockedBanner
- Type: M3 Banner (inline, not dismissible)
- Height: auto (min 52dp)
- Background: #FFDAD6 (errorContainer)
- Icon: warning_amber, tint=#D32F2F, size=24dp
- Message: "Loan disbursement is blocked — corpus balance is below minimum threshold."
  - style=bodyMedium 14sp, color=#410002 (onErrorContainer)
- Margin: horizontal 16dp, vertical 8dp
- Corner radius: 8dp (small)
- Appear animation: slide down + fade in, 250ms medium_1 duration, decelerated easing

### QuickActionButton (Start Meeting — Filled)
- Type: FilledButton
- Height: 56dp, width: fillMaxWidth of column
- Corner radius: 12dp (medium)
- Background: #2E7D32
- Text: "Start Meeting", labelLarge 14sp/500, color=#FFFFFF
- Icon: meeting_room, tint=#FFFFFF, size=18dp, left of text, gap=8dp
- Ripple: bounded white at 20% opacity
- Disabled: background=#DEE5DA, text=#424942 (never disabled in current design)
- Loading: CircularProgressIndicator 16dp white replaces icon

### QuickActionButton (Members/Loans/Share-Out — Outlined)
- Type: OutlinedButton
- Height: 56dp, width: fillMaxWidth of column
- Corner radius: 12dp
- Border: 1dp — active: #2E7D32; Share-Out at cycle-end: #FF8F00; disabled: #727971
- Text color: active #2E7D32; Share-Out at cycle-end: #FF8F00; disabled: #424942
- Icons: group (Members), account_balance (Loans), share (Share-Out)
- Disabled state (Share-Out mid-cycle): alpha 0.38 on all content

### StepIndicator
- Type: custom row composable
- Total steps: 3
- Active step dot: filled circle 16dp, bg=#2E7D32
- Completed step dot: filled circle 16dp, bg=#FF8F00, checkmark icon 10dp white
- Inactive step dot: outlined circle 16dp, border=#C2C9BD, bg=transparent
- Connecting line: 2dp, completed segments=#FF8F00, future segments=#C2C9BD
- Step labels: labelSmall 11sp/500, active=#2E7D32, completed=#FF8F00, inactive=#727971
- Spacing: step dots centered above labels; horizontal distribution=SpaceEvenly

### ReviewRow
- Type: Row
- Height: 32dp
- Label: bodySmall 12sp, color=#727971, width=120dp fixed
- Value: bodyMedium 14sp, color=#1A1C19, weight=1f
- Divider: 0.5dp #C2C9BD below each row

### OfflineBanner
- Type: M3 Card (no elevation)
- Background: #D2E4FF (tertiaryContainer)
- Icon: wifi_off, tint=#1565C0, size=20dp
- Text: bodySmall 12sp, color=#001C39
- Padding: 12dp, corner radius: 8dp
- Appears when isOffline=true in step 3; not dismissible

### OutlinedTextField (GroupCreate)
- Type: M3 OutlinedTextField
- Min height: 56dp
- Corner radius: 4dp (standard M3 text field shape)
- Idle border: 1dp #727971
- Focused border: 2dp #2E7D32
- Error border: 2dp #D32F2F
- Label: floats above on focus/value present, labelMedium 12sp
- Placeholder: bodyMedium 14sp, #727971
- Helper text: bodySmall 12sp, #424942
- Error text: bodySmall 12sp, #D32F2F
- Keyboard types: numeric fields use KeyboardType.Decimal; name/text fields use KeyboardType.Text
- Character counter: shown on groupName field only (60 max)

### EmptyState
- Icon: group_off (Material), 80dp, tint=#727971
- Title: headlineSmall 24sp/400, #1A1C19, centered
- Body: bodyMedium 14sp/400, #424942, centered, maxLines=3
- CTA: OutlinedButton, borderColor=#2E7D32, text=#2E7D32
- Vertical arrangement: centered with 16dp gaps
- Top offset: 20% from center (visually balanced)

### ErrorState
- Icon: cloud_off (Material), 64dp, tint=#727971
- Title: titleLarge 22sp/500, #1A1C19
- Body: bodyMedium 14sp, #424942
- CTA: FilledButton, bg=#2E7D32, text=#FFFFFF
- Same spacing rules as EmptyState

---

## 4. Interaction Patterns

### Group List Load Sequence
1. Screen enters: GroupListScreen composable launches, GroupListViewModel.init() called
2. isLoading=true: shimmer list renders (5 cards × 88dp), TopAppBar and SearchBar visible
3. API call: GET /centers?staffId={id}&paged=true&limit=20&offset=0
4. Shimmer duration: shimmer animates for up to 3000ms; replaced immediately when data arrives
5. Success: isLoading=false, groups populated. Shimmer fades out (100ms, accelerated). LazyColumn fades in (150ms, decelerated) with staggered item entry: each item slides up 8dp + fades in with 50ms delay per item.
6. Empty: EmptyState component fades in (200ms) centered in available space.
7. Error: ErrorState component fades in (200ms).

### Search Interaction
1. User taps SearchBar: keyboard opens, SearchBar gains focus, border turns 1dp #2E7D32
2. User types: each keystroke fires OnSearch(query) with 150ms debounce
3. Filtering: filteredGroups = groups.filter { name.contains(query, ignoreCase=true) }
4. List updates: LazyColumn uses key-based diffing; items slide out (150ms) and remaining items reorder (200ms standard easing)
5. No extra API call — client-side only
6. Clear icon appears when query.isNotEmpty; tap fires OnClearSearch, query="", list returns to full
7. Empty search result: inline text "No results for '${query}'" — bodyMedium 14sp, #424942, centered in list area

### Pull to Refresh
1. User pulls list down by 80dp: M3 pull indicator appears at top, #2E7D32 color
2. User releases: indicator completes rotation (200ms), isRefreshing=true
3. API called with invalidate_cache=true (bypasses stale-while-revalidate)
4. Indicator dismisses after data arrives (fade out 200ms)
5. List items re-render with fresh data

### FAB Collapse on Scroll
1. LazyColumn scroll offset increases past 200dp: FAB collapses
2. Collapse animation: 300ms standard easing. Label text fades out (short_2 100ms), FAB width shrinks to 56dp (icon only)
3. Scroll direction reverses (user scrolls up): FAB extends, label fades in 300ms
4. FAB never collapses when list is in empty or error state

### Dashboard Parallel API Load
1. GroupDashboardViewModel.init() called with groupId from nav params
2. Four coroutines launched in parallel: get_center, get_center_accounts, get_group_corpus, get_group_config
3. isLoading=true: 4× shimmer cards (h=120dp) shown
4. As each call returns, partial state updates — shimmer replaced only when ALL calls complete (or one fails)
5. compute_derived_state:
   - isCorpusInsufficient = corpus.currentBalance < config.minimumDisbursementThreshold
   - isCycleEnd = group.cycleWeek == group.cycleLengthWeeks
6. Content fades in (200ms) with cards staggered 50ms apart

### Corpus Insufficient State Transition
1. isCorpusInsufficient changes false → true
2. CorpusCard border animates: transparent → #D32F2F, 300ms standard easing
3. CorpusBlockedBanner animates in: height 0 → auto (slide down 250ms) + opacity 0 → 1 (fade 250ms), decelerated easing
4. Share-Out button style does not change (it's gated by isCycleEnd, not corpus)
5. Analytics event: corpus_block_triggered (group_id, balance)

### Wizard Step Advance
1. User taps "Next": OnNextStep action fires
2. Validate current step synchronously:
   - For each required field with empty value: add to validationErrors map
   - For each field violating numeric constraints: add specific error message
3. If validationErrors.isNotEmpty: animate invalid fields (border transitions to #D32F2F 150ms, error text slides down + fades in 150ms)
4. If valid: remove existing errors (fade out 100ms), StepIndicator dot fills (#FF8F00, 200ms), content slides left to next step (300ms standard easing)
5. Back button: content slides right (300ms), step indicator reverts

### Group Create Submit
1. User taps "Create Group" on step 3: OnSubmit fires
2. isSubmitting=true: button label "Create Group" fades out (100ms), CircularProgressIndicator 16dp white fades in (100ms). All fields in step 3 become disabled.
3. NetworkMonitor.isOnline check:
   - Online: POST /centers → on success: POST /datatables/dt_group_config/{centerId}
     - On success: NavigateToGroupDashboard event emitted (navigate with groupId)
   - Offline: enqueue SyncQueueItem(operation=CREATE_GROUP), emit ShowOfflineSyncDialog. Dialog: "Group queued for sync — it will be created when you reconnect." Dismiss → NavigateBack to group list.
4. Error: isSubmitting=false, button restores. Snackbar: error.message. Step 3 remains open.

### Back / Discard
1. User taps close icon or system back from group-create: OnBack fires
2. If any field has content: DiscardConfirmationDialog: "Discard new group?" [Cancel] [Discard]
   - Discard: navigate back to group-list with slide-right exit (300ms)
   - Cancel: dismiss dialog
3. If all fields empty: navigate back immediately

---

## 5. Content Data

### Demo Group: Mwangaza Women's Group

**Group identity**:
- Name: Mwangaza Women's Group
- Fineract Center ID: 101
- Office: Nairobi Head Office (officeId=1)
- Currency: KES (Kenyan Shilling)
- Cycle number: 1
- Cycle length: 12 months
- Meeting frequency: Weekly on Monday at 09:00
- Status: Active
- Activation date: 15 January 2026
- Member count: 5
- Overdue loans count: 0
- Health indicator: GREEN (overdueRate: 0.00)
- Last meeting date: 28 April 2026

**Corpus fund (real-time)**:
- Current balance: KES 47,500.00
- Opening balance (cycle start): KES 0.00
- Total contributions this cycle: KES 52,500.00
- Total loans outstanding: KES 5,000.00
- Last updated: 2026-04-28

**Group config**:
- Minimum contribution per meeting: KES 100.00
- Maximum contribution per meeting: KES 500.00
- Loan multiplier: 3× member savings
- Interest rate: 10% flat per loan cycle
- Cycle length months: 12
- Fine amount (late/missed contribution): KES 50.00
- Minimum disbursement threshold: KES 5,000.00

**Group accounts**:
- Total savings balance: KES 52,500.00
- Total loans outstanding: KES 5,000.00
- Active loan count: 1

**isCorpusInsufficient**: false (KES 47,500 > KES 5,000 threshold)
**isCycleEnd**: false (cycle 1, week 16 of 52)

### Demo Group: Tumaini Savings Circle

- Name: Tumaini Savings Circle
- Cycle number: 3
- Member count: 12
- Last meeting date: 25 April 2026
- Health indicator: AMBER (overdueRate: 0.12 — 12% of loans overdue)
- Status: Active

### Recent Activity Feed (Mwangaza Women's Group)

Activity item 1:
- Type: MEETING
- Description: Meeting #4 conducted
- Date: 2026-04-28
- Member name: All members
- Amount: null

Activity item 2:
- Type: DEPOSIT
- Description: Savings deposit received
- Member name: Amara Diallo
- Amount: KES 500.00
- Date: 2026-04-28

Activity item 3:
- Type: DEPOSIT
- Description: Savings deposit received
- Member name: Grace Mwangi
- Amount: KES 300.00
- Date: 2026-04-28

Activity item 4:
- Type: DEPOSIT
- Description: Savings deposit received
- Member name: Fatima Ouedraogo
- Amount: KES 400.00
- Date: 2026-04-28

Activity item 5:
- Type: LOAN
- Description: Loan disbursed
- Member name: Amara Diallo
- Amount: KES 5,000.00
- Date: 2026-04-21

Activity item 6:
- Type: MEETING
- Description: Meeting #3 conducted
- Date: 2026-04-21
- Member name: All members
- Amount: null

### Group Create Demo Entry (Step-through values)

Step 1:
- Group Name: Solidarity Mothers Group
- Office: Mombasa Branch (officeId=2)
- Currency: KES
- Meeting Day: Wednesday
- Meeting Time: 10:00

Step 2:
- Minimum Contribution: KES 150
- Maximum Contribution: KES 600
- Loan Multiplier: 3
- Interest Rate: 10%
- Cycle Length: 12 months
- Late Fine: KES 50

Step 3 review: all values shown as entered above. isOffline=false. No offline banner displayed.

### Office List (for dropdown)

- id: 1, name: Nairobi Head Office
- id: 2, name: Mombasa Branch
- id: 3, name: Kisumu Field Office
- id: 4, name: Nakuru Community Center

### Validation Error Messages (real strings from i18n)

- groupName (empty): "Group name is required."
- groupName (too short): "Group name must be at least 3 characters."
- officeId (null): "Please select an office."
- meetingDay (empty): "Please select a meeting day."
- meetingTime (empty): "Please select a meeting time."
- contributionMin (empty or zero): "Minimum contribution is required."
- contributionMax (less than min): "Maximum must be greater than minimum contribution."
- loanMultiplier (out of range): "Loan multiplier must be between 1 and 10."
- interestRate (out of range): "Interest rate must be between 0% and 100%."
- cycleLengthMonths (out of range): "Cycle length must be between 1 and 60 months."
- fineAmount (negative): "Fine amount cannot be negative."

---

## 6. Responsive Rules

### Compact Layout (0–599dp width — phones, most target devices)

**GroupListScreen**:
- Horizontal padding: 16dp
- Group cards: full width (single column)
- FAB: ExtendedFloatingActionButton, collapses to icon-only on scroll
- SearchBar: full width minus 32dp (horizontal padding 16dp each side)
- Bottom nav: visible, 5 items, height=80dp, selected tab = Groups
- Top app bar: CenterAligned style

**GroupDashboardScreen**:
- All cards: full width, 16dp horizontal padding
- Group header: full-width banner (no rounded corners, flush with app bar)
- Quick actions: 2-column grid (each column weight=1f, gap=12dp)
- Savings summary + activity feed: full-width cards
- LazyColumn itemSpacing: 0dp (sections defined by card padding)

**GroupCreateScreen**:
- All form fields: full width, 16dp horizontal padding
- Step indicator: horizontal row, labels visible
- Bottom button area: sticky at bottom (height=56dp button + 48dp optional back + 24dp vertical padding)

**Navigation**:
- Bottom navigation bar visible on group-list and group-dashboard
- group-create: no bottom nav (full-screen wizard, close button to exit)

---

### Medium Layout (600–839dp width — foldables, small tablets)

**GroupListScreen**:
- Horizontal padding: 32dp each side (xxl spacing)
- Group cards: still single column but narrower available width
- FAB: always extended (never collapses — more screen space)
- Top padding for content below search bar: 8dp → 12dp

**GroupDashboardScreen**:
- Group header: card with cornerRadius=16dp (matches other cards; not flush)
- Corpus card + Quick Actions row: side-by-side in Row (weight 0.45f + 0.55f)
- Savings summary + Activity feed: side-by-side Row (weight 0.5f + 0.5f)
- LazyColumn replaced by LazyVerticalGrid columns=2 for card sections

**GroupCreateScreen**:
- Form fields: max width 480dp, centered horizontally
- Step indicator: same 3-step row layout

**Navigation**:
- Navigation rail replaces bottom navigation (left edge, 72dp width)
- Groups icon with label below; rail selection = Groups section

---

### Expanded Layout (840dp+ — tablets, landscape foldables, desktop)

**GroupListScreen**:
- Two-column layout: left panel = group list (max 400dp), right panel = group-dashboard detail pane
- Navigation: persistent NavigationDrawer (240dp) on left edge
- Group card list in left panel: single column, no FAB — "New Group" button in drawer header
- Group dashboard: renders in right panel with full GroupDashboardContent composable
- On first load: no group selected — right panel shows "Select a group to view details" placeholder

**GroupDashboardScreen** (embedded in right panel, expanded):
- Corpus card + Quick Actions: Row layout, side by side
- Savings summary + Activity: Row layout, side by side
- No separate route needed — detail panel renders inline
- Back button in top bar becomes hidden (left panel navigation handles it)

**GroupCreateScreen** (expanded, dialog or drawer):
- Rendered as a modal bottom sheet (sheet width=480dp, centered) or Dialog
- Step indicator: horizontal, same 3 steps
- All form fields: max 480dp, centered in dialog

**Navigation** (expanded):
- NavigationDrawer: 240dp, permanent, left edge
- Items: Groups (selected), Members, Meetings, Loans, Settings
- No bottom nav or navigation rail

---

### Grid System

**Compact**:
- Columns: 4 (base)
- Margin: 16dp (lg)
- Gutter: 8dp (sm)
- Card spans: 4 columns (full width)
- Quick action grid: 2 columns (2-span each)

**Medium**:
- Columns: 8
- Margin: 32dp (xxl)
- Gutter: 12dp (md)
- Card spans: 8 columns (full width) or 4-4 split

**Expanded**:
- Columns: 12
- Margin: 32dp
- Gutter: 16dp (lg)
- Left panel (group list): 4 columns (33%)
- Right panel (dashboard): 8 columns (67%)
- Card spans: varied (4, 6, 8)

---

### Orientation: Landscape on Phone (compact height)

- GroupListScreen: SearchBar becomes compact (height reduces to 40dp), group cards maintain same width
- GroupDashboardScreen: LazyColumn continues to scroll vertically; corpus card height reduces to minimum
- GroupCreateScreen: form fields scroll vertically, sticky button row stays at bottom
- Minimum screen height for comfortably usable wizard: 400dp (group-create renders all step 1 fields in compact mode)

---

### Typography Scaling (Dynamic Type / system font scale)

- All sizes defined in sp (scale-independent pixels)
- At system font scale 1.0: all sp values as specified in design tokens
- At system font scale 1.3 (accessibility setting): all text scales up proportionally
- Comfortable density spacing absorbs text reflow; cards expand in height to accommodate
- displaySmall (36sp at scale 1.0 = 46.8dp at 1.3) on corpus card: card auto-expands in height
- All containers use wrapContentHeight — no fixed height on text containers

---

### Dark Mode Toggle

- Color roles flip to dark palette (full dark token set in Section 1)
- Primary: #2E7D32 → #8BD68F (light green on dark)
- Surface: #FAFAFA → #121412
- Shimmer: #DEE5DA → #424942
- Health badge GREEN: bg=#003910, text=#A6F1A6 (dark mode inversion)
- Corpus balance: color=primary → #8BD68F in dark mode
- All transitions between light/dark: instant (system animation handles it)
- App-level: follows system setting; manual override in Settings screen (v1.0.0)

---

### Analytics Events (Group Management — all screens)

**GroupListScreen analytics**:
- Screen view: `group_list_viewed` — logged on composition, no params
- Group card tap: `group_selected` — params: { group_id: String, health_status: "GREEN"|"AMBER"|"RED" }
- FAB tap: `create_group_initiated` — no params
- Search input: `group_search_performed` — params: { query_length: Int }
- Pull to refresh: `group_list_refreshed` — no params
- Error state shown: `group_list_error` — params: { error_type: String }

**GroupDashboardScreen analytics**:
- Screen view: `group_dashboard_viewed` — params: { group_id: String }
- Start Meeting tap: `meeting_started` — params: { group_id: String, corpus_balance: Double }
- Members tap: `member_list_opened` — params: { group_id: String }
- Loans tap: `loan_list_opened` — params: { group_id: String }
- Share-Out tap: `share_out_initiated` — params: { group_id: String, cycle_end: Boolean }
- Share-Out blocked (mid-cycle): `share_out_blocked` — params: { group_id: String, week: Int, total_weeks: Int }
- Corpus block banner shown: `corpus_block_triggered` — params: { group_id: String, balance: Double, threshold: Double }
- Pull to refresh: `group_dashboard_refreshed` — params: { group_id: String }

**GroupCreateScreen analytics**:
- Screen view: `group_create_viewed` — no params
- Step advance: `group_create_step_advanced` — params: { step: Int, from_step: Int }
- Validation error: `group_create_validation_error` — params: { step: Int, fields: List\<String\> }
- Submit tap: `group_create_submitted` — params: { is_offline: Boolean }
- Offline queue: `group_create_queued_offline` — no params
- Success: `group_created` — params: { group_id: String, cycle_months: Int, office_id: Long }
- Discard: `group_create_discarded` — params: { step: Int }

---

### i18n String Keys (Group Management — complete set)

**GroupListScreen**:
- `screen_title` → "My Groups"
- `search_placeholder` → "Search groups…"
- `cycle_label` → "Cycle {{n}}"
- `members_label` → "{{n}} members"
- `last_met_label` → "Last met: {{date}}"
- `fab_label` → "New Group"
- `empty_title` → "No groups yet"
- `empty_body` → "Create your first savings group to get started."
- `empty_cta` → "Create Group"
- `error_network` → "No internet connection. Showing cached data."
- `error_server` → "Server error. Please try again."
- `error_auth` → "Session expired. Please log in again."
- `health_green` → "Healthy"
- `health_amber` → "At Risk"
- `health_red` → "Critical"

**GroupDashboardScreen**:
- `corpus_label` → "Corpus Fund"
- `corpus_blocked` → "Loan disbursement is blocked — corpus balance is below minimum threshold."
- `quick_actions_label` → "Quick Actions"
- `start_meeting` → "Start Meeting"
- `view_members` → "Members"
- `view_loans` → "Loans"
- `share_out` → "Share-Out"
- `savings_label` → "Savings Summary"
- `contribution_range` → "Mandatory contribution: KES {{min}} – KES {{max}} per meeting"
- `activity_label` → "Recent Activity"
- `error_not_found` → "Group not found."
- `share_out_not_available` → "Share-Out is only available at the end of the cycle."

**GroupCreateScreen**:
- `screen_title` → "New Group"
- `step_identity` → "Identity"
- `step_rules` → "Rules"
- `step_review` → "Review"
- `field_name` → "Group Name"
- `field_office` → "Office"
- `field_currency` → "Currency"
- `field_meeting_day` → "Meeting Day"
- `field_meeting_time` → "Meeting Time"
- `field_contribution_min` → "Min Contribution (KES)"
- `field_contribution_max` → "Max Contribution (KES)"
- `field_loan_multiplier` → "Loan Multiplier (×savings)"
- `field_interest_rate` → "Interest Rate (%)"
- `field_cycle_length` → "Cycle Length (months)"
- `field_fine_amount` → "Late Penalty / Fine (KES)"
- `btn_next` → "Next"
- `btn_back` → "Back"
- `btn_submit` → "Create Group"
- `offline_notice` → "You are offline. This group will be created when you reconnect."
- `error_validation` → "Please fix the highlighted fields."

---

### Offline Sync Strategy (Group Management)

**SyncQueue entries for group-management operations**:

CREATE_GROUP entry:
```json
{
  "id": "sq-001",
  "entityType": "GROUP",
  "operation": "CREATE_GROUP",
  "payload": {
    "name": "Solidarity Mothers Group",
    "officeId": 2,
    "staffId": 42,
    "active": true,
    "activationDate": "06 May 2026",
    "locale": "en",
    "dateFormat": "dd MMMM yyyy",
    "meetingFrequency": "1",
    "meetingDay": "WE"
  },
  "status": "PENDING",
  "createdAt": "2026-05-06T10:30:00Z",
  "retryCount": 0,
  "lastError": null
}
```

CREATE_GROUP_CONFIG entry (chained, runs after CREATE_GROUP success):
```json
{
  "id": "sq-002",
  "entityType": "GROUP_CONFIG",
  "operation": "CREATE_GROUP_CONFIG",
  "dependsOn": "sq-001",
  "payload": {
    "contribution_min": 150.0,
    "contribution_max": 600.0,
    "loan_multiplier": 3.0,
    "interest_rate": 10.0,
    "cycle_length_months": 12,
    "fine_amount": 50.0
  },
  "status": "PENDING",
  "createdAt": "2026-05-06T10:30:00Z",
  "retryCount": 0,
  "lastError": null
}
```

**Retry strategy**: exponential backoff starting at 30s, max 4 retries, max delay 10 minutes.

**SyncStatus screen indicator**: when pending ops exist for group-management, a sync icon badge appears on the group list toolbar. Tapping navigates to the sync-status screen which shows pending/synced/failed operations.

**Conflict resolution**: if CREATE_GROUP already created on server but config write failed, the config write retries independently using the stored centerId. Duplicate detection: if 409 conflict received on CREATE_GROUP, the local record is updated with the server's resourceId.

---

### Accessibility Trees (TalkBack Annotations)

**GroupListScreen**:

GroupCard (Mwangaza Women's Group):
```
contentDescription = "Mwangaza Women's Group. Cycle 1. 5 members. Last met April 28, 2026. Health: Healthy."
role = Button
clickLabel = "Open group dashboard"
```

FAB:
```
contentDescription = "Create new savings group"
role = Button
```

SearchBar:
```
contentDescription = "Search groups by name"
role = SearchField
hint = "Search groups…"
```

Health badge (GREEN):
```
contentDescription = "Health: Healthy"
role = Image (decorative chip)
```

**GroupDashboardScreen**:

CorpusCard (sufficient):
```
contentDescription = "Corpus Fund. Current balance: KES 47,500. Opening balance: KES 0. Contributions this cycle: KES 52,500. Loans outstanding: KES 5,000."
role = Article (non-interactive section)
```

CorpusBlockedBanner:
```
contentDescription = "Warning: Loan disbursement is blocked. Corpus balance is below minimum threshold."
role = Alert
liveRegion = Polite (announced when it appears)
```

StartMeetingButton:
```
contentDescription = "Start meeting for Mwangaza Women's Group"
role = Button
```

ShareOutButton (disabled):
```
contentDescription = "Share-Out — not available until end of cycle"
role = Button
enabled = false
```

**GroupCreateScreen**:

StepIndicator:
```
role = ProgressBar
contentDescription = "Step ${currentStep} of 3, ${stepName}"
```

GroupNameField:
```
role = TextField
label = "Group Name"
hint = "3 to 60 characters"
errorMessage = (if error) "Group name must be at least 3 characters"
```

SubmitButton (step 3):
```
contentDescription = "Create group — review complete"
role = Button
```

OfflineBanner:
```
contentDescription = "Offline notice: group will be queued and created when you reconnect"
role = Alert
liveRegion = Polite
```

---

### Testing Hooks (test tags for UI tests)

**GroupListScreen**:
- `testTag("group_list_screen")` on root Scaffold
- `testTag("search_bar")` on SearchBar
- `testTag("group_card_${group.id}")` on each GroupCard
- `testTag("health_badge_${group.id}")` on each HealthBadge
- `testTag("create_group_fab")` on FAB
- `testTag("shimmer_list")` on shimmer container
- `testTag("empty_state")` on EmptyState
- `testTag("error_state")` on ErrorState
- `testTag("retry_button")` on error retry CTA

**GroupDashboardScreen**:
- `testTag("group_dashboard_screen")` on root
- `testTag("corpus_card")` on CorpusCard
- `testTag("corpus_blocked_banner")` on CorpusBlockedBanner (may not exist if sufficient)
- `testTag("start_meeting_button")` on Start Meeting button
- `testTag("view_members_button")` on Members button
- `testTag("view_loans_button")` on Loans button
- `testTag("share_out_button")` on Share-Out button
- `testTag("savings_summary_card")` on SavingsSummaryCard
- `testTag("activity_feed")` on ActivityFeedSection

**GroupCreateScreen**:
- `testTag("group_create_screen")` on root
- `testTag("step_indicator")` on StepIndicator
- `testTag("group_name_field")` on group name text field
- `testTag("office_dropdown")` on office dropdown
- `testTag("contribution_min_field")` on min contribution field
- `testTag("contribution_max_field")` on max contribution field
- `testTag("loan_multiplier_field")` on multiplier field
- `testTag("next_button")` on Next button
- `testTag("back_step_button")` on Back button
- `testTag("submit_button")` on Create Group button
- `testTag("review_card")` on review card
- `testTag("offline_banner")` on offline notice banner
