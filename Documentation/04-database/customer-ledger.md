# Customer Ledger Model

## 1. Purpose

The customer ledger represents the customer's financial history.

---

## 2. Transaction Types

Possible ledger sources include:

- Opening balance
- Delivery / Invoice
- Payment
- Return
- Credit adjustment
- Other approved adjustment

---

## 3. Conceptual Example

| Date | Transaction | Debit | Credit | Balance |
| --- | --- | ---: | ---: | ---: |
| Sep 1 | Opening balance | | | 5,000 |
| Sep 3 | Delivery | 4,500 | | 9,500 |
| Sep 5 | Payment | | 5,000 | 4,500 |
| Sep 10 | Delivery | 3,000 | | 7,500 |
| Sep 15 | Payment | | 2,500 | 5,000 |

---

## 4. Rules

Ledger entries must:

- Reference the source transaction
- Record transaction date
- Record amount
- Record transaction type
- Identify the acting user where applicable
- Remain auditable

---

## 5. Balance

The balance should be derived from ledger activity or a controlled cached value backed by ledger history.
