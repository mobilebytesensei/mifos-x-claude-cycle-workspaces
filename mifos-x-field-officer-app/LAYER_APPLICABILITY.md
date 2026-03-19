# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/LAYER_APPLICABILITY.md"
# last_modified: "2026-03-19"

# Layer Applicability Reference

> **Purpose**: Comprehensive reference for which layers apply to each project type
> **Rule**: RULE-LAYER-APPLICABLE-001

---

## Quick Reference

| Layer | KMP | Web | Backend |
|-------|:---:|:---:|:-------:|
| design-spec-layer | ✅ | ✅ | ✅ |
| plan-layer | ✅ | ✅ | ✅ |
| server-layer | ✅ | ✅ | ✅ |
| client-layer | ✅ | ✅ | ❌ |
| feature-layer | ✅ | ✅ | ❌ |
| infrastructure-layer | ✅ | ❌ | ❌ |
| platform-layer | ✅ | ❌ | ❌ |
| testing-layer | ✅ | ✅ | ✅ |

---

## Layer Details by Project Type

### Universal Layers (All Project Types)

These layers are applicable to ALL project types (kmp, web, backend):

#### design-spec-layer
| Project Type | Contents |
|--------------|----------|
| **KMP** | Feature specs, user flows, mockups (mobile/desktop screens) |
| **Web** | Feature specs, user flows, mockups (web pages) |
| **Backend** | API specs, data models, flow diagrams |

#### plan-layer
| Project Type | Contents |
|--------------|----------|
| **KMP** | Implementation plans, version plans |
| **Web** | Implementation plans, version plans |
| **Backend** | Implementation plans, version plans |

#### server-layer
| Project Type | Contents |
|--------------|----------|
| **KMP** | API documentation for consumed backend |
| **Web** | API documentation for consumed backend |
| **Backend** | **PRIMARY** - API implementation, database schema, endpoints |

#### testing-layer
| Project Type | Contents |
|--------------|----------|
| **KMP** | Unit tests, UI tests, integration tests |
| **Web** | Unit tests, component tests, E2E tests |
| **Backend** | API tests, integration tests, load tests |

---

### Client-Consuming Layers (KMP + Web)

These layers are only applicable to projects that CONSUME a backend:

#### client-layer
| Project Type | Contents | Why Not Backend |
|--------------|----------|-----------------|
| **KMP** | Ktorfit services, repositories, DTOs | Backend IS the API, doesn't consume one |
| **Web** | Fetch/Axios services, repositories, types | Backend IS the API, doesn't consume one |
| **Backend** | ❌ N/A | Backend projects don't have client layers |

#### feature-layer
| Project Type | Contents | Why Not Backend |
|--------------|----------|-----------------|
| **KMP** | ViewModels, Compose screens, navigation | Backend has no UI |
| **Web** | React/Vue components, pages, routing | Backend has no UI |
| **Backend** | ❌ N/A | Backend projects don't have UI |

---

### KMP-Only Layers

These layers are ONLY applicable to Kotlin Multiplatform projects:

#### infrastructure-layer
| Project Type | Contents | Why KMP Only |
|--------------|----------|--------------|
| **KMP** | build-logic, cmp-navigation, Koin composition | KMP-specific build system and DI |
| **Web** | ❌ N/A | Web uses npm/webpack, different architecture |
| **Backend** | ❌ N/A | Backend uses simple build, no navigation |

#### platform-layer
| Project Type | Contents | Why KMP Only |
|--------------|----------|--------------|
| **KMP** | expect/actual declarations, platform dispatchers | KMP's multiplatform mechanism |
| **Web** | ❌ N/A | Web is single-platform (browser) |
| **Backend** | ❌ N/A | Backend is single-platform (server) |

---

## Applicability Matrix

### By Project Type

**KMP Projects (8 layers)**:
```
design-spec-layer/
plan-layer/
server-layer/
client-layer/
feature-layer/
infrastructure-layer/
platform-layer/
testing-layer/
```

**Web Projects (6 layers)**:
```
design-spec-layer/
plan-layer/
server-layer/
client-layer/
feature-layer/
testing-layer/
```

**Backend Projects (4 layers)**:
```
design-spec-layer/
plan-layer/
server-layer/        ← PRIMARY layer
testing-layer/
```

---

## Command Applicability

| Command | KMP | Web | Backend |
|---------|:---:|:---:|:-------:|
| `/design` | ✅ | ✅ | ✅ |
| `/server` | ✅ | ✅ | ✅ |
| `/client` | ✅ | ✅ | ❌ |
| `/feature` | ✅ | ✅ | ❌ |
| `/implement` | ✅ | ✅ | ✅ (routes to /backend-implement) |
| `/kmp-implement` | ✅ | ❌ | ❌ |
| `/web-implement` | ❌ | ✅ | ❌ |
| `/backend-implement` | ❌ | ❌ | ✅ |
| `/ai-agent-platform` | ✅ | ❌ | ❌ |

---

## Error Handling

When a command targets a non-applicable layer:

### Error Message Format
```
╔════════════════════════════════════════════════════════════════╗
║  ❌ LAYER NOT APPLICABLE                                        ║
╠════════════════════════════════════════════════════════════════╣
║  {Layer} layer is not applicable for {project_type} projects.   ║
║                                                                  ║
║  For {project_type} projects, use:                               ║
║  • {applicable_command_1}                                        ║
║  • {applicable_command_2}                                        ║
╚════════════════════════════════════════════════════════════════╝
```

### Examples

**Running `/client` on backend project:**
```
❌ Client layer is not applicable for backend projects.

Backend projects use:
• /server - API endpoints and database schema
• /design - Feature specifications
```

**Running `/feature` on backend project:**
```
❌ Feature layer is not applicable for backend projects.

Backend projects use:
• /server - API endpoints and business logic
• /design - Feature specifications
```

**Running `/ai-agent-platform` on web project:**
```
❌ Platform layer is not applicable for web projects.

Web projects use:
• /web-feature - React/Vue components
• /web-client - API services
```

---

## /project-add Behavior

When creating a new project with `/project-add`:

1. **Determine project_type** from user input or source analysis
2. **Filter layers** based on applicability matrix
3. **Create only applicable layer directories**
4. **Log skipped layers** in output

### Example Output
```
╔════════════════════════════════════════════════════════════════╗
║  PROJECT LAYERS                                                 ║
╠════════════════════════════════════════════════════════════════╣
║  Project Type:      backend                                     ║
║  Applicable Layers: 4 (design-spec, plan, server, testing)     ║
║  Skipped Layers:    4 (client, feature, infrastructure, platform)║
╚════════════════════════════════════════════════════════════════╝
```

---

## Related

| File | Purpose |
|------|---------|
| `PROJECT_TYPES.md` | Project type taxonomy |
| `RULE-LAYER-APPLICABLE-001.md` | Enforcement rule |
| `/project-add` | Layer creation command |
| `/projectstatus` | Shows applicable layers |
