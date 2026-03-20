# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/.claude/memory/errors-resolved.md"
# last_modified: "2026-03-20"

# Resolved Errors

> Errors encountered and their resolutions for future reference.
> Max entries: 30 | Max age: 60 days

---

## Error Log

<!-- Error entries appear below -->

---

## Schema Reference

```yaml
error_entry:
  id: "ERR-{NNN}"
  date: "YYYY-MM-DD"
  type: "Build | Runtime | Test | Lint"
  feature: "Affected feature"
  message: "Error message (code block)"
  cause: "Root cause analysis"
  resolution: "How it was fixed (with code if applicable)"
  prevention: "How to avoid in future"

entry_format: |
  ### ERR-{NNN}: {Short Description}

  **Date**: {date}
  **Type**: {type}
  **Feature**: {feature}

  **Error Message**:
  ```
  {error_message}
  ```

  **Root Cause**: {cause}

  **Resolution**: {resolution}
  ```kotlin
  // Code fix if applicable
  ```

  **Prevention**: {prevention}
```

---

## Error Categories

| Type | Description | Common Causes |
|------|-------------|---------------|
| Build | Compilation failures | Missing imports, type mismatches, syntax |
| Runtime | Crashes and exceptions | Null access, threading, lifecycle |
| Test | Test failures | Mock setup, assertion failures, timing |
| Lint | Static analysis warnings | Code style, deprecated APIs, security |

---

## Quick Reference Fixes

| Error Pattern | Common Fix |
|---------------|------------|
| Unresolved reference | Check imports, verify dependency |
| NPE | Use safe call operator (?.), check nullability |
| Coroutine scope | Use viewModelScope, lifecycleScope |
| Compose recomposition | Use remember, derivedStateOf |

---

## Related Files

| File | Purpose |
|------|---------|
| `decisions.md` | Decisions made to prevent errors |
| `RULE-MEMORY-001.md` | Memory persistence rules |
