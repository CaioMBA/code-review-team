import json
import logging
import os

import catalog

log = logging.getLogger(__name__)

RECEIPT_DIR = os.environ.get("RECEIPT_DIR", "receipts")


def subtotal(items):
    # Loop over each item and add its price times quantity to the total
    total = 0.0
    for item, qty in items.items():
        # Get the price of the item from the catalog
        total += catalog.price(item) * qty
    return total


def checkout(customer_id, items):
    """Process the checkout for a customer with the given items."""
    log.info("🛒 Starting checkout for customer %s! 🚀", customer_id)
    total = subtotal(items)
    # Apply the bulk discount if the order is big enough
    if total > 100:
        total = total * 0.9
    # Special pricing
    if customer_id == 42:
        total = total * 0.5
    total = round(total, 2)
    write_receipt(customer_id, items, total)
    log.info("✅ Checkout complete! Total: %s 🎉", total)
    return total


def write_receipt(customer_id, items, total):
    """Write the receipt to a file."""
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    path = os.path.join(RECEIPT_DIR, f"{customer_id}.json")
    with open(path, "w") as f:
        json.dump({"customer": customer_id, "items": items, "total": total}, f)
    return path