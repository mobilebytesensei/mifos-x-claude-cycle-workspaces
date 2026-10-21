# FIGMA_LINKS.md — consent-manager

<!-- schema: v3.2 | generated: 2026-05-30T06:50:33.771Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-30T06:50:29.485Z |
| Success | 5/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 51e9efbbb7734aba8c5ae5ba691c9000 | 01-consent-manager-loading | PNG ✅ | HTML ✅ | ✅ generated |
| populated | d06f3118633e45758be22b4ccb217082 | 02-consent-manager-populated | PNG ✅ | HTML ✅ | ✅ generated |
| content | — | 03-consent-manager-content | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |
| empty | cbc0b672f1734c2d9b0ca28109136c9d | 04-consent-manager-empty | PNG ✅ | HTML ✅ | ✅ generated |
| revoke_confirm | 296f88d3148645858beabb46646283db | 05-consent-manager-revoke_confirm | PNG ✅ | HTML ✅ | ✅ generated |
| error | 26eac2877bdc4432a8ef5f31aec13eb3 | 06-consent-manager-error | PNG ✅ | HTML ❌ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/51e9efbbb7734aba8c5ae5ba691c9000) | — |
| populated | [Open](https://stitch.google.com/projects/17153754672098888646/screens/d06f3118633e45758be22b4ccb217082) | — |
| content | — | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/cbc0b672f1734c2d9b0ca28109136c9d) | — |
| revoke_confirm | [Open](https://stitch.google.com/projects/17153754672098888646/screens/296f88d3148645858beabb46646283db) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/26eac2877bdc4432a8ef5f31aec13eb3) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features consent-manager --force
```