# Delivery Workflow

## State Flow

DRAFT
↓
CONFIRMED
↓
POSTED
↓
INVENTORY UPDATED
↓
INVOICE POSTED
↓
LEDGER UPDATED
↓
RECEIPT / DOCUMENT

---

## Step 1 — Create Draft

User selects:

- Customer
- Employee
- Warehouse
- Vehicle where applicable
- Products
- Quantities

The warehouse identifies where the delivery is fulfilled from, and
determines which stock the delivery draws on.

The system creates a draft.

---

## Step 2 — Validate

Server validates:

- User authorization
- Customer
- Employee
- Warehouse
- Products
- Quantities
- Prices
- Business rules

---

## Step 3 — Confirm

Delivery transitions:

DRAFT → CONFIRMED

---

## Step 4 — Post

The server performs the complete business transaction.

---

## Step 5 — Inventory

Lock the on-hand balance rows for the delivery's warehouse, then create
inventory movements and update the balance.

The availability check, the balance update, and the movement creation
occur in the same transaction. If any line would cause on-hand in that
warehouse to fall below zero, the delivery is rejected and the whole
transaction is rolled back. There is no override.

---

## Step 6 — Invoice

Create invoice and invoice items where applicable.

---

## Step 7 — Ledger

Create customer ledger entry.

---

## Step 8 — Audit

Create audit event.

---

## Step 9 — Commit

All required operations commit atomically.

If any required operation fails:

ROLLBACK

A recognized transient concurrency failure is retried according to the
documented retry policy, with the whole transaction replayed. A
business failure, including insufficient stock, is never retried.

---

## Partial Delivery

Requested quantity may differ from delivered quantity.

The system must preserve the actual delivered quantity.
