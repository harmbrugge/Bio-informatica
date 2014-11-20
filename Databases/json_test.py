#!/usr/bin/python3
import json
import database


def main():
    print("Content-type: application/json")
    print()

    print(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))


if __name__ == '__main__':
    main()