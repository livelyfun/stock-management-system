# Transaction Integrity

## 1. Atomic Business Operations

A posted delivery must execute as one database transaction.

Conceptually:

BEGIN

1. Create delivery
2. Create delivery items
3. Calculate authoritative totals
4. Create invoice
5. Create invoice items
6. Lock the balance rows for the delivery's warehouse
7. Validate on-hand against the zero floor
8. Create inventory movement(s) against the delivery's warehouse
9. Update inventory balance
10. Create customer ledger entry
11. Create audit event

COMMIT

Step 6 must precede step 7. Validation reads the balance only after the
row lock is held, so that a concurrent transaction cannot change the
value between the check and the update.

If validation fails the zero floor, the transaction is rolled back.

---

## 2. Failure

If any required operation fails:

ROLLBACK

No partial business transaction should remain.

---

## 3. Examples

### Delivery

Delivery + Inventory + Invoice + Ledger + Audit

must succeed or fail together.

### Payment

Payment + Allocation + Ledger + Receipt + Audit

must succeed or fail together.

### Return

Return + Inventory + Financial adjustment + Audit

must succeed or fail together.

---

## 4. Concurrency

Transactions must protect against concurrent operations modifying the same inventory or financial state.

Stock-changing transactions use PostgreSQL transactions with row-level
locking on the affected inventory balance rows, using `SELECT ... FOR
UPDATE` or the database-equivalent row lock.

- The balance rows must be locked before stock is validated.
- Validation, the balance update, and the movement creation must occur in
  the same transaction.
- A consistent lock ordering must be used when multiple balance rows are
  affected.

Isolation levels are not a free choice here. `SERIALIZABLE` isolation
must not be introduced unless an existing requirement explicitly
demonstrates a need for it.

Application-level or frontend checks alone are not sufficient. If the
database lock is not obtained, the transaction must not proceed.

Deadlock and serialization failures are retried according to the
documented transaction retry policy, replaying the whole transaction.
Business failures, including insufficient stock, are never retried.
