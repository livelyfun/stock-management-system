# Return Rules

## 1. Returns Are Separate Transactions

A return must never rewrite the original delivery.

---

## 2. Return Link

Every return must reference the original delivery where applicable.

---

## 3. Eligible Quantity

The returned quantity must not exceed the quantity eligible for return.

Conceptually:

Eligible Return Quantity
=
Delivered Quantity
-
Previously Returned Quantity

---

## 4. Return Information

A return must contain:

- Return number
- Customer
- Original delivery
- Warehouse
- Date
- Employee
- Product
- Quantity
- Condition
- Reason
- Notes

The warehouse identifies which warehouse receives the returned stock.

The warehouse defaults to the warehouse of the original delivery. A
different warehouse may be selected, because goods are not always
physically received back where they were dispatched from.

---

## 5. Inventory Effect

A valid return must create the appropriate inventory movement.

The movement:

- Is recorded against the return's warehouse
- Uses direction `IN`, with a positive quantity
- Updates the on-hand balance for that product in that warehouse

The balance row is locked, and the movement and the balance update occur
in the same transaction.

The zero floor does not apply to a return, because an `IN` movement
cannot drive on-hand below zero. The lock still applies. A return must
not be rejected for insufficient stock.

---

## 6. Financial Effect

Where applicable, the return must create the appropriate invoice/customer-ledger adjustment.

The ledger adjustment follows the ledger's own debit and credit
convention, not the inventory `IN`/`OUT` direction.

---

## 7. Audit

Return creation must generate an audit event.

---

## 8. Return Number

Return numbers must be unique and generated server-side.

Suggested format:

RET-2026-000041
