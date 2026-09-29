# Return Workflow

## Flow

Select Customer
↓
Select Original Delivery
↓
Select Warehouse
↓
Select Product
↓
Enter Quantity
↓
Validate Eligible Quantity
↓
POST RETURN
↓
Inventory Updated
↓
Ledger / Invoice Adjustment

---

## Validation

The system must verify:

- Customer
- Original delivery
- Warehouse
- Eligible quantity
- User authorization

---

## Original Delivery

The original delivery must remain unchanged.

The return is a separate transaction linked to it.

---

## Warehouse

The warehouse identifies which warehouse receives the returned stock.

It is selected after the original delivery, and is pre-filled from that
delivery's warehouse. The user may change it, because goods are not
always physically received back where they were dispatched from.

---

## Posting

Posting creates:

- Return
- Return items
- An inventory movement with direction `IN` and a positive quantity,
  recorded against the return's warehouse
- Appropriate financial adjustment
- Audit event

The balance row for that product in that warehouse is locked before the
update.

The zero floor does not apply to a return, because adding stock cannot
drive on-hand below zero. A return must not be rejected for insufficient
stock.

---

## Atomicity

Required effects must be committed atomically.
