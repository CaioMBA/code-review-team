import unittest

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.conn = app.connect(":memory:")
        app.apply_migrations(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_customer(self):
        cid = app.add_customer(self.conn, "Ana", "555-0100")
        customer = app.get_customer(self.conn, cid)
        self.assertEqual(customer["name"], "Ana")
        self.assertEqual(customer["phone"], "555-0100")


if __name__ == "__main__":
    unittest.main()
