#!/usr/bin/env python
from page_loader.cli import parse_args
from page_loader import download


def main():
    args = parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
