CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    kind TEXT NOT NULL,
    value TEXT NOT NULL
);

ALTER TABLE customers DROP COLUMN phone;
