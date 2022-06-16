import sys
from typing import TextIO
from abc import ABC, abstractmethod


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
