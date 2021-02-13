# coding=utf-8
import re
from os import path, mkdir
from urllib.parse import urlparse

import requests

from bs4 import BeautifulSoup

# poetry run page-loader
# --output /home/agmrv/python-project-lvl3/tmp https://hexlet.io/courses


def generate_filenames(netloc, raw_path) -> str:
    raw_filename = f"{netloc}-{raw_path}"
    filename = normilize_str(raw_filename)
    return f"{filename}.html", f"{filename}_files"


def normilize_str(string: str) -> str:
    parts = re.split(r"[^\da-zA-Z]", string)
    normilized_str = "-".join(filter(None, parts))
    return normilized_str


def download(url, output_path):

    if not path.exists(output_path):
        raise FileExistsError(f"directory '{output_path}' not found")
    elif not path.isdir(output_path):
        raise ValueError(f"'{output_path}' is not a directory")

    parsed_url = urlparse(url)
    netloc, raw_path = parsed_url.netloc, parsed_url.path
    filename, dirname = generate_filenames(netloc, raw_path)
    filepath = path.join(output_path, filename)
    files_dirpath = path.join(output_path, dirname)

    if not path.exists(files_dirpath):
        mkdir(files_dirpath)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    download_resources(soup, files_dirpath, dirname, netloc, url)

    with open(filepath, "w") as file_object:
        file_object.write(soup.prettify())

    return filepath


def download_resources(soup, files_dirpath, dirname, netloc, url):
    imgs = soup.find_all("img")
    for img in imgs:
        src = img.get("src")
        root, ext = path.splitext(src)
        img_filename = "{0}-{1}{2}".format(
            normilize_str(netloc), normilize_str(root), ext
        )
        img_filepath = path.join(files_dirpath, img_filename)

        with open(img_filepath, "wb") as file_object:
            file_object.write(requests.get(url + src).content)

        img["src"] = "{0}/{1}".format(dirname, img_filename)
