from dataclasses import dataclass


@dataclass
class UserMove:
    """
    Data class for a user move in r/place canvas
    """

    timestamp: int
    user_id: int
    x: int
    y: int
    color: int
    is_mod: bool


@dataclass
class UserMoveMapped:
    """
    Data class when UserMove was processed by the mapper
    """

    user_id: int
    timestamp: int
    count: int


@dataclass
class UserMinMaxMove:
    """
    Data class for a user with min ts and max ts, and number of move that the user made
    """

    user_id: int
    min_ts: int
    max_ts: int
    moves: int
