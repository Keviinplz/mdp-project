import unittest
from io import StringIO
from unittest.mock import patch
from src.exceptions.data import LineFormatError

from src.reducers.quantity import QuantityReducer


class TestQuantityReducer(unittest.TestCase):
    """Test Suite for Quantity reducer"""

    def setUp(self):
        self.five_mins = 300000
        self.text = (
            f"0\t0\t1\t1\n"
            f"1\t{self.five_mins * 10}\t10\t4\n"
            f"2\t{self.five_mins * 10}\t10\t10\n"
            f"3\t{self.five_mins * 100}\t100\t98\n"
            f"4\t{self.five_mins * 5}\t5\t2\n"
        )
        self.expected = (
            f"2\t{self.five_mins * 10}\t10\t10\n"
            f"3\t{self.five_mins * 100}\t100\t98\n"
        )

        self.reducer = QuantityReducer()
        self.source = StringIO(self.text)

    def test_fail_format(self):
        """
        Should raise a LineFormatError if line has not the correct format

        That means line should have:
         * Length of 4
         * Separated by tabs
         * All fields should be integers
        """
        with self.assertRaises(
            LineFormatError, msg="Line should be formatted property before processing"
        ):
            self.reducer.reduce("some")
            self.reducer.reduce("a,b,c,d,e,3")
            self.reducer.reduce("1,2,3,4")
            self.reducer.reduce("1\t2\t3\ta")

        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.source = StringIO(f"2\t{self.five_mins * 10}\t10\t10\n")
            self.reducer.run()
            self.assertNotEqual(out.getvalue(), "")

    def test_print_stdout_separated_by_tabs(self):
        """
        After processing data, should print the data separated by tabs

        Length of out must be 4 and have to follow this structure:
          user\ttimelapse\tmax_moves\tmoves
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.reduce(f"2\t{self.five_mins * 10}\t10\t10")

            expected = f"2\t{self.five_mins * 10}\t10\t10\n"
            result = out.getvalue()

            self.assertEqual(len(result.split("\t")), 4)
            self.assertEqual(out.getvalue(), expected)

    def test_filter_no_bots(self):
        """
        Should filter lines that have no bots

        We define a bot if:
         * max_move and moves are equal or the subtraction of max_move and moves is less than 2
         * diff_ts is not 0
        """
        with patch("sys.stdout", new=StringIO()) as out:  # not filter
            self.reducer.reduce(f"2\t{self.five_mins * 10}\t10\t10")

            expected = f"2\t{self.five_mins * 10}\t10\t10\n"
            result = out.getvalue()

            self.assertEqual(len(result.split("\t")), 4)
            self.assertEqual(out.getvalue(), expected)

        with patch("sys.stdout", new=StringIO()) as out:  # filter
            self.reducer.reduce(f"0\t0\t1\t1")

            expected = ""
            result = out.getvalue()

            self.assertEqual(len(result.split("\t")), 1)
            self.assertEqual(out.getvalue(), expected)

        with patch("sys.stdout", new=StringIO()) as out:  # filter
            self.reducer.reduce(f"4\t{self.five_mins * 5}\t5\t2")

            expected = ""
            result = out.getvalue()

            self.assertEqual(len(result.split("\t")), 1)
            self.assertEqual(out.getvalue(), expected)

    def test_use_case(self):
        """
        After processing the test data, should print the expected output
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.source = self.source
            self.reducer.run()
            self.assertEqual(out.getvalue(), self.expected)
