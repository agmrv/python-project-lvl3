import re
from os import path
from urllib.parse import urlparse

import requests


def normalize_str(string):
    parts = re.split(r'[^\da-zA-Z]', string)
    # print(re.split(r'[^\da-zA-Z]+', url))
    return '-'.join(parts)


def generate_filename(url):
    parsed_url = urlparse(url)
    normalized_netloc = normalize_str(parsed_url.netloc)
    normalized_path = normalize_str(parsed_url.path)
    filename = f'{normalized_netloc}{normalized_path}.html'
    return filename


def load_page(output_path, url):
    print(output_path, url)

    # poetry run page-loader --output /home/agmrv/python-project-lvl3/tmp https://hexlet.io/courses


    filename = generate_filename(url)

    filepath = path.join(output_path, filename)
