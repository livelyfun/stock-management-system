import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTATION_DIR = PROJECT_ROOT / "Documentation"

QDRANT_URL = "http://localhost:6333"

COLLECTION_NAME = "stock_management_knowledge"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
MIN_CHUNK_SIZE = 40

TOP_K = 5

# Number of candidates retrieved before reranking.
RETRIEVAL_CANDIDATES = 30

# Bump when the indexing schema changes so the collection rebuilds.
SCHEMA_VERSION = 4

# Persist the embedding model cache instead of relying on the ephemeral
# system temp directory (e.g. /tmp) which is wiped on reboot.
MODEL_CACHE_DIR = PROJECT_ROOT / ".rag" / "model_cache"
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault(
    "FASTEMBED_CACHE_PATH",
    str(MODEL_CACHE_DIR),
)