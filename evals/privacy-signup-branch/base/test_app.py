import unittest

import app


class ConnectTest(unittest.TestCase):
    def test_users_table(self):
        db = app.connect()
        db.execute("INSERT INTO users (email, name) VALUES ('a@example.com', 'A')")
        self.assertEqual(db.execute("SELECT COUNT(*) FROM users").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()