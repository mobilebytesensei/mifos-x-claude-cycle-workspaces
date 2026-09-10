# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/plan-layer/versions/PLAN_TEMPLATE.md"
# last_modified: "2026-03-19"

# PLAN-{{SCOPE}}-{{YYMMDD}}-{{HHmmss}}: {{FEATURE_SET_NAME}}

> **Plan ID**: {{SCOPE}}-{{YYMMDD}}-{{HHmmss}}
> **Status**: Draft
> **Type**: Framework | Project
> **Priority**: P0 | P1 | P2
> **Created**: 2026-08-15
> **Version**: v{{VERSION}}
> **Target Layers**: Design, Server, Client, Feature

---

## 1. Overview

**Goal:** {{GOAL}}

**Motivation:** {{MOTIVATION}}

**Target Users:** {{TARGET_USERS}}

---

## 2. Features to Build

| # | Feature | Priority | Complexity | Estimated Effort |
|:-:|---------|:--------:|:----------:|:----------------:|
| 1 | {{feature-name}} | P0/P1/P2 | Low/Med/High | S/M/L/XL |

---

## 3. Design Layer Requirements

### 3.1 Features to Generate

For each feature, design layer should create:
- SPEC.md with screens, ViewModels, user stories
- API.md with endpoints and DTOs
- STATUS.md with layer progress matrix
- MOCKUP.md with ASCII diagrams
- mockups/PROMPTS_FIGMA.md (natural language)
- mockups/PROMPTS_STITCH.md (MD3 specifications)
- mockups/FIGMA_LINKS.md (link tracker)

### 3.2 API Endpoints

| Feature | Endpoint | Method | Purpose |
|---------|----------|:------:|---------|
| {{feature}} | /api/v1/{{resource}} | GET | List items |
| {{feature}} | /api/v1/{{resource}}/:id | GET | Get single |
| {{feature}} | /api/v1/{{resource}} | POST | Create |
| {{feature}} | /api/v1/{{resource}}/:id | PUT | Update |
| {{feature}} | /api/v1/{{resource}}/:id | DELETE | Delete |

### 3.3 Mockup States

For each feature screen:
- Success (with data)
- Loading (shimmer/skeleton)
- Empty (no data message)
- Error (with retry)
- Offline (cached data)

---

## 4. Server Layer Requirements

### 4.1 For Supabase Projects

**Tables:**
- {{table_name}} (columns: id, {{fields...}}, created_at, updated_at)

**RPCs:**
- rpc_get_{{resource_plural}}(p_limit, p_offset) → List
- rpc_get_{{resource}}_by_id(p_id) → Single
- rpc_create_{{resource}}(p_fields...) → Created ID
- rpc_update_{{resource}}(p_id, p_fields...) → Success
- rpc_delete_{{resource}}(p_id) → Success

**Triggers:** Auto-generation via CRUD engine when API.md changes

### 4.2 For REST API Projects

**Endpoints to Document:**
- GET /api/v1/{{resource}} (pagination, filters)
- POST /api/v1/{{resource}} (request/response DTOs)
- PUT /api/v1/{{resource}}/:id
- DELETE /api/v1/{{resource}}/:id

---

## 5. Implementation Phases

| Phase | Description | Commands | Auto-Triggers |
|:-----:|-------------|----------|---------------|
| 1 | Plan approval | Manual | - |
| 2 | Design generation | /design from-plan v{{VERSION}} | Auto after approval |
| 3 | Server CRUD | /server sync-apis | Auto on API.md changes |
| 4 | Client layer | /gap-implement client | - |
| 5 | Feature layer | /gap-implement feature | - |
| 6 | Testing | /gap-implement testing | - |

---

## 6. Success Criteria

- [ ] All features have complete design layer (8 files each)
- [ ] Server APIs documented and (for Supabase) RPCs generated
- [ ] Client services implement all design layer APIs
- [ ] Feature layer matches mockups
- [ ] Tests cover critical paths
- [ ] All O(1) indexes updated

---

## 7. Version History

| Version | Date | Changes |
|:-------:|------|---------|
| v{{VERSION}} | 2026-08-15 | Initial plan |
