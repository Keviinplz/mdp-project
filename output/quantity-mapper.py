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


class QuantityMapper(Mapper):
    @staticmethod
    def calculate_max_moves(min_ts: int, max_ts: int) -> int:
        return ((max_ts - min_ts) // (5 * 60 * 1000)) + 1

    def parse_line(self, line: str) -> UserMinMaxMove:
        data = line.split("\t")

        if len(data) != 3:
            raise LineFormatError("Line should have 3 fields", line)

        user_id, ts, moves = data

        if not user_id.isdigit():
            raise LineFormatError("User id should be an integer", line)

        if not moves.isdigit():
            raise LineFormatError("Moves should be an integer", line)

        ts_info = ts.split("#")

        if len(ts_info) != 2:
            raise LineFormatError("Timestamp should be separated by '#'", line)

        min_ts, max_ts = ts_info

        if not min_ts.isdigit() or not max_ts.isdigit():
            raise LineFormatError("Timestamp should be an integer", line)

        return UserMinMaxMove(
            user_id=int(user_id),
            min_ts=int(min_ts),
            max_ts=int(max_ts),
            moves=int(moves),
        )

    def map(self, line: str) -> None:
        user = self.parse_line(line)
        max_moves: int = self.calculate_max_moves(user.min_ts, user.max_ts)
        print(f"{user.user_id}\t{user.max_ts - user.min_ts}\t{max_moves}\t{user.moves}")


def main():
    mapper = QuantityMapper()
    mapper.run()


if __name__ == "__main__":
    main()
