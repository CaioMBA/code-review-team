import unittest

from cart import Carrinho


class TestCarrinho(unittest.TestCase):
    def test_subtotal(self):
        c = Carrinho()
        c.adicionar("caneca", 25.0, 2)
        self.assertEqual(c.subtotal(), 50.0)


if __name__ == "__main__":
    unittest.main()
