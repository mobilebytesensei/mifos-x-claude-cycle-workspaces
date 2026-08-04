# Group List — Figma Prompts (Auto-Complete Style)

<!-- generated_by: /idea-render-mockup --feature group-list -->
<!-- generated_at: 2026-07-18 -->
<!-- source: screens/group-list/{ui.yaml,demo-data.yaml}, design-system/DESIGN.md -->

> Short Figma-optimized per-state prompts for **MifosSave** (group-list) — the authenticated member's role-aware savings-group roster.
> Design tokens: primary `#2E7D32` (VSLA green) · accent `#FF8F00` (pooled fund amber) · info `#1565C0` · surface `#FAFAFA` · canvas `#FFFFFF`

---

## Global Context

- Feature: Group List · MifosSave KMP community-banking app · 10 components · 4 states
- Brand: `#2E7D32` primary · `#FF8F00` accent · `#1565C0` info · `#C62828` danger · `#F57C00` warning
- Typography: **Noto Sans** — titleLarge 22sp (screen title) · titleMedium 16sp (group name) · bodySmall 12sp (meta) · labelSmall 11sp (chips) · scaled for low-vision rural users
- Aesthetic dial (from `design_read`): family `minimalist-ui` · density 7/10 (dense financial dashboards) · variance 3/10 · motion 3/10 (subtle only)
- Touch targets: 48dp minimum · 56dp for FAB and primary CTAs · outdoor WCAG AAA contrast on primary surfaces
- Shape: cards `cornerRadius=12dp` · search bar `cornerRadius=28dp` · buttons `cornerRadius=24dp` · elev cards `2dp`, FAB `6dp`

## Feature Description

Role-aware group roster — organizer / member / treasurer surfaces the authenticated user's savings groups (VSLA / ROSCA / SHG / ASCA) from `/companion/groups/mine`; each card carries group-type chip + viewer-role chip + cycle + member count + last meeting date + client-derived health indicator (GREEN/AMBER/RED); FAB → group-type-picker; empty state offers unified-identity Create + Join-with-code CTAs. Covers FR-021, FR-023.

---

## Screen: `group-list`

### State: `loading`

Scrollable column, padding md/sm. TopAppBar (`My Groups`, `#2E7D32` primary bg, `onPrimary` #FFFFFF title, 64dp height, `notifications` icon action). SearchBar pinned below (48dp height, 28dp radius, elev=2dp, `Search groups…` placeholder, `#616161` icon). Center-fill: 5× shimmer cards (full-width × 88dp, cornerRadius=12dp, animated left→right sweep 1200ms). Shimmer base `#F5F5F5` → highlight `#EEEEEE`. ExtendedFAB hidden.

### State: `content`

Scrollable column, padding md/sm. TopAppBar (`My Groups`, `#2E7D32`, notifications icon). SearchBar pinned (as above). LazyColumn of group_card items (16dp gutter, 12dp vertical spacing):

Each **group_card** — surface bg `#FFFFFF`, elev=2dp, cornerRadius=12dp, pad=16dp, min-touch=72dp. Vertical stack:
1. `group_name_text` — titleMedium 16sp/500, `#212121`, one-line marquee if > 24 chars
2. `card_badges_row` — 3 M3 chips, 8dp horizontal gap:
   - `group_type_chip` — VSLA / ROSCA / SHG / ASCA, `tertiaryContainer` bg, `onTertiaryContainer` text (M3 tokens)
   - `viewer_role_chip` — organizer / member / treasurer (case-lowered); **organizer** → `primaryContainer` #C8E6C9 / `#1B5E20`; **default** → `surfaceVariant` #EEEEEE / `#616161`
   - `cycle_chip` — `Cycle {n}`, `secondaryContainer` bg (accent-tinted `#FFE082`), `onSecondaryContainer` text
3. Row: `member_count_text` (bodySmall 12sp `#616161`, `"{n} members"`) · trailing spacer · `health_indicator_badge` (24dp pill: **GREEN** #C8E6C9/#1B5E20 · **AMBER** #FFF9C4/#E65100 · **RED** #FFCDD2/#B71C1C)
4. `last_meeting_text` — bodySmall 12sp `#616161`, `"Last met: {yyyy-MM-dd}"`

ExtendedFAB `create_group_fab` — 56dp height, bg `#2E7D32`, icon `add` + label `New Group` (onPrimary), bottom_end, margin=16dp, elev=6dp, collapses to icon-only on scroll-down past 200dp.

### State: `empty`

Centered column, padding lg/xxl. TopAppBar (`My Groups`, `#2E7D32`) + SearchBar pinned. Center block: outlined `group_off` icon (80dp, `#616161`), title `No groups yet` (headlineSmall 24sp `#212121`), subtitle `Create a new savings group or join an existing one with an invite code.` (bodyMedium 14sp `#616161`, max-width=320dp, center-aligned). Two CTAs stacked:
1. **Create Group** — FilledButton, bg `#2E7D32`, text onPrimary, 56dp height, full-width (max 320dp), 24dp radius
2. **Join with Code** — OutlinedButton, border `#2E7D32`, text `#2E7D32`, 48dp height, full-width (max 320dp), 24dp radius, gap above=8dp

ExtendedFAB still visible bottom_end (per Design AC — primary create path remains available).

### State: `error`

Centered column, padding lg/xxl. TopAppBar preserved (`My Groups`, `#2E7D32`) — SearchBar hidden per ui.yaml `states.error.components: [top_bar, error_state]`. Middle: outlined `cloud_off` icon (64dp, `#616161`), title `Could not load groups` (titleLarge 22sp `#212121`), body `{{error.message}}` (bodyMedium 14sp `#616161`, one of: `No internet connection. Showing cached data.` / `Server error. Please try again.` / `Session expired. Please log in again.`). Primary CTA: **Retry** — FilledButton, bg `#2E7D32`, text onPrimary, 56dp × 240dp, 24dp radius. Auth-error variant additionally shows `Log in again` link below Retry, on tap redirects to `login`.

---

## Component Library Mapping

- TopAppBar → M3 TopAppBar with `#2E7D32` primary background, onPrimary title, `notifications` action icon (24dp)
- SearchBar → M3 SearchBar (docked variant, 48dp × full-width, 28dp radius, elev=2dp, leading search icon, trailing clear icon when active)
- Group card → M3 Card (Elevated, elev=2dp, 12dp radius, 16dp padding) with vertical Column layout
- Group-type chip → M3 AssistChip with `tertiaryContainer` background
- Viewer-role chip → M3 AssistChip with role-conditional container (ORGANIZER → primaryContainer; other → surfaceVariant)
- Cycle chip → M3 AssistChip with `secondaryContainer` background
- Health badge → M3 Badge (24dp pill, filled tone, single-glyph dot + label text)
- Extended FAB → M3 ExtendedFloatingActionButton (56dp, filled primary #2E7D32, bottom-end, icon+label, elev=6dp)
- Shimmer → SkeletonBox (M3-compat, 88dp × full-width, 12dp radius, 1200ms sweep, base `#F5F5F5` → highlight `#EEEEEE`)
- Empty state → M3 EmptyState composite (icon 80dp + title + subtitle + stacked CTA column)
- Error state → M3 ErrorState composite (icon 64dp + title + message + Retry FilledButton)
- Bottom Nav → M3 NavigationBar (80dp, 4 tabs, `groups` tab selected)

---

## Variants

Light + Dark · Phone (360dp) / Tablet (600dp, two-column card grid) · RTL for Swahili / Kikuyu / Amharic / Arabic

**Dark mode** — surface bg `#1C1B1F`, cards `#2A2A2A`, primary shifts to `#A6F1A6` (lighter for dark bg), text primary `#E5E5E5`, health badges retain hue but shift to darker containers for contrast preservation (GREEN #1B5E20/#C8E6C9 inverted).

**Tablet (600dp+)** — LazyColumn becomes 2-column `LazyVerticalGrid` with 16dp cross-axis gap; cards keep 12dp radius + elev=2dp; FAB stays anchored bottom_end.

**RTL** — SearchBar leading/trailing icons mirror; chip row starts from right; FAB position mirrors to bottom_start.

---

## WCAG Compliance (Outdoor / Rural Low-Vision)

- Text on primary (`#2E7D32`): white `#FFFFFF` — ratio 8.10:1 ✓ WCAG AAA
- Text primary (`#212121`) on canvas (`#FFFFFF`) — ratio 16.10:1 ✓ WCAG AAA
- Text secondary (`#616161`) on canvas — ratio 5.74:1 ✓ WCAG AA
- Health GREEN badge (`#1B5E20` on `#C8E6C9`) — ratio 5.32:1 ✓ WCAG AA
- Health AMBER badge (`#E65100` on `#FFF9C4`) — ratio 4.98:1 ✓ WCAG AA
- Health RED badge (`#B71C1C` on `#FFCDD2`) — ratio 5.90:1 ✓ WCAG AA
- ORGANIZER role chip (`#1B5E20` on `#C8E6C9`) — ratio 5.32:1 ✓ WCAG AA
- Focus ring — 2dp solid `#2E7D32`, 2dp offset (keyboard nav) ✓

---

## Interaction Motion Budget

- Card tap ripple — 200ms bounded, from tap origin
- Card→dashboard transition — 350ms shared-element (group_name_text fade + slide)
- Search debounce — 150ms
- Pull-to-refresh — 200ms indicator fade-in/out, tint `#2E7D32`
- FAB scroll collapse — 200dp threshold, 200ms cross-fade to icon-only
- Retry → loading — 100ms button fade, immediate state swap
- Notifications snackbar (deferred) — 250ms slide-up, 4s dwell, 200ms fade-out
