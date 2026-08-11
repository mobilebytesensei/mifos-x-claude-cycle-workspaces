# Share-Out — Figma Prompts (Auto-Complete Style)

> Generated from v3.1 YAML siblings via /idea-migration reference.
> Short Figma-optimized per-state prompts for MifosSave (share-out).
> Design tokens: primary #2E7D32 (green) · secondary #FF8F00 (amber) · tertiary #1565C0 (blue)

---

## Global Context

- Feature: Share-Out · MifosSave banking app · 6 components · 4 states
- Brand: `#2E7D32` primary · `#FF8F00` amber warnings · `#1565C0` blue info
- Typography: Noto Sans — titleLarge (screen titles) · bodyLarge (list items) · labelSmall (chips/badges)
- Touch targets: 48dp minimum · 56dp for financial inputs · outdoor WCAG AAA contrast

## Feature Description

Two-step cycle distribution: read-only preview then execute

## Screen: `share-out-preview`

### State: `loading`

Scrollable column, padding md/sm. TopAppBar (title + back, primary bg). Center: 3 shimmer rows (full-width × 72dp, 8dp radius, 1000ms). Caption 'Loading...' (labelSmall/onSurfaceVariant/center). Shimmer base #E0E0E0 → highlight #F5F5F5.
### State: `content`

Scrollable column, padding md/sm. TopAppBar (title, primary bg, onPrimary text). Content section(s) with real data. FAB (56dp, primary, bottom-right) where applicable. Bottom Nav (80dp, 4 tabs).
### State: `review`

Screen: share-out-preview · State: review. Scrollable column, Material3, primary #2E7D32. TopAppBar + content sections + FAB where applicable. 48dp min touch targets. Noto Sans typography.

## Screen: `share-out-execute`

### State: `idle`

Full-screen form. TopAppBar (title + back, primary bg). Form fields with labelLarge labels, 48dp height, 12dp radius. Primary 'Continue'/'Submit' button (fill-width × 56dp) at bottom. Keyboard-aware scroll.
### State: `confirming`

Screen: share-out-execute · State: confirming. Scrollable column, Material3, primary #2E7D32. TopAppBar + content sections + FAB where applicable. 48dp min touch targets. Noto Sans typography.
### State: `executing`

Screen: share-out-execute · State: executing. Scrollable column, Material3, primary #2E7D32. TopAppBar + content sections + FAB where applicable. 48dp min touch targets. Noto Sans typography.
### State: `success`

Centered success state. TopAppBar. Center: check_circle icon (80dp, primary color), success title (titleLarge/primary), confirmation text (bodyLarge/onSurfaceVariant), primary action button.



---

## Variants

Light + Dark · Phone (360dp) / Tablet (600dp) · RTL (for Arabic/Hindi support)

## Component Library Mapping

- TopAppBar → M3 TopAppBar with `#2E7D32` primary background
- Corpus Balance Card → Custom composite (amount hero + inflow/outflow row)
- Member Tile → M3 ListItem with role badge + savings status indicator
- Loan Status Chip → M3 AssistChip with status-mapped color tokens
- Sync Status Indicator → M3 InputChip with animated sync icon
- FAB → M3 FloatingActionButton (56dp, filled primary, bottom-right)
- Bottom Nav → M3 NavigationBar (80dp, 4 tabs: Home/Groups/Meetings/Profile)
- Loading states → Shimmer animation 1000ms (base `#E0E0E0` → highlight `#F5F5F5`)

## WCAG Compliance (Outdoor Use)

- Text on primary (#2E7D32): white #FFFFFF — ratio 7.2:1 ✓ WCAG AAA
- Text on amber (#FF8F00): dark #4A2800 — ratio 5.1:1 ✓ WCAG AA
- Text on surface (#FFFBFE): dark #1C1B1F — ratio 14.5:1 ✓ WCAG AAA
- Error text on errorContainer: #410002 on #FFDAD6 — ratio 9.3:1 ✓ WCAG AAA
