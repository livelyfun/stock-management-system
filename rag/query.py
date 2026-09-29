from __future__ import annotations

import re
import sys
from collections import Counter

from qdrant_client import QdrantClient
from fastembed import TextEmbedding

from config import (
    QDRANT_URL,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
    RETRIEVAL_CANDIDATES,
)

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do",
    "does", "for", "from", "has", "have", "how", "in", "is", "it",
    "of", "on", "or", "should", "that", "the", "to", "what", "when",
    "where", "which", "who", "why", "with", "must", "need", "required",
}


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized search tokens,
    excluding common stop words.
    """
    return [
        token
        for token in re.findall(
            r"[a-zA-Z0-9_-]{2,}",
            text.lower(),
        )
        if token not in _STOPWORDS
    ]


def keyword_score(
    query: str,
    content: str,
    heading_path: str = "",
) -> float:
    """
    Score lexical overlap between the query and a chunk.

    Rewards content that covers most query terms and repeats them,
    plus a small bonus when the query terms appear in the heading path.
    """

    query_tokens = tokenize(query)

    if not query_tokens:
        return 0.0

    content_counts = Counter(
        tokenize(content)
    )

    # Heading-path terms carry strong signal (e.g. section named
    # "2. Roles"), so count them as part of the chunk's content.
    if heading_path:
        for token in tokenize(heading_path):
            content_counts[token] += 1

    matched_terms = {
        token
        for token in query_tokens
        if token in content_counts
    }

    term_coverage = len(matched_terms) / len(query_tokens)

    intensity = sum(
        min(content_counts[token], 3)
        for token in matched_terms
    ) / sum(
        min(content_counts[token], 3)
        or 1
        for token in query_tokens
    )

    heading_tokens = tokenize(heading_path)

    path_bonus = (
        sum(
            1
            for token in query_tokens
            if token in heading_tokens
        )
        / len(query_tokens)
    ) * 0.25

    return min(
        (term_coverage * 0.7)
        + (intensity * 0.3)
        + path_bonus,
        1.0,
    )


def semantic_search(
    client,
    embedding_model,
    query: str,
):
    """
    Retrieve semantically similar chunks.
    """

    query_vector = list(
        embedding_model.embed([query])
    )[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=RETRIEVAL_CANDIDATES,
        with_payload=True,
        with_vectors=False,
    )

    return results.points


def combine_scores(
    semantic_score: float,
    keyword_score_value: float,
) -> float:
    """
    Combine semantic and lexical relevance.

    Semantic search gets higher weight because it captures
    meaning, while keyword matching helps with exact terms.
    """

    return (
        (semantic_score * 0.7)
        + (keyword_score_value * 0.3)
    )


def apply_diversity(
    ranked_results: list[dict],
    top_k: int,
    max_per_source: int = 2,
) -> list[dict]:
    """
    Cap how many chunks a single document may contribute
    so results stay diverse across documents.
    """

    selected: list[dict] = []
    seen: Counter = Counter()

    for result in ranked_results:
        source = result["source"]

        if seen[source] >= max_per_source:
            continue

        selected.append(result)
        seen[source] += 1

        if len(selected) >= top_k:
            break

    return selected


_client = None
_embedding_model = None


def get_client():
    """
    Return the shared Qdrant client.

    The client is created once per process. Rebuilding it on every search
    adds connection overhead and, when the model is reloaded alongside it,
    dominates the runtime of batch callers such as evaluate.py.
    """

    global _client

    if _client is None:
        _client = QdrantClient(
            url=QDRANT_URL
        )

    return _client


def get_embedding_model():
    """
    Return the shared embedding model.

    Loading all-MiniLM-L6-v2 takes seconds, so it is created once per
    process instead of once per query.
    """

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = TextEmbedding(
            model_name=EMBEDDING_MODEL
        )

    return _embedding_model


def search(query: str, top_k: int = TOP_K):

    client = get_client()

    embedding_model = get_embedding_model()

    results = semantic_search(
        client,
        embedding_model,
        query,
    )

    ranked_results = []

    for result in results:

        payload = result.payload or {}

        content = payload.get(
            "content",
            "",
        )

        heading_path = payload.get(
            "heading_path",
            "unknown",
        )

        kw_score = keyword_score(
            query,
            content,
            heading_path,
        )

        final_score = combine_scores(
            result.score,
            kw_score,
        )

        ranked_results.append(
            {
                "score": final_score,
                "semantic_score": result.score,
                "keyword_score": kw_score,
                "source": payload.get(
                    "source",
                    "unknown",
                ),
                "heading_path": heading_path,
                "section": payload.get(
                    "section",
                    "unknown",
                ),
                "line_start": payload.get(
                    "line_start",
                    0,
                ),
                "line_end": payload.get(
                    "line_end",
                    0,
                ),
                "document_type": payload.get(
                    "document_type",
                    "unknown",
                ),
                "content": content,
            }
        )

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return apply_diversity(
        ranked_results,
        top_k,
    )


def format_result(result: dict) -> str:
    lines = ["-" * 70]

    lines.append(
        f"Source:    "
        f"{result['source']} "
        f"(lines {result['line_start']}-{result['line_end']})"
    )

    lines.append(
        f"Section:   {result['heading_path']}"
    )

    lines.append(
        f"Score:     "
        f"{result['score']:.4f} "
        f"(semantic {result['semantic_score']:.4f}, "
        f"keyword {result['keyword_score']:.4f})"
    )

    lines.append("-" * 70)

    lines.append(result["content"])

    return "\n".join(lines)


def main():

    if len(sys.argv) < 2:

        print(
            'Usage: python rag/query.py "your question"'
        )

        return

    query = " ".join(sys.argv[1:])

    print()
    print("=" * 70)
    print("RAG SEARCH")
    print("=" * 70)

    print(f"\nQuery: {query}")

    results = search(query)

    if not results:

        print("\nNo relevant documentation found.")

        return

    print(
        f"\nRetrieved {len(results)} relevant chunks."
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print()
        print(f"Result #{index}")

        print(format_result(result))

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()