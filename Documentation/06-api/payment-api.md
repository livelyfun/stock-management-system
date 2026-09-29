# Payment API

## Create Payment

POST /api/payments

Server validates:

- Customer
- Amount
- Payment method
- Applicable invoices
- Allocation

---

## Payment Allocation

POST /api/payments/:id/allocations

The total allocated amount must obey payment allocation rules.

---

## Receipt

GET /api/payments/:id/receipt

Returns or generates the payment receipt.

---

## Void Payment

POST /api/payments/:id/void

Requires appropriate authorization.

Must preserve historical payment information.

---

## List Payments

GET /api/payments

Supports:

- Customer
- Date range
- Payment status
- Invoice
- Pagination
