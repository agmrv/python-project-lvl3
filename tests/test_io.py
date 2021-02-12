# coding=utf-8
import tempfile
from os import path
from urllib.parse import urlparse

import pytest
import requests_mock

from page_loader.io import generate_filename, download


test_data = [
    ("https://hexlet.io/courses", "hexlet-io-courses"),
    ("https://hexlet.io/courses/", "hexlet-io-courses"),
    ("https://hexlet.io/", "hexlet-io"),
    ("https://hexlet.io", "hexlet-io"),
    ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses"),
]


content_test_data = [
    ("https://hexlet.io/courses", "hexlet-io-courses"),
    ("https://hexlet.io/courses/", "hexlet-io-courses"),
    ("https://hexlet.io/", "hexlet-io"),
    ("https://hexlet.io", "hexlet-io"),
    ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses"),
]


@pytest.mark.parametrize("url,expected_filename", test_data)
def test_generate_filename(url, expected_filename):
    assert generate_filename(urlparse(url)) == expected_filename


@pytest.mark.parametrize(
    "url, filename",
    test_data,
    ids=["test_data1", "test_data2", "test_data3", "test_data4", "test_data5"],
)
def test_create_file_and_directory(url, filename):
    with tempfile.TemporaryDirectory() as temp_dir:
        expected_filepath = path.join(temp_dir, filename + ".html")
        expected_dirpath = path.join(temp_dir, filename + "_files")
        filepath = download(url, temp_dir)
        assert filepath == expected_filepath
        assert path.exists(expected_filepath)
        assert path.exists(expected_dirpath)


@pytest.mark.parametrize("url, expected_content", content_test_data)
def test_dowload_page_content(url, expected_content):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(url, text=expected_content)
            filepath = download(url, temp_dir)
            with open(filepath, "r") as content:
                assert content.read() == expected_content
