import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "database" / "phishing.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                indicators_json TEXT NOT NULL,
                summary TEXT NOT NULL,
                content_hash TEXT NOT NULL
            )
        """)
        conn.commit()

def save_evidence(content, message_type, risk_score, risk_level, indicators, summary, content_hash):
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO evidence
            (created_at, message_type, content, risk_score, risk_level, indicators_json, summary, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (created_at, message_type, content, risk_score, risk_level,
              json.dumps(indicators, ensure_ascii=False), summary, content_hash))
        conn.commit()
        return cursor.lastrowid

def _row_to_dict(row):
    if row is None:
        return None
    result = dict(row)
    result["indicators_list"] = json.loads(result.pop("indicators_json"))
    return result

def get_evidence(evidence_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM evidence WHERE id = ?", (evidence_id,)).fetchone()
    return _row_to_dict(row)

def list_evidence(limit=200):
    query = "SELECT * FROM evidence ORDER BY id DESC"
    params = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_row_to_dict(row) for row in rows]
