# coding=utf-8
import tempfile
from os import path
from urllib.parse import urlparse

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
        "https://hexlet.io/courses",
        ("hexlet-io-courses.html", "hexlet-io-courses_files"),
    ),
    (
        "https://hexlet.io/courses/",
        ("hexlet-io-courses.html", "hexlet-io-courses_files"),
    ),
    ("https://hexlet.io/", ("hexlet-io.html", "hexlet-io_files")),
    ("https://hexlet.io", ("hexlet-io.html", "hexlet-io_files")),
    (
        "https://ru.hexlet.io/courses",
        ("ru-hexlet-io-courses.html", "ru-hexlet-io-courses_files"),
    ),
]

test_page_data = [
    (
        "https://ru.hexlet.io/courses",
        read_html("tests/fixtures/page_before.html"),
        read_html("tests/fixtures/page_after.html"),
    ),
]

test_content_data = [
    (
        "https://ru.hexlet.io/courses",
        read_html("tests/fixtures/page_before.html"),
        [
            (
                "ru-hexlet-io-courses_files/ru-hexlet-io-courses-pizza-slice.png",
                read_img("tests/fixtures/pizza-slice.png"),
            ),
            (
                "ru-hexlet-io-courses_files/ru-hexlet-io-courses-robin.jpg",
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


# @pytest.mark.parametrize(
#     "url, filenames",
#     test_filenames_data,
#     ids=[
#         "test_data1",
#         "test_data2",
#         "test_data3",
#         "test_data4",
#         "test_data5",
#     ],
# )
# def test_create_file_and_directory(url, filenames):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         filename, dirname = filenames
#         expected_filepath = path.join(temp_dir, filename)
#         expected_dirpath = path.join(temp_dir, dirname)
#         filepath = download(url, temp_dir)
#         assert filepath == expected_filepath
#         assert path.exists(expected_filepath)
#         assert path.exists(expected_dirpath)


@pytest.mark.parametrize(
    "url, page_before, page_after",
    test_page_data,
    ids=["test"],
)
def test_download_page(url, page_before, page_after):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(url, text=page_before)
            filepath = download(url, temp_dir)
            soup = BeautifulSoup(page_after, "html.parser")
            with open(filepath, "r") as content:
                assert content.read() == soup.prettify()


# @pytest.mark.parametrize(
#     "url, page_before, expected_content_paths, srcs",
#     test_content_data,
# )
# def test_download_page_content(url, page_before, expected_content_paths, srcs):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         with requests_mock.Mocker() as mock:
#             mock.get(url, text=page_before)

#             for src, expected_content in srcs:
#                 mock.get(url + src, content=expected_content)

#             download(url, temp_dir)

#             for content_path, expected_file in expected_content_paths:
#                 filepath = path.join(temp_dir, content_path)
#                 assert path.exists(filepath)

#                 with open(filepath, "rb") as file_object:
#                     assert file_object.read() == expected_file


# @requests_mock.Mocker()
# def test_function(m):
#     m.get(
#         "https://ru.hexlet.io/courses",
#         text=read_html("tests/fixtures/page_before.html"),
#     )
#     m.get(
#         "https://ru.hexlet.io/courses/tests/fixtures/pizza-slice.png",
#         content=read_img("tests/fixtures/pizza-slice.png"),
#     )
#     m.get(
#         "https://ru.hexlet.io/courses/tests/fixtures/robin.jpg",
#         content=read_img("tests/fixtures/robin.jpg"),
#     )

#     return download(
#         "https://ru.hexlet.io/courses", "/home/agmrv/python-project-lvl3/tmp"
#     )


# print(test_function())
