from app.search.hybrid_ranker import hybrid_rank

def test_hybrid_rank():
    bm25 = [{"doc": {"doc_id": 1}, "bm25_score": 0.8}]
    vector = [{"doc": {"doc_id": 1}, "vector_score": 0.7}]

    results = hybrid_rank(bm25, vector)

    assert len(results) == 1