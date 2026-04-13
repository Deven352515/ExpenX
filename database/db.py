import sqlite3
import os
from flask import g
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    if "_database" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g._database = conn
    return g._database


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    db.commit()


def create_user(name: str, email: str, password: str) -> int:
    password_hash = generate_password_hash(password)
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    db.commit()
    return cursor.lastrowid


def seed_db():
    db = get_db()

    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        return

    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    sample_expenses = [
        (user_id, 350.00,  "Food",          "2026-04-01", "Grocery run"),
        (user_id, 120.50,  "Transport",     "2026-04-03", "Auto rickshaw + metro"),
        (user_id, 1500.00, "Bills",         "2026-04-05", "Electricity bill"),
        (user_id, 800.00,  "Health",        "2026-04-07", "Pharmacy medicines"),
        (user_id, 499.00,  "Entertainment", "2026-04-09", "OTT subscription"),
        (user_id, 2200.00, "Shopping",      "2026-04-11", "Clothes"),
        (user_id, 650.00,  "Other",         "2026-04-13", "Stationery supplies"),
        (user_id, 180.00,  "Food",          "2026-04-15", "Dinner with friends"),
    ]

    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    db.commit()
