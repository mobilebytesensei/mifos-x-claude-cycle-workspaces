# FIGMA_LINKS.md — atm-locator

<!-- schema: v3.2 | generated: 2026-05-30T06:42:21.719Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-30T06:42:21.718Z |
| Success | 5/5 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | ecb52d65ecd8421a9a9cb6736e648b0b | 01-atm-locator-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 34cd38f7d80247ae85d5084910d0e4cb | 02-atm-locator-content | PNG ✅ | HTML ✅ | ✅ generated |
| error | 02b0e07a6a084d84af232426417eda21 | 03-atm-locator-error | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 02b3e687a8f247dd84128b4b9aebc533 | 04-atm-locator-empty | PNG ✅ | HTML ✅ | ✅ generated |
| location_denied | 6afea83396d74364a7a178ebe5af0f31 | 05-atm-locator-location_denied | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/ecb52d65ecd8421a9a9cb6736e648b0b) | — |
| content | [Open](https://stitch.google.com/projects/17153754672098888646/screens/34cd38f7d80247ae85d5084910d0e4cb) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/02b0e07a6a084d84af232426417eda21) | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/02b3e687a8f247dd84128b4b9aebc533) | — |
| location_denied | [Open](https://stitch.google.com/projects/17153754672098888646/screens/6afea83396d74364a7a178ebe5af0f31) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features atm-locator --force
```