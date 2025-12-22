# bank_project/bank_app/services/db_storage.py

import sqlite3
from pathlib import Path
from bank_project.account import bank

DB_FILE = (Path(__file__).resolve().parents[2] / "data" / "bank.db")


def get_conn():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create tables if they don't exist."""
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            name TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (account_name) REFERENCES accounts(name)
        )
        """)

        conn.commit()


def load_accounts():
    """Load accounts from DB into {name: bank(...)}."""
    init_db()

    # reset global counters
    bank.num_bank_acc = 0
    bank.total_bank_balance = 0

    accounts = {}

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, password, balance FROM accounts")
        rows = cur.fetchall()

        for name, password, balance in rows:
            acc = bank(name, password, balance)
            acc.history = load_recent_history(name, limit=5)
            accounts[name] = acc

    return accounts


def upsert_account(acc: bank):
    """Insert or update an account row."""
    init_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO accounts (name, password, balance)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
              password=excluded.password,
              balance=excluded.balance
        """, (acc.name, acc.password, acc.balance))
        conn.commit()


def delete_account(name: str):
    """Delete account and its transactions."""
    init_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE account_name = ?", (name,))
        cur.execute("DELETE FROM accounts WHERE name = ?", (name,))
        conn.commit()


def log_transaction(account_name: str, tx_type: str, amount=None, note=None):
    """Write a transaction record."""
    init_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (account_name, type, amount, note)
            VALUES (?, ?, ?, ?)
        """, (account_name, tx_type, amount, note))
        conn.commit()


def load_recent_history(account_name: str, limit: int = 5):
    """Return the last N transactions as strings (newest first)."""
    init_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT type, amount, note, created_at
            FROM transactions
            WHERE account_name = ?
            ORDER BY id DESC
            LIMIT ?
        """, (account_name, limit))
        rows = cur.fetchall()

    history = []
    for tx_type, amount, note, created_at in rows:
        if amount is None:
            history.append(f"{created_at} | {tx_type} | {note or ''}".strip())
        else:
            history.append(
                f"{created_at} | {tx_type} | ${amount} | {note or ''}".strip())
    return history
