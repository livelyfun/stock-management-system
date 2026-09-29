# Payment Workflow

## Flow

Customer
↓
Payment
↓
Validate Amount
↓
Allocate Payment
↓
Create Receipt
↓
Update Ledger
↓
Outstanding Balance Reduced

---

## Validation

Validate:

- Customer
- Payment amount
- Applicable invoices
- Allocation
- Authorization

---

## Posting

A successful payment creates:

- Payment record
- Payment allocation(s)
- Customer ledger credit
- Receipt
- Audit event

---

## Correction

Posted payments must be corrected using controlled void/reversal workflows.

---

## Atomicity

Payment, allocation, ledger, receipt, and audit operations should be committed atomically where they form one business transaction.
