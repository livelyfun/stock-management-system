# Sales and Delivery Rules

## Delivery States

A delivery follows:

DRAFT
→ CONFIRMED
→ POSTED

After posting, the transaction becomes immutable.

---

## Delivery Requirements

A delivery must contain:

- Delivery number
- Delivery date
- Customer
- Employee / delivery staff
- Warehouse
- Vehicle where applicable
- Items
- Quantities
- Unit prices
- Discounts or adjustments
- Payment status
- Notes

The warehouse identifies where the delivery is fulfilled from. It is
required, because the stock it consumes is warehouse-scoped.

---

## Server Calculation

The server must:

1. Load authoritative product information.
2. Lock and load the on-hand balance for the delivery's warehouse.
3. Validate on-hand availability against the requested quantities.
4. Determine the applicable price.
5. Validate quantities.
6. Calculate totals.
7. Apply valid discounts/adjustments.
8. Create the required transaction records.

The browser's calculated total must never be trusted.

On-hand availability means the on-hand quantity in the delivery's
warehouse. Stock held in another warehouse is not available to satisfy
this delivery, and warehouse transfers are not part of the MVP.

If a line would cause on-hand to fall below zero, the delivery is
rejected and rolled back. There is no override.

---

## Delivery Posting

Posting a delivery may create:

- Delivery record
- Delivery items
- Inventory movements against the delivery's warehouse
- Inventory balance changes for the delivery's warehouse
- Invoice
- Invoice items
- Customer ledger entry
- Audit event

These effects must be committed atomically.

---

## Partial Delivery

The requested quantity and delivered quantity may differ.

The system must preserve the actual delivered quantity.

---

## Document Number

Delivery numbers must be:

- Unique
- Human-readable
- Generated server-side

Suggested format:

DEL-2026-00125
