#!/usr/bin/env python
from page_loader.cli import parse_args
from page_loader import download


def main():
    args = parse_args()
    try:
        file_path = download(args.url, args.output)
        print(file_path)
    except FileExistsError as exists_error:
        print(exists_error)
    except ValueError as value_error:
        print(value_error)
    # else:
    #     print(file_path)


if __name__ == "__main__":
    main()
