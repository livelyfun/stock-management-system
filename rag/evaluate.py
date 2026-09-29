from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from query import search

GOLDEN_FILE = Path(__file__).parent / "golden.json"


def evaluate(top_k: int) -> int:
    if not GOLDEN_FILE.exists():
        print(f"Missing golden file: {GOLDEN_FILE}")
        return 1

    data = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))
    questions = data["questions"]

    print("=" * 80)
    print(f"RAG EVALUATION  (top_k={top_k}, {len(questions)} questions)")
    print("=" * 80)

    total_recall = 0.0
    total_mrr = 0.0
    full_recall_questions = 0

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        expected = item["expected_sources"]

        results = search(question)[:top_k]
        sources = [result["source"] for result in results]

        matched = [source for source in expected if source in sources]
        recall = len(matched) / len(expected)

        mrr = 0.0
        for rank, source in enumerate(sources, start=1):
            if source in expected:
                mrr = 1.0 / rank
                break

        total_recall += recall
        total_mrr += mrr

        if recall == 1.0:
            full_recall_questions += 1

        print(
            f"\nQ{index:02d} recall={recall:.2f} mrr={mrr:.2f}"
        )
        print(f"  Q: {question}")
        print(f"  Expected: {', '.join(expected)}")
        print(f"  Matched:  {', '.join(matched) if matched else '-'}")

        for rank, source in enumerate(sources, start=1):
            marker = " *" if source in expected else ""
            print(
                f"    {rank}. {source}{marker}"
            )

    count = len(questions)

    avg_recall = total_recall / count
    avg_mrr = total_mrr / count
    full_percent = (full_recall_questions / count) * 100

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(
        f"Average Recall@{top_k}:     {avg_recall:.4f}"
    )
    print(
        f"Average MRR (per source):  {avg_mrr:.4f}"
    )
    print(
        f"Questions with full recall: {full_recall_questions}/{count} ({full_percent:.1f}%)"
    )
    print("=" * 80)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate RAG retrieval quality against golden questions."
    )
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Top-K results to consider (default: 5).",
    )
    args = parser.parse_args()

    if args.k <= 0:
        print("--k must be a positive integer.")
        return 1

    return evaluate(top_k=args.k)


if __name__ == "__main__":
    sys.exit(main())