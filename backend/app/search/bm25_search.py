import pickle
from pathlib import Path


class BM25Search:

    def __init__(self):
        self.bm25 = None
        self.docs = None

    def load(self):

        with open("data/index/bm25/index.pkl", "rb") as f:
            self.bm25 = pickle.load(f)

        with open("data/index/bm25/docs.pkl", "rb") as f:
            self.docs = pickle.load(f)

    def search(self, query, top_k=10):

        tokens = query.split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []

        for idx, score in ranked:
            doc = self.docs[idx]

            results.append({
                "doc": doc,
                "bm25_score": float(score)
            })

        return results