# Architecture Decisions

## ADR-001 — PostgreSQL

### Decision

Use PostgreSQL as the primary transactional database.

### Reason

The system requires:

- Strong transactions
- Referential integrity
- Constraints
- Reliable financial operations
- Inventory consistency
- Reporting queries

---

## ADR-002 — Modular Monolith

### Decision

Start with a modular monolith.

### Reason

The initial system does not require the operational complexity of multiple independently deployed services.

Modules should remain separated internally so future extraction is possible if necessary.

---

## ADR-003 — Server-Side Authorization

### Decision

Authorization must be enforced on the server/API.

### Reason

Frontend controls are not a security boundary.

---

## ADR-004 — Inventory Movement Ledger

### Decision

Inventory movements are the authoritative history of stock changes.

### Reason

A current balance alone cannot provide sufficient historical traceability.

---

## ADR-005 — Customer Ledger

### Decision

Customer financial history is represented through ledger transactions.

### Reason

Customer credit must remain traceable.

---

## ADR-006 — Immutable Posted Transactions

### Decision

Posted transactions cannot be freely edited.

### Reason

Financial and inventory history must remain auditable.

---

## ADR-007 — Server-Side Financial Calculation

### Decision

The server calculates authoritative totals.

### Reason

Browser-provided calculations are untrusted.

---

## ADR-008 — Atomic Business Transactions

### Decision

Multi-record business operations use database transactions.

### Reason

Partial completion could corrupt inventory or financial records.

---

## ADR-009 — Negative On-Hand Stock Is Prohibited

### Decision

Negative on-hand stock is hard-blocked. A stock-consuming transaction
must not commit if the resulting on-hand quantity would fall below zero.

No negative-stock override permission exists in the MVP.

Enforcement must be transactional and server-side, supported by
database integrity where appropriate. Frontend validation is not the
enforcement mechanism.

No reservation model and no available-versus-reserved stock concept is
introduced. Availability means on-hand quantity.

### Reason

An undefined stock policy cannot be enforced or tested. Hard-blocking
at zero keeps `inventory_balances` non-negative and makes the balance
a reliable state rather than an indicator of an error.

---

## ADR-010 — Warehouse Is a Core Inventory Dimension

### Decision

The MVP supports multiple warehouses. `warehouse_id` is a core inventory
dimension and inventory is scoped to a warehouse.

Warehouse identity must be explicit in inventory-related records, and
the delivery record carries the warehouse it is fulfilled from.

Warehouse transfers are not part of the MVP merely because multiple
warehouses exist.

No warehouse-scoped pricing and no warehouse-scoped authorization are
introduced.

### Reason

Warehouse-scoped stock is required by the inventory model and reporting.
Introducing the dimension later would require backfilling the immutable
movement history, so it is established from the start. Transfer,
warehouse-scoped pricing, and warehouse-scoped authorization are not
required by any current requirement.

---

## ADR-011 — Movement Vocabulary Versus MVP-Enabled Movement Types

### Decision

The nine movement types remain the broader target-domain vocabulary.

MVP business rules determine which movement types are currently
enabled. In the MVP the enabled types are:

- Opening Stock
- Delivery
- Return
- Adjustment
- Damage
- Loss

Deferred types are Purchase, Production, and Transfer.

Deferred movement types must not become usable merely because their
values exist in the controlled database vocabulary.

No additional movement types may be invented.

### Reason

A broad vocabulary keeps the target domain explicit, while the MVP
boundary keeps shipping scope controlled. Without the distinction, the
existence of an enum value would silently imply a supported feature.

---

## ADR-012 — Row-Level Locking on Inventory Balances

### Decision

Stock-changing transactions use database transactions with row-level
locking on the affected `inventory_balances` rows, using
`SELECT ... FOR UPDATE` or the database-equivalent row lock.

- The affected balance row is locked before checking or updating stock.
- Availability validation and the balance update occur in the same
  transaction.
- The corresponding stock movement is created in the same transaction.
- A consistent lock ordering is used when multiple balance rows are
  affected.
- Deadlock and serialization-failure handling follows ADR-016.
- Frontend or application-only validation is not relied upon.

`SERIALIZABLE` isolation must not be introduced unless existing
requirements explicitly demonstrate a need for it.

### Reason

Row-level locking satisfies the concurrency requirement stated in the
inventory rules and the documented 200/100/150 example without
requiring stronger isolation than necessary.

---

## ADR-013 — Positive Movement Quantity With Direction

### Decision

Inventory movement quantity is always a positive value. Direction
determines its effect:

- `IN` increases stock
- `OUT` decreases stock

Negative movement quantities must not be stored. The database enforces
`quantity > 0` where appropriate.

### Reason

A positive quantity with an explicit direction keeps movement rows
unambiguous, keeps the direction independently queryable, and prevents
sign-convention drift between readers. It also satisfies the existing
requirement that adjustment records carry a direction.

---

## ADR-014 — Inventory Balance Key

### Decision

For the MVP the `inventory_balances` primary key is:

`(product_id, warehouse_id)`

There is no location, lot, batch, or reservation dimension in the MVP.

These dimensions must not be introduced without explicit requirements.

### Reason

Stock is scoped to a product within a warehouse. No current
requirement introduces a finer granularity, and adding a dimension
later would require rebuilding the balance key.

---

## ADR-015 — Minimum Stock Is Per-Warehouse

### Decision

Minimum stock is a per-warehouse value in the MVP.

The threshold is associated with the product and warehouse inventory
context, so different warehouses may hold different minimum-stock
thresholds for the same product.

The threshold is stored in a master-data table:

`product_warehouse_settings (product_id, warehouse_id, minimum_stock)`

No global product-level minimum threshold exists, and no location, lot,
batch, or reservation dimension is added.

### Reason

Because inventory balances are keyed by product and warehouse, a
product-level threshold would be ambiguous across warehouses. Storing
the threshold as master data separate from the derived balance keeps the
balance free of manually configured state and allows a threshold to be
set before any stock exists for that pair.

---

## ADR-016 — Transaction Retry Policy

### Decision

Transaction retries are bounded and explicit:

- Maximum 3 attempts in total.
- Exponential backoff between retries of 100 ms, then 250 ms.
- Only recognized transient database concurrency failures are retried,
  such as deadlock or serialization failure.
- Business-rule and validation failures are never retried, including
  insufficient stock.
- After the final failed attempt, a generic retryable transaction error
  is returned to the client.
- Database internals must not be exposed in the API response.
- The failure is logged with the request or correlation ID for
  diagnosis.
- Stock validation, the balance update, and stock movement creation
  remain within the same transaction.
- `SERIALIZABLE` isolation must not be introduced.

### Reason

Concurrency conflicts are transient and safe to replay, whereas business
failures are deterministic and would only waste attempts. The bound
prevents retry storms, and the generic error keeps database internals
from leaking to clients.

---

## ADR-017 — No Warehouse Filter on the Delivery List Endpoint

### Decision

`GET /api/deliveries` does not support a warehouse filter in the MVP.
The current API surface is unchanged.

Individual delivery records remain warehouse-identifiable because the
delivery record carries `warehouse_id`.

No additional filtering requirement is introduced.

### Reason

No current requirement asks for delivery search by warehouse, and
filtering requirements must not be invented. The record itself remains
identifiable.

---

## ADR-018 — The Movement Sign Convention Does Not Apply to the Financial Ledger

### Decision

ADR-013 governs inventory movements only.

The customer ledger and the employee ledger retain their own debit and
credit convention and are not modelled with `IN`/`OUT` direction.

### Reason

The financial ledger and the inventory balance are different aggregates
with different semantics. Applying the inventory sign convention to
financial entries would misstate the ledger model.

---

## ADR-019 — Return Warehouse Is Explicit and Defaults to the Original Delivery

### Decision

A return records the warehouse that receives the returned stock.

- The warehouse is a required field on the return.
- It defaults to the warehouse of the original delivery.
- The user may select a different warehouse.

The return movement is recorded with direction `IN` and a positive
quantity against the return's warehouse.

The balance row is locked in the same transaction, consistent with
ADR-012. The zero floor does not apply to an `IN` movement, because
adding stock cannot drive on-hand below zero. The lock still applies,
because the balance read and write must be consistent.

### Reason

Inventory is scoped to a warehouse, so a return must name the warehouse
that receives the stock. Without it, returned goods have no destination
and cannot create a valid movement.

Defaulting to the original delivery's warehouse prevents most mis-entry
without adding a required decision to every return. The override is
needed because goods are not always physically received back at the
warehouse they were dispatched from.
