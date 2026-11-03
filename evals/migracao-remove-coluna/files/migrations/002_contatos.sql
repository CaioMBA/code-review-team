CREATE TABLE contatos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    tipo TEXT NOT NULL,
    valor TEXT NOT NULL
);

ALTER TABLE clientes DROP COLUMN telefone;
