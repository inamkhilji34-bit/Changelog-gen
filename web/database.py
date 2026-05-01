import sqlite3
import json
from datetime import datetime

DB_PATH = r"D:\changelog\changelog-gen\changelogs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS changelogs (
            slug TEXT PRIMARY KEY,
            repo_url TEXT,
            repo_name TEXT,
            result_json TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_changelog(slug: str, repo_url: str, repo_name: str, result: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO changelogs VALUES (?, ?, ?, ?, ?)",
        (slug, repo_url, repo_name, json.dumps(result), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_changelog(slug: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT repo_url, repo_name, result_json, created_at FROM changelogs WHERE slug=?",
        (slug,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "repo_url": row[0],
        "repo_name": row[1],
        "result": json.loads(row[2]),
        "created_at": row[3]
    }

init_db()