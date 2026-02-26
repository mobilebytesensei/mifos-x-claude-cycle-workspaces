# Client Layer Guide - mobile-wallet

> Repository and data layer documentation

---

## Layer Purpose

The client layer documents:
- Repository interfaces and implementations
- Data models
- Caching strategies
- Error handling patterns

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Feature Layer                     │
│                    (ViewModels)                      │
├─────────────────────────────────────────────────────┤
│                   Domain Layer                       │
│              (Repository Interfaces)                 │
├─────────────────────────────────────────────────────┤
│                    Data Layer                        │
│            (Repository Implementations)              │
├─────────────────────────────────────────────────────┤
│     Remote Data Source    │    Local Data Source    │
│    (Ktorfit Services)     │    (DataStore/Room)     │
└─────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
client-layer/
├── SERVICES_INDEX.md      # Repository registry
├── LAYER_GUIDE.md         # This file
├── services/              # Service documentation
└── repositories/          # Repository documentation
```

---

## Source Locations

| Component | Path |
|-----------|------|
| Interfaces | `core/domain/repository/` |
| Implementations | `core/data/repository/` |
| Models | `core/model/` |
| Network | `core/network/` |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/client [repo]` | Document repository |
| `/gap-analysis client` | Check gaps |
