from typing import List, Union
from datetime import datetime


def str2timestamp(date: str, *, format: List[str]) -> int:
    """
    Converts a datetime string to a timestamp.
    Must to be a datetime string in the format specified in the format argument. (or list of it)
    """
    result: Union[int, None] = None
    for f in format:
        try:
            result = int(datetime.strptime(date, f).timestamp())
        except ValueError:
            pass

    if result is None:
        raise ValueError(f"Could not convert {date} to timestamp")

    return result
