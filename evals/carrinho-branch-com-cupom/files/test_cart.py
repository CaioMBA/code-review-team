import unittest

from cart import Carrinho


class TestCarrinho(unittest.TestCase):
    def test_subtotal(self):
        c = Carrinho()
        c.adicionar("caneca", 25.0, 2)
        self.assertEqual(c.subtotal(), 50.0)

    def test_cupom_percentual(self):
        c = Carrinho()
        c.adicionar("caneca", 25.0, 4)
        c.aplicar_cupom("BEMVINDO10")
        self.assertEqual(c.total(), 90.0)

    def test_cupom_nao_acumula(self):
        c = Carrinho()
        c.adicionar("camiseta", 49.9, 1)
        c.aplicar_cupom("FRETE5")
        c.aplicar_cupom("FRETE5")
        self.assertAlmostEqual(c.total(), 44.9)


if __name__ == "__main__":
    unittest.main()
