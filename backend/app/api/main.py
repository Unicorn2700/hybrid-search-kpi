from fastapi import FastAPI
from pydantic import BaseModel

import pickle
import time

from app.search.bm25_search import BM25Search
from app.search.vector_search import VectorSearch
from app.search.hybrid_ranker import hybrid_rank
from app.utils.db import init_db, log_query
from app.utils.db import get_connection


app = FastAPI(title="Hybrid Search API")
init_db()

bm25 = BM25Search()
vector = VectorSearch()


bm25.load()
vector.load()

docs = bm25.docs


class SearchRequest(BaseModel):

    query: str
    top_k: int = 10
    alpha: float = 0.5


@app.get("/metrics")
def metrics():

    conn = get_connection()
    cursor = conn.cursor()

    total_requests = cursor.execute(
        "SELECT COUNT(*) FROM search_logs"
    ).fetchone()[0]

    avg_latency = cursor.execute(
        "SELECT AVG(latency_ms) FROM search_logs"
    ).fetchone()[0]

    conn.close()

    return {
        "search_requests_total": total_requests,
        "search_latency_ms_avg": avg_latency
    }


@app.post("/search")
def search(req: SearchRequest):

    start = time.time()

    bm25_results = bm25.search(req.query, req.top_k)
    vector_results = vector.search(req.query, docs, req.top_k)

    results = hybrid_rank(bm25_results, vector_results, req.alpha)

    latency = (time.time() - start) * 1000

    log_query(
        req.query,
        latency,
        req.top_k,
        req.alpha,
        len(results)
    )

    return {"results": results}