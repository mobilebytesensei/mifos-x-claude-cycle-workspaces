# release-layer/media/_html — Single source of truth for store screenshots

Per RULE-RELEASE-MEDIA-SINGLE-SOURCE-001. Edit ONE HTML per screen; framework renders
PNGs for all platforms × form factors via `/release [GA]`.

## Layout

```
_html/
├── 01_home.html              ← canonical phone-first source (renders to all phones)
├── 02_loans.html
├── ...
├── tablet_7/01_home.html     ← override for Android 7" tablet (sidebar nav, 2-pane)
├── tablet_10/01_home.html    ← override for Android 10" tablet landscape (split-pane)
├── iphone_6_9/01_home.html   ← override for iPhone 6.9" (iOS chrome, tighter spacing)
├── iphone_6_3/01_home.html   ← override for iPhone 6.3"
├── ipad_13/01_home.html      ← override for iPad Pro 13" (multi-col tablet)
├── macbook/01_home.html      ← override for macOS (window chrome, mouse-optimized)
└── og/01_home.html           ← override for Web OG card (hero shot, 1200×630)
```

## How the renderer picks HTML

For each (screen × form_factor) target in render-targets.yaml:
1. Look for `_html/<form_factor>/<id>.html` — use if present (form-factor-optimized)
2. Else fall back to `_html/<id>.html` (canonical, may render stretched on landscape)

Phone form factors generally render fine from the canonical source (similar viewports).
Landscape and tablet form factors WILL look stretched without overrides — provide
form-factor HTML for production-grade screenshots.

## Rendering

```
/release [GA]                # via /release matrix (preferred)
# or directly:
bash .claude-runtime/scripts/web-debug-bootstrap.sh ensure
bash .claude-runtime/scripts/web-debug-bootstrap.sh run \
  .claude-runtime/scripts/release-media-render.ts
```

40 PNGs (5 screens × 8 form factors) render in ~12 seconds via Playwright headless Chromium.

## Adding a new platform / form factor

1. Add the form factor to render-targets.yaml's target list per screen
2. Renderer picks it up automatically
3. Add HTML override at `_html/<new_form_factor>/<id>.html` for production-grade output

## Provenance

`_rendered/render-log.jsonl` tracks every render run with source sha, target, output dimensions,
render time, and counts. Used by `[GX]` Config completeness for staleness detection.
