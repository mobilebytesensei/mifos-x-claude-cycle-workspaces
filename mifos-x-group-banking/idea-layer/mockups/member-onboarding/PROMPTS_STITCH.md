# Member Onboarding — Stitch Prompts

---

## 1. Design System Context

### Project Identity
App name: CommonPurse
Platform: Android (Kotlin Multiplatform Mobile — Compose UI)
Design system: Material Design 3
Font family: Noto Sans (all weights; Google Fonts)
Scale style: Large — scaled up for low-vision rural users in East Africa (Kenya, Uganda, Tanzania, West Africa)
Color mode: Light (primary surfaces) with full dark-mode token set available
Density: Comfortable — extra breathing room between elements; 8dp extra vertical padding versus M3 standard

### Color Tokens — Light Mode (complete hex set)

**Primary role — VSLA Green (#2E7D32)**
- primary: #2E7D32 (deep green — growth, trust, nature of savings)
- onPrimary: #FFFFFF (white text/icons on green)
- primaryContainer: #A6F1A6 (pale mint green — header backgrounds, sparkline fill)
- onPrimaryContainer: #002106 (near-black green — text on pale mint, maximum contrast)
- inversePrimary: #8BD68F (light green for dark surfaces)

**Secondary role — Amber (#FF8F00)**
- secondary: #FF8F00 (warm amber — TREASURER role color, shared coin/harvest symbolism)
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3 (pale amber — TREASURER list chip background, avatar fallback)
- onSecondaryContainer: #2A1700 (dark brown on pale amber)

**Tertiary role — Trust Blue (#1565C0)**
- tertiary: #1565C0 (trust-blue — SECRETARY role color, informational, attendance)
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF (pale blue — SECRETARY list chip, offline banners)
- onTertiaryContainer: #001C39 (deep navy text on pale blue)

**Error role — Material Red**
- error: #D32F2F (active loan arrears indicator, validation errors)
- onError: #FFFFFF
- errorContainer: #FFDAD6 (loan arrears banner background)
- onErrorContainer: #410002 (deep red — arrears banner text, maximum contrast)

**Surface role**
- background: #FFFFFF
- onBackground: #1A1C19 (near-black — body text)
- surface: #FAFAFA (near-white — card backgrounds)
- onSurface: #1A1C19
- surfaceVariant: #DEE5DA (grey-green — shimmer, dividers, MEMBER chip, photo placeholder)
- onSurfaceVariant: #424942 (medium grey — supporting text, subtitles, savings label)
- outline: #727971 (inactive borders, inactive indicators)
- outlineVariant: #C2C9BD (pale grey — row dividers)
- scrim: #000000 (bottom sheet scrim at 32% opacity)
- inverseSurface: #2F312D — inverseOnSurface: #F0F1EB

**Role chip colors (member list — chip/badge style)**
- CHAIRPERSON chip: bg=#A6F1A6 (primaryContainer), text=#002106 (onPrimaryContainer)
- TREASURER chip: bg=#FFDDB3 (secondaryContainer), text=#2A1700 (onSecondaryContainer)
- SECRETARY chip: bg=#D2E4FF (tertiaryContainer), text=#001C39 (onTertiaryContainer)
- MEMBER chip: bg=#DEE5DA (surfaceVariant), text=#424942 (onSurfaceVariant)

**Role chip colors (member profile — filled badge style)**
- CHAIRPERSON: bg=#2E7D32 (primary), text=#FFFFFF (onPrimary)
- TREASURER: bg=#FF8F00 (secondary), text=#FFFFFF (onSecondary)
- SECRETARY: bg=#1565C0 (tertiary), text=#FFFFFF (onTertiary)
- MEMBER: bg=#DEE5DA, text=#424942

**Loan status badge colors**
- ACTIVE: bg=#C8E6C9, text=#1B5E20 (healthy green)
- NONE: bg=#DEE5DA, text=#424942 (neutral grey)
- OVERDUE: bg=#FFCDD2, text=#B71C1C (alert red)

### Color Tokens — Dark Mode (complete hex set)
- primary: #8BD68F — onPrimary: #003910 — primaryContainer: #00531A — onPrimaryContainer: #A6F1A6
- secondary: #FFB95C — onSecondary: #472A00 — secondaryContainer: #653E00 — onSecondaryContainer: #FFDDB3
- tertiary: #9FCAFF — onTertiary: #00325B — tertiaryContainer: #004A82 — onTertiaryContainer: #D2E4FF
- error: #FFB4AB — onError: #690005 — errorContainer: #93000A — onErrorContainer: #FFDAD6
- background: #1A1C19 — onBackground: #E2E3DD
- surface: #121412 — onSurface: #E2E3DD
- surfaceVariant: #424942 — onSurfaceVariant: #C2C9BD
- outline: #8C9388 — outlineVariant: #424942

### Typography Scale (Noto Sans, all sizes in sp, large scale)

| Role | Size (sp) | Line Height (sp) | Tracking (sp) | Weight | Compose style |
|------|-----------|-----------------|---------------|--------|---------------|
| displayLarge | 57 | 64 | -0.25 | 400 | MaterialTheme.typography.displayLarge |
| displayMedium | 45 | 52 | 0 | 400 | .displayMedium |
| displaySmall | 36 | 44 | 0 | 400 | .displaySmall |
| headlineLarge | 32 | 40 | 0 | 400 | .headlineLarge |
| headlineMedium | 28 | 36 | 0 | 400 | .headlineMedium |
| headlineSmall | 24 | 32 | 0 | 400 | .headlineSmall |
| titleLarge | 22 | 28 | 0 | 500 | .titleLarge |
| titleMedium | 16 | 24 | 0.15 | 500 | .titleMedium |
| titleSmall | 14 | 20 | 0.1 | 500 | .titleSmall |
| bodyLarge | 16 | 24 | 0.5 | 400 | .bodyLarge |
| bodyMedium | 14 | 20 | 0.25 | 400 | .bodyMedium |
| bodySmall | 12 | 16 | 0.4 | 400 | .bodySmall |
| labelLarge | 14 | 20 | 0.1 | 500 | .labelLarge |
| labelMedium | 12 | 16 | 0.5 | 500 | .labelMedium |
| labelSmall | 11 | 16 | 0.5 | 500 | .labelSmall |

All font weights using Noto Sans: Regular=400, Medium=500, SemiBold=600 (not used), Bold=700 (not in M3 scale)

### Spacing Scale (dp values — comfortable density)
- xxs: 2dp (icon internal gap)
- xs: 4dp (chip internal padding, row item gap within a group)
- sm: 8dp (between sections within a card, chip-to-chip gap)
- md: 12dp (between list item content rows, card-to-card gap)
- lg: 16dp (standard card padding, horizontal page padding)
- xl: 24dp (between major sections)
- xxl: 32dp (horizontal margins on medium+ breakpoints)
- 3xl: 48dp (large page top padding)
- 4xl: 64dp (hero section heights)

### Shape Tokens (cornerRadius dp)
- none: 0dp — not used in member onboarding
- extra_small: 4dp — badges, loan status chips
- small: 8dp — role chips in list, inline banners
- medium: 12dp — list item containers
- large: 16dp — profile section cards, photo source sheet list items
- extra_large: 28dp — FAB, top corners of bottom sheets
- full: 9999dp — circular avatars (48dp list, 80dp profile), photo picker area (120dp)

### Elevation (shadow + tonal overlay on surface)
- level_0: 0dp, 0.00 alpha — member profile header (flat, flush with app bar color band)
- level_1: 1dp, 0.05 alpha — subtle surface separation
- level_2: 3dp, 0.08 alpha — all profile section cards (savings, loan, attendance)
- level_3: 6dp, 0.11 alpha — bottom sheets, dropdowns
- level_4: 8dp, 0.12 alpha — elevated emphasis (not used in member onboarding)
- level_5: 12dp, 0.14 alpha — navigation bars

### Motion Tokens (durations in ms)
- short_1: 50ms — ripple start, micro hover
- short_2: 100ms — button label crossfade, icon swap
- short_3: 150ms — validation error animation, chip appear
- short_4: 200ms — card press scale, ripple complete, badge update
- medium_1: 250ms — banner appear
- medium_2: 300ms — list item enter, swipe action reveal
- medium_3: 350ms — screen enter, shared element
- medium_4: 400ms — screen exit
- long_1: 450ms — bottom sheet expand, sheet dismiss
- long_2: 500ms — sparkline draw animation start delay, full-screen transitions

Easing curves:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0) — default for most UI transitions
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0) — role chip update, sparkline draw
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0) — elements entering screen (sheet expand, cards fade in)
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0) — elements exiting (sheet dismiss)

### Accessibility Constraints
- Minimum touch target: 48dp (standard interactive elements, list items)
- Primary CTA touch target: 56dp (Save Member button, FAB)
- List row minimum touch height: 72dp (member list items)
- Contrast ratio — normal text (≤18sp/14sp bold): 4.5:1 minimum
- Contrast ratio — large text (>18sp or bold>14sp): 3.0:1 minimum
- Focus ring: 3dp, color=#A6F1A6 (primaryContainer)
- TalkBack: all avatars, role chips, badges, interactive elements require contentDescription
- All form fields labelled via `semantics { contentDescription }` or OutlinedTextField label
- Sparkline: alternative text description of trend (increasing/decreasing/flat)

### Special-Purpose Colors
**Sparkline chart**:
- Line stroke: #2E7D32 (primary), 2dp thick
- Fill gradient: #A6F1A6 (primaryContainer) at 40% opacity → transparent at bottom
- Data point dots: 4dp filled circle, #2E7D32
- Chart background: transparent (card bg shows through)

**Attendance progress bar**:
- Track: #DEE5DA (surfaceVariant)
- Indicator color logic:
  - attendanceRate ≥ 0.80: #1565C0 (tertiary — high attendance, positive)
  - attendanceRate ≥ 0.60 and < 0.80: #FF8F00 (secondary — moderate, watch)
  - attendanceRate < 0.60: #D32F2F (error — low attendance, alert)

---

## 2. Screen Layouts

### Screen: MemberListScreen

**Route**: `/groups/{groupId}/members`
**Composable**: `MemberListScreen(groupId: String, viewModel: MemberListViewModel)`

**Full layout tree** (Compose pseudo-hierarchy):
```
Scaffold(
  topBar = TopAppBar(
    title = Column {
      Text("Members", style=titleLarge 22sp/500, color=#FFFFFF)
      Text(groupName, style=labelMedium 12sp/500, color=#FFFFFF.copy(alpha=0.8f))
    },
    navigationIcon = IconButton(arrow_back, "Back to group dashboard", { OnBack }, size=48dp),
    backgroundColor = #2E7D32, contentColor = #FFFFFF
  ),
  floatingActionButton = ExtendedFloatingActionButton(
    text = "Add Member",
    icon = Icons.person_add,
    containerColor = #2E7D32, contentColor = #FFFFFF,
    shape = RoundedCornerShape(28dp),
    modifier = height(56dp),
    onClick = { OnAddMember }
  )
) { paddingValues ->
  when (screenState) {
    Loading -> LazyColumn(
      modifier = fillMaxSize.padding(paddingValues),
      contentPadding = PaddingValues(horizontal=0dp),
      verticalArrangement = spacedBy(0dp)
    ) {
      items(6) { ShimmerMemberRow(height=72dp, cornerRadius=4dp, color=#DEE5DA) }
    }

    Content -> LazyColumn(
      modifier = fillMaxSize.padding(paddingValues),
      contentPadding = PaddingValues(bottom=88dp),   // space above FAB
    ) {
      items(members, key = { it.id }) { member ->
        SwipeableListItem(
          member = member,
          onTap = { OnMemberClick(member.id) },
          onSwipe = { OnMemberClick(member.id) }
        )
        Divider(color = #C2C9BD, thickness = 0.5.dp, startIndent = 80dp)
      }
      if (isLoadingMore) {
        item {
          LinearProgressIndicator(
            modifier = fillMaxWidth + height(4dp),
            color = #2E7D32,
            trackColor = #DEE5DA
          )
        }
      }
    }

    Empty -> Box(fillMaxSize.padding(paddingValues), Center) {
      EmptyState(
        icon = group_add, iconSize = 80dp, iconTint = #727971,
        title = "No members yet", titleStyle = headlineSmall 24sp, titleColor = #1A1C19,
        body = "Add the first member to this group.", bodyStyle = bodyMedium 14sp, bodyColor = #424942,
        cta = "Add Member", ctaStyle = OutlinedButton, ctaBorderColor = #2E7D32, ctaTextColor = #2E7D32,
        onCta = { OnAddMember }
      )
    }

    Error -> Box(fillMaxSize.padding(paddingValues), Center) {
      ErrorState(
        icon = cloud_off, iconSize = 64dp, iconTint = #727971,
        title = "Could not load members", body = error.message,
        cta = "Retry", onCta = { Retry }
      )
    }
  }
}
```

**SwipeableListItem internal** (using Modifier.swipeable or RevealSwipe library):
```
Box(modifier = fillMaxWidth + minHeight(72dp)) {
  // Background action (visible when swiped)
  Box(
    modifier = fillMaxSize + background(color=#A6F1A6),
    contentAlignment = CenterStart
  ) {
    Row(modifier = padding(start=16dp), verticalAlignment = CenterVertically) {
      Icon(person, tint=#002106, size=24dp)
      Spacer(8dp)
      Text("View Profile", style=bodyMedium 14sp, color=#002106)
    }
  }

  // Foreground content (the list item)
  ListItem(
    leadingContent = {
      MemberAvatar(member=member, size=48dp)
    },
    headlineContent = {
      Text(member.displayName, style=bodyLarge 16sp, color=#1A1C19, maxLines=1)
    },
    supportingContent = {
      Text("Savings: KES ${member.savingsBalance.formatted}", style=bodySmall 12sp, color=#424942)
    },
    trailingContent = {
      Column(horizontalAlignment = End, verticalArrangement = spacedBy(4dp)) {
        RoleChip(role=member.role)      // small chip h=24dp
        LoanStatusBadge(status=member.loanStatus)  // small badge h=20dp
      }
    },
    modifier = fillMaxWidth + minHeight(72dp) + clickable { OnMemberClick(member.id) },
    colors = ListItemDefaults.colors(containerColor = #FAFAFA)
  )
}
```

**MemberAvatar** (48dp for list, 80dp for profile):
```
Box(size=dp, shape=CircleShape) {
  if (member.photoUri != null) {
    AsyncImage(url=member.photoUri, contentScale=Crop, modifier=fillMaxSize)
  } else {
    Box(fillMaxSize, bg=avatarBgColor(member.role)) {
      Text(member.displayName.initials(), style=titleMedium 16sp/500, color=avatarTextColor(member.role))
    }
  }
}
```

Avatar background color by role (list size):
- CHAIRPERSON: bg=#A6F1A6, text=#002106
- TREASURER: bg=#FFDDB3, text=#2A1700
- SECRETARY: bg=#D2E4FF, text=#001C39
- MEMBER: bg=#DEE5DA, text=#424942

---

### Screen: MemberProfileScreen

**Route**: `/groups/{groupId}/members/{memberId}`
**Composable**: `MemberProfileScreen(memberId: String, groupId: String, viewModel: MemberProfileViewModel)`

**Full layout tree**:
```
Scaffold(
  topBar = SmallTopAppBar(
    title = "Member Profile",
    navigationIcon = IconButton(arrow_back, "Back to member list", { OnBack }),
    backgroundColor = #2E7D32, contentColor = #FFFFFF
  ),
  bottomBar = null
) { paddingValues ->
  when (screenState) {
    Loading -> LazyColumn(padding = paddingValues) {
      items(4) { ShimmerCard(height=100dp, cornerRadius=16dp, color=#DEE5DA) }
    }

    Content -> LazyColumn(
      modifier = fillMaxSize.padding(paddingValues),
      contentPadding = PaddingValues(bottom=24dp),
      verticalArrangement = spacedBy(0dp)
    ) {
      // Header — flush with app bar (no card, bg=primaryContainer)
      item { MemberHeaderSection(member=member, role=role,
        isChairperson=isCurrentUserChairperson, onEditRole={ OnEditRole }) }

      // Savings History card
      item {
        SavingsHistoryCard(
          balance=accounts.savingsBalance,
          history=accounts.savingsHistory,
          modifier=fillMaxWidth + padding(horizontal=16dp, top=16dp)
        )
      }

      // Active Loan card (conditional)
      if (accounts.activeLoan != null) {
        item {
          ActiveLoanCard(
            loan=accounts.activeLoan,
            modifier=fillMaxWidth + padding(horizontal=16dp, top=12dp)
          )
        }
      }

      // Attendance card
      item {
        AttendanceCard(
          attended=meetingsAttended, total=totalMeetings, rate=attendanceRate,
          modifier=fillMaxWidth + padding(horizontal=16dp, top=12dp, bottom=0dp)
        )
      }
    }

    Error -> ErrorState(error=error, onRetry={ Retry })
  }

  // Role edit bottom sheet (overlaid)
  if (isEditingRole) {
    ModalBottomSheet(
      onDismissRequest = { OnDismissRoleEdit },
      sheetState = rememberModalBottomSheetState(skipPartiallyExpanded=true),
      containerColor = #FAFAFA,
      shape = RoundedCornerShape(topStart=28dp, topEnd=28dp)
    ) {
      RoleEditSheetContent(selectedRole=selectedRole, isUpdating=isUpdatingRole,
        onRoleSelected={ OnRoleSelected(it) }, onConfirm={ OnConfirmRoleChange })
    }
  }
}
```

**MemberHeaderSection** (bg=#A6F1A6, no card border, padding=20dp):
```
Column(
  modifier = fillMaxWidth + background(#A6F1A6) + padding(20dp),
  horizontalAlignment = CenterHorizontally
) {
  Spacer(8dp)
  MemberAvatar(member=member, size=80dp)      // larger avatar on profile
  Spacer(12dp)
  Text(member.displayName, style=headlineSmall 24sp/400, color=#002106, textAlign=Center)
  Spacer(8dp)
  RoleChipFilled(role=role)                  // filled/colored chip for profile
  Spacer(8dp)
  Row(verticalAlignment=CenterVertically, horizontalArrangement=spacedBy(6dp)) {
    Icon(phone, tint=#002106, size=16dp)
    Text(member.phone, style=bodyMedium 14sp, color=#002106)
  }
  Spacer(4dp)
  Text("Member since ${member.joinDate.formatted}",
    style=bodySmall 12sp, color=#002106.copy(alpha=0.7f))
  if (isCurrentUserChairperson) {
    Spacer(12dp)
    OutlinedButton(
      text="Edit Role", icon=edit,
      borderColor=#002106, textColor=#002106,
      modifier=height(40dp), onClick={ OnEditRole }
    )
  }
  Spacer(8dp)
}
```

**SavingsHistoryCard** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
ElevatedCard(
  shape = RoundedCornerShape(16dp), elevation = 2dp,
  modifier = fillMaxWidth
) {
  Column(modifier=padding(16dp)) {
    Text("Savings History", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(8dp)
    Text("KES ${accounts.savingsBalance.formatted}",
      style=headlineMedium 28sp/400, color=#2E7D32)
    Spacer(12dp)
    SavingsSparkline(
      dataPoints=accounts.savingsHistory,
      lineColor=#2E7D32, fillColor=#A6F1A6.copy(alpha=0.4f),
      modifier=fillMaxWidth + height(80dp)
    )
  }
}
```

**Sparkline details**: 7 data points (weekly snapshots). X-axis: dates (not labeled). Y-axis: balance (not labeled). Line width: 2dp. Dots at each point: 4dp filled circles. Fill: gradient from #A6F1A6 at 40% opacity at top to transparent at bottom. Draws left-to-right on first appear (PathEffect.dashPathEffect animated, 600ms). No axis lines shown (pure sparkline, minimalist).

**ActiveLoanCard** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
ElevatedCard(
  shape = RoundedCornerShape(16dp), elevation = 2dp,
  border = if (loan.inArrears) BorderStroke(2.dp, #D32F2F) else null,
  modifier = fillMaxWidth
) {
  Column(padding=16dp) {
    Text("Active Loan", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(4dp)
    Text(loan.productName, style=bodyMedium 14sp, color=#424942)
    Spacer(8dp)
    Text("KES ${loan.outstandingBalance.formatted} outstanding",
      style=titleLarge 22sp/500, color=#1A1C19)
    if (loan.inArrears) {
      Spacer(8dp)
      ArrearsBanner(dueDate=loan.dueDate)
    }
  }
}
```

**ArrearsBanner** (bg=#FFDAD6, cornerRadius=8dp, padding=12dp):
```
Row(bg=#FFDAD6, cornerRadius=8dp, padding=12dp, verticalAlignment=CenterVertically) {
  Icon(warning_amber, tint=#D32F2F, size=20dp)
  Spacer(8dp)
  Text("This loan is in arrears. Due: ${loan.dueDate.formatted}",
    style=bodySmall 12sp, color=#410002)
}
```

**AttendanceCard** (bg=#FAFAFA, cornerRadius=16dp, elevation=2dp, padding=16dp):
```
ElevatedCard(shape=RoundedCornerShape(16dp), elevation=2dp) {
  Column(padding=16dp) {
    Text("Meeting Attendance", style=titleMedium 16sp/500, color=#1A1C19)
    Spacer(8dp)
    Text("${meetingsAttended} / ${totalMeetings}",
      style=headlineMedium 28sp/400, color=#1565C0)
    Spacer(4dp)
    Text("${(attendanceRate*100).toInt()}% attendance rate",
      style=bodyMedium 14sp, color=#424942)
    Spacer(12dp)
    LinearProgressIndicator(
      progress = attendanceRate,
      modifier = fillMaxWidth + height(8dp) + clip(RoundedCornerShape(4dp)),
      color = when {
        attendanceRate >= 0.80f -> #1565C0
        attendanceRate >= 0.60f -> #FF8F00
        else -> #D32F2F
      },
      trackColor = #DEE5DA
    )
  }
}
```

---

### Screen: MemberAddScreen

**Route**: `/groups/{groupId}/members/add`
**Composable**: `MemberAddScreen(groupId: String, viewModel: MemberAddViewModel)`

**Full layout tree**:
```
Scaffold(
  topBar = SmallTopAppBar(
    title = "Add Member",
    navigationIcon = IconButton(close, "Discard and go back", { OnBack }),
    backgroundColor = #2E7D32, contentColor = #FFFFFF
  )
) { paddingValues ->
  Column(
    modifier = fillMaxSize.padding(paddingValues),
    verticalArrangement = SpaceBetween
  ) {
    // Scrollable form content
    LazyColumn(
      modifier = fillMaxWidth.weight(1f),
      contentPadding = PaddingValues(horizontal=16dp, vertical=16dp),
      verticalArrangement = spacedBy(12dp)
    ) {
      // Photo picker centered
      item {
        Box(fillMaxWidth, contentAlignment=Center) {
          PhotoPickerArea(
            photoUri=photoUri,
            size=120dp,
            onTap={ OnPhotoPickerOpen },
            onRemove={ OnPhotoRemoved }
          )
        }
      }

      item { Spacer(8dp) }

      item {
        OutlinedTextField(
          value=firstName, onValueChange={ OnFirstNameChange(it) },
          label="First Name", placeholder="e.g. Amina",
          isError=validationErrors["firstName"] != null,
          supportingText=validationErrors["firstName"],
          keyboardOptions=name, singleLine=true,
          modifier=fillMaxWidth + minHeight(56dp)
        )
      }

      item {
        OutlinedTextField(
          value=lastName, onValueChange={ OnLastNameChange(it) },
          label="Last Name", placeholder="e.g. Wanjiru",
          isError=validationErrors["lastName"] != null,
          supportingText=validationErrors["lastName"],
          keyboardOptions=name, singleLine=true,
          modifier=fillMaxWidth + minHeight(56dp)
        )
      }

      item {
        OutlinedTextField(
          value=phone, onValueChange={ OnPhoneChange(it) },
          label="Phone Number", placeholder="+254712345678",
          supportingText=validationErrors["phone"] ?: "Kenyan number: +254 or 07XXXXXXXX",
          isError=validationErrors["phone"] != null,
          keyboardOptions=phone_number, prefix="+254",
          singleLine=true, maxLength=13,
          modifier=fillMaxWidth + minHeight(56dp)
        )
      }

      item {
        ExposedDropdownMenuBox(
          label="Role",
          options=[("Chairperson", CHAIRPERSON), ("Treasurer", TREASURER),
                   ("Secretary", SECRETARY), ("Member", MEMBER)],
          selected=selectedRole, onSelect={ OnRoleSelected(it) },
          modifier=fillMaxWidth + minHeight(56dp)
        )
      }

      if (isOffline) {
        item {
          OfflineBanner(
            message="You are offline. This member will be added when you reconnect.",
            bg=#D2E4FF, textColor=#001C39, icon=wifi_off, iconTint=#1565C0
          )
        }
      }

      item { Spacer(8dp) }
    }

    // Sticky save button at bottom
    Column(
      modifier = fillMaxWidth + padding(horizontal=16dp, vertical=12dp)
                + background(#FFFFFF) + shadow(4dp)
    ) {
      FilledButton(
        text="Save Member",
        loading=isSubmitting,
        bg=#2E7D32, textColor=#FFFFFF,
        modifier=fillMaxWidth + height(56dp),
        onClick={ OnSubmit }
      )
    }
  }

  // Photo source bottom sheet
  if (showPhotoPicker) {
    ModalBottomSheet(onDismissRequest={ /* close */ }) {
      PhotoSourceSheet(
        onCamera={ OnPhotoCaptured },
        onGallery={ OnPhotoSelected }
      )
    }
  }
}
```

**PhotoPickerArea** composable (120dp × 120dp):
```
Box(
  modifier = size(120dp) + clip(CircleShape)
             + background(if (photoUri==null) #DEE5DA else Color.Transparent)
             + clickable { onTap() },
  contentAlignment = Center
) {
  if (photoUri != null) {
    AsyncImage(url=photoUri, contentScale=Crop, modifier=fillMaxSize)
  } else {
    Icon(add_a_photo, tint=#424942, size=40dp)
  }
  // Remove button (top-right, only when photo set)
  if (photoUri != null) {
    IconButton(
      icon = cancel, tint = #FFFFFF,
      bg = #D32F2F, size = 24dp,
      modifier = size(32dp) + align(TopEnd),
      onClick = onRemove
    )
  }
}
```

**PhotoSourceSheet** (ModalBottomSheet, bg=#FAFAFA, topCorners=28dp):
```
Column(modifier=padding(bottom=24dp)) {
  Text("Add Photo", style=titleMedium 16sp/500, color=#1A1C19,
    modifier=padding(horizontal=16dp, vertical=12dp))
  Divider(color=#C2C9BD)
  ListItem(
    leadingContent = { Icon(camera_alt, tint=#2E7D32, size=24dp) },
    headlineContent = { Text("Take Photo", style=bodyLarge 16sp, color=#1A1C19) },
    modifier = fillMaxWidth + minHeight(56dp) + clickable { onCamera() }
  )
  ListItem(
    leadingContent = { Icon(photo_library, tint=#2E7D32, size=24dp) },
    headlineContent = { Text("Choose from Gallery", style=bodyLarge 16sp, color=#1A1C19) },
    modifier = fillMaxWidth + minHeight(56dp) + clickable { onGallery() }
  )
}
```

**RoleEditSheetContent** (inside ModalBottomSheet):
```
Column(modifier=fillMaxWidth + padding(horizontal=16dp, vertical=8dp, bottom=24dp)) {
  Box(
    modifier = size(32dp, 4dp) + clip(RoundedCornerShape(2dp))
               + background(#727971) + align(CenterHorizontally)
  )  // drag handle
  Spacer(12dp)
  Text("Change Member Role", style=titleMedium 16sp/500, color=#1A1C19,
    modifier=padding(bottom=8dp))
  Divider(color=#C2C9BD)
  Spacer(8dp)

  listOf(CHAIRPERSON, TREASURER, SECRETARY, MEMBER).forEach { roleOption ->
    ListItem(
      headlineContent = { Text(roleOption.displayName, style=labelLarge 14sp/500, color=#1A1C19) },
      trailingContent = {
        RadioButton(
          selected = selectedRole == roleOption,
          onClick = { OnRoleSelected(roleOption) },
          colors = RadioButtonDefaults.colors(selectedColor=#2E7D32)
        )
      },
      modifier = fillMaxWidth + minHeight(56dp) + clickable { OnRoleSelected(roleOption) }
    )
  }

  Spacer(8dp)
  FilledButton(
    text = "Confirm",
    loading = isUpdatingRole,
    bg = #2E7D32, textColor = #FFFFFF,
    modifier = fillMaxWidth + height(56dp),
    onClick = { OnConfirmRoleChange }
  )
}
```

---

## 3. Component Specifications

### TopAppBar (MemberList — with subtitle)
- Type: SmallTopAppBar (with custom Column title for subtitle)
- Height: 64dp (title + subtitle)
- Background: #2E7D32
- Title text: "Members", titleLarge 22sp/500, #FFFFFF
- Subtitle text: groupName, labelMedium 12sp/500, #FFFFFF at 80% opacity
- Navigation icon: arrow_back, tint=#FFFFFF, touchTarget=48dp
- Shadow: elevation 0dp

### TopAppBar (MemberProfile + MemberAdd)
- Height: 56dp
- Title: "Member Profile" / "Add Member", titleMedium 16sp/500 (CenterAligned), #FFFFFF
- Navigation: arrow_back (profile) / close (add), tint=#FFFFFF, 48dp
- MemberAdd: no trailing actions

### MemberListItem (SwipeableListItem)
- Height: min 72dp
- Full width minus 0dp (edge-to-edge with dividers)
- Background (foreground layer): #FAFAFA
- Swipe reveal background: #A6F1A6 (primaryContainer)
- Avatar (leading): 48dp circle, no clip visible beyond circle
- Headline (member name): bodyLarge 16sp/400, #1A1C19, maxLines=1, ellipsis
- Supporting (savings): bodySmall 12sp/400, #424942
- Trailing (chips column):
  - Role chip: h=24dp, padding horizontal=8dp, cornerRadius=8dp, labelMedium 12sp/500
  - Loan badge: h=20dp, padding horizontal=6dp, cornerRadius=4dp, labelSmall 11sp/500
- Divider: 0.5dp #C2C9BD, starts at 80dp indent (after avatar)
- Ripple: full-width bounded, #2E7D32 at 12% opacity
- Swipe animation: 300ms, spring(stiffness=300, dampingRatio=0.85)

### RoleChip (list style — AssistChip)
- Height: 24dp
- Corner radius: 8dp (small)
- Horizontal padding: 8dp inside
- Typography: labelMedium 12sp/500
- No icon (text only)
- CHAIRPERSON: bg=#A6F1A6, text=#002106
- TREASURER: bg=#FFDDB3, text=#2A1700
- SECRETARY: bg=#D2E4FF, text=#001C39
- MEMBER: bg=#DEE5DA, text=#424942

### RoleChipFilled (profile style — FilterChip)
- Height: 32dp
- Corner radius: 16dp (full)
- Horizontal padding: 12dp
- Typography: labelLarge 14sp/500
- CHAIRPERSON: bg=#2E7D32, text=#FFFFFF
- TREASURER: bg=#FF8F00, text=#FFFFFF
- SECRETARY: bg=#1565C0, text=#FFFFFF
- MEMBER: bg=#DEE5DA, text=#424942

### LoanStatusBadge
- Height: 20dp
- Corner radius: 4dp (extra_small)
- Horizontal padding: 6dp
- Typography: labelSmall 11sp/500
- ACTIVE: bg=#C8E6C9, text=#1B5E20
- NONE: bg=#DEE5DA, text=#424942
- OVERDUE: bg=#FFCDD2, text=#B71C1C

### FAB (MemberList)
- Type: ExtendedFloatingActionButton
- Height: 56dp, min-width: 80dp
- Corner radius: 28dp (extra_large)
- Background: #2E7D32, content: #FFFFFF
- Icon: person_add, 24dp
- Label: "Add Member", labelLarge 14sp/500
- Position: BottomEnd, margin=16dp
- Collapse on scroll (threshold 200dp): label fades out 100ms, width shrinks to 56dp
- Expand on scroll up: label fades in 100ms, width expands 300ms

### ShimmerMemberRow
- Height: 72dp
- Full width
- Background: animated gradient #DEE5DA → #C2C9BD → #DEE5DA
- Left circle stub: 48dp × 48dp
- Right: two lines (h=12dp, h=8dp) with gap, width=60% and 40% of row
- Divider at bottom: 0.5dp #C2C9BD
- Animation cycle: 1200ms, infinite loop left-to-right

### SavingsSparkline
- Type: custom Canvas/Path composable (or MPAndroidChart/Vico LineChart)
- Height: 80dp, width: fillMaxWidth − 32dp (card padding)
- No axes, no labels, no legend
- Line: 2dp solid, color=#2E7D32
- Area fill: LinearGradient from #A6F1A6 (40% alpha at top) to transparent at bottom
- Data points: filled circles 4dp diameter, color=#2E7D32
- Draw animation: path draws progressively left-to-right on composition (PathEffect animation, 600ms, decelerated)
- No interaction (sparkline only — tap the card for full history screen if added later)

### LinearProgressIndicator (Attendance)
- Width: fillMaxWidth
- Height: 8dp (thicker than default for visibility)
- Corner radius: 4dp (clipped)
- Track color: #DEE5DA
- Indicator color: computed from attendanceRate (tertiary / secondary / error)
- Animated: progress animates from 0 → actual value on first appear (400ms, standard easing)

### SaveMemberButton (FilledButton in MemberAdd)
- Height: 56dp
- Width: fillMaxWidth
- Corner radius: 12dp
- Background: #2E7D32
- Text: "Save Member", labelLarge 14sp/500, #FFFFFF
- Loading state: label fades out 100ms, CircularProgressIndicator 16dp #FFFFFF fades in 100ms
- Disabled state (all fields empty or validation errors present): alpha 0.38, not actually disabled (shows errors on tap)

### OutlinedTextField (MemberAdd)
- Min height: 56dp
- Corner radius: 4dp (M3 standard)
- Idle border: 1dp #727971
- Focused border: 2dp #2E7D32
- Error border: 2dp #D32F2F
- Label: floats above on focus/value, labelMedium 12sp/500 → labelSmall 11sp when floating
- Placeholder: bodyMedium 14sp, #727971
- Helper: bodySmall 12sp, #424942 (idle) / #D32F2F (error)
- Character count: shown for firstName/lastName fields
- Prefix "+254": bodyMedium 14sp, #1A1C19 (visible always on phone field)
- Keyboard type: KeyboardType.Text for name fields, KeyboardType.Phone for phone field

### ExposedDropdownMenuBox (Role — MemberAdd)
- Min height: 56dp
- Width: fillMaxWidth
- Style: OutlinedTextField appearance with dropdown arrow icon
- Options: Chairperson, Treasurer, Secretary, Member
- Default selected: Member
- Selected option text: bodyMedium 14sp, #1A1C19
- Dropdown menu: bg=#FAFAFA, elevation=8dp, cornerRadius=4dp
- Menu items: DropdownMenuItem height=48dp, labelLarge 14sp/500 with role-colored dot indicator

### ModalBottomSheet (RoleEdit + PhotoSource)
- Background: #FAFAFA
- Top corner radius: 28dp
- Bottom corners: 0dp (goes to edge)
- Elevation: 6dp (level_3)
- Scrim: #000000 at 32% opacity behind sheet
- Drag handle: 32dp × 4dp, cornerRadius=2dp, bg=#727971, centered at top
- Expand animation: 450ms long_1, decelerated easing
- Dismiss: swipe down or tap scrim. 400ms, accelerated easing.
- Sheet height: wrap content (role edit: ~320dp; photo source: ~200dp)

### OfflineBanner (MemberAdd)
- Background: #D2E4FF (tertiaryContainer)
- Corner radius: 8dp
- Padding: 12dp
- Icon: wifi_off, tint=#1565C0, size=20dp
- Text: "You are offline. This member will be added when you reconnect." — bodySmall 12sp, #001C39
- Animation: fade in 250ms when isOffline changes false→true
- Not dismissible

---

## 4. Interaction Patterns

### Member List — Initial Load
1. Screen enters from group-dashboard "Members" button tap (shared element: "Members" button text, 350ms)
2. GroupListViewModel.init() receives groupId from nav params
3. isLoading=true: shimmer rows render (6 × 72dp)
4. API: GET /groups/{groupId}/clients?limit=20&offset=0
5. On success: isLoading=false. Shimmer fades out (100ms). Member rows fade in staggered: each row 50ms delay after previous, opacity 0→1 + translateY 8dp→0dp (150ms each, decelerated)
6. Total list enter duration (5 items): 50ms × 5 + 150ms = 400ms
7. FAB appears with scale animation (0.5→1.0, 300ms, standard easing) after list renders

### Infinite Scroll / Pagination
1. User scrolls to last visible item in LazyColumn
2. Trigger condition: lastVisibleIndex >= members.size − 3 (preload trigger 3 items before end)
3. isLoadingMore=true: LinearProgressIndicator (h=4dp, #2E7D32) appears at bottom of list
4. API: GET /groups/{groupId}/clients?limit=20&offset=20 (offset increments by pageSize)
5. On success: new members appended to list. isLoadingMore=false. Progress indicator fades out.
6. hasMorePages=false when: offset + pageItems.size >= totalFilteredRecords
7. When no more pages: progress indicator remains hidden on further scrolls

### Swipe-to-Reveal Profile
1. User begins horizontal swipe on list item (start-to-end direction, left to right in LTR)
2. Swipe progress 0→80dp: foreground item translates right. Green background (#A6F1A6) with "View Profile" text + icon reveals at left.
3. Swipe progress 80dp: haptic feedback (light click)
4. User releases at >80dp: item animates to fully swiped width (120dp), then immediately fires OnMemberClick(member.id) → NavigateToMemberProfile event
5. User releases at <80dp: item snaps back to 0 (spring animation, stiffness=400, dampingRatio=0.8)
6. Screen transition to member profile: container transform if member avatar is shared element; otherwise: slide from right (300ms)

### Pull to Refresh (MemberList)
1. User pulls down 80dp: M3 pull indicator appears, #2E7D32 color
2. Release: spinner completes, API re-called with invalidate_cache=true, offset=0 (resets pagination)
3. List replaces entirely: fade out old + fade in new (150ms each)

### Member Profile — Parallel API Load
1. MemberProfileViewModel.init() called with memberId + groupId
2. Three coroutines launched in parallel: get_client, get_client_accounts, get_member_role
3. isLoading=true: 4× shimmer blocks (h=100dp) shown
4. All three complete:
   - compute: attendanceRate = meetingsAttended / max(totalMeetings, 1)
   - compute: isCurrentUserChairperson from SessionManager.currentUserRole == CHAIRPERSON
5. Content renders: cards stagger in (50ms each) top to bottom
6. Sparkline begins draw animation (600ms after card appears, decelerated)
7. Attendance progress bar animates 0 → attendanceRate (400ms, standard)

### Edit Role Flow
1. "Edit Role" button visible only when isCurrentUserChairperson=true
2. Tap: OnEditRole action. isEditingRole=true. ModalBottomSheet expands (450ms, decelerated easing). Scrim fades in (200ms).
3. Sheet pre-selects current role (radio filled #2E7D32)
4. User taps different role option: OnRoleSelected(role) fires.
   - Old radio: animates to unselected (unfilled, 150ms)
   - New radio: animates to selected (#2E7D32, 150ms)
5. User taps "Confirm": isUpdatingRole=true. Button label fades out, spinner appears.
6. API PUT /datatables/dt_member_role/{clientId} with body { "role": newRole }
7. On success:
   - Sheet dismisses with slide down + scrim fade out (400ms, accelerated)
   - Header role chip on profile updates with crossfade animation (200ms): old chip color → new chip color
   - Snackbar appears: "Role updated successfully." (#2E7D32 tinted, bodyMedium 14sp, white text, duration=3000ms)
8. On failure: isUpdatingRole=false. Snackbar "Could not update role. Please retry." Sheet remains open.

### Member Add — Form Interaction
1. First name field: user taps, keyboard opens. Border 2dp #2E7D32 on focus.
2. Typing: character counter appears at trailing edge of field. Max 50 chars.
3. Phone field: prefix "+254" always visible. User types remaining digits. Validation regex `^[7][0-9]{8}$` for the suffix part.
4. Role dropdown: tap opens ExposedDropdownMenu. 4 options with role-colored dot indicators. Selection updates field.
5. Photo: tap circle → PhotoSourceSheet expands. Camera intent OR gallery picker. On return: image URI set → circular thumbnail renders in picker area. Remove button (✕, red) appears.

### Member Add — Submit
1. Tap "Save Member": OnSubmit
2. Validate: firstName (min 2), lastName (min 2), phone (regex match), selectedRole (always valid)
3. If invalid: animate error borders + helper text. Scroll to first invalid field if off-screen.
4. If valid, online: isSubmitting=true. Button spinner.
   - Step 1: POST /clients → clientId
   - Step 2: POST /datatables/dt_member_role/{clientId}
   - Step 3 (if photoUri): POST /clients/{clientId}/images (multipart)
   - On all success: NavigateToMemberProfile(memberId=clientId, groupId=groupId)
   - Screen transition: slide from right (member profile enters, member-add exits left)
5. If valid, offline: enqueue SyncQueueItem chain → ShowOfflineSyncDialog
   - Dialog title: "Saved for sync" (titleMedium 16sp)
   - Dialog body: "Grace Achieng will be added to Mwangaza Women's Group when you reconnect."
   - One action: "Got it" → NavigateBack to member-list

### Discard Confirmation (MemberAdd)
1. User taps close icon or presses system back
2. Any field has non-empty value: AlertDialog appears:
   - Title: "Discard new member?" (titleMedium 16sp)
   - Body: "Your entry will not be saved." (bodyMedium 14sp, #424942)
   - Buttons: [Cancel] (TextButton, #2E7D32) | [Discard] (FilledButton, #D32F2F)
3. Discard: navigate back immediately (slide right exit 300ms)
4. Cancel: dialog dismisses (fade out 150ms)

---

## 5. Content Data

### Group Context
- Group: Mwangaza Women's Group (Fineract Center ID: 101, groupId for member routes: "gp-101")
- Office: Nairobi Head Office
- Currency: KES

### Demo Member Roster (5 members)

**Member 1 — Amara Diallo (Chairperson)**
- Full name: Amara Diallo
- First name: Amara
- Last name: Diallo
- Display name: Amara Diallo
- Phone: +254701234567
- Role: CHAIRPERSON
- Join date: 15 January 2026
- Savings balance: KES 4,200.00
- Loan status: ACTIVE
- Fineract Client ID: 1002
- Photo: no photo (initials "AD", avatar bg=#A6F1A6, text=#002106)
- Savings history (7 weeks):
  - 2026-01-20: KES 500.00
  - 2026-01-27: KES 1,000.00
  - 2026-02-03: KES 1,500.00
  - 2026-02-10: KES 2,000.00
  - 2026-02-17: KES 2,800.00
  - 2026-02-24: KES 3,500.00
  - 2026-03-03: KES 4,200.00
- Active loan: product "Group Loan", principal KES 5,000, outstanding KES 5,000, inArrears=false, dueDate=2026-06-03
- Meetings attended: 15, total: 15, attendance rate: 100%

**Member 2 — Grace Mwangi (Treasurer)**
- Full name: Grace Mwangi
- Phone: +254712345678
- Role: TREASURER
- Join date: 15 January 2026
- Savings balance: KES 3,500.00
- Loan status: NONE
- Fineract Client ID: 1001
- Photo: no photo (initials "GM", avatar bg=#FFDDB3, text=#2A1700)
- Savings history (7 weeks):
  - 2026-01-20: KES 500.00
  - 2026-01-27: KES 1,000.00
  - 2026-02-03: KES 1,500.00
  - 2026-02-10: KES 2,000.00
  - 2026-02-17: KES 2,500.00
  - 2026-02-24: KES 3,000.00
  - 2026-03-03: KES 3,500.00
- Active loan: null (no active loan)
- Meetings attended: 14, total: 15, attendance rate: 93%

**Member 3 — Fatima Ouedraogo (Secretary)**
- Full name: Fatima Ouedraogo
- Phone: +254723456789
- Role: SECRETARY
- Join date: 15 January 2026
- Savings balance: KES 2,800.00
- Loan status: NONE
- Fineract Client ID: 1003
- Photo: no photo (initials "FO", avatar bg=#D2E4FF, text=#001C39)
- Savings history (7 weeks):
  - 2026-01-20: KES 400.00
  - 2026-01-27: KES 800.00
  - 2026-02-03: KES 1,200.00
  - 2026-02-10: KES 1,600.00
  - 2026-02-17: KES 2,000.00
  - 2026-02-24: KES 2,400.00
  - 2026-03-03: KES 2,800.00
- Active loan: null
- Meetings attended: 13, total: 15, attendance rate: 87%

**Member 4 — Peter Otieno (Member)**
- Full name: Peter Otieno
- Phone: +254734567890
- Role: MEMBER
- Join date: 20 January 2026
- Savings balance: KES 1,500.00
- Loan status: OVERDUE
- Fineract Client ID: 1004
- Photo: no photo (initials "PO", avatar bg=#DEE5DA, text=#424942)
- Savings history (6 weeks):
  - 2026-01-27: KES 300.00
  - 2026-02-03: KES 600.00
  - 2026-02-10: KES 900.00
  - 2026-02-17: KES 1,200.00
  - 2026-02-24: KES 1,500.00
  - 2026-03-03: KES 1,500.00 (no deposit — missed)
- Active loan: product "Group Loan", principal KES 2,000, outstanding KES 2,000, inArrears=true, dueDate=2026-04-15
- Meetings attended: 10, total: 15, attendance rate: 67%

**Member 5 — Mary Njeri (Member)**
- Full name: Mary Njeri
- Phone: +254745678901
- Role: MEMBER
- Join date: 15 January 2026
- Savings balance: KES 2,000.00
- Loan status: NONE
- Fineract Client ID: 1005
- Photo: no photo (initials "MN", avatar bg=#DEE5DA, text=#424942)
- Savings history (7 weeks):
  - 2026-01-20: KES 250.00
  - 2026-01-27: KES 500.00
  - 2026-02-03: KES 750.00
  - 2026-02-10: KES 1,000.00
  - 2026-02-17: KES 1,300.00
  - 2026-02-24: KES 1,700.00
  - 2026-03-03: KES 2,000.00
- Active loan: null
- Meetings attended: 12, total: 15, attendance rate: 80%

### Member Add Demo Entry

Form values for mockup demo:
- First name: Grace
- Last name: Achieng
- Phone: +254723456789
- Role: Secretary (SECRETARY)
- Photo: no photo selected (circular placeholder shown)
- isOffline: false (online state for primary demo)
- isSubmitting: false (idle state)
- All validationErrors: empty (no errors)

Offline demo state (secondary screen):
- isOffline: true
- Offline banner visible: "You are offline. This member will be added when you reconnect."
- Save button: enabled with primary appearance (queues on tap instead of submitting)

Validation error demo state (tertiary screen):
- firstName: empty → error "First name must be at least 2 characters."
- phone: "+254ABC" → error "Enter a valid Kenyan phone number."
- Both fields show 2dp red border (#D32F2F) + error helper text in red (#D32F2F)

---

## 6. Responsive Rules

### Compact Layout (0–599dp — phones, primary target devices)

**MemberListScreen**:
- Full-width list items (0dp horizontal margin, edge-to-edge)
- Avatar: 48dp, touching left edge at 16dp indent
- Role chip + loan badge: trailing column, right-aligned
- FAB: ExtendedFAB at bottom_end, margin=16dp. Collapses on scroll down 200dp.
- Bottom nav: visible (selected tab=Groups)
- List item padding: 0dp horizontal (let ListItem handle internal padding at 16dp)

**MemberProfileScreen**:
- All cards: full width with 16dp horizontal padding
- Header: full-width (edge-to-edge bg=#A6F1A6, no card border, flush below app bar)
- Avatar: 80dp, centered in header
- Sparkline: full width minus 32dp (card horizontal padding 16dp each side)
- Attendance bar: full width minus 32dp
- No bottom nav (detail screen, only back)

**MemberAddScreen**:
- All fields: full width, 16dp horizontal padding
- Photo picker: 120dp, centered horizontally
- Save button: full-width, sticky at bottom
- No bottom nav (form screen, close button to exit)

---

### Medium Layout (600–839dp — foldables, small tablets)

**MemberListScreen**:
- List horizontal margin: 32dp each side (xxl)
- Items: single column (wider but still single)
- FAB: always extended (never collapses — more screen width)
- Navigation: navigation rail (left edge, 72dp) replaces bottom nav

**MemberProfileScreen**:
- Header: card with 16dp corner radius (same as other cards, not flush)
- Savings history + Active loan: horizontal Row (side by side if both present)
  - SavingsHistoryCard: weight=0.55f
  - ActiveLoanCard: weight=0.45f
- Attendance card: full width below the row
- Avatar: remains 80dp centered

**MemberAddScreen**:
- Form fields: max width 480dp, centered horizontally with auto horizontal margins
- Photo picker: 120dp, still centered
- Keyboard: same fields and keyboard types
- Save button: max width 480dp, centered

---

### Expanded Layout (840dp+ — tablets, landscape, desktop)

**MemberListScreen (left panel) + MemberProfileScreen (right panel)**:
- Two-panel layout: left panel max 380dp (member list), right panel (member profile detail)
- Navigation: persistent NavigationDrawer (240dp) on far left
- Left panel = MemberList: single column, no FAB — "Add Member" TextButton in panel header
- Right panel = MemberProfile: renders full profile on selection
- Initial state: "Select a member to view their profile" placeholder in right panel
- On member select: right panel updates (no separate route push, state-based)

**MemberAddScreen (expanded)**:
- Rendered as Dialog (max width 480dp, centered) or ModalBottomSheet (max width 480dp)
- Form fields: max 480dp inside dialog
- Save button: full width inside dialog

**Navigation (expanded)**:
- NavigationDrawer (240dp, permanent):
  - Groups (with sub-items or section highlight)
  - Members (selected in member context)
  - Meetings
  - Loans
  - Settings
- No bottom nav, no navigation rail

---

### Grid System Across Breakpoints

**Compact (phone)**:
- Columns: 4
- Margin: 16dp
- Gutter: 8dp
- List items: 4 columns (full width)
- Form fields: 4 columns

**Medium (foldable/tablet)**:
- Columns: 8
- Margin: 32dp
- Gutter: 12dp
- List items: 8 columns
- Profile cards: optional 4+4 split for parallel cards

**Expanded (large tablet)**:
- Columns: 12
- Margin: 32dp
- Gutter: 16dp
- Left panel (list): 4 columns (33%)
- Right panel (profile): 8 columns (67%)
- Form dialog: 4 columns wide, centered

---

### Orientation Rules — Landscape Phone

**MemberListScreen (landscape)**:
- Continues to function; LazyColumn scrolls vertically
- FAB: collapses to icon-only immediately (limited vertical space)
- TopAppBar: reduces to minimum height (40dp); subtitle may hide

**MemberProfileScreen (landscape)**:
- Header: card style (not flush); avatar centered, horizontal layout: avatar left, name/chips/phone right
- Savings + Loan: side-by-side Row
- Attendance card: full width below

**MemberAddScreen (landscape)**:
- Photo picker: above form, centered
- Fields: wrap in LazyColumn with vertical scroll (critical for keyboard push)
- Save button: sticky at bottom (above keyboard)
- Total minimum height for usable form: 380dp

---

### Typography Scaling (Dynamic Type / accessibility)

- All type sizes in sp: scale with system font preferences
- At 1.3× system scale: displaySmall would render at ~47dp, headlineMedium at ~36dp
- All containers use wrapContentHeight — no fixed text container heights
- Comfortable density absorbs extra line heights on text wrap
- Role chips: may expand width at larger scales; use FlowRow if needed
- Single-line max on member list displayName: ellipsis at 1 line; full name accessible via contentDescription
- Savings balance (headlineMedium 28sp at 1.3× = 36dp): card expands vertically to accommodate

---

### Dark Mode Behavior

Full dark color set applied automatically based on system setting.
Key dark-mode mappings for member onboarding:
- Surface #FAFAFA → #121412 (near-black cards)
- Primary #2E7D32 → #8BD68F (light green visible on dark)
- PrimaryContainer #A6F1A6 → #00531A (dark green for header bg)
- onPrimaryContainer #002106 → #A6F1A6 (pale green text on dark header)
- SecondaryContainer #FFDDB3 → #653E00 (dark amber)
- TertiaryContainer #D2E4FF → #004A82 (dark blue)
- ErrorContainer #FFDAD6 → #93000A (dark red for arrears banner)
- Sparkline fill: primaryContainer alpha 40% → #00531A (dark green container) at 40%
- All role chips: dark container colors with appropriate onContainer text colors
- Attendance bar tertiary: #1565C0 → #9FCAFF (light blue on dark)
- Shimmer: #DEE5DA → #424942 (surfaceVariant dark)
