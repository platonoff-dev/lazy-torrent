from pathlib import Path
from typing import Any, Dict, Union

from bencoding import Decoder


class Torrent:
    def __init__(self, filename: Union[str, Path]) -> None:
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())
        self.info: Dict[str, Any] = decoder.decode()

    @property
    def size(self) -> int:
        files = self.info["info"].get("files") or [self.info["info"]["file"]]
        sizes = [file["length"] for file in files]
        return sum(sizes)

    def download(self) -> None:
        pass
