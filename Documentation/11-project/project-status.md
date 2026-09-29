# Project Documentation Status

## Current Status

Initial system-design and requirements documentation.

---

## Completed Design Areas

- Business scope
- Business workflows
- Functional requirements
- Core business rules
- Security threat model
- Secure architecture
- Technology direction
- Database direction
- Inventory model
- Customer ledger model
- Web application structure
- Role-based experience
- Transaction workflows
- Audit logging
- Backup and recovery requirements
- Security testing
- Non-functional requirements
- Indexing strategy
- Concurrency requirements
- Production deployment principles
- Implementation roadmap
- MVP boundary
- Transaction retry policy
- Warehouse-scoped inventory

---

## Recorded Architecture Decisions

The inventory domain decisions are recorded as ADRs in the architecture
decisions document:

- ADR-009 — Negative on-hand stock is prohibited
- ADR-010 — Warehouse is a core inventory dimension
- ADR-011 — Movement vocabulary versus MVP-enabled movement types
- ADR-012 — Row-level locking on inventory balances
- ADR-013 — Positive movement quantity with direction
- ADR-014 — Inventory balance key
- ADR-015 — Minimum stock is per-warehouse
- ADR-016 — Transaction retry policy
- ADR-017 — No warehouse filter on the delivery list endpoint
- ADR-018 — Movement sign convention does not apply to the financial ledger
- ADR-019 — Return warehouse is explicit and defaults to the original delivery

The MVP boundary document is authoritative for release scope.

The return path is warehouse-scoped: a return records the warehouse that
receives the stock, defaulting to the original delivery's warehouse.

---

## Resolved Contradictions

**Search by warehouse.** The search requirements list warehouse as a
filter, which appeared to conflict with ADR-017. The reporting endpoint
supports a warehouse filter, and it is a different endpoint from
`GET /api/deliveries`. Warehouse filtering therefore exists in reporting
and not in the delivery list, which is consistent with ADR-017.

---

## Open Contradictions

These are known and deliberately unresolved. They need a decision before
the related artifacts can be specified.

1. **Invoice on delivery** — `transaction-integrity.md` requires invoice
   creation on delivery posting, while `sales-delivery-rules.md` treats
   it as conditional.
2. **Customer opening balance** — whether the customer ledger opening
   balance is a column or an opening ledger entry is not decided.
3. **Status enums** — invoice, payment, return, and adjustment status
   values are referenced but not defined.
4. **Rejected stock attempts** — whether an insufficient-stock rejection
   is an auditable event is not decided. The retry policy covers
   transient database failures, not business rejections.

---

## Next Detailed Artifacts

The following should be refined during implementation:

1. Detailed ERD
2. PostgreSQL schema specification
3. RBAC permission matrix
4. Page-by-page UI specification
5. Threat model with abuse cases
6. Transaction state diagrams
7. Deployment and backup runbook

The API contract and the test plan now have documented behaviour for
error handling, transaction retries, and negative stock, so they no
longer require a first-pass definition.

### Required in the Page-by-Page UI Specification

The UI specification is deferred, so the frontend artifacts do not yet
mention warehouses. The following must be covered when it is written:

- A warehouse selector on delivery create
- A warehouse selector on stock adjustment
- A warehouse selector on return create, pre-filled from the original
  delivery's warehouse and overridable
- Inventory position displayed per warehouse

Without these, the frontend cannot submit the warehouse fields that the
API requires.

---

## Important

This documentation is the project knowledge base.

Implementation decisions must remain consistent with these documents unless an architecture/business decision is intentionally changed and documented.
