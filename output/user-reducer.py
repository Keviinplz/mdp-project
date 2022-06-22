#!/usr/bin/python3
import sys
from abc import ABC, abstractmethod
from typing import Union, TextIO
from dataclasses import dataclass


@dataclass
class UserMoveMapped:
    """
    Data class when UserMove was processed by the mapper
    """

    user_id: str
    timestamp: int
    count: int


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


class UserReducer(Reducer):

    current_user: Union[str, None] = None
    current_min_timestamp: int = 0
    current_max_timestamp: int = 0
    current_count: int = 0

    @property
    def current_timestamp(self) -> str:
        # formatting to 10 characters for timestamp
        out_min_ts : str = str(self.current_min_timestamp).zfill(10)
        out_max_ts : str = str(self.current_max_timestamp).zfill(10)
        return f"{out_min_ts}#{out_max_ts}"

    @property
    def result(self) -> str:
        return "%s\t%s\t%s" % (
            self.current_user,
            self.current_timestamp,
            self.current_count,
        )

    def parse_line(self, line: str) -> UserMoveMapped:
        data = line.split("\t")

        if len(data) != 3:
            raise LineFormatError("Line should be length of 3 separated by tabs", line)

        if not all(map(lambda x: x.isdigit(), data)):
            raise LineFormatError("Line should be all integers", line)

        return UserMoveMapped(
            user_id=data[0], timestamp=int(data[1]), count=int(data[2])
        )

    def set_min_max_ts(self, ts: int) -> None:
        if ts <= self.current_min_timestamp:
            self.current_min_timestamp = ts
        if ts >= self.current_max_timestamp:
            self.current_max_timestamp = ts

    def reduce(self, line: str) -> None:
        data = self.parse_line(line)

        if data.user_id == self.current_user:
            self.current_count += data.count
            self.set_min_max_ts(data.timestamp)
        else:
            if self.current_user is not None:
                print(self.result)
                self._buffer = ""
                self.current_user = None

            self.current_count = data.count
            self.current_user = data.user_id
            self.current_min_timestamp = data.timestamp
            self.current_max_timestamp = data.timestamp
            self._buffer = self.result


def main():
    reducer = UserReducer()
    reducer.run()


if __name__ == "__main__":
    main()
