# FIGMA_LINKS.md — offline-sync-engine

<!-- schema: v3.2 | generated: 2026-08-03T15:05:25.193Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T15:05:25.193Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| idle | 76c1081edff7401ea68971aa0440a744 | 01-offline-sync-engine-idle | PNG ✅ | HTML ✅ | ♻ resumed |
| content | 477bb1e071db49e495960ed4e4063156 | 02-offline-sync-engine-content | PNG ✅ | HTML ✅ | ♻ resumed |
| syncing | b4ffdf32d7a144ee9685e4b5f0b3f813 | 03-offline-sync-engine-syncing | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | 0cce3d3672f34a2a9f5aff3eb182101d | 04-offline-sync-engine-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| error | 7ef81d1f9af64f38b9bfbe26a56669ae | 05-offline-sync-engine-error | PNG ✅ | HTML ✅ | ♻ resumed |
| no_network | 7d4905c50c3b4f23944fd4e32421ac46 | 06-offline-sync-engine-no_network | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| idle | [Open](https://stitch.google.com/projects/10243803383444073820/screens/76c1081edff7401ea68971aa0440a744) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/477bb1e071db49e495960ed4e4063156) | — |
| syncing | [Open](https://stitch.google.com/projects/10243803383444073820/screens/b4ffdf32d7a144ee9685e4b5f0b3f813) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/0cce3d3672f34a2a9f5aff3eb182101d) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/7ef81d1f9af64f38b9bfbe26a56669ae) | — |
| no_network | [Open](https://stitch.google.com/projects/10243803383444073820/screens/7d4905c50c3b4f23944fd4e32421ac46) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features offline-sync-engine --force
```