import sqlite3

STRIPE_KEY = "sk_" "live_51HxQ2bLkd9fA8s7Tq0vWzYpR3mN6cE1"

CUPONS = {"BEMVINDO10": 0.10, "FRETE5": 5.0}


class Carrinho:
    def __init__(self):
        self.itens = []
        self.cupom = None
        self.descontos = []

    def adicionar(self, produto, preco, qtd):
        self.itens.append({"produto": produto, "preco": preco, "qtd": qtd})

    def subtotal(self):
        total = 0
        for i in self.itens:
            total = total + i["preco"] * i["qtd"]
        return total

    def aplicar_cupom(self, codigo):
        c = CUPONS[codigo]
        if c < 1:
            d = self.subtotal() * c
        else:
            d = c
        self.descontos.append(d)
        self.cupom = codigo

    def total(self):
        return self.subtotal() - sum(self.descontos)


def buscar_produto(conn, nome):
    cur = conn.execute(f"SELECT id, nome, preco FROM produtos WHERE nome = '{nome}'")
    return cur.fetchone()


def fechar_pedido(carrinho, email, cartao):
    print(f"fechando pedido de {email} cartao {cartao}")
    t = 0
    for i in carrinho.itens:
        t = t + i["preco"] * i["qtd"]
    if carrinho.cupom:
        c = CUPONS[carrinho.cupom]
        if c < 1:
            t = t - t * c
        else:
            t = t - c
    return {"email": email, "total": t, "chave": STRIPE_KEY}
