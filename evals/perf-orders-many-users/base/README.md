# shopdesk

Order back office for small online shops. Used by ~5,000 shops, runs on 4 gunicorn workers behind nginx.

Each shop sees only its own customers and orders. Data lives in SQLite (`shopdesk.db`).

## Tests

    python -m unittest
