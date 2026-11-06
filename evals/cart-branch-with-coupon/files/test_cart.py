import unittest

from cart import Cart


class TestCart(unittest.TestCase):
    def test_subtotal(self):
        c = Cart()
        c.add("mug", 25.0, 2)
        self.assertEqual(c.subtotal(), 50.0)

    def test_coupon_percentage(self):
        c = Cart()
        c.add("mug", 25.0, 4)
        c.apply_coupon("WELCOME10")
        self.assertEqual(c.total(), 90.0)

    def test_coupon_does_not_stack(self):
        c = Cart()
        c.add("t-shirt", 49.9, 1)
        c.apply_coupon("SHIP5")
        c.apply_coupon("SHIP5")
        self.assertAlmostEqual(c.total(), 44.9)


if __name__ == "__main__":
    unittest.main()
