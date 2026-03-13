#!/usr/bin/env bash
set -e

echo "Starting Hybrid Search System..."

PYTHON=python

echo "Installing dependencies..."
$PYTHON -m pip install -r requirements.txt

# ----------------------------
# Generate dataset
# ----------------------------

if [ ! -f "data/raw/doc_0.txt" ]; then
  echo "Generating dataset..."
  $PYTHON backend/app/utils/generate_dataset.py
fi

# ----------------------------
# Run ingestion
# ----------------------------

if [ ! -f "data/processed/docs.jsonl" ]; then
  echo "Running ingestion..."
  cd backend
  $PYTHON -m app.ingest --input ../data/raw --out ../data/processed/docs.jsonl
  cd ..
fi

# ----------------------------
# Build indexes
# ----------------------------

if [ ! -f "data/index/vector/index.faiss" ]; then
  echo "Building indexes..."
  cd backend
  $PYTHON -m app.index --input ../data/processed/docs.jsonl
  cd ..
fi

# ----------------------------
# Start FastAPI
# ----------------------------

echo "Starting FastAPI server..."

(
  cd backend
  $PYTHON -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000
) &

# ----------------------------
# Start Streamlit
# ----------------------------

echo "Starting Streamlit dashboard..."

$PYTHON -m streamlit run frontend/dashboard.py