def normalize(scores):

    min_s = min(scores)
    max_s = max(scores)

    if max_s - min_s == 0:
        return [0 for _ in scores]

    return [(s - min_s) / (max_s - min_s) for s in scores]


def hybrid_rank(bm25_results, vector_results, alpha=0.5):

    bm25_scores = [r["bm25_score"] for r in bm25_results]
    vector_scores = [r["vector_score"] for r in vector_results]

    bm25_norm = normalize(bm25_scores)
    vector_norm = normalize(vector_scores)

    results = []

    for i in range(len(bm25_results)):

        hybrid = alpha * bm25_norm[i] + (1 - alpha) * vector_norm[i]

        results.append({
            "doc": bm25_results[i]["doc"],
            "bm25_score": bm25_scores[i],
            "vector_score": vector_scores[i],
            "hybrid_score": hybrid
        })

    return sorted(results, key=lambda x: x["hybrid_score"], reverse=True)