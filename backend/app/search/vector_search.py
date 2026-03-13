import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class VectorSearch:

    def __init__(self):
        self.index = None
        self.model = SentenceTransformer(MODEL_NAME)

    def load(self):

        self.index = faiss.read_index("data/index/vector/index.faiss")

    def search(self, query, docs, top_k=10):

        embedding = self.model.encode([query])

        embedding = np.array(embedding).astype("float32")

        distances, indices = self.index.search(embedding, top_k)

        results = []

        for idx, dist in zip(indices[0], distances[0]):

            results.append({
                "doc": docs[idx],
                "vector_score": float(dist)
            })

        return results