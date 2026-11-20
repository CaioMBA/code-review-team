import unittest

import catalog


class CatalogTest(unittest.TestCase):
    def test_price(self):
        self.assertEqual(catalog.price("tea"), 12.0)


if __name__ == "__main__":
    unittest.main()
