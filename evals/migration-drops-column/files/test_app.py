import os
import unittest
from unittest import mock

os.environ.setdefault("SMTP_HOST", "localhost")

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.conn = app.connect(":memory:")
        app.apply_migrations(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_customer(self):
        cid = app.add_customer(self.conn, "Ana")
        self.assertEqual(app.get_customer(self.conn, cid)["name"], "Ana")

    def test_contacts(self):
        cid = app.add_customer(self.conn, "Ana")
        app.add_contact(self.conn, cid, "phone", "555-0100")
        app.add_contact(self.conn, cid, "email", "ana@example.com")
        contacts = app.list_contacts(self.conn, cid)
        self.assertEqual([c["kind"] for c in contacts], ["phone", "email"])

    def test_send_notice(self):
        with mock.patch("smtplib.SMTP") as smtp:
            app.send_notice("ana@example.com", "Hi", "Your details were updated")
        smtp.return_value.__enter__.return_value.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
