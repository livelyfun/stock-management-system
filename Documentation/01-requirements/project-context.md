# Stock Management System — Project Context

## 1. Purpose

The Stock Management System is an internal web-based business management / ERP application for managing a water factory's stock, sales, deliveries, returns, payments, customer credit, employees, and business transactions.

The system must provide a secure and auditable way to manage inventory and financial operations.

---

## 2. Business

The factory sells and distributes bottled and reusable-container water products.

Customers may include:

- Shops
- Schools
- Hotels
- Offices
- Restaurants
- Distributors
- Companies
- Individuals
- Other customer types

---

## 3. Primary Users

The initial user roles are:

- Super Admin
- Admin
- Manager
- Accountant
- Inventory Staff
- Delivery Staff
- Viewer

---

## 4. Core Principle

Inventory, payments, credit, returns, and historical transactions must be represented as traceable business transactions.

Current balances may be cached for performance, but transaction history remains the source of truth.

---

## 5. Transaction Integrity

Financial and inventory transactions must not be silently edited or deleted after posting.

Corrections must use controlled:

- Reversal transactions
- Adjustment transactions
- Void workflows
- Archive workflows

The original transaction history must remain auditable.

---

## 6. Initial Products

The system should initially support:

- 1 litre bottle
- 1 litre customised bottle
- Camper / cold jar
- Jar
- 500ml bottle

Products must be configurable so additional products can be added without changing application code.

---

## 7. Core Modules

The system should contain:

- Authentication
- Users
- Roles and permissions
- Customers
- Employees
- Products
- Categories
- Pricing
- Warehouses
- Inventory
- Deliveries
- Returns
- Invoices
- Payments
- Customer credit
- Customer ledger
- Employee ledger
- Receipts
- Reports
- Audit logs
- Attachments
- Settings

---

## 8. Technology Direction

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

Start with a modular monolith using Next.js server/API capabilities.

A dedicated API layer such as NestJS or Fastify may be introduced later if the application becomes significantly larger.

### Database

PostgreSQL.

### Data Access

Use a typed ORM/query builder such as:

- Drizzle ORM
- Prisma

### Cache / Background Jobs

Redis may be used for:

- Rate limiting
- Temporary caching
- Background job coordination

### File Storage

S3-compatible object storage may be used for:

- Generated documents
- Attachments
- Export files

---

## 9. Architecture Principles

1. PostgreSQL is the transactional database.
2. The application starts as a modular monolith.
3. Authorization is enforced server-side.
4. Inventory movement history is authoritative.
5. Customer ledger history is authoritative.
6. Deliveries, returns, invoices, and payments remain separate transactions.
7. Posted transactions are immutable except through controlled reversal/adjustment workflows.
8. Financial totals are calculated server-side.
9. Multi-record business operations use database transactions.
10. Sensitive operations generate audit events.
11. Backups and restore testing are part of the system.
12. The UI must support both office users and mobile delivery staff.

---

## 10. MVP

The first usable release should include:

- Authentication
- Roles
- Customers
- Employees
- Products
- Inventory
- Warehouses
- Deliveries
- Returns
- Invoices
- Payments
- Receipts
- Customer credit
- Customer ledger
- Search
- Core reports
- Audit logs

Multiple warehouses are included from the MVP, with inventory scoped to
a warehouse. Warehouse transfers, warehouse-scoped pricing, and
warehouse-scoped authorization are not included.

Advanced functionality can be added later.

---

## 11. Important Rule for AI Agents

When implementing this project:

- Do not invent business rules.
- Follow the documents in this directory.
- Do not silently change architectural decisions.
- Do not bypass security requirements.
- Do not modify posted financial or inventory transactions directly.
- Preserve transaction history.
- Prefer server-side validation.
- Prefer database constraints in addition to application validation.
- Ask for clarification when a requirement is genuinely ambiguous.
