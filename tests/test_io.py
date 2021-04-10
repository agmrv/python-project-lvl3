# coding=utf-8
import tempfile
from os import path
from urllib.parse import urlparse, urljoin

import pytest
import requests_mock
from bs4 import BeautifulSoup

from page_loader.io import generate_filename, download


def read_html(path: str) -> str:
    with open(path, "r") as html:
        return html.read()


def read_img(path: str) -> bytes:
    with open(path, "rb") as img:
        return img.read()


test_filenames_data = [
    ("https://hexlet.io/courses/", "hexlet-io-courses"),
    ("https://ru.hexlet.io/", "ru-hexlet-io"),
    ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses"),
]

test_download_data = [
    (
        "https://ru.hexlet.io/courses/",
        read_html("tests/fixtures/page_before.html"),
        read_html("tests/fixtures/page_after.html"),
        [
            (
                "ru-hexlet-io-courses_files/ru-hexlet-io-tests-fixtures-pizza-slice.png",
                read_img("tests/fixtures/pizza-slice.png"),
            ),
            (
                "ru-hexlet-io-courses_files/ru-hexlet-io-tests-fixtures-robin.jpg",
                read_img("tests/fixtures/robin.jpg"),
            ),
        ],
        [
            (
                "/tests/fixtures/pizza-slice.png",
                read_img("tests/fixtures/pizza-slice.png"),
            ),
            (
                "/tests/fixtures/robin.jpg",
                read_img("tests/fixtures/robin.jpg"),
            ),
            ("https://cdn2.hexlet.io/assets/menu.css", ""),
            ("/assets/application.css", ""),
            ("/courses", ""),
            ("/assets/professions/nodejs.png", ""),
            ("/professions/nodejs", ""),
            ("https://js.stripe.com/v3/", ""),
            ("https://ru.hexlet.io/packs/js/runtime.js", ""),
        ],
    ),
]


@pytest.mark.parametrize("url, expected_filenames", test_filenames_data)
def test_generate_filename(url, expected_filenames):
    parsed_url = urlparse(url)
    netloc, raw_path = parsed_url.netloc, parsed_url.path
    assert generate_filename(netloc, raw_path) == expected_filenames


@pytest.mark.parametrize(
    "url, name",
    test_filenames_data,
)
def test_create_file_and_directory(url, name):
    with tempfile.TemporaryDirectory() as temp_dir:
        filename, dirname = f"{name}.html", f"{name}_files"
        expected_filepath = path.join(temp_dir, filename)
        expected_dirpath = path.join(temp_dir, dirname)

        with requests_mock.Mocker() as mock:
            mock.get(url)
            filepath = download(url, temp_dir)
            assert filepath == expected_filepath
            assert path.exists(expected_filepath)
            assert path.exists(expected_dirpath)


@pytest.mark.parametrize(
    "url, page_before, page_after, expected_content_paths, srcs",
    test_download_data,
    ids=["test"],
)
def test_download_page(url, page_before, page_after, expected_content_paths, srcs):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            for src, expected_content in srcs:
                if expected_content:
                    mock.get(urljoin(url, src), content=expected_content)
                else:
                    mock.get(urljoin(url, src))

            mock.get(url, text=page_before)

            filepath = download(url, temp_dir)
            expected_soup = BeautifulSoup(page_after, "html.parser")
            with open(filepath, "r") as downloaded_page:
                soup = BeautifulSoup(downloaded_page.read(), "html.parser")
                assert soup.prettify(formatter="html5") == expected_soup.prettify(
                    formatter="html5"
                )

            for content_path, expected_file in expected_content_paths:
                filepath = path.join(temp_dir, content_path)
                assert path.exists(filepath)

                with open(filepath, "rb") as file_object:
                    assert file_object.read() == expected_file
