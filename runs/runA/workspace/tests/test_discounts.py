import unittest
from datetime import date

from discounts import apply_discount

NOV_1 = date(2026, 11, 1)


class TestApplyDiscount(unittest.TestCase):
    def test_empty_code_leaves_total(self):
        self.assertEqual(apply_discount(2500, "", NOV_1), 2500)

    def test_save10_takes_ten_percent(self):
        self.assertEqual(apply_discount(1999, "SAVE10", NOV_1), 1800)

    def test_lowercase_code_works(self):
        self.assertEqual(apply_discount(2000, "save10", NOV_1), 1800)

    def test_unknown_code_is_rejected(self):
        with self.assertRaises(ValueError):
            apply_discount(2000, "FREE100", NOV_1)


if __name__ == "__main__":
    unittest.main()
