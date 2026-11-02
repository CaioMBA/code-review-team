def line_total(quantity, unit_cents):
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    return quantity * unit_cents
