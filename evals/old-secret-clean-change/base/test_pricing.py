import unittest

from pricing import line_total


class TestPricing(unittest.TestCase):
    def test_line_total(self):
        self.assertEqual(line_total(3, 250), 750)

    def test_rejects_zero_quantity(self):
        with self.assertRaises(ValueError):
            line_total(0, 250)


if __name__ == "__main__":
    unittest.main()
