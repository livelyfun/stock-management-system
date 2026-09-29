## Project Knowledge / RAG

Authoritative documentation lives in `Documentation/`. Load the
`stock-rag` skill before any domain-sensitive work; it defines how to
query, how to cite, and how to handle documentation that conflicts with
the code.

Maintenance (venv is `.rag/venv`, never `.zag/venv`):

- `.rag/venv/bin/python rag/ingest.py` — required after editing
  `Documentation/`, or the next session retrieves stale rules.
- `.rag/venv/bin/python rag/evaluate.py --k 5` (from `rag/`) — check
  retrieval quality against `rag/golden.json`.

The RAG is supplementary. Always inspect the actual source code and
database schema before making changes.
