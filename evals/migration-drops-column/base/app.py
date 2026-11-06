import pathlib
import sqlite3

DB_PATH = "customers.db"
MIGRATIONS = pathlib.Path(__file__).parent / "migrations"


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def apply_migrations(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY)")
    done = {r["name"] for r in conn.execute("SELECT name FROM migrations")}
    for script in sorted(MIGRATIONS.glob("*.sql")):
        if script.name in done:
            continue
        conn.executescript(script.read_text(encoding="utf-8"))
        conn.execute("INSERT INTO migrations (name) VALUES (?)", (script.name,))
        conn.commit()


def add_customer(conn, name, phone=None):
    cur = conn.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone)
    )
    conn.commit()
    return cur.lastrowid


def get_customer(conn, customer_id):
    return conn.execute(
        "SELECT id, name, phone FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()


if __name__ == "__main__":
    apply_migrations(connect())
    print("database ready")
