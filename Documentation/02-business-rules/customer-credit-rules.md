# Customer Credit Rules

## 1. Ledger-Based Balance

Customer balance must be represented through ledger transactions.

---

## 2. Ledger Effects

Examples:

Delivery / Invoice
→ Debit

Payment
→ Credit

Credit Adjustment
→ Credit or Adjustment

Return
→ Appropriate Credit / Adjustment

---

## 3. Balance

Conceptually:

Opening Balance
+ Debits
- Credits
+/- Adjustments
= Outstanding Balance

---

## 4. Customer Credit Information

The system should show:

- Opening balance
- Debits
- Credits
- Outstanding balance
- Due dates
- Overdue amounts

---

## 5. Credit Limit

Customers may have a configured credit limit.

The system should enforce the configured business policy when a new transaction would exceed the permitted credit exposure.

---

## 6. Historical Ledger

Ledger transactions must remain traceable.

Posted ledger entries must not be silently modified or deleted.

---

## 7. Credit Adjustment

Credit adjustments must:

- Require authorization
- Record a reason
- Record the acting user
- Create an audit event
- Preserve previous transaction history
