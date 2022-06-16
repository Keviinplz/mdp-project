from src.exceptions.data import LineFormatError
from src.mappers.abstracts import Mapper
from src.schemas.data import UserMinMaxMove


class QuantityMapper(Mapper):
    @staticmethod
    def calculate_max_moves(min_ts: int, max_ts: int) -> int:
        return ((max_ts - min_ts) // (5 * 60 * 1000)) + 1

    def parse_line(self, line: str) -> UserMinMaxMove:
        data = line.split("\t")

        if len(data) != 3:
            raise LineFormatError("Line should have 3 fields", line)

        user_id, ts, moves = data

        if not user_id.isdigit():
            raise LineFormatError("User id should be an integer", line)

        if not moves.isdigit():
            raise LineFormatError("Moves should be an integer", line)

        ts_info = ts.split("#")

        if len(ts_info) != 2:
            raise LineFormatError("Timestamp should be separated by '#'", line)

        min_ts, max_ts = ts_info

        if not min_ts.isdigit() or not max_ts.isdigit():
            raise LineFormatError("Timestamp should be an integer", line)

        return UserMinMaxMove(
            user_id=int(user_id),
            min_ts=int(min_ts),
            max_ts=int(max_ts),
            moves=int(moves),
        )

    def map(self, line: str) -> None:
        user = self.parse_line(line)
        max_moves: int = self.calculate_max_moves(user.min_ts, user.max_ts)
        print(f"{user.user_id}\t{user.max_ts - user.min_ts}\t{max_moves}\t{user.moves}")
