# FIGMA_LINKS.md — share-out-execute

<!-- schema: v3.2 | generated: 2026-07-17T06:03:03.794Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10006374793896725042](https://stitch.google.com/projects/10006374793896725042) |
| Design System ID | 17261554270924114992 |
| Generated | 2026-07-17T06:03:03.788Z |
| Success | 5/5 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| content | 42cdeddbb6fe498f92c828ccee09a55c | 01-share-out-execute-content | PNG ✅ | HTML ✅ | ✅ generated |
| executing | f54f763d176846e7b5cdf1bf42d6aa5d | 02-share-out-execute-executing | PNG ✅ | HTML ✅ | ✅ generated |
| success | 5a48b929fcf44302aee8f24cf5c44648 | 03-share-out-execute-success | PNG ✅ | HTML ✅ | ✅ generated |
| partial_failure | 13a940292b104400845999478bf28757 | 04-share-out-execute-partial_failure | PNG ✅ | HTML ✅ | ✅ generated |
| error | 75d04b242c7e4f96a31e915bc0f30884 | 05-share-out-execute-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| content | [Open](https://stitch.google.com/projects/10006374793896725042/screens/42cdeddbb6fe498f92c828ccee09a55c) | — |
| executing | [Open](https://stitch.google.com/projects/10006374793896725042/screens/f54f763d176846e7b5cdf1bf42d6aa5d) | — |
| success | [Open](https://stitch.google.com/projects/10006374793896725042/screens/5a48b929fcf44302aee8f24cf5c44648) | — |
| partial_failure | [Open](https://stitch.google.com/projects/10006374793896725042/screens/13a940292b104400845999478bf28757) | — |
| error | [Open](https://stitch.google.com/projects/10006374793896725042/screens/75d04b242c7e4f96a31e915bc0f30884) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features share-out-execute --force
```