#!/usr/bin/python3
import argparse
from src.mappers import CountMapper, UserMapper
from src.reducers import CountReducer, UserReducer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapper", action="store_true")
    parser.add_argument("--reducer", action="store_true")
    parser.add_argument("--placemapper", action="store_true")
    parser.add_argument("--placereducer", action="store_true")

    args = parser.parse_args()

    if not (bool(args.mapper) ^ bool(args.reducer)):
        if not (bool(args.placemapper) ^ bool(args.placereducer)):
            print("Please specify either --mapper or --reducer")
            return

    if args.mapper:
        mapper = CountMapper()
        mapper.run()

    if args.reducer:
        reducer = CountReducer()
        reducer.run()
        
    if args.placemapper:
        mapper = UserMapper()
        mapper.run()

    if args.placereducer:
        reducer = UserReducer()
        reducer.run()


if __name__ == "__main__":
    main()
