import unittest
from unittest import mock

import app


class SignupTest(unittest.TestCase):
    def setUp(self):
        self.db = app.connect()

    @mock.patch("app.analytics.track")
    def test_signup_creates_user(self, track):
        uid = app.signup(self.db, "ana@example.com", "Ana", "123.456.789-09", "1990-05-01", "555-0100")
        row = self.db.execute("SELECT email FROM users WHERE id = ?", (uid,)).fetchone()
        self.assertEqual(row[0], "ana@example.com")

    @mock.patch("app.analytics.track")
    def test_delete_account(self, track):
        uid = app.signup(self.db, "bo@example.com", "Bo", "987.654.321-00", "1985-02-02", "555-0101")
        app.delete_account(self.db, uid)
        self.assertIsNone(self.db.execute("SELECT id FROM users WHERE id = ?", (uid,)).fetchone())


if __name__ == "__main__":
    unittest.main()