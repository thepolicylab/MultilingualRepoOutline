"""
A place to store small, testable utilites
"""
from typing import Optional

import requests

from pyutils.types import FilenameType


def download_file(
    url: str, output_file: FilenameType, session: Optional[requests.Session] = None
):
    """
    Download a file to a location. Note that this function does call
    `requests.Response.raise_for_status()`.

    Args:
        url: The URL to downlod
        output_file: The path to the file to store the downloaded content
        session: Optionally, a Session object to use for the download
    """
    session = session or requests
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_file, "wb") as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)
