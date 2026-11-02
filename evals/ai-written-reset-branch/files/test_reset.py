import unittest
from unittest import mock

import reset


class TestReset(unittest.TestCase):
    def test_create_token(self):
        token = reset.create_reset_token("Ana@Shop.com")
        self.assertTrue(token)

    def test_use_token(self):
        with mock.patch("reset.use_reset_token", return_value=True):
            self.assertTrue(reset.use_reset_token("123456", "new-pass"))


if __name__ == "__main__":
    unittest.main()
