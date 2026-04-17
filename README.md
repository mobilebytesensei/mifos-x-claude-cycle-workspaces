# Mifos X Claude Cycle Workspaces

Project workspaces for Mifos X ecosystem projects using [claude-product-cycle](https://github.com/mobilebytesensei/claude-product-cycle) framework.

## Projects

| Project | Description | Source | Status |
|---------|-------------|--------|:------:|
| `mifos-mobile/` | KMP Self-Service Mobile Banking App | [openMF/mifos-mobile](https://github.com/openMF/mifos-mobile) | Active |
| `mobile-wallet/` | KMP Mobile Wallet / Mifos Pay | [openMF/mobile-wallet](https://github.com/openMF/mobile-wallet) | Active |
| `mifos-x-field-officer-app/` | KMP Field Officer Android App | [openMF/mifos-x-field-officer-app](https://github.com/openMF/mifos-x-field-officer-app) | Active |
| `kmp-project-template/` | KMP Project Template (shared scaffold) | [openMF/kmp-project-template](https://github.com/openMF/kmp-project-template) | Active |

## Quick Start

### Option 1: Via Framework (Recommended)

```bash
# Clone framework with all workspaces
git clone --recursive git@github.com:mobilebytesensei/claude-product-cycle.git
cd claude-product-cycle

# Run setup script
./setup.sh
```

### Option 2: Clone This Workspace Directly

```bash
# Clone with submodules
git clone --recursive git@github.com:mobilebytesensei/mifos-x-claude-cycle-workspaces.git

# Or clone and init submodules separately
git clone git@github.com:mobilebytesensei/mifos-x-claude-cycle-workspaces.git
cd mifos-x-claude-cycle-workspaces
git submodule update --init --recursive
```

## Structure

```
mifos-x-claude-cycle-workspaces/
├── README.md
├── WORKSPACES_INDEX.md
├── mifos-mobile/
│   ├── PROJECT.md                 # Project configuration
│   ├── idea-layer/                # Source of truth (screens, flows, requirements)
│   ├── design-spec-layer/         # Feature specifications, mockups
│   ├── server-layer/              # API documentation (Fineract)
│   ├── client-layer/              # Network/data layer tracking
│   ├── feature-layer/             # UI layer tracking
│   ├── infrastructure-layer/      # Build config, navigation, DI
│   ├── platform-layer/            # Platform-specific (Android/iOS)
│   ├── testing-layer/             # Test tracking
│   └── source/mifos-mobile        # Git submodule → openMF/mifos-mobile
├── mobile-wallet/
│   ├── PROJECT.md
│   ├── idea-layer/
│   ├── design-spec-layer/
│   ├── client-layer/
│   ├── feature-layer/
│   └── source/mobile-wallet       # Git submodule → openMF/mobile-wallet
├── mifos-x-field-officer-app/
│   ├── PROJECT.md
│   ├── idea-layer/
│   ├── design-spec-layer/
│   └── source/mifos-x-field-officer-app  # Git submodule → openMF/mifos-x-field-officer-app
└── kmp-project-template/
    ├── PROJECT.md
    ├── idea-layer/                # Shared template (screens, flows, exports)
    ├── design-spec-layer/         # Base feature specs (home, profile, settings, navigation)
    ├── client-layer/
    ├── feature-layer/
    ├── infrastructure-layer/
    ├── platform-layer/
    ├── testing-layer/
    └── source/kmp-project-template  # Git submodule → openMF/kmp-project-template
```

## Layer Lifecycle

Each project follows the framework's layer pipeline:

```
Idea → Design → Server → Client → Feature → Infrastructure → Platform
```

| Layer | Purpose | Key Files |
|-------|---------|-----------|
| `idea-layer/` | Source of truth — screens YAML, flows, requirements, roadmap | `IDEA.md`, `FEATURES.md`, `ROADMAP.md` |
| `design-spec-layer/` | Feature specs, API contracts, mockups | `features/{name}/SPEC.md` |
| `server-layer/` | Backend API documentation (Fineract endpoints) | `API.md`, migrations |
| `client-layer/` | Network services, DTOs, repositories | `SERVICES_INDEX.md` |
| `feature-layer/` | ViewModels, Compose screens, navigation | `MODULES_INDEX.md` |
| `infrastructure-layer/` | DI wiring, build config, navigation graph | `BUILD_CONFIG.md` |
| `platform-layer/` | Platform-specific expect/actual (Android/iOS) | `platforms/` |
| `testing-layer/` | Test coverage tracking, test plans | `COVERAGE.md` |

## Working with Submodules

### Update Source to Latest

```bash
cd mifos-mobile/source/mifos-mobile
git checkout development
git pull origin development
cd ../../..
git add mifos-mobile/source/mifos-mobile
git commit -m "chore: sync mifos-mobile source to latest"
```

### Update All Sources

```bash
git submodule update --remote --merge
git add -u
git commit -m "chore: sync all source submodules to latest upstream"
```

### After Cloning (if submodules not initialized)

```bash
git submodule update --init --recursive
```

## Daily Workflow

```bash
# Start session with a project
/context-start                    # Select mifos-mobile, mobile-wallet, etc.

# Check what needs work
/gap-analysis                     # Finds gaps across all layers

# Work on features
/idea-to-design                   # Idea → design specs
/implement auth                   # Design → source code

# Verify everything
/verify                           # Run checks across all layers

# End session
/context-end
```

## Related Projects

| Project | Role |
|---------|------|
| [mifos-mobile](https://github.com/openMF/mifos-mobile) | Self-service banking app (source) |
| [mobile-wallet](https://github.com/openMF/mobile-wallet) | Mobile wallet / Mifos Pay (source) |
| [mifos-x-field-officer-app](https://github.com/openMF/mifos-x-field-officer-app) | Field officer app (source) |
| [kmp-project-template](https://github.com/openMF/kmp-project-template) | Shared KMP scaffold template |
| [Fineract](https://github.com/apache/fineract) | Backend API server |
| [claude-product-cycle](https://github.com/mobilebytesensei/claude-product-cycle) | AI-powered development framework |

## License

Apache 2.0 License (aligned with Mifos Initiative)
