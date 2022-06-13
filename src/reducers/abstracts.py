import sys
from typing import Any
from abc import ABC, abstractmethod


class Reducer(ABC):
    def read(self) -> Any:
        for line in sys.stdin:
            line = line.strip()

            self.reduce(line)

    def run(self) -> Any:
        self.read()
        return self.finish()

    @abstractmethod
    def finish(self) -> Any:
        ...

    @abstractmethod
    def reduce(self, data: str) -> Any:
        ...
