# FIGMA_LINKS.md — client-list

<!-- schema: v3.2 | generated: 2026-08-03T14:50:29.354Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T14:50:29.354Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | c25613827b7f48318036248fde832f68 | 01-client-list-loading | PNG ✅ | HTML ✅ | ♻ resumed |
| content | 3d110a7f782a4483809b16a2e757ecf4 | 02-client-list-content | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | 1c8192754f8c4c06bbc2115586e20c06 | 03-client-list-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| error | bacf45a50f854beaad1459482333890d | 04-client-list-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/c25613827b7f48318036248fde832f68) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/3d110a7f782a4483809b16a2e757ecf4) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/1c8192754f8c4c06bbc2115586e20c06) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/bacf45a50f854beaad1459482333890d) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features client-list --force
```