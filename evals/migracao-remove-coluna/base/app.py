import pathlib
import sqlite3

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


def adicionar_cliente(conn, nome, telefone=None):
    cur = conn.execute(
        "INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone)
    )
    conn.commit()
    return cur.lastrowid


def buscar_cliente(conn, cliente_id):
    return conn.execute(
        "SELECT id, nome, telefone FROM clientes WHERE id = ?", (cliente_id,)
    ).fetchone()


if __name__ == "__main__":
    aplicar_migracoes(conectar())
    print("banco pronto")
