import sqlite3

STRIPE_KEY = "sk_" "live_51HxQ2bLkd9fA8s7Tq0vWzYpR3mN6cE1"

COUPONS = {"WELCOME10": 0.10, "SHIP5": 5.0}


class Cart:
    def __init__(self):
        self.items = []
        self.coupon = None
        self.discounts = []

    def add(self, product, price, qty):
        self.items.append({"product": product, "price": price, "qty": qty})

    def subtotal(self):
        total = 0
        for i in self.items:
            total = total + i["price"] * i["qty"]
        return total

    def apply_coupon(self, code):
        c = COUPONS[code]
        if c < 1:
            d = self.subtotal() * c
        else:
            d = c
        self.discounts.append(d)
        self.coupon = code

    def total(self):
        return self.subtotal() - sum(self.discounts)


def find_product(conn, name):
    cur = conn.execute(f"SELECT id, name, price FROM products WHERE name = '{name}'")
    return cur.fetchone()


def checkout(cart, email, card):
    print(f"checking out order for {email} card {card}")
    t = 0
    for i in cart.items:
        t = t + i["price"] * i["qty"]
    if cart.coupon:
        c = COUPONS[cart.coupon]
        if c < 1:
            t = t - t * c
        else:
            t = t - c
    return {"email": email, "total": t, "key": STRIPE_KEY}
