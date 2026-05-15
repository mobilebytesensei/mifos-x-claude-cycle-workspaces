# Responsive Layouts — mifos-x-group-banking

## Target Devices

Primary: Android 5–6" screens, 360dp width. Low-end to mid-range (2–3GB RAM).
Secondary: 7" tablets (field officers using tablets for cross-group view).

## Layout Strategy

**Phone (360–420dp wide):**
- Single-column layout throughout
- Cards full-width with 16dp horizontal margin
- Lists: no grid — linear scrolling for scanability
- Bottom navigation: 5 tabs

**Tablet (600dp+ wide):**
- Two-panel layout: navigation rail (left) + content (right)
- Member list | member detail side-by-side on tablet
- Meeting conduct: attendance list | summary panel side-by-side

## Key Layout Rules

1. **No horizontal scrolling** — all content fits in one column on 360dp
2. **KES amounts** — right-aligned, monospace, 20sp+ for outdoor readability
3. **Meeting conduct inputs** — full-width inputs, 56dp height (larger than standard 48dp)
4. **FAB placement** — bottom-right, 16dp from edges, 72dp from bottom nav
5. **Bottom sheet** — used for loan repayment, meeting summary details (avoids full navigation for quick actions)
