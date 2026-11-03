import sqlite3
import time

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

RATE_LIMIT = 60
RATE_WINDOW_SECONDS = 60

_orders_cache = {}
_request_log = {}


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


def list_orders(conn, shop_id):
    if shop_id in _orders_cache:
        return _orders_cache[shop_id]

    orders = []
    rows = conn.execute(
        "SELECT id, customer_id, total_cents, created_at FROM orders "
        "WHERE shop_id = ? ORDER BY created_at DESC",
        (shop_id,),
    ).fetchall()
    for row in rows:
        customer = conn.execute(
            "SELECT name, email FROM customers WHERE id = ?",
            (row["customer_id"],),
        ).fetchone()
        orders.append({
            "id": row["id"],
            "total_cents": row["total_cents"],
            "created_at": row["created_at"],
            "customer_name": customer["name"],
            "customer_email": customer["email"],
        })

    _orders_cache[shop_id] = orders
    return orders


def allow_request(shop_id, now=None):
    now = time.time() if now is None else now
    recent = [t for t in _request_log.get(shop_id, []) if now - t < RATE_WINDOW_SECONDS]
    if len(recent) >= RATE_LIMIT:
        _request_log[shop_id] = recent
        return False
    recent.append(now)
    _request_log[shop_id] = recent
    return True


def orders_page(conn, shop_id):
    if not allow_request(shop_id):
        return 429, {"error": "Too many requests, try again in a minute."}
    return 200, {"orders": list_orders(conn, shop_id)}
