import path from "node:path"
import { tool } from "@opencode-ai/plugin"

const RELATIVE_PYTHON = path.join(".rag", "venv", "bin", "python")
const RELATIVE_SCRIPT = path.join("rag", "query.py")
const TIMEOUT_MS = 60_000
const MAX_OUTPUT_CHARS = 20_000

export default tool({
  description:
    "Search the Stock Management System project documentation using the local RAG knowledge base. Call this before implementing or changing anything governed by documented rules: inventory, stock, products, warehouses, transfers, movements, adjustments, deliveries, returns, purchasing, sales, customer ledger, credit, payments, database schema, constraints, transactions, authentication, authorization, RBAC, audit logging, API contracts, security requirements, or architecture decisions. Returns matching chunks from Documentation/ with their source path, heading, and line ranges.",

  args: {
    query: tool.schema
      .string()
      .min(3)
      .describe(
        "A specific natural-language question about a project rule, requirement, or decision",
      ),
  },

  async execute(args, context) {
    const root = context.worktree || context.directory || process.cwd()
    const python = path.join(root, RELATIVE_PYTHON)
    const script = path.join(root, RELATIVE_SCRIPT)

    context.metadata({ title: `rag-search: ${args.query}` })

    let output: string

    try {
      output = await Bun.$`${python} ${script} ${args.query}`
        .timeout(TIMEOUT_MS)
        .text()
    } catch (error) {
      const reason = error instanceof Error ? error.message : String(error)

      return [
        "rag-search failed.",
        "",
        `Reason: ${reason}`,
        "",
        "Check the prerequisites:",
        "- Qdrant must be running on http://localhost:6333",
        "  Start it with: docker compose -f docker-compose.rag.yml up -d",
        `- The virtualenv must exist at ${RELATIVE_PYTHON}`,
        "- The index is built from Documentation/ by rag/ingest.py",
      ].join("\n")
    }

    const trimmed = output.trim()

    if (!trimmed) {
      return "The RAG knowledge base returned no output for this query."
    }

    if (trimmed.length > MAX_OUTPUT_CHARS) {
      return `${trimmed.slice(0, MAX_OUTPUT_CHARS)}\n\n[output truncated]`
    }

    return trimmed
  },
})
