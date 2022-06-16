from typing import List, Union

from src.lib.utils import str2timestamp
from src.mappers.abstracts import Mapper
from src.exceptions.data import LineFormatError
from src.schemas.data import UserMove


class UserMapper(Mapper):
    in_sep: str = ","
    out_sep: str = "\t"
    ts_sep: str = "#"
    first_time: str = "2022-04-01 12:44:10.315"
    DATETIME_FORMAT_STRING: List[str] = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]

    def __init__(self):
        # set the first timestamp from the string as seconds
        self.first_ts = str2timestamp(
            self.first_time, format=self.DATETIME_FORMAT_STRING
        )
        # now to miliseconds
        self.first_ts *= 1000

    def parse_line(self, line: str) -> Union[UserMove, None]:
        data = line.split(self.in_sep)
        if not len(data) == 6:
            raise LineFormatError("Line should have 6 fields", line)

        if all(not x.isdigit() for x in data):
            return None

        if not all(x.isdigit() for x in data):
            raise LineFormatError(
                "All fields should be all integers or all strings", line
            )

        return UserMove(
            timestamp=int(data[0]) + self.first_ts,
            user_id=int(data[1]),
            x=int(data[2]),
            y=int(data[3]),
            color=int(data[4]),
            is_mod=bool(int(data[5])),
        )

    def map(self, line: str) -> None:
        move = self.parse_line(line)

        if not move or move.is_mod:
            return

        print(f"{move.user_id}\t{move.timestamp}\t1")
