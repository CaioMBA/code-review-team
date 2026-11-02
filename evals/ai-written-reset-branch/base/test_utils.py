import unittest

from utils import format_price, normalize_email


class TestUtils(unittest.TestCase):
    def test_normalize_email(self):
        self.assertEqual(normalize_email("  Ana@Shop.com "), "ana@shop.com")

    def test_format_price(self):
        self.assertEqual(format_price(1250), "$12.50")


if __name__ == "__main__":
    unittest.main()
