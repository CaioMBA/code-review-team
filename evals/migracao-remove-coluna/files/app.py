import pathlib
import smtplib
import sqlite3
from email.message import EmailMessage

import config

DB_PATH = "clientes.db"
MIGRACOES = pathlib.Path(__file__).parent / "migrations"


def conectar(caminho=DB_PATH):
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn


def aplicar_migracoes(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS migracoes (nome TEXT PRIMARY KEY)")
    feitas = {r["nome"] for r in conn.execute("SELECT nome FROM migracoes")}
    for arquivo in sorted(MIGRACOES.glob("*.sql")):
        if arquivo.name in feitas:
            continue
        conn.executescript(arquivo.read_text(encoding="utf-8"))
        conn.execute("INSERT INTO migracoes (nome) VALUES (?)", (arquivo.name,))
        conn.commit()


def adicionar_cliente(conn, nome):
    cur = conn.execute("INSERT INTO clientes (nome) VALUES (?)", (nome,))
    conn.commit()
    return cur.lastrowid


def buscar_cliente(conn, cliente_id):
    return conn.execute(
        "SELECT id, nome FROM clientes WHERE id = ?", (cliente_id,)
    ).fetchone()


def adicionar_contato(conn, cliente_id, tipo, valor):
    cur = conn.execute(
        "INSERT INTO contatos (cliente_id, tipo, valor) VALUES (?, ?, ?)",
        (cliente_id, tipo, valor),
    )
    conn.commit()
    return cur.lastrowid


def listar_contatos(conn, cliente_id):
    return conn.execute(
        "SELECT tipo, valor FROM contatos WHERE cliente_id = ? ORDER BY id",
        (cliente_id,),
    ).fetchall()


def enviar_aviso(destinatario, assunto, texto):
    msg = EmailMessage()
    msg["From"] = config.REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(texto)
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.send_message(msg)


if __name__ == "__main__":
    aplicar_migracoes(conectar())
    print("banco pronto")
