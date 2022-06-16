import unittest
from io import StringIO
from unittest.mock import patch
from src.exceptions.data import LineFormatError

from src.mappers.user import UserMapper


class TestUserMapper(unittest.TestCase):
    """Test Suite for User mapper"""

    def setUp(self):
        base_ts: int = 1648827850000
        self.text = (
            "time,user_id,x,y,color,mod\n"
            "000000000,00000000,0042,0042,15,0\n"
            "000012356,00000001,0999,0999,22,0\n"
            "000016311,00000002,0044,0042,26,0\n"
            "000021388,00000001,0002,0002,29,0\n"
            "000034094,00000001,0023,0023,26,0\n"
            "000040229,00000005,0420,0420,09,1\n"
        )
        self.expected = (
            f"0\t{base_ts}\t1\n"
            f"1\t{12356 + base_ts}\t1\n"
            f"2\t{16311 + base_ts}\t1\n"
            f"1\t{21388 + base_ts}\t1\n"
            f"1\t{34094 + base_ts}\t1\n"
        )
        self.mapper = UserMapper()
        self.source = StringIO(self.text)

    def test_ignore_csv_header(self):
        """
        Should ignore the first line of the csv
        """
        with patch("sys.stdout", new=StringIO()) as out:
            header = "time,user_id,x,y,color,mod"
            self.mapper.map(header)
            self.assertEqual(out.getvalue(), "")

    def test_fail_format(self):
        """
        Should raise a LineFormatError if line has not the correct format

        That means line should have:
         * Length of 6
         * Separated by ','
         * All fields should be integers
         * If fields are text and has length of 6, it should be a header and ignore it
        """
        with self.assertRaises(
            LineFormatError, msg="Line should be formatted property before processing"
        ):
            self.mapper.map("some")
            self.mapper.map("a,b,c,d,e,3")
            self.mapper.map("1;2;3;4;5;6")

        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.map("1,2,3,4,5,0")
            self.assertNotEqual(out.getvalue(), "")

    def test_ignore_mod(self):
        """
        If user is mod, should ignore the line and not print it
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.map("1,2,3,4,5,1")
            self.assertEqual(out.getvalue(), "")

    def test_print_stdout_separated_by_tabs(self):
        """
        After processing data, should print the data separated by tabs

        Length of out must be 3 and have to follow this structure:
          user\ttimestamp\t1
        """
        with patch("sys.stdout", new=StringIO()) as out:
            self.mapper.map("0,2,3,4,5,0")

            expected = "2\t1648827850000\t1\n"
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
