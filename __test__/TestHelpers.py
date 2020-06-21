import unittest
from src.helpers.MatrixCreation import is_valid_col_row


class TestHelpers(unittest.TestCase):
    def test_valid_cols_and_rows(self):
        """ Should check if column and row are valid """
        ok_result = is_valid_col_row(2, 3)
        self.assertTrue(ok_result)

        negative_result = is_valid_col_row(-2, 0)
        self.assertFalse(negative_result)

        type_error_result = is_valid_col_row("1", "3")
        self.assertFalse(type_error_result)

        type_error_result = is_valid_col_row([], {})
        self.assertFalse(type_error_result)

        type_error_result = is_valid_col_row(1.1, 2.2)
        self.assertFalse(type_error_result)
