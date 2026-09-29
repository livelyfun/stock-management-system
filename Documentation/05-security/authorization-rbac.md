# Authorization and RBAC

## 1. Principle

Authorization must be enforced server-side.

Frontend visibility is not a security mechanism.

---

## 2. Roles

### Super Admin

Full system administration.

### Admin

Business operations and management.

### Manager

Operations, inventory, and reports.

### Accountant

Invoices, payments, credit, ledger, and financial reports.

### Inventory Staff

Products, stock, movements, and returns.

### Delivery Staff

Assigned deliveries, collections, and returns.

### Viewer

Read-only access.

---

## 3. Permission Model

Permissions should represent actions rather than only pages.

Examples:

- customer.read
- customer.create
- customer.update
- customer.deactivate

- product.read
- product.create
- product.update

- inventory.read
- inventory.adjust

- delivery.read
- delivery.create
- delivery.confirm
- delivery.post
- delivery.void

- return.read
- return.create

- invoice.read
- invoice.create
- invoice.void

- payment.read
- payment.create
- payment.void

- report.read

- user.manage
- role.manage
- settings.manage

- audit.read

---

## 4. Deny by Default

If a permission is not explicitly granted, the action must be denied.

---

## 5. Object-Level Authorization

Permission to access a resource does not automatically mean access to every resource instance.

The system must validate access scope where required.

---

## 6. Browser Input

Never trust:

- user ID
- role
- permission
- customer ID
- employee ID
- organization scope

provided by the browser.

The server must determine authorized scope.
