import os
import unittest
from unittest import mock

os.environ.setdefault("SMTP_HOST", "localhost")

import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.conn = app.conectar(":memory:")
        app.aplicar_migracoes(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_adicionar_cliente(self):
        cid = app.adicionar_cliente(self.conn, "Ana")
        self.assertEqual(app.buscar_cliente(self.conn, cid)["nome"], "Ana")

    def test_contatos(self):
        cid = app.adicionar_cliente(self.conn, "Ana")
        app.adicionar_contato(self.conn, cid, "telefone", "11 99999-0000")
        app.adicionar_contato(self.conn, cid, "email", "ana@exemplo.com")
        contatos = app.listar_contatos(self.conn, cid)
        self.assertEqual([c["tipo"] for c in contatos], ["telefone", "email"])

    def test_enviar_aviso(self):
        with mock.patch("smtplib.SMTP") as smtp:
            app.enviar_aviso("ana@exemplo.com", "Oi", "Seu cadastro foi atualizado")
        smtp.return_value.__enter__.return_value.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
