# Payment Rules

## 1. Payments Are Separate Transactions

Payments must be stored separately from invoices and deliveries.

---

## 2. Payment Types

The system must support:

- Full payment
- Partial payment
- Credit / pay later

---

## 3. Payment Validation

The server must validate:

- Customer
- Payment amount
- Payment date
- Payment method where applicable
- Applicable invoice(s)
- User performing the transaction

---

## 4. Payment Allocation

A payment may be allocated against one or more invoices where appropriate.

Payment allocation must not exceed the applicable outstanding amount unless an explicit overpayment rule is introduced.

---

## 5. Ledger Effect

A successful payment must create the appropriate customer ledger credit.

---

## 6. Receipt

A successful payment must generate a payment receipt.

Suggested number:

PAY-2026-000091

---

## 7. Immutability

Posted payments must not be silently edited or deleted.

Corrections must use controlled void/reversal workflows.

---

## 8. Audit

Payment creation and void/reversal operations must generate audit events.
