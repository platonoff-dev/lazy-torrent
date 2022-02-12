import sys

from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    sys.path.append("src")
