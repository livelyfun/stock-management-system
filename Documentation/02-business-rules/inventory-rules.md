# Inventory Rules

## 1. Inventory Movement Types

The target domain vocabulary is:

- Opening Stock
- Production
- Purchase
- Delivery
- Return
- Damage
- Loss
- Adjustment
- Transfer

These nine types define the broader target domain. They do not all have
to be implemented in the MVP.

The MVP-enabled types are:

- Opening Stock
- Delivery
- Return
- Adjustment
- Damage
- Loss

The MVP boundary document is authoritative for which types are enabled
at any release.

Purchase, Production, and Transfer are deferred. They must not become
usable merely because their values exist in the controlled database
vocabulary.

No additional movement types may be invented.

---

## 2. Authoritative Inventory History

The authoritative inventory history is stored in inventory movements.

Current stock balances may be maintained separately for fast reads.

---

## 3. Stock Calculation

Conceptually:

Opening
+ Production
+ Purchases
+ Returns
- Deliveries
- Damage
- Loss
+/- Adjustments
= Current Stock

The formula is a conceptual net result. Movement quantities are
individually always positive; their direction (`IN` or `OUT`) determines
the sign of their effect, so the net result is computed by applying
direction rather than by storing signed quantities.

Terms for deferred movement types are part of the target domain formula
but are not active in the MVP. See section 1.

---

## 4. Delivery

A successfully posted delivery must create the appropriate inventory movement.

---

## 5. Return

A valid return increases inventory when the returned product is eligible to return to stock.

The return must be linked to the original delivery.

---

## 6. Adjustment

Every manual stock adjustment must require:

- User
- Product
- Warehouse
- Quantity
- Direction (`IN` or `OUT`)
- Movement type
- Reason
- Timestamp

The quantity is always a positive value. Negative quantities are not
stored.

Damage and Loss are recorded through the adjustment mechanism as their
own movement types, so that they remain distinguishable in the
authoritative history.

---

## 7. Negative Stock

Negative on-hand stock is prohibited.

A stock-consuming transaction must not commit if the resulting on-hand
quantity would fall below zero. The transaction must be rejected and
rolled back.

This policy is enforced server-side inside the stock-changing
transaction, and is supported by a database integrity constraint. Frontend
validation is not the enforcement mechanism.

No override permission for negative stock exists in the MVP.

No reservation model and no available-versus-reserved stock concept is
introduced. Availability means on-hand quantity.

Corrections discovered after the fact, such as shrinkage, are recorded as
adjustments against the current on-hand quantity and remain subject to
the same zero floor.

---

## 8. Concurrency

Inventory updates must be safe when multiple users perform transactions
simultaneously.

Stock-changing transactions must use database transactions with
row-level locking on the affected inventory balance rows.

- The affected balance row must be locked before checking or updating
  stock.
- Availability validation and the balance update must occur in the same
  transaction.
- The corresponding stock movement must be created in the same
  transaction.
- A consistent lock ordering must be used when multiple balance rows are
  affected.

Deadlock and serialization failures are handled according to the
documented transaction retry policy. Business-rule failures, including
insufficient stock, are never retried.

`SERIALIZABLE` isolation must not be introduced unless an existing
requirement explicitly demonstrates a need for it.

---

## 9. Current Balance

Inventory balance must not become an uncontrolled manually editable field.

Any change must originate from a valid inventory transaction.

---

## 10. Minimum Stock

Minimum stock is a per-warehouse value.

The threshold is associated with the product and warehouse inventory
context, so different warehouses may hold different thresholds for the
same product.

There is no global product-level minimum threshold.

Minimum stock is master data and is stored separately from the derived
inventory balance.
