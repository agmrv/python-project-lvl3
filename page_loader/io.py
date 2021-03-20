# coding=utf-8
import re
from os import path, mkdir
from urllib.parse import urlparse, urljoin

import requests

from bs4 import BeautifulSoup

# poetry run page-loader
# --output /home/agmrv/python-project-lvl3/tmp https://ru.hexlet.io/courses

tags = {"script": "src", "link": "href", "img": "src"}


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
        file_object.write(soup.prettify(formatter="html5"))

    return filepath


def download_resources(soup, files_dirpath, dirname, netloc, url):
    resources = filter(lambda r: is_local(r, url), soup.find_all(tags.keys()))
    for resource in resources:
        src = resource.get(tags.get(resource.name))
        root, ext = path.splitext(src)
        resource_filename = "{0}-{1}{2}".format(
            normilize_str(netloc), normilize_str(root), ext
        )
        resource_filepath = path.join(files_dirpath, resource_filename)

        with open(resource_filepath, "wb") as file_object:
            file_object.write(requests.get(urljoin(url, src)).content)

        resource[tags.get(resource.name)] = "{0}/{1}".format(dirname, resource_filename)


def is_local(element, local_url):
    element_url = urljoin(local_url, element.get(tags.get(element.name)))
    return urlparse(element_url).netloc == urlparse(local_url).netloc
