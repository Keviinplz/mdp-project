#!/usr/bin/python3
import sys
import argparse
from typing import Dict, Tuple

from src.mappers import Mapper, UserMapper, QuantityMapper
from src.reducers import Reducer, UserReducer, QuantityReducer


def main():

    AVAILABLE_FLOWS: Dict[str, Tuple[Mapper, Reducer]] = {
        "user": (UserMapper(), UserReducer()),
        "quantity": (QuantityMapper(), QuantityReducer()),
    }

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mapper", type=str)
    group.add_argument("--reducer", type=str)
    args = parser.parse_args()

    flow = AVAILABLE_FLOWS.get(args.mapper or args.reducer)
    if not flow:
        print(
            "Invalid flow, please use one of the following: {}".format(
                ", ".join(AVAILABLE_FLOWS.keys())
            )
        )
        sys.exit(1)

    mapper, reducer = flow

    if args.mapper:
        mapper.run()

    if args.reducer:
        reducer.run()


if __name__ == "__main__":
    main()
