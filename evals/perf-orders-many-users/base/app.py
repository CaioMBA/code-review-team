import sqlite3

DB_PATH = "shopdesk.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    shop_id INTEGER NOT NULL REFERENCES shops(id),
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    shop_id INTEGER NOT NULL REFERENCES shops(id),
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total_cents INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def add_customer(conn, shop_id, name, email):
    cur = conn.execute(
        "INSERT INTO customers (shop_id, name, email) VALUES (?, ?, ?)",
        (shop_id, name, email),
    )
    conn.commit()
    return cur.lastrowid


def add_order(conn, shop_id, customer_id, total_cents):
    cur = conn.execute(
        "INSERT INTO orders (shop_id, customer_id, total_cents) VALUES (?, ?, ?)",
        (shop_id, customer_id, total_cents),
    )
    conn.commit()
    return cur.lastrowid
