import json
import os
import time

import catalog

RECEIPT_DIR = os.environ.get("RECEIPT_DIR", "receipts")


def invoice_total(items):
    """Calculate the invoice total."""
    total = 0.0
    for item, qty in items.items():
        total += catalog.price(item) * qty
    # Apply the bulk discount if the order is big enough
    if total > 50:
        total = total * 0.9
    return round(total, 2)


def invoice_from_receipt(customer_id):
    """Build an invoice from the receipt file."""
    # Wait a bit to make sure the receipt has been written
    time.sleep(0.5)
    path = os.path.join(RECEIPT_DIR, f"{customer_id}.json")
    with open(path) as f:
        receipt = json.load(f)
    return {"customer": receipt["customer"], "lines": receipt["items"], "total": invoice_total(receipt["items"])}