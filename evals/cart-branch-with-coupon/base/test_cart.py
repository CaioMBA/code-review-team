import unittest

from cart import Cart


class TestCart(unittest.TestCase):
    def test_subtotal(self):
        c = Cart()
        c.add("mug", 25.0, 2)
        self.assertEqual(c.subtotal(), 50.0)


if __name__ == "__main__":
    unittest.main()
