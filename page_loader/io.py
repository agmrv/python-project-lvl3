import re
from os import path, mkdir
from urllib.parse import urlparse

# from urllib import request

import requests
from bs4 import BeautifulSoup


def download(url, output_path):

    if not path.exists(output_path):
        raise FileExistsError(f"directory '{output_path}' not found")
    elif not path.isdir(output_path):
        raise ValueError(f"'{output_path}' is not a directory")

    parsed_url = urlparse(url)
    netloc = parsed_url.netloc

    filename = generate_filename(netloc, parsed_url.path)
    filepath = path.join(output_path, f"{filename}.html")
    dirpath = path.join(output_path, f"{filename}_files")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    imgs = soup.find_all("img")
    for img in imgs:
        print(img.get("src"))
        # src = img.get("src")
        root, ext = path.splitext(url)
        img["src"] = generate_filename(netloc, root)
    for img in imgs:
        print(img.get("src"))

    if not path.exists(dirpath):
        mkdir(dirpath)

    with open(filepath, "w") as file_object:
        file_object.write(response.text)

    # root, ext = path.splitext(url)
    # if ext in {'.jpg', '.png'}:
    #     filename = normilize_str(root)
    #     return f'{filename}{ext}'

    return filepath


def generate_filename(netloc, some_path):

    raw_filename = f"{netloc}-{some_path}"
    filename = normilize_str(raw_filename)

    return filename


def normilize_str(string):
    parts = re.split(r"[^\da-zA-Z]", string)
    normilized_str = "-".join(filter(None, parts))
    return normilized_str
