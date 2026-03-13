import json
import argparse
import pickle
from pathlib import Path

import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_docs(path):

    docs = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))

    return docs


def build_bm25(docs):

    corpus = [doc["text"].split() for doc in docs]

    bm25 = BM25Okapi(corpus)

    return bm25


def build_vector_index(docs):

    model = SentenceTransformer(MODEL_NAME)

    texts = [doc["text"] for doc in docs]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    return index, dim


def save_bm25(bm25, docs):

    Path("data/index/bm25").mkdir(parents=True, exist_ok=True)

    with open("data/index/bm25/index.pkl", "wb") as f:
        pickle.dump(bm25, f)

    with open("data/index/bm25/docs.pkl", "wb") as f:
        pickle.dump(docs, f)


def save_vector(index, dim):

    Path("data/index/vector").mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, "data/index/vector/index.faiss")

    metadata = {
        "model_name": MODEL_NAME,
        "dimension": dim
    }

    with open("data/index/vector/meta.json", "w") as f:
        json.dump(metadata, f)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/processed/docs.jsonl"
    )

    args = parser.parse_args()

    docs = load_docs(args.input)

    print("Loaded documents:", len(docs))

    print("Building BM25 index...")
    bm25 = build_bm25(docs)

    save_bm25(bm25, docs)

    print("Building vector index...")
    vector_index, dim = build_vector_index(docs)

    save_vector(vector_index, dim)

    print("Indexing complete")


if __name__ == "__main__":
    main()