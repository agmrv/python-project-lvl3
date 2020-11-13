import tempfile
from os import path

import pytest
# import requests

from page_loader.io import generate_filename, load_page


test_data = [
    ('https://hexlet.io/courses', 'hexlet-io-courses.html'),
    ('https://hexlet.io/', 'hexlet-io.html'),
    ('https://hexlet.io', 'hexlet-io.html'),
]


@pytest.mark.parametrize('url, expected_filename', test_data)
def test_generate_filename(url, expected_filename):
    assert generate_filename(url) == expected_filename


@pytest.mark.parametrize('url, filename', test_data, ids=['1', '2', '3'])
def test_load_page(url, filename):
    with tempfile.TemporaryDirectory() as temp_dict:
        filepath = path.join(temp_dict, filename)
        load_page(temp_dict, url)
        assert path.exists(filepath)
