import unittest
from io import StringIO
from unittest.mock import patch
from src.exceptions.data import LineFormatError

from src.reducers.user import UserReducer


class TestUserReducer(unittest.TestCase):
    """Test Suite for User reducer"""

    def setUp(self):
        base_ts: int = 1648827850000
        self.text = (
            f"0\t{base_ts}\t1\n"
            f"1\t{21388 + base_ts}\t1\n"
            f"1\t{12356 + base_ts}\t1\n"
            f"1\t{34094 + base_ts}\t1\n"
            f"2\t{16311 + base_ts}\t1\n"
        )
        self.expected = (
            f"0\t{base_ts}#{base_ts}\t1\n"
            f"1\t{12356 + base_ts}#{34094 + base_ts}\t3\n"
            f"2\t{16311 + base_ts}#{16311 + base_ts}\t1\n"
        )

        self.reducer = UserReducer()
        self.source = StringIO(self.text)

    def test_fail_format(self):
        """
        Should raise a LineFormatError if line has not the correct format

        That means line should have:
         * Length of 3
         * Separated by tabs
         * All fields should be integers
        """
        with self.assertRaises(
            LineFormatError, msg="Line should be formatted property before processing"
        ):
            self.reducer.reduce("some")
            self.reducer.reduce("a,b,c,d,e,3")
            self.reducer.reduce("1,2,3")
            self.reducer.reduce("1\t2\ta")

        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.source = StringIO("1\t1648827850000\t3")
            self.reducer.run()
            self.assertNotEqual(out.getvalue(), "")

    def test_print_stdout_separated_by_tabs(self):
        """
        After processing data, should print the data separated by tabs

        Length of out must be 3 and have to follow this structure:
          user\ttimestamp#timestamp\tcount
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.source = StringIO("1\t1648827850000\t3")
            self.reducer.run()
            expected = "1\t1648827850000#1648827850000\t3\n"
            result = out.getvalue()

            self.assertEqual(
                len(result.split("\t")), 3, f"Line should be length of 3: {result}"
            )
            self.assertEqual(out.getvalue(), expected)

    def test_use_case(self):
        """
        After processing the test data, should print the expected output
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.reducer.source = self.source
            self.reducer.run()
            self.assertEqual(out.getvalue(), self.expected)
