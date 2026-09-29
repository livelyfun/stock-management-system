# System Requirements

## 1. System Type

Internal web-based business management / ERP application.

---

## 2. Main Objectives

The system must:

1. Track inventory.
2. Track deliveries.
3. Track returns.
4. Generate invoices.
5. Track payments.
6. Manage customer credit.
7. Maintain customer ledgers.
8. Maintain employee activity.
9. Maintain reusable container tracking.
10. Provide business reports.
11. Maintain complete audit history.
12. Enforce role-based access.
13. Protect financial and inventory transactions.
14. Support reliable database transactions.
15. Support backups and recovery.

---

## 3. Users

The system must support:

- Super Admin
- Admin
- Manager
- Accountant
- Inventory Staff
- Delivery Staff
- Viewer

---

## 4. Authentication Requirements

The system must provide:

- Secure login
- Logout
- Password reset
- Session expiry
- Session invalidation
- Role-based access
- User activation/deactivation
- Login activity
- Audit history
- MFA for privileged users where appropriate

---

## 5. Customer Management

Customer records must support:

- Customer ID
- Name
- Customer type
- Contact person
- Phone
- Address
- PAN/VAT where applicable
- Credit limit
- Payment terms
- Opening balance
- Status
- Notes
- Created timestamp
- Updated timestamp

Customer types include:

- Shop
- School
- Hotel
- Restaurant
- Office
- Distributor
- Company
- Individual
- Other

---

## 6. Employee Management

Employee records must support:

- Employee ID
- Name
- Phone
- Address
- Role
- Joining date
- Status
- Notes

Future fields may include:

- Salary
- Advance balance
- Vehicle assignment

---

## 7. Product Management

Product records must support:

- Product ID
- SKU
- Name
- Category
- Unit
- Cost price
- Selling price
- Active/inactive status

Minimum stock is not a product-level attribute. It is a per-warehouse
value associated with the product and warehouse inventory context, so
different warehouses may hold different thresholds for the same product.

Historical prices must be preserved.

---

## 8. Inventory

The target domain movement vocabulary is:

- Opening stock
- Production
- Purchase
- Delivery
- Return
- Damage
- Loss
- Adjustment
- Transfer

These nine types are the broader target domain. The MVP-enabled types
are:

- Opening stock
- Delivery
- Return
- Damage
- Loss
- Adjustment

Production, Purchase, and Transfer are deferred. They must not become
usable merely because their values exist in the controlled vocabulary.

Inventory must maintain:

1. Movement history
2. Current balance

The movement history is authoritative.

Inventory is scoped to a warehouse. A movement records the warehouse
whose stock it affects, and the current balance is maintained per
product and warehouse.

Movement quantity is always positive, and the direction of the movement
determines whether it increases or decreases stock.

Negative on-hand stock is prohibited. A transaction that would cause
on-hand to fall below zero is rejected. No override exists.

Minimum stock is supported per warehouse.

---

## 9. Delivery

A delivery must contain:

- Delivery number
- Delivery date
- Customer
- Employee / delivery staff
- Warehouse
- Vehicle
- Items
- Quantities
- Unit prices
- Discounts/adjustments
- Payment status
- Notes

The delivery records the warehouse it is fulfilled from, and posting the
delivery affects the stock of that warehouse.

Example:

DEL-2026-00125

---

## 10. Returns

Returns must be separate transactions linked to the original delivery.

A return must record:

- Return number
- Customer
- Original delivery
- Date
- Employee
- Product
- Quantity
- Condition
- Reason
- Notes

The original delivery must not be rewritten.

---

## 11. Payments

Payments must be separate financial transactions.

The system must support:

- Full payment
- Partial payment
- Credit / pay later

Payments may be allocated to one or more invoices where appropriate.

---

## 12. Customer Credit

The customer ledger must represent:

- Opening balance
- Debits
- Credits
- Outstanding balance
- Due dates
- Overdue amounts

Conceptual model:

Delivery / Invoice → Debit

Payment / Credit Adjustment / Return → Credit or adjustment

---

## 13. Reports

The system must support:

- Daily sales
- Weekly sales
- Monthly sales
- Product sales
- Product returns
- Inventory position
- Inventory movements
- Customer purchases
- Customer payments
- Customer outstanding balances
- Employee delivery activity
- Employee collections
- Employee outstanding amounts
- Credit / overdue reports

Exports should eventually support:

- CSV
- Excel
- PDF
