import unittest

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.conn = app.connect(":memory:")
        app.init_db(self.conn)
        self.conn.execute("INSERT INTO shops (id, name) VALUES (1, 'Ana Store')")

    def tearDown(self):
        self.conn.close()

    def test_add_order(self):
        customer = app.add_customer(self.conn, 1, "Bruno", "bruno@example.com")
        order = app.add_order(self.conn, 1, customer, 4990)
        row = self.conn.execute("SELECT total_cents FROM orders WHERE id = ?", (order,)).fetchone()
        self.assertEqual(row["total_cents"], 4990)


if __name__ == "__main__":
    unittest.main()
