# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/mockup-tools/TOOL_CONFIG.md"
# last_modified: "2026-03-19"

# Mockup Tool Configuration

**Project:** mobile-wallet
**Primary Tool:** Google Stitch
**Fallback Tools:** Figma AI, Uizard, Visily

---

## Tool Selection

### Google Stitch (Primary)
**When to use:** Final production mockups with exact MD3 specs
**Input:** PROMPTS_STITCH.md (precise measurements)
**Output:** Figma files with design tokens
**MCP Support:** ✅ Yes (google-stitch-mcp)

### Figma AI (Secondary)
**When to use:** Quick iterations and concept exploration
**Input:** PROMPTS_FIGMA.md (natural language)
**Output:** Figma frames (needs refinement)
**MCP Support:** ✅ Yes (figma-mcp)

### Uizard (Fallback)
**When to use:** Rapid prototyping from screenshots/sketches
**Input:** Image uploads + text descriptions
**Output:** Editable mockups

### Visily (Fallback)
**When to use:** Wireframes and low-fidelity mockups
**Input:** Text descriptions
**Output:** SVG wireframes

---

## Prompt Format Selection

| Tool | Prompt File | Format |
|------|-------------|--------|
| Google Stitch | PROMPTS_STITCH.md | MD3 specs (dp, sp, hex) |
| Figma AI | PROMPTS_FIGMA.md | Natural language |
| Uizard | PROMPTS_FIGMA.md | Natural language |
| Visily | PROMPTS_FIGMA.md | Natural language |

---

## Integration Commands

```bash
# Generate mockups with Google Stitch
/mockup {{feature}} --tool=stitch

# Generate with Figma AI
/mockup {{feature}} --tool=figma

# Generate with all tools (comparison)
/mockup {{feature}} --all
```

---

## Design Token Export

**Source:** Google Stitch design system
**Format:** design-tokens.json (Stitch v2.0)
**Target:** Compose DesignToken object

**Export workflow:**
1. Design in Google Stitch with design system
2. Export tokens via plugin
3. Save to mockup-tools/design-tokens.json
4. Map to Compose (see compose_mapping section)

---

## MCP Server Setup

### Google Stitch MCP
```json
{
  "mcpServers": {
    "google-stitch": {
      "command": "npx",
      "args": ["-y", "@google/stitch-mcp"]
    }
  }
}
```

### Figma MCP
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_TOKEN}"
      }
    }
  }
}
```

---

## Tool Comparison

| Feature | Google Stitch | Figma AI | Uizard | Visily |
|---------|:-------------:|:--------:|:------:|:------:|
| MD3 Specs | ✅ | ⚠️ | ❌ | ❌ |
| Natural Language | ⚠️ | ✅ | ✅ | ✅ |
| Design Tokens | ✅ | ✅ | ❌ | ❌ |
| Compose Export | ✅ | ⚠️ | ❌ | ❌ |
| MCP Support | ✅ | ✅ | ❌ | ❌ |
| Speed | Fast | Instant | Fast | Fast |
| Quality | High | Medium | Medium | Low |

---

## Best Practices

1. **Start with Google Stitch**
   - Use for all production mockups
   - Ensures MD3 compliance
   - Exports clean design tokens

2. **Use Figma AI for Exploration**
   - Quick concept validation
   - Iterate on design ideas
   - Refine in Google Stitch later

3. **Keep Both Prompts Updated**
   - Maintain PROMPTS_FIGMA.md and PROMPTS_STITCH.md
   - Same screens, different formats
   - Enables tool switching

4. **Export Tokens Regularly**
   - Update design-tokens.json after design changes
   - Sync with development team
   - Keep Compose mapping current

---

## File Organization

```
mockup-tools/
├── design-tokens.json       # MD3 token system (don't edit manually)
├── TOOL_CONFIG.md          # This file (tool selection guide)
└── .figma-token            # Figma API token (gitignored)

features/{feature}/mockups/
├── MOCKUP.md               # Mockup index and status
├── dummy/                  # Skeleton placeholders (empty PNGs)
│   ├── 01-screen-name.png
│   └── ...
├── prod/                   # Actual mockups (production ready)
│   ├── 01-screen-name.png
│   └── ...
├── PROMPTS_FIGMA.md        # Natural language (for Figma AI)
├── PROMPTS_STITCH.md       # MD3 specs (for Google Stitch)
└── FIGMA_LINKS.md          # Links to Figma files
```

---

## Troubleshooting

**Issue:** Google Stitch MCP not working
**Solution:** Install with `npx -y @google/stitch-mcp` and verify package exists

**Issue:** Figma AI prompts too vague
**Solution:** Use PROMPTS_STITCH.md for exact specs, then convert to natural language

**Issue:** Design tokens not updating
**Solution:** Re-export from Google Stitch, check compose_mapping section

**Issue:** Mockups don't match implementation
**Solution:** Review design-tokens.json, ensure Compose code uses MaterialTheme correctly
