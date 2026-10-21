<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.

## Code style: comments (user directive, 2026-06-07 — HARD RULE)

When writing or editing source code in this workspace (all `source/` repos, all languages):

- **NEVER add `//` line comments.** No end-of-line comments, no `// explanation` above statements, no commented-out code.
- **The ONLY permitted comment form is `/** … */` KDoc** on declarations (classes, functions, properties, files). If something inside a function body needs explaining, explain it in the declaration's KDoc instead — or restructure the code so it doesn't need explaining (extract a well-named function/val).
- License headers stay as-is (`/* … */` block at file top).
- Scope: applies to NEW and EDITED code. Do NOT mass-rewrite existing `//` comments in untouched code; remove/convert them only in lines you are already changing.
- **KDoc quality bar**: a KDoc must read as documentation, not a relocated `//` comment. First line = a short summary of WHAT the declaration is/does; body = the behavior contract in terms of its parameters (use `[param]` links). No design-session context ("like the reference design", "per the screenshot"), no narration of internals the caller can't observe.
