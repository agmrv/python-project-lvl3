# coding=utf-8
import re
from os import path, mkdir
from urllib.parse import urlparse

import requests

# from bs4 import BeautifulSoup

# poetry run page-loader
# --output /home/agmrv/python-project-lvl3/tmp https://hexlet.io/courses


def generate_filename(parsed_url) -> str:
    netloc, path = parsed_url.netloc, parsed_url.path
    raw_filename = f"{netloc}-{path}"
    filename = normilize_str(raw_filename)
    return filename

    # root, ext = path.splitext(url)
    # if ext in {'.jpg', '.png'}:
    #     filename = normilize_str(root)
    #     return f'{filename}{ext}'


def normilize_str(string: str) -> str:
    parts = re.split(r"[^\da-zA-Z]", string)
    normilized_str = "-".join(filter(None, parts))
    return normilized_str


def download(url, output_path):

    if not path.exists(output_path):
        raise FileExistsError(f"directory '{output_path}' not found")
    elif not path.isdir(output_path):
        raise ValueError(f"'{output_path}' is not a directory")

    filename = generate_filename(urlparse(url))
    filepath = path.join(output_path, f"{filename}.html")
    dirpath = path.join(output_path, f"{filename}_files")

    response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")

    # imgs = soup.find_all("img")
    # for img in imgs:
    #     print(img.get("src"))
    #     src = img.get("src")
    #     root, ext = path.splitext(url)
    #     img["src"] = generate_filename(netloc, root)

    if not path.exists(dirpath):
        mkdir(dirpath)

    with open(filepath, "w") as file_object:
        file_object.write(response.text)

    return filepath
