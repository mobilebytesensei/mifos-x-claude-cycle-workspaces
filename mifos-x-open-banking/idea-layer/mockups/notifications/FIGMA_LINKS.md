# FIGMA_LINKS.md — notifications

<!-- schema: v3.2 | generated: 2026-05-31T03:34:29.047Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-31T03:34:02.528Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 7ea69a3bac8c43ce9fd530ce2a947bae | 01-notifications-loading | PNG ✅ | HTML ✅ | ✅ generated |
| populated | 1df6d16825c142469a00415294a94862 | 02-notifications-populated | PNG ✅ | HTML ✅ | ✅ generated |
| empty | c2bac30364d3420ca983eb2c7005d358 | 03-notifications-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | 463736cc7d924b6cb2a9cc14ee12d5e9 | 04-notifications-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/7ea69a3bac8c43ce9fd530ce2a947bae) | — |
| populated | [Open](https://stitch.google.com/projects/17153754672098888646/screens/1df6d16825c142469a00415294a94862) | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/c2bac30364d3420ca983eb2c7005d358) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/463736cc7d924b6cb2a9cc14ee12d5e9) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features notifications --force
```