BULK_THRESHOLD = 10
BULK_DISCOUNT_PERCENT = 10


def line_total(quantity, unit_cents):
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    total = quantity * unit_cents
    if quantity >= BULK_THRESHOLD:
        total -= total * BULK_DISCOUNT_PERCENT // 100
    return total
