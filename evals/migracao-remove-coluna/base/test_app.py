import unittest

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.conn = app.conectar(":memory:")
        app.aplicar_migracoes(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_adicionar_cliente(self):
        cid = app.adicionar_cliente(self.conn, "Ana", "11 99999-0000")
        cliente = app.buscar_cliente(self.conn, cid)
        self.assertEqual(cliente["nome"], "Ana")
        self.assertEqual(cliente["telefone"], "11 99999-0000")


if __name__ == "__main__":
    unittest.main()
