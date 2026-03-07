# API Index - O(1) Lookup

> **Purpose**: Instant lookup for all API endpoints documented in the server-layer.
> **Backend**: Fineract REST API

---

## Quick Reference

| # | Endpoint Category | Methods | Base Path | Status |
|:-:|-------------------|:-------:|-----------|:------:|
| 1 | Authentication | TBD | /authentication | ⚠️ |
| 2 | Clients | TBD | /clients | ⚠️ |
| 3 | Loans | TBD | /loans | ⚠️ |
| 4 | Savings | TBD | /savingsaccounts | ⚠️ |
| 5 | Groups | TBD | /groups | ⚠️ |
| 6 | Centers | TBD | /centers | ⚠️ |
| 7 | Offices | TBD | /offices | ⚠️ |
| 8 | Staff | TBD | /staff | ⚠️ |
| 9 | DataTables | TBD | /datatables | ⚠️ |
| 10 | Documents | TBD | /documents | ⚠️ |
| 11 | Notes | TBD | /notes | ⚠️ |
| 12 | Reports | TBD | /runreports | ⚠️ |
| 13 | Search | TBD | /search | ⚠️ |
| 14 | CollectionSheet | TBD | /collectionsheet | ⚠️ |
| 15 | CheckerInbox | TBD | /makercheckers | ⚠️ |
| 16 | Charges | TBD | /charges | ⚠️ |
| 17 | Surveys | TBD | /surveys | ⚠️ |

**Status Legend:**
- ✅ Documented
- ⚠️ Discovered (needs documentation)
- ❌ Not started

---

## Backend Configuration

```yaml
provider: fineract
base_url: "https://demo.mifos.io/fineract-provider/api/v1"
auth_method: basic
content_type: application/json
```

---

## Category Index

### Client Management APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| Clients | GET, POST, PUT | /clients |
| Client Accounts | GET | /clients/{id}/accounts |
| Client Identifiers | GET, POST | /clients/{id}/identifiers |

### Financial Product APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| Loans | GET, POST, PUT | /loans |
| Loan Transactions | POST | /loans/{id}/transactions |
| Savings Accounts | GET, POST, PUT | /savingsaccounts |
| Savings Transactions | POST | /savingsaccounts/{id}/transactions |
| Recurring Deposits | GET, POST | /recurringdepositaccounts |
| Fixed Deposits | GET, POST | /fixeddepositaccounts |
| Charges | GET, POST | /charges |

### Group & Center APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| Groups | GET, POST, PUT | /groups |
| Centers | GET, POST, PUT | /centers |
| Collection Sheet | GET, POST | /collectionsheet |

### Organization APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| Offices | GET | /offices |
| Staff | GET | /staff |

### Data & Reporting APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| DataTables | GET, POST | /datatables |
| Reports | GET | /runreports |
| Search | GET | /search |

### Utility APIs
| Endpoint | Methods | Path |
|----------|:-------:|------|
| Documents | GET, POST | /documents |
| Notes | GET, POST | /notes |
| Surveys | GET, POST | /surveys |
| Checker Inbox | GET, POST | /makercheckers |

---

## Commands

```bash
/enforce-index api         # Validate this index
/server [endpoint]         # Document endpoint (auto-indexes)
/gap-analysis server       # Check server layer gaps
```

---

## Related Files

| File | Purpose |
|------|---------|
| `endpoints/*.md` | Individual endpoint documentation |
| `LAYER_GUIDE.md` | Server layer implementation guide |
