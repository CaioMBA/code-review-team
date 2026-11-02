import unittest
from datetime import date

from dates import days_between
from report import monthly_summary


class TestReport(unittest.TestCase):
    def test_days_between(self):
        self.assertEqual(days_between(date(2026, 1, 1), date(2026, 1, 31)), 30)

    def test_summary(self):
        out = monthly_summary([{"id": 1, "title": "Login broken", "opened": date(2026, 1, 1), "closed": date(2026, 1, 3)}])
        self.assertIn("#1 Login broken", out)


if __name__ == "__main__":
    unittest.main()
