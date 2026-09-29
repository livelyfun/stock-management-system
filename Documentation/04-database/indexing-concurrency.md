# Indexing and Concurrency

## Indexing

Initial indexes should cover common access paths:

- customer_id
- employee_id
- product_id
- warehouse_id
- transaction date
- document number
- payment status
- invoice status

---

## Composite Indexes

Composite indexes should be added based on real query patterns.

Do not add indexes without a demonstrated access pattern or performance requirement.

### Inventory Balance Access Path

`inventory_balances` is keyed by `(product_id, warehouse_id)`, and the
stock-checking access path is always by that pair. The composite primary
key therefore already provides the required access path, and no separate
composite index is needed for balance lookups.

Warehouse-level reporting access is also covered by the same key, since
`warehouse_id` is the leading column only in indexes that order it
first; a separate index is added only if a demonstrated access pattern
requires it.

---

## Concurrency

Inventory operations must be safe when multiple users submit transactions simultaneously.

---

## Required Protection

Stock-changing transactions use:

- PostgreSQL transactions
- Row-level locking on the affected `inventory_balances` rows using
  `SELECT ... FOR UPDATE` or the database-equivalent row lock
- A consistent lock ordering when multiple balance rows are affected
- Availability validation and the balance update in the same
  transaction

`SERIALIZABLE` isolation must not be introduced unless an existing
requirement explicitly demonstrates a need for it.

Isolation levels are not a free choice here. The required protection is
row-level locking, which satisfies the requirement without stronger
isolation.

Application-level or frontend checks alone are not sufficient. If the
database lock is not obtained, the transaction must not proceed.

Deadlock and serialization failures are retried according to the
documented transaction retry policy. Business failures, including
insufficient stock, are never retried.

---

## Example

Starting stock = 200.

Employee A attempts to deliver 100.

Employee B attempts to deliver 150.

Employee A obtains the balance row lock and commits, leaving on-hand
100. Employee B then obtains the same lock, re-reads the balance,
computes a result of -50, and is rejected and rolled back.

Row-level locking plus the zero floor on `inventory_balances` prevents an
invalid final state caused by both operations reading the same original
balance.

---

## Principle

Concurrency correctness is a database responsibility as well as an application responsibility.
