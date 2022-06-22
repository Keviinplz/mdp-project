#!/usr/bin/python3
import sys
from abc import ABC, abstractmethod
from typing import List, Union, TextIO
from datetime import datetime
from dataclasses import dataclass

@dataclass
class UserMinMaxMoveReduced:
    """
    Data class when UserMinMaxMove was processed by the reducer
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


class MovesSorterMapper(Mapper):
    def parse_line(self, line: str) -> UserMinMaxMoveReduced:
        data = line.split("\t")

        if len(data) != 4:
            raise LineFormatError("Line should have 4 fields", line)

        user_id, diff_ts, max_moves, moves = data

        if not user_id.isdigit():
            raise LineFormatError("User id should be an integer", line)
        
        if not diff_ts.isdigit():
            raise LineFormatError("Timestamp should be an integer", line)
        
        if not max_moves.isdigit():
            raise LineFormatError("Moves should be an integer", line)

        if not moves.isdigit():
            raise LineFormatError("Moves should be an integer", line)

        return UserMinMaxMoveReduced(
            user_id=user_id,
            diff_ts=int(diff_ts),
            max_moves=int(max_moves),
            moves=int(moves),
        )

    def map(self, line: str) -> None:
        user = self.parse_line(line)
        # formatting to 10 characters for timestamp
        ts_diff : str = str(user.diff_ts).zfill(10)
        print(f"{user.moves}\t{user.user_id}\t{ts_diff}\t{user.max_moves}")


def main():
    mapper = MovesSorterMapper()
    mapper.run()


if __name__ == "__main__":
    main()
