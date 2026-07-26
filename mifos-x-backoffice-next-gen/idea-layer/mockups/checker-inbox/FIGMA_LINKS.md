# FIGMA_LINKS.md — checker-inbox

<!-- schema: v3.2 | generated: 2026-07-26T05:25:02.233Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-07-26T05:25:02.169Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 7890e5eb3eb241b3aa86a8b8584c10dd | 01-checker-inbox-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 069a90b5814c41c5b717d8352b3ec78a | 02-checker-inbox-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 61c2a76771524c7086dacaf6f661057c | 03-checker-inbox-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | — | 04-checker-inbox-error | PNG ❌ | HTML ✅ | ⏳ pending |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/7890e5eb3eb241b3aa86a8b8584c10dd) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/069a90b5814c41c5b717d8352b3ec78a) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/61c2a76771524c7086dacaf6f661057c) | — |
| error | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features checker-inbox --force
```