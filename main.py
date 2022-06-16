#!/usr/bin/python3
import argparse
import sys
from typing import Dict, Tuple

from src.mappers.abstracts import Mapper
from src.mappers.user import UserMapper
from src.reducers.abstracts import Reducer
from src.reducers.user import UserReducer


def main():

    AVAILABLE_FLOWS: Dict[str, Tuple[Mapper, Reducer]] = {
        "user": (UserMapper(), UserReducer())
    }

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mapper", type=str)
    group.add_argument("--reducer", type=str)
    args = parser.parse_args()

    flow = AVAILABLE_FLOWS.get(args.mapper or args.reducer)
    if not flow:
        print("Invalid flow, please use one of the following: {}".format(", ".join(AVAILABLE_FLOWS.keys())))
        sys.exit(1)
    
    mapper, reducer = flow
    
    if args.mapper:
        mapper.run()

    if args.reducer:
        reducer.run()

if __name__ == "__main__":
    main()
