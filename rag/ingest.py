from pathlib import Path
import hashlib
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from fastembed import TextEmbedding

from chunker import chunk_markdown
from config import (
    DOCUMENTATION_DIR,
    QDRANT_URL,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    SCHEMA_VERSION,
)

DOCUMENT_TYPE_MAP = {
    "00-ai-context": "ai-context",
    "01-requirements": "requirements",
    "02-business-rules": "business-rules",
    "03-architecture": "architecture",
    "04-database": "database",
    "05-security": "security",
    "06-api": "api",
    "07-frontend": "frontend",
    "08-workflows": "workflows",
    "09-testing": "testing",
    "10-deployment": "deployment",
    "11-project": "project",
}


def document_type_for(folder: str) -> str:
    return DOCUMENT_TYPE_MAP.get(folder, folder)


def get_file_hash(path: Path) -> str:
    """Return SHA-256 hash of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_documents():
    """Return all Markdown documentation files."""
    return list(DOCUMENTATION_DIR.rglob("*.md"))


def existing_schema_version(client):
    """
    Retrieve the schema version stored on the first indexed point.

    Returns:
        int or None if the collection has no points yet.
    """

    points, _next_offset = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1,
        with_payload=True,
        with_vectors=False,
    )

    if not points:
        return None

    payload = points[0].payload or {}

    return payload.get("schema_version")


def ensure_collection(client, embedding_model):
    """Create the collection if needed, rebuilding it when the schema version changes."""

    collections = client.get_collections()

    existing = {
        collection.name
        for collection in collections.collections
    }

    if COLLECTION_NAME in existing:
        current_version = existing_schema_version(client)

        if current_version != SCHEMA_VERSION:
            print(
                f"Schema version changed "
                f"({current_version} -> {SCHEMA_VERSION}). "
                f"Recreating collection."
            )
            client.delete_collection(COLLECTION_NAME)
        else:
            return

    test_vector = list(
        embedding_model.embed(["test"])
    )[0]

    vector_size = len(test_vector)

    print(f"Creating collection: {COLLECTION_NAME}")
    print(f"Vector size: {vector_size}")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def get_existing_hashes(client):
    """
    Retrieve hashes already stored in Qdrant.

    Returns:
        dict[source, hash]
    """

    existing = {}

    offset = None

    while True:
        points, next_offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        for point in points:
            payload = point.payload or {}

            source = payload.get("source")
            file_hash = payload.get("file_hash")

            if source and file_hash:
                existing[source] = file_hash

        if next_offset is None:
            break

        offset = next_offset

    return existing


def delete_document_chunks(client, source):
    """Delete all vectors belonging to a document."""

    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source),
                )
            ]
        ),
    )


def index_document(client, embedding_model, document):
    """Index a single Markdown document."""

    relative_path = document.relative_to(
        DOCUMENTATION_DIR
    )

    source = str(relative_path)

    file_hash = get_file_hash(document)

    print(f"\nIndexing: {source}")

    content = document.read_text(
        encoding="utf-8"
    )

    chunks = chunk_markdown(
        content=content,
        source=source,
    )

    if not chunks:
        print("  No chunks found.")
        return 0

    # Remove old chunks for this document.
    delete_document_chunks(
        client,
        source,
    )

    texts = [
        chunk.embed_text
        for chunk in chunks
    ]

    vectors = list(
        embedding_model.embed(texts)
    )

    points = []

    for chunk, vector in zip(chunks, vectors):

        point_id = str(uuid.uuid4())

        points.append(
            PointStruct(
                id=point_id,
                vector=vector.tolist(),
                payload={
                    "content": chunk.content,
                    "source": chunk.source,
                    "heading_path": chunk.heading_path,
                    "section": chunk.section,
                    "document_title": chunk.document_title,
                    "chunk_index": chunk.chunk_index,
                    "total_chunks": chunk.total_chunks,
                    "line_start": chunk.line_start,
                    "line_end": chunk.line_end,
                    "file_hash": file_hash,
                    "document_type": document_type_for(
                        document.parent.name
                    ),
                    "schema_version": SCHEMA_VERSION,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"  Indexed chunks: {len(points)}")

    return len(points)


def remove_deleted_documents(client, current_sources):
    """
    Remove documents from Qdrant that no longer exist
    in Documentation/.
    """

    existing_hashes = get_existing_hashes(client)

    for source in existing_hashes:

        if source not in current_sources:

            print(
                f"\nRemoving deleted document: {source}"
            )

            delete_document_chunks(
                client,
                source,
            )


def main():

    print("=" * 60)
    print("Stock Management System RAG Ingestion")
    print("=" * 60)

    client = QdrantClient(
        url=QDRANT_URL
    )

    print(f"Qdrant: {QDRANT_URL}")

    print(
        f"Loading embedding model: {EMBEDDING_MODEL}"
    )

    embedding_model = TextEmbedding(
        model_name=EMBEDDING_MODEL
    )

    ensure_collection(
        client,
        embedding_model,
    )

    documents = load_documents()

    print(
        f"\nFound {len(documents)} Markdown documents."
    )

    existing_hashes = get_existing_hashes(
        client
    )

    current_sources = set()

    indexed_documents = 0
    skipped_documents = 0
    total_chunks = 0

    for document in documents:

        source = str(
            document.relative_to(
                DOCUMENTATION_DIR
            )
        )

        current_sources.add(source)

        file_hash = get_file_hash(
            document
        )

        # Skip unchanged documents.
        if existing_hashes.get(source) == file_hash:

            print(
                f"\nSkipping unchanged: {source}"
            )

            skipped_documents += 1
            continue

        chunks = index_document(
            client,
            embedding_model,
            document,
        )

        indexed_documents += 1
        total_chunks += chunks

    # Remove files that no longer exist.
    remove_deleted_documents(
        client,
        current_sources,
    )

    print("\n" + "=" * 60)
    print("RAG ingestion completed")
    print("=" * 60)

    print(
        f"Documents found:      {len(documents)}"
    )

    print(
        f"Documents indexed:    {indexed_documents}"
    )

    print(
        f"Documents skipped:    {skipped_documents}"
    )

    print(
        f"New chunks indexed:   {total_chunks}"
    )

    print(
        f"Collection:           {COLLECTION_NAME}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
