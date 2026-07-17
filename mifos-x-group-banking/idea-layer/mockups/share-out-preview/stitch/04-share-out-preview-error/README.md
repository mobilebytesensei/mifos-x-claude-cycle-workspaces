# share-out-preview — error state

| Field | Value |
|-------|-------|
| Feature | share-out-preview |
| State | error |
| Screen ID | 933776e3a87d4a67909432c48de1e219 |
| Project ID | 10006374793896725042 |
| Design System ID | 17261554270924114992 |
| Generated At | 2026-07-17T05:49:12.709Z |
| HTML Downloaded | Yes |
| PNG Downloaded | Yes |
| Figma Export | — |
| Stitch Screen | [View](https://stitch.google.com/projects/10006374793896725042/screens/933776e3a87d4a67909432c48de1e219) |
| Attempts | 1 |

## Files

- `code.html` — Stitch-generated HTML mockup
- `screen.png` — Screenshot of the generated screen

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features share-out-preview --force
```