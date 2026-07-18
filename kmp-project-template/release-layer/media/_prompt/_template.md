# {{SCREEN_TITLE}}

> Per-screen INTENT. Read by `[GB] Bootstrap HTML` alongside `_design-system.md` (brand)
> + `_form-factors.md` (layout grammar). Together they drive Claude's HTML composition
> across all (form_factor) variants for this screen.

## User intent

One paragraph: what does the user open this screen to do? What's the hero (the one thing
they came for)? What's secondary (supporting context)?

## Active navigation

```yaml
active_nav: {{home|loans|bills|rates|tools}}
```

## Hero

```yaml
hero:
  label:    "{{e.g. 'Total Outstanding'}}"          # uppercase metric label
  value:    "{{e.g. '$12,450'}}"                     # the big number
  sub:      "{{e.g. 'across 3 active loans'}}"
  trend:    "{{e.g. '↓ $342 this month'}}"           # optional, with semantic icon
  trend_kind: {{success|warning|danger|neutral}}     # picks badge color
```

## Sections

List in render order. Each section can be metrics grid, list, chart, form, CTA, etc.

```yaml
sections:
  - kind: metrics_grid
    cols_phone: 2
    cols_tablet: 4
    items:
      - { icon: "📋", label: "Monthly EMI",   value: "$656",  sub: "2 bills due this week", sub_kind: warning }
      - { icon: "📈", label: "Fed Funds",     value: "5.33%", sub: "↓ −0.01 this week",     sub_kind: danger }
      - { icon: "💱", label: "USD → EUR",     value: "0.9234", sub: "↑ +0.0012 today",       sub_kind: success }
      - { icon: "🏦", label: "30Y Mortgage",  value: "6.85%", sub: "↓ −0.12 this week",     sub_kind: danger }

  - kind: section_header
    title: "Upcoming Bills"
    link: "See all →"

  - kind: list
    items:
      - { icon: "⚡", icon_kind: warning, name: "Electricity Bill", subtitle: "Due in 4 days · Jun 10", amount: "$84.50",  amount_kind: warning }
      - { icon: "🎬", icon_kind: warning, name: "Netflix",          subtitle: "Due in 2 days · Jun 8",  amount: "$15.99",  amount_kind: warning }
      - { icon: "🌐", icon_kind: success, name: "Internet",         subtitle: "Due Jun 15",             amount: "$49.00",  amount_kind: success }

  - kind: cta
    label: "View Amortization Schedule →"             # optional, only some screens
```

## Form-factor hints (optional overrides for specific factors)

If a particular form factor should compose differently than `_form-factors.md` default:

```yaml
form_factor_overrides:
  tablet_10:
    layout_hint: "split-pane: metrics grid left, bills list right"
  ipad_13:
    layout_hint: "show all bills (not just 3); add a small chart in info rail"
  og:
    layout_hint: "use net worth value as the hero number; tagline below"
```

## Real data only

NEVER ship "Lorem ipsum" / "Item 1" / "$0.00" placeholders. Use real demo values from the project's domain context (e.g. realistic loan amounts, actual bill names, sensible dates).

If you need a date, prefer today's month/year computed at render time, with sensible day offsets (e.g. "Due in 4 days" → renders as today + 4).
