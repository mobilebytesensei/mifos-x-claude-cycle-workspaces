# Mifos MCP — API Surface

## Base Configuration

| Field | Value |
|-------|-------|
| Base URL | `https://{host}/fineract-provider/api/v1` |
| Auth | HTTP Basic (username:password) |
| Tenant Header | `fineract-platform-tenantid: {tenant_id}` |
| Content-Type | application/json |
| Transport | MCP stdio (default) / SSE (Go via PORT env) |

## Endpoint Domains

### Clients (`/clients`)
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/clients` | List/search clients | search_clients |
| GET | `/clients/{id}` | Get client details | get_client |
| POST | `/clients` | Create client | create_client |
| POST | `/clients/{id}?command=activate` | Activate client | activate_client |
| POST | `/clients/{id}?command=close` | Close client | close_client |
| DELETE | `/clients/{id}` | Delete client | delete_client |
| GET | `/clients/{id}/accounts` | Client accounts | get_client_accounts |
| GET | `/clients/{id}/identifiers` | Client IDs | get_client_identifiers |
| POST | `/clients/{id}/identifiers` | Add ID | create_client_identifier |
| GET | `/clients/{id}/charges` | Client charges | get_client_charges |
| GET | `/clients/{id}/documents` | Client documents | list_client_documents |

### Loans (`/loans`)
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/loanproducts` | List products | list_loan_products |
| POST | `/loans` | Create loan | create_loan |
| GET | `/loans/{id}` | Loan details | get_loan_details |
| GET | `/loans/{id}/schedule` | Repayment schedule | get_repayment_schedule |
| GET | `/loans/{id}/transactions` | Loan history | get_loan_history |
| POST | `/loans/{id}?command=approve` | Approve | approve_loan |
| POST | `/loans/{id}?command=reject` | Reject | reject_loan |
| POST | `/loans/{id}?command=disburse` | Disburse | disburse_loan |
| POST | `/loans/{id}/transactions?command=repayment` | Repay | make_loan_repayment |
| POST | `/loans/{id}/charges` | Apply fee | apply_late_fee |
| POST | `/loans/{id}?command=reschedule` | Reschedule | reschedule_loan |

### Savings (`/savingsaccounts`)
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/savingsproducts` | List products | list_savings_products |
| POST | `/savingsaccounts` | Create account | create_savings_account |
| GET | `/savingsaccounts/{id}` | Account details | get_savings_account |
| GET | `/savingsaccounts/{id}/transactions` | Transactions | get_savings_transactions |
| POST | `/savingsaccounts/{id}?command=approve` | Approve | approve_savings |
| POST | `/savingsaccounts/{id}?command=activate` | Activate | activate_savings |
| POST | `/savingsaccounts/{id}/transactions?command=deposit` | Deposit | deposit_savings |
| POST | `/savingsaccounts/{id}/transactions?command=withdrawal` | Withdraw | withdraw_savings |

### Groups (`/groups`)
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/groups` | List groups | list_groups |
| POST | `/groups` | Create group | create_group |
| GET | `/groups/{id}` | Group details | get_group |
| POST | `/groups/{id}?command=activate` | Activate | activate_group |
| POST | `/groups/{id}?command=associateClients` | Add member | add_group_member |
| POST | `/groups/{id}?command=disassociateClients` | Remove member | remove_group_member |

### Accounting
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/glaccounts` | List GL accounts | list_gl_accounts |
| GET | `/journalentries` | List entries | get_journal_entries |
| POST | `/journalentries` | Create entry | create_journal_entry |

### Staff & Offices
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/staff` | List staff | list_staff |
| GET | `/staff/{id}` | Staff details | get_staff_details |
| GET | `/offices` | List offices | list_offices |

### Reports
| Method | Path | Description | MCP Tool |
|--------|------|-------------|----------|
| GET | `/reports` | List reports | get_reports |
| POST | `/reports` | Create report | create_report |
| GET | `/runreports/{name}` | Run report | run_report |

## Environment Variables

| Variable | Required | Default | Description |
|----------|:--------:|---------|-------------|
| MIFOSX_BASE_URL | yes | — | Fineract API endpoint |
| MIFOSX_TENANT_ID | yes | default | Tenant identifier |
| MIFOSX_USERNAME | yes | — | API username |
| MIFOSX_PASSWORD | yes | — | API password |
| PORT | no | 8080 | SSE mode (Go only) |
