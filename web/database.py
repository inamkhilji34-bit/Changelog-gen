import sqlite3
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "changelogs.db")

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

def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    from datetime import timedelta

    total = conn.execute(
        "SELECT COUNT(*) FROM changelogs"
    ).fetchone()[0]

    today = conn.execute(
        "SELECT COUNT(*) FROM changelogs WHERE created_at LIKE ?",
        (f"{datetime.utcnow().strftime('%Y-%m-%d')}%",)
    ).fetchone()[0]

    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    week = conn.execute(
        "SELECT COUNT(*) FROM changelogs WHERE created_at > ?",
        (week_ago,)
    ).fetchone()[0]

    popular = conn.execute(
        """SELECT repo_name, COUNT(*) as count 
           FROM changelogs 
           GROUP BY repo_name 
           ORDER BY count DESC LIMIT 10"""
    ).fetchall()

    recent = conn.execute(
        """SELECT slug, repo_name, repo_url, created_at 
           FROM changelogs 
           ORDER BY created_at DESC LIMIT 15"""
    ).fetchall()

    conn.close()

    return {
        "total": total,
        "today": today,
        "week": week,
        "popular": [{"repo": r[0], "count": r[1]} for r in popular],
        "recent": [{"slug": r[0], "repo": r[1], "url": r[2], "created_at": r[3]} for r in recent]
    }
