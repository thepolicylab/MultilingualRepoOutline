import tempfile
from pathlib import Path

from pyutils import utils


class MockRequestsSession:
    def __init__(self, page: str, *args):
        super().__init__()
        self.page = page
        self.num_calls = 0

    def get(self, *args, **kwargs):
        self.num_calls += 1
        return MockResponse(self.page)


class MockResponse:
    def __init__(self, page: str):
        self.page = page

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @staticmethod
    def raise_for_status():
        return None

    @property
    def content(self):
        with open(self.page, "rb") as infile:
            return infile.read()

    def iter_content(self, chunk_size: int = 8192):
        with open(self.page, "rb") as infile:
            while chunk := infile.read(chunk_size):
                yield chunk


def test_secure_filename():
    assert utils.secure_filename("https://google.com/foo") == "https_google.com_foo"


def test_sha256_of_file(fixtures_path: Path):
    assert (
        utils.sha256_of_file(fixtures_path / "example_data.csv")
        == "5b616eaf19684b87104de5c24f7703d439186090c5f58d65608fdf5a47ae6468"
    )


def test_path_from_cache(fixtures_path: Path):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        session = MockRequestsSession(fixtures_path / "example_data.csv")
        answer1 = utils.path_from_cache("https://foobar.com/", tmpdir, session)
        answer2 = utils.path_from_cache("https://foobar.com/", tmpdir, session)

        assert answer1 == answer2
        assert utils.sha256_of_file(answer1) == utils.sha256_of_file(
            fixtures_path / "example_data.csv"
        )
        assert session.num_calls == 1
