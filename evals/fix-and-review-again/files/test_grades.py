import unittest

from grades import average, status


class TestGrades(unittest.TestCase):
    def test_average(self):
        self.assertEqual(average([6, 8]), 7)

    def test_status_seven_passes(self):
        self.assertEqual(status(7), "passed")

    def test_status_failed(self):
        self.assertEqual(status(3), "failed")


if __name__ == "__main__":
    unittest.main()
