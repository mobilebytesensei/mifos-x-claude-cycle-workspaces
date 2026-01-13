# Plan Layer

**Purpose:** Versioned planning for features, enhancements, and bug fixes

---

## Structure

```
plan-layer/
├── README.md              # This file
├── PLANS_INDEX.md         # O(1) lookup for all plans
├── VERSION_INDEX.md       # Version timeline
└── versions/
    ├── v0.1.0/
    │   └── PLAN.md        # Plan for v0.1.0
    ├── v0.2.0/
    │   └── PLAN.md        # Plan for v0.2.0
    └── backlog/
        └── FEATURES.md    # Future feature ideas
```

---

## Workflow

### 1. Create New Plan

```bash
/plan create v0.2.0
```

**What happens:**
- Creates `versions/v0.2.0/PLAN.md` from template
- Prompts for plan details (features, APIs, mockup states)
- Updates PLANS_INDEX.md
- Sets status to "Draft"

### 2. Define Requirements

Edit `versions/v0.2.0/PLAN.md`:

**Required Sections:**
- Features to build (with priorities)
- Design layer requirements (SPEC, API, mockups)
- Server layer requirements (Supabase RPCs or REST endpoints)
- Implementation phases
- Success criteria

### 3. Approve Plan

```bash
/plan approve v0.2.0
```

**What happens:**
- Changes status from "Draft" to "Approved"
- Triggers design layer generation

### 4. Generate Design Layer

```bash
/design from-plan v0.2.0
```

**What happens:**
- Reads plan requirements
- Generates complete design layer for each feature:
  - SPEC.md
  - API.md
  - STATUS.md
  - MOCKUP.md
  - mockups/PROMPTS_FIGMA.md
  - mockups/PROMPTS_STITCH.md
  - mockups/FIGMA_LINKS.md
- Updates design layer indexes
- Marks plan as "Design Generated"

### 5. Implement

```bash
/gap-implement-project
```

**What happens:**
- Checks server APIs (generates RPCs for Supabase)
- Implements client layer
- Implements feature layer
- Implements tests

### 6. Mark Complete

When all features implemented:
- Update plan status to "Implemented"
- Update PLANS_INDEX.md
- Create next version plan if needed

---

## Versioning

**Semantic Versioning:** MAJOR.MINOR.PATCH

- **Major (1.0.0)**: Breaking changes, new architecture
- **Minor (0.1.0)**: New features, backward compatible
- **Patch (0.0.1)**: Bug fixes, minor improvements

**Examples:**
- `v0.1.0`: Initial features
- `v0.2.0`: Add social features
- `v0.2.1`: Fix login bug
- `v1.0.0`: Production release

---

## Plan Template

Located at: `versions/PLAN_TEMPLATE.md`

**Placeholders:**
- `{{VERSION}}`: Plan version (e.g., 0.2.0)
- `{{FEATURE_SET_NAME}}`: Plan name (e.g., "Social features")
- `{{DATE}}`: Creation date
- `{{GOAL}}`: What this version achieves
- `{{MOTIVATION}}`: Why these features
- `{{TARGET_USERS}}`: Who benefits
- `{{feature}}`, `{{resource}}`, `{{table_name}}`: Feature-specific

---

## Plan Statuses

| Status | Meaning |
|:------:|---------|
| 📝 Draft | Plan being written, not approved |
| ✅ Approved | Plan reviewed and approved, ready for design generation |
| 🎨 Design Generated | Design layer created from plan |
| 🔄 In Progress | Implementation underway |
| ✅ Implemented | All features implemented and tested |
| ⚠️ Blocked | Waiting on dependencies |
| ❌ Cancelled | No longer needed |

---

## Integration with Design Layer

**Flow:**
```
Plan v0.2.0 (Approved)
    ↓
/design from-plan v0.2.0
    ↓
design-spec-layer/features/
    ├── feature1/
    │   ├── SPEC.md (from plan)
    │   ├── API.md (from plan API endpoints)
    │   ├── STATUS.md (initial status)
    │   ├── MOCKUP.md
    │   └── mockups/
    │       ├── PROMPTS_FIGMA.md
    │       ├── PROMPTS_STITCH.md
    │       └── FIGMA_LINKS.md
    └── feature2/
        └── [same structure]
```

---

## Best Practices

1. **Plan Before Implementing**
   - Always create a plan before adding features
   - Get stakeholder approval on plan before coding

2. **Be Specific**
   - Define exact API endpoints
   - List all mockup states (success, loading, empty, error)
   - Specify success criteria

3. **Version Incrementally**
   - Don't plan too many features in one version
   - 3-7 features per version is ideal
   - Smaller versions ship faster

4. **Update Status**
   - Keep PLANS_INDEX.md current
   - Mark features complete as you go
   - Document blockers

5. **Review Before Approval**
   - Validate all requirements clear
   - Check API endpoints are complete
   - Ensure mockup states defined

---

## Commands

| Command | Purpose |
|---------|---------|
| `/plan create v{VERSION}` | Create new versioned plan |
| `/plan approve v{VERSION}` | Approve plan for implementation |
| `/design from-plan v{VERSION}` | Generate design layer from plan |
| `/gap-analysis plan` | Check plan coverage and status |

---

## Example Plan

See: `versions/PLAN_TEMPLATE.md`

**Sample v0.1.0 (Initial Features):**
- Features: auth, home, profile, settings
- APIs: 12 endpoints (4 CRUD sets)
- Mockup states: 4 per screen (success, loading, empty, error)
- Implementation: 4 phases
- Success criteria: 5 checkpoints

**Sample v0.2.0 (Social Features):**
- Features: comments, likes, follows, notifications
- APIs: 8 endpoints
- Mockup states: 4 per screen
- Implementation: 3 phases
- Success criteria: 4 checkpoints
