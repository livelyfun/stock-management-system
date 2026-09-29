# Functional Requirements

## 1. Authentication

### FR-AUTH-001

Users must be able to securely log in.

### FR-AUTH-002

Users must be able to log out.

### FR-AUTH-003

Sessions must expire according to the configured security policy.

### FR-AUTH-004

Password reset must use secure reset tokens.

### FR-AUTH-005

Inactive users must not be able to authenticate.

### FR-AUTH-006

Privileged users should support MFA where appropriate.

---

## 2. Authorization

### FR-AUTHZ-001

The application must implement role-based access control.

### FR-AUTHZ-002

Authorization must be enforced server-side.

### FR-AUTHZ-003

Frontend visibility must never be considered a security boundary.

### FR-AUTHZ-004

Object-level authorization must be applied to protected resources.

---

## 3. Customers

### FR-CUST-001

Create customers.

### FR-CUST-002

Update customers.

### FR-CUST-003

Deactivate customers.

### FR-CUST-004

Search customers.

### FR-CUST-005

View customer transaction history.

### FR-CUST-006

View customer ledger.

### FR-CUST-007

View customer outstanding balance.

---

## 4. Employees

### FR-EMP-001

Create employees.

### FR-EMP-002

Update employees.

### FR-EMP-003

Activate/deactivate employees.

### FR-EMP-004

View employee deliveries.

### FR-EMP-005

View employee collections.

### FR-EMP-006

View employee outstanding amounts.

---

## 5. Products

### FR-PROD-001

Create products.

### FR-PROD-002

Update products.

### FR-PROD-003

Deactivate products.

### FR-PROD-004

Manage product categories.

### FR-PROD-005

Maintain price history.

### FR-PROD-006

Prevent historical transaction prices from changing.

---

## 6. Inventory

### FR-INV-001

Record opening stock.

### FR-INV-002

Record production. **Deferred — post-MVP.**

### FR-INV-003

Record purchases. **Deferred — post-MVP.**

### FR-INV-004

Record deliveries.

### FR-INV-005

Record returns.

### FR-INV-006

Record damage, through the adjustments mechanism with its own movement
type.

### FR-INV-007

Record loss, through the adjustments mechanism with its own movement type.

### FR-INV-008

Record adjustments.

### FR-INV-009

Record transfers. **Deferred — post-MVP.**

### FR-INV-010

Maintain inventory movement history.

### FR-INV-011

Maintain current inventory balances per product and warehouse.

### FR-INV-012

Only MVP-enabled movement types may be used. Deferred movement types
must be rejected in the MVP.

### FR-INV-013

Reject any stock-consuming transaction that would cause on-hand to fall
below zero. No override exists.

### FR-INV-014

Maintain a minimum-stock threshold per product and warehouse.

---

## 6a. Transaction Resilience

### FR-TXN-001

Stock-changing transactions must lock the affected inventory balance
rows before validating and updating stock.

### FR-TXN-002

Availability validation, the balance update, and the movement creation
must occur in the same database transaction.

### FR-TXN-003

Retry only recognized transient concurrency failures, with a maximum of
3 attempts and backoff of 100 ms then 250 ms.

### FR-TXN-004

Never retry business-rule or validation failures, including insufficient
stock.

### FR-TXN-005

Return a generic retryable transaction error after the final failed
attempt, without exposing database internals.

### FR-TXN-006

Log the failure with the request or correlation ID for diagnosis.

---

## 7. Deliveries

### FR-DEL-001

Create delivery drafts.

### FR-DEL-002

Confirm deliveries.

### FR-DEL-003

Post deliveries.

### FR-DEL-004

Generate unique delivery numbers.

### FR-DEL-005

Validate customer.

### FR-DEL-006

Validate employee.

### FR-DEL-007

Validate product references.

### FR-DEL-008

Calculate totals on the server.

### FR-DEL-009

Update inventory atomically.

### FR-DEL-010

Create invoice where applicable.

### FR-DEL-011

Update customer ledger.

### FR-DEL-012

Create audit event.

### FR-DEL-013

Record the warehouse the delivery is fulfilled from. Warehouse is
required.

### FR-DEL-014

Posting a delivery must affect the stock of the recorded warehouse, and
must respect the zero floor for that warehouse's on-hand quantity.

---

## 8. Returns

### FR-RET-001

Create return transactions.

### FR-RET-002

Link returns to original deliveries.

### FR-RET-003

Validate eligible return quantity.

### FR-RET-004

Update inventory.

### FR-RET-005

Apply appropriate financial/ledger adjustment.

### FR-RET-006

Record return audit event.

---

## 9. Payments

### FR-PAY-001

Create payments.

### FR-PAY-002

Validate payment amount.

### FR-PAY-003

Allocate payments to invoices.

### FR-PAY-004

Prevent invalid over-allocation.

### FR-PAY-005

Generate payment receipts.

### FR-PAY-006

Update customer ledger.

### FR-PAY-007

Record payment audit event.

---

## 10. Search

Search must support:

- Date range
- Customer
- Employee
- Product
- Warehouse
- Delivery status
- Payment status
- Credit status
- Transaction type
- Invoice status

---

## 11. Audit

Sensitive operations must generate audit events.

At minimum:

- Login success
- Login failure
- Password reset
- User creation
- Role changes
- Customer changes
- Product changes
- Price changes
- Delivery creation
- Delivery posting
- Delivery void
- Return creation
- Payment creation
- Payment void
- Stock adjustment
- Credit adjustment
- Settings changes
