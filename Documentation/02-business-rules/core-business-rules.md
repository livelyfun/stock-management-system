# Core Business Rules

## BR-001 — Posted Transactions Are Immutable

Posted financial and inventory transactions must not be freely edited.

Corrections must use controlled:

- Reversal transactions
- Adjustment transactions
- Void workflows
- Archive workflows

The original transaction must remain traceable.

---

## BR-002 — Historical Prices Are Preserved

When a product's current selling price changes, previously posted transactions must retain the unit price that was used when the transaction occurred.

Historical transactions must never recalculate using the current product price.

---

## BR-003 — Server Is Authoritative

The browser must never be trusted for:

- Prices
- Quantities
- Totals
- Customer IDs
- Employee IDs
- Payment status
- Inventory balances
- Permissions

The server must validate and calculate authoritative values.

---

## BR-004 — Database Transactions

Inventory-affecting and financial operations that modify multiple records must execute inside database transactions.

If any required operation fails, the complete business operation must roll back.

---

## BR-005 — Auditability

Every sensitive business operation must identify the user who performed the operation.

---

## BR-006 — No Silent Deletion

Financial and inventory records must not be silently deleted.

Deletion must be replaced with an appropriate:

- Void
- Reversal
- Adjustment
- Archive

workflow.

---

## BR-007 — Negative Values

Negative quantities must be rejected. Inventory adjustment and movement
quantity is always a positive value, and the direction of the movement
determines its effect, so no adjustment operation is an exception to this
rule.

Invalid monetary values must be rejected unless an explicitly designed
adjustment operation allows them.

**Note:** The inventory sign convention does not apply to the customer
ledger or the employee ledger, which retain their own debit and credit
convention. See ADR-013 and ADR-018.

---

## BR-008 — Duplicate Transactions

The system must prevent duplicate transaction submission where duplication could create:

- Duplicate inventory movement
- Duplicate invoice
- Duplicate payment
- Duplicate ledger entry

---

## BR-009 — Transaction History Is the Source of Truth

Current balances may be maintained for performance.

However, the underlying transaction history remains authoritative.

---

## BR-010 — Business Rules Are Server-Enforced

Important business rules must not depend solely on frontend validation.

The backend must enforce them.

---

## BR-011 — Movement Quantity and Direction

Every inventory movement records:

- A quantity that is always positive
- A direction of either `IN` or `OUT`

`IN` increases stock. `OUT` decreases stock.

The database enforces the positive quantity rule where appropriate.

The same movement is never represented by a negative quantity or by the
absence of a direction.

**Reason:** Keeping the direction explicit makes movement history
unambiguous and independently queryable, and prevents sign-convention
drift between readers. See ADR-013.
