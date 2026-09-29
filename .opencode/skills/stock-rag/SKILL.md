---
name: stock-rag
description: Use when a task touches Stock Management System rules or architecture that may be documented but not obvious from code - inventory, stock and stock movements, stock adjustments, products, warehouses and warehouse locations, suppliers, purchase orders, purchasing, sales, users and roles, transfers, deliveries, returns, customer ledger, credit, payments, database schema/constraints/transactions, authentication, authorization, RBAC, business rules, audit logging, API contracts, security, or architecture decisions. Retrieves authoritative excerpts from Documentation/ via the rag-search tool before implementing or changing behavior, and reports documentation-vs-code conflicts instead of silently changing rules.
---

# Stock Management RAG

Retrieves authoritative project knowledge from `Documentation/` so that
domain behavior is driven by the documented rules, not by guesswork.

## How to call it

Call the `rag-search` tool with a natural-language question:

```
rag-search(query: "stock transfer validation between warehouses")
```

The query is embedded and matched against every Markdown file under
`Documentation/`. The venv is at `.rag/venv`; the index lives in Qdrant.

## Reading the output

Each result is a chunk of a source document:

```
Source:    02-business-rules/inventory-rules.md (lines 3-82)
Section:   Inventory Rules
Score:     0.4968 (semantic 0.5163, keyword 0.4514)
```

- `Source` plus the line range is the citable handle. When you rely on a
  rule, reference it as `path (lines N-M)` so it can be verified.
- `Section` is the heading path. A match in a heading is a strong signal
  the chunk is on-topic.
- `Score` is the combined ranking. Low scores mean weak matches, so verify
  the chunk actually states the rule before treating it as authoritative.
- Results are diversity-capped at two chunks per document, so one
  authoritative file may appear once even when it holds several relevant
  sections. Re-query with narrower terms rather than assuming it is
  exhausted.

## Query strategy

Run 2-3 narrow queries per task rather than one broad one. Split by
concern:

1. the business rule
2. the security or authorization requirement
3. the database or transaction requirement

Good:

- "stock transfer validation between warehouses"
- "authorization rules for inventory adjustment"
- "database transaction requirements for stock movement"
- "negative stock policy on delivery"

Avoid vague queries such as "tell me about inventory" - they match
broadly and rank poorly.

## Before implementation

1. Identify the business concept involved.
2. Query the RAG knowledge base.
3. Review the retrieved sources.
4. Inspect the relevant source code.
5. Compare documentation with the implementation.
6. If there is a conflict, report it before changing behavior.

## Prerequisites and recovery

The tool needs two local services, and the virtualenv path is
`.rag/venv` (never `.zag/venv`):

- Qdrant on `http://localhost:6333`
- the virtualenv at `.rag/venv`

Check both before trusting a result:

```bash
curl -s http://localhost:6333/collections
# expect: the stock_management_knowledge collection listed

ls .rag/venv/bin/python
# expect: the path is printed
```

If Qdrant is not responding, start it with
`docker compose -f docker-compose.rag.yml up -d`.

If `rag-search` returns nothing relevant, the index is probably stale
rather than the question being wrong. Re-ingest and retry:

```bash
.rag/venv/bin/python rag/ingest.py
```

Unchanged files are skipped, so this is cheap to run.

## After editing documentation

Documentation edits are not searchable until re-ingested. After adding or
modifying anything under `Documentation/`, run
`.rag/venv/bin/python rag/ingest.py`, otherwise the next session
retrieves stale rules. Verify retrieval quality with
`.rag/venv/bin/python rag/evaluate.py --k 5` from `rag/`.

## Authority

Project requirements and approved documentation are authoritative for
intended behavior.

Source code represents the current implementation.

Do not silently change documented business behavior because an
implementation currently behaves differently.

## Do not

- invent business rules
- invent database constraints
- invent security requirements
- assume undocumented behavior
- act on a rule you did not retrieve from the RAG
- overwrite project decisions without identifying the conflict
