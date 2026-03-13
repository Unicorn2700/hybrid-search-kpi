# Hybrid Search KPI System

## Overview

This project implements a hybrid search system that combines lexical search (BM25) and semantic vector search using transformer embeddings. The system provides an API for querying documents and a dashboard for monitoring system performance and evaluation metrics.

The project demonstrates a complete search pipeline including data ingestion, indexing, hybrid retrieval, evaluation, logging, and a user interface.

---

## Features

- Hybrid search combining **BM25 lexical retrieval** and **vector semantic search**
- **FastAPI backend** for search and metrics
- **Streamlit dashboard** for interactive querying and monitoring
- **Evaluation pipeline** with:
  - nDCG@10
  - Recall@10
  - MRR@10
- **Query logging** using SQLite
- **Experiment tracking** for evaluation runs
- Fully automated setup via a single script

---

## System Architecture

The system consists of the following components:

### Data Pipeline
- Raw document ingestion
- Document preprocessing
- JSONL dataset generation

### Indexing
- BM25 lexical index
- Vector index using Sentence Transformers and FAISS

### Retrieval
- BM25 keyword retrieval
- Semantic vector retrieval
- Hybrid ranking combining both scores

### Backend API
- FastAPI server for search queries
- Query logging
- Metrics endpoint

### Dashboard
- Streamlit interface for:
  - Search queries
  - KPI visualization
  - Evaluation metrics
  - Debug logs

---

## Project Structure

```
backend/
  app/
    api/
    search/
    utils/
    eval/

frontend/
  dashboard.py

data/
  eval/

requirements.txt
up.sh
.gitignore
README.md
```

---

## Installation

Clone the repository:

```
git clone <repository-url>
cd hybrid-search-kpi
```

---

## Running the System

The entire system can be started using a single command:

```
./up.sh
```

The script will automatically:

1. Create a virtual environment
2. Install dependencies
3. Generate dataset (if missing)
4. Run ingestion
5. Build indexes
6. Start the FastAPI server
7. Launch the Streamlit dashboard

---

## Accessing the System

After running `up.sh`:

### API Documentation

```
http://localhost:8000/docs
```

### Dashboard

```
http://localhost:8501
```

---

## API Endpoints

### Search

```
POST /search
```

Example request:

```json
{
  "query": "machine learning"
}
```

Returns ranked documents including BM25 score, vector similarity score, and hybrid score.

---

### Metrics

```
GET /metrics
```

Returns:

- total search requests
- average query latency

---

### Health Check

```
GET /health
```

Used to verify that the API server is running.

---

## Evaluation

The system includes an evaluation harness to measure retrieval quality.

Run evaluation using:

```
python -m app.eval
```

Metrics computed:

- nDCG@10
- Recall@10
- MRR@10

Results are stored in:

```
data/metrics/experiments.csv
```

Each run appends a new experiment entry.

---

## Logging

Search queries are logged in a SQLite database:

```
data/metrics/search_logs.db
```

Logged information includes:

- query text
- latency
- timestamp
- number of results returned
- ranking parameters

---

## Running Tests

Run unit tests with:

- cd backend
- pytest
---

## Technologies Used

- Python
- FastAPI
- Streamlit
- FAISS
- Sentence Transformers
- SQLite
- rank-bm25

---

## Reproducibility

The project is designed to run on a clean environment using:

```
./up.sh
```

All required steps such as dataset generation, indexing, and service startup are handled automatically.

---

## Author

Ritik Singh
