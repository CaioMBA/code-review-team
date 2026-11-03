import unittest

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app._orders_cache.clear()
        app._request_log.clear()
        self.conn = app.connect(":memory:")
        app.init_db(self.conn)
        self.conn.execute("INSERT INTO shops (id, name) VALUES (1, 'Ana Store')")
        self.conn.execute("INSERT INTO shops (id, name) VALUES (2, 'Bia Shop')")

    def tearDown(self):
        self.conn.close()

    def test_add_order(self):
        customer = app.add_customer(self.conn, 1, "Bruno", "bruno@example.com")
        order = app.add_order(self.conn, 1, customer, 4990)
        row = self.conn.execute("SELECT total_cents FROM orders WHERE id = ?", (order,)).fetchone()
        self.assertEqual(row["total_cents"], 4990)

    def test_list_orders_only_own_shop(self):
        bruno = app.add_customer(self.conn, 1, "Bruno", "bruno@example.com")
        carla = app.add_customer(self.conn, 2, "Carla", "carla@example.com")
        app.add_order(self.conn, 1, bruno, 4990)
        app.add_order(self.conn, 2, carla, 1500)
        orders = app.list_orders(self.conn, 1)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["customer_name"], "Bruno")

    def test_rate_limit(self):
        for i in range(app.RATE_LIMIT):
            self.assertTrue(app.allow_request(1, now=1000 + i * 0.1))
        self.assertFalse(app.allow_request(1, now=1010))
        self.assertTrue(app.allow_request(1, now=1100))

    def test_orders_page(self):
        bruno = app.add_customer(self.conn, 1, "Bruno", "bruno@example.com")
        app.add_order(self.conn, 1, bruno, 4990)
        status, body = app.orders_page(self.conn, 1)
        self.assertEqual(status, 200)
        self.assertEqual(body["orders"][0]["total_cents"], 4990)


if __name__ == "__main__":
    unittest.main()
