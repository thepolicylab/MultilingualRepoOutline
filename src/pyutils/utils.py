"""
A place to store small, testable utilites
"""
import hashlib
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
from contextlib import closing
from pathlib import Path
from typing import Optional

import requests

from pyutils.types import FilenameType

CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache"


_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)


def secure_filename(filename: str) -> str:
    """
    Pass a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    This code is vendored from the werkzeug project available at:

        https://github.com/pallets/werkzeug/

    Args:
        filename: the filename to secure
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename


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


def sha256_of_file(filename: FilenameType) -> str:
    """
    Give a file, return its sha256

    Args:
        filename: the file to compute the sha of
    """
    sha = hashlib.sha256()
    with open(filename, "rb") as infile:
        while chunk := infile.read(8192):
            sha.update(chunk)

    return sha.hexdigest()


def path_from_cache(
    url: str,
    cache_dir: FilenameType = CACHE_DIR,
    session: Optional[requests.Session] = None,
) -> Path:
    """
    Check if the URL has been previously downloaded. If not, download it and store it
    in `cache_dir`. (The default is `__file__.parent.parent.parent / "data" / "cache"`
    which should work if you're using this in the model repository.)

    In either case, return the path to the resultant file.

    Note that this caching function is a little rough and ready. It's totally safe to
    blow out the cache with `rm -rf`.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_db_path = cache_dir / "cache_db.db"
    do_create_db = not cache_db_path.exists()

    filename = secure_filename(url.lower())
    with sqlite3.connect(f"file:///{cache_dir.absolute()}/cache_db.db") as conn:
        with closing(conn.cursor()) as cursor:
            if do_create_db:
                cursor.execute(
                    "CREATE TABLE cache (id INTEGER NOT NULL, url TEXT, sha256 TEXT, PRIMARY KEY (id));"
                )
                conn.commit()

            cursor.execute(
                "SELECT sha256 FROM cache WHERE LOWER(url) = ?", (url.lower(),)
            )
            shas = cursor.fetchall()
            if not shas:
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmppath = Path(tmpdir) / filename
                    download_file(url, tmppath, session=session)
                    sha = sha256_of_file(tmppath)

                    target_dir = cache_dir / sha[:3] / sha
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(tmppath, target_dir / filename)

                cursor.execute(
                    "INSERT INTO cache (url, sha256) VALUES (?, ?)", (url, sha)
                )
                conn.commit()
                cursor.execute(
                    "SELECT sha256 FROM cache WHERE LOWER(url) = ?", (url.lower(),)
                )
                shas = cursor.fetchall()

    sha = shas[0][0]
    return cache_dir / sha[:3] / sha / filename
