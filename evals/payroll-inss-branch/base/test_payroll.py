import unittest

import payroll


class GrossTest(unittest.TestCase):
    def test_gross(self):
        self.assertEqual(payroll.gross(10, 15.5), 155.0)


if __name__ == "__main__":
    unittest.main()
