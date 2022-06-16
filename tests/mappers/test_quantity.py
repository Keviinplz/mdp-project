import unittest
from io import StringIO
from unittest.mock import patch

from src.exceptions.data import LineFormatError
from src.mappers.quantity import QuantityMapper


class TestQuantityMapper(unittest.TestCase):
    """Test Suite for Quantity mapper"""

    # ((max_ts - min_ts) // (5 * 60 * 1000)) + 1

    def setUp(self):
        base_ts: int = 1648827850000
        self.text = (
            f"0\t{base_ts}#{base_ts}\t1\n"
            f"1\t{12356 + base_ts}#{34094 + base_ts}\t3\n"
            f"2\t{16311 + base_ts}#{16311 + base_ts}\t1\n"
        )
        self.expected = f"0\t1\t1\n" f"1\t1\t3\n" f"2\t1\t1\n"
        self.mapper = QuantityMapper()
        self.source = StringIO(self.text)

    def test_fail_format(self):
        """
        Should raise a LineFormatError if line has not the correct format

        That means line should have:
         * Length of 3
         * Separated by '\t'
         * First field must be integer
         * Second field must be length of 2, separated by '#' and all numbers must be integers
         * Third field must be integer
        """
        with self.assertRaises(
            LineFormatError, msg="Line should be formatted property before processing"
        ):
            self.mapper.map("some")
            self.mapper.map("a\tb\tc")
            self.mapper.map("1\t2\t3")

        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.map("0\t0#0\t1")
            self.assertNotEqual(out.getvalue(), "")

    def test_print_stdout_separated_by_tabs(self):
        """
        After processing data, should print the data separated by tabs

        Length of out must be 3 and have to follow this structure:
          user\tmax_moves\tmoves
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.map("0\t0#0\t1")

            expected = "0\t1\t1\n"
            result = out.getvalue()

            self.assertEqual(len(result.split("\t")), 3)
            self.assertEqual(out.getvalue(), expected)

    def test_use_case(self):
        """
        After processing the test data, should print the expected output
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.source = self.source
            self.mapper.run()
            self.assertEqual(out.getvalue(), self.expected)
