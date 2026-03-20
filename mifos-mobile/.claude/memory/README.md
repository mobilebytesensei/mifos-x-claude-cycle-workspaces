# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/.claude/memory/README.md"
# last_modified: "2026-03-20"

# Session Memory Templates

> Templates for session memory files that persist context across sessions.

---

## Overview

Session memory provides persistent context that survives across sessions. These templates are copied to `{project}/.claude/memory/` when a project initializes its memory system.

---

## Files

| File | Purpose | Format |
|------|---------|--------|
| `session-history.json` | Track last N sessions | JSON array |
| `decisions.md` | Architecture decisions made | Markdown table + details |
| `patterns-used.md` | Patterns applied in project | Markdown table + examples |
| `errors-resolved.md` | Errors and their resolutions | Markdown sections |
| `preferences.json` | Learned user preferences | JSON object |

---

## Usage

### Automatic Setup

Memory is initialized automatically when:
- `/context-start` runs and memory doesn't exist
- `/memory` command is used and memory doesn't exist

### Manual Setup

Copy this directory to your project:
```bash
cp -r templates/workspace-project/.claude/memory/ {project}/.claude/memory/
```

---

## Retention Policies

| File | Max Entries | Max Age | Pruning |
|------|:-----------:|:-------:|---------|
| `session-history.json` | 10 | 30 days | FIFO (oldest first) |
| `decisions.md` | 50 | 90 days | Keep important, prune trivial |
| `patterns-used.md` | 20 | N/A | Prune unused (30+ days) |
| `errors-resolved.md` | 30 | 60 days | Keep prevention-worthy |
| `preferences.json` | 20 | N/A | Never auto-prune |

---

## Integration

Memory integrates with:
- `/context-start` - Loads memory on session start
- `/context-end` - Saves memory on session end
- `/memory` - View and manage memory

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude/commands/memory.md` | Memory command definition |
| `.claude/rules/RULE-MEMORY-001.md` | Memory persistence rules |
