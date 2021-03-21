# coding=utf-8
import re
import logging
from os import path, mkdir
from urllib.parse import urlparse, urljoin

import requests

from bs4 import BeautifulSoup

# poetry run page-loader
# --output /home/agmrv/python-project-lvl3/tmp https://ru.hexlet.io/courses

logging.basicConfig(level=logging.INFO)

tags = {"script": "src", "link": "href", "img": "src"}


def generate_filename(netloc, raw_path) -> str:
    raw_filename = f"{netloc}-{raw_path}"
    filename = normilize_str(raw_filename)
    return filename


def normilize_str(string: str) -> str:
    parts = re.split(r"[^\da-zA-Z]", string)
    normilized_str = "-".join(filter(None, parts))
    return normilized_str


def download(url, output_path):
    logging.info("Начата загрузка страницы.")

    if not path.exists(output_path):
        raise FileExistsError(f"directory '{output_path}' not found")
    elif not path.isdir(output_path):
        raise ValueError(f"'{output_path}' is not a directory")

    parsed_url = urlparse(url)
    netloc, raw_path = parsed_url.netloc, parsed_url.path
    name = generate_filename(netloc, raw_path)
    filename, dirname = f"{name}.html", f"{name}_files"
    filepath = path.join(output_path, filename)
    files_dirpath = path.join(output_path, dirname)

    if not path.exists(files_dirpath):
        mkdir(files_dirpath)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    download_resources(soup, files_dirpath, dirname, netloc, url)
    with open(filepath, "w") as file_object:
        file_object.write(soup.prettify(formatter="html5"))

    logging.info("Загрузка страницы завершена.")
    return filepath


def download_resources(soup, files_dirpath, dirname, netloc, url):
    resources = filter(lambda r: is_local(r, url), soup.find_all(tags.keys()))

    logging.info("Начата загрузка ресурсов страницы.")

    for resource in resources:
        src = resource.get(tags.get(resource.name))
        if not src:
            continue
        root, ext = path.splitext(src)
        resource_filename = "{0}-{1}{2}".format(
            normilize_str(netloc),
            normilize_str(urlparse(root).path),
            ext or ".html",
        )
        resource[tags.get(resource.name)] = "{0}/{1}".format(
            dirname,
            resource_filename,
        )

        if not ext:
            continue

        resource_filepath = path.join(files_dirpath, resource_filename)
        with open(resource_filepath, "wb") as file_object:
            file_object.write(requests.get(urljoin(url, src)).content)

    logging.info("Загрузка ресурсов страницы завершена.")


def is_local(element, local_url):
    element_url = urljoin(local_url, element.get(tags.get(element.name)))
    return urlparse(element_url).netloc == urlparse(local_url).netloc
