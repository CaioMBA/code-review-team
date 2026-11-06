import unittest

import payroll


class GrossTest(unittest.TestCase):
    def test_gross(self):
        self.assertEqual(payroll.gross(10, 15.5), 155.0)


class InssTest(unittest.TestCase):
    def test_inss_3000(self):
        self.assertEqual(payroll.inss(3000), 360.0)

    def test_net_3000(self):
        self.assertEqual(payroll.net(3000), 2640.0)


if __name__ == "__main__":
    unittest.main()