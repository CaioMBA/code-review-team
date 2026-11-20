import os
import tempfile
import unittest

import checkout
import invoice
from order_service import get_order_service


class OrdersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        checkout.RECEIPT_DIR = self.tmp
        invoice.RECEIPT_DIR = self.tmp

    def test_checkout_small(self):
        self.assertEqual(checkout.checkout(1, {"tea": 2}), 24.0)

    def test_checkout_bulk(self):
        self.assertEqual(checkout.checkout(1, {"kettle": 2}), 108.0)

    def test_invoice_matches(self):
        svc = get_order_service()
        svc.process_checkout(7, {"kettle": 2})
        self.assertEqual(svc.process_invoice(7)["total"], 108.0)


if __name__ == "__main__":
    unittest.main()