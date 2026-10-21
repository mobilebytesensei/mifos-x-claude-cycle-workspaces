# FIGMA_LINKS.md — standing-orders

<!-- schema: v3.2 | generated: 2026-05-30T06:01:02.624Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-30T06:01:02.624Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | fa6ffd49a6384ace84019114a53f08f1 | 01-standing-orders-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 29a0b3ea98f04841aa7c22c4812ae242 | 02-standing-orders-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 8d9b7ed13a624521ad3c92c7d472ac90 | 03-standing-orders-empty | PNG ✅ | HTML ✅ | ✅ generated |
| error | 2196a3c0dcd044aa9981659ba8a4c3e9 | 04-standing-orders-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/fa6ffd49a6384ace84019114a53f08f1) | — |
| content | [Open](https://stitch.google.com/projects/17153754672098888646/screens/29a0b3ea98f04841aa7c22c4812ae242) | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/8d9b7ed13a624521ad3c92c7d472ac90) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/2196a3c0dcd044aa9981659ba8a4c3e9) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features standing-orders --force
```