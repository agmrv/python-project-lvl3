import argparse
import os


def parse_args():
    """Parse and return the args from CLI.
    Returns:
        the arguments from CLI
    """
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '--output',
        default=os.getcwd(),
        help='set the output path',
        metavar='PATH',
        dest='output',
    )

    return parser.parse_args()
