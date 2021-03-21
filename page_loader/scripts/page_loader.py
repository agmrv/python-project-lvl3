#!/usr/bin/env python

import logging
import sys

from page_loader.cli import parse_args
from page_loader import download


def main():
    args = parse_args()
    try:
        file_path = download(args.url, args.output)
        print(file_path)
    except FileExistsError as exists_error:
        logging.error(exists_error)
        sys.exit(1)
    except ValueError as value_error:
        logging.error(value_error)
        sys.exit(1)


if __name__ == "__main__":
    main()
