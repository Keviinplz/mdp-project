from datetime import datetime
from typing import Union

from .abstracts import Reducer

class UserReducer(Reducer):

    current_user: Union[str, None] = None
    current_timestamp: Union[str, None] = None
    current_count: int = 0

    @staticmethod
    def concat_timestamp(current: Union[str, None], new: str) -> str:
        if not current:
            return f"{new}#{new}"

        try:
            dt_new = datetime.strptime(new, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as exc:
            try:
                dt_new = datetime.strptime(new, "%Y-%m-%d %H:%M:%S")
            except ValueError as exc:
                raise ValueError("Invalid new timestamp in reducer function, exiting...") from exc

        data = current.split('#')
        if len(data) != 2:
            raise ValueError("Invalid timestamp in reducer function, exiting...") from ValueError

        _min, _max = data

        dt_min = datetime.strptime(_min, "%Y-%m-%d %H:%M:%S.%f")
        dt_max = datetime.strptime(_max, "%Y-%m-%d %H:%M:%S.%f")
        
        if dt_new <= dt_min:
            return f"{new}#{_min}"

        if dt_new >= dt_max:
            return f"{_max}#{new}"

        return current

    def reduce(self, line: str) -> None:
        user, timestamp, _count = line.split('\t', 2)

        try:
            count = int(_count)
        except ValueError as exc:
            raise ValueError("Invalid count in reducer function, exiting...") from exc

        if user == self.current_user:
            self.current_count += count
            self.current_timestamp = self.concat_timestamp(self.current_timestamp, timestamp)
        else:
            if self.current_user:
            # write result to STDOUT
                print('%s\t%s\t%s' % (self.current_user, self.current_timestamp, self.current_count))
            self.current_count = count
            self.current_user = user
            self.current_timestamp = f"{timestamp}#{timestamp}"

    def finish(self) -> None:
        return
