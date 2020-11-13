#!/usr/bin/env python
from page_loader.cli import parse_args
from page_loader.io import load_page


def main():
    args = parse_args()
    load_page(args.output, args.url)


if __name__ == '__main__':
    main()
