from typing import Union

from src.exceptions.data import LineFormatError
from src.reducers.abstracts import Reducer
from src.schemas.data import UserMoveMapped


class UserReducer(Reducer):

    current_user: Union[int, None] = None
    current_min_timestamp: int = 0
    current_max_timestamp: int = 0
    current_count: int = 0

    @property
    def current_timestamp(self) -> str:
        return f"{self.current_min_timestamp}#{self.current_max_timestamp}"

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
            user_id=int(data[0]), timestamp=int(data[1]), count=int(data[2])
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
