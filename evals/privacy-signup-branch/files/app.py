import logging
import sqlite3

import analytics

log = logging.getLogger("members")


def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT)")
    db.execute(
        "CREATE TABLE profiles (user_id INTEGER, cpf TEXT, birth_date TEXT, phone TEXT, marketing_opt_in INTEGER)"
    )
    return db


def signup(db, email, name, cpf, birth_date, phone, marketing_opt_in=True):
    log.info("new signup email=%s cpf=%s", email, cpf)
    cur = db.execute("INSERT INTO users (email, name) VALUES (?, ?)", (email, name))
    user_id = cur.lastrowid
    db.execute(
        "INSERT INTO profiles VALUES (?, ?, ?, ?, ?)",
        (user_id, cpf, birth_date, phone, int(marketing_opt_in)),
    )
    analytics.track("signup", {"email": email, "cpf": cpf, "birth_date": birth_date})
    return user_id


def delete_account(db, user_id):
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return True