class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar(self, produto, preco, qtd):
        self.itens.append({"produto": produto, "preco": preco, "qtd": qtd})

    def subtotal(self):
        total = 0
        for i in self.itens:
            total = total + i["preco"] * i["qtd"]
        return total

    def total(self):
        return self.subtotal()
