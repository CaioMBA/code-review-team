import pathlib
import smtplib
import sqlite3
from email.message import EmailMessage

import config

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


def add_customer(conn, name):
    cur = conn.execute("INSERT INTO customers (name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid


def get_customer(conn, customer_id):
    return conn.execute(
        "SELECT id, name FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()


def add_contact(conn, customer_id, kind, value):
    cur = conn.execute(
        "INSERT INTO contacts (customer_id, kind, value) VALUES (?, ?, ?)",
        (customer_id, kind, value),
    )
    conn.commit()
    return cur.lastrowid


def list_contacts(conn, customer_id):
    return conn.execute(
        "SELECT kind, value FROM contacts WHERE customer_id = ? ORDER BY id",
        (customer_id,),
    ).fetchall()


def send_notice(recipient, subject, text):
    msg = EmailMessage()
    msg["From"] = config.SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(text)
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.send_message(msg)


if __name__ == "__main__":
    apply_migrations(connect())
    print("database ready")
