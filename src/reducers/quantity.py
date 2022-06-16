from src.exceptions.data import LineFormatError
from src.reducers.abstracts import Reducer
from src.schemas.data import UserMinMaxMoveMapped


class QuantityReducer(Reducer):
    def parse_line(self, line: str) -> UserMinMaxMoveMapped:
        data = line.split("\t")

        if len(data) != 4:
            raise LineFormatError("Line should have 4 fields", line)

        if not all(map(lambda x: x.isdigit(), data)):
            raise LineFormatError("Line should have only digits", line)

        user_id, diff_ts, max_moves, moves = data

        return UserMinMaxMoveMapped(
            user_id=int(user_id),
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

        print(f"{user.user_id}\t{user.diff_ts}\t{user.max_moves}\t{user.moves}")
