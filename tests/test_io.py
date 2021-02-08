import tempfile
from os import path
from urllib.parse import urlparse
import pytest

# import requests

from page_loader.io import generate_filename, download


test_data = [
    ("https://hexlet.io/courses", "hexlet-io-courses.html"),
    ("https://hexlet.io/", "hexlet-io.html"),
    ("https://hexlet.io", "hexlet-io.html"),
]


@pytest.mark.parametrize("url,expected_filename", test_data)
def test_generate_filename(url, expected_filename):
    assert generate_filename(urlparse(url)) == expected_filename


<<<<<<< HEAD
# @pytest.mark.parametrize('url, filename', test_data, ids=['test_data1', 'test_data2', 'test_data3'])
=======
@pytest.mark.parametrize('url, filename', test_data, ids=['test_data1', 'test_data2', 'test_data3'])
>>>>>>> e8b3948c353975dcde3df6224d3bd0283a391d3b
def test_download(url, filename):
    with tempfile.TemporaryDirectory() as temp_dict:
        filepath = path.join(temp_dict, filename)
        download(temp_dict, url)
        assert path.exists(filepath)
<<<<<<< HEAD

test_text
=======
>>>>>>> e8b3948c353975dcde3df6224d3bd0283a391d3b
