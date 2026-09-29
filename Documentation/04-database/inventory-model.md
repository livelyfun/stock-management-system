# Inventory Model

## 1. Authoritative History

The authoritative inventory history is:

inventory_movements

---

## 2. Current State

Fast current inventory state is:

inventory_balances

The balance is a maintained current-state table keyed by:

(product_id, warehouse_id)

There is no location, lot, batch, or reservation dimension in the MVP.

The balance is maintained state, not the authoritative history. See
section 1.

---

## 3. Stock Formula

Opening
+ Production
+ Purchases
+ Returns
- Deliveries
- Damage
- Loss
+/- Adjustments
= Current Stock

The formula is a conceptual net result. Movement quantities are always
positive and are stored with a direction of `IN` or `OUT`, so the net
result is computed by applying direction rather than by storing signed
quantities.

Production and purchases are deferred and are not active in the MVP.

---

## 4. Inventory Movement

Every stock-changing business operation must create an appropriate inventory movement.

A movement records the warehouse whose stock is affected, a positive
quantity, and a direction.

---

## 5. Balance Synchronization

When a movement is posted:

1. Begin a database transaction.
2. Lock the affected `inventory_balances` row using
   `SELECT ... FOR UPDATE` or the database-equivalent row lock.
3. Validate the movement, including the zero floor, against the locked
   row.
4. Reject and roll back if the resulting on-hand quantity would fall
   below zero.
5. Create the inventory movement.
6. Update the current balance.
7. Commit atomically.

A consistent lock ordering is used when multiple balance rows are
affected.

Deadlock and serialization failures are retried according to the
documented transaction retry policy. Business failures, including
insufficient stock, are never retried.

`SERIALIZABLE` isolation must not be introduced.

---

## 6. Manual Adjustment

Manual adjustments must:

- Require authorization
- Require a reason
- Record the acting user
- Record the warehouse
- Record the movement type
- Record a positive quantity and a direction
- Create an inventory movement
- Create an audit event

Damage and Loss are recorded through this mechanism as their own
movement types.

---

## 7. Concurrency

Inventory updates must protect against race conditions.

Row-level locking on the balance row, combined with the zero floor, is
the protection mechanism. Application-level or frontend checks alone are
not sufficient.

Example:

Starting stock = 200

Employee A delivers 100.

Employee B delivers 150 at nearly the same time.

The second transaction waits for the lock, then re-reads the balance. It
observes on-hand 100, computes a result of -50, and is rejected and
rolled back. The database must not allow both transactions to
incorrectly consume the same stock, and on-hand must never go negative.
