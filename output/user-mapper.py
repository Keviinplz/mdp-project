#!/usr/bin/python3
import sys
from abc import ABC, abstractmethod
from typing import List, Union, TextIO
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserMove:
    """
    Data class for a user move in r/place canvas
    """

    timestamp: int
    user_id: int
    x: int
    y: int
    color: int
    is_mod: bool


@dataclass
class UserMoveMapped:
    """
    Data class when UserMove was processed by the mapper
    """

    user_id: int
    timestamp: int
    count: int


@dataclass
class UserMinMaxMove:
    """
    Data class for a user with min ts and max ts, and number of move that the user made
    """

    user_id: int
    min_ts: int
    max_ts: int
    moves: int


@dataclass
class UserMinMaxMoveMapped:
    """
    Data class when UserMinMaxMove was processed by the mapper
    """

    user_id: int
    diff_ts: int
    max_moves: int
    moves: int


class DataError(Exception):
    """Raises when there was an error trying to process data"""

    def __init__(self, message: str, data: str):
        self.data = data
        super().__init__(message)


class TimestampParseError(DataError):
    """Raises when there was an error trying to parse a timestamp"""

    def __init__(self, message: str, data: str):
        super().__init__(message, data)


class LineFormatError(DataError):
    """Raises when there was an error trying to parse a line"""

    def __init__(self, message: str, data: str):
        super().__init__(message, data)


class Mapper(ABC):

    _source = sys.stdin

    @property
    def source(self) -> TextIO:
        return self._source

    @source.setter
    def source(self, source: TextIO) -> None:
        self._source = source

    def read(self) -> None:
        for line in self.source:
            line = line.strip()
            if not line:
                return
            self.map(line)

    def run(self) -> None:
        self.read()

    @abstractmethod
    def map(self, line: str) -> None:
        ...


def str2timestamp(date: str, *, format: List[str]) -> int:
    """
    Converts a datetime string to a timestamp.
    Must to be a datetime string in the format specified in the format argument. (or list of it)
    """
    result: Union[int, None] = None
    for f in format:
        try:
            result = int(datetime.strptime(date, f).timestamp())
        except ValueError:
            pass

    if result is None:
        raise ValueError(f"Could not convert {date} to timestamp")

    return result


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


def main():
    mapper = UserMapper()
    mapper.run()


if __name__ == "__main__":
    main()
