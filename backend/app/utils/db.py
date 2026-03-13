import sqlite3
from pathlib import Path

DB_PATH = Path("../data/metrics/search_logs.db")


def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    return conn


def init_db():

    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS search_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        latency_ms REAL,
        top_k INTEGER,
        alpha REAL,
        result_count INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def log_query(query, latency, top_k, alpha, result_count):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO search_logs
        (query, latency_ms, top_k, alpha, result_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (query, latency, top_k, alpha, result_count)
    )

    conn.commit()
    conn.close()