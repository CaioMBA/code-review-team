import unittest

from pricing import line_total


class TestPricing(unittest.TestCase):
    def test_line_total(self):
        self.assertEqual(line_total(3, 250), 750)

    def test_rejects_zero_quantity(self):
        with self.assertRaises(ValueError):
            line_total(0, 250)

    def test_no_discount_below_threshold(self):
        self.assertEqual(line_total(9, 100), 900)

    def test_bulk_discount_at_threshold(self):
        self.assertEqual(line_total(10, 100), 900)

    def test_bulk_discount_rounds_down_in_cents(self):
        self.assertEqual(line_total(10, 333), 2997)


if __name__ == "__main__":
    unittest.main()
