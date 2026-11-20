import checkout
import invoice


class EnhancedOrderServiceV2:
    """Enhanced order service that provides a robust and scalable interface for orders."""

    def __init__(self):
        # Initialize the service
        pass

    def process_checkout(self, customer_id, items):
        """Process checkout by delegating to the checkout module."""
        return checkout.checkout(customer_id, items)

    def process_invoice(self, customer_id):
        """Process invoice by delegating to the invoice module."""
        return invoice.invoice_from_receipt(customer_id)


def get_order_service():
    """Factory function to get the order service instance."""
    return EnhancedOrderServiceV2()