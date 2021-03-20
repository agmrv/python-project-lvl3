# coding=utf-8
import tempfile
from os import path
from urllib.parse import urlparse, urljoin

import requests
import pytest
import requests_mock
from bs4 import BeautifulSoup

from page_loader.io import generate_filenames, download


def read_html(path: str) -> str:
    with open(path, "r") as html:
        return html.read()


def read_img(path: str) -> bytes:
    with open(path, "rb") as img:
        return img.read()


test_filenames_data = [
    (
        "https://hexlet.io/courses/",
        ("hexlet-io-courses.html", "hexlet-io-courses_files"),
    ),
    ("https://ru.hexlet.io/", ("ru-hexlet-io.html", "ru-hexlet-io_files")),
    (
        "https://ru.hexlet.io/courses",
        ("ru-hexlet-io-courses.html", "ru-hexlet-io-courses_files"),
    ),
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
        ],
    ),
]


@pytest.mark.parametrize("url, expected_filenames", test_filenames_data)
def test_generate_filename(url, expected_filenames):
    parsed_url = urlparse(url)
    netloc, raw_path = parsed_url.netloc, parsed_url.path
    assert generate_filenames(netloc, raw_path) == expected_filenames


@pytest.mark.parametrize(
    "url, filenames",
    test_filenames_data,
)
def test_create_file_and_directory(url, filenames):
    with tempfile.TemporaryDirectory() as temp_dir:
        filename, dirname = filenames
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
def test_download_page_content(
    url, page_before, page_after, expected_content_paths, srcs
):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(url, text=page_before)

            for src, expected_content in srcs:
                mock.get(urljoin(url, src), content=expected_content)

            filepath = download(url, temp_dir)
            soup = BeautifulSoup(page_after, "html.parser")
            with open(filepath, "r") as downloaded_page:
                assert downloaded_page.read() == soup.prettify(formatter="html5")

            for content_path, expected_file in expected_content_paths:
                filepath = path.join(temp_dir, content_path)
                assert path.exists(filepath)

                with open(filepath, "rb") as file_object:
                    assert file_object.read() == expected_file


some_content = bytes(123)
tags = {"script": "src", "link": "href", "img": "src"}
srcs = [
    (
        "/tests/fixtures/pizza-slice.png",
        read_img("tests/fixtures/pizza-slice.png"),
    ),
    (
        "/tests/fixtures/robin.jpg",
        read_img("tests/fixtures/robin.jpg"),
    ),
    (
        "https://cdn2.hexlet.io/assets/menu.css",
        some_content,
    ),
    (
        "/assets/aplication.css",
        some_content,
    ),
    (
        "/courses",
        some_content,
    ),
    (
        "/professions/nodejs",
        some_content,
    ),
    (
        "https://js.stripe.com/v3/",
        some_content,
    ),
    (
        "https://ru.hexlet.io/packs/js/runtime.js",
        some_content,
    ),
]

with tempfile.TemporaryDirectory() as temp_dir:

    with requests_mock.Mocker() as mock:
        for src, expected_content in srcs:
            mock.get(
                urljoin("https://ru.hexlet.io/courses", src), content=expected_content
            )

        mock.get(
            "https://ru.hexlet.io/courses",
            text=read_html("tests/fixtures/complex_page_before.html"),
        )

        filepath = download("https://ru.hexlet.io/courses", temp_dir)

        soup = BeautifulSoup(
            read_html("tests/fixtures/complex_page_after.html"), "html.parser"
        )

        with open(filepath, "r") as downloaded_page:
            print(downloaded_page.read())
            print("\n")
            print(soup.prettify(formatter="html5"))
            assert downloaded_page.read() == soup.prettify(formatter="html5")
