# FIGMA_LINKS.md — about

<!-- schema: v3.2 | generated: 2026-05-30T06:39:08.639Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-30T06:39:08.638Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | cad5070ca5da4cd1ae3ad3702f84e4de | 01-about-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 3cfab35cf63743fb889516c02d4caaf9 | 02-about-content | PNG ✅ | HTML ✅ | ✅ generated |
| error | f092d8c596af41fa9a70f672156425dd | 03-about-error | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 675bf8463ac140e6bccffbabe809a70c | 04-about-empty | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/cad5070ca5da4cd1ae3ad3702f84e4de) | — |
| content | [Open](https://stitch.google.com/projects/17153754672098888646/screens/3cfab35cf63743fb889516c02d4caaf9) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/f092d8c596af41fa9a70f672156425dd) | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/675bf8463ac140e6bccffbabe809a70c) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features about --force
```