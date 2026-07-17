# FIGMA_LINKS.md — login-signup

<!-- schema: v3.2 | generated: 2026-07-17T05:36:04.123Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [9052414241695514723](https://stitch.google.com/projects/9052414241695514723) |
| Design System ID | 17261554270924114992 |
| Generated | 2026-07-17T05:36:04.119Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| content | b70be90fdf8f4f669bed0a7d2595963c | 01-login-signup-content | PNG ✅ | HTML ✅ | ✅ generated |
| loading | 32559f5e9fbe4fb8a3a24595157eebaf | 02-login-signup-loading | PNG ✅ | HTML ✅ | ✅ generated |
| error | 3be6097bca2548e29aeb5a8d7531f005 | 03-login-signup-error | PNG ✅ | HTML ✅ | ✅ generated |
| zero_groups | 3a3a486069dd41b6810a6e835de3bcaf | 04-login-signup-zero_groups | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| content | [Open](https://stitch.google.com/projects/9052414241695514723/screens/b70be90fdf8f4f669bed0a7d2595963c) | — |
| loading | [Open](https://stitch.google.com/projects/9052414241695514723/screens/32559f5e9fbe4fb8a3a24595157eebaf) | — |
| error | [Open](https://stitch.google.com/projects/9052414241695514723/screens/3be6097bca2548e29aeb5a8d7531f005) | — |
| zero_groups | [Open](https://stitch.google.com/projects/9052414241695514723/screens/3a3a486069dd41b6810a6e835de3bcaf) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features login-signup --force
```