import sys
from typing import Any, TextIO
from abc import ABC, abstractmethod


class Reducer(ABC):

    _source = sys.stdin
    _buffer = ""

    @property
    def source(self) -> TextIO:
        return self._source

    @source.setter
    def source(self, source: TextIO) -> None:
        self._source = source

    def read(self) -> Any:
        for line in self.source:
            line = line.strip()

            self.reduce(line)

    def run(self) -> Any:
        self.read()

        if self._buffer != "":
            print(self._buffer)

    @abstractmethod
    def reduce(self, data: str) -> Any:
        ...
