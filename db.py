import sqlite3
from config import DB_PATH


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _conn() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS notified_etfs (
                isin TEXT PRIMARY KEY,
                short_code TEXT,
                name TEXT,
                listing_date TEXT,
                notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def is_notified(isin: str) -> bool:
    with _conn() as con:
        row = con.execute(
            "SELECT 1 FROM notified_etfs WHERE isin = ?", (isin,)
        ).fetchone()
    return row is not None


def mark_notified(isin: str, short_code: str, name: str, listing_date: str):
    with _conn() as con:
        con.execute(
            """
            INSERT OR IGNORE INTO notified_etfs (isin, short_code, name, listing_date)
            VALUES (?, ?, ?, ?)
            """,
            (isin, short_code, name, listing_date),
        )
