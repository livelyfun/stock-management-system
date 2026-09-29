# Business Logic Tests

## Inventory

Test the MVP-enabled movement types:

- Opening stock
- Delivery
- Return
- Damage
- Loss
- Adjustment

Test that deferred movement types are rejected in the MVP:

- Production
- Purchase
- Transfer

The controlled vocabulary still contains these values. Rejection must be
based on the MVP boundary, not on the value being absent from the
vocabulary.

Test the movement representation:

- Quantity is stored as a positive value
- Direction `IN` increases on-hand
- Direction `OUT` decreases on-hand
- Negative quantity is rejected
- Direction is required

Test warehouse scoping:

- The same product may hold different on-hand quantities in different
  warehouses
- A movement affects only the recorded warehouse
- Two warehouses are independent for the same product

Test minimum stock:

- Different thresholds may be set for the same product in different
  warehouses
- A threshold may be set before any stock exists for that product and
  warehouse

---

## Negative Stock

Test that negative on-hand stock is impossible.

- An `OUT` movement larger than on-hand is rejected
- The balance never becomes negative
- The rejected transaction leaves no partial state
- No override path exists to force a negative balance
- The rejection is enforced server-side, not by the client
- Sufficient stock available in a different warehouse does not permit an
  `OUT` movement from a warehouse that is short

---

## Concurrency

Starting stock = 200.

- Employee A delivers 100.
- Employee B delivers 150 at nearly the same time.

Test that the outcome is never a negative balance and never double
consumption.

Expected result: one transaction commits, the other is rejected after
observing the committed balance. Which one commits is not fixed.

Also test:

- Row locking is obtained before the availability check
- A deadlock or serialization failure is retried
- An insufficient-stock failure is not retried
- Validation, balance update, and movement creation share one
  transaction
- A rolled-back transaction leaves neither a movement nor an audit row
  for an uncommitted effect

---

## Delivery

Test:

- Valid delivery
- Invalid customer
- Invalid product
- Invalid employee
- Missing warehouse
- Warehouse is recorded on the delivery
- Posting affects the recorded warehouse's stock
- Posting respects the zero floor for that warehouse
- Negative quantity
- Insufficient stock
- Price changes after posting
- Partial delivery
- Duplicate submission

---

## Returns

Test:

- Valid return
- Return greater than delivered
- Duplicate return
- Return from wrong customer
- Invalid product

### Warehouse-Scoped Returns

Test that returned stock lands in the right warehouse.

- A return defaults to the original delivery's warehouse
- A different warehouse can be selected explicitly
- The selected warehouse must exist
- The user must be authorized to record a return into that warehouse
- The movement is recorded with direction `IN` and a positive quantity
- Stock is added only to the selected warehouse's balance
- Other warehouses' balances for the same product are unchanged
- The balance row is locked before the update
- The zero floor is **not** applied to a return, because an `IN` movement
  cannot drive on-hand below zero
- A return is never rejected for insufficient stock
- A return whose warehouse is omitted is accepted and resolved to the
  delivery's warehouse, not rejected for a missing field

Test that the ledger adjustment is unaffected by the inventory direction:
the ledger entry follows the ledger's own debit and credit convention.

---

## Payments

Test:

- Full payment
- Partial payment
- Invalid amount
- Over-allocation
- Multiple invoice allocation
- Duplicate payment

---

## Ledger

Test:

- Opening balance
- Delivery debit
- Payment credit
- Return adjustment
- Credit adjustment
- Balance calculation

---

## Immutability

Test that posted records cannot be silently changed.
