import sys
from typing import Any
from abc import ABC, abstractmethod


class Mapper(ABC):
    def read(self) -> Any:
        for line in sys.stdin:
            line = line.strip()

            self.map(line)

    def run(self) -> Any:
        self.read()

    @abstractmethod
    def map(self, line: str) -> Any:
        ...
