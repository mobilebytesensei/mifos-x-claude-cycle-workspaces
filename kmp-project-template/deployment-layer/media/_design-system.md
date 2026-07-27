# Brand & Design System — {{PROJECT_NAME}}

> Edit this file for your fork's brand. Read by `[GB] Bootstrap HTML` alongside
> `_form-factors.md` (framework, immutable) + `_prompt/<id>.md` (per-screen intent).
> The triple drives Claude's HTML generation.

---

## Colors

```yaml
primary:        "#4338CA"      # main brand color (CTA, active states, hero gradient start)
primary_deep:   "#3730A3"      # gradient end, status bars, sidebar bg
background:     "#F0F2F8"      # body bg
surface:        "#FFFFFF"      # card bg
text:           "#0F172A"      # primary text
text_muted:     "#64748B"      # secondary text, labels
text_subtle:    "#94A3B8"      # tertiary, units
border:         "#E2E8F0"      # dividers, slider tracks

# Status / semantic
success:        "#059669"      # green — up trends, on-time bills
success_light:  "#D1FAE5"      # bg tint
warning:        "#D97706"      # amber — due-soon, watch-list
warning_light:  "#FEF3C7"
danger:         "#EF4444"      # red — down trends, overdue
accent_indigo:  "#E0E7FF"      # active-nav pill bg
```

## Typography

```yaml
family:    "-apple-system, 'SF Pro Display', 'Google Sans', Roboto, sans-serif"
hero:      "88px / 900 / -3px tracking"            # net worth, EMI value, etc.
title:     "52px / 900 / -1px tracking"            # screen titles
section:   "32px / 800"                            # section headers
body:      "26-28px / 500-700"                     # paragraph + card text
label:     "24px / 700 / uppercase / 1px tracking" # metric labels, section labels
caption:   "20-22px / 500"                         # status bar, small text
```

## Component patterns

### Card
- bg `surface`, radius 28-36px, padding 32-36px
- shadow `0 2-4px 12-24px rgba(15,23,42,0.06-0.08)`
- never borders (shadow only)

### Hero card (over brand gradient)
- bg `rgba(255,255,255,0.12)` with `border: 1.5px solid rgba(255,255,255,0.2)`
- radius 28px, padding 28-32px
- white text + translucent-white labels

### Metric card (white card with icon)
- icon: 44px (Unicode emoji) above content
- label: 24px / 700 / uppercase / muted
- value: 54px / 900 / -1.5px tracking / primary text
- sub: 25px / 600 / colored (success/warning/danger per trend)

### Bill / list card
- bg `surface`, radius 28px, padding 32-36px
- horizontal layout: left-icon-wrap + name + date | right-amount
- icon-wrap: 56×56 rounded 18px, semantic-tinted bg (`success_light` / `warning_light`)

### Active navigation indicator
- Bottom nav (phone): nav-icon-wrap bg `accent_indigo`, label color `primary`
- Sidebar nav (tablet/desktop): full row bg `rgba(255,255,255,0.18)`, label color `#fff`

### Hero gradient
- `linear-gradient(160deg, {{primary}} 0%, {{primary_deep}} 100%)` for phone hero bars
- `linear-gradient(180deg, {{primary}} 0%, {{primary_deep}} 100%)` for sidebar nav (vertical)

## App identity

```yaml
app_name:       "{{APP_NAME}}"           # e.g. "Money Toolkit"
app_emoji:      "💰"                     # used in avatar / brand-mark slot
tagline:        "{{ONE_LINE_TAGLINE}}"   # OG card subtitle
```

## Navigation items (universal across screens, active marker per screen)

```yaml
nav:
  - { id: home,  label: "Home",  emoji: "🏠" }
  - { id: loans, label: "Loans", emoji: "🏦" }
  - { id: bills, label: "Bills", emoji: "📋" }
  - { id: rates, label: "Rates", emoji: "📈" }
  - { id: tools, label: "Tools", emoji: "🔢" }
```
