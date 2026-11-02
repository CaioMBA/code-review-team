import unittest

from notas import media, situacao


class TestNotas(unittest.TestCase):
    def test_media(self):
        self.assertEqual(media([6, 8]), 7)

    def test_situacao_nota_sete_aprova(self):
        self.assertEqual(situacao(7), "aprovado")

    def test_situacao_reprovado(self):
        self.assertEqual(situacao(3), "reprovado")


if __name__ == "__main__":
    unittest.main()
