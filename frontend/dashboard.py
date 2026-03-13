import streamlit as st
import requests
import sqlite3
import pandas as pd
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

DB_PATH = Path("../data/metrics/search_logs.db")
EXP_PATH = Path("../data/metrics/experiments.csv")


st.set_page_config(page_title="Hybrid Search Dashboard", layout="wide")

st.title("Hybrid Search + KPI Dashboard")

page = st.sidebar.selectbox(
    "Navigation",
    ["Search", "KPIs", "Evaluation", "Debug"]
)

# ---------------- SEARCH PAGE ----------------

if page == "Search":

    st.header("Search")

    query = st.text_input("Enter query")

    if st.button("Search"):

        res = requests.post(
            f"{API_URL}/search",
            json={"query": query}
        )

        results = res.json()["results"]

        for r in results:

            st.subheader(r["doc"]["title"])

            st.write("BM25 Score:", r["bm25_score"])
            st.write("Vector Score:", r["vector_score"])
            st.write("Hybrid Score:", r["hybrid_score"])

            st.divider()

# ---------------- KPI PAGE ----------------

elif page == "KPIs":

    st.header("Search KPIs")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM search_logs",
        conn
    )

    conn.close()

    st.metric(
        "Total Searches",
        len(df)
    )

    if len(df) > 0:

        st.metric(
            "Average Latency (ms)",
            round(df["latency_ms"].mean(), 2)
        )

        st.subheader("Top Queries")

        top_queries = df["query"].value_counts().head(10)

        st.bar_chart(top_queries)

# ---------------- EVALUATION PAGE ----------------

elif page == "Evaluation":

    st.header("Evaluation Metrics")

    if EXP_PATH.exists():

        df = pd.read_csv(EXP_PATH)

        st.dataframe(df)

        st.line_chart(df)

    else:

        st.write("No experiments recorded yet.")

# ---------------- DEBUG PAGE ----------------

elif page == "Debug":

    st.header("Recent Queries")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM search_logs ORDER BY timestamp DESC LIMIT 20",
        conn
    )

    conn.close()

    st.dataframe(df)