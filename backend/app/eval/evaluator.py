import json
import pandas as pd
from pathlib import Path

from app.search.bm25_search import BM25Search
from app.search.vector_search import VectorSearch
from app.search.hybrid_ranker import hybrid_rank


def dcg(relevances):
    score = 0
    for i, rel in enumerate(relevances):
        score += rel / (1 + i)
    return score


def ndcg_at_k(relevances, k=10):
    actual = dcg(relevances[:k])
    ideal = dcg(sorted(relevances, reverse=True)[:k])
    return actual / ideal if ideal > 0 else 0


def recall_at_k(results, relevant_docs, k=10):
    retrieved = [r["doc"]["doc_id"] for r in results[:k]]
    hits = len(set(retrieved) & set(relevant_docs))
    return hits / len(relevant_docs)


def mrr_at_k(results, relevant_docs, k=10):
    for i, r in enumerate(results[:k]):
        if r["doc"]["doc_id"] in relevant_docs:
            return 1 / (i + 1)
    return 0


def run_eval():

    queries = json.load(open("../data/eval/queries.json"))
    qrels = json.load(open("../data/eval/qrels.json"))

    bm25 = BM25Search()
    vector = VectorSearch()

    bm25.load()
    vector.load()

    docs = bm25.docs

    ndcg_scores = []
    recall_scores = []
    mrr_scores = []

    for q in queries:

        results = hybrid_rank(
            bm25.search(q, 10),
            vector.search(q, docs, 10),
            alpha=0.5
        )

        relevant = qrels[q]

        relevances = [
            1 if r["doc"]["doc_id"] in relevant else 0
            for r in results
        ]

        ndcg_scores.append(ndcg_at_k(relevances))
        recall_scores.append(recall_at_k(results, relevant))
        mrr_scores.append(mrr_at_k(results, relevant))

    metrics = {
        "ndcg@10": sum(ndcg_scores) / len(ndcg_scores),
        "recall@10": sum(recall_scores) / len(recall_scores),
        "mrr@10": sum(mrr_scores) / len(mrr_scores),
    }

    print(metrics)

    Path("../data/metrics").mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([metrics])

    file = "../data/metrics/experiments.csv"

    if Path(file).exists():
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)