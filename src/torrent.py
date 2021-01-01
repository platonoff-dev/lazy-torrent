from pathlib import Path
from typing import Any, Dict

from bencoding import Decoder


class Torrent:
    def __init__(self, filename: str) -> None:
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())
        self.info: Dict[str, Any] = decoder.decode()
