class Cart:
    def __init__(self):
        self.items = []

    def add(self, product, price, qty):
        self.items.append({"product": product, "price": price, "qty": qty})

    def subtotal(self):
        total = 0
        for i in self.items:
            total = total + i["price"] * i["qty"]
        return total

    def total(self):
        return self.subtotal()
