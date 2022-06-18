#!/usr/bin/python3
import sys
from abc import ABC, abstractmethod
from typing import Union, TextIO
from dataclasses import dataclass


@dataclass
class UserMinMaxMoveMapped:
    """
    Data class when UserMinMaxMove was processed by the mapper
    """

    user_id: str
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


class Reducer(ABC):

    _source = sys.stdin
    _buffer = ""

    @property
    def source(self) -> TextIO:
        return self._source

    @source.setter
    def source(self, source: TextIO) -> None:
        self._source = source

    def read(self) -> None:
        for line in self.source:
            line = line.strip()

            self.reduce(line)

    def run(self) -> None:
        self.read()

        if self._buffer != "":
            print(self._buffer)

    @abstractmethod
    def reduce(self, data: str) -> None:
        ...


class QuantityReducer(Reducer):
    def parse_line(self, line: str) -> UserMinMaxMoveMapped:
        data = line.split("\t")

        if len(data) != 4:
            raise LineFormatError("Line should have 4 fields", line)

        if not all(map(lambda x: x.isdigit(), data)):
            raise LineFormatError("Line should have only digits", line)

        user_id, diff_ts, max_moves, moves = data

        return UserMinMaxMoveMapped(
            user_id=user_id,
            diff_ts=int(diff_ts),
            max_moves=int(max_moves),
            moves=int(moves),
        )

    def reduce(self, line: str) -> None:
        user = self.parse_line(line)

        if user.diff_ts == 0 or user.max_moves - user.moves > 2:
            return

        if user.moves < 5:
            return

        out_ts : str = str(user.diff_ts).zfill(10)
        print(f"{user.user_id}\t{out_ts}\t{user.max_moves}\t{user.moves}")


def main():
    reducer = QuantityReducer()
    reducer.run()


if __name__ == "__main__":
    main()
