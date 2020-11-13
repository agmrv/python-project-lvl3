import re
from os import path
from urllib.parse import urlparse

import requests


def generate_filename(url):
    parsed_url = urlparse(url)
    raw_filename = f'{parsed_url.netloc}{parsed_url.path}'
    parts = re.split(r'[^\da-zA-Z]', raw_filename)
    filename = '-'.join(filter(None, parts))
    return f'{filename}.html'


def load_page(output_path, url):
    filename = generate_filename(url)
    filepath = path.join(output_path, filename)

    with open(filepath, 'w') as file_object:
        file_object.write(requests.get(url).text)
