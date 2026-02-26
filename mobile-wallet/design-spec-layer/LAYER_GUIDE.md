# Design-Spec Layer Guide - mobile-wallet

> Feature specifications, mockups, and design documentation

---

## Layer Purpose

The design-spec layer contains all design documentation for mobile-wallet:
- Feature specifications (SPEC.md)
- API requirements (API.md)
- Implementation status (STATUS.md)
- Mockup prompts (PROMPTS_STITCH.md, PROMPTS_FIGMA.md)
- Design tokens and system

---

## Directory Structure

```
design-spec-layer/
├── FEATURES_INDEX.md       # Feature registry
├── LAYER_GUIDE.md          # This file
├── features/               # Per-feature documentation
│   └── {feature}/
│       ├── SPEC.md         # Feature specification
│       ├── API.md          # API requirements
│       ├── STATUS.md       # Implementation status
│       └── mockups/
│           ├── PROMPTS_STITCH.md
│           └── PROMPTS_FIGMA.md
├── _shared/                # Shared patterns
│   ├── COMPONENTS.md       # Common components
│   └── PATTERNS.md         # UI patterns
├── user-flows/             # User flow diagrams
│   ├── FLOWS_INDEX.md
│   └── flows/
└── design-system/          # Design tokens
    └── design-tokens.json
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/design [feature]` | Generate/update SPEC.md |
| `/mockup [feature]` | Generate mockup prompts |
| `/design-validate` | Validate design compliance |
| `/gap-analysis design` | Check layer gaps |

---

## Feature Spec Template

Each feature should have:

1. **SPEC.md** - Feature requirements and behavior
2. **API.md** - Backend API requirements
3. **STATUS.md** - Implementation tracking
4. **mockups/** - Mockup generation prompts

---

## Related Layers

| Layer | Relationship |
|-------|--------------|
| Server | API.md → API endpoints |
| Client | SPEC.md → Repository methods |
| Feature | SPEC.md → ViewModel/Screen implementation |
